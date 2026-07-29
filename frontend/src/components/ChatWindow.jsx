import { useState, useRef, useEffect } from 'react'
import MessageBubble from './MessageBubble'

const BACKEND = 'http://localhost:8000'

export default function ChatWindow({ open, onClose }) {
  const [stage, setStage] = useState('onboard') // 'onboard' | 'chat'
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  function handleStart() {
    if (!name.trim() || !email.trim()) return
    setStage('chat')
    setMessages([{
      role: 'bot',
      content: `Hi ${name}! 🎬 What are you in the mood to watch? Or name a film and I'll review it for you.`
    }])
  }

  async function handleSend() {
    if (!input.trim() || loading) return
    const userMsg = input.trim()
    setInput('')
    setMessages(prev => [...prev, { role: 'user', content: userMsg }])
    setLoading(true)

    // Add empty bot message to stream into
    setMessages(prev => [...prev, { role: 'bot', content: '' }])

    try {
      const response = await fetch(`${BACKEND}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: userMsg,
          user_name: name,
          session_id: email
        })
      })

      const reader = response.body.getReader()
      const decoder = new TextDecoder()

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        const chunk = decoder.decode(value)
        const lines = chunk.split('\n').filter(l => l.startsWith('data: '))

        for (const line of lines) {
          const data = JSON.parse(line.replace('data: ', ''))

          if (data.type === 'token') {
            setMessages(prev => {
              const updated = [...prev]
              updated[updated.length - 1] = {
                role: 'bot',
                content: updated[updated.length - 1].content + data.content
              }
              return updated
            })
          }
        }
      }
    } catch (err) {
      setMessages(prev => {
        const updated = [...prev]
        updated[updated.length - 1] = {
          role: 'bot',
          content: 'Something went wrong. Please try again.'
        }
        return updated
      })
    } finally {
      setLoading(false)
    }
  }

  const panelStyle = {
    position: 'fixed', bottom: '96px', right: '28px',
    zIndex: 99, width: '340px',
    background: '#13121a',
    border: '1px solid rgba(200,145,58,0.15)',
    borderRadius: '16px',
    boxShadow: '0 20px 60px rgba(0,0,0,0.6)',
    overflow: 'hidden',
    transform: open ? 'scale(1) translateY(0)' : 'scale(0.9) translateY(20px)',
    opacity: open ? 1 : 0,
    pointerEvents: open ? 'all' : 'none',
    transition: 'transform 0.3s cubic-bezier(0.34,1.56,0.64,1), opacity 0.25s',
    transformOrigin: 'bottom right',
    display: 'flex', flexDirection: 'column'
  }

  return (
    <div style={panelStyle}>
      {/* Header */}
      <div style={{
        padding: '14px 16px',
        background: 'rgba(200,145,58,0.08)',
        borderBottom: '1px solid rgba(200,145,58,0.1)',
        display: 'flex', alignItems: 'center',
        justifyContent: 'space-between'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{
            width: '32px', height: '32px', borderRadius: '50%',
            background: 'linear-gradient(135deg, #c8913a, #a06e28)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: '14px', fontWeight: 700, color: '#0a0a0f'
          }}>M</div>
          <div>
            <div style={{ fontSize: '13px', fontWeight: 500, color: '#f0ead6' }}>
              Movie Companion
            </div>
            <div style={{ fontSize: '11px', color: '#8a8070' }}>
              Ask me anything about films
            </div>
          </div>
        </div>
        <button onClick={onClose} style={{
          background: 'none', border: 'none', cursor: 'pointer',
          color: '#8a8070', fontSize: '18px', lineHeight: 1
        }}>×</button>
      </div>

      {/* Onboarding */}
      {stage === 'onboard' && (
        <div style={{ padding: '16px', display: 'flex', flexDirection: 'column', gap: '10px' }}>
          <div style={{
            background: 'rgba(200,145,58,0.08)',
            border: '1px solid rgba(200,145,58,0.12)',
            borderRadius: '4px 12px 12px 12px',
            padding: '10px 13px', fontSize: '13px',
            color: '#c8b89a', lineHeight: 1.5
          }}>
            Hey! Before we dive in — what's your name and email?
          </div>
          <input
            placeholder="Your name"
            value={name}
            onChange={e => setName(e.target.value)}
            style={inputStyle}
          />
          <input
            placeholder="Your email"
            type="email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleStart()}
            style={inputStyle}
          />
          <button onClick={handleStart} style={btnStyle}>
            Let's go 🎬
          </button>
        </div>
      )}

      {/* Chat */}
      {stage === 'chat' && (
        <>
          <div style={{
            padding: '16px', overflowY: 'auto',
            maxHeight: '320px', display: 'flex',
            flexDirection: 'column', gap: '10px'
          }}>
            {messages.map((msg, i) => (
              <MessageBubble key={i} role={msg.role} content={msg.content} />
            ))}
            {loading && messages[messages.length - 1]?.content === '' && (
              <div style={{
                display: 'flex', gap: '4px', padding: '10px 13px',
                background: 'rgba(200,145,58,0.08)',
                borderRadius: '4px 12px 12px 12px', width: 'fit-content'
              }}>
                {[0, 1, 2].map(i => (
                  <div key={i} style={{
                    width: '5px', height: '5px', borderRadius: '50%',
                    background: '#c8913a',
                    animation: `bounce 1.2s ${i * 0.2}s infinite`
                  }} />
                ))}
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input row */}
          <div style={{
            padding: '12px',
            borderTop: '1px solid rgba(200,145,58,0.1)',
            display: 'flex', gap: '8px', alignItems: 'center'
          }}>
            <input
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && handleSend()}
              placeholder="Ask for a rec or a review..."
              style={{ ...inputStyle, flex: 1, marginBottom: 0 }}
            />
            <button onClick={handleSend} disabled={loading} style={{
              width: '34px', height: '34px', borderRadius: '8px',
              background: 'linear-gradient(135deg, #c8913a, #a06e28)',
              border: 'none', cursor: 'pointer',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              opacity: loading ? 0.5 : 1
            }}>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="#0a0a0f">
                <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
              </svg>
            </button>
          </div>
        </>
      )}

      <style>{`
        @keyframes bounce {
          0%, 80%, 100% { transform: translateY(0); opacity: 0.3; }
          40% { transform: translateY(-4px); opacity: 1; }
        }
      `}</style>
    </div>
  )
}

const inputStyle = {
  background: 'rgba(255,255,255,0.04)',
  border: '1px solid rgba(200,145,58,0.15)',
  borderRadius: '8px', padding: '9px 12px',
  fontSize: '12px', color: '#f0ead6',
  fontFamily: 'DM Sans, sans-serif',
  outline: 'none', width: '100%'
}

const btnStyle = {
  background: 'linear-gradient(135deg, #c8913a, #a06e28)',
  border: 'none', borderRadius: '8px', padding: '10px',
  color: '#0a0a0f', fontSize: '13px', fontWeight: 500,
  fontFamily: 'DM Sans, sans-serif', cursor: 'pointer'
}