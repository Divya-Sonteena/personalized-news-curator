import feedparser, time, hashlib, random
from typing import List, Dict
import config

def hash_id(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()[:12]

def guess_topic(text: str) -> str:
    t = (text or "").lower()
    if any(k in t for k in ["tech","software","ai","startup","app","gadget","silicon"]): return "tech"
    if any(k in t for k in ["covid","health","vaccine","medicine","doctor","disease"]): return "health"
    if any(k in t for k in ["stock","market","inflation","bank","finance","budget","ipo"]): return "finance"
    if any(k in t for k in ["match","goal","tournament","ipl","cricket","football","nba"]): return "sports"
    if any(k in t for k in ["space","research","science","quantum","lab","study"]): return "science"
    if any(k in t for k in ["film","movie","celebrity","music","show","entertainment"]): return "entertainment"
    if any(k in t for k in ["india","delhi","mumbai","bangalore","bengaluru"]): return "india"
    return "world"

def fetch_rss() -> List[Dict]:
    out = []
    for src, url in config.SOURCES_RSS.items():
        try:
            d = feedparser.parse(url)
            for e in (d.entries or [])[:50]:
                title = (e.get("title") or "").strip()
                summary = e.get("summary") or e.get("description") or ""
                link = e.get("link") or ""
                if not link: continue
                aid = hash_id(src + "|" + link + "|" + title)
                out.append({
                    "id": aid,
                    "title": title or "(no title)",
                    "url": link,
                    "topic": guess_topic(title + " " + summary),
                    "source": src,
                    "freshness_h": 1,
                    "length_w": max(80, min(1200, len((summary or "").split()))),
                    "summary": (summary or "")[:400],
                    "ts": int(time.time())
                })
        except Exception:
            continue
    # dedupe
    seen = set(); dedup=[]
    for a in out:
        if a["id"] in seen: continue
        seen.add(a["id"]); dedup.append(a)
    if not dedup:
        # fallback synthetic seed
        random.seed(1)
        sources = list(config.SOURCES_RSS.keys()) or ["Wire"]
        for i in range(80):
            s = random.choice(sources)
            t = random.choice(config.TOPICS)
            dedup.append({
                "id": f"seed{i}",
                "title": f"{t.title()} news sample {i}",
                "url": f"https://example.com/{t}/{i}",
                "topic": t,
                "source": s,
                "freshness_h": random.randint(1,72),
                "length_w": random.randint(80,800),
                "summary": f"Sample {t} article {i}",
                "ts": int(time.time())
            })
    return dedup
