import React, { useState } from "react";
import { chat } from "../api";

export default function Chat() {
  const [messages, setMessages] = useState<{role:string,text:string}[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
 
  const send = async () => {
    if (!input.trim()) return;
    const userMsg = { role: "user", text: input };
    setMessages(prev => [...prev, userMsg]);
    setInput("");
    setLoading(true);
    try {
      const res = await chat(input);
      const { answer, sources } = res.data;
      let botText = answer;
      if (sources && sources.length) {
        botText += "\n\nSources:\n" + sources.map((s:any)=>`- ${s.title} (${s.url})`).join("\n");
      }
      setMessages(prev => [...prev, {role: "assistant", text: botText}]);
    } catch (err:any) {
      setMessages(prev => [...prev, {role:"assistant", text:`Error: ${err?.message || 'unknown'}`}]);
    } finally {
      setLoading(false);
    }
  };

const uploadFile = async (e: React.ChangeEvent<HTMLInputElement>) => {
  const file = e.target.files?.[0];
  if (!file) return;
  const formData = new FormData();
  formData.append("file", file);
  try {
    const res = await axios.post(`${API_BASE}/ingest-file`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    alert(`File ingested: ${res.data.ingested_chunks} chunks`);
  } catch (err:any) {
    alert(`Error: ${err?.message || 'unknown'}`);
  }
};


  return (
    <div style={{maxWidth:800, margin:"0 auto", padding:20}}>
      <h2>Confluence RAG Chat</h2>
      <div style={{border:"1px solid #ddd", minHeight:300, padding:10, marginBottom:10}}>
        {messages.map((m,i)=>(
          <div key={i} style={{marginBottom:12}}>
            <strong>{m.role==="user"?"You":"Assistant"}:</strong>
            <div style={{whiteSpace:"pre-wrap"}}>{m.text}</div>
          </div>
        ))}
      </div>
      <input type="file" onChange={uploadFile} style={{ marginBottom: 10 }} />
      <div>
        <input value={input} onChange={e=>setInput(e.target.value)} style={{width:"70%"}} placeholder="Ask about Confluence docs..." />
        <button onClick={send} disabled={loading} style={{marginLeft:8}}>Send</button>
      </div>
    </div>
  );
}
