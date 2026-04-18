import { useState, useEffect } from 'react'
import SiteMap from './SiteMap'
import SiteTable from './SiteTable'
import SiteDetail from './SiteDetail'
import WhyMidlandCard from './WhyMidlandCard'

export default function SiteSelectionTab({ apiBase }) {
  const [sites, setSites] = useState([])
  const [selectedSite, setSelectedSite] = useState(null)
  const [sortKey, setSortKey] = useState('rank')
  const [sortAsc, setSortAsc] = useState(true)

  useEffect(() => {
    fetch(`${apiBase}/api/sites`)
      .then(r => r.json())
      .then(data => {
        setSites(data.sites || [])
        if (data.sites && data.sites.length > 0) {
          setSelectedSite(data.sites[0])
        }
      })
      .catch(err => console.error('Failed to load sites:', err))
  }, [apiBase])

  const handleSort = (key) => {
    if (sortKey === key) {
      setSortAsc(!sortAsc)
    } else {
      setSortKey(key)
      setSortAsc(key === 'rank')
    }
  }

  const sortedSites = [...sites].sort((a, b) => {
    let aVal = a[sortKey]
    let bVal = b[sortKey]
    if (typeof aVal === 'string') {
      return sortAsc ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal)
    }
    return sortAsc ? aVal - bVal : bVal - aVal
  })

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <div className="site-header-strip">
        Historical BTM Spread Analysis · 2019–2024 · 7 Candidate Sites · ERCOT & WECC
      </div>
      <div className="site-selection">
        <div className="map-panel">
          <SiteMap 
            sites={sites} 
            selectedSite={selectedSite} 
            onSelectSite={setSelectedSite} 
          />
        </div>
        <div className="right-panel">
          <SiteTable 
            sites={sortedSites}
            selectedSite={selectedSite}
            onSelectSite={setSelectedSite}
            onSort={handleSort}
            sortKey={sortKey}
            sortAsc={sortAsc}
          />
          {selectedSite && <SiteDetail site={selectedSite} />}
          <WhyMidlandCard />
        </div>
      </div>
    </div>
  )
}
