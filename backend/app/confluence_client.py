import os
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional

BASE = os.getenv("CONFLUENCE_BASE_URL")
AUTH = (os.getenv("CONFLUENCE_EMAIL"), os.getenv("CONFLUENCE_API_TOKEN"))

def fetch_pages_from_space(space_key: Optional[str] = None, limit: int = 200) -> List[Dict]:
    pages = []
    start = 0
    while True:
        params = {
            "start": start,
            "limit": 50,
            "expand": "body.storage,version"
        }
        if space_key:
            params["spaceKey"] = space_key
        url = f"{BASE}/rest/api/content"
        resp = requests.get(url, params=params, auth=AUTH)
        resp.raise_for_status()
        data = resp.json()
        results = data.get("results", [])
        for r in results:
            pid = r.get("id")
            title = r.get("title")
            webui = f"{BASE}/spaces/{r.get('space', {}).get('key','')}/pages/{pid}"
            body_html = r.get("body", {}).get("storage", {}).get("value", "")
            body_text = html_to_text(body_html)
            pages.append({
                "id": pid,
                "title": title,
                "url": webui,
                "body": body_text,
                "version": r.get("version", {}).get("number")
            })
        if not data.get("_links", {}).get("next"):
            break
        start += params["limit"]
        if len(pages) >= limit:
            break
    return pages

def html_to_text(html: str) -> str:
    soup = BeautifulSoup(html or "", "html.parser")
    for el in soup(["script", "style"]):
        el.decompose()
    lines = [line.strip() for line in soup.get_text(separator="\n").splitlines() if line.strip()]
    return "\n".join(lines)
