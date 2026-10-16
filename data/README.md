# Demonstration dataset

`business_research.txt` contains five short notes:

| Document | Topic |
| --- | --- |
| 1 | Customer problems |
| 2 | Market opportunities |
| 3 | Startup challenges |
| 4 | Customer expectations |
| 5 | Business differentiation |

The subject is website design services for small businesses. The file does not identify its original authorship, collection method, external sources, publication dates, or geographic evidence. Treat it as illustrative material, not an authoritative market dataset. Do not infer Malaysia-specific facts or verified commercial findings from it.

## Format

Save as UTF-8. Use a unique numbered heading:

```text
[Document 6: Descriptive Topic]

Short research note with enough context to understand it independently.
```

The parser splits at `[Document ` followed by digits and a colon. Keep the syntax consistent. Avoid introductory text before the first heading: nonempty introductory text would become another retrieval unit. Keep notes short because there is no token-aware chunking.

## Adding sourced research

Before presenting real findings, record the source title, publisher, original URL, publication/access date, geography, and permission to redistribute text. These can be plain text inside a note, but the application will not validate or parse them as structured metadata.

Do not add confidential documents, personal data, API keys, copyrighted material without permission, or unsupported statistics. Full RAG sends selected notes to hosted inference. Adding a note does not fine-tune the model; the corpus is re-embedded on the next run.
