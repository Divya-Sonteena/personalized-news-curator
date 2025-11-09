from flask import Blueprint, request, jsonify
from models.recommender import recommend_for_user, ensure_catalog_in_db
from utils.db_utils import get_db
from utils.rss_utils import fetch_rss
import config, time

news_bp = Blueprint("news", __name__)

@news_bp.route("/catalog/refresh", methods=["POST"])
def refresh_catalog():
    items = fetch_rss()
    if not items:
        return jsonify({"status":"ok","note":"no_items"}), 200
    db = get_db()
    # upsert articles by id
    for a in items:
        db.articles.update_one({"id": a["id"]}, {"$set": a}, upsert=True)
    return jsonify({"status":"ok","articles": len(items)})

@news_bp.route("/articles", methods=["GET"])
def list_articles():
    db = get_db()
    arts = list(db.articles.find({}, {"_id":0}).limit(200))
    return jsonify({"articles": arts})

@news_bp.route("/recommend", methods=["POST"])
def recommend():
    req = request.get_json(force=True) or {}
    user_id = req.get("user_id") or "guest"
    k = int(req.get("k", 5))
    topic_weights = req.get("topic_weights")
    source_quota = int(req.get("source_quota", config.DEFAULT_SOURCE_QUOTA))
    payload = recommend_for_user(user_id, k=k, topic_weights=topic_weights, source_quota=source_quota)
    return jsonify({"status":"ok", "user_id": user_id, **payload})

@news_bp.route("/feedback", methods=["POST"])
def feedback():
    req = request.get_json(force=True) or {}
    user_id = req.get("user_id") or "guest"
    article_id = req.get("article_id")
    reward = float(req.get("reward", 0.0))
    db = get_db()
    art = db.articles.find_one({"id": article_id})
    if not art:
        return jsonify({"error":"unknown article"}), 400

    # load embeddings and articles
    from models.embeddings import load_embeddings
    E, dim = load_embeddings()
    articles = list(db.articles.find({}))
    id_to_row = {articles[i]["id"]: i for i in range(len(articles))}
    emb = None
    if E is not None and article_id in id_to_row:
        emb = E[id_to_row[article_id]]

    # load user policy
    user = db.users.find_one({"user_id": user_id}) or {}
    from models.linucb import LinUCBPolicy
    if "policy" in user:
        policy = LinUCBPolicy.from_dict(user["policy"])
    else:
        sources = sorted(list({a["source"] for a in articles}))
        d = len(config.TOPICS) + len(sources) + 3 + config.BANDIT_EMB_USE
        policy = LinUCBPolicy(d=d)

    # featureize and update
    from models.feature_extractor import feature_vector, get_sources_vocab
    sources_vocab = get_sources_vocab(articles)
    topic_weights = user.get("topic_weights", {t:1.0 for t in config.TOPICS})
    x = feature_vector(art, topic_weights, emb, sources_vocab)
    policy.update(x, reward)

    # persist policy and likes
    if reward >= 0.5:
        likes = user.get("likes", [])
        likes = (likes + [article_id])[-200:]
    else:
        likes = user.get("likes", [])
    db.users.update_one({"user_id": user_id}, {"$set": {"policy": policy.to_dict(), "likes": likes, "topic_weights": topic_weights}}, upsert=True)
    db.events.insert_one({"type":"feedback","user_id": user_id, "article_id": article_id, "reward": reward, "ts": int(time.time())})
    return jsonify({"status":"ok"})
