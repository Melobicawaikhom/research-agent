"""
evidence_merger.py
------------------

    {
        "id": str,            
        "text": str,          
        "source_type": str,   
        "source_id": str,     
        "score": float|None,  
        "meta": dict          
    }
"""

import uuid


def _make_id():
    return str(uuid.uuid4())[:8]


def normalize_paper_result(r: dict) -> dict:
    return {
        "id": _make_id(),
        "text": r.get("text", ""),
        "source_type": "paper",
        "source_id": r.get("source", "unknown"),
        "score": r.get("relevance_score"),
        "meta": {},
    }
def normalize_db_result(r: dict) -> dict:
    return {
        "id": _make_id(),
        "text": r.get("text", ""),
        "source_type": "database",
        "source_id": r.get("source", "unknown"),
        "score": r.get("relevance_score"),
        "meta": {},
    }
def normalize_web_result(r: dict) -> dict:
    return {
        "id": _make_id(),
        "text": r.get("text", ""),
        "source_type": "web",
        "source_id": r.get("source", "unknown"),
        "score": r.get("relevance_score"),
        "meta": {},
    }


def merge_evidence(paper_results=None, db_results=None, web_results=None):
    pool = []

    for r in (paper_results or []):
        pool.append(normalize_paper_result(r))

    for r in (db_results or []):
        pool.append(normalize_db_result(r))

    for r in (web_results or []):
        pool.append(normalize_web_result(r))

    # Drop empty/junk entries (e.g. a scrape that returned nothing)
    pool = [e for e in pool if e["text"] and e["text"].strip()]

    return pool
