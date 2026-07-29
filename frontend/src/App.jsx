import ChatWidget from './components/ChatWidget'
import './index.css'

export default function App() {
  return (
    <div style={{
      minHeight: '100vh',
      background: '#0a0a0f',
      position: 'relative',
      overflow: 'hidden'
    }}>
      {/* Background gradients */}
      <div style={{
        position: 'absolute', inset: 0,
        background: `
          radial-gradient(ellipse 60% 50% at 20% 30%, rgba(180,120,60,0.12) 0%, transparent 70%),
          radial-gradient(ellipse 40% 60% at 80% 70%, rgba(80,60,160,0.1) 0%, transparent 70%)
        `
      }} />

      {/* Landing content */}
      <div style={{
        position: 'relative', zIndex: 1,
        display: 'flex', flexDirection: 'column',
        alignItems: 'center', justifyContent: 'center',
        minHeight: '100vh', textAlign: 'center',
        padding: '40px'
      }}>
        <p style={{
          fontSize: '11px', letterSpacing: '3px',
          textTransform: 'uppercase', color: '#c8913a',
          marginBottom: '20px', fontWeight: 500
        }}>
          Your AI cinema guide
        </p>

        <h1 style={{
          fontFamily: 'Playfair Display, serif',
          fontSize: 'clamp(36px, 6vw, 64px)',
          fontWeight: 700, lineHeight: 1.1,
          color: '#f0ead6', marginBottom: '20px'
        }}>
          Welcome to<br />
          <span style={{ color: '#c8913a' }}>Movie Companion</span>
        </h1>

        <p style={{
          fontSize: '15px', fontWeight: 300,
          color: '#8a8070', maxWidth: '420px',
          lineHeight: 1.7, marginBottom: '48px'
        }}>
          Discover films tailored to your mood, get honest reviews,
          and build your perfect watchlist — all through conversation.
        </p>

        <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap', justifyContent: 'center' }}>
          {['Personalized picks', 'In-depth reviews', 'Streaming availability', 'Watchlist'].map(tag => (
            <span key={tag} style={{
              padding: '7px 16px', borderRadius: '20px',
              border: '1px solid rgba(200,145,58,0.25)',
              color: '#8a8070', fontSize: '12px',
              background: 'rgba(200,145,58,0.04)'
            }}>
              {tag}
            </span>
          ))}
        </div>
      </div>

      {/* Chat widget */}
      <ChatWidget />
    </div>
  )
}