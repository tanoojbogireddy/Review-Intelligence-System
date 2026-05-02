"""
pipeline/preprocessor.py
------------------------
Text cleaning and data validation layer.

Responsibilities:
- Strip whitespace, lowercase text
- Remove special characters and noise
- Drop rows where the review column is null or empty
- Optionally normalise the date column for trend analysis
"""

import re
import pandas as pd
from config.settings import REVIEW_COLUMN, DATE_COLUMN


def _clean_text(text: str) -> str:
    """
    Apply a lightweight text-cleaning pipeline:
      1. Lowercase
      2. Remove URLs
      3. Remove HTML tags
      4. Collapse extra whitespace
      5. Strip leading / trailing whitespace

    Deliberately does NOT strip punctuation so that TextBlob sentiment
    analysis can still pick up negations (e.g. "not good", "wasn't clean").
    """
    if not isinstance(text, str):
        return ""

    text = text.lower()
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)   # URLs
    text = re.sub(r"<[^>]+>", " ", text)                  # HTML tags
    text = re.sub(r"\s+", " ", text)                      # Collapse whitespace
    return text.strip()


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """
    Entry-point for the preprocessing stage.

    Parameters
    ----------
    df : pd.DataFrame
        Raw dataframe loaded from the uploaded CSV.

    Returns
    -------
    pd.DataFrame
        Cleaned dataframe with a new 'clean_review' column added.
        Rows with missing/empty reviews are dropped.

    Raises
    ------
    ValueError
        If the required review column is absent from the dataframe.
    """
    if REVIEW_COLUMN not in df.columns:
        raise ValueError(
            f"Expected a column named '{REVIEW_COLUMN}' in the uploaded file. "
            f"Found: {list(df.columns)}"
        )

    # ── Drop rows with no review text ────────────────────────────────────────
    df = df.dropna(subset=[REVIEW_COLUMN]).copy()
    df = df[df[REVIEW_COLUMN].astype(str).str.strip() != ""]
    df = df.reset_index(drop=True)

    # ── Apply text cleaning ──────────────────────────────────────────────────
    df["clean_review"] = df[REVIEW_COLUMN].astype(str).apply(_clean_text)

    # ── Optionally normalise the date column ─────────────────────────────────
    if DATE_COLUMN in df.columns:
        df[DATE_COLUMN] = pd.to_datetime(df[DATE_COLUMN], errors="coerce")

    return df
