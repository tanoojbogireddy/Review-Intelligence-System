"""
pipeline/classifier.py
----------------------
Category classification layer.

Strategy:
- DEFAULT (rule-based): Keyword matching against CATEGORY_RULES dict.
  Each review is checked against every category's keyword list.
  First match wins (priority order = dict insertion order).
  If no keywords match, the review is labelled as the DEFAULT_CATEGORY.

- UPGRADE PATH: Set USE_LLM=true in .env to use OpenAI for richer
  semantic classification.  The LLM prompt is designed so the output
  is always one of the known category labels, making downstream code
  fully compatible with both backends.

Output columns added:
  - category : one of the keys in CATEGORY_RULES or DEFAULT_CATEGORY
"""

import pandas as pd
from config.settings import USE_LLM, OPENAI_API_KEY, OPENAI_MODEL
from config.categories import CATEGORY_RULES, DEFAULT_CATEGORY


# ── Helper: build a combined category label string for the LLM prompt ────────
_CATEGORY_LIST_STR = ", ".join(
    list(CATEGORY_RULES.keys()) + [DEFAULT_CATEGORY]
)


# ── Rule-based classifier ────────────────────────────────────────────────────

def _rule_based_classify(text: str) -> str:
    """
    Scan the cleaned review for keywords in each category bucket.

    Matching logic:
    - The review text is checked for whole-word-ish substring presence.
      We do NOT use strict word-boundary regex so that compound words
      (e.g. "overpriced") still match ("price" is in "overpriced").
    - The first category whose keyword is found in the text wins.
    - Ties are broken by dict order (most specific → most general).

    Returns
    -------
    str : category label
    """
    for category, keywords in CATEGORY_RULES.items():
        for kw in keywords:
            if kw in text:
                return category
    return DEFAULT_CATEGORY


# ── LLM-based classifier ─────────────────────────────────────────────────────

def _llm_classify(text: str) -> str:
    """
    Classify review category using an OpenAI chat completion.

    The prompt constrains the model to reply with exactly one of the
    known category labels, so no post-processing mapping is needed.

    Falls back to rule-based on any API error.

    Returns
    -------
    str : category label
    """
    try:
        from openai import OpenAI  # lazy import

        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a review category classifier for a restaurant / retail business. "
                        f"Classify the customer review into exactly one of these categories: "
                        f"{_CATEGORY_LIST_STR}. "
                        "Reply with only the category name, nothing else."
                    ),
                },
                {"role": "user", "content": f"Review: {text}"},
            ],
            temperature=0,
            max_tokens=10,
        )
        label = response.choices[0].message.content.strip()

        # Validate the returned label; fall back if unexpected
        valid_labels = list(CATEGORY_RULES.keys()) + [DEFAULT_CATEGORY]
        return label if label in valid_labels else DEFAULT_CATEGORY

    except Exception as exc:
        print(f"[WARN] LLM classify failed ({exc}), falling back to rule-based.")
        return _rule_based_classify(text)


# ── Public API ───────────────────────────────────────────────────────────────

def _classify_single(text: str) -> str:
    """Route to the correct classification backend based on settings."""
    if USE_LLM and OPENAI_API_KEY:
        return _llm_classify(text)
    return _rule_based_classify(text)


def classify_category(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a 'category' column to the dataframe.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe that has already been through sentiment analysis
        (must contain 'clean_review').

    Returns
    -------
    pd.DataFrame
        Input dataframe with 'category' column appended.
    """
    df["category"] = df["clean_review"].apply(_classify_single)
    return df
