export default function StatusBar({ data, replayMode, replayEntry, replayEvent, children }) {
  if (!data) return <div className="status-bar">Loading...</div>

  return (
    <div className={`status-bar ${replayMode ? 'replay-mode' : ''}`}>
      <div className="status-item">
        {replayMode ? (
          <span className="regime-badge" style={{ background: '#7F1D1D', color: '#EF4444' }}>
            ● REPLAY: {replayEvent || 'HISTORICAL'}
          </span>
        ) : (
          <span className="regime-badge" style={{ background: '#065F46', color: '#10B981' }}>
            <span className="live-dot" style={{ width: 6, height: 6 }}></span> LIVE
          </span>
        )}
      </div>

      {/* Site Selector */}
      {!replayMode && children}

      <div className="status-item">
        <span className="status-value">{data.settlement_point}</span>
        <span className="status-label">· {data.location}</span>
      </div>

      <span className="status-divider">|</span>

      {replayMode && replayEntry && (
        <>
          <div className="status-item">
            <span className="status-label">Date:</span>
            <span className="status-value">{replayEntry.date} {replayEntry.time} CST</span>
          </div>
          <span className="status-divider">|</span>
          <div className="status-item">
            <span className="status-label">Temp:</span>
            <span className="status-value" style={{ color: replayEntry.temp_f <= 0 ? '#3B82F6' : replayEntry.temp_f >= 100 ? '#EF4444' : '#F9FAFB' }}>
              {replayEntry.temp_f}°F
            </span>
          </div>
          <span className="status-divider">|</span>
        </>
      )}

      {!replayMode && (
        <div className="status-item">
          <span className="status-label">Last Pull:</span>
          <span className="status-value">{new Date(data.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})} CST</span>
        </div>
      )}

      <span className="status-divider">|</span>

      <div className="status-item">
        <span className="status-label">Gas:</span>
        <span className="status-value">${data.gas_price}/MMBtu ({data.gas_hub})</span>
      </div>

      <span className="status-divider">|</span>

      <div className="status-item">
        <span className="status-label">Heat Rate:</span>
        <span className="status-value">{data.heat_rate}</span>
      </div>

      <span className="status-divider">|</span>

      <div className="status-item">
        <span className="status-label">Gen Cost:</span>
        <span className="status-value">${data.gen_cost}/MWh</span>
      </div>

      <span className="status-divider">|</span>

      {data.regime && (
        <span
          className="regime-badge"
          style={{
            background: data.regime.badge_bg,
            color: data.regime.color,
          }}
        >
          {data.regime.icon} {data.regime.name} · {data.regime.confidence}%
        </span>
      )}
    </div>
  )
}
