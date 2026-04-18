export default function RegimeBadge({ data }) {
  if (!data || !data.regime) return null

  const regime = data.regime

  return (
    <div className="regime-detail-card card" style={{ borderLeft: `3px solid ${regime.color}` }}>
      <div className="regime-title" style={{ color: regime.color }}>
        <span style={{ fontSize: '24px' }}>{regime.icon}</span>
        {regime.name}
      </div>
      <div className="regime-confidence">
        Confidence: {regime.confidence}%
      </div>
      <div className="regime-description">
        {regime.description}
      </div>
      <div className="regime-dispatch-note">
        {regime.dispatch_note}
      </div>
    </div>
  )
}
