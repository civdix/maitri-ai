import { useEffect, useRef, useState } from 'react'
import { openStreamSocket } from '../lib/ws'

export default function CaptureStream() {
  const [active, setActive] = useState(false)
  const wsRef = useRef(null)
  const mediaStreamRef = useRef(null)
  const audioCtxRef = useRef(null)
  const processorRef = useRef(null)
  const videoRef = useRef(null)
  const canvasRef = useRef(null)

  useEffect(() => {
    return () => stop()
  }, [])

  async function start() {
    if (active) return
    const ws = openStreamSocket()
    wsRef.current = ws

    ws.onopen = async () => {
      mediaStreamRef.current = await navigator.mediaDevices.getUserMedia({ video: true, audio: { channelCount:1, sampleRate:16000 } })
      const video = document.createElement('video')
      video.autoplay = true
      video.srcObject = mediaStreamRef.current
      videoRef.current = video
      const canvas = document.createElement('canvas')
      canvasRef.current = canvas

      const audioCtx = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 16000 })
      audioCtxRef.current = audioCtx
      const source = audioCtx.createMediaStreamSource(mediaStreamRef.current)
      const processor = audioCtx.createScriptProcessor(4096, 1, 1)
      processorRef.current = processor
      source.connect(processor)
      processor.connect(audioCtx.destination)
      processor.onaudioprocess = (e) => {
        if (ws.readyState !== 1) return
        const input = e.inputBuffer.getChannelData(0)
        const int16 = new Int16Array(input.length)
        for (let i=0;i<input.length;i++){
          int16[i] = Math.max(-1, Math.min(1, input[i])) * 32767
        }
        const b = new Blob([int16.buffer], {type:'application/octet-stream'})
        const fr = new FileReader()
        fr.onload = () => {
          const base64 = arrayBufferToBase64(fr.result)
          ws.send(JSON.stringify({type:'audio_chunk', audio_b64: base64}))
        }
        fr.readAsArrayBuffer(b)
      }

      setActive(true)
      frameLoop()
    }
    ws.onclose = stop
    ws.onerror = stop
  }

  function stop() {
    setActive(false)
    try { wsRef.current && wsRef.current.close() } catch {}
    try { processorRef.current && processorRef.current.disconnect() } catch {}
    try { audioCtxRef.current && audioCtxRef.current.close() } catch {}
    if (mediaStreamRef.current) {
      mediaStreamRef.current.getTracks().forEach(t => t.stop())
    }
  }

  function frameLoop() {
    if (!active) return
    const video = videoRef.current
    const canvas = canvasRef.current
    if (video && canvas && wsRef.current?.readyState === 1) {
      const w = 320, h = 240
      canvas.width = w; canvas.height = h
      const ctx = canvas.getContext('2d')
      ctx.drawImage(video, 0, 0, w, h)
      canvas.toBlob((blob) => {
        const fr = new FileReader()
        fr.onload = () => {
          const base64 = arrayBufferToBase64(fr.result)
          wsRef.current.send(JSON.stringify({type:'video_frame', image_b64: base64}))
        }
        fr.readAsArrayBuffer(blob)
      }, 'image/jpeg', 0.7)
    }
    requestAnimationFrame(frameLoop)
  }

  function arrayBufferToBase64(buffer) {
    let binary = ''
    const bytes = new Uint8Array(buffer)
    const len = bytes.byteLength
    for (let i = 0; i < len; i++) {
      binary += String.fromCharCode(bytes[i])
    }
    return btoa(binary)
  }

  return (
    <div className="card capture">
      <button className="btn" onClick={active ? stop : start}>{active ? 'Stop Capture' : 'Start Capture'}</button>
      <span>Streams mic + camera to onboard AI</span>
    </div>
  )
}