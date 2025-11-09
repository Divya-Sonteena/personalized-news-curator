from pymongo import MongoClient
import config

_client = None
_db = None

def get_client():
    global _client
    if _client is None:
        _client = MongoClient(config.MONGO_URI)
    return _client

def get_db():
    global _db
    if _db is None:
        _db = get_client()[config.MONGO_DB]
        # Ensure common indexes
        try:
            _db.users.create_index("user_id", unique=True)
            _db.users.create_index("email", unique=True, sparse=True)
            _db.articles.create_index("id", unique=True)
            _db.events.create_index("ts")
        except Exception:
            pass
    return _db
