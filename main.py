import os
import chromadb
from sentence_transformers import SentenceTransformer

# Load embedding model (converts text into numbers the AI can compare)
print("Loading embedding model...")
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Set up ChromaDB (local vector database)
client = chromadb.Client()
collection = client.create_collection(name="college_docs")

# Step 1: Load all documents from the docs folder
docs_folder = "docs"
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

print(f"Loaded {doc_id} chunks from documents.")

# Step 2: Simple search function
def search(query, top_k=2):
    query_embedding = embedder.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return results["documents"][0]

# Step 3: Test it
if __name__ == "__main__":
    while True:
        question = input("\nAsk a question (or type 'exit'): ")
        if question.lower() == "exit":
            break
        relevant_chunks = search(question)
        print("\n--- Relevant info found ---")
        for chunk in relevant_chunks:
            print("-", chunk)