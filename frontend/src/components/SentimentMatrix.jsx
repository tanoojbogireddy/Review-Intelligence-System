import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer,
} from 'recharts'
import './Chart.css'

const COLORS = {
  Positive: '#3fb950',
  Neutral:  '#8b949e',
  Negative: '#f85149',
}

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null
  return (
    <div className="chart-tooltip">
      <div className="chart-tooltip-label">{label}</div>
      {payload.map(p => (
        <div key={p.dataKey} style={{ color: p.fill, fontSize: '0.84rem', marginTop: 3 }}>
          {p.dataKey}: <strong>{p.value}</strong>
        </div>
      ))}
    </div>
  )
}

export default function SentimentMatrix({ data }) {
  const chartData = Object.entries(data).map(([category, counts]) => ({
    category: category.split(' / ')[0], // Shorten "Staff / Service" → "Staff"
    Positive: counts.Positive ?? 0,
    Neutral:  counts.Neutral  ?? 0,
    Negative: counts.Negative ?? 0,
  }))

  return (
    <div className="chart-card card">
      <p className="section-title">Sentiment by Category</p>
      <ResponsiveContainer width="100%" height={280}>
        <BarChart
          data={chartData}
          margin={{ top: 0, right: 8, bottom: 24, left: -12 }}
          barSize={10}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#21262d" vertical={false} />
          <XAxis
            dataKey="category"
            tick={{ fill: '#8b949e', fontSize: 10 }}
            axisLine={false}
            tickLine={false}
            angle={-28}
            textAnchor="end"
          />
          <YAxis
            tick={{ fill: '#8b949e', fontSize: 11 }}
            axisLine={false}
            tickLine={false}
          />
          <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(255,255,255,0.03)' }} />
          <Legend
            iconType="circle"
            iconSize={8}
            wrapperStyle={{ fontSize: '12px', color: '#8b949e', paddingTop: 8 }}
          />
          {['Positive', 'Neutral', 'Negative'].map(key => (
            <Bar key={key} dataKey={key} fill={COLORS[key]} radius={[3, 3, 0, 0]} />
          ))}
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
