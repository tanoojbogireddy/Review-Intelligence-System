"""
pipeline/aggregator.py
----------------------
Aggregation layer — turns the enriched per-review dataframe into
business-level summary statistics.

Produces:
  1. category_counts     → pd.Series  — review count per category
  2. sentiment_counts    → pd.Series  — review count per sentiment
  3. top_negative_issue  → str        — category with most negative reviews
  4. category_sentiment  → pd.DataFrame — pivot: category × sentiment counts
  5. trend_data          → pd.DataFrame | None — monthly review volume
                           (only when a valid date column exists)
  6. avg_score_by_cat    → pd.DataFrame — mean sentiment score per category
"""

from __future__ import annotations

import pandas as pd
from config.settings import DATE_COLUMN


def aggregate_insights(df: pd.DataFrame) -> dict:
    """
    Compute all aggregated metrics from the enriched review dataframe.

    Parameters
    ----------
    df : pd.DataFrame
        Enriched dataframe (must contain 'category', 'sentiment',
        'sentiment_score' columns).

    Returns
    -------
    dict with keys:
        - category_counts     : pd.Series
        - sentiment_counts    : pd.Series
        - top_negative_issue  : str
        - category_sentiment  : pd.DataFrame
        - trend_data          : pd.DataFrame | None
        - avg_score_by_cat    : pd.DataFrame
        - total_reviews       : int
        - negative_pct        : float
    """
    total = len(df)

    # ── 1. Counts by category ────────────────────────────────────────────────
    category_counts: pd.Series = (
        df["category"].value_counts().rename("count")
    )

    # ── 2. Counts by sentiment ───────────────────────────────────────────────
    sentiment_counts: pd.Series = (
        df["sentiment"].value_counts().rename("count")
    )

    # ── 3. Top negative issue ────────────────────────────────────────────────
    negative_df = df[df["sentiment"] == "Negative"]
    if not negative_df.empty:
        top_negative_issue: str = negative_df["category"].value_counts().idxmax()
    else:
        top_negative_issue = "No negative reviews detected 🎉"

    # ── 4. Category × Sentiment pivot ────────────────────────────────────────
    category_sentiment: pd.DataFrame = (
        df.groupby(["category", "sentiment"])
        .size()
        .unstack(fill_value=0)
    )
    # Ensure all three sentiment columns are present even if one has 0 rows
    for col in ["Positive", "Neutral", "Negative"]:
        if col not in category_sentiment.columns:
            category_sentiment[col] = 0

    # ── 5. Trend analysis (optional) ─────────────────────────────────────────
    trend_data: pd.DataFrame | None = None
    if DATE_COLUMN in df.columns and pd.api.types.is_datetime64_any_dtype(df[DATE_COLUMN]):
        trend_df = df.dropna(subset=[DATE_COLUMN]).copy()
        if not trend_df.empty:
            trend_df["month"] = trend_df[DATE_COLUMN].dt.to_period("M").astype(str)
            trend_data = (
                trend_df.groupby("month")
                .agg(
                    total=("category", "count"),
                    negative=("sentiment", lambda s: (s == "Negative").sum()),
                )
                .reset_index()
            )

    # ── 6. Average sentiment score by category ────────────────────────────────
    avg_score_by_cat: pd.DataFrame = (
        df.groupby("category")["sentiment_score"]
        .mean()
        .round(3)
        .reset_index()
        .rename(columns={"sentiment_score": "avg_sentiment_score"})
        .sort_values("avg_sentiment_score")
    )

    # ── 7. Overall negative percentage ───────────────────────────────────────
    negative_count = int(sentiment_counts.get("Negative", 0))
    negative_pct   = round((negative_count / total * 100) if total else 0, 1)

    return {
        "category_counts":    category_counts,
        "sentiment_counts":   sentiment_counts,
        "top_negative_issue": top_negative_issue,
        "category_sentiment": category_sentiment,
        "trend_data":         trend_data,
        "avg_score_by_cat":   avg_score_by_cat,
        "total_reviews":      total,
        "negative_pct":       negative_pct,
    }
