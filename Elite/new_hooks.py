
import asyncio
import aiohttp
from datetime import datetime, timezone, timedelta
from .config import NEWSAPI_KEY

KEY_TERMS = ["injury","out","doubtful","suspended","lineup","starting","illness"]

def _window_iso(minutes=120):
    dt = datetime.now(timezone.utc) - timedelta(minutes=minutes)
    return dt.isoformat(timespec="seconds").replace("+00:00","Z")

async def fetch_newsapi(home, away, minutes=120):
    if not NEWSAPI_KEY:
        return []
    q = f"({home} OR {away}) AND ({' OR '.join(KEY_TERMS)})"
    url = "https://newsapi.org/v2/everything"
    params = {"q":q,"from":_window_iso(minutes),"language":"en","pageSize":10,"sortBy":"publishedAt","apiKey":NEWSAPI_KEY}
    out=[]
    async with aiohttp.ClientSession() as s:
        try:
            async with s.get(url,params=params,timeout=15) as r:
                js = await r.json()
                for a in js.get("articles",[]):
                    text = f"{a.get('title','')} — {a.get('description','')}".strip()
                    if text: out.append(text[:220])
        except:
            return []
    return out[:5]
