from flask import Blueprint, request, jsonify
from utils.db_utils import get_db
import bcrypt, jwt, time
import config

auth_bp = Blueprint("auth", __name__)

def _hash_pw(pw: str) -> bytes:
    return bcrypt.hashpw(pw.encode("utf-8"), bcrypt.gensalt())

def _check_pw(pw: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(pw.encode("utf-8"), hashed)

def _make_token(user_id: str):
    payload = {"sub": user_id, "iat": int(time.time()), "exp": int(time.time()) + config.JWT_EXP_SECONDS}
    return jwt.encode(payload, config.SECRET_KEY, algorithm=config.JWT_ALGORITHM)

@auth_bp.route("/register", methods=["POST"])
def register():
    req = request.get_json(force=True) or {}
    user_id = req.get("user_id")
    email = req.get("email")
    password = req.get("password")
    topic_weights = req.get("topic_weights") or {t:1.0 for t in config.TOPICS}
    if not user_id or not password:
        return jsonify({"error":"user_id and password required"}), 400
    db = get_db()
    if db.users.find_one({"user_id": user_id}):
        return jsonify({"error":"user exists"}), 400
    hashed = _hash_pw(password)
    db.users.insert_one({"user_id": user_id, "email": email, "password_hash": hashed, "topic_weights": topic_weights, "likes": [], "created_at": int(time.time())})
    token = _make_token(user_id)
    return jsonify({"status":"ok", "token": token, "user_id": user_id})

@auth_bp.route("/login", methods=["POST"])
def login():
    req = request.get_json(force=True) or {}
    uid = req.get("user_id")
    email = req.get("email")
    password = req.get("password")
    if not password or (not uid and not email):
        return jsonify({"error":"credentials required"}), 400
    db = get_db()
    q = {"user_id": uid} if uid else {"email": email}
    user = db.users.find_one(q)
    if not user:
        return jsonify({"error":"user not found"}), 404
    if not _check_pw(password, user["password_hash"]):
        return jsonify({"error":"invalid credentials"}), 401
    token = _make_token(user["user_id"])
    return jsonify({"status":"ok","token": token, "user_id": user["user_id"]})
