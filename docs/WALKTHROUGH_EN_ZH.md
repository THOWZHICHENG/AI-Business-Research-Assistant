# Project walkthrough / 项目中英双语说明

## 1. Understand the project / 先理解项目

**English:** This is a command-line AI prototype for answering questions using local business notes. It combines semantic retrieval with a hosted language model. The existing example is about website design businesses, not every industry.

**中文：** 这是一个命令行 AI 原型，用本地商业笔记帮助回答问题。它结合了“语义检索”和“托管大语言模型”。目前的示例围绕网站设计业务，并不覆盖所有行业。

**English:** Its portfolio value is the end-to-end integration: load documents → generate vectors → retrieve relevant text → build a prompt → call an API → display an answer and sources.

**中文：** 它在作品集中的价值是完整流程的整合：读取文档 → 生成向量 → 检索相关内容 → 组装提示词 → 调用 API → 显示回答和来源。

## 2. Learn the vocabulary / 理解核心概念

| Term | English explanation | 中文解释 |
| --- | --- | --- |
| NLP | Processing human language with software | 自然语言处理：让程序处理人类语言 |
| LLM | A language model that generates text from input | 大语言模型：根据输入生成文字的模型 |
| Embedding | A numeric vector representing text for comparison | 文本向量：用一组数字表示文本，便于比较语义 |
| Semantic search | Search based on meaning rather than exact wording alone | 语义检索：按意思寻找内容，而不只匹配相同字词 |
| Normalization | Rescale a vector to unit length here | 归一化：这里指把向量长度缩放为 1 |
| FAISS | A library used here to index and search vectors | 向量检索库：本项目用它存放和搜索向量 |
| Top-k | Return the k closest indexed documents | 返回最相近的 k 篇文档；这里最多三篇 |
| Context | Retrieved text supplied to the generator | 上下文：发送给生成模型的参考资料 |
| Prompt | Instructions and input sent to the model | 提示词：发送给模型的任务要求与输入 |
| RAG | Retrieval-Augmented Generation: retrieve evidence, then generate | 检索增强生成：先找资料，再根据资料生成回答 |
| Hallucination | Generated content unsupported by evidence | 幻觉：模型生成了缺乏证据支持的内容 |
| API key | A credential authorizing a service request | API 密钥：用于验证调用权限，必须保密 |
| Inference | Running a model to obtain output | 推理：运行已有模型取得结果，不等于训练 |

**English:** RAG does not teach the model permanently. It supplies relevant reference text for the current request, much like answering an open-book question. Having a book available does not guarantee the answer uses it correctly.

**中文：** RAG 不会把这些资料永久教给模型，而是在当前请求中提供相关参考内容，可以理解成“开卷答题”。即使有参考资料，模型仍然可能引用错误或回答错误。

## 3. Read the files in this order / 建议阅读顺序

1. **`README.md`** — Project summary, features, and limitations.  
   **中文：** 先了解项目做什么、实现了什么、还缺少什么。
2. **`data/business_research.txt`** — The five short notes the system can retrieve.  
   **中文：** 看清楚 AI 实际能使用哪些资料，不要把示例笔记当成权威市场报告。
3. **`code/semantic_search.py`** — Retrieval without generation.  
   **中文：** 先学习“找资料”，暂时不涉及生成回答。
4. **`code/llm_integration.py`** — Hosted generation without retrieval.  
   **中文：** 再学习如何通过 API 单独调用大模型。
5. **`code/rag_pipeline.py`** — Combine retrieval and generation.  
   **中文：** 最后看如何把“找到的资料”和“生成回答”连接起来。
6. **`docs/ARCHITECTURE.md`** — Decisions and failure modes.  
   **中文：** 理解为什么这样设计，以及系统可能在哪里出错。

## 4. Prepare your environment / 准备运行环境

**English:** If you already have this repository open, use its folder and existing environment. The following commands create an environment only when needed; installation uses the dependency list.

**中文：** 如果已经打开本项目，直接使用当前项目目录和已有环境即可。尚未创建环境时，再执行创建命令；依赖按照清单安装。

Windows PowerShell, from the repository root / 在项目根目录执行：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

**English:** The virtual environment keeps this project's Python dependencies separate from other projects. `requirements.txt` records the five direct packages found in the local environment. The current environment uses Python 3.14.7; a fresh installation on another platform has not been verified.

**中文：** 虚拟环境让本项目的 Python 依赖与其他项目分开。`requirements.txt` 记录了本地已有环境中的五个直接依赖。当前环境使用 Python 3.14.7；其他平台上的全新安装尚未验证。

## 5. Configure the API key / 配置 API 密钥

```powershell
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```

Edit `.env` / 编辑本地 `.env`：

```dotenv
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

**English:** Replace the placeholder with your own key. Keep the existing `.env` if one is already configured. The code uses the OpenAI Python client to connect to OpenRouter; the client library name does not determine the hosting provider. The requested route is `openrouter/free`, whose availability and terms are external dependencies.

**中文：** 用自己的密钥替换占位文字。如果已经有配置好的 `.env`，保留原文件。代码使用 OpenAI Python 客户端连接 OpenRouter；客户端库的名字并不代表模型一定由 OpenAI 托管。代码请求的是 `openrouter/free`，是否可用及相关条款取决于外部服务。

**English:** The semantic-search demo does not need this key. Never commit the real `.env` or show its contents in a screenshot.

**中文：** 单独运行语义检索不需要这个密钥。不要提交真实 `.env`，也不要在截图中展示密钥。

## 6. Run retrieval first / 第一步运行语义检索

```powershell
.\.venv\Scripts\python.exe code/semantic_search.py
```

Question / 输入问题：

```text
How can a website design agency differentiate itself?
```

**English:** The script loads an embedding model, reads the notes, generates normalized document vectors, builds a FAISS index, embeds your question, and prints up to three similar documents. It does not generate a new business answer.

**中文：** 程序加载向量模型、读取笔记、生成归一化文档向量、建立 FAISS 索引，再把问题转换成向量，输出最多三篇相近文档。这个脚本不会生成新的商业回答。

**English:** Compare the retrieved text with your question. A high similarity score means a closer vector match, not a higher probability that a business idea will succeed.

**中文：** 将检索结果与问题进行比较。相似度较高表示向量更接近，不代表商业项目成功率更高，也不是事实正确率。

## 7. Run the LLM-only demo / 第二步单独调用大模型

```powershell
.\.venv\Scripts\python.exe code/llm_integration.py
```

**English:** Ask the same question. This script sends the question and a general system prompt to the hosted model. It does not use the five local notes. This provides a useful qualitative comparison, but one example is not a controlled accuracy experiment.

**中文：** 输入相同问题。这个脚本只把问题与通用系统提示词发送给托管模型，不读取五篇本地笔记。可以观察回答差异，但单个例子不能证明准确率提升。

## 8. Run full RAG / 第三步运行完整 RAG

```powershell
.\.venv\Scripts\python.exe code/rag_pipeline.py
```

**English:** Ask the same question again. Now the program first retrieves notes, assigns source labels, and includes them in the model request. The model is instructed to cite evidence and state limitations. The program then prints the answer and the retrieved sources.

**中文：** 再次输入相同问题。程序先检索笔记、分配来源标签，再把笔记放进模型请求。提示词要求模型引用资料并说明限制，随后程序显示回答与检索来源。

Conceptual flow / 概念流程：

```text
Question / 用户问题
    ↓
Question embedding / 问题向量
    ↓
FAISS similarity search / FAISS 相似度检索
    ↓
Up to three notes / 最多三篇相关笔记
    ↓
Question + notes + instructions / 问题 + 资料 + 提示词
    ↓
Hosted language model / 托管大语言模型
    ↓
Answer + printed sources / 回答 + 来源展示
```

**English:** `[Source 1]` is the first retrieved result for this question. It might contain Document 5. Check the actual printed mapping. The program does not verify that each citation supports the generated claim.

**中文：** `[Source 1]` 指本次检索的第一条结果，它可能对应 Document 5。请查看实际显示的原文对应关系。程序不会自动判断每条引用是否真的支持回答中的说法。

## 9. Understand the code step by step / 理解代码每个阶段

| Code action | Why it exists | 中文解释 |
| --- | --- | --- |
| `Path(__file__).resolve().parent.parent` | Locate the repository from the script | 从脚本位置找到项目根目录 |
| `load_dotenv(...)` | Load local configuration | 读取本地环境配置 |
| `re.split(...)` | Separate notes at numbered headings | 按编号标题拆分笔记，每篇整体作为检索单元 |
| `SentenceTransformer(...)` | Load the pretrained embedding model | 加载预训练向量模型，不是自行训练 |
| `model.encode(...)` | Turn text into comparable vectors | 将文字转换为可比较的数值向量 |
| `normalize_embeddings=True` | Make vectors unit length | 将向量归一化，便于用内积比较方向相似度 |
| `np.asarray(..., dtype="float32")` | Match FAISS vector representation | 转换为 FAISS 使用的浮点数组 |
| `faiss.IndexFlatIP(...)` | Create exact inner-product search | 建立精确内积检索索引 |
| `index.search(...)` | Find the closest available notes | 找出目前笔记中最相近的内容 |
| `context_parts` | Attach source labels and combine text | 给资料加来源标签并拼接 |
| `client.chat.completions.create(...)` | Request hosted text generation | 调用外部服务生成回答 |
| Source-printing loop | Make retrieved evidence visible | 展示参考原文，供人工核对 |

## 10. Check whether it works / 检查结果是否可信

**English:** First ask an answerable question such as `What do customers expect from website services?` Compare the answer with Document 4. Then ask for an exact Malaysian market-size statistic that the notes do not contain. A desirable response admits that the evidence is missing; you must observe whether the model actually does this.

**中文：** 先问资料能够回答的问题，例如“客户对网站服务有哪些期望？”，并与 Document 4 核对。再询问笔记中没有的马来西亚市场规模精确数字。理想回答应说明缺乏证据，但必须实际观察模型是否做到了，不能只因为写了提示词就认为已经保证正确。

**English:** Use [the evaluation guide](DEMO_AND_EVALUATION.md) to record expected documents, actual retrieval, citations, unsupported statements, and failures. No accuracy or speed measurement is included yet.

**中文：** 使用[评估指南](DEMO_AND_EVALUATION.md)记录预期文档、实际检索结果、引用、缺乏依据的说法和运行错误。目前没有已完成的准确率或速度测量。

**English:** An initial dependency-import check encountered a Windows Application Control error involving a SciPy DLL. A subsequent offline run of the actual retrieval script succeeded: the differentiation question returned Document 5 first (similarity 0.8171), followed by Documents 3 and 2. The cause of the earlier error was not established. No hosted API call was made.

**中文：** 首次依赖导入检查遇到了涉及 SciPy DLL 的 Windows 应用程序控制错误。随后实际检索脚本的离线运行成功：“如何差异化”的问题将 Document 5 排在第一位（相似度 0.8171），之后是 Document 3 和 Document 2。此前错误的原因尚未确定。本次没有调用托管模型 API。

## 11. Present it on your résumé / 如何写进简历

**English:** Put it under Personal Projects. State what you built, how the pipeline works, and what remains unverified. Use [the portfolio guide](PORTFOLIO.md) for ready-to-edit bullets and interview answers.

**中文：** 放在“个人项目”栏目，说明实现内容、流程及尚未验证的部分。[作品集说明](PORTFOLIO.md)提供了可修改的简历要点与面试回答。

English example:

> Built a Python RAG prototype using Sentence Transformers and FAISS to retrieve business notes and generate source-labeled answers through hosted LLM inference.

中文示例：

> 使用 Python、Sentence Transformers 和 FAISS 开发 RAG 原型，检索商业笔记，并通过托管大语言模型生成带来源标签的回答。

**English:** Prepare a real demonstration before describing it as validated. Add screenshots only from successful, sanitized runs. Current next steps are improving the environment, documenting real data sources, measuring retrieval, and validating answer support.

**中文：** 在声称“已经验证可用”前，先完成真实演示。只添加来自真实运行且已隐藏敏感信息的截图。接下来应优先解决环境问题、补充有来源的数据、测量检索效果并检查回答依据。
