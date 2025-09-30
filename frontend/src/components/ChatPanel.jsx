import { useRef, useState } from 'react'
import { chat } from '../lib/api'
import Avatar3D from './Avatar3D'

export default function ChatPanel({ astronaut }) {
  const [text, setText] = useState('')
  const [log, setLog] = useState([])
  const [lang, setLang] = useState('en_IN')
  const audioRef = useRef(null)

  async function send() {
    if (!text.trim()) return
    const me = { role:'user', content: text }
    setLog(l => [...l, me])
    setText('')
    const res = await chat(astronaut.id, me.content, lang)
    const ai = { role:'assistant', content: res.text }
    setLog(l => [...l, ai])
    if (res.audio_b64) {
      const b = atob(res.audio_b64)
      const arr = new Uint8Array(b.length)
      for (let i=0;i<b.length;i++) arr[i] = b.charCodeAt(i)
      const blob = new Blob([arr], {type:'audio/wav'})
      const url = URL.createObjectURL(blob)
      const a = new Audio(url)
      audioRef.current = a
      a.play()
    }
  }

  return (
    <div className="card">
      <h3>On-board AI (Talking)</h3>
      <Avatar3D audioElement={audioRef.current} />
      <div style={{maxHeight:200, overflowY:'auto', margin:'10px 0', padding:'8px', background:'#0b1220', borderRadius:'8px'}}>
        {log.map((m,i) => <div key={i}><b>{m.role==='user'?'You':'AI'}:</b> {m.content}</div>)}
      </div>
      <div className="row" style={{marginBottom:8}}>
        <label>Voice:</label>
        <select value={lang} onChange={e=>setLang(e.target.value)}>
          <option value="en_IN">English (India)</option>
          <option value="hi_IN">Hindi</option>
        </select>
      </div>
      <div className="row">
        <input style={{flex:1, padding:8, borderRadius:8, border:'1px solid #334155'}} value={text} onChange={e=>setText(e.target.value)} placeholder="Type to AI for this astronaut..." />
        <button className="btn" onClick={send}>Send</button>
      </div>
      <small>Responses adapt to latest metrics. Lip movement approximated via audio amplitude.</small>
    </div>
  )
}