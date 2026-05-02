"""
app.py
------
RIAS — Review Intelligence Automation System
Streamlit Dashboard

Orchestrates the full pipeline:
  Upload → Preprocess → Sentiment → Classify → Aggregate → Recommend → Display

Run with:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Internal modules ──────────────────────────────────────────────────────────
from pipeline.preprocessor import preprocess
from pipeline.sentiment import analyze_sentiment
from pipeline.classifier import classify_category
from pipeline.aggregator import aggregate_insights
from pipeline.recommender import generate_recommendations
from utils.io_helpers import load_csv, export_csv
from utils.validators import validate_dataframe
from config.settings import USE_LLM, REVIEW_COLUMN

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="RIAS — Review Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════════════════════
# CUSTOM CSS — Premium dark theme
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown(
    """
<style>
    /* ── Global ──────────────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── Background ──────────────────────────────────────────── */
    .stApp {
        background: linear-gradient(135deg, #0d1117 0%, #161b22 50%, #0d1117 100%);
        color: #e6edf3;
    }

    /* ── Sidebar ─────────────────────────────────────────────── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #161b22 0%, #21262d 100%);
        border-right: 1px solid #30363d;
    }

    /* ── Metric cards ────────────────────────────────────────── */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #21262d, #2d333b);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 16px 20px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    [data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.4);
    }

    /* ── Section cards ───────────────────────────────────────── */
    .rias-card {
        background: linear-gradient(135deg, #21262d, #2d333b);
        border: 1px solid #30363d;
        border-radius: 16px;
        padding: 24px 28px;
        margin-bottom: 20px;
        transition: box-shadow 0.2s ease;
    }
    .rias-card:hover {
        box-shadow: 0 8px 32px rgba(0,0,0,0.5);
    }

    /* ── Hero header ─────────────────────────────────────────── */
    .hero-title {
        background: linear-gradient(90deg, #58a6ff, #3fb950, #f78166);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 0;
    }
    .hero-sub {
        color: #8b949e;
        font-size: 1.05rem;
        font-weight: 400;
        margin-top: 4px;
    }

    /* ── Recommendation cards ────────────────────────────────── */
    .rec-card {
        background: linear-gradient(135deg, #1c2128, #22272e);
        border-left: 4px solid #58a6ff;
        border-radius: 10px;
        padding: 18px 22px;
        margin-bottom: 14px;
        animation: slideIn 0.4s ease-out;
    }
    .rec-card.critical { border-left-color: #f85149; }
    .rec-card.high     { border-left-color: #f0883e; }
    .rec-card.medium   { border-left-color: #d29922; }

    .rec-category {
        font-size: 1.1rem;
        font-weight: 700;
        color: #e6edf3;
        margin-bottom: 8px;
    }
    .rec-action {
        color: #8b949e;
        font-size: 0.92rem;
        line-height: 1.7;
        margin: 3px 0;
    }

    /* ── Badge ───────────────────────────────────────────────── */
    .badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-left: 8px;
    }
    .badge-positive { background: #1a4731; color: #3fb950; }
    .badge-negative { background: #4b1b18; color: #f85149; }
    .badge-neutral  { background: #2d2f36; color: #8b949e; }

    /* ── Section headings ────────────────────────────────────── */
    .section-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #e6edf3;
        border-bottom: 1px solid #30363d;
        padding-bottom: 10px;
        margin-bottom: 18px;
    }

    /* ── Divider ─────────────────────────────────────────────── */
    .rias-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #30363d, transparent);
        margin: 28px 0;
    }

    /* ── Animations ──────────────────────────────────────────── */
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(10px); }
        to   { opacity: 1; transform: translateY(0);    }
    }

    /* ── Table styling ───────────────────────────────────────── */
    .dataframe thead tr th {
        background-color: #21262d !important;
        color: #58a6ff !important;
        font-weight: 600 !important;
    }
    .dataframe tbody tr:hover { background-color: #2d333b !important; }

    /* ── Upload area ─────────────────────────────────────────── */
    [data-testid="stFileUploader"] {
        border: 2px dashed #30363d;
        border-radius: 12px;
        padding: 12px;
        transition: border-color 0.2s ease;
    }
    [data-testid="stFileUploader"]:hover { border-color: #58a6ff; }

    /* ── Buttons ─────────────────────────────────────────────── */
    .stButton > button {
        background: linear-gradient(135deg, #238636, #2ea043);
        color: #ffffff;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 10px 24px;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #2ea043, #3fb950);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(46,160,67,0.4);
    }

    /* ── Plotly chart frames ─────────────────────────────────── */
    .js-plotly-plot { border-radius: 12px; overflow: hidden; }

    /* ── Hide Streamlit branding ─────────────────────────────── */
    #MainMenu, footer, header { visibility: hidden; }
</style>
""",
    unsafe_allow_html=True,
)


# ═══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

CHART_THEME = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor":  "rgba(0,0,0,0)",
    "font_color":    "#8b949e",
    "gridcolor":     "#21262d",
}

SENTIMENT_COLORS = {
    "Positive": "#3fb950",
    "Neutral":  "#8b949e",
    "Negative": "#f85149",
}

CATEGORY_COLOR_SEQ = [
    "#58a6ff", "#3fb950", "#f78166", "#d29922",
    "#a371f7", "#79c0ff", "#ffa657", "#56d364",
]


def _sentiment_badge(sentiment: str) -> str:
    cls_map = {"Positive": "positive", "Negative": "negative", "Neutral": "neutral"}
    cls = cls_map.get(sentiment, "neutral")
    return f'<span class="badge badge-{cls}">{sentiment}</span>'


@st.cache_data(show_spinner=False)
def run_pipeline(raw_df: pd.DataFrame) -> tuple[pd.DataFrame, dict, list]:
    """
    Cache the full pipeline run so re-renders don't re-process.
    The cache key is the dataframe content hash.
    """
    df = preprocess(raw_df)
    df = analyze_sentiment(df)
    df = classify_category(df)
    insights = aggregate_insights(df)
    recs = generate_recommendations(df, insights, top_n=3)
    return df, insights, recs


# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown(
        """
        <div style="text-align:center; padding: 12px 0 24px;">
            <div style="font-size:2.4rem;">🧠</div>
            <div style="font-size:1.15rem; font-weight:700; color:#e6edf3;">RIAS</div>
            <div style="font-size:0.8rem; color:#8b949e;">Review Intelligence System</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 📂 Data Source")
    uploaded_file = st.file_uploader(
        "Upload a CSV file",
        type=["csv"],
        help=f"CSV must contain a column named '{REVIEW_COLUMN}'.",
    )

    use_sample = st.checkbox("Use sample data", value=True)

    st.markdown("---")
    st.markdown("### ⚙️ Filters")

    # These will be populated after the pipeline runs
    sentiment_filter = st.multiselect(
        "Sentiment",
        options=["Positive", "Neutral", "Negative"],
        default=["Positive", "Neutral", "Negative"],
    )
    category_filter = st.multiselect(
        "Category",
        options=[
            "Taste", "Staff / Service", "Cleanliness",
            "Wait Time", "Pricing", "Product Quality", "Delivery", "Other",
        ],
        default=[
            "Taste", "Staff / Service", "Cleanliness",
            "Wait Time", "Pricing", "Product Quality", "Delivery", "Other",
        ],
    )

    st.markdown("---")

    engine_label = "🤖 OpenAI (LLM)" if USE_LLM else "📐 Rule-based (TextBlob)"
    st.markdown(f"**Engine:** {engine_label}")
    st.markdown(
        "<div style='font-size:0.78rem;color:#8b949e;margin-top:4px;'>"
        "Toggle via USE_LLM env var</div>",
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.75rem;color:#484f58;text-align:center;'>"
        "Built with ❤️ · RIAS v1.0</div>",
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# LOAD DATA
# ═══════════════════════════════════════════════════════════════════════════════

raw_df: pd.DataFrame | None = None

if uploaded_file is not None:
    raw_df = load_csv(uploaded_file)
elif use_sample:
    try:
        raw_df = load_csv("data/sample_reviews.csv")
    except FileNotFoundError:
        st.error("Sample data file not found. Please upload a CSV.")

# ═══════════════════════════════════════════════════════════════════════════════
# HERO HEADER
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown(
    """
    <div class="rias-card" style="text-align:center; padding: 36px 40px;">
        <div class="hero-title">Review Intelligence Automation System</div>
        <div class="hero-sub">
            AI-powered pipeline that converts raw customer reviews into
            structured insights &amp; actionable business recommendations
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ═══════════════════════════════════════════════════════════════════════════════
# NO DATA STATE
# ═══════════════════════════════════════════════════════════════════════════════

if raw_df is None:
    st.markdown(
        """
        <div class="rias-card" style="text-align:center;padding:48px;">
            <div style="font-size:3rem;">📥</div>
            <div style="font-size:1.2rem;font-weight:600;color:#e6edf3;margin:12px 0 8px;">
                Upload a CSV to get started
            </div>
            <div style="color:#8b949e;">
                Or check <b>Use sample data</b> in the sidebar to explore with built-in reviews.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

# ═══════════════════════════════════════════════════════════════════════════════
# VALIDATE + RUN PIPELINE
# ═══════════════════════════════════════════════════════════════════════════════

is_valid, err_msg = validate_dataframe(raw_df)
if not is_valid:
    st.error(f"❌ **Validation Error:** {err_msg}")
    st.stop()

with st.spinner("🔄 Running RIAS pipeline…"):
    df, insights, recs = run_pipeline(raw_df)

# ── Apply sidebar filters ─────────────────────────────────────────────────────
filtered_df = df.copy()
if sentiment_filter:
    filtered_df = filtered_df[filtered_df["sentiment"].isin(sentiment_filter)]
if category_filter:
    filtered_df = filtered_df[filtered_df["category"].isin(category_filter)]

# ═══════════════════════════════════════════════════════════════════════════════
# KPI METRICS ROW
# ═══════════════════════════════════════════════════════════════════════════════

m1, m2, m3, m4, m5 = st.columns(5)

total      = insights["total_reviews"]
pos_count  = int(insights["sentiment_counts"].get("Positive", 0))
neg_count  = int(insights["sentiment_counts"].get("Negative", 0))
neu_count  = int(insights["sentiment_counts"].get("Neutral",  0))
neg_pct    = insights["negative_pct"]

m1.metric("📋 Total Reviews",   total)
m2.metric("✅ Positive",        pos_count, f"{round(pos_count/total*100,1)}%")
m3.metric("⚠️ Negative",        neg_count, f"-{neg_pct}%",  delta_color="inverse")
m4.metric("➖ Neutral",         neu_count)
m5.metric("🔥 Top Issue",       insights["top_negative_issue"])

st.markdown('<div class="rias-divider"></div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# CHARTS ROW
# ═══════════════════════════════════════════════════════════════════════════════

col_left, col_right = st.columns([3, 2])

# ── Category distribution bar chart ──────────────────────────────────────────
with col_left:
    st.markdown('<div class="section-title">📊 Reviews by Category</div>', unsafe_allow_html=True)

    cat_data = (
        filtered_df["category"]
        .value_counts()
        .reset_index()
        .rename(columns={"index": "category", "count": "count"})
    )
    # Rename for plotly compatibility across pandas versions
    cat_data.columns = ["category", "count"]

    fig_bar = px.bar(
        cat_data,
        x="count",
        y="category",
        orientation="h",
        color="category",
        color_discrete_sequence=CATEGORY_COLOR_SEQ,
        text="count",
    )
    fig_bar.update_layout(
        showlegend=False,
        paper_bgcolor=CHART_THEME["paper_bgcolor"],
        plot_bgcolor=CHART_THEME["plot_bgcolor"],
        font_color=CHART_THEME["font_color"],
        xaxis=dict(gridcolor=CHART_THEME["gridcolor"], showgrid=True),
        yaxis=dict(gridcolor="rgba(0,0,0,0)"),
        margin=dict(l=0, r=0, t=8, b=0),
        height=340,
    )
    fig_bar.update_traces(
        textposition="outside",
        marker_line_width=0,
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ── Sentiment donut chart ─────────────────────────────────────────────────────
with col_right:
    st.markdown('<div class="section-title">🎯 Sentiment Distribution</div>', unsafe_allow_html=True)

    sent_data = (
        filtered_df["sentiment"]
        .value_counts()
        .reset_index()
    )
    sent_data.columns = ["sentiment", "count"]

    fig_donut = px.pie(
        sent_data,
        names="sentiment",
        values="count",
        hole=0.55,
        color="sentiment",
        color_discrete_map=SENTIMENT_COLORS,
    )
    fig_donut.update_layout(
        paper_bgcolor=CHART_THEME["paper_bgcolor"],
        font_color=CHART_THEME["font_color"],
        legend=dict(orientation="h", y=-0.1),
        margin=dict(l=0, r=0, t=8, b=0),
        height=340,
    )
    fig_donut.update_traces(
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>Count: %{value}<extra></extra>",
    )
    st.plotly_chart(fig_donut, use_container_width=True)

st.markdown('<div class="rias-divider"></div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# CATEGORY × SENTIMENT HEATMAP  +  TREND CHART
# ═══════════════════════════════════════════════════════════════════════════════

col_heat, col_trend = st.columns(2)

# ── Category × Sentiment grouped bar ─────────────────────────────────────────
with col_heat:
    st.markdown('<div class="section-title">🔥 Sentiment by Category</div>', unsafe_allow_html=True)

    cat_sent = insights["category_sentiment"].reset_index()
    # Melt for plotly
    melt_cols = [c for c in ["Positive", "Neutral", "Negative"] if c in cat_sent.columns]
    melted = cat_sent.melt(id_vars="category", value_vars=melt_cols,
                            var_name="Sentiment", value_name="Count")

    fig_group = px.bar(
        melted,
        x="category",
        y="Count",
        color="Sentiment",
        barmode="group",
        color_discrete_map=SENTIMENT_COLORS,
    )
    fig_group.update_layout(
        paper_bgcolor=CHART_THEME["paper_bgcolor"],
        plot_bgcolor=CHART_THEME["plot_bgcolor"],
        font_color=CHART_THEME["font_color"],
        xaxis=dict(gridcolor="rgba(0,0,0,0)", tickangle=-30),
        yaxis=dict(gridcolor=CHART_THEME["gridcolor"]),
        legend_title_text="",
        margin=dict(l=0, r=0, t=8, b=0),
        height=320,
    )
    st.plotly_chart(fig_group, use_container_width=True)

# ── Trend chart (monthly) ─────────────────────────────────────────────────────
with col_trend:
    st.markdown('<div class="section-title">📈 Monthly Review Trend</div>', unsafe_allow_html=True)

    trend_data = insights.get("trend_data")
    if trend_data is not None and not trend_data.empty:
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=trend_data["month"], y=trend_data["total"],
            name="Total", mode="lines+markers",
            line=dict(color="#58a6ff", width=2),
            marker=dict(size=7),
        ))
        fig_line.add_trace(go.Scatter(
            x=trend_data["month"], y=trend_data["negative"],
            name="Negative", mode="lines+markers",
            line=dict(color="#f85149", width=2, dash="dot"),
            marker=dict(size=7),
        ))
        fig_line.update_layout(
            paper_bgcolor=CHART_THEME["paper_bgcolor"],
            plot_bgcolor=CHART_THEME["plot_bgcolor"],
            font_color=CHART_THEME["font_color"],
            xaxis=dict(gridcolor=CHART_THEME["gridcolor"]),
            yaxis=dict(gridcolor=CHART_THEME["gridcolor"]),
            legend=dict(orientation="h", y=1.1),
            margin=dict(l=0, r=0, t=8, b=0),
            height=320,
        )
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info(
            "📅 No date column detected. Add a **'date'** column to your CSV "
            "to unlock monthly trend analysis."
        )

st.markdown('<div class="rias-divider"></div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# RECOMMENDATIONS ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown('<div class="section-title">💡 Actionable Recommendations</div>', unsafe_allow_html=True)

if not recs:
    st.success("🎉 No significant negative issues detected. Keep up the excellent work!")
else:
    for rec in recs:
        priority_lower = rec["priority"].split()[-1].lower()  # "critical" | "high" | "medium"
        actions_html   = "".join(
            f'<div class="rec-action">• {a}</div>' for a in rec["actions"]
        )
        st.markdown(
            f"""
            <div class="rec-card {priority_lower}">
                <div class="rec-category">
                    #{rec['rank']} — {rec['category']}
                    &nbsp;
                    <span style="font-size:0.85rem;font-weight:400;color:#8b949e;">
                        {rec['negative_count']} negative reviews
                        ({rec['share_pct']}% of all negatives)
                    </span>
                    &nbsp;&nbsp;
                    <span style="font-size:0.82rem;">{rec['priority']}</span>
                </div>
                {actions_html}
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown('<div class="rias-divider"></div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# AVG SENTIMENT SCORE TABLE
# ═══════════════════════════════════════════════════════════════════════════════

col_avg, col_spacer = st.columns([1, 1])
with col_avg:
    st.markdown('<div class="section-title">📉 Average Sentiment Score by Category</div>', unsafe_allow_html=True)

    avg_df = insights["avg_score_by_cat"].copy()
    avg_df.columns = ["Category", "Avg Sentiment Score"]
    avg_df["Signal"] = avg_df["Avg Sentiment Score"].apply(
        lambda s: "🟢 Positive" if s > 0.05 else ("🔴 Negative" if s < -0.05 else "⚪ Neutral")
    )

    st.dataframe(
        avg_df,
        use_container_width=True,
        hide_index=True,
    )

st.markdown('<div class="rias-divider"></div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PROCESSED REVIEW TABLE
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown('<div class="section-title">📋 Processed Reviews</div>', unsafe_allow_html=True)

display_cols = [REVIEW_COLUMN, "sentiment", "sentiment_score", "category"]
if "date" in filtered_df.columns:
    display_cols.insert(1, "date")
if "rating" in filtered_df.columns:
    display_cols.insert(1, "rating")

display_df = filtered_df[[c for c in display_cols if c in filtered_df.columns]].copy()

# Pagination
page_size   = 15
total_pages = max(1, -(-len(display_df) // page_size))  # ceiling division
page_num    = st.number_input(
    f"Page (1 – {total_pages})",
    min_value=1, max_value=total_pages, value=1, step=1
)

start = (page_num - 1) * page_size
end   = start + page_size
st.dataframe(
    display_df.iloc[start:end],
    use_container_width=True,
    hide_index=True,
)

st.caption(f"Showing {min(end, len(display_df))} of {len(display_df)} filtered reviews")

# ═══════════════════════════════════════════════════════════════════════════════
# EXPORT
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown('<div class="rias-divider"></div>', unsafe_allow_html=True)

st.markdown("### 📥 Export Results")
col_dl1, col_dl2, _ = st.columns([1, 1, 2])

with col_dl1:
    st.download_button(
        label="⬇️ Download Full Results (CSV)",
        data=export_csv(df),
        file_name="rias_results_full.csv",
        mime="text/csv",
    )

with col_dl2:
    st.download_button(
        label="⬇️ Download Filtered Results (CSV)",
        data=export_csv(filtered_df),
        file_name="rias_results_filtered.csv",
        mime="text/csv",
    )
