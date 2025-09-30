export default function PersonKPI({ astronaut }) {
  return (
    <div className="card">
      <h3>{astronaut.name} — KPIs</h3>
      <div className="kpi">
        <div>Stress</div>
        <div>Valence</div>
        <div>Arousal</div>
        <div>Emotion</div>
      </div>
      <p>Trends & sleep cycles coming soon. Integrate wearable or schedule data here.</p>
    </div>
  )
}