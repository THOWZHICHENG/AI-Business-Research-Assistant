from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


# Step 1: Load embedding model
print("[1/6] Loading Hugging Face embedding model...", flush=True)

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

print("Embedding model loaded successfully!", flush=True)


# Step 2: Load research documents
print("[2/6] Loading business documents...", flush=True)

project_root = Path(__file__).resolve().parent.parent
file_path = project_root / "data" / "business_research.txt"

with open(file_path, "r", encoding="utf-8") as file:
    content = file.read()

# Split documents using their headings
import re

documents = [
    doc.strip()
    for doc in re.split(r"(?=\[Document \d+:)", content)
    if doc.strip()
]

print(f"Successfully loaded {len(documents)} documents!")


# Step 3: Generate document embeddings
print("[3/6] Generating embeddings...", flush=True)

document_embeddings = model.encode(
    documents,
    convert_to_numpy=True,
    normalize_embeddings=True
)

document_embeddings = np.asarray(
    document_embeddings,
    dtype="float32"
)

print("Embeddings generated successfully!")


# Step 4: Create FAISS index
print("[4/6] Creating FAISS vector index...", flush=True)

dimension = document_embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)
index.add(document_embeddings)

print(f"FAISS index created with {index.ntotal} documents!")


# Step 5: Ask question
print("[5/6] Ready for semantic search!", flush=True)

question = input("\nEnter your business question: ")

question_embedding = model.encode(
    [question],
    convert_to_numpy=True,
    normalize_embeddings=True
)

question_embedding = np.asarray(
    question_embedding,
    dtype="float32"
)


# Step 6: Retrieve relevant documents
print("[6/6] Searching relevant documents...", flush=True)

top_k = min(3, len(documents))

scores, indices = index.search(
    question_embedding,
    top_k
)

print("\n===== RELEVANT DOCUMENTS =====\n")

for rank, (doc_index, score) in enumerate(
    zip(indices[0], scores[0]),
    start=1
):
    print(f"Result {rank}")
    print(f"Similarity Score: {score:.4f}")
    print(documents[doc_index])
    print("-" * 50)