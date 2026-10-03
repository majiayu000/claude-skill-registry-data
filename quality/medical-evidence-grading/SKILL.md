---
name: medical-evidence-grading
description: 医学证据等级排序与编排层 skill - evidence grading orchestrator. 当用户请求"证据等级 / GRADE / 证据排序 / 医学证据评估 / 系统评价排序 / 临床证据排序 / 证据金字塔 / 给 PMID 打分 / Practice Guideline 优先 / Cochrane 优先 / 反向证据交叉验证 / evidence grading / quality of evidence / evidence pyramid / GRADE assessment / Cochrane review ranking / clinical evidence ranking"时,**调用本 skill 进行医学证据自动分级,自动选择最佳信息源**。本 skill 是编排层(L2)·不直接打 NCBI/Europe PMC/ClinicalTrials API,而是编排 6 个底层原子 skill(pubmed-eutils / europepmc-search / clinical-trials-v2 / aact-bulk-trials / bioc-fulltext-fetch / pubtator-entity-search)的召回结果,按证据金字塔(指南 > Meta > RCT > Cohort > Case-Control > Case Report)做 GRADE A/B/C/D 自动评级,自动剔除 editorial/letter/comment。优先使用 BioMCP MCP server 做 fan-out(genomoncology/biomcp);无 BioMCP 时走自建 slow-path 兜底。跨平台无锁(Claude Code / Codex / Gemini CLI)。
---

# medical-evidence-grading · 医学证据等级排序与编排层(L2)

## 一句话定义

对底层 6 个原子 skill 召回的医学文献做"证据金字塔排序",输出带 GRADE A/B/C/D 评级的文献集与汇总报告;同时充当智能调度器,根据问题类型(疗效/诊断/病因/预后/不良反应/预测/指南/SR)自动选择最佳原子 skill 与 PubMed Clinical Queries filter。

---

## Iron Law(不可违反)

> **GRADE 评级前必须调用 `pubmed-eutils.efetch_pubmed()` 拿真实 publication_type。不可仅凭 title/abstract 关键词推断。**

理由:title 含"randomized"未必是 RCT(可能是综述讨论 RCT);只有 NLM MeSH 索引员人工标注的 publication_type 才是权威依据。仅当 efetch 返回为空(发表 < 6 个月新文献)才允许启发式推断,且必须给 grade 加 `_inferred` 后缀。

完整规则见 `references/grade-rules.md`。

---

## 何时调用(Auto-trigger)

**调用本 skill (✅)**:
- "评估这个临床声明的证据强度" → ✅ `cross_validate_evidence(claim=...)`
- "找血液 IFI 最新指南级证据" → ✅ `evidence_search(query=..., target_grade='guideline_only')`
- "对比这些 PMID 的 GRADE 等级" → ✅ `grade_pmid_list(pmid_list=[...])`
- "我要给附录 C 重新分级" → ✅ `grade_pmid_list` + `evidence_summary`
- "venetoclax AML 高质量 RCT" → ✅ `evidence_search(target_grade='rct_or_above')`

**不调用本 skill (❌,直接调原子 skill)**:
- "检索 PubMed" → ❌ 直接调 `pubmed-eutils`
- "找 NCT 试验" → ❌ 直接调 `clinical-trials-v2`
- "拿全文段落" → ❌ 直接调 `bioc-fulltext-fetch`
- "全库批量分析" → ❌ 直接调 `aact-bulk-trials`

---

## 与其他 skill 协作矩阵(关键 · 编排核心)

| 协作方向 | Skill | 调用的具体函数 | 用途 |
|---------|-------|--------------|------|
| 上游调用方 | `ifi-market-sizing-skill` | (调本 skill) | 市场规模研究的"数据回补" |
| 上游调用方 | `disease-market-sizing-orchestration` | (调本 skill) | 调研启动阶段的高等级证据搜集 |
| 下游被调 1 | `pubmed-eutils` | `.esearch_pubmed()` / `.efetch_pubmed()` / `.pubmed_clinical_queries()` | 拿 PMID + publication_type |
| 下游被调 2 | `europepmc-search` | `.search_articles()` / `.find_similar_articles()` | EuropePMC + open-access 链接 |
| 下游被调 3 | `clinical-trials-v2` | `.search_studies()` | NCT + phase + enrollment |
| 下游被调 4 | `aact-bulk-trials` | `.bulk_disease_landscape()` | 全库历史试验(罕见病/纵向) |
| 下游被调 5 | `bioc-fulltext-fetch` | `.to_rag_chunks()` | 抽样本量(只对疑似 RCT/Cohort) |
| 下游被调 6 | `pubtator-entity-search` | `.search_by_relation()` | 给文献打疾病/药物 entity tag |
| 下游接收方 | `evidence-appendix-sync` | (接受本 skill 输出) | 报告附录 C 同步 |

```
              用户 / 上游 skill (ifi-market-sizing-skill, disease-market-sizing-orchestration)
                              │
                              ▼
                  [medical-evidence-grading]
                       ↙             ↘
            BioMCP fast-path      自建 slow-path
                  │                       │
            (单次 fan-out)        并发调 6 原子 skill
                  ↓                       ↓
                统一去重 (PMID > PMCID > DOI)
                              ↓
                publication_type 解析 (efetch · Iron Law)
                              ↓
                GRADE 评级 (A/B/C/D/excluded · 见 grade-rules.md)
                              ↓
                  evidence-appendix-sync (报告附录 C)
```

---

## BioMCP fast-path vs 自建 slow-path 双模式

### Fast-path: BioMCP MCP server (优先)
[genomoncology/biomcp](https://github.com/genomoncology/biomcp) 一次性 fan-out PubMed + EuropePMC + ClinicalTrials + PubTator。

### Slow-path: 自建 fan-out (兜底)
当 BioMCP 不可用,并发调 `pubmed-eutils.esearch_pubmed()` + `europepmc-search.search_articles()` + `clinical-trials-v2.search_studies()`,然后 `pubmed-eutils.efetch_pubmed()` 拿 publication_type,可选调 `bioc-fulltext-fetch.to_rag_chunks()` 抽样本量。

**完整检测/配置/兜底逻辑见 `references/biomcp-integration.md`。**

性能对比:

| 模式 | 100 条文献延迟 | API 调用数 | 缓存命中后 |
|------|---------------|-----------|-----------|
| Fast-path (BioMCP) | ~3-5s | 1 | <500ms |
| Slow-path (自建) | ~15-25s | 6-10 | <500ms |

---

## 5 核心函数签名(跨平台稳定)

```python
# ============== 1. 主入口:综合证据搜索 ==============
def evidence_search(
    query: str,
    target_grade: str = "all",          # 'guideline_only' | 'rct_or_above' | 'all'
    max_results: int = 200,
    include_preprints: bool = False,
    include_trials: bool = True,
    date_range: str = "10years",        # 'all' | '5years' | '10years' | '2020:2025'
    rare_disease_mode: bool = False,    # 罕见病阈值放宽,见 grade-rules.md
    use_biomcp_if_available: bool = True,
) -> dict:
    """
    返回 {total, by_grade, fast_path_used, cache_hit, elapsed_seconds, results: [{evidence_id, pmid, pmcid, doi, title, authors, journal, year, publication_types, sample_size, is_preprint, grade, grade_rationale, abstract, source}]}
    """

# ============== 2. 给现有 PMID 列表打分 ==============
def grade_pmid_list(
    pmid_list: list[str],
    fetch_fulltext_for_sample_size: bool = False,
) -> list[dict]:
    """
    输入 ['38234567', ...] → 输出每条带 grade / grade_rationale 的字典。
    内部:批量 pubmed-eutils.efetch_pubmed() → 解析 publication_type → 应用 grade-rules.md。
    fetch_fulltext_for_sample_size=True 时,对疑似 RCT/Cohort 调 bioc-fulltext-fetch.to_rag_chunks() 抽 n。
    """

# ============== 3. 推荐检索策略 ==============
def recommend_search_strategy(
    question_type: str,       # 'therapy' | 'diagnosis' | 'etiology' | 'prognosis' | 'harm' | 'prediction' | 'guideline' | 'sr'
    user_query: str = "",
) -> dict:
    """
    返回 {clinical_queries_filter, pubmed_query_template, europepmc_query_template,
          expected_grade_distribution, recommended_skill, tips[]}.
    完整 8 类映射见 references/clinical-queries-mapping.md。
    """

# ============== 4. 反向证据交叉验证 ==============
def cross_validate_evidence(
    claim: str,               # 例: "Posaconazole 预防 IFI 比 fluconazole 更有效"
    top_k: int = 10,
    min_grade: str = "B",
) -> dict:
    """
    NLP 拆解 claim → PICO → 反向搜索高等级证据。
    返回 {claim, pico, supporting[], contradicting[], verdict, confidence}.
    verdict ∈ {supported, contradicted, mixed, insufficient}.
    """

# ============== 5. 证据汇总报告 ==============
def evidence_summary(
    graded_list: list[dict],
    output_format: str = "markdown",   # 'markdown' | 'html' | 'json'
    output_path: str | None = None,    # 提供则写 evidence/_summary.md
) -> str:
    """
    生成等级分布表 + Top 5 grade-A 摘要表 + 关键发现 + 引用建议 + 缺口提示。
    """
```

---

## Clinical Queries 8 类问题速览

| question_type | 优先 grade | 主调 skill |
|--------------|----------|-----------|
| therapy | A-B | pubmed-eutils.pubmed_clinical_queries(scope='therapy/narrow') |
| diagnosis | A-C | pubmed-eutils + europepmc-search |
| etiology | B-C | pubmed-eutils |
| prognosis | B-C | pubmed-eutils |
| harm | A-C | pubmed-eutils + clinical-trials-v2 (AE 表) |
| prediction | A-B | pubmed-eutils |
| guideline | A only | pubmed-eutils.pubmed_clinical_queries(scope='guidelines') |
| sr | A only | pubmed-eutils + europepmc-search |

完整查询模板与罕见病调整见 `references/clinical-queries-mapping.md`。

---

## 失败模式速查 (10 条)

| 症状 | 可能原因 | 处理方式 |
|------|---------|---------|
| BioMCP 检测到但调用失败 | MCP server 配置存在但未启动/版本不兼容 | 静默回退 slow-path,日志告警,不阻塞 |
| BioMCP 故障 fall-back 至 slow-path 但 NCBI 也限流 | 双路连续失败 | 加 jitter 退避,3 次后切 europepmc-search 单源,grade 标 `_partial` |
| GRADE 自动评级 publication_type 缺失 | 文献 < 6 个月未 MeSH 索引 | 启发式推断(见 grade-rules.md),grade 加 `_inferred` 后缀,警告用户人工复核 |
| 样本量提取失败(efetch 摘要不含 n) | 全文不可访问 / 摘要写法不规范 | 跳过 n 校验,grade 按 publication_type 默认值,不应用 n 阈值降权 |
| 重复 PMID 跨原子 skill 未去重 | BioMCP 已去重但回退到 slow-path 未去重 | 强制 `evidence_id = "PMID:" + pmid` 三段优先级(PMID > PMCID > DOI)再去重 |
| 证据矛盾(同一 claim 高等级证据正反皆有) | 真实存在的临床争议 | `cross_validate_evidence` 返回 `verdict='mixed'`,supporting 与 contradicting 并列展示,不强行下结论 |
| 缓存命中但 GRADE 规则更新过 | grade-rules.md 升级未 bump 版本 | `grade_rule_version` 字段不匹配视为 miss,自动重算并刷新缓存 |
| evidence/ 文件夹组织规范冲突 | 下游 evidence-appendix-sync 期望 grade-A/B/C/D 子目录 | 严格按 `grade-A/PMID-XXX_AuthorYear.json` 命名,变动需双方同步升级 |
| 同一研究多 PMID(预印本+正式版) | medRxiv → 期刊 | 优先保留期刊版,预印本标记 `superseded_by` |
| 中文期刊文献缺失 | NCBI 不索引部分中文期刊 | 提示用户用 CNKI / 万方补充,本 skill 不覆盖中文数据库 |

完整缓存策略见 `references/cache-schema.md`。

---

## evidence/ 文件夹组织规范

下游 `evidence-appendix-sync` 期望本 skill 产出:

```
evidence/
├── grade-A/
│   ├── PMID-32786187_DiNardo-NEJM-2020.json
│   └── PMID-32786187_DiNardo-NEJM-2020_abs.txt
├── grade-B/  grade-C/  grade-D/  excluded/
├── _summary.md          # evidence_summary() 产出
├── _index.csv           # 全部文献索引(便于附录 C 引用)
└── _query_log.jsonl     # 检索日志(可复现)
```

每条 `*.json` 含 `{evidence_id, grade, grade_rationale, citation_apa, citation_chinese, metadata, abstract, fetched_at, source_chain}`。

---

## 跨疾病移植清单

本 skill 与具体疾病无关,移植到肺癌/糖尿病等只需:
- [ ] 确认底层 6 原子 skill 已安装(`/skills` 列表查看)
- [ ] 涉及罕见病时 `evidence_search(rare_disease_mode=True)` 自动放宽阈值(见 grade-rules.md)
- [ ] 涉及外科器械时,补充 `Comparative Effectiveness Research` 类型识别
- [ ] 中文医学领域加 CNKI / 万方补充检索(本 skill 不覆盖,建议外挂)

---

## 跨平台兼容(无锁)

| 平台 | 兼容性 | 说明 |
|------|-------|------|
| Claude Code | 原生 | SKILL.md 自动加载,Skill 工具直接调用 |
| Codex (CLI) | 兼容 | 复制到 `$CODEX_HOME/skills/medical-evidence-grading/`,通过 skill-installer |
| Gemini CLI | 兼容 | 作为 prompt template 使用,函数签名需手工实现 |
| Cursor / Continue | 部分 | 提取 GRADE 规则表(见 grade-rules.md)作为 system prompt |

**关键不变量**(确保跨平台一致):
- 函数签名稳定(5 个核心函数不重命名)
- GRADE 规则用 Markdown 表格表达(任何 LLM 可解析)
- 缓存路径 `~/.claude/skills/medical-evidence-grading/cache.sqlite` (`Path.home()` 自动适配)
- BioMCP 检测三路:`~/.claude/mcp.json` / `~/.codex/config.toml` / `BIOMCP_ENDPOINT` 环境变量

---

## References (Progressive Disclosure)

主文件保持精简;深度细节按需加载:

- `references/grade-rules.md` — GRADE 评级完整规则表 + 降权升权信号 + 启发式推断 + 跨疾病阈值
- `references/clinical-queries-mapping.md` — Clinical Queries 8 类问题映射 + 多类型并行 + 罕见病调整 + 中国本土补充
- `references/biomcp-integration.md` — BioMCP fast-path 检测三路 + fall-back 触发条件 + slow-path 自建 fan-out + 跨平台配置
- `references/cache-schema.md` — SQLite cache 表结构 + TTL 策略 + 命中检测 + 维护命令

---

## 调用示例

```python
# 示例 1: 找血液 IFI 最新指南
result = evidence_search(
    query="invasive fungal infection prophylaxis hematology",
    target_grade="guideline_only",
    max_results=20,
    date_range="5years",
)
# 返回 ECIL / IDSA / NCCN 等指南

# 示例 2: 给已有 PMID 列表打分
graded = grade_pmid_list(
    pmid_list=["32786187", "37123456", "38234567"],
    fetch_fulltext_for_sample_size=True,
)

# 示例 3: 反向验证临床声明
verdict = cross_validate_evidence(
    claim="Posaconazole 预防 IFI 比 fluconazole 更有效",
    top_k=10,
    min_grade="B",
)
```

---

## 版本与依赖

- **版本**: 1.1.0 (P0.2 阶段 · references 拆分版)
- **GRADE 规则版本**: v1.0.0 (改动需 bump,见 cache-schema.md)
- **依赖原子 skill**: pubmed-eutils ≥1.0, europepmc-search ≥1.0, clinical-trials-v2 ≥2.0, aact-bulk-trials ≥1.0, bioc-fulltext-fetch ≥1.0, pubtator-entity-search ≥1.0
- **可选 MCP**: biomcp (genomoncology/biomcp,推荐安装以启用 fast-path)
- **更新日志**:
  - v1.1.0 (2026-04-25): references/ 拆分(grade-rules / clinical-queries-mapping / biomcp-integration / cache-schema),主文件 500 → ~370 行,新增 Iron Law / Auto-trigger 5 prompt / 函数级原子 skill 引用
  - v1.0.0 (2026-04-25): 初始版本
