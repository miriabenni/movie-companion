export default function MessageBubble({ role, content }) {
  const isBot = role === 'bot'
  return (
    <div style={{
      maxWidth: '85%',
      alignSelf: isBot ? 'flex-start' : 'flex-end',
      background: isBot
        ? 'rgba(200,145,58,0.08)'
        : 'rgba(200,145,58,0.18)',
      border: isBot ? '1px solid rgba(200,145,58,0.12)' : 'none',
      borderRadius: isBot ? '4px 12px 12px 12px' : '12px 4px 12px 12px',
      padding: '10px 13px',
      fontSize: '13px', lineHeight: 1.6,
      color: isBot ? '#c8b89a' : '#f0ead6',
      whiteSpace: 'pre-wrap'
    }}>
      {content}
    </div>
  )
}