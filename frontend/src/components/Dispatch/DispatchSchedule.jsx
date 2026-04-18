export default function DispatchSchedule({ schedule, replayMode, replayData, replayIndex, savingsLabel }) {
  // During replay, show replay-specific schedule
  if (replayMode && replayData) {
    const totalHours = replayData.data.length
    const currentEntry = replayData.data[replayIndex]
    const cumulativeSavings = currentEntry ? currentEntry.cumulative_savings : 0

    return (
      <div className="schedule-section">
        <div className="card-header">REPLAY DISPATCH SCHEDULE</div>
        <div className="schedule-grid">
          {replayData.data.map((entry, i) => (
            <div
              key={i}
              className={`schedule-cell ${i <= replayIndex ? (entry.should_generate ? 'generate' : 'import') : ''}`}
              style={{
                opacity: i <= replayIndex ? 1 : 0.2,
                border: i === replayIndex ? '2px solid #F9FAFB' : 'none',
              }}
              title={`H${entry.hour}: ${entry.date} ${entry.time} | LMP: $${entry.lmp} | Spread: $${entry.spread}`}
            >
              {entry.hour}
            </div>
          ))}
        </div>
        <div className="savings-banner" style={{ borderColor: '#065F46' }}>
          <div className="savings-label">{savingsLabel || 'VALUE CAPTURED'}</div>
          <div className="savings-value" style={{ fontSize: '36px' }}>
            ${cumulativeSavings >= 1000000
              ? `${(cumulativeSavings / 1000000).toFixed(1)}M`
              : cumulativeSavings >= 1000
              ? `${(cumulativeSavings / 1000).toFixed(0)}K`
              : cumulativeSavings.toFixed(0)
            }
          </div>
          <div className="savings-detail">
            Hour {replayIndex + 1} of {totalHours} · 200MW Facility
          </div>
        </div>
      </div>
    )
  }

  if (!schedule || !schedule.schedule) {
    return (
      <div className="schedule-section">
        <div className="card-header">72-HOUR DISPATCH SCHEDULE</div>
        <div style={{ color: 'var(--text-muted)', fontFamily: 'var(--font-mono)', fontSize: '12px', padding: '16px', textAlign: 'center' }}>
          Loading schedule...
        </div>
      </div>
    )
  }

  const generateHours = schedule.schedule.filter(h => h.should_generate).length
  const importHours = schedule.schedule.length - generateHours

  return (
    <div className="schedule-section">
      <div className="card-header">72-HOUR DISPATCH SCHEDULE</div>
      <div className="schedule-grid">
        {schedule.schedule.map((hour, i) => (
          <div
            key={i}
            className={`schedule-cell ${hour.should_generate ? 'generate' : 'import'}`}
            title={`H${hour.hour}: ${hour.recommendation} | Spread: $${hour.spread?.toFixed(1)}/MWh`}
          >
            {hour.hour}
          </div>
        ))}
      </div>
      <div className="savings-banner">
        {importHours > 0 ? (
          <>
            <div className="savings-label">Optimized schedule vs. always-generate:</div>
            <div className="savings-value">
              SAVES ${schedule.savings.total_savings >= 1000000
                ? `${(schedule.savings.total_savings / 1000000).toFixed(2)}M`
                : schedule.savings.total_savings >= 1000
                ? `${(schedule.savings.total_savings / 1000).toFixed(0)}K`
                : schedule.savings.total_savings.toFixed(0)
              }
            </div>
            <div className="savings-detail">
              Avoids {schedule.savings.avoided_uneconomic_hours} hours of uneconomic generation · {generateHours} generate / {importHours} import
            </div>
          </>
        ) : (
          <>
            <div className="savings-label">72-hour generation profit (200MW facility):</div>
            <div className="savings-value">
              +${schedule.savings.total_profit >= 1000000
                ? `${(schedule.savings.total_profit / 1000000).toFixed(2)}M`
                : schedule.savings.total_profit >= 1000
                ? `${(schedule.savings.total_profit / 1000).toFixed(0)}K`
                : (schedule.savings.total_profit || 0).toFixed(0)
              }
            </div>
            <div className="savings-detail">
              All {generateHours} hours profitable — full generation recommended
            </div>
          </>
        )}
      </div>
    </div>
  )
}
