"""
config/categories.py
--------------------
Single source of truth for:
  1. CATEGORY_RULES    → keyword lists used by the rule-based classifier
  2. RECOMMENDATION_MAP → category → list of business actions

To add a new category: add entries to both dicts — no other code needs changing.
"""

from typing import Dict, List

# ── Category keyword rules ────────────────────────────────────────────────────
CATEGORY_RULES: Dict[str, List[str]] = {
    "Taste": [
        "taste", "flavor", "flavour", "delicious", "bland", "spicy",
        "sweet", "salty", "fresh", "stale", "yummy", "disgusting",
        "overcooked", "undercooked", "raw", "burnt", "food quality",
        "portion", "soggy", "crispy", "texture", "aroma", "greasy",
    ],
    "Staff / Service": [
        "staff", "service", "waiter", "waitress", "rude", "friendly",
        "helpful", "attentive", "ignored", "unprofessional", "polite",
        "server", "cashier", "employee", "manager", "host", "hostess",
        "customer service", "attitude", "nice", "horrible staff",
    ],
    "Cleanliness": [
        "clean", "dirty", "hygiene", "sanitation", "filthy", "spotless",
        "messy", "tidy", "restroom", "bathroom", "toilet", "cockroach",
        "pest", "mold", "mould", "dusty", "sticky table", "gross",
    ],
    "Wait Time": [
        "wait", "slow", "long wait", "quick", "fast", "delayed",
        "took forever", "hours", "rushed", "queue", "line",
        "reservation", "on time", "late", "prompt", "forever",
    ],
    "Pricing": [
        "price", "expensive", "cheap", "affordable", "overpriced",
        "value", "worth", "cost", "pricey", "budget", "deal",
        "discount", "reasonable", "rip off", "ripoff", "costly",
    ],
    "Product Quality": [
        "quality", "packaging", "broken", "damaged", "defective",
        "excellent quality", "poor quality", "well made", "sturdy",
        "flimsy", "expired", "shelf", "ingredients", "material",
    ],
    "Delivery": [
        "delivery", "deliver", "shipped", "shipping", "courier",
        "arrived", "package", "tracking", "late delivery",
        "wrong order", "missing item", "cold food", "driver",
    ],
}

DEFAULT_CATEGORY: str = "Other"

# ── Recommendation map ────────────────────────────────────────────────────────
RECOMMENDATION_MAP: Dict[str, List[str]] = {
    "Taste": [
        "🍽️  Conduct weekly recipe review sessions with the kitchen team.",
        "🧂  Source fresher, higher-quality ingredients from vetted suppliers.",
        "📋  Implement a quality-control tasting checklist before each service shift.",
    ],
    "Staff / Service": [
        "🎓  Schedule mandatory customer-service training workshops.",
        "⭐  Introduce a peer-recognition and staff incentive program.",
        "📝  Set up a mystery-shopper program to monitor service standards.",
    ],
    "Cleanliness": [
        "🧹  Increase scheduled deep-cleaning frequency (daily minimum).",
        "✅  Implement hourly cleanliness checklists for front-of-house.",
        "🔍  Hire a third-party hygiene auditor for monthly inspections.",
    ],
    "Wait Time": [
        "👨‍🍳  Optimise kitchen workflow and prep schedules during peak hours.",
        "📱  Introduce online pre-ordering or reservation management software.",
        "📊  Analyse peak-hour data to adjust staffing levels proactively.",
    ],
    "Pricing": [
        "💰  Benchmark menu pricing against local competitors quarterly.",
        "🎁  Introduce a loyalty rewards program to increase perceived value.",
        "📦  Create bundled meal deals to improve value-for-money perception.",
    ],
    "Product Quality": [
        "🏭  Audit suppliers and enforce minimum acceptance standards.",
        "🔄  Establish a clear return/replacement policy for defective items.",
        "📦  Review packaging materials for durability and freshness during transit.",
    ],
    "Delivery": [
        "🚀  Partner with a more reliable last-mile delivery provider.",
        "🌡️  Invest in insulated, tamper-evident packaging for food orders.",
        "📍  Add real-time order tracking for customers post-dispatch.",
    ],
    "Other": [
        "📊  Collect more specific feedback through targeted follow-up surveys.",
        "💬  Respond personally to ambiguous reviews to extract actionable detail.",
    ],
}
