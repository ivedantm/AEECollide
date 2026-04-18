import { useEffect, useRef } from 'react'
import { MapContainer, TileLayer, CircleMarker, Polyline, Tooltip, useMap } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'

function MapUpdater({ center }) {
  const map = useMap()
  useEffect(() => {
    if (center) {
      map.flyTo(center, map.getZoom(), { duration: 0.5 })
    }
  }, [center, map])
  return null
}

function getColor(score) {
  if (score >= 80) return '#10B981'
  if (score >= 60) return '#F97316'
  if (score >= 50) return '#EAB308'
  return '#EF4444'
}

function getRadius(score) {
  return 8 + (score / 100) * 14
}

export default function SiteMap({ sites, selectedSite, onSelectSite }) {
  const center = [31.5, -101.0]

  // Pipeline hub locations
  const wahaHub = { lat: 31.38, lng: -103.15, name: 'Waha Hub' }
  const henryHub = { lat: 29.95, lng: -93.85, name: 'Henry Hub' }

  return (
    <MapContainer
      center={center}
      zoom={6}
      style={{ height: '100%', width: '100%' }}
      zoomControl={false}
      attributionControl={false}
    >
      <TileLayer
        url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
        attribution='&copy; <a href="https://carto.com/">CARTO</a>'
      />

      {/* Pipeline connection lines */}
      {sites.map(site => {
        const hub = site.gas_hub === 'Waha' ? wahaHub : 
                    site.gas_hub === 'Henry Hub' ? henryHub : null
        if (!hub) return null
        return (
          <Polyline
            key={`line-${site.id}`}
            positions={[[site.lat, site.lng], [hub.lat, hub.lng]]}
            pathOptions={{
              color: '#374151',
              weight: 1,
              dashArray: '4 6',
              opacity: 0.5,
            }}
          />
        )
      })}

      {/* Hub markers */}
      <CircleMarker
        center={[wahaHub.lat, wahaHub.lng]}
        radius={5}
        pathOptions={{ color: '#F97316', fillColor: '#F97316', fillOpacity: 0.8, weight: 1 }}
      >
        <Tooltip className="map-tooltip" permanent={false}>
          <div className="tooltip-title">⛽ Waha Hub</div>
          <div style={{ color: '#9CA3AF', fontSize: '11px' }}>Gas Pipeline Hub · West Texas</div>
        </Tooltip>
      </CircleMarker>

      <CircleMarker
        center={[henryHub.lat, henryHub.lng]}
        radius={5}
        pathOptions={{ color: '#F97316', fillColor: '#F97316', fillOpacity: 0.8, weight: 1 }}
      >
        <Tooltip className="map-tooltip" permanent={false}>
          <div className="tooltip-title">⛽ Henry Hub</div>
          <div style={{ color: '#9CA3AF', fontSize: '11px' }}>Gas Pipeline Hub · Louisiana</div>
        </Tooltip>
      </CircleMarker>

      {/* Site markers */}
      {sites.map(site => {
        const isSelected = selectedSite && selectedSite.id === site.id
        const color = getColor(site.composite_score)
        const radius = getRadius(site.composite_score)
        
        return (
          <CircleMarker
            key={site.id}
            center={[site.lat, site.lng]}
            radius={isSelected ? radius + 4 : radius}
            pathOptions={{
              color: isSelected ? '#F9FAFB' : color,
              fillColor: color,
              fillOpacity: isSelected ? 0.9 : 0.6,
              weight: isSelected ? 2 : 1,
            }}
            eventHandlers={{
              click: () => onSelectSite(site),
            }}
          >
            <Tooltip className="map-tooltip">
              <div className="tooltip-title">{site.label}</div>
              <div className="tooltip-row">
                <span>Avg Spread:</span>
                <span className="tooltip-value">+${site.avg_spread}/MWh</span>
              </div>
              <div className="tooltip-row">
                <span>Positive Hours:</span>
                <span className="tooltip-value">{site.positive_hours_pct}%</span>
              </div>
              <div className="tooltip-row">
                <span>Composite Score:</span>
                <span className="tooltip-value">{site.composite_score}/100</span>
              </div>
            </Tooltip>
          </CircleMarker>
        )
      })}

      {selectedSite && (
        <MapUpdater center={[selectedSite.lat, selectedSite.lng]} />
      )}
    </MapContainer>
  )
}
