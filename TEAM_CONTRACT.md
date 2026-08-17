\# Team Contract — Agentic Research Assistant



\## Architecture

User Question → AI Planner → \[Search Papers | Database | Web] (parallel)

→ Evidence Retrieval (merge) → Analysis Agent → Fact Checking → Research Report



\## Team Roles

\- Person A: AI Planner + Orchestrator + Report Generation

\- Person B (me): Search Papers tool + Database tool + RBAC

\- Person C: Web Search tool + Evidence Merging + Fact Checking



\## SHARED DATA FORMAT (mandatory — every tool must follow this exactly)



Every retrieval tool (search\_papers, search\_database, search\_web) must

take a query string and return a list of dictionaries in this exact shape:



&#x20;   \[

&#x20;       {

&#x20;           "text": "the actual content/finding",

&#x20;           "source": "filename or url or db table name",

&#x20;           "type": "paper" | "database" | "web",

&#x20;           "relevance\_score": 0.85

&#x20;       },

&#x20;       ...

&#x20;   ]



\## FUNCTION SIGNATURES (each person implements their own file)



Person B, papers\_tool.py:

&#x20;   def search\_papers(query: str, top\_k: int = 3) -> list\[dict]



Person B, database\_tool.py:

&#x20;   def search\_database(query: str, user\_role: str, top\_k: int = 3) -> list\[dict]



Person C, web\_tool.py:

&#x20;   def search\_web(query: str, top\_k: int = 3) -> list\[dict]



Person C, evidence\_merge.py:

&#x20;   def merge\_evidence(papers\_results, db\_results, web\_results) -> list\[dict]



Person C, fact\_check.py:

&#x20;   def verify\_claims(evidence: list\[dict]) -> list\[dict]

&#x20;   # adds a "verified": true/false and "confidence" field to each item



Person A, planner.py:

&#x20;   def plan\_and\_execute(user\_question: str, user\_role: str) -> dict

&#x20;   # decides which tools to call, calls them, returns final report



\## FILE STRUCTURE (shared GitHub repo)

research-agent/

&#x20; papers\_tool.py       <- Person B

&#x20; database\_tool.py     <- Person B

&#x20; web\_tool.py           <- Person C

&#x20; evidence\_merge.py     <- Person C

&#x20; fact\_check.py          <- Person C

&#x20; planner.py             <- Person A

&#x20; main.py                <- Person A (imports everything, final integration)

&#x20; docs/                  <- shared documents/papers for the Papers tool

&#x20; requirements.txt       <- shared package list



\## RULES

1\. Every function must return the exact format above — no exceptions,

&#x20;  or the pipeline breaks when integrated.

2\. Test your own function standalone before pushing to GitHub.

3\. Push your own file(s) only — don't edit teammates' files directly,

&#x20;  raise it with them if something needs to change.

4\. Integration happens once ALL THREE tools (papers/database/web) work

&#x20;  standalone — don't wait until the very end.

