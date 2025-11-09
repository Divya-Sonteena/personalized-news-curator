import numpy as np
from typing import List, Dict
import config

def one_hot(value: str, vocab: List[str]) -> List[float]:
    return [1.0 if value == v else 0.0 for v in vocab]

def get_sources_vocab(articles: List[Dict]) -> List[str]:
    return sorted(list({a.get("source","unknown") for a in articles}))

def feature_vector(article: Dict, topic_weights: Dict[str, float], emb_vec, sources_vocab: List[str]):
    topic_vec = one_hot(article.get("topic","world"), config.TOPICS)
    source_vec = one_hot(article.get("source","unknown"), sources_vocab)
    freshness = float(article.get("freshness_h", 1.0))
    freshness_feat = np.exp(-freshness / 24.0)
    length_norm = min(1.0, max(0.0, (article.get("length_w", 200) - 80) / 1200))
    tw = float(topic_weights.get(article.get("topic","world"), 1.0))
    emb_feats = emb_vec[:config.BANDIT_EMB_USE] if (emb_vec is not None and len(emb_vec) >= config.BANDIT_EMB_USE) else [0.0]*config.BANDIT_EMB_USE
    vec = np.concatenate([np.array(topic_vec),
                          np.array(source_vec),
                          np.array([freshness_feat, length_norm, tw]),
                          np.array(emb_feats)])
    return vec.astype(np.float64)
