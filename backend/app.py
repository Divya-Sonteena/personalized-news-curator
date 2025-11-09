from flask import Flask
from flask_cors import CORS
import os
import config

# blueprints
from routes.auth_routes import auth_bp
from routes.news_routes import news_bp
from routes.user_routes import user_bp

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = config.SECRET_KEY
    CORS(app)

    # register blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(news_bp, url_prefix="/api")
    app.register_blueprint(user_bp, url_prefix="/api")

    @app.get("/api/health")
    def health():
        from utils.db_utils import get_db
        db = get_db()
        users = db.users.count_documents({}) if "users" in db.list_collection_names() else 0
        articles = db.articles.count_documents({}) if "articles" in db.list_collection_names() else 0
        return {"status":"ok","service":"news-rl-app-backend","users": users, "articles": articles}

    return app

if __name__ == "__main__":
    os.makedirs(config.DATA_DIR, exist_ok=True)
    app = create_app()
    app.run(host="127.0.0.1", port=8505, debug=True)
