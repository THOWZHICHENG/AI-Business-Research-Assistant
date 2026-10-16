import os
import re
from pathlib import Path

import faiss
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import SentenceTransformer


# ==========================================
# STEP 1: CONFIGURATION
# ==========================================

project_root = Path(__file__).resolve().parent.parent

load_dotenv(project_root / ".env")

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY is missing from .env")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)


# ==========================================
# STEP 2: LOAD EMBEDDING MODEL
# ==========================================

print("[1/5] Loading Hugging Face embedding model...")

embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


# ==========================================
# STEP 3: LOAD RESEARCH DOCUMENTS
# ==========================================

print("[2/5] Loading business research documents...")

file_path = project_root / "data" / "business_research.txt"

with open(file_path, "r", encoding="utf-8") as file:
    content = file.read()

documents = [
    doc.strip()
    for doc in re.split(r"(?=\[Document \d+:)", content)
    if doc.strip()
]

if not documents:
    raise ValueError("No research documents found!")


# ==========================================
# STEP 4: GENERATE EMBEDDINGS
# ==========================================

print("[3/5] Generating document embeddings...")

document_embeddings = embedding_model.encode(
    documents,
    convert_to_numpy=True,
    normalize_embeddings=True
)

document_embeddings = np.asarray(
    document_embeddings,
    dtype="float32"
)


# ==========================================
# STEP 5: CREATE FAISS INDEX
# ==========================================

print("[4/5] Creating FAISS vector index...")

dimension = document_embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)
index.add(document_embeddings)

print(f"Successfully indexed {index.ntotal} documents!")


# ==========================================
# STEP 6: ASK BUSINESS QUESTION
# ==========================================

question = input("\nEnter your business research question: ").strip()

if not question:
    raise ValueError("Please enter a business question.")


# ==========================================
# STEP 7: RETRIEVE RELEVANT DOCUMENTS
# ==========================================

print("[5/5] Retrieving relevant documents...")

question_embedding = embedding_model.encode(
    [question],
    convert_to_numpy=True,
    normalize_embeddings=True
)

question_embedding = np.asarray(
    question_embedding,
    dtype="float32"
)

top_k = min(3, len(documents))

scores, indices = index.search(
    question_embedding,
    top_k
)

retrieved_documents = []

for doc_index, score in zip(indices[0], scores[0]):
    retrieved_documents.append(
        {
            "content": documents[int(doc_index)],
            "score": float(score)
        }
    )


# ==========================================
# STEP 8: BUILD RAG CONTEXT
# ==========================================

context_parts = []

for i, document in enumerate(retrieved_documents, start=1):
    context_parts.append(
        f"[Source {i}]\n{document['content']}"
    )

context = "\n\n".join(context_parts)


# ==========================================
# STEP 9: SEND CONTEXT TO OPENROUTER LLM
# ==========================================

system_prompt = """
You are an AI Business Research Assistant.

Answer the user's question using only the
provided research documents.

Rules:
1. Base your answer on the retrieved documents.
2. Cite the source number for each key claim,
   for example [Source 1].
3. Do not invent statistics, facts, or references.
4. If the documents do not contain enough
   information, clearly state the limitation.
5. Separate documented findings from suggestions.
6. Provide practical business insights.
"""

user_prompt = f"""
Research Documents:

{context}

User Question:
{question}

Please provide a clear, structured answer with
citations to the supplied research documents.
"""

print("\nGenerating RAG response...\n")

try:
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        max_tokens=700
    )

    answer = response.choices[0].message.content

    print("=" * 50)
    print("AI BUSINESS RESEARCH ASSISTANT")
    print("=" * 50)

    print("\n" + (answer or "No response generated."))

    print("\n" + "=" * 50)
    print("RETRIEVD SOURCES")
    print("=" * 50)

    for i, document in enumerate(retrieved_documents, start=1):
        print(
            f"[Source {i}] "
            f"Similarity: {document['score']:.4f}"
        )
        print(document["content"])
        print("-" * 50)

except Exception as error:
    print(f"API Error: {error}")