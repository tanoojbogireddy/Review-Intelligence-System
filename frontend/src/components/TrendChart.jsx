import {
  LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer,
} from 'recharts'
import './Chart.css'

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null
  return (
    <div className="chart-tooltip">
      <div className="chart-tooltip-label">{label}</div>
      {payload.map(p => (
        <div key={p.dataKey} style={{ color: p.stroke, fontSize: '0.84rem', marginTop: 3 }}>
          {p.name}: <strong>{p.value}</strong>
        </div>
      ))}
    </div>
  )
}

export default function TrendChart({ data }) {
  if (!data || data.length === 0) {
    return (
      <div className="chart-card card trend-empty">
        <p className="section-title">Monthly Review Trend</p>
        <div className="trend-empty-body">
          <div className="trend-empty-icon">📅</div>
          <p>No date column detected.</p>
          <p className="trend-empty-sub">
            Add a <code>date</code> column (YYYY-MM-DD) to your CSV to unlock trend analysis.
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="chart-card card">
      <p className="section-title">Monthly Review Trend</p>
      <ResponsiveContainer width="100%" height={280}>
        <LineChart data={data} margin={{ top: 0, right: 12, bottom: 0, left: -12 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#21262d" />
          <XAxis
            dataKey="month"
            tick={{ fill: '#8b949e', fontSize: 11 }}
            axisLine={false}
            tickLine={false}
          />
          <YAxis
            tick={{ fill: '#8b949e', fontSize: 11 }}
            axisLine={false}
            tickLine={false}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend
            iconType="circle"
            iconSize={8}
            wrapperStyle={{ fontSize: '12px', color: '#8b949e', paddingTop: 8 }}
          />
          <Line
            type="monotone"
            dataKey="total"
            name="Total"
            stroke="#58a6ff"
            strokeWidth={2}
            dot={{ fill: '#58a6ff', r: 4 }}
            activeDot={{ r: 6 }}
          />
          <Line
            type="monotone"
            dataKey="negative"
            name="Negative"
            stroke="#f85149"
            strokeWidth={2}
            strokeDasharray="5 3"
            dot={{ fill: '#f85149', r: 4 }}
            activeDot={{ r: 6 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
