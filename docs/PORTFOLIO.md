# Portfolio and résumé material

## Project title and description

**AI Business Research Assistant | Python, RAG, Sentence Transformers, FAISS, OpenRouter**

Built a command-line prototype that retrieves business notes using semantic similarity and supplies the selected context to a hosted language model for source-labeled answers.

Use this under **Projects / Personal Projects**, not employment experience, unless it was actually completed as part of a job. Add your real development dates and repository link. Do not invent a client, deployment, user count, measured improvement, or employer.

## Résumé bullets

Choose two or three bullets that you can explain and demonstrate:

- Implemented a Python RAG prototype combining Sentence Transformers embeddings, FAISS similarity search, and hosted LLM inference through an OpenAI-compatible API.
- Built document loading, normalized vector indexing, and top-3 retrieval over a five-document demonstration corpus of business notes.
- Designed prompts requesting source citations and acknowledgment of insufficient evidence, with retrieved text and similarity scores displayed for manual review.
- Documented system architecture, environment setup, data limitations, and a manual evaluation procedure for reproducible demonstrations.

These describe implementation, not measured quality. Do not claim reduced hallucinations, improved research accuracy, production readiness, or validated market insights without evidence.

## Chinese translation / 中文翻译

**AI 商业研究助手 | Python、RAG、Sentence Transformers、FAISS、OpenRouter**

开发命令行原型，通过语义相似度检索商业笔记，并将相关内容提供给托管大语言模型，生成带来源标签的回答。

- 使用 Python 将 Sentence Transformers 文本向量、FAISS 相似度检索和兼容 OpenAI 接口的托管大模型调用整合为 RAG 原型。
- 实现文档读取、向量归一化、索引建立及前三条相关文档检索，使用五篇商业示例笔记演示流程。
- 设计要求标注来源及说明证据不足的提示词，并显示检索原文与相似度分数，便于人工检查。
- 编写系统架构、环境配置、数据限制及人工评估说明，支持他人理解和复现项目演示。

建议放在简历的“个人项目”栏目。填写真实开发日期，不要把个人项目写成正式工作经历，也不要编造客户数量、准确率或商业成果。

## 60-second interview introduction

“I built a Python command-line assistant to explore how business notes can support language-model answers. The retrieval stage embeds documents and questions with the same Sentence Transformers model, then uses FAISS to select up to three relevant notes. The generation stage sends those notes to OpenRouter with instructions to cite the supplied sources and acknowledge missing evidence. I separated retrieval, LLM-only inference, and RAG into three scripts to inspect each stage. The current dataset is five illustrative notes, so I present it as a prototype. My next priorities are sourced data, a labeled evaluation set, and automatic checks for unsupported claims.”

中文：

“我开发了一个 Python 命令行助手，探索如何让大语言模型根据商业笔记回答问题。检索阶段用同一个 Sentence Transformers 模型把文档和问题转换成向量，再用 FAISS 选出最多三篇相关笔记。生成阶段将笔记发送给 OpenRouter，并通过提示词要求模型标注来源、说明资料不足。我把语义检索、单独调用大模型和完整 RAG 分成三个脚本，方便观察每个阶段。目前只有五篇示例笔记，所以我将它定位为原型。下一步会补充有来源的数据、建立标注评估集，并检查回答中缺乏依据的内容。”

## Questions to prepare

| Interview question | Answer to understand |
| --- | --- |
| Why RAG? | It supplies relevant external text at answer time and makes the evidence inspectable. It does not guarantee correctness. |
| Did you train the model? | No. I use pretrained embeddings and hosted generation; document indexing is not model training. |
| Why normalize vectors? | With unit-length vectors, inner product equals cosine similarity. |
| What does FAISS store here? | In-memory document vectors; the Python list retains the corresponding text. |
| Is Source 1 always Document 1? | No. It is the first result for that question. |
| How did you measure quality? | No benchmark result is claimed. Describe the actual checks and the evaluation plan, then show recorded results if available. |
| What is the main limitation? | Tiny unverified corpus, no relevance threshold, and no automatic validation of answer support. |
| How would you scale it? | Introduce better source metadata, token-aware chunks, persistent indexing, reusable modules, and measured retrieval improvements. |

## Before sharing publicly

1. Run the demonstration when the local environment permits it.
2. Record actual output and failures; identify the routed generator if the provider exposes it.
3. Add a sanitized screenshot or short video only after a real run. No screenshot is supplied by this documentation update.
4. Confirm only intended files are staged and no credentials appear.
5. Publish through your normal Git workflow. This update does not push, deploy, or create a release.
6. Link the repository on your résumé and prepare to explain the pipeline without reading the code.

If runtime is blocked, state it clearly and avoid describing the demonstration as successfully validated.
