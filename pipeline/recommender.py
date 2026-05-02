"""
pipeline/recommender.py
-----------------------
Recommendation engine — maps aggregated insights to concrete
business actions.

Logic:
  1. Identify the top N most-complained-about categories
     (by volume of NEGATIVE reviews).
  2. Pull the pre-defined action items from RECOMMENDATION_MAP.
  3. Return a prioritised, structured list of recommendations.

This is intentionally rule-based so it's 100% explainable.
Swap or augment with LLM calls here for more context-aware advice.
"""

from __future__ import annotations

import pandas as pd
from config.categories import RECOMMENDATION_MAP, DEFAULT_CATEGORY


def generate_recommendations(
    df: pd.DataFrame,
    insights: dict,
    top_n: int = 3,
) -> list[dict]:
    """
    Generate prioritised business recommendations.

    Parameters
    ----------
    df : pd.DataFrame
        Enriched review dataframe (post-classification).
    insights : dict
        Output from aggregate_insights().
    top_n : int
        Number of top problem categories to surface (default: 3).

    Returns
    -------
    list[dict]
        Ordered list of recommendation objects:
        [
          {
            "rank":           int,
            "category":       str,
            "negative_count": int,
            "actions":        list[str],
            "priority":       str,   # "Critical" | "High" | "Medium"
          },
          ...
        ]
    """
    # ── Rank categories by negative review volume ─────────────────────────────
    negative_df = df[df["sentiment"] == "Negative"]

    if negative_df.empty:
        return []  # No issues to recommend on

    neg_by_category: pd.Series = (
        negative_df["category"]
        .value_counts()
        .head(top_n)
    )

    total_negatives = len(negative_df)
    recommendations: list[dict] = []

    for rank, (category, neg_count) in enumerate(neg_by_category.items(), start=1):
        # Determine priority tier based on share of total negatives
        share = neg_count / total_negatives
        if share >= 0.40:
            priority = "🔴 Critical"
        elif share >= 0.20:
            priority = "🟠 High"
        else:
            priority = "🟡 Medium"

        actions = RECOMMENDATION_MAP.get(category, RECOMMENDATION_MAP[DEFAULT_CATEGORY])

        recommendations.append(
            {
                "rank":           rank,
                "category":       category,
                "negative_count": int(neg_count),
                "share_pct":      round(share * 100, 1),
                "actions":        actions,
                "priority":       priority,
            }
        )

    return recommendations
