def fmt_explain(score, exploit, explore, topic_weight, similar_info=None):
    out = {
        "score": float(score),
        "exploit": float(exploit),
        "explore": float(explore),
        "topic_weight": float(topic_weight)
    }
    if similar_info:
        out["similar_to_like"] = similar_info
    else:
        out["similar_to_like"] = None
    return out
