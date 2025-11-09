# backend/models/recommender.py
from typing import Dict, List, Tuple
import numpy as np
from utils.db_utils import get_db
from models.embeddings import build_embeddings, load_embeddings
from models.feature_extractor import feature_vector, get_sources_vocab
from models.linucb import LinUCBPolicy
from models.diversity_metrics import simpson_index, entropy
import config
import time
from pymongo.errors import BulkWriteError

def ensure_catalog_in_db():
    """
    Ensure there are articles in DB. Use upsert to avoid duplicate-key errors.
    """
    db = get_db()
    # If already present, do nothing
    if db.articles.count_documents({}) > 0:
        return
    from utils.rss_utils import fetch_rss
    items = fetch_rss()
    if not items:
        return
    # Upsert each item by id to avoid duplicates & BulkWrite errors
    for a in items:
        try:
            db.articles.update_one({"id": a["id"]}, {"$set": a}, upsert=True)
        except Exception:
            # don't crash; continue to next item
            continue

def build_or_load_embeddings():
    db = get_db()
    # Fetch articles but exclude MongoDB internal _id to avoid ObjectId in later structures
    articles = list(db.articles.find({}, {"_id": 0}))
    corpus = [(a.get("title","") + " " + a.get("summary","")).strip() for a in articles]
    if not corpus:
        return None, articles, {}
    E, dim = load_embeddings()
    if E is None or E.shape[0] != len(corpus):
        E = build_embeddings(corpus)
    id_to_row = {articles[i]["id"]: i for i in range(len(articles))}
    return E, articles, id_to_row

def recommend_for_user(user_id: str, k: int = 5, topic_weights: Dict[str, float] = None, source_quota: int = config.DEFAULT_SOURCE_QUOTA):
    db = get_db()
    ensure_catalog_in_db()
    E, articles, id_to_row = build_or_load_embeddings()
    # articles already have no "_id" because of projection in build_or_load_embeddings
    sources_vocab = get_sources_vocab(articles)
    if topic_weights is None:
        user = db.users.find_one({"user_id": user_id}, {"_id":0}) or {}
        topic_weights = user.get("topic_weights", {t:1.0 for t in config.TOPICS})
    else:
        user = db.users.find_one({"user_id": user_id}, {"_id":0}) or {}

    d = len(config.TOPICS) + len(sources_vocab) + 3 + config.BANDIT_EMB_USE

    # Load or create policy for user
    if user and "policy" in user:
        policy = LinUCBPolicy.from_dict(user["policy"])
        if policy.d != d:
            policy = LinUCBPolicy(d=d, alpha=policy.alpha, epsilon=policy.epsilon)
    else:
        policy = LinUCBPolicy(d=d)

    # Build feature matrix (n x d) and keep plain Python lists for articles (no ObjectId)
    X_list = []
    for a in articles:
        emb = None
        if E is not None and a["id"] in id_to_row:
            emb = E[id_to_row[a["id"]]]
        X_list.append(feature_vector(a, topic_weights, emb, sources_vocab))
    if len(X_list) == 0:
        return {"items": [], "metrics": {}}
    X = np.stack(X_list, axis=0)

    chosen = []
    seen = set()
    per_source = {}
    for _ in range(min(k, len(articles))):
        cand_idxs = [i for i in range(len(articles)) if i not in seen and per_source.get(articles[i]["source"],0) < source_quota]
        if not cand_idxs:
            break
        X_cand = X[cand_idxs]
        sel_local = policy.select(X_cand)
        sel_idx = cand_idxs[sel_local]
        art = articles[sel_idx].copy()  # copy to avoid modifying DB-returned dicts
        score, exploit, explore = policy.score(X[sel_idx])

        # similarity to likes (robust handling)
        sim_info = None
        likes = user.get("likes", []) if user else []
        if likes and E is not None:
            like_vecs = []
            recent_likes = likes[-50:]
            for lid in recent_likes:
                if lid in id_to_row:
                    like_vecs.append(E[id_to_row[lid]])
            if like_vecs:
                L = np.vstack(like_vecs)
                v = E[id_to_row[art["id"]]]
                sims = (L @ v) / ((np.linalg.norm(L,axis=1) * (np.linalg.norm(v)+1e-9)) + 1e-9)
                best = int(np.argmax(sims))
                sim_info = {"article_id": recent_likes[best], "cosine": float(sims[best])}

        explain = {"score": float(score), "exploit": float(exploit), "explore": float(explore),
                   "topic_weight": float(topic_weights.get(art["topic"],1.0)), "similar_to_like": sim_info}

        # make sure all fields are JSON serializable (no numpy types)
        art["_explain"] = explain
        # convert any numpy scalar fields if present (defensive)
        for kf, vf in list(art.items()):
            if isinstance(vf, (np.floating, np.integer)):
                art[kf] = float(vf)
        chosen.append(art)

        seen.add(sel_idx)
        per_source[art["source"]] = per_source.get(art["source"], 0) + 1

    topics = [a["topic"] for a in chosen]
    sources = [a["source"] for a in chosen]
    metrics = {"simpson_topic": round(simpson_index(topics),4), "entropy_topic": round(entropy(topics),4),
               "simpson_source": round(simpson_index(sources),4), "entropy_source": round(entropy(sources),4)}

    # persist impression event (ensure event doc is serializable)
    imp = {"type":"impression","user_id": user_id, "ts": int(time.time()), "article_ids":[a["id"] for a in chosen], "metrics":metrics}
    try:
        db.events.insert_one(imp)
    except Exception:
        pass

    # persist policy (only policy dict, which is JSON-serializable)
    try:
        db.users.update_one({"user_id": user_id}, {"$set": {"policy": policy.to_dict()}}, upsert=True)
    except Exception:
        pass

    return {"items": chosen, "metrics": metrics}
