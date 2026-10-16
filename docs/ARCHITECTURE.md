# Architecture and technical decisions

## Scope

The repository contains three standalone scripts. They execute at module level, so importing them can load models, prompt for input, or trigger requests. They are learning stages, not a reusable package or deployed service.

## Retrieval path

1. Resolve `data/business_research.txt` relative to the script.
2. Read UTF-8 text and split using `re.split(r"(?=\[Document \d+:)", content)`.
3. Strip empty pieces. Each entire document, including its heading, becomes one retrieval unit.
4. Encode documents with `sentence-transformers/all-MiniLM-L6-v2` and `normalize_embeddings=True`.
5. Convert embeddings to NumPy `float32`.
6. Construct `faiss.IndexFlatIP` using the array's dimension and add the vectors.
7. Encode and normalize the question with the same model.
8. Search with `top_k = min(3, len(documents))` and map indices to document text.

`IndexFlatIP` performs exact inner-product search. For unit-normalized vectors, inner product equals cosine similarity:

```text
cosine(q, d) = (q · d) / (||q|| × ||d||)
If ||q|| = ||d|| = 1, cosine(q, d) = q · d.
```

Scores measure vector similarity. They are not probabilities, confidence percentages, business viability scores, or evidence that a statement is true.

## Generation path

`llm_integration.py` sends the question with a general business-assistant system prompt. It does not load or cite the local corpus.

`rag_pipeline.py` labels retrieval results `[Source 1]` through `[Source k]`, joins them into context, and sends that context plus the question. Its system prompt requests source citations, no invented facts, and acknowledgment of missing information.

Both scripts instantiate the OpenAI client with `base_url="https://openrouter.ai/api/v1"`, obtain `OPENROUTER_API_KEY` through python-dotenv, and request `model="openrouter/free"`. The LLM-only script requests at most 500 output tokens; RAG requests at most 700. These are request limits, not measured response lengths. The routed model can vary; no specific underlying generator is guaranteed.

## Why these choices

| Decision | Benefit | Tradeoff |
| --- | --- | --- |
| Separate retrieval, generation, and RAG demos | Makes stages visible for learning and comparison | Repeated code and no shared configuration |
| Heading-based splitting | Preserves short notes as meaningful units | No token-aware splitting; long text may be truncated |
| Normalized embeddings and exact FAISS search | Simple, inspectable retrieval | No hybrid search or reranking |
| In-memory index | No external vector service required | Documents are encoded each run |
| Prompted citations and printed text | Supports manual answer review | No automated citation or entailment verification |
| Hosted generation | No local generator to deploy | Network, availability, cost, privacy, and routing dependencies |

## Data flow and trust boundaries

The text file and embeddings are processed locally. The embedding model may be downloaded from Hugging Face. The question and up to three retrieved documents are transmitted to OpenRouter for hosted generation. The LLM-only request contains the system prompt and question without the local corpus.

No generated-answer persistence, document database, authentication layer, or session history is implemented. External services may have their own data retention policies. Source labels identify retrieval positions within one answer; they are not stable bibliography identifiers or verified external citations.

## Known failure modes

- The small corpus cannot support broad market claims or current statistics.
- Top-k retrieval returns notes even when all are irrelevant.
- Similarity ranking can miss the best evidence.
- Instructions inside documents can influence generation; source isolation is not enforced.
- The LLM may ignore instructions or misattribute citations.
- Model loading, encoding, and file errors happen outside the API exception handler.
- Broad API exceptions are printed; caught failures do not explicitly set a failing exit status.
- There is no application-configured timeout/retry policy or automated regression suite.

## Development priorities

Establish a sourced corpus and evaluation set. Then extract reusable functions, improve validation and API errors, add token-aware chunks and stable metadata, and measure whether thresholds or reranking improve retrieval. A UI and persistent index can follow after evaluation.
