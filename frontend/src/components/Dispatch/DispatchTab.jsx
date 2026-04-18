import { useState, useEffect, useCallback } from 'react'
import StatusBar from './StatusBar'
import SpreadTicker from './SpreadTicker'
import RegimeBadge from './RegimeBadge'
import ForecastChart from './ForecastChart'
import DispatchSchedule from './DispatchSchedule'
import AIBriefing from './AIBriefing'
import ScenarioPanel from './ScenarioPanel'
import SiteSelector from './SiteSelector'

export default function DispatchTab({ apiBase }) {
  const [dispatchData, setDispatchData] = useState(null)
  const [forecast, setForecast] = useState(null)
  const [schedule, setSchedule] = useState(null)
  const [briefing, setBriefing] = useState(null)
  const [selectedSiteId, setSelectedSiteId] = useState('midland')

  // Replay state
  const [replayMode, setReplayMode] = useState(false)
  const [replayData, setReplayData] = useState(null)
  const [replayIndex, setReplayIndex] = useState(0)
  const [showSummary, setShowSummary] = useState(false)
  const [flashTicker, setFlashTicker] = useState(false)
  const [activeScenarioId, setActiveScenarioId] = useState(null)

  const fetchAllData = useCallback(() => {
    if (replayMode) return

    fetch(`${apiBase}/api/dispatch/current?site_id=${selectedSiteId}`)
      .then(r => r.json())
      .then(data => setDispatchData(data))
      .catch(err => console.error('Dispatch fetch error:', err))

    fetch(`${apiBase}/api/dispatch/forecast?site_id=${selectedSiteId}`)
      .then(r => r.json())
      .then(data => setForecast(data))
      .catch(err => console.error('Forecast fetch error:', err))

    fetch(`${apiBase}/api/dispatch/schedule?site_id=${selectedSiteId}`)
      .then(r => r.json())
      .then(data => setSchedule(data))
      .catch(err => console.error('Schedule fetch error:', err))

    fetch(`${apiBase}/api/dispatch/briefing?site_id=${selectedSiteId}`)
      .then(r => r.json())
      .then(data => setBriefing(data))
      .catch(err => console.error('Briefing fetch error:', err))
  }, [apiBase, replayMode, selectedSiteId])

  useEffect(() => {
    fetchAllData()
  }, [fetchAllData])

  // Handle site change
  const handleSiteChange = (siteId) => {
    setSelectedSiteId(siteId)
    // Reset data while new site loads
    setDispatchData(null)
    setForecast(null)
    setSchedule(null)
    setBriefing(null)
  }

  // Start a replay scenario
  const startReplay = (scenarioId) => {
    fetch(`${apiBase}/api/replay/${scenarioId}`)
      .then(r => r.json())
      .then(data => {
        if (data.error) {
          console.error(data.error)
          return
        }
        setReplayData(data)
        setReplayMode(true)
        setReplayIndex(0)
        setShowSummary(false)
        setActiveScenarioId(scenarioId)
      })
  }

  const stopReplay = () => {
    setReplayMode(false)
    setReplayData(null)
    setReplayIndex(0)
    setShowSummary(false)
    setActiveScenarioId(null)
    fetchAllData()
  }

  // Replay animation loop
  useEffect(() => {
    if (!replayMode || !replayData) return

    const totalHours = replayData.data.length
    const intervalMs = (60 * 1000) / totalHours // 60 seconds total

    const timer = setInterval(() => {
      setReplayIndex(prev => {
        const next = prev + 1
        if (next >= totalHours) {
          clearInterval(timer)
          setShowSummary(true)
          return totalHours - 1
        }
        setFlashTicker(true)
        setTimeout(() => setFlashTicker(false), 400)
        return next
      })
    }, intervalMs)

    return () => clearInterval(timer)
  }, [replayMode, replayData])

  // Build replay dispatch data
  const currentReplayEntry = replayMode && replayData ? replayData.data[replayIndex] : null

  const displayData = replayMode && currentReplayEntry ? {
    lmp: currentReplayEntry.lmp,
    gas_price: currentReplayEntry.gas_price,
    gas_hub: 'Waha',
    gen_cost: currentReplayEntry.gen_cost,
    spread: currentReplayEntry.spread,
    decision: {
      action: currentReplayEntry.recommendation,
      icon: currentReplayEntry.should_generate ? '▲' : '▼',
      color: currentReplayEntry.should_generate ? 'green' : 'red',
    },
    regime: {
      id: currentReplayEntry.regime,
      name: currentReplayEntry.regime === 'uri_emergency' ? 'URI EMERGENCY' :
            currentReplayEntry.regime === 'winter_storm' ? 'Winter Storm' :
            currentReplayEntry.regime === 'scarcity' ? 'Scarcity Pricing' :
            currentReplayEntry.regime === 'heat_dome' ? 'Heat Dome' :
            currentReplayEntry.regime === 'wind_glut' ? 'Wind Glut' :
            currentReplayEntry.regime === 'oversupply' ? 'Oversupply' :
            'Normal Operations',
      icon: currentReplayEntry.regime === 'uri_emergency' ? '🚨' :
            currentReplayEntry.regime === 'winter_storm' ? '❄️' :
            currentReplayEntry.regime === 'scarcity' ? '⚡' :
            currentReplayEntry.regime === 'heat_dome' ? '🔥' :
            currentReplayEntry.regime === 'wind_glut' ? '🌀' :
            currentReplayEntry.regime === 'oversupply' ? '📉' : '✅',
      color: currentReplayEntry.regime === 'uri_emergency' ? '#FF0000' :
             currentReplayEntry.regime === 'winter_storm' ? '#3B82F6' :
             currentReplayEntry.regime === 'scarcity' ? '#EF4444' :
             currentReplayEntry.regime === 'heat_dome' ? '#F97316' :
             currentReplayEntry.regime === 'wind_glut' ? '#06B6D4' :
             currentReplayEntry.regime === 'oversupply' ? '#8B5CF6' : '#6B7280',
      badge_bg: currentReplayEntry.regime === 'uri_emergency' ? '#450A0A' :
                currentReplayEntry.regime === 'winter_storm' ? '#1E3A5F' :
                currentReplayEntry.regime === 'scarcity' ? '#7F1D1D' :
                currentReplayEntry.regime === 'heat_dome' ? '#7C2D12' :
                currentReplayEntry.regime === 'wind_glut' ? '#164E63' :
                currentReplayEntry.regime === 'oversupply' ? '#3B0764' : '#1F2937',
      description: currentReplayEntry.regime === 'uri_emergency' ? 'CRITICAL: System-wide emergency. Rolling blackouts in effect. LMP at system cap.' :
                   currentReplayEntry.regime === 'winter_storm' ? 'Cold weather event stressing heating demand. Gas supply disruptions possible.' :
                   currentReplayEntry.regime === 'scarcity' ? 'Operating reserves below threshold. ERCOT deploying emergency pricing adders.' :
                   currentReplayEntry.regime === 'heat_dome' ? 'Extreme heat driving record AC load. Grid reserves thinning.' :
                   currentReplayEntry.regime === 'wind_glut' ? 'Massive wind output exceeding demand. Prices going negative — IMPORT from grid.' :
                   currentReplayEntry.regime === 'oversupply' ? 'Renewable generation exceeding demand. Low or negative pricing.' :
                   'Grid operating within normal parameters.',
      dispatch_note: currentReplayEntry.regime === 'uri_emergency' ? 'MAXIMUM GENERATION. Every MWh generated avoids catastrophic grid purchase costs.' :
                     currentReplayEntry.regime === 'winter_storm' ? 'Gas prices may spike due to supply constraints. Monitor fuel availability closely.' :
                     currentReplayEntry.regime === 'scarcity' ? 'LMP includes scarcity adders. Maximize generation.' :
                     currentReplayEntry.regime === 'heat_dome' ? 'Sustained high spreads expected through evening. Maximize output.' :
                     currentReplayEntry.regime === 'wind_glut' ? 'STOP GENERATION. Grid is paying you to take power. Import immediately.' :
                     currentReplayEntry.regime === 'oversupply' ? 'Spreads compressed. Consider reducing generation.' :
                     'Follow standard dispatch schedule.',
      confidence: currentReplayEntry.regime === 'uri_emergency' ? 99 :
                  currentReplayEntry.regime === 'winter_storm' ? 92 :
                  currentReplayEntry.regime === 'scarcity' ? 88 :
                  currentReplayEntry.regime === 'heat_dome' ? 90 :
                  currentReplayEntry.regime === 'wind_glut' ? 85 : 70,
    },
    settlement_point: replayData.location?.includes('Houston') ? 'LZ_HOUSTON' : 'LZ_WEST',
    location: replayData.location || 'Midland TX',
    heat_rate: 7.5,
    facility_mw: 200,
    timestamp: `${currentReplayEntry.date} ${currentReplayEntry.time}`,
    temp_f: currentReplayEntry.temp_f,
    history_24h: replayData.data.slice(Math.max(0, replayIndex - 24), replayIndex + 1).map((d, i) => ({
      hour: i,
      timestamp: d.time,
      lmp: d.lmp,
      spread: d.spread,
    })),
  } : dispatchData

  // Determine the savings label based on scenario
  const getSavingsLabel = () => {
    if (!activeScenarioId) return 'STRANDED COSTS AVOIDED'
    if (activeScenarioId === 'wind_glut_2024') return 'LOSS AVOIDED BY IMPORTING'
    return 'VALUE CAPTURED BY DISPATCH IQ'
  }

  return (
    <div className="dispatch-layout">
      <StatusBar
        data={displayData}
        replayMode={replayMode}
        replayEntry={currentReplayEntry}
        replayEvent={replayData?.event}
      >
        <SiteSelector
          apiBase={apiBase}
          selectedSiteId={selectedSiteId}
          onSiteChange={handleSiteChange}
          disabled={replayMode}
        />
      </StatusBar>

      <div className="dispatch-columns">
        {/* Left Column */}
        <div className="dispatch-left">
          <SpreadTicker
            data={displayData}
            flash={flashTicker}
          />
          <RegimeBadge data={displayData} />
        </div>

        {/* Center Column */}
        <div className="dispatch-center">
          <ForecastChart
            forecast={replayMode ? null : forecast}
            replayMode={replayMode}
            replayData={replayData}
            replayIndex={replayIndex}
          />
          <DispatchSchedule
            schedule={replayMode ? null : schedule}
            replayMode={replayMode}
            replayData={replayData}
            replayIndex={replayIndex}
            savingsLabel={getSavingsLabel()}
          />
        </div>

        {/* Right Column */}
        <div className="dispatch-right">
          <AIBriefing
            briefing={replayMode ? null : briefing}
            replayMode={replayMode}
            replayEntry={currentReplayEntry}
            replayEvent={replayData?.event}
          />
          <ScenarioPanel
            apiBase={apiBase}
            onStartReplay={startReplay}
            onStopReplay={stopReplay}
            replayMode={replayMode}
            replayData={replayData}
            replayIndex={replayIndex}
            activeScenarioId={activeScenarioId}
          />
        </div>
      </div>

      {/* Summary Overlay */}
      {showSummary && replayData && (
        <div className="uri-overlay" onClick={() => setShowSummary(false)}>
          <div className="uri-summary-card" onClick={e => e.stopPropagation()}
               style={{ borderColor: replayData.color || '#10B981' }}>
            <div className="uri-summary-facility">200MW FACILITY · {replayData.location || 'ERCOT WEST'}</div>
            <div className="uri-summary-event">{replayData.event} · {replayData.period}</div>
            <div className="uri-summary-value" style={{ color: replayData.color || '#10B981', textShadow: `0 0 40px ${replayData.color || '#10B981'}40` }}>
              ${(replayData.data[replayData.data.length - 1].cumulative_savings / 1000000).toFixed(1)}M
            </div>
            <div className="uri-summary-label">
              {activeScenarioId === 'wind_glut_2024'
                ? 'In Losses Avoided By Following Dispatch IQ Import Signal'
                : 'In Value Captured By Following Dispatch IQ Signal'
              }
            </div>
            <button className="uri-dismiss-btn" onClick={stopReplay}>
              ← RETURN TO LIVE
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
