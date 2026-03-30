import { useState } from "react";
import Sidebar from "./components/sidebar/Sidebar";
import ChatWindow from "./components/chat/ChatWindow";
import { useChat } from "./hooks/useChat";

export default function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const {
    files,
    activeFile,
    setActiveFile,
    messages,
    isLoading,
    uploadStatus,
    handleUpload,
    handleSend,
  } = useChat();

  return (
    <div className="flex h-screen bg-[#0e1015] text-white overflow-hidden">
      <Sidebar
        isOpen={sidebarOpen}
        files={files}
        activeFile={activeFile}
        onSelectFile={setActiveFile}
        onUpload={handleUpload}
        uploadStatus={uploadStatus}
      />
      <ChatWindow
        activeFile={activeFile}
        messages={messages}
        isLoading={isLoading}
        onSend={handleSend}
        onToggleSidebar={() => setSidebarOpen((p) => !p)}
      />
    </div>
  );
}