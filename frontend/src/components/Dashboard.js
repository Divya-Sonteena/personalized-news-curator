import React, { useEffect, useState } from "react";
import { recommend, feedback, saveUserConfig, refreshCatalog, getLiked } from "../api/api";
import ArticleCard from "./ArticleCard";
import SidebarProfile from "./SidebarProfile";
import { getUserId } from "../api/api";
const TOPICS = ["world","tech","sports","finance","entertainment","science","health","india"];

export default function Dashboard({ userId, onLogout }) {
  const [uid, setUid] = useState(userId || "guest");
  const [k, setK] = useState(6);
  const [quota, setQuota] = useState(2);
  const [topicWeights, setTopicWeights] = useState(Object.fromEntries(TOPICS.map(t => [t, 1.0])));
  const [items, setItems] = useState([]);
  const [metrics, setMetrics] = useState({});
  const [impressionId, setImpressionId] = useState(null);
  const [likedArticles, setLikedArticles] = useState([]);

  useEffect(() => {
    const uidStored = getUserId();
    if (uidStored) setUid(uidStored);
    fetchRecommendations();
    fetchLiked();
    // eslint-disable-next-line
  }, []);

  async function fetchRecommendations() {
    const payload = { user_id: uid, k, topic_weights: topicWeights, source_quota: quota };
    const res = await recommend(payload);
    if (res && res.items) {
      setItems(res.items);
      setMetrics(res.metrics || {});
      setImpressionId(res.impression_id || null);
    } else {
      setItems([]);
    }
  }

  async function fetchLiked() {
    if (!uid || uid === "guest") { setLikedArticles([]); return; }
    const res = await getLiked(uid);
    if (res && res.liked) setLikedArticles(res.liked);
  }

  function onSliderChange(topic, value) {
    setTopicWeights(prev => ({ ...prev, [topic]: parseFloat(value) }));
  }

  async function savePrefs() {
    await saveUserConfig({ user_id: uid, topic_weights: topicWeights, source_quota: quota });
    alert("Preferences saved");
    fetchRecommendations();
  }

  async function onLike(article) {
    setItems(prev => prev.filter(a => a.id !== article.id));
    await feedback({ user_id: uid, article_id: article.id, reward: 1.0 });
    fetchLiked();
  }

  async function onSkip(article) {
    setItems(prev => prev.filter(a => a.id !== article.id));
    await feedback({ user_id: uid, article_id: article.id, reward: 0.0 });
  }

  return (
    <div className="container wide">
      <div className="topbar">
        <h1>Dashboard</h1>
        <div className="row">
          <div className="muted">Signed in: <b>{uid}</b></div>
          <button className="btn outline" onClick={() => { if (onLogout) onLogout(); }}>Logout</button>
        </div>
      </div>

      <div className="layout">
        <div className="main">
          <div className="card">
            <h3>Controls</h3>
            <div className="row" style={{alignItems:'center', gap:'12px'}}>
              <label>Number of items</label>
              <input type="number" min="1" max="12" value={k} onChange={e => setK(Number(e.target.value))} />
              <label>Per-source quota</label>
              <input type="number" min="1" max="6" value={quota} onChange={e => setQuota(Number(e.target.value))} />
              <button className="btn" onClick={fetchRecommendations}>Get Recommendations</button>
              <button className="btn outline" onClick={async () => { await refreshCatalog(); alert("Catalog refreshed"); }}>Refresh Catalog</button>
              <button className="btn" onClick={savePrefs}>Save Preferences</button>
            </div>
            <div className="muted" style={{marginTop:8}}>
              <span className="pill">Diversity — topic: Simpson {metrics.simpson_topic || 0} | entropy {metrics.entropy_topic || 0}</span>
              <span className="pill">Diversity — source: Simpson {metrics.simpson_source || 0} | entropy {metrics.entropy_source || 0}</span>
            </div>

            <h4 style={{marginTop:12}}>Topic sliders</h4>
            <div className="sliders">
              {TOPICS.map(t => (
                <div className="slider-row" key={t}>
                  <div className="label">{t}</div>
                  <input type="range" min="0" max="1" step="0.05" value={topicWeights[t]} onChange={e => onSliderChange(t, e.target.value)} />
                  <div className="val">{topicWeights[t]}</div>
                </div>
              ))}
            </div>
          </div>

          <div className="card">
            <h3>Recommendations</h3>
            {items.length === 0 && <div className="muted">No recommendations yet — try refresh or change sliders.</div>}
            {items.map(item => (
              <ArticleCard key={item.id} article={item} onLike={() => onLike(item)} onSkip={() => onSkip(item)} />
            ))}
          </div>
        </div>

        <aside className="sidebar">
          <SidebarProfile userId={uid} liked={likedArticles} refreshLiked={fetchLiked} />
        </aside>
      </div>
    </div>
  );
}
