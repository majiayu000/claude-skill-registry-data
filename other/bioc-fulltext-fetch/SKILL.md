---
name: bioc-fulltext-fetch
description: 给定 PMID/PMCID 取结构化全文（NLM BioC XML/JSON）。封装 BioC PubMed（标题+摘要）和 BioC PMC OA（开放获取全文）端点，输出按章节切分的段落、表格上下文、RAG 友好 chunk，适合大批量入向量库。Fetches structured fulltext from NLM BioC API for PMID/PMCID, outputs section-segmented paragraphs and RAG-ready chunks. 触发词：全文抽取 / BioC / RAG 入库 / 文献全文 / PMC 开放获取 / structured fulltext / 段落抽取 / 表格抽取 / chunking / fulltext to vector store / paragraph extraction.
keywords:
  - bioc
  - fulltext-extraction
  - pmc-open-access
  - rag-ingestion
  - structured-fulltext
  - paragraph-extraction
  - table-extraction
  - vector-store
  - chunking
  - section-segmentation
license: MIT
---

# BioC Fulltext Fetch

封装 NLM BioC API，把 PubMed / PMC 文献转成 RAG 友好的结构化全文 chunk。**只做全文抽取与切片，不做检索、不做实体标注、不做向量化。**

## 1. 何时使用

触发场景：
- "把这批 PMID 的全文取下来准备入 ChromaDB / 我有 PMCID 列表要按章节切分做 RAG"
- "提取 Methods 章节段落 / 找出表格周围的语义文本"
- "Build vector index from PMC open access papers"
- "PMC1234567 的全文段落 + 章节标签"
- "把 100 篇血液 IFI PMID 入向量库"

不要使用本 skill：
- 用户只要标题/摘要纯文本 → 用 `pubmed-eutils` efetch
- 用户要做语义检索找文献 → 用 `pubmed-search` / `europepmc-search`
- 用户要实体标注（基因/疾病/化合物）→ 用 `pubtator-entity-search`（可在本 skill 输出之上叠加，不替代）
- 用户要做证据等级评分 → 用 `medical-evidence-grading`（其内部会调用本 skill 抽 Methods 段落）

## 2. 跨 skill 协作（显式）

| 上游 / 下游 skill | 协作方式 |
|------------------|----------|
| `pubmed-eutils.elink_pubmed_to_pmc()` | **上游**，把 PMID 列表转换成 PMCID 列表，喂给本 skill |
| `europepmc-search.get_full_text_links()` | **替代源**，当 PMC OA 不可用时回退到 Europe PMC 的开放获取链接 |
| `pubtator-entity-search` | **后置叠加**，在本 skill 产的 chunk 上做实体标注，不替代本 skill |
| `medical-evidence-grading` | **下游**，调 `extract_paragraphs` 取 Methods 段落做 sample size / study design 检测 |

典型 pipeline：
```
europepmc-search ──► PMID list ──► pubmed-eutils.elink ──► PMCID list
                                                              │
                                                              ▼
                                            bioc-fulltext-fetch (本 skill)
                                                              │
                                                              ├─► [可选] pubtator-entity-search 实体叠加
                                                              ├─► [可选] medical-evidence-grading 证据评分
                                                              └─► LangChain / LlamaIndex 入库
```

## 3. 两个 BioC 端点

| 端点 | 输入 | 覆盖 | 内容 |
|------|------|------|------|
| **BioC PubMed** | PMID | 全 PubMed (~37M) | 标题 + 摘要 + MeSH（结构化） |
| **BioC PMC OA** | PMCID | PMC 开放获取子集（~10M，约占 PMC 25%） | 全文章节、段落、表格、图注 |

```
摘要级:  https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pubmed.cgi/BioC_json/{PMID}/unicode
全文级:  https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json/{PMCID}/unicode
```

格式细节、`section_type` 取值、字符 offset 一致性见 [`references/bioc-format-spec.md`](references/bioc-format-spec.md)。

## 4. 推荐工作流

```
PMID list
  │
  ▼
[可选] elink PMID→PMCID  (调 pubmed-eutils)
  │
  ├─ PMCID 存在且 OA ──► fetch_fulltext_bioc(pmcid) ──► extract_paragraphs / extract_tables_context ──► to_rag_chunks
  │
  └─ 不可用/非 OA ─────► fetch_abstract_bioc(pmid) ─────────────────────────────────────────────────► to_rag_chunks
```

## 5. 核心能力（5 个函数 · 跨平台签名）

### 5.1 `fetch_abstract_bioc(pmid: str) -> BioCDocument`

取标题 + 摘要 + MeSH 的 BioC 结构化版本。

```python
doc = fetch_abstract_bioc("39523456")
# doc.passages → [{"infons": {"section_type": "TITLE"}, "text": "..."},
#                 {"infons": {"section_type": "ABSTRACT"}, "text": "..."}]
# doc.infons["mesh"] → ["Leukemia, Myeloid, Acute", "FLT3 Mutation", ...]
```

### 5.2 `fetch_fulltext_bioc(pmcid: str) -> BioCDocument`

取 PMC OA 全文，按章节切分（`section_type` ∈ {TITLE, ABSTRACT, INTRO, METHODS, RESULTS, DISCUSS, CONCL, REF, FIG, TABLE, ...}）。

```python
doc = fetch_fulltext_bioc("PMC10234567")
# 不可用时抛 NotOpenAccessError，调用方应回退到 fetch_abstract_bioc
```

### 5.3 `extract_paragraphs(doc: BioCDocument) -> list[Paragraph]`

按 BioC `passage` 提取段落数组，保留 section 标签 + 字符 offset。

```python
paragraphs = extract_paragraphs(doc)
# [{"section_label": "METHODS", "text": "Flow cytometry was performed...",
#   "offset_start": 2890, "offset_end": 3401}, ...]
```

要点：跳过 `REF` / `FIG_LABEL` 纯标签段；合并同 section 内 < 50 字符短 passage；offset 来自 BioC `passage.offset`。

### 5.4 `extract_tables_context(doc: BioCDocument, window: int = 200) -> list[TableContext]`

提取每个表格的上下文（前后 200 字），帮 RAG 给表打语义标签。

```python
tables = extract_tables_context(doc, window=200)
# [{"table_id": "T1", "caption": "Patient baseline characteristics",
#   "before_context": "...", "after_context": "...", "section": "RESULTS"}, ...]
```

表格本体（cell 数据）不解析；只取 caption + 周围文本。

### 5.5 `to_rag_chunks(doc: BioCDocument, chunk_size: int = 512, overlap: int = 50) -> list[Chunk]`

把 BioC 文档切成 RAG 入库 chunk。token 单位、不跨章节、段落优先、可追溯 `chunk_id`。

```python
chunks = to_rag_chunks(doc, chunk_size=512, overlap=50)
# {
#   "chunk_id": "PMC10234567_METHODS_2890",
#   "text": "...",
#   "metadata": {"pmcid": "...", "pmid": "...", "section": "METHODS",
#                "offset_start": 2890, "offset_end": 3401, "doi": "...",
#                "year": 2024, "is_oa": True, "title": "...", "journal": "..."}
# }
```

切片策略详见 [`references/chunking-strategies.md`](references/chunking-strategies.md)。

## 6. 速率限制 + 缓存

- **速率**：BioC 不强制 RPS，但建议 ≤ 5 RPS（批量 > 100 篇时降到 3）；用 `asyncio.Semaphore(5)` 或 `aiolimiter`
- **缓存**：`~/.cache/bioc/{id}.json` + SQLite 索引 `index.db`（key, file_path, fetched_at, is_oa, doi, year）
- **TTL**：默认 30 天（`BIOC_CACHE_TTL_DAYS`），`force_refresh=True` 绕过

## 7. 错误处理

所有错误继承 `BioCFetchError` 基类。

| 错误 | 类型 | 处理 |
|------|------|------|
| 404 (PMC OA) | `NotOpenAccessError` | 调用方回退 abstract |
| 404 (PubMed) | `NotFoundError` | PMID 不存在，跳过 |
| 429 | `RateLimitError` | 指数退避 1s/2s/4s，最多 3 次 |
| 5xx | `BioCServerError` | 重试 3 次后抛出 |
| JSON 解析失败 | `BioCParseError` | 记录原始响应，跳过 |
| 超时（默认 30s） | `BioCTimeoutError` | 重试 1 次 |

## 8. 失败模式与避坑（必读）

1. **OA 不可用**：PMC OA 子集仅占 PMC 的 ~25%，大量 PMID 没有可用全文。**必须**在调用方实现 abstract 兜底路径，不要假设 fetch_fulltext_bioc 总能成功。
2. **章节标签不统一**：不同期刊的 `section_type` 命名有差异（`Methods` vs `Materials and Methods` vs `Subjects and Methods`），BioC 已部分归一化但仍有例外（综述偶尔出现 `INTRO_RESULTS` 合并段）。下游过滤时用集合而非精确匹配。
3. **公式与 unicode 丢失**：BioC unicode 端点把数学符号转 Unicode，但希腊字母 / 上下标偶尔丢失。关键公式建议从 `BioC_xml` 端点取，或解析时检测 `?` 占位符。
4. **chunk 跨章节切碎**：朴素的 token 切片会让 Methods 末尾和 Results 开头被切到同一 chunk，破坏 section 过滤检索。`to_rag_chunks` 默认按 section 分组，不要绕过。
5. **缓存命中但 TTL 过期**：批量任务跨天运行时，第二天命中缓存的旧条目可能与新条目混用（DOI 元数据已更新）。检查 `fetched_at` 而非只看文件存在。
6. **BioC API 超时**：单篇大文档（> 1MB BioC JSON）在网络抖动时易超时。timeout 不要低于 30s；批量任务必须有失败隔离（`failed.jsonl`），不能让一篇阻断整批。
7. **大文档内存**：单篇 PMC 全文 BioC JSON 可达 1–3 MB，1000 篇并发会吃 3 GB RAM。批量处理用流式读写或分批 flush。
8. **不要走 PubTator3 全文端点替代**：PubTator3 的 BioC 输出绑定标注模型版本，体积更大；本 skill 保持纯净结构化全文，标注由 `pubtator-entity-search` 后置叠加。

## 9. RAG 集成

LangChain / LlamaIndex / 元数据过滤检索 / pubtator 实体叠加 / medical-evidence-grading 联用的完整代码示例见 [`references/rag-integration.md`](references/rag-integration.md)。

## 10. 环境与依赖

```toml
[project]
dependencies = [
  "httpx>=0.27",       # 异步 HTTP
  "aiolimiter>=1.1",   # RPS 限流
  "tiktoken>=0.7",     # token 计数
  "tenacity>=9.0",     # 退避重试
  "platformdirs>=4.0", # 缓存目录
]
```

环境变量：`BIOC_CACHE_DIR`（默认 `~/.cache/bioc`）、`BIOC_CACHE_TTL_DAYS`（30）、`BIOC_MAX_RPS`（5）、`BIOC_TIMEOUT_SEC`（30）。

## 11. 测试要点

| 测试 | 预期 |
|------|------|
| `fetch_abstract_bioc("39523456")` | 返回 title + abstract passages |
| `fetch_fulltext_bioc("PMC10234567")` | 返回章节切分的全文 |
| `fetch_fulltext_bioc("PMC1")` 非 OA | 抛 `NotOpenAccessError` |
| `extract_paragraphs(doc)` | 段落 ≥ 3，每段有 section_label |
| `extract_tables_context(doc)` | 上下文左右各 ≤ 200 字 |
| `to_rag_chunks(doc, 512, 50)` | chunk token ≤ 512、overlap ≈ 50、不跨章节 |
| 缓存命中 | 第二次调用 < 50ms，无网络请求 |
| 429 退避 | 模拟 429 后能在 3 次内成功 |

最低单元测试覆盖率 80%，集成测试用 5 篇真实 PMCID 跑端到端。

## 12. References

- [`references/bioc-format-spec.md`](references/bioc-format-spec.md) — BioC XML/JSON 格式规范、字段定义、`section_type` 取值
- [`references/rag-integration.md`](references/rag-integration.md) — LangChain Chroma + LlamaIndex 完整代码、批量入库要点、向量库选型
- [`references/chunking-strategies.md`](references/chunking-strategies.md) — token 切片、不跨章节策略、overlap 设计、chunk_id 设计、评测指标
