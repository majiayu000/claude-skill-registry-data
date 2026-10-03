---
name: europepmc-search
description: Europe PMC RESTful Web Service 多源文献聚合检索原子 skill。**使用本 skill 进行医学文献广召回 / RAG 知识库构建 / 跨库聚合 / 预印本扫描 / 全文链接发现**。一次调用同时召回 PubMed (MED) + PMC + AGRICOLA + CABI + 预印本(bioRxiv / medRxiv / ChemRxiv / Research Square)+ NCBI Bookshelf + 专利,自动按 PMID/PMCID/DOI 三级去重,返回完整元数据(全文 OA 链接、citations、grants 资助信息)。**定位:广召回 · 多源 · RAG 友好**(与 pubmed-eutils 互补 — 后者做单源精准官方检索 + Clinical Queries;本 skill 做"撒网"式多源聚合)。触发词:Europe PMC / EuropePMC / 多源文献聚合 / 广召回 / RAG 召回 / RAG 知识库 / 预印本搜索 / preprint search / bioRxiv / medRxiv / ChemRxiv / DOI 检索 / DOI lookup / 全文链接 / full-text links / OA 全文 / PMCID / 灰色文献 / grey literature / 跨库去重 / 资助检索 / grant search / NIH funded / Wellcome funded / citations metadata。**不做**:NCBI E-utilities 直检(→ pubmed-eutils)、临床试验注册(→ clinical-trials-v2)、全文 XML 抽取(→ bioc-fulltext-fetch)、实体识别(→ pubtator-entity-search)、证据分级(→ medical-evidence-grading)、参考文献终态写入(→ evidence-appendix-sync)。
keywords:
  - europe-pmc
  - europepmc
  - 多源文献聚合
  - rag-召回
  - rag-知识库
  - 广召回
  - 预印本
  - preprint
  - biorxiv
  - medrxiv
  - chemrxiv
  - research-square
  - 全文链接
  - full-text-links
  - oa-全文
  - doi-检索
  - doi-lookup
  - pmcid
  - 灰色文献
  - grey-literature
  - grants-检索
  - nih-funded
  - citations-metadata
  - 跨库去重
license: MIT
---

# europepmc-search

Europe PMC RESTful Web Service 的薄封装。**一次请求 = 多源召回**:PubMed(MED)、PubMed Central(PMC)、AGRICOLA(AGR)、CABI(CBA)、预印本(PPR,涵盖 bioRxiv/medRxiv/ChemRxiv/arXiv 生命科学子集/Research Square/SSRN/Preprints.org)、专利(PAT)、NCBI Bookshelf(NBK)、ETHOS 论文集等。

跨平台 Python(Windows / macOS / Linux 均可),无需 Anaconda 锁定环境。

## 1. 何时使用本 skill

| 场景 | 用本 skill | 应改用 |
|------|-----------|------|
| RAG 知识库构建,需"撒网"式广召回 | ✅ | — |
| 同时要 PubMed + 预印本 | ✅ | — |
| 拿 DOI 反查全文 OA 链接 | ✅ | — |
| 找特定基金(NIH/NSFC/Wellcome)资助的研究 | ✅(`grant_id`) | — |
| 只要 PubMed 官方源 + Clinical Queries | ❌ | `pubmed-eutils` |
| 抽取已知 PMCID 的全文 XML / 段落 | ❌ | `bioc-fulltext-fetch` |
| 临床试验注册号检索 | ❌ | `clinical-trials-v2` |
| 实体(基因/疾病/化合物)关联 | ❌ | `pubtator-entity-search` |
| 给文献排 GRADE 等级 | ❌ | `medical-evidence-grading` |
| 报告 Appendix C 终态参考文献 | ❌ | `evidence-appendix-sync` |

**与 pubmed-eutils 的差异化(必读)**:

- pubmed-eutils:PubMed **单源** · Clinical Queries · MeSH 精准 · PubDate 严格范围 → **高精准**
- europepmc-search:**多源聚合** + 自动去重 + 全文链接 + citations metadata → **高召回**
- 推荐编排:RAG 知识库构建 → 本 skill 广召回 → 输出 PMID 列表 → `pubmed-eutils` 精准复核 → `bioc-fulltext-fetch` 取 OA 全文 → `pubtator-entity-search` 实体抽取 → `medical-evidence-grading` 分级 → `evidence-appendix-sync` 写入报告

## 2. 配置加载

Europe PMC RESTful 是**完全开放 API,无需 API key**,但服务条款要求传 `email` 联系方式。

**配置加载顺序**(高到低):
1. 项目级:`.config/europepmc.local.yaml`
2. 用户级:`~/.config/europepmc.yaml`
3. 环境变量:`EUROPEPMC_EMAIL`
4. 都没有 → 退化为 `anonymous@example.org` 并打印 ⚠️ 警告

```yaml
# ~/.config/europepmc.yaml
email: your-email@example.com
default_page_size: 100
default_result_type: core      # lite | core | idlist
default_format: json
timeout_seconds: 30
max_retries: 3
```

## 3. API 端点速查

基础 URL:`https://www.ebi.ac.uk/europepmc/webservices/rest/`

| 端点 | 用途 |
|------|------|
| `search` | 通用检索(本 skill 主力) |
| `article/{source}/{id}` | 单篇详情 |
| `{source}/{id}/fullTextXML` | 全文 XML(仅 OA PMC 子集) |
| `{source}/{id}/references` | 参考文献 |
| `{source}/{id}/citations` | 被引列表 |
| `{source}/{id}/supplementaryFiles` | 补充材料 |
| `grant/search` | 资助检索 |

## 4. 核心检索能力(5 个原子函数,带 type hint)

### 4.1 `search_articles`

```python
from typing import Literal
def search_articles(
    query: str,
    source_filter: list[str] | None = None,
    max_results: int = 200,
    sort: Literal["date", "cited"] | None = None,
) -> list[dict]:
    """通用多源检索,自动 cursorMark 分页拉满到 max_results。"""
```

- `source_filter`:`["MED","PMC","PPR"]` 限定来源;`None` = 全部。详细来源代码见 `references/source-filters.md`
- 返回每条含 `pmid / pmcid / doi / title / authors / journal / pub_year / abstract / source / is_preprint / preprint_server / has_full_text / oa_status / cited_by_count` 等(完整 schema 见 §11)

### 4.2 `get_article_details`

```python
def get_article_details(identifier: str) -> dict:
    """单篇完整元数据。identifier 自动识别:
    - 纯数字 → PMID(查 MED)
    - PMC 前缀 → PMCID(查 PMC)
    - 10. 开头 → DOI(用 query=DOI:"..." 反查)
    - PPR 前缀 → 预印本 ID(查 PPR)
    """
```

### 4.3 `get_full_text_links`

```python
def get_full_text_links(pmid_or_pmcid: str) -> dict[str, str | list[str] | None]:
    """返回所有可用全文链接,按类型分类:
    {
      "oa_xml": "...",            # OA 子集才有
      "oa_pdf": "...",
      "publisher_html": "...",
      "subscription": [...],       # SUBSCRIPTION 类型
      "text_mining": [...],        # TM 类型
      "preprint_server": "..."     # 仅预印本
    }"""
```

### 4.4 `search_with_grants`

```python
def search_with_grants(
    query: str,
    grant_id: str | None = None,
    funder: str | None = None,
) -> list[dict]:
    """资助检索。Europe PMC 有专门的 GRANT_ID / FUNDER 字段。
    例:search_with_grants(query="cancer", grant_id="R01-CA123456")
        search_with_grants(query="cardiology", funder="Wellcome Trust")
    """
```

### 4.5 `find_similar_articles`

```python
def find_similar_articles(pmid_or_pmcid: str, limit: int = 20) -> list[dict]:
    """调用 Europe PMC 内置 'Similar Articles' 算法(MeSH + 文本相似度)。
    比 PubMed elink neighbor 召回略广,适合 RAG 邻域扩展。"""
```

## 5. Auto-trigger prompt 模拟

| 用户 prompt 示例 | 应否触发本 skill |
|------------------|----------------|
| "找血液 IFI 相关的 PubMed + PMC + 预印本聚合检索" | ✅ 触发 |
| "给我所有支持论文的全文链接,包括 OA 状态" | ✅ 触发(`get_full_text_links`) |
| "查特定 NIH grant R01CA255621 资助的肿瘤研究" | ✅ 触发(`search_with_grants`) |
| "我做 RAG 知识库,需要广撒网召回 1000 条" | ✅ 触发 |
| "DOI 10.1038/... 反查全文链接" | ✅ 触发(`get_article_details` + `get_full_text_links`) |
| "我只要 PubMed 官方源的高精准查询 + Clinical Queries 过滤" | ❌ 改用 `pubmed-eutils` |
| "查 PMC 文章 PMC10987654 的全文段落" | 部分:本 skill `get_full_text_links` 给链接 → 全文取用交 `bioc-fulltext-fetch` |
| "给 200 篇文献排 GRADE 等级" | ❌ 改用 `medical-evidence-grading`(可链式接本 skill 输出) |
| "找 NCT12345678 临床试验招募信息" | ❌ 改用 `clinical-trials-v2` |

## 6. 查询语法核心字段

最常用字段速查(完整 cheatsheet 见 `references/query-syntax.md`):

| 字段 | 示例 |
|------|------|
| `TITLE` / `TITLE_ABS` | `TITLE_ABS:"acute myeloid leukemia"` |
| `AUTH` | `AUTH:"Smith J"` |
| `JOURNAL` | `JOURNAL:"Nature"` |
| `PUB_YEAR` | `PUB_YEAR:[2020 TO 2024]` |
| `PUB_TYPE` | `PUB_TYPE:"Review"` |
| `SRC` | `SRC:MED` / `SRC:PPR` |
| `HAS_FT` / `OPEN_ACCESS` | `HAS_FT:Y AND OPEN_ACCESS:Y` |
| `MESH` | `MESH:"Hematologic Neoplasms"` |
| `GRANT_ID` / `FUNDER` | `GRANT_ID:"R01CA12345"` |
| `DOI` | `DOI:"10.1038/s41586-020-2196-x"` |

⚠️ 字段名 **必须大写**,`title:foo` 会被当成普通短语。

## 7. 多源去重(本 skill 强制内置)

同一篇文章常在 MED + PMC + PPR 同时出现。去重规则按优先级:

1. **PMID 相同 → 合并**,保留 MED 版本(PubMed 元数据最权威)
2. **PMCID 相同 → 合并**,保留 PMC 版本(因含全文)
3. **DOI 相同 → 合并**,优先 MED > PMC > PPR
4. **预印本特殊处理**:同一 DOI 既有预印本(PPR)又有正式发表(MED) → 两条都保留,但预印本条目标记 `superseded_by_pmid: <发表版 PMID>`,下游 `medical-evidence-grading` 据此自动丢弃。

## 8. 预印本处理(医学证据特别注意)

每条 PPR 结果显式标注:

```python
{
  "source": "PPR",
  "is_preprint": True,
  "preprint_server": "bioRxiv",   # 或 medRxiv / ChemRxiv / Research Square / SSRN
  "preprint_doi": "10.1101/2024.03.15.123456",
  "posted_date": "2024-03-15",
  "version": 2
}
```

下游 `medical-evidence-grading` 看到 `is_preprint=True` 自动**降权**(GRADE 中作为 "very low" 起点)。本 skill 自身**不做证据分级**,只如实标注。

## 9. 失败模式表(标准化)

| ID | 故障 | 现象 | 处理 / 抛出 |
|----|------|------|------------|
| F1 | API 速率限制(429) | HTTP 429 + `Retry-After` | 指数退避 `2^n + jitter`,最多 `max_retries=3`;仍失败抛 `EuropePMCRateLimitError` |
| F2 | 多源去重失败 | 同 DOI/PMID 出现多条未合并 | 走 `_dedupe_three_tier()` 强制去重;若三级 ID 都缺,按 `(title 前 80 字 + first_author + pub_year)` MD5 哈希再合并;无法合并则保留并标 `dedup_warning=True` |
| F3 | 预印本未标记 | 结果里 `source=="PPR"` 但 `is_preprint=False` | 检测到 source==PPR 强制设 `is_preprint=True`,补 `preprint_server` 字段(从 publisher 字段映射);写 WARN log |
| F4 | cursorMark 分页失败 | `nextCursorMark` 与上次相同但 `hitCount` 未取完 / 连续两次空响应 | 第一种正常终止;第二种抛 `EuropePMCPaginationError`,附最后一次 cursor 值便于断点续抓。详见 `references/cursormark-pagination.md` |
| F5 | email 未配置警告 | 配置链 4 级全空 | 退化用 `anonymous@example.org`,**首次请求前打印 ⚠️ WARN**,提示用户配置 `~/.config/europepmc.yaml` |
| F6 | 查询语法错误 | HTTP 400 + `errMsg` | 抛 `EuropePMCQueryError(errMsg)`,**不静默吞**;常见原因:字段名小写、引号未配对、`AND/OR` 未大写 |
| F7 | 命中为 0 | HTTP 200 + `hitCount=0` | 返回空列表 + WARN"无命中,建议放宽 query / 移除 source_filter / 检查字段大小写" |
| F8 | 服务端 5xx / 超时 | HTTP 5xx 或 `requests.Timeout` | 指数退避重试 `max_retries` 次;仍失败抛 `EuropePMCServerError` |
| F9 | 结果超 max_results | `hitCount > max_results` | 截断并在返回 dict 顶层设 `truncated=True`,附 `last_cursor_mark` 便于续抓 |

致命错误一律抛异常,不静默吞(遵循 `coding-style.md` 错误处理原则)。

## 10. 分页与流量(摘要)

- 单页上限 `pageSize=1000`
- **强制使用 `cursorMark`**(从 `*` 起),不要用 `page=` 偏移分页(>1000 条时官方不保证一致性)
- 全局并发 ≤ 5,QPS ≤ 8
- 详细分页规则、退避策略、并发陷阱 → `references/cursormark-pagination.md`

## 11. 输出契约(下游 skill 依赖)

每篇文章返回的标准 schema(本 skill 是契约源 — `bioc-fulltext-fetch` / `pubtator-entity-search` / `medical-evidence-grading` / `evidence-appendix-sync` 都按此消费):

```python
{
  "primary_id": "PMID:38123456" | "PMCID:PMC10987654" | "DOI:10.xxx/...",
  "all_ids": {"pmid": str|None, "pmcid": str|None, "doi": str|None, "ppr_id": str|None},
  "title": str,
  "authors": [{"full_name": str, "affiliation": str|None, "orcid": str|None}],
  "journal": {"name": str, "iso_abbr": str|None, "issn": str|None},
  "pub_year": int,
  "pub_date": "YYYY-MM-DD",
  "abstract": str|None,
  "mesh_terms": list[str],
  "keywords": list[str],
  "source": "MED" | "PMC" | "PPR" | "AGR" | "CBA" | "PAT" | "NBK",
  "sources_merged": list[str],         # 去重前出现的所有源
  "is_preprint": bool,
  "preprint_server": str|None,
  "preprint_doi": str|None,
  "version": int|None,
  "superseded_by_pmid": str|None,
  "has_full_text": bool,
  "oa_status": "OA" | "SUBSCRIPTION" | "UNKNOWN",
  "full_text_links": {"oa_xml": str|None, "oa_pdf": str|None, "publisher_html": str|None},
  "cited_by_count": int,
  "grants": [{"grant_id": str, "agency": str, "country": str|None}],
  "fetched_at": "ISO-8601 UTC",
  "europepmc_url": "https://europepmc.org/article/MED/38123456"
}
```

**字段缺失用 `None`,不省略 key**(下游解构稳定性)。

## 12. 与同体系其他 skill 的协作链路

```
[用户问题]
    │
    ├─→ europepmc-search       ← 本 skill (广召回 200~1000 条 + 多源去重)
    │       │
    │       ├─→ pubmed-eutils         ← 拿 PMID 子集精准复核 + Clinical Queries
    │       │       │
    │       │       └─→ bioc-fulltext-fetch  ← OA PMC 全文 XML
    │       │               │
    │       │               └─→ pubtator-entity-search  ← 实体识别
    │       │                       │
    │       │                       └─→ medical-evidence-grading  ← GRADE 分级
    │       │                              (依据 is_preprint 自动降权)
    │       │                              │
    │       │                              └─→ evidence-appendix-sync  ← 终下游(写 Appendix C)
    │       │
    │       └─→ medical-evidence-grading 也可直接消费本 skill 输出(跳过精准复核)
    │
    └─→ clinical-trials-v2 / aact-bulk-trials  ← 试验注册号另走专线
```

## 13. 调用示例

```python
from europepmc_search import EuropePMCClient

cli = EuropePMCClient()  # 自动加载 ~/.config/europepmc.yaml

# 1) 广召回:急性髓系白血病近 5 年 PubMed + 预印本
hits = cli.search_articles(
    query='(TITLE:"acute myeloid leukemia" OR ABSTRACT:"AML") AND PUB_YEAR:[2020 TO 2025]',
    source_filter=["MED", "PPR"],
    max_results=500,
    sort="date",
)
print(f"去重后 {len(hits)} 条,预印本 {sum(h['is_preprint'] for h in hits)} 条")

# 2) DOI 反查全文链接
links = cli.get_full_text_links("10.1056/NEJMoa2024850")

# 3) NIH R01 资助的 CAR-T 研究
ft = cli.search_with_grants(query="CAR-T", grant_id="R01CA255621")

# 4) 邻域扩展(RAG)
similar = cli.find_similar_articles("38123456", limit=30)
```

## 14. 进阶参考(references/)

| 文件 | 内容 |
|------|------|
| `references/query-syntax.md` | 完整字段表 + 布尔/通配/邻近搜索 + 5 个常用查询配方 + 排序参数 |
| `references/source-filters.md` | 全部 SRC 来源代码 + 量级 + 预印本子源(bioRxiv/medRxiv/...) + 选择策略 |
| `references/cursormark-pagination.md` | cursorMark 流程伪代码 + 终止条件 + 退避策略 + 5 个常见坑 |

## 参考链接

- Europe PMC RESTful Web Service:https://europepmc.org/RestfulWebService
- 查询语法 Help:https://europepmc.org/Help#SSR
- 字段速查:https://europepmc.org/Help#fieldsearch
- 服务条款:https://europepmc.org/About#TermsOfUse
