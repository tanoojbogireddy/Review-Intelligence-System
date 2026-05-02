import { useState, useMemo } from 'react'
import './ReviewTable.css'

const PAGE_SIZE = 12

const SENTIMENT_CLS = {
  Positive: 'badge-positive',
  Negative: 'badge-negative',
  Neutral:  'badge-neutral',
}

export default function ReviewTable({ rows, insights }) {
  const [sentimentFilter, setSentimentFilter] = useState('All')
  const [categoryFilter,  setCategoryFilter]  = useState('All')
  const [page, setPage] = useState(1)

  const categories = useMemo(
    () => ['All', ...Object.keys(insights.category_counts)],
    [insights]
  )

  const filtered = useMemo(() => {
    return rows.filter(r => {
      if (sentimentFilter !== 'All' && r.sentiment !== sentimentFilter) return false
      if (categoryFilter  !== 'All' && r.category  !== categoryFilter)  return false
      return true
    })
  }, [rows, sentimentFilter, categoryFilter])

  const totalPages = Math.ceil(filtered.length / PAGE_SIZE)
  const paginated  = filtered.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE)

  const handleFilter = (setter) => (val) => {
    setter(val)
    setPage(1)
  }

  return (
    <div className="review-table-section">
      <div className="rt-header">
        <p className="section-title" style={{ margin: 0 }}>
          Processed Reviews
        </p>
        <span className="rt-count">{filtered.length} of {rows.length} shown</span>
      </div>

      {/* Filters */}
      <div className="rt-filters">
        <div className="rt-filter-group">
          <label className="rt-filter-label">Sentiment</label>
          <div className="rt-pills">
            {['All', 'Positive', 'Neutral', 'Negative'].map(s => (
              <button
                key={s}
                className={`rt-pill ${sentimentFilter === s ? 'rt-pill--active' : ''}`}
                onClick={() => handleFilter(setSentimentFilter)(s)}
              >
                {s}
              </button>
            ))}
          </div>
        </div>
        <div className="rt-filter-group">
          <label className="rt-filter-label">Category</label>
          <select
            className="rt-select"
            value={categoryFilter}
            onChange={e => handleFilter(setCategoryFilter)(e.target.value)}
          >
            {categories.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
        </div>
      </div>

      {/* Table */}
      <div className="rt-wrapper">
        <table className="rt-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Review</th>
              <th>Sentiment</th>
              <th>Score</th>
              <th>Category</th>
              {rows[0]?.date   && <th>Date</th>}
              {rows[0]?.rating && <th>Rating</th>}
            </tr>
          </thead>
          <tbody>
            {paginated.map((row, i) => (
              <tr key={i}>
                <td className="rt-num">{(page - 1) * PAGE_SIZE + i + 1}</td>
                <td className="rt-review">{row.review}</td>
                <td>
                  <span className={`badge ${SENTIMENT_CLS[row.sentiment] ?? 'badge-neutral'}`}>
                    {row.sentiment}
                  </span>
                </td>
                <td className="rt-score">{row.sentiment_score?.toFixed(3)}</td>
                <td className="rt-cat">{row.category}</td>
                {row.date   !== undefined && <td className="rt-date">{String(row.date).slice(0, 10)}</td>}
                {row.rating !== undefined && <td className="rt-rating">{'⭐'.repeat(Math.min(row.rating, 5))}</td>}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="rt-pagination">
          <button className="rt-page-btn" disabled={page === 1} onClick={() => setPage(p => p - 1)}>
            ← Prev
          </button>
          <span className="rt-page-info">Page {page} of {totalPages}</span>
          <button className="rt-page-btn" disabled={page === totalPages} onClick={() => setPage(p => p + 1)}>
            Next →
          </button>
        </div>
      )}
    </div>
  )
}
