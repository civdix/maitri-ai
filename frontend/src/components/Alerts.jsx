import { useEffect, useState } from 'react'
import AssignIdentityModal from './AssignIdentityModal'

const BASE = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'

export default function Alerts() {
  const [items, setItems] = useState([])
  const [openAssign, setOpenAssign] = useState(false)

  useEffect(() => {
    load()
    const id = setInterval(load, 3000)
    return () => clearInterval(id)
  }, [])

  async function load() {
    const r = await fetch(`${BASE}/alerts`)
    const data = await r.json()
    setItems(data)
  }

  const hasUnknown = items.some(a => a.type === 'identity' && a.level === 'critical')

  return (
    <div className="card">
      <h3>Recent Alerts</h3>
      {items.length === 0 && <div>No alerts yet.</div>}
      <div style={{ display:'grid', gap:8, marginBottom: hasUnknown ? 8 : 0 }}>
        {items.map(a => (
          <div key={a.id} style={{ padding:8, borderRadius:8, background: a.level==='critical' ? '#3a0d0d' : '#0d1b2a', border: '1px solid #4b5563' }}>
            <div style={{fontWeight:700}}>{a.level.toUpperCase()} — {a.type}</div>
            <div>{a.message}</div>
            <small>{new Date(a.created_at).toLocaleString()}</small>
          </div>
        ))}
      </div>
      {hasUnknown && (
        <button className="btn" onClick={() => setOpenAssign(true)}>Assign identity (resolve Unknown)</button>
      )}
      <AssignIdentityModal open={openAssign} onClose={() => setOpenAssign(false)} />
      <small>Unknown detections trigger critical alerts so you can enroll and assign identity quickly.</small>
    </div>
  )
}