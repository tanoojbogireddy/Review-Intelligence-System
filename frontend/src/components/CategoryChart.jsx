import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, Cell,
} from 'recharts'
import './Chart.css'

const COLORS = [
  '#58a6ff', '#3fb950', '#f78166', '#d29922',
  '#a371f7', '#79c0ff', '#ffa657', '#56d364',
]

const CustomTooltip = ({ active, payload }) => {
  if (!active || !payload?.length) return null
  return (
    <div className="chart-tooltip">
      <div className="chart-tooltip-label">{payload[0].payload.category}</div>
      <div className="chart-tooltip-value">{payload[0].value} reviews</div>
    </div>
  )
}

export default function CategoryChart({ data }) {
  const chartData = Object.entries(data)
    .sort((a, b) => b[1] - a[1])
    .map(([category, count]) => ({ category, count }))

  return (
    <div className="chart-card card">
      <p className="section-title">Reviews by Category</p>
      <ResponsiveContainer width="100%" height={280}>
        <BarChart
          data={chartData}
          layout="vertical"
          margin={{ top: 0, right: 24, bottom: 0, left: 0 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#21262d" horizontal={false} />
          <XAxis
            type="number"
            tick={{ fill: '#8b949e', fontSize: 11 }}
            axisLine={false}
            tickLine={false}
          />
          <YAxis
            type="category"
            dataKey="category"
            tick={{ fill: '#8b949e', fontSize: 11 }}
            axisLine={false}
            tickLine={false}
            width={110}
          />
          <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(255,255,255,0.03)' }} />
          <Bar dataKey="count" radius={[0, 6, 6, 0]} maxBarSize={26}>
            {chartData.map((_, i) => (
              <Cell key={i} fill={COLORS[i % COLORS.length]} fillOpacity={0.9} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
