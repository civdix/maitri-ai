export default function CrewCard({ data, onClick }) {
  const stressClass = data.stress > 0.7 ? 'crit' : data.stress > 0.5 ? 'warn' : 'ok'
  return (
    <div className="card row" onClick={onClick} style={{cursor:'pointer', justifyContent:'space-between'}}>
      <div>
        <div style={{fontWeight:'bold'}}>{data.name}</div>
        <div className="kpi">
          <div>Stress: <span className={`badge ${stressClass}`}>{data.stress.toFixed(2)}</span></div>
          <div>Valence: <span className="badge ok">{data.valence.toFixed(2)}</span></div>
          <div>Arousal: <span className="badge ok">{data.arousal.toFixed(2)}</span></div>
          <div>Emotion: <span className="badge ok">{data.dominant_emotion}</span></div>
        </div>
      </div>
      <div>›</div>
    </div>
  )
}