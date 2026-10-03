---
name: pubtator-entity-search
description: NLM PubTator3 实体级关系挖掘 — 检索"疾病-药物-基因-化学品-突变"在生物医学文献中的标注与关系。当用户问"哪些研究讨论了 BTK 抑制剂与肺曲霉病"、"基因 X 与疾病 Y 的关联"、"药物-基因相互作用"、"找含某突变的文献"、"PubTator / 实体标注 / NER / annotation / biomedical entity / 疾病基因关联 / 药物-基因 / 化学品-疾病 / 突变检索"时使用。无需 API key。**实体级 · 关系挖掘**定位 — 不做文献综合检索(用 pubmed-eutils / europepmc-search)、不做全文(用 BioC)、不做试验(用 ct-v2)。
keywords:
  - pubtator
  - pubtator3
  - biomedical-entity
  - NER
  - annotation
  - entity-relation
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

封装 NLM PubTator3 RESTful API,用于在 PubMed 文献中做**实体级标注 + 关系挖掘**。
聚焦"疾病 - 药物 - 基因 - 化学品 - 突变 - 物种"的联动检索,适合"实体 X 与实体 Y 在文献中怎样被讨论"这类问题。

---

## 1. 何时使用本技能

**适合**:
- "哪些文献提到了 BTK 抑制剂用于侵袭性肺曲霉病" — 实体 + 关系
- "基因 EGFR 在非小细胞肺癌中的相关研究" — 共现 / 关联
- "找出讨论 voriconazole 与 CYP2C19 相互作用的文献" — 药物-基因
- "把这一组 PMID 里的疾病/药物/基因都标出来" — 标注提取
- "ibrutinib 在文献中映射到哪个 MeSH/DrugBank ID" — 实体规范化

**不适合(用其他技能)**:
- 用 MeSH 树/出版类型/PubDate 做文献检索 → `pubmed-eutils` + Clinical Queries
- 拿全文 XML/段落 → `BioC` (BioC PubMed/PMC)
- 临床试验注册信息 → `ct-v2` (ClinicalTrials.gov)
- 综合性自然语言检索 → `europepmc-search`

---

## 2. API 概览(无需 Key)

Base URL: `https://www.ncbi.nlm.nih.gov/research/pubtator3-api/`

PubTator3 是 NLM 开放服务,**不需要 API key**,但请遵守速率限制(建议 ≤ 3 req/s,失败时退避)。

核心端点:

| 端点 | 用途 |
|------|------|
| `GET /search/?text=<query>` | 自由文本/实体检索文献 |
| `GET /publications/export/biocjson?pmids=<csv>` | 拉取 PMID 的实体标注 BioC-JSON |
| `GET /entity/autocomplete/?query=<text>&concept=<type>` | 实体规范化(text → ID) |
| `GET /relations?e1=<id>&e2=<id>` | 关系/共现挖掘 |

文档: https://www.ncbi.nlm.nih.gov/research/pubtator3-api/

---

## 3. 核心能力(5 个函数)

### 3.1 `search_by_entity(entity_text, entity_type=None, max_results=50)`
检索包含某实体的 PubMed 文献。

```
GET /search/?text=@<TYPE>_<ID> 或 ?text=<free text>
```
示例:`text=@DISEASE_MESH:D055744` → 侵袭性曲霉病。
返回 `{pmids:[...], score:[...]}`。

### 3.2 `search_by_relation(entity1_id, relation_type, entity2_id)`
检索表达"实体1 — 关系 — 实体2"的文献。

```
GET /relations?e1=<id1>&e2=<id2>&type=<relation>
```
返回涉及该关系的 PMID 列表 + 句级证据片段(若有)。

### 3.3 `annotate_pmid(pmid_list)`
给定 PMID 数组,返回标题 + 摘要内的全部实体标注。

```
GET /publications/export/biocjson?pmids=12345,67890&full=false
```
解析 BioC-JSON `documents[].passages[].annotations[]`。

### 3.4 `entity_normalize(free_text, concept=None)`
自由文本 → 标准实体 ID。

```
GET /entity/autocomplete/?query=BTK%20inhibitor&concept=chemical
```
返回 `[{name, id, type, score}, ...]`,例如 `BTK inhibitor → MeSH:D000077180`。

### 3.5 `find_co_mentions(entity1_id, entity2_id, top_n=20, recent_years=None)`
共现分析 — 找两实体共同出现最多的文献,可按近 N 年过滤。
内部组合 `search` + `annotate` 验证两实体确实在同一文献被标注。

---

## 4. 实体类型 Reference

| 类型 (concept) | 标识体系 | 示例 ID | 说明 |
|---|---|---|---|
| `Gene` | NCBI Gene | `695` (BTK) | 蛋白编码基因 |
| `Disease` | MeSH / OMIM | `MESH:D055744` (Invasive Pulmonary Aspergillosis) | 疾病 / 综合征 |
| `Chemical` | MeSH / DrugBank | `MESH:D000077594` (ibrutinib) | 化学品 / 药物 |
| `Variant` | dbSNP / ClinVar / tmVar | `rs113488022` | 多态位点 / 变异 |
| `Mutation` | tmVar | `p.V600E` | 蛋白/核酸级具体突变 |
| `Species` | NCBI Taxonomy | `9606` (Homo sapiens) | 物种 |
| `CellLine` | Cellosaurus | `CVCL_0030` (HeLa) | 细胞系 |

> Variant 与 Mutation 在 PubTator3 多被合并为 `Variant`;查询时统一用 `concept=variant`。

---

## 5. 关系类型 Reference

PubTator3 关系标签(在 `/relations` 端点的 `type` 参数):

| 关系 | 含义 | 典型主语 → 宾语 |
|---|---|---|
| `treat` / `treats` | 治疗 | Chemical → Disease |
| `cause` / `causes` | 致病 / 引发 | Chemical/Variant → Disease |
| `interact_with` | 相互作用 | Gene ↔ Gene / Chemical ↔ Gene |
| `associate` / `associated_with` | 关联(弱因果) | Gene ↔ Disease / Variant ↔ Disease |
| `regulate` / `regulates` | 调控(上下游) | Gene → Gene |
| `inhibit` / `inhibits` | 抑制 | Chemical → Gene/Protein |
| `co-occur` | 共现(无方向) | 任意 ↔ 任意 |

> 当不确定关系语义时,优先使用 `co-occur` 做共现挖掘,再人工/二次核对方向。

---

## 6. 输出格式(标准 schema)

每条标注统一输出:

```python
{
    "pmid": "12345",
    "entity_text": "BTK",
    "entity_type": "Gene",
    "identifier": "695",            # NCBI Gene ID / MeSH / dbSNP / ...
    "section": "Title",             # Title / Abstract
    "offset": 23,                   # 字符级起点(passage 内)
    "length": 3,
    "confidence": 0.95,             # PubTator3 置信度(若 API 返回)
}
```

关系输出:

```python
{
    "pmid": "12345",
    "subject": {"text": "ibrutinib", "type": "Chemical", "id": "MESH:D000077594"},
    "predicate": "inhibits",
    "object":  {"text": "BTK",       "type": "Gene",     "id": "695"},
    "evidence_sentence": "Ibrutinib irreversibly inhibits BTK ...",
    "section": "Abstract",
}
```

---

## 7. 典型工作流

### 用例 A:疾病 + 药物联动
> "找近 5 年讨论 BTK 抑制剂与侵袭性肺曲霉病关系的文献"

1. `entity_normalize("BTK inhibitor", "chemical")` → `MESH:D000077180`
2. `entity_normalize("invasive pulmonary aspergillosis", "disease")` → `MESH:D055744`
3. `find_co_mentions(e1, e2, top_n=30, recent_years=5)`
4. 对返回 PMID 用 `annotate_pmid()` 提取上下文实体 → 输出三元组表

### 用例 B:批量标注
> "把这 20 个 PMID 里所有疾病/药物/基因列出来"

1. `annotate_pmid([...20 PMIDs...])`
2. 按 `entity_type ∈ {Gene, Disease, Chemical}` 过滤 → 去重计数 → 输出频次表

### 用例 C:实体规范化
> "ibrutinib 的 MeSH 是什么?DrugBank 呢?"

1. `entity_normalize("ibrutinib", "chemical")`
2. 取首条 hit 的 `id` 字段(MeSH);若需 DrugBank 走 cross-ref(PubTator3 主返回 MeSH)

---

## 8. 实现要点

- 使用 `requests` + `tenacity` 做指数退避(429 / 5xx)
- `concept` 参数小写:`gene | disease | chemical | variant | species | cellline`
- BioC-JSON 路径:`documents[*].passages[*].annotations[*].infons.{type,identifier}` + `text` + `locations[0].offset/length`
- 一次 `annotate_pmid` 上限 100 PMID(超过自动分批)
- 自由文本 + 实体混合查询语法:`text=ibrutinib AND @DISEASE_MESH:D055744`

---

## 9. 错误处理

| 错误 | 处理 |
|---|---|
| 429 Too Many Requests | 退避 2s → 4s → 8s,最多 5 次 |
| 5xx | 同上退避 |
| 实体规范化无 hit | 返回空列表 + 建议:换同义词 / 改 concept |
| BioC-JSON 缺 annotations | 该 PMID 暂未被 PubTator 标注,跳过并记录 |
| PMID 不存在 | 在响应中按 PMID 标 `status=not_found` |

不要静默吞错;每个失败请求记录 `{pmid, endpoint, status_code, message}`。

---

## 10. 安全 / 合规

- 公共 NLM API,无 PHI
- 不要把用户上传的非公开文本发给 PubTator3 — 仅检索公开 PMID
- 输出注明 "Source: NLM PubTator3, retrieved <date>"
- PubTator3 标注属机器抽取,**置信度 < 0.8 的关系应人工核对**

---

## 11. 与其他 skill 的协同

| 用户问题 | 路由 |
|---|---|
| "哪些研究讨论 X 与 Y 的关系" / "实体级关联" | **本技能** |
| "近 5 年所有 X 的 RCT" / "MeSH + 出版类型筛选" | `pubmed-eutils` + Clinical Queries |
| "PMID 12345 全文写了什么" | `BioC-PubMed/PMC` |
| "正在招募的 X 临床试验" | `ct-v2` (ClinicalTrials.gov) |
| "Europe PMC 综合检索 + 引文" | `europepmc-search` |

本技能输出的 PMID 集合可直接喂给 `pubmed-eutils` / `BioC` 做下游展开。

---

## 12. 快速 cheatsheet

```text
# 1) 文本 → 实体 ID
GET /entity/autocomplete/?query=ibrutinib&concept=chemical

# 2) 实体检索文献
GET /search/?text=@CHEMICAL_MESH:D000077594

# 3) 关系挖掘
GET /relations?e1=MESH:D000077594&e2=695&type=inhibits

# 4) PMID 批量标注
GET /publications/export/biocjson?pmids=12345,67890

# 5) 共现:先 search,各拿 PMID 集合 → 求交 → 按引用/年份排序
```

实体类型缩写(查询前缀):`@GENE_`、`@DISEASE_MESH:`、`@CHEMICAL_MESH:`、`@VARIANT_`、`@SPECIES_`、`@CELLLINE_`。

---

**版本**: v1.0  ·  **维护**: 跟随 NLM PubTator3 API 文档更新(关注 endpoints 变更与新增 concept)。
