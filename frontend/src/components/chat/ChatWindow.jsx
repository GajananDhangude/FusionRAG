import { useRef, useEffect } from "react";
import ChatMessage from "./ChatMessage";
import ChatInput from "./ChatInput";

const SUGGESTIONS = [
  "Summarize the key findings",
  "What are the main topics?",
  "Find specific data points",
  "Compare across documents",
];

export default function ChatWindow({
  activeFile,
  messages,
  isLoading,
  onSend,
  onToggleSidebar,
}) {
  const bottomRef = useRef(null);

  // scroll to bottom when new message arrives
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  return (
    <div className="flex-1 flex flex-col overflow-hidden">

      {/* Topbar */}
      <div className="flex items-center gap-3.5 px-6 py-3.5 flex-shrink-0
                      border-b border-white/[0.06] bg-[#0e1015]">
        <div className="w-10 h-10 rounded-xl flex-shrink-0
                        bg-gradient-to-br from-[#134e4a] to-[#1a5c58]
                        border border-teal-400/20
                        flex items-center justify-center">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none"
            stroke="#2dd4bf" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
          </svg>
        </div>
        <div className="flex-1">
          <p className="text-[15px] font-semibold text-white/90">RAG Assistant</p>
          <p className="text-[12px] text-white/25 mt-0.5">Chat with your documents</p>
        </div>
        {/* hamburger — collapses sidebar */}
        <button
          onClick={onToggleSidebar}
          className="w-8 h-8 rounded-lg bg-white/[0.04] border border-white/[0.07]
                     text-white/25 hover:text-white/50 hover:bg-white/[0.07]
                     flex items-center justify-center transition-all duration-150"
        >
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" strokeWidth="2" strokeLinecap="round">
            <line x1="3" y1="6"  x2="21" y2="6"/>
            <line x1="3" y1="12" x2="21" y2="12"/>
            <line x1="3" y1="18" x2="21" y2="18"/>
          </svg>
        </button>
      </div>

      {/* Empty state — no messages yet */}
      {messages.length === 0 ? (
        <div className="flex-1 flex flex-col items-center justify-center
                        gap-4 px-10 text-center">
          <div className="w-[72px] h-[72px] rounded-2xl
                          bg-gradient-to-br from-[#134e4a] to-[#1a5c58]
                          border border-teal-400/20
                          flex items-center justify-center">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none"
              stroke="#2dd4bf" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
              <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
            </svg>
          </div>
          <h2 className="text-[22px] font-semibold text-white/85 mt-1">
            Ask anything about your docs
          </h2>
          <p className="text-sm text-white/25 leading-relaxed max-w-[420px]">
            Upload files to the knowledge base, then ask questions.
            I'll find answers from your documents.
          </p>

          {/* 2x2 suggestion chips */}
          <div className="grid grid-cols-2 gap-2.5 mt-2 w-full max-w-[520px]">
            {SUGGESTIONS.map((s) => (
              <button
                key={s}
                onClick={() => activeFile && onSend(s)}
                disabled={!activeFile}
                className="px-4 py-3.5 rounded-xl text-left text-[13px]
                           bg-white/[0.03] border border-white/[0.07] text-white/35
                           hover:bg-teal-400/[0.06] hover:border-teal-400/25 hover:text-teal-100
                           disabled:opacity-30 disabled:cursor-not-allowed
                           transition-all duration-150"
              >
                {s}
              </button>
            ))}
          </div>
        </div>

      ) : (
        /* Message list */
        <div className="flex-1 overflow-y-auto px-6 py-7 flex flex-col gap-5">
          {messages.map((msg, i) => (
            <ChatMessage key={i} message={msg} />
          ))}
          <div ref={bottomRef} />
        </div>
      )}

      <ChatInput onSend={onSend} disabled={isLoading || !activeFile} />
    </div>
  );
}