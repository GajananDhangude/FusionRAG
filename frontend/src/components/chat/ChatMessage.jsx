// Animated dots shown while AI is thinking
const TypingDots = () => (
  <div className="flex gap-1.5 items-center py-1">
    {[0, 1, 2].map((i) => (
      <div
        key={i}
        className="w-1.5 h-1.5 rounded-full bg-teal-400 animate-bounce"
        style={{ animationDelay: `${i * 0.15}s` }}
      />
    ))}
  </div>
);

export default function ChatMessage({ message }) {
  const isUser = message.role === "user";

  return (
    <div className={`
      flex animate-[fadeUp_0.25s_ease]
      ${isUser ? "justify-end" : "justify-start"}
    `}>

      {/* AI avatar */}
      {!isUser && (
        <div className="w-7 h-7 rounded-lg flex-shrink-0 mt-0.5 mr-2.5
                        bg-gradient-to-br from-[#134e4a] to-[#1a5c58]
                        border border-teal-400/20
                        flex items-center justify-center
                        text-teal-400 text-[10px] font-bold font-mono">
          AI
        </div>
      )}

      <div className="flex flex-col gap-1.5">
        {/* Message bubble */}
        <div className={`
          max-w-[70%] px-4 py-3 rounded-2xl text-sm leading-relaxed
          ${isUser
            ? "bg-gradient-to-br from-[#134e4a] to-[#1a5c58] border border-teal-400/20 text-teal-50 rounded-tr-sm"
            : "bg-white/[0.04] border border-white/[0.07] text-white/75 rounded-tl-sm"
          }
        `}>
          {message.loading ? <TypingDots /> : message.text}
        </div>

        {/* Source tag under AI messages */}
        {!isUser && message.source && (
          <div className="flex items-center gap-1.5 px-1
                          text-[11px] text-white/20 font-mono">
            <div className="w-1 h-1 rounded-full bg-teal-400" />
            {message.source}
          </div>
        )}
      </div>

      {/* User avatar */}
      {isUser && (
        <div className="w-7 h-7 rounded-lg flex-shrink-0 mt-0.5 ml-2.5
                        bg-white/[0.06] border border-white/[0.08]
                        flex items-center justify-center
                        text-white/30 text-[10px] font-bold">
          U
        </div>
      )}
    </div>
  );
}