import { useState } from "react";
import { uploadFile, sendMessage } from "../services/api";

export function useChat() {
  const [files, setFiles] = useState([]);
  const [activeFile, setActiveFile] = useState(null);
  const [chats, setChats] = useState({});       // { filename: [messages] }
  const [isLoading, setIsLoading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState("idle"); // idle | uploading | done | error

  // messages for currently selected file
  const messages = activeFile ? (chats[activeFile] || []) : [];

  const addMessage = (filename, msg) => {
    setChats((prev) => ({
      ...prev,
      [filename]: [...(prev[filename] || []), msg],
    }));
  };

  const replaceLastMessage = (filename, msg) => {
    setChats((prev) => {
      const msgs = [...(prev[filename] || [])];
      msgs[msgs.length - 1] = msg;
      return { ...prev, [filename]: msgs };
    });
  };

  // ── Upload ────────────────────────────────────────────────────────────
  const handleUpload = async (file) => {
    if (!file) return;

    const allowed = [".pdf", ".txt", ".docx"];
    const ext = "." + file.name.split(".").pop().toLowerCase();
    if (!allowed.includes(ext)) {
      alert("Only PDF, TXT, DOCX supported.");
      return;
    }

    setUploadStatus("uploading");

    try {
      await uploadFile(file);

      // add to sidebar list if not already there
      setFiles((prev) =>
        prev.includes(file.name) ? prev : [...prev, file.name]
      );

      // init chat for this file
      setChats((prev) => ({
        ...prev,
        [file.name]: prev[file.name] || [
          { role: "ai", text: `"${file.name}" indexed. Ask me anything!` },
        ],
      }));

      setActiveFile(file.name);
      setUploadStatus("done");
    } catch (err) {
      setUploadStatus("error");
      alert(err.response?.data?.detail || "Upload failed.");
    }
  };

  // ── Send message ──────────────────────────────────────────────────────
  const handleSend = async (query) => {
    if (!query.trim() || isLoading || !activeFile) return;

    addMessage(activeFile, { role: "user", text: query });
    addMessage(activeFile, { role: "ai", text: null, loading: true });
    setIsLoading(true);

    try {
      const data = await sendMessage(query);
      replaceLastMessage(activeFile, {
        role: "ai",
        text: data.answer,
        source: data.source,
        loading: false,
      });
    } catch {
      replaceLastMessage(activeFile, {
        role: "ai",
        text: "Something went wrong. Please try again.",
        loading: false,
      });
    } finally {
      setIsLoading(false);
    }
  };

  return {
    files,
    activeFile,
    setActiveFile,
    messages,
    isLoading,
    uploadStatus,
    handleUpload,
    handleSend,
  };
}