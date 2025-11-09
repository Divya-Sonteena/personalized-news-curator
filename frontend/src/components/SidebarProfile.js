import React from "react";

export default function SidebarProfile({ userId, liked, refreshLiked }) {
  return (
    <div className="card">
      <h3>Profile</h3>
      <div className="muted">User ID: <b>{userId}</b></div>
      <div style={{marginTop:8}}>
        <h4>Liked Articles</h4>
        {(!liked || liked.length === 0) && <div className="muted small">No liked articles yet.</div>}
        <ul className="liked">
          {(liked || []).map(a => (
            <li key={a.id}><a href={a.url} target="_blank" rel="noreferrer">{a.title}</a></li>
          ))}
        </ul>
        <div style={{marginTop:8}}>
          <button className="btn outline" onClick={refreshLiked}>Refresh Liked</button>
        </div>
      </div>
    </div>
  );
}
