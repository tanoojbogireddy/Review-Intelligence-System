import './ExportBar.css'

function rowsToCsv(rows) {
  if (!rows || rows.length === 0) return ''
  const cols = Object.keys(rows[0])
  const header = cols.join(',')
  const lines = rows.map(row =>
    cols.map(c => {
      const val = row[c] ?? ''
      return typeof val === 'string' && (val.includes(',') || val.includes('"') || val.includes('\n'))
        ? `"${val.replace(/"/g, '""')}"`
        : val
    }).join(',')
  )
  return [header, ...lines].join('\n')
}

function downloadCsv(content, filename) {
  const blob = new Blob([content], { type: 'text/csv;charset=utf-8;' })
  const url  = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.setAttribute('href', url)
  link.setAttribute('download', filename)
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
}

export default function ExportBar({ rows, fileName }) {
  const baseName = fileName?.replace(/\.csv$/i, '') ?? 'rias_results'

  const handleDownload = () => {
    const csv = rowsToCsv(rows)
    downloadCsv(csv, `${baseName}_processed.csv`)
  }

  return (
    <div className="export-bar">
      <div className="export-info">
        <span className="export-icon">📥</span>
        <div>
          <div className="export-title">Export Results</div>
          <div className="export-sub">{rows.length} processed reviews ready to download</div>
        </div>
      </div>
      <button className="btn-primary export-btn" onClick={handleDownload}>
        ⬇ Download CSV
      </button>
    </div>
  )
}
