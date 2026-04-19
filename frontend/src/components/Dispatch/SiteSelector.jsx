import { useState, useEffect, useRef } from 'react'

export default function SiteSelector({ selectedSiteId, onSiteChange, disabled, apiBase }) {
  const [open, setOpen] = useState(false)
  const [sites, setSites] = useState([])
  const ref = useRef(null)

  useEffect(() => {
    fetch(`${apiBase}/api/sites`)
      .then(r => r.json())
      .then(data => {
        if (data.sites) {
          // Sort dynamically to match rest of UI (highest score first)
          const sorted = data.sites.sort((a,b) => b.composite_score - a.composite_score)
          setSites(sorted)
        }
      })
      .catch(err => console.error('SiteSelector fetch error:', err))
  }, [apiBase])

  const selected = sites.find(s => s.id === selectedSiteId) || { id: selectedSiteId, label: 'Loading...', zone: '', composite_score: 0 }

  // Close dropdown on outside click
  useEffect(() => {
    const handler = (e) => {
      if (ref.current && !ref.current.contains(e.target)) setOpen(false)
    }
    document.addEventListener('mousedown', handler)
    return () => document.removeEventListener('mousedown', handler)
  }, [])

  return (
    <div ref={ref} style={{ position: 'relative' }}>
      <button
        onClick={() => !disabled && setOpen(!open)}
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          padding: '4px 12px',
          background: 'var(--bg-elevated)',
          border: '1px solid var(--border-medium)',
          borderRadius: 'var(--radius-sm)',
          color: disabled ? 'var(--text-muted)' : 'var(--text-primary)',
          fontFamily: 'var(--font-mono)',
          fontSize: '11px',
          fontWeight: 600,
          cursor: disabled ? 'not-allowed' : 'pointer',
          transition: 'all 0.2s',
          whiteSpace: 'nowrap',
        }}
      >
        <span style={{ color: 'var(--text-muted)', fontSize: '10px' }}>SITE:</span>
        {selected.label}
        <span style={{ fontSize: '8px', color: 'var(--text-muted)' }}>▼</span>
      </button>

      {open && (
        <div style={{
          position: 'absolute',
          top: '100%',
          left: 0,
          marginTop: '4px',
          background: 'var(--bg-surface)',
          border: '1px solid var(--border-medium)',
          borderRadius: 'var(--radius-md)',
          boxShadow: '0 8px 32px rgba(0,0,0,0.6)',
          zIndex: 100,
          minWidth: '240px',
          animation: 'slide-up 0.15s ease-out',
          overflow: 'hidden',
        }}>
          <div style={{
            padding: '8px 12px',
            fontFamily: 'var(--font-mono)',
            fontSize: '9px',
            color: 'var(--text-muted)',
            letterSpacing: '1.5px',
            textTransform: 'uppercase',
            borderBottom: '1px solid var(--border-subtle)',
          }}>
            Select Dispatch Location
          </div>
          {sites.map(site => (
            <button
              key={site.id}
              onClick={() => { onSiteChange(site.id); setOpen(false) }}
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                width: '100%',
                padding: '10px 12px',
                background: site.id === selectedSiteId ? 'var(--bg-elevated)' : 'transparent',
                border: 'none',
                borderBottom: '1px solid var(--border-subtle)',
                borderLeft: site.id === selectedSiteId ? '3px solid var(--orange)' : '3px solid transparent',
                color: 'var(--text-primary)',
                fontFamily: 'var(--font-mono)',
                fontSize: '12px',
                cursor: 'pointer',
                transition: 'background 0.15s',
                textAlign: 'left',
              }}
              onMouseEnter={e => e.target.style.background = 'var(--bg-surface-hover)'}
              onMouseLeave={e => e.target.style.background = site.id === selectedSiteId ? 'var(--bg-elevated)' : 'transparent'}
            >
              <div>
                <div style={{ fontWeight: 600 }}>{site.label}</div>
                <div style={{ fontSize: '10px', color: 'var(--text-muted)', marginTop: '2px' }}>{site.zone}</div>
              </div>
              <div style={{
                fontFamily: 'var(--font-mono)',
                fontSize: '11px',
                fontWeight: 700,
                color: site.composite_score >= 80 ? '#10B981' : site.composite_score >= 60 ? '#F97316' : '#EF4444',
              }}>
                {site.composite_score}
              </div>
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
