from ddgs import DDGS

def search_web(query: str, top_k: int = 3) -> list[dict]:
    output = []
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=top_k)
            for r in results:
                output.append({
                    "text": r.get("body", ""),
                    "source": r.get("href", "unknown"),
                    "type": "web",
                    "relevance_score": 0.6  # web results get a lower default trust score
                })
    except Exception as e:
        print(f"web_tool: search failed - {e}")

    return output

# Quick standalone test
if __name__ == "__main__":
    results = search_web("what is a transformer architecture in machine learning")
    for r in results:
        print(r)
        print()