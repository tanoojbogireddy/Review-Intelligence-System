import './KpiStrip.css'

const SENTIMENT_ICONS = { Positive: '✅', Negative: '⚠️', Neutral: '➖' }

export default function KpiStrip({ insights }) {
  const {
    total_reviews,
    sentiment_counts,
    top_negative_issue,
    negative_pct,
    category_counts,
  } = insights

  const pos   = sentiment_counts.Positive ?? 0
  const neg   = sentiment_counts.Negative ?? 0
  const neu   = sentiment_counts.Neutral  ?? 0
  const topCat = Object.entries(category_counts).sort((a, b) => b[1] - a[1])[0]?.[0] ?? '—'

  const cards = [
    {
      id: 'total',
      label: 'Total Reviews',
      value: total_reviews,
      sub: 'processed this session',
      icon: '📋',
      accent: 'blue',
    },
    {
      id: 'positive',
      label: 'Positive',
      value: pos,
      sub: `${Math.round((pos / total_reviews) * 100)}% of reviews`,
      icon: '✅',
      accent: 'green',
    },
    {
      id: 'negative',
      label: 'Negative',
      value: neg,
      sub: `${negative_pct}% of reviews`,
      icon: '⚠️',
      accent: 'red',
    },
    {
      id: 'neutral',
      label: 'Neutral',
      value: neu,
      sub: `${Math.round((neu / total_reviews) * 100)}% of reviews`,
      icon: '➖',
      accent: 'muted',
    },
    {
      id: 'top-issue',
      label: 'Top Issue',
      value: top_negative_issue,
      sub: `Most negative category`,
      icon: '🔥',
      accent: 'orange',
      small: true,
    },
  ]

  return (
    <div className="kpi-strip animate-fade-up">
      {cards.map((card, i) => (
        <div
          key={card.id}
          className={`kpi-card kpi-card--${card.accent}`}
          style={{ animationDelay: `${i * 60}ms` }}
        >
          <div className="kpi-top">
            <span className="kpi-icon">{card.icon}</span>
            <span className="kpi-label">{card.label}</span>
          </div>
          <div className={`kpi-value ${card.small ? 'kpi-value--sm' : ''}`}>
            {card.value}
          </div>
          <div className="kpi-sub">{card.sub}</div>
        </div>
      ))}
    </div>
  )
}
