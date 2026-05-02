"""
pipeline/__init__.py
--------------------
Exposes the full RIAS pipeline as a single callable.
"""

from .preprocessor import preprocess
from .sentiment import analyze_sentiment
from .classifier import classify_category
from .aggregator import aggregate_insights
from .recommender import generate_recommendations

__all__ = [
    "preprocess",
    "analyze_sentiment",
    "classify_category",
    "aggregate_insights",
    "generate_recommendations",
]
