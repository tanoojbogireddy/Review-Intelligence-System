import './Header.css'

export default function Header({ onReset, hasData }) {
  return (
    <header className="header">
      <div className="container header-inner">
        <div className="header-brand" onClick={hasData ? onReset : undefined} style={{ cursor: hasData ? 'pointer' : 'default' }}>
          <div className="header-logo">
            <span className="logo-icon">🧠</span>
          </div>
          <div>
            <div className="header-title">RIAS</div>
            <div className="header-sub">Review Intelligence System</div>
          </div>
        </div>

        <div className="header-right">
          <div className="engine-badge">
            <span className="engine-dot" />
            Rule-based Engine
          </div>
          {hasData && (
            <button className="btn-ghost header-reset" onClick={onReset}>
              ← New Analysis
            </button>
          )}
        </div>
      </div>
    </header>
  )
}
