---
name: bioc-fulltext-fetch
description: 给定 PMID / PMCID 取结构化全文（BioC XML/JSON）。封装 NLM BioC PubMed API（标题+摘要）和 BioC PMC OA API（开放获取全文），输出按章节切分的段落、表格上下文、RAG 友好 chunk。适合大批量入向量库。触发词：全文抽取 / BioC / RAG 入库 / 文献全文 / PMC 开放获取 / structured fulltext / 段落抽取 / 表格抽取 / fulltext to vector store。
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

封装 NLM BioC API,用于将 PubMed / PMC 文献转换为 RAG 友好的结构化全文 chunk。

## 1. 职责边界（单一职责）

**只做**:给定 PMID / PMCID,取结构化全文(BioC XML/JSON 格式),输出段落、章节、表格上下文、RAG chunk。

**不做**:
- 检索文献(交给 `pubmed-eutils` / `europepmc-search`)
- 实体标注(交给 `pubtator3`)
- 向量化(交给下游的 embedding pipeline / LangChain / LlamaIndex)
- ID 转换(可调用 `pubmed-eutils.elink_pubmed_to_pmc`,但本 skill 不实现 elink)

如果需要这些能力,请使用对应的 skill。

## 2. 何时使用

触发场景:
- "把这批 PMID 的全文取下来,准备入 ChromaDB"
- "我有 PMCID 列表,需要按章节切分做 RAG"
- "提取 Methods 章节段落"
- "找出表格周围的语义文本"
- "Build vector index from PMC open access papers"

不要使用本 skill 当:
- 用户只需要标题/摘要的纯文本 → 用 `pubmed-eutils.efetch`
- 用户需要做语义检索 → 用 `europepmc-search` 或 `pubmed-search`
- 用户需要实体标注(基因/疾病/化合物) → 用 PubTator3 类 skill

## 3. 两个 BioC 端点

| 端点 | 输入 | 覆盖 | 内容 |
|------|------|------|------|
| **BioC PubMed** | PMID | 全 PubMed (~37M) | 标题 + 摘要 + MeSH (结构化) |
| **BioC PMC OA** | PMCID | PMC 开放获取子集 (~10M) | 全文(章节、段落、表格、图注) |

端点示例:
```
# 摘要级
https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pubmed.cgi/BioC_json/{PMID}/unicode

# 全文级
https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json/{PMCID}/unicode
```

文档参考:
- BioC PubMed: https://www.ncbi.nlm.nih.gov/research/bionlp/APIs/BioC-PubMed/
- BioC PMC OA: https://www.ncbi.nlm.nih.gov/research/bionlp/APIs/BioC-PMC/

## 4. 推荐工作流

```
用户给 PMID list
  │
  ▼
[可选] elink PMID → PMCID  (调用 pubmed-eutils)
  │
  ├── PMCID 存在 + 是 OA ──► fetch_fulltext_bioc(pmcid)  ← 全文
  │                                  │
  │                                  ▼
  │                          extract_paragraphs / extract_tables_context
  │                                  │
  │                                  ▼
  │                          to_rag_chunks(chunk_size=512, overlap=50)
  │
  └── 不可用 / 非 OA ──────► fetch_abstract_bioc(pmid)   ← 摘要兜底
                                     │
                                     ▼
                              to_rag_chunks (摘要也按段切)
```

## 5. 核心能力(5 个函数)

### 5.1 `fetch_abstract_bioc(pmid: str) → BioCDocument`

取标题 + 摘要 + MeSH 的 BioC 结构化版本。

```python
doc = fetch_abstract_bioc("39523456")
# doc.passages → [{"infons": {"section_type": "TITLE"}, "text": "..."},
#                 {"infons": {"section_type": "ABSTRACT"}, "text": "..."}]
# doc.infons["mesh"] → ["Leukemia, Myeloid, Acute", "FLT3 Mutation", ...]
```

### 5.2 `fetch_fulltext_bioc(pmcid: str) → BioCDocument`

取 PMC OA 全文,按章节切分(`section_type` ∈ {TITLE, ABSTRACT, INTRO, METHODS, RESULTS, DISCUSS, CONCL, REF, FIG, TABLE, ...})。

```python
doc = fetch_fulltext_bioc("PMC10234567")
# 不可用时抛 NotOpenAccessError 或 NotFoundError
```

错误处理:
- `404` → 该 PMCID 不在 PMC OA 子集 → 抛 `NotOpenAccessError`,调用方应回退到 `fetch_abstract_bioc`
- `429` → 限流 → 退避重试(最多 3 次,指数退避)
- 网络错误 → 抛 `BioCFetchError`,记录日志

### 5.3 `extract_paragraphs(doc: BioCDocument) → list[Paragraph]`

按 BioC `passage` 提取段落数组,保留 section 标签 + 字符 offset。

```python
paragraphs = extract_paragraphs(doc)
# [
#   {"section_label": "INTRO", "text": "Acute myeloid leukemia (AML) is...",
#    "offset_start": 1234, "offset_end": 1820},
#   {"section_label": "METHODS", "text": "Flow cytometry was performed...",
#    "offset_start": 2890, "offset_end": 3401},
#   ...
# ]
```

实现要点:
- 跳过 `section_type ∈ {REF, FIG_LABEL}` 的纯标签段
- 合并连续相同 section 的短 passage(< 50 字符)
- offset 来自 BioC `passage.offset` 字段,保持原文索引一致

### 5.4 `extract_tables_context(doc: BioCDocument, window: int = 200) → list[TableContext]`

提取每个表格的上下文(前后 200 字),帮助 RAG 给表格打语义标签。

```python
tables = extract_tables_context(doc, window=200)
# [
#   {
#     "table_id": "T1",
#     "caption": "Patient baseline characteristics",
#     "before_context": "...as shown in Table 1, baseline characteristics...",
#     "after_context": "These data confirm that age and ELN risk...",
#     "section": "RESULTS"
#   },
#   ...
# ]
```

实现要点:
- BioC 中 table 通常以 `section_type=TABLE` 或 `passage.infons["xml"]="table"` 出现
- 上下文从同 section 内的相邻 passage 拼接
- 表格本体的结构化数据不解析(交给专门的 table parser),只取 caption + 周围文本

### 5.5 `to_rag_chunks(doc: BioCDocument, chunk_size: int = 512, overlap: int = 50) → list[Chunk]`

把 BioC 文档切成 RAG 入库友好的 chunk。

```python
chunks = to_rag_chunks(doc, chunk_size=512, overlap=50)
# 每个 chunk:
{
    "chunk_id": "PMC10234567_METHODS_2890",
    "text": "Flow cytometry was performed on bone marrow aspirates...",
    "metadata": {
        "pmcid": "PMC10234567",
        "pmid": "39523456",
        "section": "METHODS",
        "offset_start": 2890,
        "offset_end": 3401,
        "doi": "10.1038/s41586-024-xxxxx",
        "year": 2024,
        "is_oa": True,
        "title": "Targeting FLT3 in AML: ...",
        "journal": "Nature",
    }
}
```

切片策略:
- 单位:tokens(用 `tiktoken` cl100k_base)而非字符,默认 512 token
- **不跨章节切**:每个 section 独立切片,避免 chunk 跨越 Methods/Results 边界
- 段落优先:尽量在段落边界切,实在超长再硬切
- overlap:50 token,保证语义连续性
- `chunk_id` 格式:`{pmcid}_{section}_{offset_start}` 唯一可追溯

## 6. 速率限制 + 缓存

### 速率
- BioC 不强制 RPS,但服务端对滥用 IP 会封禁
- 建议 ≤ 5 RPS,批量超过 100 篇时降到 3 RPS
- 用 `asyncio.Semaphore(5)` 或 `aiolimiter` 控制并发

### 缓存
- 位置:`~/.cache/bioc/{pmcid_or_pmid}.json`(原始 BioC JSON)
- 索引:SQLite 元数据表 `~/.cache/bioc/index.db`
  ```sql
  CREATE TABLE bioc_cache (
      key TEXT PRIMARY KEY,        -- "pmc:PMC10234567" or "pmid:39523456"
      file_path TEXT,
      fetched_at INTEGER,           -- Unix epoch
      is_oa INTEGER,
      doi TEXT,
      year INTEGER
  );
  ```
- 过期:默认 30 天(`CACHE_TTL_DAYS=30`),可通过环境变量覆盖
- 命中流程:查 SQLite → 检查 mtime → 未过期则读 JSON;过期或不存在则重新拉取
- 失效场景:用户传 `force_refresh=True` 时绕过缓存

## 7. 错误处理

| 错误 | 类型 | 处理 |
|------|------|------|
| HTTP 404 (PMC OA) | `NotOpenAccessError` | 调用方回退到 abstract |
| HTTP 404 (PubMed) | `NotFoundError` | 该 PMID 不存在,记录并跳过 |
| HTTP 429 | `RateLimitError` | 指数退避重试 (1s, 2s, 4s),最多 3 次 |
| HTTP 5xx | `BioCServerError` | 重试 3 次后抛出 |
| JSON 解析失败 | `BioCParseError` | 记录原始响应,跳过 |
| 网络超时 | `BioCTimeoutError` | timeout=30s,重试 1 次 |

所有错误继承 `BioCFetchError` 基类,调用方可以统一捕获。

## 8. RAG 集成示例

### 8.1 LangChain

```python
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# 1. 取全文 → chunk
pmcids = ["PMC10234567", "PMC11122233", ...]
all_chunks = []
for pmcid in pmcids:
    try:
        doc = fetch_fulltext_bioc(pmcid)
    except NotOpenAccessError:
        # 回退到摘要
        pmid = elink_pmc_to_pubmed(pmcid)  # 调用 pubmed-eutils
        doc = fetch_abstract_bioc(pmid)
    all_chunks.extend(to_rag_chunks(doc, chunk_size=512, overlap=50))

# 2. 转 LangChain Document
lc_docs = [
    Document(page_content=c["text"], metadata=c["metadata"])
    for c in all_chunks
]

# 3. 入向量库
vectorstore = Chroma.from_documents(
    lc_docs,
    embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
    collection_name="aml_literature",
    persist_directory="./chroma_aml",
)
```

### 8.2 LlamaIndex

```python
from llama_index.core import Document, VectorStoreIndex
from llama_index.embeddings.openai import OpenAIEmbedding

li_docs = [
    Document(
        text=c["text"],
        metadata=c["metadata"],
        doc_id=c["chunk_id"],
        excluded_llm_metadata_keys=["offset_start", "offset_end"],
    )
    for c in all_chunks
]
index = VectorStoreIndex.from_documents(
    li_docs,
    embed_model=OpenAIEmbedding(model="text-embedding-3-small"),
)
index.storage_context.persist("./li_aml_index")
```

### 8.3 元数据过滤检索(LangChain)

```python
# 只在 Methods 章节检索
retriever = vectorstore.as_retriever(
    search_kwargs={"filter": {"section": "METHODS"}, "k": 5}
)
results = retriever.invoke("flow cytometry gating strategy for AML blasts")
```

## 9. 与其他 skill 的协作

| 配合的 skill | 用途 |
|--------------|------|
| `pubmed-eutils` | PMID ↔ PMCID 转换(elink) |
| `europepmc-search` / `pubmed-search` | 先检索得到 PMID list |
| `pubtator3` | 在 chunk 上叠加实体标注(基因、疾病、化合物) |
| `medical-research` | 上层科研 narrative 生成 |

典型 pipeline:
```
europepmc-search ──► PMID list ──► pubmed-eutils.elink ──► PMCID list
                                                              │
                                                              ▼
                                            bioc-fulltext-fetch (本 skill)
                                                              │
                                                              ▼
                                          [可选] pubtator3 实体叠加
                                                              │
                                                              ▼
                                                     LangChain / LlamaIndex
```

## 10. 环境与依赖

```toml
# pyproject 片段
[project]
dependencies = [
    "httpx>=0.27",          # 异步 HTTP
    "aiolimiter>=1.1",      # RPS 限流
    "tiktoken>=0.7",        # token 计数
    "tenacity>=9.0",        # 退避重试
    "platformdirs>=4.0",    # 缓存目录定位
]
```

环境变量:
- `BIOC_CACHE_DIR`(可选,默认 `~/.cache/bioc`)
- `BIOC_CACHE_TTL_DAYS`(默认 30)
- `BIOC_MAX_RPS`(默认 5)
- `BIOC_TIMEOUT_SEC`(默认 30)

## 11. 测试要点

| 测试 | 预期 |
|------|------|
| `fetch_abstract_bioc("39523456")` | 返回 title + abstract passages |
| `fetch_fulltext_bioc("PMC10234567")` | 返回章节切分的全文 |
| `fetch_fulltext_bioc("PMC1")` (非 OA) | 抛 `NotOpenAccessError` |
| `extract_paragraphs(doc)` | 段落数 ≥ 3,每段有 section_label |
| `extract_tables_context(doc)` | 表格上下文左右各 ≤ 200 字 |
| `to_rag_chunks(doc, 512, 50)` | chunk token ≤ 512,overlap ≈ 50,不跨章节 |
| 缓存命中 | 第二次调用 < 50ms,无网络请求 |
| 429 退避 | 模拟 429 响应后能在 3 次内成功 |

最低单元测试覆盖率 80%,集成测试用 5 篇真实 PMCID 跑端到端。

## 12. 已知限制与避坑

1. **OA 子集只占 PMC 的 ~25%**:大量 PMID 没有可用全文,务必准备 abstract 兜底路径
2. **章节标签不统一**:不同期刊的 `section_type` 命名有差异(`INTRO` vs `Introduction`),做归一化
3. **公式与符号**:BioC unicode 端点把数学符号转 Unicode,但希腊字母/特殊符号偶尔丢失,关键公式建议从原 XML 端点取
4. **图与表的图像**:BioC 不返回图像,只有 caption 和周围文本;如需图像走 PMC FTP
5. **大文档内存**:单篇 PMC 全文 BioC JSON 可达 1-3 MB,批量处理时注意流式或分批
6. **非英文文献**:BioC PubMed 对非英文摘要支持有限,可能返回原文(西班牙语/中文等),embedding 模型需多语言版本
7. **历史版本**:BioC 端点不返回文章版本号,如需追溯版本变更走 NCBI E-utilities 的 history
8. **不要直接走 PubTator3 全文端点替代**:PubTator3 的 BioC 输出是带实体标注的"加料版",数据量更大且会绑定标注模型版本,本 skill 保持纯净结构化全文,标注由独立 skill 叠加

完成。该 skill 应当与 `pubmed-eutils` 和 `europepmc-search` 形成"检索 → ID 转换 → 全文抽取 → RAG 入库"完整闭环。
