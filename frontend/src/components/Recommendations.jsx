import './Recommendations.css'

const PRIORITY_CLASS = {
  'Critical': 'critical',
  'High':     'high',
  'Medium':   'medium',
}

export default function Recommendations({ recommendations }) {
  if (!recommendations || recommendations.length === 0) {
    return (
      <div className="rec-section">
        <p className="section-title">Actionable Recommendations</p>
        <div className="rec-empty card">
          <span>🎉</span>
          <p>No significant issues detected. Keep up the excellent work!</p>
        </div>
      </div>
    )
  }

  return (
    <div className="rec-section">
      <div className="rec-header">
        <p className="section-title" style={{ margin: 0 }}>Actionable Recommendations</p>
        <span className="rec-count">{recommendations.length} priority areas</span>
      </div>

      <div className="rec-grid">
        {recommendations.map((rec, i) => {
          const priorityWord = rec.priority.split(' ').pop() // "Critical" | "High" | "Medium"
          const cls = PRIORITY_CLASS[priorityWord] ?? 'medium'
          return (
            <div
              key={rec.rank}
              className={`rec-card rec-card--${cls} animate-fade-up`}
              style={{ animationDelay: `${i * 80}ms` }}
            >
              <div className="rec-card-header">
                <div className="rec-rank">#{rec.rank}</div>
                <div className="rec-meta">
                  <div className="rec-category">{rec.category}</div>
                  <div className="rec-stats">
                    <span className={`badge badge-${cls}`}>{rec.priority}</span>
                    <span className="rec-count-text">
                      {rec.negative_count} negative · {rec.share_pct}% of all negatives
                    </span>
                  </div>
                </div>
              </div>

              <div className="rec-actions">
                {rec.actions.map((action, j) => (
                  <div key={j} className="rec-action">
                    <span className="rec-action-bullet" />
                    {action}
                  </div>
                ))}
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
