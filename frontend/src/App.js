import React, { useState } from "react";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: "user", text: input };
    setMessages(prev => [...prev, userMessage]);

    // Parse input
    const lower = input.trim().toLowerCase();
    let type = null, name = "";
    if (lower.startsWith("project player ")) {
      type = "player";
      name = input.trim().slice(15).trim();
    } else if (lower.startsWith("project pitcher ")) {
      type = "pitcher";
      name = input.trim().slice(16).trim();
    } else {
      setMessages(prev => [...prev, { sender: "bot", text: "Please type: project player <name> or project pitcher <name>" }]);
      setInput("");
      return;
    }

    try {
      // Step 1: Get player ID
      const idRes = await fetch(`http://localhost:5001/api/player-id`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name })
      });
      const idData = await idRes.json();
      if (!idRes.ok || !idData.player_id) {
        setMessages(prev => [...prev, { sender: "bot", text: idData.error || "Player not found." }]);
        setInput("");
        return;
      }
      const player_id = idData.player_id;

      // Step 2: Get stats
      const statsEndpoint = type === "player" ? "player-stats" : "pitcher-stats";
      const statsRes = await fetch(`http://localhost:5001/api/${statsEndpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ player_id })
      });
      const statsData = await statsRes.json();
      if (!statsRes.ok || !statsData.stats) {
        setMessages(prev => [...prev, { sender: "bot", text: statsData.error || "Stats not found." }]);
        setInput("");
        return;
      }

      setMessages(prev => [...prev, { sender: "bot", text: `Stats for ${name}:\n${JSON.stringify(statsData.stats, null, 2)}` }]);

      // Step 3: Get AI projection
      const projEndpoint = type === "player" ? "project-player" : "project-pitcher";
      const projRes = await fetch(`http://localhost:5001/api/${projEndpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ [`${type}_name`]: name, stats: statsData.stats })
      });
      const projData = await projRes.json();
      if (!projRes.ok || !projData.projection) {
        setMessages(prev => [...prev, { sender: "bot", text: projData.error || "Projection failed." }]);
        setInput("");
        return;
      }

      setMessages(prev => [...prev, { sender: "bot", text: `Projected Stats for ${name}:\n${projData.projection}` }]);

    } catch (err) {
      setMessages(prev => [...prev, { sender: "bot", text: "Error contacting backend." }]);
    }
    setInput("");
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") sendMessage();
  };

  return (
    <div className="chat-container">
      <div className="chat-window">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.sender}`}
            style={{ whiteSpace: "pre-wrap" }}>
            {msg.text}
          </div>
        ))}
      </div>

      <div className="input-container">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type: project player ohtani or project pitcher sale"
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}

export default App;