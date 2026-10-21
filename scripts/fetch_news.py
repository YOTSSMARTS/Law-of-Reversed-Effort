#!/usr/bin/env python3
"""Fetch public Google News RSS feeds and write a deduplicated news JSON file."""
import json, os, re, time
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from urllib.parse import quote
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET

FEEDS = [
    ("ไทย", "ประเทศไทย OR ข่าวไทย", "TH:th"),
    ("โลก", "world news OR international news", "US:en"),
    ("เศรษฐกิจ", "เศรษฐกิจ OR การเงิน OR ตลาดหุ้น", "TH:th"),
    ("เทคโนโลยี", "เทคโนโลยี OR ปัญญาประดิษฐ์ OR AI", "TH:th"),
    ("ธุรกิจ", "ธุรกิจ OR บริษัท OR business", "TH:th"),
]
def fetch(category, query, edition):
    url = "https://news.google.com/rss/search?q=" + quote(query) + "&hl=" + ("en-US" if edition=="US:en" else "th") + "&gl=" + edition.split(":")[0] + "&ceid=" + edition
    req = Request(url, headers={"User-Agent":"Mozilla/5.0 (compatible; NewsCenterRSS/1.0)"})
    with urlopen(req, timeout=20) as response:
        root = ET.fromstring(response.read())
    articles = []
    for item in root.findall("./channel/item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub = (item.findtext("pubDate") or "").strip()
        source_el = item.find("source")
        source = (source_el.text or "").strip() if source_el is not None else "Google News"
        if not title or not link:
            continue
        # Google News commonly appends the publisher to the title.
        if source == "Google News" and " - " in title:
            title, source = title.rsplit(" - ", 1)
        try:
            published = parsedate_to_datetime(pub).astimezone(timezone.utc).isoformat()
        except Exception:
            published = None
        articles.append({"title": title, "link": link, "published": published, "source": source, "category": category})
    return articles

def main():
    articles, errors = [], []
    for category, query, edition in FEEDS:
        try:
            articles.extend(fetch(category, query, edition))
        except Exception as exc:
            errors.append(category + ": " + str(exc))
    # Deduplicate by canonical link and sort newest first.
    unique = {}
    for article in articles:
        unique[article["link"]] = article
    final = sorted(unique.values(), key=lambda x: x.get("published") or "", reverse=True)[:250]
    payload = {"updatedAt": datetime.now(timezone.utc).isoformat(), "articleCount": len(final), "articles": final, "feedErrors": errors}
    os.makedirs("data", exist_ok=True)
    with open("data/news.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("Saved", len(final), "articles; feed errors:", len(errors))
    if errors:
        print("\n".join(errors))
if __name__ == "__main__":
    main()
