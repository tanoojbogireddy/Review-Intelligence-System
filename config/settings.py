"""
config/settings.py
------------------
Central configuration for RIAS.
All environment variables and feature flags live here.
Swap USE_LLM=True to enable OpenAI-based classification.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ── LLM toggle ────────────────────────────────────────────────────────────────
# Set to True (or export USE_LLM=true) to enable OpenAI classification.
USE_LLM: bool = os.getenv("USE_LLM", "false").lower() == "true"

# OpenAI config (only used when USE_LLM=True)
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL: str   = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

# ── Pipeline config ───────────────────────────────────────────────────────────
REVIEW_COLUMN: str  = "review"   # Expected column name in uploaded CSV
DATE_COLUMN: str    = "date"     # Optional — enables trend analysis
RATING_COLUMN: str  = "rating"  # Optional — used for additional context

# Sentiment thresholds (TextBlob polarity: -1.0 → +1.0)
POSITIVE_THRESHOLD: float =  0.05
NEGATIVE_THRESHOLD: float = -0.05
