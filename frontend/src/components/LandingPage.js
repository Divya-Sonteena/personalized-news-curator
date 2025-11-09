import React from "react";
import { Link } from "react-router-dom";

export default function LandingPage({ user }) {
  return (
    <div className="container">
      <header className="header">
        <h1>Personalized News — RL</h1>
        {user ? <div className="muted">Signed in as <b>{user}</b></div> : <div className="muted">Sign up or login to get personalized news</div>}
      </header>

      <main className="card">
        <p>Welcome — this app personalizes news for you using a contextual bandit (LinUCB) and semantic embeddings.</p>
        <div className="row">
          {!user && <Link className="btn" to="/register">Register</Link>}
          {!user && <Link className="btn outline" to="/login">Login</Link>}
          <a className="btn" href="/dashboard">Open Dashboard (guest)</a>
        </div>
      </main>

      <footer className="card muted small">Built with empathy + LinUCB contextual bandit.</footer>
    </div>
  );
}
