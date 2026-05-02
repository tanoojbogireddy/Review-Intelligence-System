"""
server.py
---------
RIAS FastAPI backend.

Exposes:
  POST /api/analyze   — accepts a CSV upload, runs the full pipeline,
                        returns JSON insights + processed rows
  GET  /api/health    — liveness check

Run with:
    uvicorn server:app --reload --port 8000
"""

from __future__ import annotations

import io
import json
from typing import Any

import pandas as pd
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from pipeline.preprocessor import preprocess
from pipeline.sentiment import analyze_sentiment
from pipeline.classifier import classify_category
from pipeline.aggregator import aggregate_insights
from pipeline.recommender import generate_recommendations
from utils.io_helpers import load_csv
from utils.validators import validate_dataframe
from config.settings import USE_LLM

# ── App setup ─────────────────────────────────────────────────────────────────
app = FastAPI(
    title="RIAS API",
    description="Review Intelligence Automation System — AI-powered review analytics",
    version="1.0.0",
)

# Allow the Vite dev server (port 5173) and any localhost origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://localhost:4173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Health check ──────────────────────────────────────────────────────────────
@app.get("/api/health")
def health():
    return {"status": "ok", "engine": "llm" if USE_LLM else "rule-based"}


# ── Main analysis endpoint ────────────────────────────────────────────────────
@app.post("/api/analyze")
async def analyze(file: UploadFile = File(...)) -> JSONResponse:
    """
    Accept a CSV upload and return full pipeline results as JSON.

    The response schema:
    {
      "rows": [...],           // processed review rows (list of dicts)
      "insights": {
        "total_reviews": int,
        "negative_pct": float,
        "top_negative_issue": str,
        "category_counts": {category: count, ...},
        "sentiment_counts": {sentiment: count, ...},
        "category_sentiment": {category: {Positive: n, Neutral: n, Negative: n}, ...},
        "avg_score_by_cat": [{category, avg_sentiment_score}, ...],
        "trend_data": [{month, total, negative}, ...] | null,
      },
      "recommendations": [
        {rank, category, negative_count, share_pct, actions, priority},
        ...
      ]
    }
    """
    # ── Read upload ───────────────────────────────────────────────────────────
    try:
        contents = await file.read()
        raw_df = load_csv(io.BytesIO(contents))
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Could not read CSV: {exc}")

    # ── Validate ──────────────────────────────────────────────────────────────
    is_valid, err_msg = validate_dataframe(raw_df)
    if not is_valid:
        raise HTTPException(status_code=422, detail=err_msg)

    # ── Run pipeline ──────────────────────────────────────────────────────────
    try:
        df = preprocess(raw_df)
        df = analyze_sentiment(df)
        df = classify_category(df)
        insights = aggregate_insights(df)
        recs = generate_recommendations(df, insights, top_n=3)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Pipeline error: {exc}")

    # ── Serialise ─────────────────────────────────────────────────────────────
    # Convert pandas Timestamps → ISO strings so JSON serialisation works
    rows_df = df.copy()
    for col in rows_df.select_dtypes(include=["datetime64[ns]", "datetimetz"]).columns:
        rows_df[col] = rows_df[col].astype(str)
    rows = rows_df.where(pd.notna(rows_df), None).to_dict(orient="records")

    def _series_to_dict(s: pd.Series) -> dict:
        return {str(k): int(v) for k, v in s.items()}

    category_sentiment_raw = insights["category_sentiment"]
    cat_sent_dict: dict[str, dict] = {}
    for cat in category_sentiment_raw.index:
        cat_sent_dict[cat] = {
            col: int(category_sentiment_raw.loc[cat, col])
            for col in category_sentiment_raw.columns
        }

    trend: list | None = None
    if insights["trend_data"] is not None:
        trend = insights["trend_data"].to_dict(orient="records")

    payload = {
        "rows": rows,
        "insights": {
            "total_reviews":      insights["total_reviews"],
            "negative_pct":       insights["negative_pct"],
            "top_negative_issue": insights["top_negative_issue"],
            "category_counts":    _series_to_dict(insights["category_counts"]),
            "sentiment_counts":   _series_to_dict(insights["sentiment_counts"]),
            "category_sentiment": cat_sent_dict,
            "avg_score_by_cat":   insights["avg_score_by_cat"].to_dict(orient="records"),
            "trend_data":         trend,
        },
        "recommendations": recs,
    }

    return JSONResponse(content=payload)


# ── Sample data endpoint ──────────────────────────────────────────────────────
@app.get("/api/sample")
def get_sample() -> JSONResponse:
    """Run the pipeline on the built-in sample CSV and return results."""
    try:
        raw_df = load_csv("data/sample_reviews.csv")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Sample data file not found.")

    is_valid, err_msg = validate_dataframe(raw_df)
    if not is_valid:
        raise HTTPException(status_code=422, detail=err_msg)

    df = preprocess(raw_df)
    df = analyze_sentiment(df)
    df = classify_category(df)
    insights = aggregate_insights(df)
    recs = generate_recommendations(df, insights, top_n=3)

    rows_df = df.copy()
    for col in rows_df.select_dtypes(include=["datetime64[ns]", "datetimetz"]).columns:
        rows_df[col] = rows_df[col].astype(str)
    rows = rows_df.where(pd.notna(rows_df), None).to_dict(orient="records")

    def _series_to_dict(s: pd.Series) -> dict:
        return {str(k): int(v) for k, v in s.items()}

    category_sentiment_raw = insights["category_sentiment"]
    cat_sent_dict: dict[str, dict] = {}
    for cat in category_sentiment_raw.index:
        cat_sent_dict[cat] = {
            col: int(category_sentiment_raw.loc[cat, col])
            for col in category_sentiment_raw.columns
        }

    trend = None
    if insights["trend_data"] is not None:
        trend = insights["trend_data"].to_dict(orient="records")

    return JSONResponse(content={
        "rows": rows,
        "insights": {
            "total_reviews":      insights["total_reviews"],
            "negative_pct":       insights["negative_pct"],
            "top_negative_issue": insights["top_negative_issue"],
            "category_counts":    _series_to_dict(insights["category_counts"]),
            "sentiment_counts":   _series_to_dict(insights["sentiment_counts"]),
            "category_sentiment": cat_sent_dict,
            "avg_score_by_cat":   insights["avg_score_by_cat"].to_dict(orient="records"),
            "trend_data":         trend,
        },
        "recommendations": recs,
    })
