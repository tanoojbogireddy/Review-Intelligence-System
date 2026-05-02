import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import './Chart.css'

const COLORS = {
  Positive: '#3fb950',
  Neutral:  '#8b949e',
  Negative: '#f85149',
}

const CustomTooltip = ({ active, payload }) => {
  if (!active || !payload?.length) return null
  const total = payload[0].payload.total
  const val   = payload[0].value
  return (
    <div className="chart-tooltip">
      <div className="chart-tooltip-label">{payload[0].name}</div>
      <div className="chart-tooltip-value">{val} reviews ({Math.round(val / total * 100)}%)</div>
    </div>
  )
}

const renderCustomLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent, name }) => {
  const RADIAN = Math.PI / 180
  const radius = innerRadius + (outerRadius - innerRadius) * 0.5
  const x = cx + radius * Math.cos(-midAngle * RADIAN)
  const y = cy + radius * Math.sin(-midAngle * RADIAN)
  if (percent < 0.06) return null
  return (
    <text x={x} y={y} fill="#fff" textAnchor="middle" dominantBaseline="central"
          fontSize={11} fontWeight={600}>
      {`${(percent * 100).toFixed(0)}%`}
    </text>
  )
}

export default function SentimentDonut({ data }) {
  const total = Object.values(data).reduce((a, b) => a + b, 0)
  const chartData = Object.entries(data).map(([name, value]) => ({
    name, value, total,
  }))

  return (
    <div className="chart-card card">
      <p className="section-title">Sentiment Distribution</p>
      <ResponsiveContainer width="100%" height={280}>
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            innerRadius={72}
            outerRadius={110}
            paddingAngle={3}
            dataKey="value"
            labelLine={false}
            label={renderCustomLabel}
          >
            {chartData.map((entry) => (
              <Cell
                key={entry.name}
                fill={COLORS[entry.name] || '#58a6ff'}
                stroke="transparent"
              />
            ))}
          </Pie>
          <Tooltip content={<CustomTooltip />} />
          <Legend
            iconType="circle"
            iconSize={8}
            wrapperStyle={{ fontSize: '12px', color: '#8b949e', paddingTop: 12 }}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  )
}
