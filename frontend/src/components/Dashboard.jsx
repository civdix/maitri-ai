import { useEffect, useState } from 'react'
import { getCrew } from '../lib/api'
import CrewCard from './CrewCard'
import CaptureStream from './CaptureStream'
import Alerts from './Alerts'

export default function Dashboard({ onSelect }) {
  const [crew, setCrew] = useState([])

  useEffect(() => {
    load()
    const id = setInterval(load, 3000)
    return () => clearInterval(id)
  }, [])

  async function load() {
    const data = await getCrew()
    setCrew(data)
  }

  return (
    <div className="grid">
      <div className="card">
        <h2>Crew Overview</h2>
        <div className="list">
          {crew.map(c => <CrewCard key={c.id} data={c} onClick={() => onSelect(c)} />)}
        </div>
      </div>
      <div>
        <CaptureStream />
        <Alerts />
      </div>
    </div>
  )
}