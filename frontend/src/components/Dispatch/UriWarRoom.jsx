export default function UriWarRoom({ onStartReplay, onStopReplay, replayMode, replayData, replayIndex }) {
  if (replayMode && replayData) {
    const totalHours = replayData.data.length
    const progress = (replayIndex / totalHours) * 100

    return (
      <div className="war-room">
        <div className="war-room-card">
          <div className="war-room-label">● REPLAY MODE ACTIVE</div>
          <div className="war-room-desc">
            Winter Storm Uri · Feb 2021
          </div>
          
          <button className="replay-btn stop" onClick={onStopReplay}>
            ■ ABORT REPLAY
          </button>

          <div className="replay-progress">
            <div className="replay-progress-bar">
              <div 
                className="replay-progress-fill" 
                style={{ width: `${progress}%` }} 
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
    <div className="war-room">
      <div className="war-room-card">
        <div className="war-room-label">WAR ROOM · FEB 2021</div>
        <div className="war-room-desc">
          Replay the Uri winter storm event. See how Dispatch IQ would have performed.
        </div>
        <button className="replay-btn" onClick={onStartReplay}>
          ▶ INITIATE REPLAY
        </button>
      </div>
    </div>
  )
}
