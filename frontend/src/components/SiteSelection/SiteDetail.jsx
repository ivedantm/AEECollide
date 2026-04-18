import { AreaChart, Area, ResponsiveContainer, XAxis, YAxis } from 'recharts'

const REGIME_COLORS = {
  normal: '#6B7280',
  heat_dome: '#F97316',
  wind_glut: '#06B6D4',
  scarcity: '#EF4444',
  oversupply: '#8B5CF6',
  winter_storm: '#3B82F6',
}

const MONTH_LABELS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

export default function SiteDetail({ site }) {
  // Build sparkline data
  const sparklineData = site.monthly_spreads.map((val, i) => ({
    month: MONTH_LABELS[i],
    spread: val,
  }))

  // Build regime breakdown
  const regimeEntries = Object.entries(site.regime_breakdown || {})
  const totalRegime = regimeEntries.reduce((sum, [, v]) => sum + v, 0)

  return (
    <div className="site-detail">
      <h3>{site.label} — Detailed Analysis</h3>

      <div className="detail-grid">
        <div className="detail-stat">
          <div className="detail-stat-label">Avg Spread</div>
          <div className="detail-stat-value">+${site.avg_spread}</div>
        </div>
        <div className="detail-stat">
          <div className="detail-stat-label">Positive Hours</div>
          <div className="detail-stat-value">{site.positive_hours_pct}%</div>
        </div>
        <div className="detail-stat">
          <div className="detail-stat-label">Score</div>
          <div className="detail-stat-value" style={{ color: site.composite_score >= 80 ? '#10B981' : site.composite_score >= 60 ? '#F97316' : '#EF4444' }}>
            {site.composite_score}/100
          </div>
        </div>
        <div className="detail-stat">
          <div className="detail-stat-label">Gas Hub</div>
          <div className="detail-stat-value" style={{ fontSize: '14px', color: '#F9FAFB' }}>
            {site.gas_hub}
          </div>
        </div>
      </div>

      {/* Monthly Spread Sparkline */}
      <div className="card-header" style={{ marginTop: '8px' }}>Monthly Avg Spread (5yr)</div>
      <div className="sparkline-container">
        <ResponsiveContainer width="100%" height={60}>
          <AreaChart data={sparklineData}>
            <defs>
              <linearGradient id="sparkGreen" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#10B981" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#10B981" stopOpacity={0} />
              </linearGradient>
            </defs>
            <Area
              type="monotone"
              dataKey="spread"
              stroke="#10B981"
              strokeWidth={2}
              fill="url(#sparkGreen)"
              dot={false}
            />
            <XAxis dataKey="month" hide />
            <YAxis hide domain={['auto', 'auto']} />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      {/* Regime Breakdown Bar */}
      <div className="card-header">Regime Frequency</div>
      <div className="regime-bar">
        {regimeEntries.map(([regime, pct]) => (
          <div
            key={regime}
            className="regime-bar-segment"
            style={{
              width: `${(pct / totalRegime) * 100}%`,
              background: REGIME_COLORS[regime] || '#6B7280',
            }}
            title={`${regime}: ${pct}%`}
          />
        ))}
      </div>
      <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap', marginBottom: '12px' }}>
        {regimeEntries.map(([regime, pct]) => (
          <div key={regime} style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '10px', fontFamily: 'var(--font-mono)', color: 'var(--text-muted)' }}>
            <div style={{ width: 8, height: 8, borderRadius: 2, background: REGIME_COLORS[regime] }} />
            {regime.replace('_', ' ')}: {pct}%
          </div>
        ))}
      </div>

      {/* Insight */}
      <div className="detail-insight">
        {site.insight}
      </div>
    </div>
  )
}
