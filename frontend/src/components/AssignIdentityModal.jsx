import { useEffect, useRef, useState } from 'react'
import { enroll } from '../lib/api'

export default function AssignIdentityModal({ open, onClose }) {
  const videoRef = useRef(null)
  const canvasRef = useRef(null)
  const [name, setName] = useState('')
  const [role, setRole] = useState('')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  useEffect(() => {
    let stream
    async function start() {
      if (!open) return
      setError(''); setSuccess('')
      try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false })
        if (videoRef.current) {
          videoRef.current.srcObject = stream
          await videoRef.current.play()
        }
      } catch (e) {
        setError('Camera access denied or unavailable.')
      }
    }
    start()
    return () => {
      if (stream) stream.getTracks().forEach(t => t.stop())
    }
  }, [open])

  function grabFrameB64() {
    const v = videoRef.current
    const c = canvasRef.current
    if (!v || !c) return null
    c.width = 640; c.height = 480
    const ctx = c.getContext('2d')
    ctx.drawImage(v, 0, 0, c.width, c.height)
    const dataUrl = c.toDataURL('image/jpeg', 0.85)
    return dataUrl.split(',')[1]
  }

  async function onEnroll() {
    setBusy(true); setError(''); setSuccess('')
    const image_b64 = grabFrameB64()
    if (!image_b64) { setError('Unable to capture image.'); setBusy(false); return }
    if (!name.trim()) { setError('Please enter a name.'); setBusy(false); return }
    try {
      const res = await enroll(name.trim(), image_b64, role.trim() || undefined)
      if (res.error) throw new Error(res.error)
      setSuccess(`Enrolled ${name} (ID ${res.astronaut_id}). Close this dialog and resume.`)
    } catch (e) {
      setError(e.message || 'Enrollment failed.')
    } finally {
      setBusy(false)
    }
  }

  if (!open) return null
  return (
    <div style={{position:'fixed', inset:0, background:'rgba(0,0,0,0.6)', display:'flex', alignItems:'center', justifyContent:'center', zIndex:50}}>
      <div className="card" style={{width:600}}>
        <h3>Assign Identity</h3>
        <p>Capture a frame and enroll a name to resolve “Unknown”. Ensure the person’s face is clearly visible.</p>
        <div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:12}}>
          <video ref={videoRef} style={{width:'100%', background:'#0b1220', borderRadius:8}} muted playsInline />
          <div>
            <div className="row" style={{marginBottom:8}}>
              <label style={{width:80}}>Name</label>
              <input style={{flex:1, padding:8, borderRadius:8, border:'1px solid #334155'}} value={name} onChange={e=>setName(e.target.value)} placeholder="Full name" />
            </div>
            <div className="row" style={{marginBottom:8}}>
              <label style={{width:80}}>Role</label>
              <input style={{flex:1, padding:8, borderRadius:8, border:'1px solid #334155'}} value={role} onChange={e=>setRole(e.target.value)} placeholder="Optional (e.g., Team leader)" />
            </div>
            <div className="row" style={{gap:8}}>
              <button className="btn" onClick={onEnroll} disabled={busy}>{busy ? 'Enrolling...' : 'Enroll'}</button>
              <button className="btn" style={{background:'#475569'}} onClick={onClose} disabled={busy}>Close</button>
            </div>
            {error && <div style={{color:'#ef4444', marginTop:8}}>{error}</div>}
            {success && <div style={{color:'#16a34a', marginTop:8}}>{success}</div>}
          </div>
        </div>
        <canvas ref={canvasRef} style={{display:'none'}} />
      </div>
    </div>
  )
}