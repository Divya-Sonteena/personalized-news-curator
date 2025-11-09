import os

# App / Security
SECRET_KEY = os.getenv("NEWS_RL_SECRET", "change_this_secret_in_prod")
JWT_ALGORITHM = "HS256"
JWT_EXP_SECONDS = int(os.getenv("JWT_EXP_SECONDS", 60 * 60 * 24))  # 24h

# MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "news_rl_db")

# Catalog & embeddings
DATA_DIR = os.getenv("DATA_DIR", "data_news_rl_v2")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
EMBED_DIM = int(os.getenv("EMBED_DIM", 128))  # canonical embedding dim
BANDIT_EMB_USE = int(os.getenv("BANDIT_EMB_USE", 16))  # number of emb dims used in feature vector

# RL hyperparams
LINUCB_ALPHA = float(os.getenv("LINUCB_ALPHA", 0.8))
LINUCB_EPSILON = float(os.getenv("LINUCB_EPSILON", 0.08))

# Other
DEFAULT_SOURCE_QUOTA = int(os.getenv("DEFAULT_SOURCE_QUOTA", 2))
TOPICS = ["world","tech","sports","finance","entertainment","science","health","india"]
SOURCES_RSS = {
    "BBC World": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "TechCrunch": "http://feeds.feedburner.com/TechCrunch/",
    "ESPN": "https://www.espn.com/espn/rss/news",
    "Reuters Business": "http://feeds.reuters.com/reuters/businessNews",
    "Hollywood Reporter": "https://www.hollywoodreporter.com/t/hr/feed/",
    "Science Daily": "https://www.sciencedaily.com/rss/top/science.xml",
    "Healthline": "https://www.healthline.com/rss",
    "NDTV India": "https://feeds.feedburner.com/ndtvnews-india-news",
}
