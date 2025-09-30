import { useState } from 'react'
import Dashboard from './components/Dashboard'
import PersonKPI from './components/PersonKPI'
import ChatPanel from './components/ChatPanel'
import './styles.css'

export default function App() {
  const [selected, setSelected] = useState(null)
  return (
    <div className="app">
      <h1>Maitri AI — BAS Crew Well-being Assistant</h1>
      {!selected ? (
        <Dashboard onSelect={setSelected} />
      ) : (
        <div className="grid">
          <div>
            <button className="btn" onClick={() => setSelected(null)}>← Back</button>
            <PersonKPI astronaut={selected} />
          </div>
          <div>
            <ChatPanel astronaut={selected} />
          </div>
        </div>
      )}
    </div>
  )
}