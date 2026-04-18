import { useState, useEffect } from 'react'

const SCENARIO_STYLES = {
  uri_2021: { bg: '#1a0505', border: '#4a1212', color: '#EF4444' },
  heat_dome_2023: { bg: '#1a0f05', border: '#4a3012', color: '#F97316' },
  wind_glut_2024: { bg: '#051a1a', border: '#124a4a', color: '#06B6D4' },
}

export default function ScenarioPanel({ apiBase, onStartReplay, onStopReplay, replayMode, replayData, replayIndex, activeScenarioId }) {
  const [scenarios, setScenarios] = useState([])

  useEffect(() => {
    fetch(`${apiBase}/api/replay/scenarios`)
      .then(r => r.json())
      .then(data => setScenarios(data.scenarios || []))
      .catch(() => {
        // Fallback hardcoded scenarios
        setScenarios([
          { id: 'uri_2021', name: 'Winter Storm Uri', icon: '❄️', period: 'Feb 2021', description: 'Grid collapse, $9K/MWh cap, rolling blackouts.', color: '#3B82F6' },
          { id: 'heat_dome_2023', name: 'Heat Dome', icon: '🔥', period: 'Aug 2023', description: '116°F, LMP hit $5K/MWh at peak AC load.', color: '#F97316' },
          { id: 'wind_glut_2024', name: 'Wind Glut', icon: '🌀', period: 'Apr 2024', description: 'Negative pricing — why NOT generating saves money.', color: '#06B6D4' },
        ])
      })
  }, [apiBase])

  // Active replay progress
  if (replayMode && replayData) {
    const totalHours = replayData.data.length
    const progress = (replayIndex / totalHours) * 100
    const style = SCENARIO_STYLES[activeScenarioId] || SCENARIO_STYLES.uri_2021

    return (
      <div className="war-room">
        <div className="war-room-card" style={{ background: style.bg, borderColor: style.border }}>
          <div className="war-room-label" style={{ color: style.color }}>
            ● REPLAY: {replayData.event?.toUpperCase()}
          </div>
          <div className="war-room-desc">{replayData.period}</div>

          <button className="replay-btn stop" onClick={onStopReplay}>
            ■ ABORT REPLAY
          </button>

          <div className="replay-progress">
            <div className="replay-progress-bar">
              <div
                className="replay-progress-fill"
                style={{ width: `${progress}%`, background: style.color }}
              />
            </div>
            <div className="replay-counter">
              HOUR {replayIndex + 1} OF {totalHours}
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="war-room" style={{ padding: '12px' }}>
      <div className="card-header" style={{ marginBottom: '12px', paddingLeft: '4px' }}>
        HISTORICAL SCENARIOS
      </div>
      {scenarios.map(scenario => {
        const style = SCENARIO_STYLES[scenario.id] || { bg: '#111827', border: '#374151', color: '#6B7280' }
        return (
          <div
            key={scenario.id}
            style={{
              background: style.bg,
              border: `1px solid ${style.border}`,
              borderRadius: 'var(--radius-md)',
              padding: '14px 16px',
              marginBottom: '8px',
              cursor: 'pointer',
              transition: 'all 0.2s',
            }}
            onMouseEnter={e => { e.currentTarget.style.borderColor = style.color; e.currentTarget.style.transform = 'translateY(-1px)' }}
            onMouseLeave={e => { e.currentTarget.style.borderColor = style.border; e.currentTarget.style.transform = 'none' }}
          >
            <div style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              marginBottom: '6px',
            }}>
              <div style={{
                fontFamily: 'var(--font-mono)',
                fontSize: '12px',
                fontWeight: 700,
                color: style.color,
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
              }}>
                <span style={{ fontSize: '16px' }}>{scenario.icon}</span>
                {scenario.name}
              </div>
              <span style={{
                fontFamily: 'var(--font-mono)',
                fontSize: '10px',
                color: 'var(--text-muted)',
              }}>
                {scenario.period}
              </span>
            </div>

            <div style={{
              fontFamily: 'var(--font-mono)',
              fontSize: '11px',
              color: 'var(--text-muted)',
              lineHeight: '1.4',
              marginBottom: '10px',
            }}>
              {scenario.description}
            </div>

            <button
              onClick={(e) => { e.stopPropagation(); onStartReplay(scenario.id) }}
              style={{
                width: '100%',
                padding: '8px',
                background: style.color,
                border: 'none',
                borderRadius: 'var(--radius-sm)',
                color: '#fff',
                fontFamily: 'var(--font-mono)',
                fontSize: '11px',
                fontWeight: 700,
                letterSpacing: '1px',
                cursor: 'pointer',
                transition: 'all 0.2s',
              }}
              onMouseEnter={e => e.target.style.opacity = '0.85'}
              onMouseLeave={e => e.target.style.opacity = '1'}
            >
              ▶ REPLAY
            </button>
          </div>
        )
      })}
    </div>
  )
}
