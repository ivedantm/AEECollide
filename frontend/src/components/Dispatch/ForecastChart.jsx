import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, ReferenceLine
} from 'recharts'

function CustomTooltip({ active, payload, label }) {
  if (!active || !payload || !payload.length) return null
  const d = payload[0]?.payload
  if (!d) return null

  return (
    <div className="custom-tooltip">
      <div className="tooltip-label">{d.day_label || `Hour ${d.hour}`}</div>
      <div className="tooltip-row">
        <span>p90:</span>
        <span style={{ color: '#10B981', fontWeight: 600 }}>+${d.spread_p90?.toFixed(1)}/MWh</span>
      </div>
      <div className="tooltip-row">
        <span>p50:</span>
        <span style={{ color: '#F9FAFB', fontWeight: 600 }}>
          {d.spread_p50 >= 0 ? '+' : ''}${d.spread_p50?.toFixed(1)}/MWh
        </span>
      </div>
      <div className="tooltip-row">
        <span>p10:</span>
        <span style={{ color: d.spread_p10 >= 0 ? '#10B981' : '#EF4444', fontWeight: 600 }}>
          {d.spread_p10 >= 0 ? '+' : ''}${d.spread_p10?.toFixed(1)}/MWh
        </span>
      </div>
      <div style={{ borderTop: '1px solid #374151', marginTop: '6px', paddingTop: '6px', color: d.should_generate ? '#10B981' : '#EF4444', fontWeight: 700 }}>
        {d.recommendation}
      </div>
    </div>
  )
}

export default function ForecastChart({ forecast, replayMode, replayData, replayIndex }) {
  // During replay, show the historical LMP data
  if (replayMode && replayData) {
    const replayChartData = replayData.data.slice(0, replayIndex + 1).map(d => ({
      hour: d.hour,
      day_label: `${d.date} ${d.time}`,
      lmp: d.lmp,
      gen_cost: d.gen_cost,
      spread: d.spread,
    }))

    return (
      <div className="forecast-section">
        <div className="card-header">
          REPLAY · ERCOT WEST HUB LMP · FEB 2021
        </div>
        <div className="forecast-chart-container">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={replayChartData}>
              <defs>
                <linearGradient id="replayLMP" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#EF4444" stopOpacity={0.4} />
                  <stop offset="95%" stopColor="#EF4444" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#1F2937" />
              <XAxis
                dataKey="hour"
                tick={{ fontSize: 10, fill: '#6B7280' }}
                tickFormatter={(h) => `H${h}`}
                interval={6}
              />
              <YAxis
                tick={{ fontSize: 10, fill: '#6B7280' }}
                tickFormatter={(v) => v >= 1000 ? `$${(v/1000).toFixed(0)}K` : `$${v}`}
              />
              <Tooltip
                content={({ active, payload }) => {
                  if (!active || !payload?.length) return null
                  const d = payload[0].payload
                  return (
                    <div className="custom-tooltip">
                      <div className="tooltip-label">{d.day_label}</div>
                      <div className="tooltip-row">
                        <span>LMP:</span>
                        <span style={{ color: '#EF4444', fontWeight: 600 }}>${d.lmp.toLocaleString()}/MWh</span>
                      </div>
                      <div className="tooltip-row">
                        <span>Gen Cost:</span>
                        <span style={{ color: '#F9FAFB' }}>${d.gen_cost.toFixed(1)}/MWh</span>
                      </div>
                      <div className="tooltip-row">
                        <span>Spread:</span>
                        <span style={{ color: '#10B981', fontWeight: 600 }}>+${d.spread.toLocaleString()}/MWh</span>
                      </div>
                    </div>
                  )
                }}
              />
              <Area
                type="monotone"
                dataKey="lmp"
                stroke="#EF4444"
                strokeWidth={2}
                fill="url(#replayLMP)"
                dot={false}
              />
              <Area
                type="monotone"
                dataKey="gen_cost"
                stroke="#F97316"
                strokeWidth={1}
                strokeDasharray="4 4"
                fill="none"
                dot={false}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>
    )
  }

  if (!forecast || !forecast.forecast) {
    return (
      <div className="forecast-section">
        <div className="card-header">72-HOUR SPREAD FORECAST</div>
        <div className="forecast-chart-container" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)', fontSize: '12px' }}>
          Loading forecast data...
        </div>
      </div>
    )
  }

  return (
    <div className="forecast-section">
      <div className="card-header">72-HOUR SPREAD FORECAST · P10 / P50 / P90</div>
      <div className="forecast-chart-container">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={forecast.forecast}>
            <defs>
              <linearGradient id="p90Fill" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#10B981" stopOpacity={0.15} />
                <stop offset="95%" stopColor="#10B981" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="p10Fill" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#EF4444" stopOpacity={0} />
                <stop offset="95%" stopColor="#EF4444" stopOpacity={0.15} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#1F2937" />
            <XAxis
              dataKey="hour"
              tick={{ fontSize: 10, fill: '#6B7280' }}
              tickFormatter={(h) => {
                if (h % 6 === 0) return `H${h}`
                return ''
              }}
              interval={0}
            />
            <YAxis
              tick={{ fontSize: 10, fill: '#6B7280' }}
              tickFormatter={(v) => `$${v}`}
            />
            <ReferenceLine y={0} stroke="#6B7280" strokeDasharray="6 4" strokeWidth={1.5} />
            <Tooltip content={<CustomTooltip />} />
            <Area
              type="monotone"
              dataKey="spread_p90"
              stroke="transparent"
              fill="url(#p90Fill)"
              dot={false}
            />
            <Area
              type="monotone"
              dataKey="spread_p50"
              stroke="#10B981"
              strokeWidth={2}
              fill="none"
              dot={false}
            />
            <Area
              type="monotone"
              dataKey="spread_p10"
              stroke="transparent"
              fill="url(#p10Fill)"
              dot={false}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
