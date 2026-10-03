---
name: pubtator-entity-search
description: NLM PubTator3 实体级关系挖掘原子 skill — 在 PubMed 文献里检索"疾病-药物-基因-化学品-突变-物种-细胞系"的标注与关系三元组。当用户问"BTK 与肺曲霉病的关联文献"、"BTK 抑制剂(MeSH D000077180)在哪些研究被讨论"、"标注这些 PMID 中提到的所有疾病/药物/基因实体"、"ibrutinib 的 MeSH/DrugBank ID"、"voriconazole 与 CYP2C19 药物-基因相互作用"、"BRAF V600E 突变 / rs113488022 检索"、"实体共现 / co-mention / 关系挖掘 / 实体规范化 / NER / annotation / entity normalization / disease-gene association / drug-gene interaction / chemical-disease relation" 时使用。无需 API key,跨平台稳定。**实体级 + 关系级**定位 — 不做综合文献检索(走 pubmed-eutils / europepmc-search)、不做全文段落抽取(走 bioc-fulltext-fetch)、不做证据等级排序(走 medical-evidence-grading)。
keywords:
  - pubtator
  - pubtator3
  - biomedical-entity
  - NER
  - annotation
  - entity-relation
  - entity-normalization
  - co-mention
  - 实体标注
  - 疾病基因关联
  - 药物-基因
  - 化学品-疾病
  - 突变检索
  - mesh
  - dbsnp
  - drugbank
license: MIT
---

# PubTator3 Entity & Relation Search

封装 NLM PubTator3 RESTful API,做**实体级标注 + 关系挖掘**。聚焦"疾病 — 药物 — 基因 — 化学品 — 突变 — 物种 — 细胞系"的联动检索。

---

## 1. 何时使用本技能

**适合 (✅ 自动触发)**:

| 用户问题 | 路由 |
|---|---|
| "找 BTK 与肺曲霉病的关联文献" | ✅ 本技能 (`find_co_mentions`) |
| "BTK 抑制剂 (MeSH D000077180) 在哪些研究被讨论" | ✅ 本技能 (`search_by_entity`) |
| "标注这些 PMID 中提到的所有疾病/药物/基因实体" | ✅ 本技能 (`annotate_pmid`) |
| "ibrutinib 在文献中映射到哪个 MeSH/DrugBank" | ✅ 本技能 (`entity_normalize`) |
| "voriconazole 与 CYP2C19 相互作用" | ✅ 本技能 (`search_by_relation`) |
| "BRAF V600E / rs113488022 突变文献" | ✅ 本技能 (`search_by_entity` concept=variant) |

**不适合 (❌ 路由到其他 skill)**:

| 用户问题 | 路由 |
|---|---|
| "查 PubMed 上近 5 年所有 X 的 RCT" | ❌ → `pubmed-eutils` + Clinical Queries |
| "MeSH 树 / 出版类型 / PubDate 综合检索" | ❌ → `pubmed-eutils` |
| "Europe PMC 综合检索 + 引文" | ❌ → `europepmc-search` |
| "全文段落抽取 / BioC 全文" | ❌ → `bioc-fulltext-fetch` |
| "证据等级 / GRADE / 推荐级别" | ❌ → `medical-evidence-grading` |
| "正在招募的 X 临床试验" | ❌ → `clinical-trials-v2` |

---

## 2. API 概览 (无需 Key)

Base URL: `https://www.ncbi.nlm.nih.gov/research/pubtator3-api/`

PubTator3 是 NLM 开放服务,**无需 API key**,但请遵守速率限制 (≤ 5 req/s,失败时指数退避)。

| 端点 | 用途 |
|------|------|
| `GET /search/?text=<query>` | 自由文本 / 实体检索文献 |
| `GET /publications/export/biocjson?pmids=<csv>` | 拉取 PMID 的实体标注 BioC-JSON |
| `GET /entity/autocomplete/?query=<text>&concept=<type>` | 实体规范化 (text → ID) |
| `GET /relations?e1=<id>&e2=<id>` | 关系/共现挖掘 |

文档: <https://www.ncbi.nlm.nih.gov/research/pubtator3-api/>

---

## 3. 5 个原子函数 (跨平台签名)

每个签名命名稳定,可在 Python / TS / Go / Rust 任意语言实现。

### 3.1 `search_by_entity(entity_text, entity_type=None, max_results=50) -> list[PMID]`

```
GET /search/?text=@<TYPE>_<ID>  或  ?text=<free text>
```
示例: `text=@DISEASE_MESH:D055744` → 返回 `{pmids:[...], score:[...]}`。

### 3.2 `search_by_relation(entity1_id, relation_type, entity2_id) -> list[Relation]`

```
GET /relations?e1=<id1>&e2=<id2>&type=<relation>
```
关系类型见 `references/relation-types.md`。返回涉及关系的 PMID + score + 句级证据。

### 3.3 `annotate_pmid(pmid_list) -> list[Annotation]`

```
GET /publications/export/biocjson?pmids=12345,67890&full=false
```
解析 BioC-JSON `documents[].passages[].annotations[]`。一次最多 100 PMID,超出自动分批。

### 3.4 `entity_normalize(free_text, concept=None) -> list[EntityCandidate]`

```
GET /entity/autocomplete/?query=BTK%20inhibitor&concept=chemical
```
返回 `[{name, id, type, score}, ...]`,例如 `BTK inhibitor → MESH:D000077180`。

### 3.5 `find_co_mentions(entity1_id, entity2_id, top_n=20, recent_years=None) -> list[CoMention]`

组合 `search` + `annotate` 验证两实体在同一文献被标注。可按近 N 年过滤。

---

## 4. 实体类型 & 关系类型 (Reference)

主文档不嵌入完整定义,按需展开:

- **实体类型** (7 种 + identifier 格式 + 查询前缀): 见 [`references/entity-types.md`](references/entity-types.md)
  - `gene` / `disease` / `chemical` / `variant` / `mutation` / `species` / `cellline`
- **关系类型** (8 种 + 主-宾语典型组合 + score 阈值): 见 [`references/relation-types.md`](references/relation-types.md)
  - `treat` / `cause` / `inhibit` / `interact_with` / `regulate` / `associate` / `compare` / `co-occur`

---

## 5. 输出格式 (标准 schema)

每条标注:

```python
{
    "pmid": "12345",
    "entity_text": "BTK",
    "entity_type": "Gene",          # Gene/Disease/Chemical/Variant/Species/CellLine
    "identifier": "695",            # NCBI Gene / MESH / rs# / Taxonomy / CVCL
    "section": "Title",             # Title / Abstract
    "offset": 23,                   # passage 内字符级起点
    "length": 3,
    "confidence": 0.95,             # 若 API 返回
}
```

每条关系:

```python
{
    "pmid": "12345",
    "subject":   {"text": "ibrutinib", "type": "Chemical", "id": "MESH:D000077594"},
    "predicate": "inhibits",
    "object":    {"text": "BTK",       "type": "Gene",     "id": "695"},
    "score": 0.92,
    "evidence_sentence": "Ibrutinib irreversibly inhibits BTK ...",
    "section": "Abstract",
}
```

---

## 6. 典型工作流

### 用例 A — 疾病 + 药物联动

> "找近 5 年讨论 BTK 抑制剂与侵袭性肺曲霉病关系的文献"

1. `entity_normalize("BTK inhibitor", "chemical")` → `MESH:D000077180`
2. `entity_normalize("invasive pulmonary aspergillosis", "disease")` → `MESH:D055744`
3. `find_co_mentions(e1, e2, top_n=30, recent_years=5)`
4. 对返回 PMID 用 `annotate_pmid()` 提取上下文 → 三元组表
5. 需要证据等级 → 输出喂给 `medical-evidence-grading`

### 用例 B — 批量标注

> "把这 20 个 PMID 里所有疾病/药物/基因列出来"

1. `annotate_pmid([...20 PMIDs...])`
2. 按 `entity_type ∈ {Gene, Disease, Chemical}` 过滤 → 去重计数 → 频次表

### 用例 C — 实体规范化

> "ibrutinib 的 MeSH 是什么?"

1. `entity_normalize("ibrutinib", "chemical")` → 取首条 hit 的 `id`

### 用例 D — 上下游链接

> 本技能产出 PMID 集合后,可直接喂给:
- `pubmed-eutils` → 拿元数据 / 出版类型
- `bioc-fulltext-fetch` → 拿全文段落
- `medical-evidence-grading` → 实体级证据排序

---

## 7. 失败模式 (≥ 5 条)

| # | 失败模式 | 检测 | 处理 |
|---|---|---|---|
| 1 | **实体未识别** — PubTator 不支持的术语 / 拼写 / 罕见同义词 | `autocomplete` 返回空 | 退化用 `pubmed-eutils` 自由文本检索;同时建议规范同义词或换 concept |
| 2 | **实体规范化多义词** — `BTK` 既是基因 (NCBI 695) 也是缩写 / 化学品 | `autocomplete` 返回多 hit,score 接近 | 让用户确认 concept;必要时用 ID 而非 symbol |
| 3 | **关系置信度低 (`score < 0.5`)** — 假阳性高 | `/relations` 返回 score | **过滤丢弃**,不进入证据表;0.5–0.8 区间需人工核句 |
| 4 | **共现假阳性** — 两实体出现在同一文献但语义无关 (review / 综述堆砌名词) | 句级 evidence 不在同一句 / passage | 至少要求两实体在同一 sentence 才算 co-mention;否则降权 |
| 5 | **API rate limit (429)** — 过快请求被限流 | HTTP 429 / 503 | 退避 2 → 4 → 8s,最多 5 次;批处理时控制 ≤ 5 RPS |
| 6 | **PMID 暂未被 PubTator 标注** — 太新 / 待索引 | BioC-JSON 缺 `annotations` | 在结果里标 `status=pending_annotation`,跳过并记录;可走 `bioc-fulltext-fetch` 拿全文再 LLM 标 |
| 7 | **PMID 不存在** | BioC-JSON 文档为空 | 返回 `status=not_found` |
| 8 | **方向反转 / 否定语** — 句子含 "not", "fail to", "no association" | `evidence_sentence` 正则或 LLM 判否定 | 标记 `polarity=negative`,从证据表剔除或单列 |

不要静默吞错;每个失败请求记录 `{pmid, endpoint, status_code, message}`。

---

## 8. 实现要点

- 用 `requests` + `tenacity` (Python) / `axios-retry` (TS) 做指数退避
- `concept` 参数小写: `gene | disease | chemical | variant | species | cellline`
- BioC-JSON 路径: `documents[*].passages[*].annotations[*].infons.{type,identifier}` + `text` + `locations[0].offset/length`
- 一次 `annotate_pmid` 上限 100 PMID (超过自动分批 + 并发上限 ≤ 3)
- 自由文本 + 实体混合查询: `text=ibrutinib AND @DISEASE_MESH:D055744`
- 跨平台: 函数签名只用 string / list / dict,不依赖任何特定运行时

---

## 9. 安全 / 合规

- 公共 NLM API,无 PHI
- **不要把用户上传的非公开文本发给 PubTator3** — 仅用公开 PMID
- 输出注明 `Source: NLM PubTator3, retrieved <date>`
- PubTator3 标注属机器抽取,**置信度 < 0.8 的关系应人工核对**

---

## 10. 与其他 skill 的协同 (显式互补,无重叠)

| 技能 | 边界 | 协同方向 |
|---|---|---|
| **`pubmed-eutils`** | E-utilities — MeSH 树 / 出版类型 / PubDate 综合检索 | **互补**: 本技能给 PMID,`pubmed-eutils` 拿元数据 |
| **`europepmc-search`** | Europe PMC 广召回 + 引文 + 多源融合 | **互补**: 召回扩展;不重叠 |
| **`bioc-fulltext-fetch`** | BioC PMC 全文 XML/JSON 段落抽取 | **互补**: PubTator3 标题/摘要,BioC 全文;PubTator3 不替代全文 |
| **`medical-evidence-grading`** | GRADE / 证据等级 / 推荐级别 (上层) | **上层**: 本技能输出实体三元组,grading 给等级 |
| **`clinical-trials-v2`** | ClinicalTrials.gov 试验注册 | **不相关**: 走 NCT |

本技能输出的 PMID 集合 / 三元组可直接喂给上述任意下游。

---

## 11. 快速 cheatsheet

```text
# 1) 文本 → 实体 ID
GET /entity/autocomplete/?query=ibrutinib&concept=chemical

# 2) 实体检索文献
GET /search/?text=@CHEMICAL_MESH:D000077594

# 3) 关系挖掘
GET /relations?e1=MESH:D000077594&e2=695&type=inhibit

# 4) PMID 批量标注
GET /publications/export/biocjson?pmids=12345,67890

# 5) 共现: search 各拿 PMID 集合 → 求交 → annotate 验证 → 按 score/年份排序
```

实体类型查询前缀:
`@GENE_<NCBIid>` · `@DISEASE_MESH:<Did>` · `@CHEMICAL_MESH:<Did>` · `@VARIANT_<rs#>` · `@SPECIES_<TaxId>` · `@CELLLINE_<CVCLid>`

---

**版本**: v1.1 · **维护**: 跟随 NLM PubTator3 API 文档更新 (关注 endpoints 变更与新增 concept)。
