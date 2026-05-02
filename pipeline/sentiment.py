"""
pipeline/sentiment.py
---------------------
Sentiment classification layer.

Strategy:
- DEFAULT (rule-based): Uses TextBlob polarity score.
  Polarity ranges from -1.0 (very negative) to +1.0 (very positive).
  Thresholds are configurable in config/settings.py.
- UPGRADE PATH: Set USE_LLM=true in .env to route to OpenAI instead.

Output columns added:
  - sentiment        : "Positive" | "Negative" | "Neutral"
  - sentiment_score  : float polarity score (TextBlob) or 0–1 confidence (LLM)
"""

import pandas as pd
from textblob import TextBlob
from config.settings import (
    USE_LLM,
    POSITIVE_THRESHOLD,
    NEGATIVE_THRESHOLD,
    OPENAI_API_KEY,
    OPENAI_MODEL,
)


# ── Rule-based (TextBlob) ────────────────────────────────────────────────────

def _textblob_sentiment(text: str) -> tuple[str, float]:
    """
    Classify sentiment using TextBlob polarity.

    Returns
    -------
    (label, score) where label is one of Positive / Negative / Neutral
    and score is the raw TextBlob polarity float.
    """
    polarity: float = TextBlob(text).sentiment.polarity

    if polarity >= POSITIVE_THRESHOLD:
        label = "Positive"
    elif polarity <= NEGATIVE_THRESHOLD:
        label = "Negative"
    else:
        label = "Neutral"

    return label, round(polarity, 4)


# ── LLM-based (OpenAI) ───────────────────────────────────────────────────────

def _llm_sentiment(text: str) -> tuple[str, float]:
    """
    Classify sentiment using OpenAI chat completion.

    Prompt is structured for deterministic, parseable output.
    Falls back to TextBlob on any API error so the pipeline never stalls.

    Returns
    -------
    (label, confidence) where confidence is a synthetic float derived
    from the model's categorical response (1.0 / 0.5 / 0.0).
    """
    try:
        from openai import OpenAI  # lazy import — only required when USE_LLM=True

        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a sentiment classifier. "
                        "Reply with exactly one word: Positive, Negative, or Neutral."
                    ),
                },
                {"role": "user", "content": f"Review: {text}"},
            ],
            temperature=0,
            max_tokens=5,
        )
        label = response.choices[0].message.content.strip().capitalize()
        if label not in ("Positive", "Negative", "Neutral"):
            label = "Neutral"

        # Map label to a synthetic confidence score
        score_map = {"Positive": 1.0, "Neutral": 0.5, "Negative": 0.0}
        return label, score_map[label]

    except Exception as exc:
        # Graceful fallback — log the error and use TextBlob
        print(f"[WARN] LLM sentiment failed ({exc}), falling back to TextBlob.")
        return _textblob_sentiment(text)


# ── Public API ───────────────────────────────────────────────────────────────

def _classify_single(text: str) -> tuple[str, float]:
    """Route to the correct sentiment backend based on settings."""
    if USE_LLM and OPENAI_API_KEY:
        return _llm_sentiment(text)
    return _textblob_sentiment(text)


def analyze_sentiment(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add 'sentiment' and 'sentiment_score' columns to the dataframe.

    Operates on the 'clean_review' column produced by the preprocessor.

    Parameters
    ----------
    df : pd.DataFrame
        Preprocessed dataframe (must contain 'clean_review').

    Returns
    -------
    pd.DataFrame
        Input dataframe with two new columns appended.
    """
    results = df["clean_review"].apply(_classify_single)
    df["sentiment"]       = results.apply(lambda x: x[0])
    df["sentiment_score"] = results.apply(lambda x: x[1])
    return df
