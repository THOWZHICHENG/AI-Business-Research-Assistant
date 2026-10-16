# Installation and usage

## 1. Get the project

```sh
git clone https://github.com/THOWZHICHENG/AI-Business-Research-Assistant.git
cd AI-Business-Research-Assistant
```

You need Git, Python, enough disk space for the ML dependencies and model cache, and internet access for installation and the first model download. The existing environment uses Python 3.14.7 on Windows. This documentation does not claim a verified Python compatibility range or a successful clean install.

## 2. Create an isolated environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

macOS / Linux:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

These commands use the environment's interpreter directly, so activation is optional and PowerShell execution-policy changes are unnecessary. Requirements pin the five direct dependencies found locally. Transitive dependencies, including PyTorch, are resolved by pip; this is not a complete environment lock.

## 3. Configure hosted inference

Skip this step for semantic search alone. For either generation script, create a local `.env` at the repository root from `.env.example`.

PowerShell:

```powershell
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```

macOS / Linux:

```sh
test -f .env || cp .env.example .env
```

Edit it in your editor:

```dotenv
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

Use your own OpenRouter key. A Hugging Face token is not required by the application configuration for this public embedding model. Never paste your real key into documentation, screenshots, commits, or issue reports.

The scripts hardcode the API URL and `openrouter/free`. Adding an `OPENROUTER_MODEL` variable to `.env` will not change them. If you choose another model, edit the `model=` argument in the relevant script and review current provider terms and costs first.

## 4. Run the three stages

Run from the repository root. Each script asks one question and then exits.

| Script | Purpose | OpenRouter key | Network |
| --- | --- | --- | --- |
| `code/semantic_search.py` | Print closest notes and scores | No | Initial embedding download; cached runs can work offline |
| `code/llm_integration.py` | Generate without retrieval | Yes | Hosted inference |
| `code/rag_pipeline.py` | Retrieve, generate, print sources | Yes | Hosted inference and initial embedding download |

Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe code/semantic_search.py
.\.venv\Scripts\python.exe code/llm_integration.py
.\.venv\Scripts\python.exe code/rag_pipeline.py
```

macOS / Linux:

```sh
.venv/bin/python code/semantic_search.py
.venv/bin/python code/llm_integration.py
.venv/bin/python code/rag_pipeline.py
```

These are three separate demonstrations. Try `What challenges do new website design agencies face?` for each. Retrieval output includes headings and scores. Full RAG adds generated text and labels such as `[Source 1]`; that label refers to the first retrieval result, not necessarily Document 1.

## 5. Add demonstration material

Follow [the dataset format](../data/README.md). Save short UTF-8 notes in `data/business_research.txt` with document headings on their own lines. Restart the script to rebuild the index. There is no upload feature or automatic web collection.

## Troubleshooting

| Symptom | Action |
| --- | --- |
| Python opens the Microsoft Store or is not found | Configure a working Python interpreter; confirm `python --version` before creating the environment. |
| `ModuleNotFoundError` | Install through the same environment interpreter used to run the script. |
| pip cannot find a compatible distribution | Check the package's supported Python/platform wheels. The snapshot may not be available for every environment. |
| Missing `OPENROUTER_API_KEY` | Check spelling and the repository-root `.env`; keep the value private. |
| API authentication, quota, or model error | Check account/key, network, model access, and the provider response. |
| Embedding download fails | Check network/proxy access and cache. Offline execution needs a complete cached model. |
| SciPy DLL blocked by Application Control | An initial import check encountered this locally, although a subsequent offline retrieval run succeeded. If it recurs, ask the device administrator to review the dependency; do not disable security policy. |
| Empty dataset | Restore a correctly formatted note. Full RAG checks for no documents; standalone search has less validation. |
| Unrelated question still retrieves notes | There is no minimum similarity threshold. A match is not proof of relevant evidence. |
| Answer lacks citations or invents details | Compare claims with printed sources; citation instructions are not enforced by a validator. |

For a repeatable presentation, use [the demonstration guide](DEMO_AND_EVALUATION.md).
