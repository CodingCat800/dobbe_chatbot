import { useState } from "react";

function Chat() {
  const [sessionId] = useState("demo-session-11001");
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { role: "user", text: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");

    const res = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        session_id: sessionId,
        message: input,
      }),
    });

    const data = await res.json();

    const botMsg = { role: "bot", text: data.response };
    setMessages((prev) => [...prev, botMsg]);
  };

  return (
    <div style={styles.container}>
      <h2>🩺 Doctor Appointment Assistant</h2>

      <div style={styles.chatBox}>
        {messages.map((msg, idx) => (
          <div
            key={idx}
            style={{
              ...styles.message,
              alignSelf: msg.role === "user" ? "flex-end" : "flex-start",
              backgroundColor:
                msg.role === "user" ? "#DCF8C6" : "#F1F0F0",
            }}
          >
            {msg.text}
          </div>
        ))}
      </div>

      <div style={styles.inputRow}>
        <input
          style={styles.input}
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <button style={styles.button} onClick={sendMessage}>
          Send
        </button>
      </div>
    </div>
  );
}

const styles = {
  container: {
    maxWidth: "600px",
    margin: "40px auto",
    fontFamily: "Arial, sans-serif",
  },
  chatBox: {
    border: "1px solid #ccc",
    borderRadius: "6px",
    padding: "10px",
    height: "400px",
    overflowY: "auto",
    display: "flex",
    flexDirection: "column",
    marginBottom: "10px",
  },
  message: {
    padding: "8px 12px",
    borderRadius: "6px",
    marginBottom: "8px",
    maxWidth: "80%",
  },
  inputRow: {
    display: "flex",
    gap: "10px",
  },
  input: {
    flex: 1,
    padding: "8px",
    fontSize: "14px",
  },
  button: {
    padding: "8px 16px",
    fontSize: "14px",
    cursor: "pointer",
  },
};

export default Chat;
