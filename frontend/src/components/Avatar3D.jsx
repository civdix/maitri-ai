import { Canvas, useFrame } from '@react-three/fiber'
import { OrbitControls, useGLTF } from '@react-three/drei'
import { useEffect, useMemo, useRef } from 'react'

function Humanoid({ analyser }) {
  const group = useRef()
  const { scene } = useGLTF('/models/avatar.glb')
  const mouthNode = useMemo(() => {
    const n = scene.getObjectByName('Head') || scene
    return n
  }, [scene])

  useFrame(() => {
    let amp = 0.05
    if (analyser?.current) {
      const arr = new Uint8Array(analyser.current.frequencyBinCount)
      analyser.current.getByteTimeDomainData(arr)
      let sum = 0
      for (let i = 0; i < arr.length; i++) {
        const v = (arr[i] - 128) / 128
        sum += v * v
      }
      amp = Math.min(0.5, Math.sqrt(sum / arr.length) * 4)
    }
    if (mouthNode && mouthNode.morphTargetInfluences && mouthNode.morphTargetInfluences.length > 0) {
      mouthNode.morphTargetInfluences[0] = amp
    } else if (mouthNode) {
      mouthNode.rotation.x = 0.02 + amp * 0.25
    }
  })

  return <primitive ref={group} object={scene} dispose={null} />
}

export default function Avatar3D({ audioElement }) {
  const analyser = useRef(null)

  useEffect(() => {
    if (!audioElement) return
    const ctx = new (window.AudioContext || window.webkitAudioContext)()
    const src = ctx.createMediaElementSource(audioElement)
    const an = ctx.createAnalyser()
    an.fftSize = 2048
    src.connect(an)
    an.connect(ctx.destination)
    analyser.current = an
    return () => {
      try { src.disconnect(); an.disconnect(); ctx.close() } catch {}
    }
  }, [audioElement])

  return (
    <div style={{ width: '100%', height: 300, background: '#0f172a', borderRadius: 8 }}>
      <Canvas camera={{ position: [0, 1.2, 2.2], fov: 40 }}>
        <ambientLight intensity={0.5} />
        <directionalLight position={[2, 4, 2]} intensity={1.2} />
        <Humanoid analyser={analyser} />
        <OrbitControls enablePan={false} />
      </Canvas>
    </div>
  )
}

useGLTF.preload('/models/avatar.glb')