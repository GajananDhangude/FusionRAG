import { useState, useRef, useEffect } from "react";

export default function ChatInput({ onSend, disabled }) {
  const [value, setValue] = useState("");
  const textareaRef = useRef(null);

  // auto-grow textarea as user types
  useEffect(() => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = Math.min(el.scrollHeight, 140) + "px";
  }, [value]);

  const handleSubmit = () => {
    if (!value.trim() || disabled) return;
    onSend(value.trim());
    setValue("");
  };

  // Enter = send, Shift+Enter = new line
  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="px-5 pb-5 pt-3 border-t border-white/[0.05]
                    bg-[#0e1015] flex-shrink-0">
      <div className="flex items-end gap-2.5 max-w-[820px] mx-auto
                      bg-[#1a1d27] border border-white/[0.08] rounded-2xl px-3.5 py-3
                      focus-within:border-teal-400/35 transition-colors duration-200">

        {/* Paperclip icon — matches reference screenshot */}
        <button tabIndex={-1}
          className="flex-shrink-0 w-7 h-7 flex items-center justify-center
                     text-white/20 hover:text-teal-400 transition-colors rounded-md">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" strokeWidth="2" strokeLinecap="round">
            <path d="M21.44 11.05l-9.19 9.19a6 6 0 01-8.49-8.49l9.19-9.19a4 4 0 015.66 5.66l-9.2 9.19a2 2 0 01-2.83-2.83l8.49-8.48"/>
          </svg>
        </button>

        <textarea
          ref={textareaRef}
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={disabled}
          placeholder="Ask about your documents..."
          rows={1}
          className="flex-1 bg-transparent border-none outline-none resize-none
                     text-white/80 text-sm leading-relaxed placeholder-white/15
                     disabled:opacity-40 min-h-6 max-h-36"
        />

        <button
          onClick={handleSubmit}
          disabled={!value.trim() || disabled}
          className="flex-shrink-0 w-9 h-9 rounded-xl bg-teal-400
                     hover:bg-teal-300 disabled:opacity-25 disabled:cursor-not-allowed
                     flex items-center justify-center
                     transition-all duration-150 hover:scale-105 disabled:hover:scale-100"
        >
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none">
            <path d="M22 2L11 13" stroke="#0a0a0f" strokeWidth="2.5" strokeLinecap="round"/>
            <path d="M22 2L15 22L11 13L2 9L22 2Z" stroke="#0a0a0f" strokeWidth="2.5"
              strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </button>
      </div>
    </div>
  );
}