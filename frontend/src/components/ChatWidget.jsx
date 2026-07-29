import { useState } from 'react'
import ChatWindow from './ChatWindow'

export default function ChatWidget() {
  const [open, setOpen] = useState(false)

  return (
    <>
      {/* Chat window */}
      <ChatWindow open={open} onClose={() => setOpen(false)} />

      {/* Bubble button */}
      <button
        onClick={() => setOpen(!open)}
        style={{
          position: 'fixed', bottom: '28px', right: '28px',
          zIndex: 100, width: '56px', height: '56px',
          borderRadius: '50%', border: 'none', cursor: 'pointer',
          background: 'linear-gradient(135deg, #c8913a, #a06e28)',
          boxShadow: '0 4px 20px rgba(200,145,58,0.4)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          transition: 'transform 0.2s, box-shadow 0.2s',
        }}
        onMouseEnter={e => e.currentTarget.style.transform = 'scale(1.08)'}
        onMouseLeave={e => e.currentTarget.style.transform = 'scale(1)'}
        title="Chat with Movie Companion"
      >
        <svg width="22" height="22" viewBox="0 0 24 24" fill="#0a0a0f">
          <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z" />
        </svg>
      </button>
    </>
  )
}