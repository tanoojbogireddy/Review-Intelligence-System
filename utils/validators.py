"""
utils/validators.py
-------------------
Input validation helpers to give clear, user-friendly error messages
before the pipeline starts processing.
"""

from __future__ import annotations

import pandas as pd
from config.settings import REVIEW_COLUMN


def validate_dataframe(df: pd.DataFrame) -> tuple[bool, str]:
    """
    Validate that the uploaded dataframe is usable by the RIAS pipeline.

    Checks performed (in order):
      1. DataFrame is not empty
      2. Required 'review' column exists
      3. At least one non-null review is present

    Parameters
    ----------
    df : pd.DataFrame

    Returns
    -------
    (is_valid: bool, message: str)
        is_valid = True  → pipeline can proceed; message is empty
        is_valid = False → message explains the validation failure
    """
    if df.empty:
        return False, "The uploaded file is empty."

    if REVIEW_COLUMN not in df.columns:
        available = ", ".join(f"'{c}'" for c in df.columns)
        return (
            False,
            f"Column '{REVIEW_COLUMN}' not found. "
            f"Available columns: {available}. "
            f"Please rename your review column to '{REVIEW_COLUMN}'.",
        )

    non_null_reviews = df[REVIEW_COLUMN].dropna()
    non_empty_reviews = non_null_reviews[
        non_null_reviews.astype(str).str.strip() != ""
    ]

    if non_empty_reviews.empty:
        return (
            False,
            f"Column '{REVIEW_COLUMN}' exists but contains no usable text.",
        )

    return True, ""
