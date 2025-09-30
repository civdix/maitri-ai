const BASE = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

export function openStreamSocket() {
  const wsUrl = BASE.replace('http', 'ws') + '/ws/stream';
  return new WebSocket(wsUrl);
}