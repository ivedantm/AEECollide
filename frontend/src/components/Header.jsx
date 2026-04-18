export default function Header({ activeTab, setActiveTab, lastUpdated }) {
  return (
    <header className="header">
      <div className="header-left">
        <div>
          <div className="logo">DISPATCH IQ</div>
          <div className="logo-sub">Powered by ERCOT · EIA · AI</div>
        </div>
      </div>

      <div className="header-center">
        <button
          className={`tab-btn ${activeTab === 'sites' ? 'active' : ''}`}
          onClick={() => setActiveTab('sites')}
        >
          Site Selection
        </button>
        <button
          className={`tab-btn ${activeTab === 'dispatch' ? 'active' : ''}`}
          onClick={() => setActiveTab('dispatch')}
        >
          Dispatch
        </button>
      </div>

      <div className="header-right">
        <div className="live-indicator">
          <span className="live-dot"></span>
          LIVE
        </div>
        <span className="last-updated">Last updated: {lastUpdated}</span>
      </div>
    </header>
  )
}
