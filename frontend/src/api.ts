import axios from "axios";
const API_BASE = process.env.REACT_APP_API_BASE || "http://localhost:8000";

export async function ingest(spaceKey?: string) {
  return axios.post(`${API_BASE}/ingest`, { space_key: spaceKey });
}

export async function chat(query: string) {
  return axios.post(`${API_BASE}/chat`, { query });
}
