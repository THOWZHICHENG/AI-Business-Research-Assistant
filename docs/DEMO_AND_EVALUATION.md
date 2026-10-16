# Demonstration and evaluation

## Five-minute demonstration

1. **Explain the problem (30 seconds).** A user wants an answer from business notes without reading every note.
2. **Show the dataset (30 seconds).** Open the five notes and explain that they are illustrative, unverified material.
3. **Show retrieval (one minute).** Run `code/semantic_search.py` and ask: `How can a website design agency differentiate itself?` Inspect where Document 5 appears and compare the other results. Its rank is not assumed in advance.
4. **Show the baseline (one minute).** Run `code/llm_integration.py` with the same question. Explain that it receives no local notes.
5. **Show RAG (one minute).** Run `code/rag_pipeline.py` with the same question. Match each key claim and `[Source N]` label against the printed source.
6. **Show a limitation (one minute).** Ask: `What is the exact 2026 market size in MYR for Malaysian website design agencies?` The notes contain no such number. Check whether the answer acknowledges this instead of inventing one.

Commands are in [SETUP.md](SETUP.md). Hosted output is nondeterministic; this guide does not include invented transcripts or measured comparisons. Run the question again by restarting the script.

## Manual evaluation set

These are intended evidence targets based on reading the corpus, not observed retrieval results or a statistically representative benchmark.

| ID | Question | Expected evidence or limitation |
| --- | --- | --- |
| Q1 | What problems do small businesses face when establishing an online presence? | Document 1: technical expertise, maintenance resources, UX knowledge, communication |
| Q2 | What services could a website design agency offer? | Document 2: online presence, mobile UX, maintenance, SEO, e-commerce |
| Q3 | What challenges do new website design agencies face? | Document 3: skills, portfolio, acquisition, project management, competition |
| Q4 | What do customers expect from website services? | Document 4: responsiveness, compatibility, speed, communication, maintenance, support |
| Q5 | How can an agency differentiate itself? | Document 5: specialization, personalized design, support, UX expertise |
| Q6 | What is the exact 2026 market size in MYR for Malaysian website design agencies? | Unsupported: no market-size statistics, dates, or Malaysia-specific evidence |
| Q7 | Which named competitor has the highest revenue? | Unsupported: no named competitors or revenue figures |

For Q1–Q5, record whether the target document occurs in the top three. For Q6–Q7, measure whether the generated answer clearly acknowledges missing evidence. Closest documents will still be returned because there is no threshold.

## Review rubric

| Check | How to record |
| --- | --- |
| Retrieval hit@3 | For each of Q1–Q5, 1 if the expected document appears in top three, otherwise 0. Mean = hits divided by 5. |
| Source-label validity | Number of cited labels that refer to supplied results divided by all cited labels. Record N/A if there are no citations; also mark missing citations. |
| Claim support | Manually mark each factual claim supported, unsupported, or unclear against the cited text. Valid labels alone do not prove support. |
| Missing-evidence behavior | For Q6–Q7, record whether the answer explicitly states the evidence gap and avoids invented facts. |
| Operational behavior | Record success/failure, Python and package versions, model route if known, and any network/API errors. |

Do not treat similarity scores as accuracy. A small evaluation cannot support broad claims about all business research. If comparing LLM-only with RAG, use the same questions, record generator differences, and do not attribute every difference to retrieval when routing varies.

## Result record template

Copy one record per question. Leave unknown fields unfilled rather than guessing.

```text
Run date/time and timezone:
Commit or local snapshot:
Python / OS:
Dependency versions:
Question ID / exact wording:
Script:
Requested model route:
Actual generator, if known:
Retrieved document IDs and scores:
Expected document in top 3 (yes/no/N/A):
Generated answer:
Citation labels valid (count / total / N/A):
Unsupported or unclear claims:
Acknowledged missing evidence (yes/no/N/A):
Operational result and error, if any:
Reviewer notes:
```

## Verification during documentation preparation

- Inspected all three Python scripts, the five source notes, Git configuration, and existing license.
- Read direct package versions from the existing local Python 3.14.7 environment for `requirements.txt`. This is not a clean installation or a complete lockfile.
- All three scripts passed Python AST syntax checks; all 18 local Markdown links resolved; code fences were balanced; all five dependency pins matched local package metadata; the dataset contained five document headings; `.env` and `.env.local` were ignored while `.env.example` remained publishable. `git diff --check` found no whitespace errors in tracked changes.
- An initial dependency-import check failed because Windows Application Control rejected the SciPy `_rbfinterp_pythran` DLL. A subsequent offline run of the actual semantic-search script completed successfully without changing the application or security settings. The reason for the difference was not established.
- Offline retrieval check: for Q5, the script loaded the cached embedding model, indexed all five documents, and returned Document 5 (0.8171), Document 3 (0.5758), and Document 2 (0.5314). The intended evidence appeared first. This is one observed retrieval result, not a full benchmark.
- No hosted inference call, generated-answer quality score, timing benchmark, clean dependency installation, or production deployment has been verified.

The DLL error is an environment issue observed during verification and may need investigation if it recurs. Do not disable organizational security controls. If needed, ask the device administrator to review the blocked dependency, or reproduce in an environment whose approved packages can load.
