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
        "text": r.get("chunk") or r.get("text", ""),
        "source_type": "paper",
        "source_id": r.get("doc_id", "unknown"),
        "score": r.get("score"),
        "meta": {"title": r.get("title", "")},
    }


def normalize_db_result(r: dict) -> dict:
    return {
        "id": _make_id(),
        "text": r.get("row_summary") or r.get("text", ""),
        "source_type": "database",
        "source_id": str(r.get("id", "unknown")),
        "score": None,
        "meta": {"table": r.get("table", "")},
    }


def normalize_web_result(r: dict) -> dict:
    return {
        "id": _make_id(),
        "text": r.get("text", ""),
        "source_type": "web",
        "source_id": r.get("url", "unknown"),
        "score": None,
        "meta": {"title": r.get("title", "")},
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