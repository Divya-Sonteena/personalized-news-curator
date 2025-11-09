from flask import Blueprint, request, jsonify
from utils.db_utils import get_db
import jwt, config

user_bp = Blueprint("user", __name__)

@user_bp.route("/user/config", methods=["POST"])
def set_config():
    req = request.get_json(force=True) or {}
    user_id = req.get("user_id")
    topic_weights = req.get("topic_weights")
    source_quota = int(req.get("source_quota", config.DEFAULT_SOURCE_QUOTA))
    if not user_id:
        return jsonify({"error":"user_id required"}), 400
    db = get_db()
    db.users.update_one({"user_id": user_id}, {"$set": {"topic_weights": topic_weights, "source_quota": source_quota}}, upsert=True)
    return jsonify({"status":"ok","user_id": user_id, "topic_weights": topic_weights, "source_quota": source_quota})

@user_bp.route("/user/liked", methods=["GET"])
def liked():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error":"user_id required"}), 400
    db = get_db()
    u = db.users.find_one({"user_id": user_id}) or {}
    likes = u.get("likes", [])
    articles = []
    if likes:
        arts = list(db.articles.find({"id": {"$in": likes}}, {"_id":0}))
        articles = [{"id":a["id"], "title": a["title"], "url": a["url"]} for a in arts]
    return jsonify({"liked": articles})
