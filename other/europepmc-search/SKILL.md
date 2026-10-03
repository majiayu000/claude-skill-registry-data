---
name: europepmc-search
description: Europe PMC RESTful Web Service 多源文献聚合检索原子 skill。一次调用同时召回 PubMed + PMC + AGRICOLA + CABI + 预印本(bioRxiv / medRxiv / ChemRxiv 等)+ 灰色文献,自动按 PMID/PMCID/DOI 三级去重,返回完整元数据(含全文 OA 链接、citations metadata、grants 资助信息)。当任务出现 Europe PMC、多源文献聚合、广召回、RAG 检索、预印本搜索、bioRxiv、medRxiv、全文链接、DOI 检索、跨库去重、灰色文献、资助检索 等触发词时使用。**定位**:广召回 · 多源聚合 · RAG 友好(与 pubmed-eutils 互补——后者做精准官方源、Clinical Queries;本 skill 做"撒网"式广召回)。**不做**:NCBI E-utilities 直检(交给 pubmed-eutils)、临床试验(clinical-trials-v2)、全文 XML 抽取(bioc-fulltext-fetch)、实体识别(pubtator-entity-search)、证据分级(medical-evidence-grading)。
keywords:
  - europe-pmc
  - europepmc
  - 多源文献聚合
  - rag-召回
  - 广召回
  - 预印本
  - biorxiv
  - medrxiv
  - chemrxiv
  - 全文链接
  - doi-检索
  - pmcid
  - 灰色文献
  - grants-检索
  - citations-metadata
  - 跨库去重
license: MIT
---

# europepmc-search

Europe PMC RESTful Web Service 的薄封装。**一次请求 = 多源召回**:PubMed(MED)、PubMed Central(PMC)、AGRICOLA(AGR)、CABI(CBA)、预印本(PPR,涵盖 bioRxiv/medRxiv/ChemRxiv/arXiv 生命科学子集)、专利(PAT)、ETHOS 论文集等。

## 1. 何时使用本 skill

| 场景 | 用本 skill | 不用本 skill |
|------|-----------|------------|
| RAG 知识库构建,需"撒网"式广召回 | ✅ | |
| 同时要 PubMed + 预印本 | ✅ | |
| 只要 PubMed 官方源 + Clinical Queries | | ❌ → pubmed-eutils |
| 拿 DOI 反查全文 OA 链接 | ✅ | |
| 找特定基金(NIH/NSFC/Wellcome)资助的研究 | ✅(`grant_id` 检索) | |
| 抽取已知 PMCID 的全文 XML | | ❌ → bioc-fulltext-fetch |
| 临床试验注册号检索 | | ❌ → clinical-trials-v2 |
| 实体(基因/疾病/化合物)关联 | | ❌ → pubtator-entity-search |

**与 pubmed-eutils 的差异化(必读)**:

- pubmed-eutils:PubMed **单源**、Clinical Queries 过滤、PubDate 精确范围 → 高精准
- europepmc-search:**多源聚合** + 自动去重 + 全文链接 + citations metadata → 高召回
- 推荐编排:RAG 知识库构建用本 skill 广召回 → 拿 PMID 列表喂给 pubmed-eutils 做精准复核

## 2. 前置准备 / 配置加载

Europe PMC RESTful 是**完全开放 API,无需 API key**,但服务条款要求传 `email` 联系方式(礼貌请求,便于 EBI 在大流量异常时联系到使用者)。

**配置加载顺序(优先级从高到低)**:

1. 项目级:`.config/europepmc.local.yaml`(可选,优先于全局)
2. 用户级:`~/.config/europepmc.yaml`
3. 环境变量:`EUROPEPMC_EMAIL`
4. 都没有 → 退化为 `anonymous@example.org` 并打印 ⚠️ 警告(建议用户配置)

**配置文件示例**(`~/.config/europepmc.yaml`):

```yaml
email: your-email@example.com
default_page_size: 100        # 单页条数,1-1000
default_result_type: core     # lite | core | idlist
default_format: json          # json | xml | dc
timeout_seconds: 30
max_retries: 3
```

## 3. API 端点速查

基础 URL:`https://www.ebi.ac.uk/europepmc/webservices/rest/`

| 端点 | 用途 | 关键参数 |
|------|------|---------|
| `search` | 通用检索(本 skill 主力) | `query`, `resultType`, `pageSize`, `cursorMark`, `format`, `sort` |
| `article/{source}/{id}` | 单篇详情 | source∈{MED,PMC,PPR,AGR,CBA,PAT,CTX,ETH,HIR,NBK} |
| `{source}/{id}/fullTextXML` | 全文 XML(仅 OA) | 仅 PMC 子集 |
| `{source}/{id}/references` | 参考文献 | 分页 |
| `{source}/{id}/citations` | 被引列表 | 分页 |
| `{source}/{id}/supplementaryFiles` | 补充材料 | |
| `grant/search` | 资助检索 | `query=GR:"R01..."` |

## 4. 核心检索能力(5 个原子函数)

### 4.1 `search_articles(query, source_filter=None, max_results=200, sort=None)`

通用多源检索,自动分页(cursorMark)拉满到 `max_results`。

- `query`:Europe PMC 查询语法(支持字段限定,见 §5)
- `source_filter`:`["MED","PMC","PPR"]` 限定来源;`None` = 全部
- `sort`:`"date"`(出版日期降序)/ `"cited"`(被引降序)/ `None`(默认相关性)

**返回**:`List[Article]`,每条含 `pmid / pmcid / doi / title / authors / journal / pub_year / abstract / source / is_preprint / preprint_server / has_full_text / oa_status / cited_by_count`。

### 4.2 `get_article_details(identifier)`

单篇完整元数据。`identifier` 自动识别:

- 纯数字 → PMID(查 MED 源)
- `PMC` 前缀 → PMCID(查 PMC 源)
- `10.` 开头 → DOI(用 query=`DOI:"..."` 反查)
- `PPR` 开头 → 预印本 ID(查 PPR 源)

### 4.3 `get_full_text_links(pmid_or_pmcid)`

返回所有可用全文链接,按类型分类:

```python
{
  "oa_xml": "https://.../fullTextXML",      # OA 子集才有
  "oa_pdf": "https://europepmc.org/...pdf",
  "publisher_html": "https://...",
  "subscription": [...],                     # SUBSCRIPTION 类型
  "text_mining": [...],                      # TM 类型(NLM 等)
  "preprint_server": "https://www.biorxiv.org/..."
}
```

### 4.4 `search_with_grants(query, grant_id=None, funder=None)`

资助检索。Europe PMC 有专门的 `GRANT_ID` / `FUNDER` 字段。

```python
# 找 NIH R01-CA123456 资助的所有 paper
search_with_grants(query="cancer", grant_id="R01-CA123456")

# 找 Wellcome Trust 资助的全部 cardiology paper
search_with_grants(query="cardiology", funder="Wellcome Trust")
```

### 4.5 `find_similar_articles(pmid_or_pmcid, limit=20)`

调用 Europe PMC 内置的 "Similar Articles" 算法(基于 MeSH + 文本相似度)。比 PubMed `elink neighbor` 召回略广,适合做 RAG "扩展邻域"。

## 5. 查询语法核心字段

Europe PMC 查询语法兼容 Lucene 风格,字段大写。常用字段:

| 字段 | 含义 | 示例 |
|------|------|------|
| `TITLE` | 标题 | `TITLE:"CAR-T"` |
| `ABSTRACT` | 摘要 | `ABSTRACT:cytokine` |
| `AUTH` | 作者 | `AUTH:"Smith J"` |
| `JOURNAL` | 期刊 | `JOURNAL:"Nature"` |
| `PUB_YEAR` | 年份 | `PUB_YEAR:[2020 TO 2024]` |
| `PUB_TYPE` | 文献类型 | `PUB_TYPE:"Review"` |
| `SRC` | 来源数据库 | `SRC:MED`, `SRC:PPR`, `SRC:PMC` |
| `HAS_FT` | 有全文 | `HAS_FT:Y` |
| `OPEN_ACCESS` | OA | `OPEN_ACCESS:Y` |
| `MESH` | MeSH 主题词 | `MESH:"Hematologic Neoplasms"` |
| `GRANT_ID` | 资助号 | `GRANT_ID:"R01CA12345"` |
| `DOI` | DOI | `DOI:"10.1038/s41586-020-2196-x"` |
| `LANG` | 语种 | `LANG:eng` |

**预印本筛选示例**:`(SRC:PPR) AND (TITLE:"acute myeloid leukemia") AND (PUB_YEAR:2024)`

## 6. 多源去重逻辑(本 skill 强制内置)

同一篇文章常在 MED + PMC + PPR 同时出现。去重规则按以下优先级合并:

1. **第一级:PMID 相同 → 合并**,保留 MED 版本(PubMed 元数据最权威)
2. **第二级:PMCID 相同 → 合并**,保留 PMC 版本(因含全文)
3. **第三级:DOI 相同 → 合并**,优先 MED > PMC > PPR
4. **预印本特殊处理**:若同一 DOI 既有预印本(PPR)又有正式发表(MED),**两条都保留**,但预印本条目标记 `superseded_by_pmid: <发表版 PMID>`,下游(medical-evidence-grading)据此决定是否丢弃预印本。

**返回的合并条目结构**:

```python
{
  "primary_id": "PMID:38123456",
  "all_ids": {"pmid": "38123456", "pmcid": "PMC10987654", "doi": "10.1038/..."},
  "sources": ["MED", "PMC"],          # 出现的所有源
  "is_preprint": False,
  "preprint_server": None,
  "superseded_by_pmid": None,
  ...其他元数据
}
```

## 7. 预印本处理(医学证据特别注意)

预印本 = `source == "PPR"`。本 skill 在每条结果中显式标注:

```python
{
  "source": "PPR",
  "is_preprint": True,
  "preprint_server": "bioRxiv",   # 或 medRxiv / ChemRxiv / Research Square / SSRN ...
  "preprint_doi": "10.1101/2024.03.15.123456",
  "posted_date": "2024-03-15",
  "version": 2                      # 预印本版本号
}
```

**下游约定**:`medical-evidence-grading` skill 看到 `is_preprint=True` 会自动**降权**(GRADE 中作为 "very low" 起点),且若同 DOI 已有正式发表版,直接丢弃预印本。本 skill 自身**不做证据分级**,只如实标注。

## 8. 分页与流量

- Europe PMC 单页上限:`pageSize=1000`
- 分页方式:**强制使用 `cursorMark`**(从 `*` 起,响应里的 `nextCursorMark` 拿来下一页);**不要用 `page=` 偏移分页**(>1000 条时官方明确不保证一致性)
- 流量礼貌:全局并发 ≤ 5,每秒 ≤ 8 请求(自动 sleep)
- 429 / 5xx 退避:指数退避 `2^n` 秒,最多重试 `max_retries`(默认 3)

## 9. 错误处理与边界情况

| 状态 | 处理 |
|------|------|
| HTTP 200 + `hitCount=0` | 返回空列表 + warning"无命中,建议放宽 query" |
| HTTP 400 | 多半是查询语法错误 → 抛 `EuropePMCQueryError`,附原始 `errMsg` |
| HTTP 429 | 指数退避重试 |
| HTTP 5xx | 指数退避重试 |
| `cursorMark` 与上一次相同 | 已到末页,正常终止 |
| 同 query 已超过 `max_results` | 截断并返回 `truncated=True` 标志 |

**致命错误一律抛异常,不静默吞**(遵循全局 `coding-style.md` 错误处理原则)。

## 10. 调用示例

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
print(f"去重后 {len(hits)} 条,其中预印本 {sum(h['is_preprint'] for h in hits)} 条")

# 2) DOI 反查全文链接
links = cli.get_full_text_links("10.1056/NEJMoa2024850")

# 3) 找 NIH R01 资助的 CAR-T 研究
ft = cli.search_with_grants(query="CAR-T", grant_id="R01CA255621")

# 4) 邻域扩展
similar = cli.find_similar_articles("38123456", limit=30)
```

## 11. 与同体系其他 skill 的协作

```
[用户问题]
    │
    ├─→ europepmc-search       ← 本 skill,广召回 200~1000 条
    │       │
    │       └─→ pubmed-eutils  ← 拿 PMID 子集精准复核 + Clinical Queries 过滤
    │               │
    │               └─→ bioc-fulltext-fetch  ← 对 OA PMC 取全文 XML
    │                       │
    │                       └─→ pubtator-entity-search  ← 实体识别
    │                               │
    │                               └─→ medical-evidence-grading  ← GRADE 分级
    │                                      (在此处依据 is_preprint 自动降权)
    │
    └─→ clinical-trials-v2 / aact-bulk-trials  ← 试验注册号另走专线
```

## 12. 输出契约(下游 skill 依赖)

每篇文章返回的标准 schema(本 skill 是契约源):

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
  "mesh_terms": [str],
  "keywords": [str],
  "source": "MED" | "PMC" | "PPR" | "AGR" | "CBA" | "PAT",
  "sources_merged": ["MED","PMC"],   # 去重前出现的所有源
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

下游 skill(medical-evidence-grading / bioc-fulltext-fetch / pubtator-entity-search)按此契约消费,**字段缺失用 `None`,不省略 key**。

## 参考链接

- Europe PMC RESTful Web Service 总览:https://europepmc.org/RestfulWebService
- 查询语法 Help:https://europepmc.org/Help#SSR
- 字段速查:https://europepmc.org/Help#fieldsearch
- 服务条款:https://europepmc.org/About#TermsOfUse
- API 端点:`https://www.ebi.ac.uk/europepmc/webservices/rest/search`
