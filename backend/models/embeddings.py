import os
import numpy as np
from typing import List, Tuple
import config

EMB_PATH = os.path.join(config.DATA_DIR, "embeddings.npy")
TEXTS_PATH = os.path.join(config.DATA_DIR, "texts.json")

# attempt to import sentence-transformers
try:
    from sentence_transformers import SentenceTransformer
    S_MODEL = SentenceTransformer(config.EMBEDDING_MODEL)
except Exception:
    S_MODEL = None

# TF-IDF fallback
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    TFV = TfidfVectorizer(stop_words="english", max_features=config.EMBED_DIM)
except Exception:
    TFV = None

def build_embeddings(corpus: List[str]):
    os.makedirs(config.DATA_DIR, exist_ok=True)
    if S_MODEL is not None:
        try:
            E = S_MODEL.encode(corpus, normalize_embeddings=True)
            np.save(EMB_PATH, E.astype("float32"))
            return E
        except Exception:
            pass
    # TF-IDF fallback
    if TFV is not None:
        matrix = TFV.fit_transform(corpus).astype("float32").toarray()
        norms = np.linalg.norm(matrix, axis=1, keepdims=True) + 1e-9
        E = matrix / norms
        np.save(EMB_PATH, E.astype("float32"))
        return E
    # random last-resort (deterministic)
    rng = np.random.default_rng(0)
    E = rng.normal(size=(len(corpus), config.EMBED_DIM)).astype("float32")
    norms = np.linalg.norm(E, axis=1, keepdims=True) + 1e-9
    E = E / norms
    np.save(EMB_PATH, E)
    return E

def load_embeddings():
    if os.path.exists(EMB_PATH):
        E = np.load(EMB_PATH)
        return E, E.shape[1]
    return None, 0
