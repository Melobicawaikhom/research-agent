"""
web_search_tool.py
------------------

"""

from ddgs import DDGS  # pip install ddgs (this replaced the old duckduckgo-search package)
import time


def web_search(query: str, max_results: int = 5, retries: int = 2):
    last_error = None

    for attempt in range(retries + 1):
        try:
            results = []
            with DDGS() as ddgs:
                for r in ddgs.text(query, max_results=max_results):
                    results.append({
                        "text": r.get("body", "").strip(),
                        "title": r.get("title", "").strip(),
                        "url": r.get("href", ""),
                        "source_type": "web",
                    })
            return results
        except Exception as e:
            last_error = e
            time.sleep(1.5)  # brief backoff before retry

    # If all retries failed, don't crash the whole pipeline —
    # return an empty list and let the orchestrator continue with
    # whatever Papers/Database evidence it still has.
    print(f"[web_search_tool] WARNING: web search failed after retries: {last_error}")
    return []
