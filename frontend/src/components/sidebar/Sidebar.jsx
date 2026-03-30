import { useState } from "react";

export default function Sidebar({
  isOpen,
  files,
  activeFile,
  onSelectFile,
  onUpload,
  uploadStatus,
}) {
  const [dragging, setDragging] = useState(false);

  // drag & drop handlers
  const handleDragOver  = (e) => { e.preventDefault(); setDragging(true); };
  const handleDragLeave = () => setDragging(false);
  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    onUpload(e.dataTransfer.files[0]);
  };

  // click to open file picker
  const handleClick = () => {
    const input = document.createElement("input");
    input.type = "file";
    input.accept = ".pdf,.txt,.docx";
    input.onchange = (e) => onUpload(e.target.files[0]);
    input.click();
  };

  return (
    <div className={`
      flex flex-col bg-[#111318]
      border-r border-white/[0.07]
      transition-all duration-300 overflow-hidden
      ${isOpen ? "w-[280px] min-w-[280px]" : "w-0 min-w-0 border-r-0"}
    `}>

      {/* Header */}
      <div className="px-5 pt-6 pb-4 border-b border-white/[0.05]">
        <p className="text-[11px] font-bold tracking-[0.12em] uppercase
                      text-white/90 font-mono whitespace-nowrap">
          Knowledge Base
        </p>
        <p className="text-xs text-white/25 mt-1 whitespace-nowrap">
          Upload documents to chat with
        </p>
      </div>

      {/* Drop zone */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={handleClick}
        className={`
          mx-3 mt-4 rounded-xl border-[1.5px] border-dashed p-6
          flex flex-col items-center gap-3 cursor-pointer transition-all duration-200
          ${dragging
            ? "border-teal-400/60 bg-teal-400/5"
            : "border-white/10 hover:border-teal-400/40 hover:bg-teal-400/[0.03]"
          }
        `}
      >
        <div className="w-10 h-10 rounded-full bg-teal-400/15
                        flex items-center justify-center">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none"
            stroke="#2dd4bf" strokeWidth="2" strokeLinecap="round">
            <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/>
            <polyline points="17 8 12 3 7 8"/>
            <line x1="12" y1="3" x2="12" y2="15"/>
          </svg>
        </div>
        <p className="text-[13px] text-white/40 text-center leading-relaxed">
          Drop files here or{" "}
          <span className="text-teal-400 font-medium">browse</span>
        </p>
        <p className="text-[11px] text-white/20 font-mono">PDF, TXT, DOCX</p>
      </div>

      {/* Uploading progress bar */}
      {uploadStatus === "uploading" && (
        <div className="mx-3 mt-3">
          <div className="h-[2px] bg-white/5 rounded-full overflow-hidden">
            <div className="h-full w-2/5 rounded-full
                            bg-gradient-to-r from-teal-400 to-indigo-500
                            animate-[slide_1.2s_ease-in-out_infinite]" />
          </div>
          <p className="text-[11px] text-teal-400 font-mono mt-1.5">
            Indexing document...
          </p>
        </div>
      )}

      {/* File list */}
      <div className="flex-1 overflow-y-auto px-2.5 py-3 flex flex-col gap-1">
        {files.length > 0 && (
          <p className="text-[10px] font-semibold tracking-[0.1em] uppercase
                        text-white/15 px-2 mb-1.5 font-mono">
            Documents
          </p>
        )}

        {files.length === 0 ? (
          <p className="text-xs text-white/15 text-center py-5">
            No documents yet
          </p>
        ) : (
          files.map((name) => (
            <button
              key={name}
              onClick={() => onSelectFile(name)}
              title={name}
              className={`
                flex items-center gap-2.5 w-full px-2.5 py-2.5
                rounded-lg border text-left transition-all duration-150
                ${activeFile === name
                  ? "bg-teal-400/8 border-teal-400/20 text-teal-100"
                  : "bg-transparent border-transparent text-white/35 hover:bg-white/[0.03]"
                }
              `}
            >
              <div className={`w-1.5 h-1.5 rounded-full flex-shrink-0
                ${activeFile === name ? "bg-teal-400" : "bg-white/15"}`}
              />
              <span className="text-[13px] truncate">{name}</span>
            </button>
          ))
        )}
      </div>
    </div>
  );
}