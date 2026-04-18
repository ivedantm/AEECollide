export default function AIBriefing({ briefing, replayMode, replayEntry, replayEvent }) {
  if (replayMode && replayEntry) {
    const isNegativeSpread = replayEntry.spread < 0

    if (isNegativeSpread) {
      // Wind glut / negative pricing scenario
      return (
        <div className="ai-briefing card" style={{ background: '#051a1a', borderColor: '#124a4a', flexShrink: 0 }}>
          <div className="briefing-card" style={{ padding: 0 }}>
            <div className="briefing-title" style={{ color: '#06B6D4' }}>🌀 WIND GLUT ALERT</div>
            <div className="briefing-text" style={{ color: '#06B6D4' }}>
              STOP GENERATION IMMEDIATELY. LMP is ${replayEntry.lmp}/MWh — generating now means paying the grid to take your power.
              Import from grid at negative cost. Current savings from import: ${Math.abs(replayEntry.spread).toFixed(0)}/MWh per unit.
            </div>
          </div>
        </div>
      )
    }

    // Emergency / high-value generation scenario
    const isExtreme = replayEntry.lmp > 1000
    return (
      <div className="ai-briefing card" style={{ background: isExtreme ? '#1a0505' : '#111827', borderColor: isExtreme ? '#4a1212' : '#374151', flexShrink: 0 }}>
        <div className="briefing-card" style={{ padding: 0 }}>
          <div className="briefing-title" style={{ color: isExtreme ? '#EF4444' : '#F97316' }}>
            {isExtreme ? '🚨 EMERGENCY DIRECTIVE' : `⚡ ${(replayEvent || 'EVENT').toUpperCase()}`}
          </div>
          <div className="briefing-text" style={{ color: isExtreme ? '#EF4444' : '#FCD34D' }}>
            {isExtreme
              ? `CRITICAL: LMP at $${replayEntry.lmp.toLocaleString()}/MWh. MAXIMUM GENERATION. Every MWh generated avoids catastrophic grid purchase costs. Current generation value: $${(replayEntry.hourly_value).toLocaleString()}/hour for a 200MW facility.`
              : `Grid prices elevated at $${replayEntry.lmp.toLocaleString()}/MWh. Spread is +$${replayEntry.spread.toFixed(0)}/MWh. Sustain generation to capture value. Generation cost at $${replayEntry.gen_cost.toFixed(1)}/MWh remains well below grid price.`
            }
          </div>
        </div>
      </div>
    )
  }

  if (!briefing) {
    return (
      <div className="ai-briefing card" style={{ flexShrink: 0 }}>
        <div className="briefing-title">OPERATOR BRIEFING</div>
        <div className="briefing-text">Generating briefing...</div>
      </div>
    )
  }

  return (
    <div className="ai-briefing card" style={{ flexShrink: 0 }}>
      <div className="briefing-card" style={{ padding: 0 }}>
        <div className="briefing-watermark">OpenAI GPT-4o</div>
        <div className="briefing-title">OPERATOR BRIEFING · Updated {briefing.updated_at}</div>
        <div className="briefing-text">
          {briefing.briefing}
        </div>
      </div>
    </div>
  )
}
