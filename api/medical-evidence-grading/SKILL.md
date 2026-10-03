---
name: medical-evidence-grading
description: 医学证据等级排序与编排层 skill。当用户请求"证据等级 / GRADE / 证据排序 / 医学证据评估 / evidence grading / quality of evidence / 系统评价排序 / 临床证据排序 / 证据金字塔"时触发。本 skill 不直接调用 NCBI/Europe PMC/ClinicalTrials API,而是编排 6 个底层原子 skill(pubmed-eutils / europepmc-search / clinical-trials-v2 / aact-bulk-trials / bioc-fulltext-fetch / pubtator-entity-search)的召回结果,按 ChatGPT 推荐的证据金字塔(指南 > Meta > RCT > Cohort > Case-Control > Case Report)做 GRADE 自动评级,自动剔除 editorial / letter / comment。优先使用 BioMCP MCP server 做 fan-out(genomoncology/biomcp),无 BioMCP 时走自建 slow-path 兜底。
---

# medical-evidence-grading · 医学证据等级排序与编排层

## 一句话定义
对底层 6 个原子 skill 召回的医学文献做"证据金字塔排序",输出带 GRADE A/B/C/D 评级的文献集与汇总报告;同时充当智能调度器,根据问题类型(疗效/诊断/病因/预后/不良反应)自动选择最佳原子 skill 与 PubMed Clinical Queries filter。

---

## 何时调用

**调用本 skill**:
- 用户问"找血液 IFI 最新指南" / "查 venetoclax AML 高质量证据" / "找 CAR-T 不良反应 RCT"
- 已有一批 PMID,需要按证据等级重新排序
- 给临床声明做"反向证据交叉验证"
- 上游 ifi-market-sizing-skill 需要"数据回补"(找指南/RCT 替代低质量来源)
- 下游 evidence-appendix-sync 需要按 GRADE 组织参考文献

**不调用本 skill**(直接调原子 skill):
- 只需要 PubMed 摘要 → `pubmed-eutils`
- 只需要 ClinicalTrials.gov 试验列表 → `clinical-trials-v2`
- 只需要全文段落 → `bioc-fulltext-fetch`
- 只需要实体标注(基因/疾病) → `pubtator-entity-search`
- 全库批量分析 → `aact-bulk-trials`

---

## 与其他 skill 协作矩阵

| 协作方向 | Skill | 用途 | 数据流 |
|---------|-------|------|--------|
| 上游调用方 | `ifi-market-sizing-skill` | 市场规模研究中的"数据回补" | 接收疾病关键词 → 返回分级文献 |
| 上游调用方 | `disease-market-sizing-orchestration` | 市场调研启动阶段的证据搜集 | 接收 PICO 问题 → 返回 Top 20 高等级文献 |
| 下游被调方 1 | `pubmed-eutils` | PubMed 检索 + Clinical Queries filter | 调 esearch/efetch 拿 PMID + publication_type |
| 下游被调方 2 | `europepmc-search` | EuropePMC 检索 + 全文链接 | 拿 PMCID + open access 标记 |
| 下游被调方 3 | `clinical-trials-v2` | ClinicalTrials.gov v2 API | 拿 NCT ID + phase + status |
| 下游被调方 4 | `aact-bulk-trials` | AACT 数据库 PostgreSQL bulk | 大批量试验过滤(n>=500 等) |
| 下游被调方 5 | `bioc-fulltext-fetch` | BioC 全文段落抽取 | 验证摘要中的样本量数字 |
| 下游被调方 6 | `pubtator-entity-search` | PubTator 实体标注 | 给文献打疾病/药物 tag |
| 下游接收方 | `evidence-appendix-sync` | 报告附录 C 同步 | 输出 grade-A/B/C/D 分级清单 |

```
                   用户/上游 skill
                         │
                         ▼
              [medical-evidence-grading]
                  ↙          ↘
        BioMCP fast-path   自建 slow-path
            │                    │
       (单次 fan-out)      并发调 6 个原子 skill
            ↓                    ↓
        统一去重 (PMID > PMCID > DOI)
                    ↓
           publication_type 解析
                    ↓
          GRADE 评级算法 (A/B/C/D/排除)
                    ↓
        evidence-appendix-sync (报告附录)
```

---

## BioMCP fast-path vs 自建 slow-path 双模式

### Fast-path: BioMCP MCP server(优先)
[genomoncology/biomcp](https://github.com/genomoncology/biomcp) 已实现:
- PubMed + Europe PMC + ClinicalTrials.gov + PubTator 一次性 fan-out
- 内置去重(PMID/DOI 归一)
- 暴露为 MCP `article_searcher` / `trial_searcher` / `variant_searcher` 等工具

```python
def detect_biomcp_available() -> bool:
    """
    检测 BioMCP MCP server 是否可用:
    1. 检查 ~/.claude/mcp.json (or ~/.codex/config.toml) 中是否有 'biomcp' 服务器配置
    2. 或检查环境变量 BIOMCP_ENDPOINT
    3. 或检查 `mcp__biomcp__*` 工具是否在已加载工具列表
    4. 都没有 → 返回 False,走 slow-path
    """
    import os, json
    from pathlib import Path

    if os.environ.get("BIOMCP_ENDPOINT"):
        return True

    for cfg in [
        Path.home() / ".claude" / "mcp.json",
        Path.home() / ".claude" / "settings.json",
        Path.home() / ".codex" / "config.toml",
    ]:
        if cfg.exists():
            text = cfg.read_text(encoding="utf-8")
            if "biomcp" in text.lower():
                return True
    return False
```

### Slow-path: 自建 fan-out(兜底)
当 BioMCP 不可用,本 skill 自己:
1. 并发调 `pubmed-eutils` + `europepmc-search` + `clinical-trials-v2`(asyncio.gather)
2. 用 PMID > PMCID > DOI 三段优先级去重(创建 `evidence_id` 哈希)
3. 调 `pubmed-eutils` efetch 拿 publication_type
4. 调 `bioc-fulltext-fetch` 抽样本量(只对疑似 RCT/Cohort)
5. 应用 GRADE 算法

**性能对比**:
| 模式 | 100 条文献延迟 | API 调用数 | 缓存命中后 |
|------|---------------|-----------|-----------|
| Fast-path (BioMCP) | ~3-5s | 1 | <500ms |
| Slow-path (自建) | ~15-25s | 6-10 | <500ms |

---

## GRADE 自动评级规则表

```
输入: publication_type(MeSH 标签数组) + abstract + 样本量(可选)

┌─────────────────────────────────────────────────────────────────┐
│  Grade A (最高质量,优先纳入)                                    │
│  ├─ "Practice Guideline" / "Guideline"                          │
│  ├─ "Consensus Development Conference"                          │
│  ├─ "Meta-Analysis"                                             │
│  ├─ "Systematic Review"                                         │
│  └─ "Randomized Controlled Trial" AND n >= 1000                 │
├─────────────────────────────────────────────────────────────────┤
│  Grade B (高质量)                                               │
│  ├─ "Randomized Controlled Trial" AND n < 1000                  │
│  ├─ "Clinical Trial, Phase III"                                 │
│  ├─ "Multicenter Study" AND prospective                         │
│  └─ "Cohort Studies" AND n >= 500                               │
├─────────────────────────────────────────────────────────────────┤
│  Grade C (中等质量)                                             │
│  ├─ "Cohort Studies" AND n < 500                                │
│  ├─ "Case-Control Studies"                                      │
│  ├─ "Cross-Sectional Studies"                                   │
│  ├─ "Clinical Trial, Phase II"                                  │
│  └─ "Observational Study"                                       │
├─────────────────────────────────────────────────────────────────┤
│  Grade D (低质量,谨慎引用)                                      │
│  ├─ "Case Reports"                                              │
│  ├─ "Review" (非 systematic)                                    │
│  ├─ "Narrative Review"                                          │
│  ├─ "Clinical Trial, Phase I"                                   │
│  └─ Preprint (medRxiv / bioRxiv) → Grade D-                     │
├─────────────────────────────────────────────────────────────────┤
│  EXCLUDED (自动剔除)                                            │
│  ├─ "Editorial"                                                 │
│  ├─ "Letter"                                                    │
│  ├─ "Comment"                                                   │
│  ├─ "News"                                                      │
│  ├─ "Biography"                                                 │
│  └─ "Retracted Publication" (除非用户明确要求)                  │
└─────────────────────────────────────────────────────────────────┘
```

### 降权信号(Grade 降一级)
- 单中心研究(non-multicenter)
- 样本量 < 100 且非罕见病
- 期刊影响因子 < 2.0(可选,需 NLM Catalog API)
- 发表 > 10 年前且无更新指南
- 无利益冲突声明

### 升权信号(Grade 升一级,极少用)
- 大型登记研究 n > 10000
- NEJM / Lancet / JAMA / BMJ 顶刊一级证据

---

## Clinical Queries 推荐策略表

PubMed 提供 Clinical Queries filter,本 skill 根据"问题类型"自动选择:

| 问题类型 | Clinical Queries filter | 等价 PubMed query | 优先 grade |
|---------|------------------------|-------------------|-----------|
| 疗效 (Therapy) | `therapy/narrow` | `randomized controlled trial[pt]` | A-B |
| 诊断 (Diagnosis) | `diagnosis/narrow` | `sensitivity[ti] OR specificity[ti]` | A-C |
| 病因 (Etiology) | `etiology/narrow` | `cohort studies[mh] OR risk[ti]` | B-C |
| 预后 (Prognosis) | `prognosis/narrow` | `prognosis[mh] OR survival[ti]` | B-C |
| 不良反应 (Harm) | `etiology/broad` | `adverse effects[sh]` | A-C |
| 临床预测 (Prediction) | `clinical_prediction_guides/narrow` | `decision rule[tw]` | A-B |
| 指南 (Guidelines) | n/a | `practice guideline[pt]` | A only |
| 系统综述 (SR) | n/a | `systematic[sb]` | A only |

`recommend_search_strategy(question_type)` 函数返回上表对应行的 query 模板。

---

## 5 核心函数签名

```python
# ============== 1. 主入口:综合证据搜索 ==============
def evidence_search(
    query: str,
    target_grade: str = "all",  # 'guideline_only' | 'rct_or_above' | 'all'
    max_results: int = 200,
    include_preprints: bool = False,
    include_trials: bool = True,
    date_range: str = "10years",  # 'all' | '5years' | '10years' | '2020:2025'
    use_biomcp_if_available: bool = True,
) -> dict:
    """
    返回:
    {
        "total": 156,
        "by_grade": {"A": 12, "B": 34, "C": 67, "D": 43, "excluded": 21},
        "fast_path_used": True,  # BioMCP 是否命中
        "cache_hit": False,
        "elapsed_seconds": 4.2,
        "results": [
            {
                "evidence_id": "PMID:38234567",
                "pmid": "38234567",
                "pmcid": "PMC10891234",
                "doi": "10.1056/NEJMoa2024xxx",
                "title": "...",
                "authors": [...],
                "journal": "NEJM",
                "year": 2024,
                "publication_types": ["Randomized Controlled Trial", "Multicenter Study"],
                "sample_size": 1450,
                "is_preprint": False,
                "grade": "A",
                "grade_rationale": "RCT n>=1000",
                "abstract": "...",
                "source": "pubmed",  # 或 'europepmc' / 'clinicaltrials' / 'biomcp'
            },
            ...
        ]
    }
    """

# ============== 2. 给现有 PMID 列表打分 ==============
def grade_pmid_list(
    pmid_list: list[str],
    fetch_fulltext_for_sample_size: bool = False,
) -> list[dict]:
    """
    输入: ['38234567', '37123456', ...]
    输出: 每条带 grade / grade_rationale 的字典
    用 efetch 拿 publication_type;若 fetch_fulltext_for_sample_size=True,
    对疑似 RCT/Cohort 调 bioc-fulltext-fetch 验证 n。
    """

# ============== 3. 推荐检索策略 ==============
def recommend_search_strategy(
    question_type: str,  # 'therapy' | 'diagnosis' | 'etiology' | 'prognosis' | 'harm' | 'guideline' | 'sr'
    user_query: str = "",
) -> dict:
    """
    返回:
    {
        "clinical_queries_filter": "therapy/narrow",
        "pubmed_query_template": "({user_query}) AND randomized controlled trial[pt]",
        "europepmc_query_template": "({user_query}) AND PUB_TYPE:\"Randomized Controlled Trial\"",
        "expected_grade_distribution": {"A": "30%", "B": "50%", "C": "20%"},
        "recommended_skill": "pubmed-eutils",  # 可能是 clinical-trials-v2 等
        "tips": ["建议加 hasabstract filter", "排除 case report"],
    }
    """

# ============== 4. 反向证据交叉验证 ==============
def cross_validate_evidence(
    claim: str,  # 例: "Posaconazole 预防 IFI 比 fluconazole 更有效"
    top_k: int = 10,
    min_grade: str = "B",
) -> dict:
    """
    用 NLP 拆解 claim → PICO → 反向搜索高等级证据。
    返回:
    {
        "claim": "...",
        "pico": {"P": "high-risk neutropenia", "I": "posaconazole", "C": "fluconazole", "O": "IFI incidence"},
        "supporting": [...top_k 文献,grade>=min_grade...],
        "contradicting": [...],
        "verdict": "supported" | "contradicted" | "mixed" | "insufficient",
        "confidence": 0.87,
    }
    """

# ============== 5. 证据汇总报告 ==============
def evidence_summary(
    graded_list: list[dict],
    output_format: str = "markdown",  # 'markdown' | 'html' | 'json'
    output_path: str | None = None,  # 若提供,写入 evidence/summary.md
) -> str:
    """
    生成:
    - 各等级数量统计表
    - Top 5 grade-A 文献的摘要表
    - 关键发现摘要(用 sequential-thinking 提炼)
    - 引用建议(优先 grade-A,补充 grade-B)
    - 缺口提示(若 grade-A 数量<3,提示扩展检索)
    """
```

---

## 输出格式示例

### 分级文献集 (JSON)
见 `evidence_search` 返回结构。

### 汇总报告 (Markdown)
```markdown
# 证据汇总报告 · venetoclax AML 一线治疗

**生成时间**: 2026-04-25  **总计**: 156 篇  **检索路径**: BioMCP fast-path

## 等级分布
| Grade | 数量 | 占比 |
|-------|------|------|
| A (指南/Meta/大型 RCT) | 12 | 7.7% |
| B (RCT/Phase 3/大型队列) | 34 | 21.8% |
| C (中小型队列/对照) | 67 | 42.9% |
| D (病例/综述/Preprint) | 43 | 27.6% |
| 已剔除 (社论/letter) | 21 | -- |

## Top 5 Grade-A 证据
1. **DiNardo et al. NEJM 2020** · PMID 32786187 · VIALE-A 三期 RCT (n=431)
2. **NCCN Guidelines AML v3.2024** · 临床实践指南
3. **Konopleva et al. Cancer Discov 2016 Meta-analysis** · PMID 27520294
...

## 关键发现
- Grade-A 证据一致支持 venetoclax+azacitidine 优于 azacitidine 单药 (OS HR 0.66)
- 老年/不耐受强化化疗人群证据最充足
- 缺口: 中国人群头对头 RCT 数据稀缺(仅 3 篇 grade-B)

## 引用建议
- 主结论引用 ≥3 篇 grade-A
- 补充安全性数据可用 grade-B 大型队列
- 不建议引用 grade-D(除非"首次报道某不良反应")
```

---

## 缓存层

```python
# SQLite 本地缓存,7 天有效期
CACHE_DB = Path.home() / ".claude" / "skills" / "medical-evidence-grading" / "cache.sqlite"

# 表结构
CREATE TABLE evidence_cache (
    query_hash TEXT PRIMARY KEY,    -- SHA256(query + target_grade + date_range)
    query_text TEXT,
    result_json TEXT,
    created_at TIMESTAMP,
    expires_at TIMESTAMP,           -- created_at + 7 days
    fast_path_used BOOLEAN,
    total_results INTEGER
);

CREATE TABLE pmid_grade_cache (
    pmid TEXT PRIMARY KEY,
    publication_types TEXT,         -- JSON array
    sample_size INTEGER,            -- 可空
    grade TEXT,                     -- A/B/C/D/excluded
    grade_rationale TEXT,
    cached_at TIMESTAMP             -- 30 天有效(publication_type 不变)
);
```

**缓存策略**:
- `evidence_search` 完整结果缓存 7 天
- 单 PMID 的 grade 缓存 30 天(publication_type 几乎不变)
- 命中加速 10-50x,完全避免重复 API 调用

---

## 失败模式速查

| 症状 | 可能原因 | 处理方式 |
|------|---------|---------|
| BioMCP 检测到但调用失败 | MCP server 未启动 | 静默回退 slow-path,日志告警 |
| Slow-path 调用 pubmed-eutils 超时 | NCBI 限流 (3 req/s) | 加 jitter 重试 3 次,仍失败用 europepmc-search 替代 |
| `publication_type` 字段为空 | 文献过新还未 MeSH 索引 | 用 abstract 关键词启发式判定(`randomized` / `meta-analysis`),grade 加 `_inferred` 后缀 |
| 样本量提取失败 | 全文不可访问 | 跳过样本量校验,Grade 按 publication_type 默认值 |
| 同一研究多 PMID(预印本+正式版) | medRxiv → 期刊 | 优先保留期刊版,预印本标记 `superseded_by` |
| 中文期刊文献缺失 | NCBI 不索引部分中文期刊 | 提示用户用 CNKI / 万方补充,本 skill 不覆盖 |
| `evidence_search(target_grade='guideline_only')` 返回 0 | 该领域确无指南 | 自动 fallback 到 `rct_or_above` 并提示用户 |
| 缓存损坏 | SQLite 文件错误 | 自动重建,丢弃旧缓存 |

---

## evidence/ 文件夹组织规范

下游 `evidence-appendix-sync` 期望本 skill 产出如下结构:

```
evidence/
├── grade-A/
│   ├── PMID-32786187_DiNardo-NEJM-2020.json     # 完整元数据
│   ├── PMID-32786187_DiNardo-NEJM-2020_abs.txt  # 摘要全文
│   └── ...
├── grade-B/
├── grade-C/
├── grade-D/
├── excluded/
├── _summary.md                                   # 汇总报告
├── _index.csv                                    # 全部文献索引(便于附录 C 引用)
└── _query_log.jsonl                              # 检索日志(可复现)
```

每条 `*.json` 文件结构:
```json
{
  "evidence_id": "PMID:32786187",
  "grade": "A",
  "grade_rationale": "Phase 3 multicenter RCT, n=431, NEJM",
  "citation_apa": "DiNardo CD, et al. (2020). NEJM, 383(7), 617-629.",
  "citation_chinese": "DiNardo 等,2020,NEJM",
  "metadata": {...},
  "abstract": "...",
  "fetched_at": "2026-04-25T14:32:11Z",
  "source_chain": ["biomcp", "pubmed_efetch"]
}
```

---

## 跨疾病移植清单

本 skill 与具体疾病无关,移植到新疾病(如肺癌、糖尿病)只需:

- [ ] 确认底层 6 个原子 skill 都已安装(`/skills` 列表查看)
- [ ] 调整 `recommend_search_strategy` 中的 question_type 映射(领域可能有专属 filter)
- [ ] 若涉及罕见病,把 GRADE 算法中的"n>=500/1000"阈值降低(建议 100/200)
- [ ] 若涉及外科器械,补充 `Comparative Effectiveness Research` 类型识别
- [ ] 中文医学领域加 CNKI / 万方补充检索(本 skill 不直接支持,建议外挂)

---

## 跨平台兼容

| 平台 | 兼容性 | 说明 |
|------|-------|------|
| Claude Code | 原生支持 | SKILL.md 自动加载,Skill 工具直接调用 |
| Codex (CLI) | 兼容 | 复制到 `$CODEX_HOME/skills/medical-evidence-grading/SKILL.md`,通过 `skill-installer` |
| Gemini CLI | 兼容 | 作为 prompt template 使用,函数签名需手工实现 |
| Cursor / Continue | 部分 | 提取 GRADE 规则表作为 system prompt |

**关键不变量**(确保跨平台一致):
- 函数签名稳定(5 个核心函数不重命名)
- GRADE 规则表用 Markdown 表格表达(任何 LLM 都能解析)
- 缓存路径用 `~/.claude/skills/medical-evidence-grading/cache.sqlite`(各平台自动适配)
- BioMCP 检测逻辑同时支持 `~/.claude/mcp.json` / `~/.codex/config.toml` / 环境变量三路

---

## 版本与依赖

- **版本**: 1.0.0 (P0.2 阶段首发)
- **依赖原子 skill**: pubmed-eutils ≥1.0, europepmc-search ≥1.0, clinical-trials-v2 ≥2.0, aact-bulk-trials ≥1.0, bioc-fulltext-fetch ≥1.0, pubtator-entity-search ≥1.0
- **可选 MCP**: biomcp (genomoncology/biomcp,推荐安装以启用 fast-path)
- **Python 依赖**: requests / httpx, sqlite3 (标准库), asyncio (标准库)
- **更新日志**:
  - v1.0.0 (2026-04-25): 初始版本,5 核心函数 + BioMCP 双模式 + SQLite 缓存

---

## 调用示例

### 示例 1: 找血液 IFI 最新指南
```python
result = evidence_search(
    query="invasive fungal infection prophylaxis hematology",
    target_grade="guideline_only",
    max_results=20,
    date_range="5years",
)
# 返回 ECIL / IDSA / NCCN 等指南
```

### 示例 2: 给已有 PMID 列表打分
```python
graded = grade_pmid_list(
    pmid_list=["32786187", "37123456", "38234567"],
    fetch_fulltext_for_sample_size=True,
)
# 返回 [{pmid, grade, rationale}, ...]
```

### 示例 3: 反向验证临床声明
```python
verdict = cross_validate_evidence(
    claim="Posaconazole 预防 IFI 比 fluconazole 更有效",
    top_k=10,
    min_grade="B",
)
# 返回 supporting / contradicting 文献 + 总体判断
```

---

**End of SKILL.md**
