import { AreaChart, Area, ResponsiveContainer, XAxis, YAxis, ReferenceLine } from 'recharts'

export default function SpreadTicker({ data, flash }) {
  if (!data) {
    return (
      <div className="spread-ticker">
        <div className="ticker-label">Current Spread</div>
        <div className="ticker-value positive">---</div>
      </div>
    )
  }

  const spread = data.spread
  const isPositive = spread >= 0
  const colorClass = isPositive ? 'positive' : 'negative'
  const action = isPositive ? '▲ GENERATE' : '▼ IMPORT'

  // Format the spread value
  const formatSpread = (val) => {
    const abs = Math.abs(val)
    if (abs >= 1000) return `${isPositive ? '+' : '-'}$${(abs / 1000).toFixed(1)}K`
    return `${isPositive ? '+' : '-'}$${abs.toFixed(2)}`
  }

  return (
    <div className="spread-ticker">
      <div className="ticker-label">Current Spread</div>

      <div className={`ticker-value ${colorClass} ${flash ? 'animate-flash' : ''}`}>
        {formatSpread(spread)}
      </div>

      <div className="ticker-unit">/MWh</div>

      <div className={`ticker-action ${colorClass}`}>
        {action}
      </div>

      <div className="ticker-breakdown">
        Grid: ${data.lmp.toFixed(1)}/MWh · Gen cost: ${data.gen_cost.toFixed(1)}/MWh
      </div>

      {/* 24-hour sparkline */}
      {data.history_24h && data.history_24h.length > 0 && (
        <div style={{ marginTop: '16px', height: '50px' }}>
          <ResponsiveContainer width="100%" height={50}>
            <AreaChart data={data.history_24h}>
              <defs>
                <linearGradient id="spreadGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor={isPositive ? '#10B981' : '#EF4444'} stopOpacity={0.3} />
                  <stop offset="95%" stopColor={isPositive ? '#10B981' : '#EF4444'} stopOpacity={0} />
                </linearGradient>
              </defs>
              <Area
                type="monotone"
                dataKey="spread"
                stroke={isPositive ? '#10B981' : '#EF4444'}
                strokeWidth={2}
                fill="url(#spreadGradient)"
                dot={false}
              />
              <ReferenceLine y={0} stroke="#374151" strokeDasharray="3 3" />
              <XAxis dataKey="timestamp" hide />
              <YAxis hide domain={['auto', 'auto']} />
            </AreaChart>
          </ResponsiveContainer>
          <div style={{ textAlign: 'center', fontFamily: 'var(--font-mono)', fontSize: '9px', color: 'var(--text-muted)', marginTop: '4px' }}>
            24-HOUR SPREAD HISTORY
          </div>
        </div>
      )}
    </div>
  )
}
