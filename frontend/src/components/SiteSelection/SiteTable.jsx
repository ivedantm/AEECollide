function getScoreColor(score) {
  if (score >= 80) return '#10B981'
  if (score >= 60) return '#F97316'
  if (score >= 50) return '#EAB308'
  return '#EF4444'
}

export default function SiteTable({ sites, selectedSite, onSelectSite, onSort, sortKey, sortAsc }) {
  const columns = [
    { key: 'rank', label: '#', width: '40px' },
    { key: 'label', label: 'Location', width: 'auto' },
    { key: 'avg_spread', label: 'Avg Spread', width: '100px' },
    { key: 'positive_hours_pct', label: '+ve Hours', width: '80px' },
    { key: 'volatility', label: 'Vol', width: '60px' },
    { key: 'composite_score', label: 'Score', width: '120px' },
  ]

  const sortIndicator = (key) => {
    if (sortKey !== key) return ''
    return sortAsc ? ' ↑' : ' ↓'
  }

  return (
    <div className="site-table-wrapper">
      <table className="site-table">
        <thead>
          <tr>
            {columns.map(col => (
              <th key={col.key} onClick={() => onSort(col.key)} style={{ width: col.width }}>
                {col.label}{sortIndicator(col.key)}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {sites.map(site => (
            <tr
              key={site.id}
              className={`${site.rank === 1 ? 'rank-1' : ''} ${selectedSite && selectedSite.id === site.id ? 'selected' : ''}`}
              onClick={() => onSelectSite(site)}
            >
              <td>{site.rank}</td>
              <td style={{ fontWeight: 500, color: site.rank === 1 ? '#F9FAFB' : undefined }}>
                {site.label}
              </td>
              <td className="spread-positive">+${site.avg_spread}/MWh</td>
              <td>{site.positive_hours_pct}%</td>
              <td>{site.volatility}</td>
              <td>
                <div className="score-bar">
                  <div className="score-bar-track">
                    <div
                      className="score-bar-fill"
                      style={{
                        width: `${site.composite_score}%`,
                        background: getScoreColor(site.composite_score),
                      }}
                    />
                  </div>
                  <span style={{ fontWeight: 600, color: getScoreColor(site.composite_score) }}>
                    {site.composite_score}
                  </span>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
