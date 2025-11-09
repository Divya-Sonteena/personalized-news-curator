import React from "react";

export default function ArticleCard({ article, onLike, onSkip }) {
  const ex = article._explain || {};
  const why = `score=${(ex.score||0).toFixed(3)} • exploit=${(ex.exploit||0).toFixed(3)} • explore=${(ex.explore||0).toFixed(3)}`;

  return (
    <div className="item">
      <div style={{display:'flex', justifyContent:'space-between', alignItems:'center'}}>
        <div><span className="topic">{article.topic}</span> <b style={{marginLeft:8}}>{article.title}</b></div>
        <div className="muted small">{article.source}</div>
      </div>
      <div className="muted small">{article.summary}</div>
      <div className="explain">Why this? {why}</div>
      <div className="row" style={{marginTop:8}}>
        <button className="btn" onClick={onLike}>👍 Like</button>
        <button className="btn outline" onClick={onSkip}>Skip</button>
        <a className="btn small" href={article.url} target="_blank" rel="noreferrer">Open</a>
      </div>
    </div>
  );
}
