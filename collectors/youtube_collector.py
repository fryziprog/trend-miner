import csv
import time
from typing import List, Dict
import requests

YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

def search_youtube_videos(api_key: str, query: str, max_pages: int = 1) -> List[Dict]:
    rows = []
    next_page_token = None
    
    for _ in range(max_pages):
        
        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "maxResults": 50,
            "key": api_key,
            "regionCode": "BR",
            "relevanceLanguage": "pt-br"
        }
        
        if next_page_token:
            params["pageToken"] = next_page_token
        
        response = requests.get(YOUTUBE_SEARCH_URL, params=params, timeout=30)
        
        if not response.ok:
            print("STATUS:", response.status_code)
            print("BODY:", response.text)
            response.raise_for_status()
        
        data = response.json()
        
        for item in data.get("items",[]):
            
            snippet = item.get("snippet",{})
            
            published_at = snippet.get("publishedAt", "")
            channel_tiltle = snippet.get("channelTitle", "unknown_channel")
            title = snippet.get("title", "").strip()
            
            if not published_at or not title:
                continue
            
            rows.append({
                "date": published_at[:10],
                "source": f'youtube/{channel_tiltle}',
                "title": title
            })
        
        next_page_token = data.get("nextPageToken")
        
        if not next_page_token:
            break
    return rows

def collect_multiple_queries(api_key: str, queries: List[str], max_pages: int = 5) -> List[Dict]:
    all_rows = []
    seen = set()

    for query in queries:
        rows = search_youtube_videos(
            api_key=api_key,
            query=query,
            max_pages=max_pages
            )

        for row in rows:
            key = (row["date"], row["source"], row["title"])
            
            if key in seen:
                continue

            seen.add(key)
            all_rows.append(row)
            
        time.sleep(1)
    return all_rows


def save_rows_to_csv(rows: List[Dict], output_path: str) -> None:
    with open(output_path, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["date", "source", "title"])
        writer.writeheader()
        writer.writerows(rows)