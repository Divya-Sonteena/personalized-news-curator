import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { register } from "../api/api";

const TOPICS = ["world","tech","sports","finance","entertainment","science","health","india"];

export default function Register({ onRegistered }) {
  const [userId, setUserId] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [topicWeights, setTopicWeights] = useState(Object.fromEntries(TOPICS.map(t => [t,1.0])));
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  function onSliderChange(topic, value) {
    setTopicWeights(prev => ({ ...prev, [topic]: parseFloat(value) }));
  }

  async function submit(e) {
    e.preventDefault();
    if (!userId || !password) return alert("user_id and password required");
    setLoading(true);
    const payload = { user_id: userId, email, password, topic_weights: topicWeights };
    const res = await register(payload);
    setLoading(false);
    if (res.error) return alert("Error: " + res.error);
    alert("Registered!");
    if (onRegistered) onRegistered(res.token, res.user_id);
    navigate("/dashboard");
  }

  return (
    <div className="container">
      <div className="card">
        <h2>Register</h2>
        <form onSubmit={submit}>
          <label>User ID</label>
          <input value={userId} onChange={e => setUserId(e.target.value)} />
          <label>Email (optional)</label>
          <input value={email} onChange={e => setEmail(e.target.value)} />
          <label>Password</label>
          <input type="password" value={password} onChange={e => setPassword(e.target.value)} />
          <h4>Topic preferences (optional)</h4>
          <div className="sliders">
            {TOPICS.map(t => (
              <div key={t} className="slider-row">
                <div className="label">{t}</div>
                <input type="range" min="0" max="1" step="0.05" value={topicWeights[t]} onChange={e => onSliderChange(t, e.target.value)} />
                <div className="val">{topicWeights[t]}</div>
              </div>
            ))}
          </div>
          <div className="row">
            <button className="btn" type="submit" disabled={loading}>{loading ? "Creating..." : "Register"}</button>
            <button className="btn outline" type="button" onClick={() => navigate("/")}>Cancel</button>
          </div>
        </form>
      </div>
    </div>
  );
}
