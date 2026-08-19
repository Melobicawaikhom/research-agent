import os
import chromadb
from sentence_transformers import SentenceTransformer

# Load embedding model once when this module is imported
print("Loading embedding model for papers_tool...")
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Set up ChromaDB
client = chromadb.Client()
collection = client.create_collection(name="papers_collection")

# Load documents from the docs folder into the collection
def load_documents(docs_folder="docs"):
    doc_id = 0
    for filename in os.listdir(docs_folder):
        filepath = os.path.join(docs_folder, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            lines = [line.strip() for line in content.split("\n") if line.strip()]
            for line in lines:
                embedding = embedder.encode(line).tolist()
                collection.add(
                    ids=[str(doc_id)],
                    embeddings=[embedding],
                    documents=[line],
                    metadatas=[{"source": filename}]
                )
                doc_id += 1
    print(f"papers_tool: loaded {doc_id} chunks.")

# Load documents immediately when this module is imported
load_documents()

# THE CONTRACT FUNCTION — this is what Person A's planner will call
def search_papers(query: str, top_k: int = 3) -> list[dict]:
    query_embedding = embedder.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    output = []
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for doc, meta, dist in zip(documents, metadatas, distances):
        relevance_score = round(1 - dist, 2)
        output.append({
            "text": doc,
            "source": meta["source"],
            "type": "paper",
            "relevance_score": relevance_score
        })

    return output

# Quick standalone test
if __name__ == "__main__":
    results = search_papers("when is the DBMS exam")
    for r in results:
        print(r)