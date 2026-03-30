import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
});

export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append("file", file);
  const res = await api.post("/ingest", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return res.data; // { message, path? }
};


export const sendMessage = async (query) => {
  const res = await api.post("/chat", { query });
  return res.data; // { question, answer, source }
};