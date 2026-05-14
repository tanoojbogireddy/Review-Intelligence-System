# Review Intelligence Automation System (RIAS)

> An end-to-end AI-powered platform that ingests raw customer reviews, runs sentiment analysis and category classification, generates actionable recommendations, and surfaces everything through a polished React dashboard.

---

## Features

- **CSV / Excel Upload** — Drag-and-drop review ingestion with instant processing
- **Sentiment Analysis** — TextBlob-powered polarity scoring (positive / neutral / negative)
- **Category Classification** — Rule-based or LLM-backed tagging (Delivery, Quality, Support, Pricing, …)
- **Trend Detection** — Rolling sentiment trends visualised with Recharts
- **Recommendation Engine** — Automatically surfaces top improvement areas by category
- **KPI Strip** — At-a-glance metrics: total reviews, avg rating, sentiment breakdown
- **Data Table** — Searchable, sortable review table with export to CSV/Excel
- **Dark-Mode Dashboard** — Premium glassmorphism UI built with React + Vite

---

## Project Structure

```
rias/
├── app.py                  # FastAPI app entry point
├── server.py               # Server bootstrap / CORS / static serving
├── requirements.txt
├── .env.example
│
├── pipeline/               # Core processing pipeline
│   ├── preprocessor.py     # Cleaning & normalisation
│   ├── sentiment.py        # TextBlob sentiment scoring
│   ├── classifier.py       # Category classification
│   ├── aggregator.py       # KPI & trend aggregation
│   └── recommender.py      # Recommendation generation
│
├── config/
│   ├── settings.py         # App-wide settings (LLM toggle, etc.)
│   └── categories.py       # Category keyword definitions
│
├── utils/
│   ├── io_helpers.py       # File parsing helpers
│   └── validators.py       # Input validation
│
├── data/
│   └── sample_reviews.csv  # Demo dataset
│
└── frontend/               # React + Vite dashboard
    ├── index.html
    ├── vite.config.js
    └── src/
        ├── App.jsx
        ├── index.css
        └── components/
            ├── Header.jsx
            ├── KpiStrip.jsx
            ├── UploadZone.jsx
            ├── TrendChart.jsx
            ├── CategoryChart.jsx
            ├── SentimentDonut.jsx
            ├── SentimentMatrix.jsx
            ├── Recommendations.jsx
            ├── ReviewTable.jsx
            └── ExportBar.jsx
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+

---

### 1. Clone the repo

```bash
git clone https://github.com/tanoojbogireddy/Review-Intelligence-System.git
cd Review-Intelligence-System
```

### 2. Set up the backend

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env
```

### 3. Configure environment (optional)

Open `.env` and set your values. The app runs fully **without** an OpenAI key using rule-based classification:

```env
USE_LLM=false          # Set to true to enable GPT-based classification
OPENAI_API_KEY=        # Required only when USE_LLM=true
OPENAI_MODEL=gpt-3.5-turbo
```

### 4. Start the backend

```bash
uvicorn app:app --reload --port 8000
```

### 5. Set up and start the frontend

```bash
cd frontend
npm install
npm run dev
```

The dashboard will be available at **http://localhost:5173**

---

## How It Works

```
CSV/Excel Upload
      │
      ▼
 Preprocessor  ──► clean text, normalise columns
      │
      ▼
 Sentiment      ──► TextBlob polarity → positive / neutral / negative
      │
      ▼
 Classifier     ──► keyword match (or GPT) → category tags
      │
      ▼
 Aggregator     ──► KPIs, category counts, rolling trend data
      │
      ▼
 Recommender    ──► top issues per category ranked by negative volume
      │
      ▼
 React Dashboard ◄── Recharts visualisations + exportable table
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI, Python 3.10+ |
| NLP | TextBlob, OpenAI (optional) |
| Data | Pandas |
| Frontend | React 19, Vite 8 |
| Charts | Recharts |
| Icons | Lucide React |
| HTTP | Axios |
| File Upload | React Dropzone |

---

## Sample Data

A demo dataset (`data/sample_reviews.csv`) is included so you can explore the dashboard immediately without uploading your own data.

---

## License

MIT — feel free to use, modify, and distribute.

---

<p align="center">Built by <a href="https://github.com/tanoojbogireddy">Tanooj Bogireddy</a></p>
