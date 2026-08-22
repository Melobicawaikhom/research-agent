"""
fact_checker.py
---------------
"""
import json
import ollama  # same library Person A uses for planning/generation

MODEL_NAME = "llama3.1"  # change to whatever model Person A has pulled locally


def _build_prompt(claim: str, evidence_list: list) -> str:
    evidence_block = "\n".join(
        f"[{i+1}] ({e['source_type']} | id={e['source_id']}) {e['text']}"
        for i, e in enumerate(evidence_list)
    )

    return f"""You are a fact-checking assistant. You are given a CLAIM and a list of
EVIDENCE snippets pulled from different sources (papers, a database, and the web).

Your job: judge how well the claim is supported by the evidence.

CLAIM:
{claim}

EVIDENCE:
{evidence_block if evidence_block else "(no evidence found)"}

Respond with ONLY a JSON object (no extra text, no markdown fences) in this exact shape:
{{
  "verdict": "supported_by_multiple" | "supported_by_one" | "contradicted" | "no_evidence",
  "supporting_evidence_ids": [list of evidence numbers like 1, 2],
  "contradicting_evidence_ids": [list of evidence numbers like 1, 2],
  "explanation": "one or two sentence explanation"
}}
"""


def _call_llm(prompt: str) -> str:
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
    )
    return response["message"]["content"]


def _safe_parse_json(raw: str) -> dict:
    """LLMs sometimes wrap JSON in ```json fences or add stray text — clean it up."""
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        cleaned = cleaned.replace("json\n", "", 1).replace("json", "", 1)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # last resort: try to find the first {...} block
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start != -1 and end != -1:
            try:
                return json.loads(cleaned[start:end + 1])
            except json.JSONDecodeError:
                pass
        return {
            "verdict": "no_evidence",
            "supporting_evidence_ids": [],
            "contradicting_evidence_ids": [],
            "explanation": f"LLM returned unparseable output: {raw[:200]}",
        }


def fact_check(claim: str, evidence_list: list) -> dict:
    """
    Args:
        claim: a single factual statement to verify
        evidence_list: the unified evidence pool (or a filtered subset
                       relevant to this claim) from evidence_merger.py

    Returns:
        dict with keys: verdict, supporting_evidence_ids,
        contradicting_evidence_ids, explanation, and the original claim
    """
    if not evidence_list:
        return {
            "claim": claim,
            "verdict": "no_evidence",
            "supporting_evidence_ids": [],
            "contradicting_evidence_ids": [],
            "explanation": "No evidence was retrieved for this claim.",
        }

    prompt = _build_prompt(claim, evidence_list)
    raw = _call_llm(prompt)
    result = _safe_parse_json(raw)
    result["claim"] = claim
    return result


def fact_check_all(claims: list, evidence_list: list) -> list:
    """Convenience wrapper: fact-check a list of claims against the same evidence pool."""
    return [fact_check(claim, evidence_list) for claim in claims]


# ---- Quick manual test ----
if __name__ == "__main__":
    mock_evidence = [
        {"id": "e1", "text": "RAG reduces hallucination by grounding answers in retrieved documents.",
         "source_type": "paper", "source_id": "paper_001", "score": 0.91, "meta": {}},
        {"id": "e2", "text": "Some studies found RAG has no significant effect on hallucination rates.",
         "source_type": "web", "source_id": "https://example.com/counter", "score": None, "meta": {}},
    ]
    claim = "Retrieval augmented generation reduces hallucination in LLMs."
    result = fact_check(claim, mock_evidence)
    print(json.dumps(result, indent=2))
