import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../api/api";

export default function Login({ onLogin }) {
  const [ident, setIdent] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  async function submit(e) {
    e.preventDefault();
    if (!password || (!ident && !email)) return alert("Provide credentials");
    const payload = ident ? { user_id: ident, password } : { email, password };
    const res = await login(payload);
    if (res.error) return alert("Error: " + res.error);
    if (onLogin) onLogin(res.token, res.user_id);
    navigate("/dashboard");
  }

  return (
    <div className="container">
      <div className="card">
        <h2>Login</h2>
        <form onSubmit={submit}>
          <label>User ID</label>
          <input value={ident} onChange={e => setIdent(e.target.value)} placeholder="user id (or leave empty to use email)" />
          <label>Email</label>
          <input value={email} onChange={e => setEmail(e.target.value)} placeholder="email (or use user id)" />
          <label>Password</label>
          <input type="password" value={password} onChange={e => setPassword(e.target.value)} />
          <div className="row">
            <button className="btn" type="submit">Login</button>
            <button className="btn outline" type="button" onClick={() => navigate("/")}>Back</button>
          </div>
        </form>
      </div>
    </div>
  );
}
