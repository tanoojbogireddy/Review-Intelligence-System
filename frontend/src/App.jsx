import { useState, useCallback } from 'react'
import axios from 'axios'
import Header from './components/Header'
import UploadZone from './components/UploadZone'
import KpiStrip from './components/KpiStrip'
import CategoryChart from './components/CategoryChart'
import SentimentDonut from './components/SentimentDonut'
import SentimentMatrix from './components/SentimentMatrix'
import TrendChart from './components/TrendChart'
import Recommendations from './components/Recommendations'
import ReviewTable from './components/ReviewTable'
import ExportBar from './components/ExportBar'
import './App.css'

export default function App() {
  const [state, setState] = useState('idle') // idle | loading | done | error
  const [data, setData]   = useState(null)
  const [error, setError] = useState('')
  const [fileName, setFileName] = useState('')

  const runAnalysis = useCallback(async (source) => {
    setState('loading')
    setError('')
    try {
      let res
      if (source === 'sample') {
        res = await axios.get('/api/sample')
        setFileName('sample_reviews.csv')
      } else {
        const form = new FormData()
        form.append('file', source)
        res = await axios.post('/api/analyze', form)
        setFileName(source.name)
      }
      setData(res.data)
      setState('done')
    } catch (err) {
      const msg = err.response?.data?.detail || err.message || 'Unknown error'
      setError(msg)
      setState('error')
    }
  }, [])

  const reset = () => { setState('idle'); setData(null); setError('') }

  return (
    <div className="app-root">
      <Header onReset={reset} hasData={state === 'done'} />

      <main className="container main-content">
        {state === 'idle' && (
          <UploadZone onUpload={runAnalysis} />
        )}

        {state === 'loading' && (
          <LoadingState />
        )}

        {state === 'error' && (
          <ErrorState message={error} onRetry={reset} />
        )}

        {state === 'done' && data && (
          <Dashboard data={data} fileName={fileName} />
        )}
      </main>
    </div>
  )
}

/* ── Loading skeleton ──────────────────────────────────────── */
function LoadingState() {
  return (
    <div className="loading-state animate-fade-in">
      <div className="loading-spinner" />
      <p className="loading-text">Running RIAS pipeline…</p>
      <p className="loading-sub">Preprocessing → Sentiment → Classification → Insights</p>
    </div>
  )
}

/* ── Error state ───────────────────────────────────────────── */
function ErrorState({ message, onRetry }) {
  return (
    <div className="error-state animate-fade-up card">
      <div className="error-icon">⚠️</div>
      <h2 className="error-title">Pipeline Error</h2>
      <p className="error-msg">{message}</p>
      <button className="btn-primary" onClick={onRetry}>Try Again</button>
    </div>
  )
}

/* ── Full dashboard ────────────────────────────────────────── */
function Dashboard({ data, fileName }) {
  const { rows, insights, recommendations } = data

  return (
    <div className="dashboard animate-fade-up">
      {/* KPI strip */}
      <KpiStrip insights={insights} />

      <div className="divider" />

      {/* Charts row 1 */}
      <div className="grid-2" style={{ marginBottom: 20 }}>
        <CategoryChart data={insights.category_counts} />
        <SentimentDonut data={insights.sentiment_counts} />
      </div>

      {/* Charts row 2 */}
      <div className="grid-2" style={{ marginBottom: 20 }}>
        <SentimentMatrix data={insights.category_sentiment} />
        <TrendChart data={insights.trend_data} />
      </div>

      <div className="divider" />

      {/* Recommendations */}
      <Recommendations recommendations={recommendations} />

      <div className="divider" />

      {/* Review table */}
      <ReviewTable rows={rows} insights={insights} />

      <div className="divider" />

      {/* Export */}
      <ExportBar rows={rows} fileName={fileName} />
    </div>
  )
}
