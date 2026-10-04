---
name: equity-researcher
description: 机构级投研报告生成技能。覆盖中国A股、港股、美股上市公司。输出模式：1）投资速览：3-5页，含公司概览、核心财务指标、估值倍数、投资逻辑与风险因素；2）深度研报：≥25页，含行业分析、产业链图谱、三表模型、DCF估值、情景分析与敏感性测试。触发条件：1）直接请求：分析/看看/研究/调研/介绍一下 + 公司名或股票；2）投资询问：你怎么看/能不能买/值得投吗/帮我看看/扒一扒 + 公司或股票；3）关键词：研报、投资简报、投资速览、公司一页纸、深度研报、深度研究、深度分析、个股分析、一页纸、速览、公司速览、投研报告；4）股票代码：标准格式（如 600519.SH、0700.HK、AAPL、TSLA、BYD）。意图不明确时主动询问输出模式，禁止默认推断。
---

# Equity Research Skill 

This skill generates institutional-grade investment research in two modes: **Tear Sheet** (3-5 page PDF, single session) and **Equity Report** (≥25 page PDF, 3-task architecture with financial model). Both modes share the same analytical philosophy — the difference is depth, scope, and delivery structure.

**Your first job: figure out what the user wants.** Then carry the Core Principles into the next file.

---

## Phase 0.0: Router — Intent Clarification + Output Type Detection

### Step 1: Detect Language

Detect the user's language from their message. Use that language for ALL follow-up questions and the final report.

| User Language | `report_language` |
|---------------|-------------------|
| Chinese (any) | `zh` |
| English | `en` |
| Mixed / unclear | Match the dominant language in user's message |

### Step 2: Classify Intent (3 Tiers)

Not every company analysis request needs a full report. **Before committing resources, determine what the user actually wants.**

| Tier                                           | User Signal Examples                                                                                                                                                   | Action                                                                          |
| ---------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| **Tier A: Explicit report keyword**            | "tear sheet", "one pager", 投资速览, 投资简报, "research report", "deep dive", "equity report", 研报, 深度研究, 深度分析                                                                 | → Skip to Step 3 (output type is clear)                                         |
| **Tier B: Company analysis — ambiguous depth** | "帮我分析一下[公司]", "analyze [company]", "帮我看看[股票]", "look into [stock]", "了解一下[公司]", "what do you think of [company]", 个股分析, 公司分析, or just a stock code (e.g. AAPL, 600519) | → **Ask user** (Step 2a)                                                        |
| **Tier C: Simple question**                    | "XX公司是做什么的", "what's [company]'s market cap", "when is [stock]'s next earnings"                                                                                        | → **Do NOT trigger this skill.** Answer conversationally. No report generation. |

### Step 2a: Clarify Intent (Tier B only)

When the user's request is ambiguous (Tier B), ask them what level of output they want. **Do not assume they want a full report — that wastes their time and tokens.**

Present 3 clear options (in the user's language):

**Chinese example:**
> 我可以用以下几种方式帮你分析 [公司名]:
>
> 1. **投资速览 (Tear Sheet)** — 3-5页专业机构级投资简报，包含估值、催化剂、产业链、情景分析等，适合快速决策参考
> 2. **深度研究报告 (Equity Report)** — ≥25页机构级深度研报，包含完整财务模型、DCF估值、敏感性分析等，适合深入研究
> 3. **简单回答** — 不生成报告，直接用对话回答你的问题，最节省时间
>
> 你想要哪种？

**English example:**
> I can analyze [company] at different levels of depth:
>
> 1. **Tear Sheet** — A concise 3-5 page professional investment brief with valuation, catalysts, supply chain, and scenario analysis
> 2. **Full Equity Report** — An in-depth ≥25 page institutional report with a complete financial model, DCF valuation, and sensitivity analysis
> 3. **Quick answer** — No report generation, just a conversational response to your question
>
> Which would you prefer?

**If user chooses option 3**: Answer their question conversationally. **Do NOT proceed with this skill.** End here.

### Step 3: Determine Output Type

| User Choice / Signal | Output Type | Variable |
|---------------------|-------------|----------|
| Tear Sheet / 投资速览 / option 1 | Tear Sheet | `output_type = TEAR_SHEET` |
| Equity Report / 深度研究 / option 2 | Equity Report | `output_type = EQUITY_REPORT` |
| Explicit "tear sheet", "one pager", 投资速览, 投资简报, 公司一页纸, "quick glance", "investment memo" | Tear Sheet | `output_type = TEAR_SHEET` |
| Explicit "research report", "full report", "deep dive", "equity report", 研报, 深度研究, 深度分析 | Equity Report | `output_type = EQUITY_REPORT` |

**Once output_type is set, record it.** This variable determines which mode-specific file to read next.

---

### Step 3a: Equity Report Valuation Depth Selection (only when `output_type = EQUITY_REPORT`)

When the user wants an equity report, **ask one more question** before starting analysis. The report can be built at two valuation depths — this significantly affects time and complexity.

**Present the choice** (in the user's language):

**Chinese:**
> 深度研报可以按两种估值深度生成：
>
> 1. **完整版（含财务模型）** — 构建完整的三表财务模型（利润表/资产负债表/现金流表）+ DCF绝对估值 + 可比公司估值 + 敏感性分析 + 历史估值带。适合需要深入研究、精确目标价的场景。大约需要 3 步完成。
> 2. **精简版（Level 1 估值）** — 基于可比公司估值（PE/PB/PS 倍数）+ 一致预期 + 情景分析，快速生成专业研报。无复杂 Excel 建模，速度更快。大约需要 2 步完成。
>
> 你选哪种？

**English:**
> The equity report can be built at two valuation depths:
>
> 1. **Full version (with financial model)** — Complete 3-statement financial model (IS/BS/CF) + DCF absolute valuation + comparable companies + sensitivity analysis + historical valuation band. Best for in-depth research with precise target price. Approximately 3 steps.
> 2. **Streamlined version (Level 1 valuation only)** — Comparable company valuation (PE/PB/PS multiples) + consensus expectations + scenario analysis, generating a professional report without complex Excel modeling. Faster turnaround. Approximately 2 steps.
>
> Which would you prefer?

**Record the user's choice**:

| User Choice | Valuation Depth | Variable | Task Architecture |
|-------------|-----------------|----------|-------------------|
| Full version / 完整版 / option 1 | Level 2 (DCF + Comps + Sensitivity) | `valuation_depth = L2` | 3 Tasks: Task 1 → Task 2 (Excel model) → Task 3 |
| Streamlined version / 精简版 / option 2 | Level 1 (Comps + Multiples only) | `valuation_depth = L1` | 2 Tasks: Task 1 → Task 3 (L1 mode, no Task 2 Excel) |

**Key difference**:
- **L2**: Task 2 produces a real Excel model (8+ tabs) with DCF. Task 3 reads numbers from Excel via openpyxl.
- **L1**: Skip Task 2 entirely. Task 1's research document contains all valuation inputs. Task 3 generates valuation tables directly from the research document (no Excel model needed).

**If `output_type = TEAR_SHEET`**: Skip this step entirely. Tear sheets always use Level 1.

---

## ⚠️ Core Principles — CARRY THESE INTO THE NEXT FILE

> **These principles apply to BOTH modes.** Read them now. They are NOT repeated in the mode-specific files. If you skip them, you will produce a bad report.

| Principle | Requirement |
|-----------|-------------|
| **Data Authenticity** | All data must have real sources; strictly prohibit fabrication. No placeholders, no "TBD". |
| **Data Verification** | Critical data cross-verified by 2+ independent sources |
| **Timeliness** | Must use latest financial reports and real-time market data |
| **Recent News Weight** | News within past 7 days affecting marginal expectations must be included |
| **Authoritative Source Weight** | Prioritize official sources and professional financial institutions |
| **Source Attribution** | All data attributed. API data labels original source |
| **Deep Analysis** | Mandatory six-dimension framework; each data point answers "so what" |
| **Bull/Bear Balance** | Both bullish and bearish viewpoints required — no one-sided analysis |
| **Analysis First** | Complete Phase 2-3 analysis, THEN Phase 4 begins layout — never skip ahead |
| **Narrative Consistency** | All modules develop around Phase 3 core narrative |
| **Default Output** | PDF format |
| **File Read Confirmation** | Must confirm required files read before each Phase (see Hard Gate Table in mode file) |

### Data Authenticity Rule

> Prohibit fabricating data, eliminate scaffold/placeholders. See `references/data-sources.md` §Data Missing Handling + quality checklist A6-A8.

---

## Step 4: Route NOW

| Output Type | Valuation Depth | Action |
|-------------|-----------------|--------|
| `TEAR_SHEET` | L1 (fixed) | **Read `SKILL-tearsheet.md` now.** Complete single-session workflow. |
| `EQUITY_REPORT` | L2 | **Read `SKILL-equity-task1.md` now.** Task 1 → Task 2 (Excel model) → Task 3. |
| `EQUITY_REPORT` | L1 | **Read `SKILL-equity-task1.md` now.** Task 1 → Task 3 (no Task 2 Excel). |

**Before starting Task 1**: Tell the user the full flow and step count:

**Chinese (L2):**
> 我将为你生成深度研报（完整版），共 3 步：
> - **第 1 步**：深度研究分析（数据收集 + 六维分析 + 行业研究）→ 输出研究文档
> - **第 2 步**：财务建模与估值（Excel 三表模型 + DCF 估值 + 敏感性分析）
> - **第 3 步**：生成最终 PDF 研报（≥25页）
>
> 现在开始第 1 步。

**English (L2):**
> I'll generate the full equity report in 3 steps:
> - **Step 1**: Deep research analysis (data collection + six-dimension analysis + industry research) → Research Document
> - **Step 2**: Financial modeling & valuation (Excel 3-statement model + DCF + sensitivity)
> - **Step 3**: Generate final PDF report (≥25 pages)
>
> Starting Step 1 now.

**Chinese (L1):**
> 我将为你生成深度研报（精简版），共 2 步：
> - **第 1 步**：深度研究分析（数据收集 + 六维分析 + 可比公司估值）→ 输出研究文档
> - **第 2 步**：生成最终 PDF 研报（≥25页，基于可比公司估值）
>
> 现在开始第 1 步。

**English (L1):**
> I'll generate the streamlined equity report in 2 steps:
> - **Step 1**: Deep research analysis (data collection + six-dimension analysis + comps-based valuation) → Research Document
> - **Step 2**: Generate final PDF report (≥25 pages, comparable-company valuation)
>
> Starting Step 1 now.

**Stop sequential reading here.** The mode-specific file you read next has all execution instructions you need. The REFERENCE SECTION below (Output Type Comparison, Task architecture, File Index, Common Rules) is a look-up resource — consult specific sub-sections when you need to locate a file or confirm a mode detail. Do not read it cover-to-cover.

---
---

# REFERENCE SECTION

> **You do not need to read this section sequentially.** It is reference material for when you need to look up mode details, task architecture, or file locations. The mode-specific files will tell you which files to read and when.

---

## Output Type Comparison

| Dimension           | Tear Sheet                                   | Equity Report                                                  |
| ------------------- | -------------------------------------------- | -------------------------------------------------------------- |
| **Pages**           | 3-5 A4                                       | ≥25 A4 (25-40 pages)                                           |
| **Layout**          | Compact dual-box side-by-side                | Full-width, flexible single/dual-column                        |
| **Module Count**    | 11 fixed modules                             | 21 mandatory modules                                           |
| **Content Style**   | Condensed bullets, max info density          | Fully developed paragraphs with data                           |
| **Valuation Depth** | Level 1 (comparable + multiples + consensus) | Level 2 (L1 + DCF + historical band + sensitivity + synthesis) |
| **CSS**             | `output/tearsheet.css`                       | `output/report.css`                                            |
| **Target Audience** | Quick reference for decision-makers          | In-depth research for institutional investors                  |
| **Phase 4 File**    | `output/tearsheet-layout.md`                 | `output/report-layout.md`                                      |
| **Phase 5 File**    | `output/tearsheet-qa.md`                     | `output/report-qa.md`                                          |

---

## Mode A: Tear Sheet / 投资速览 (Single Session)

A concise 3-5 page PDF produced entirely within one session.

```
Phase 0 → Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → PDF delivered
(Router)   (Data)    (Analysis) (Synthesis) (Layout)  (QA)
```

- Entry file: **`SKILL-tearsheet.md`**
- Output document: Analysis Brief → `references/analysis-brief-template.md`
- Layout: `output/tearsheet-layout.md` → `output/tearsheet.css`
- QA: `output/tearsheet-qa.md`

---

## Mode B: Equity Report / 深度研究 (Multi-Task Architecture)

An in-depth ≥25 page PDF built across **2 or 3 Tasks** depending on valuation depth. Both L1 and L2 share the same Task 1.

### L2 (Full Version — 3 Tasks)

```
Task 1 (SKILL-equity-task1.md):  Phase 0 → Phase 1 → Phase 2 → Phase 3 → Research Document (.md)
                                                                                  ↓
Task 2 (SKILL-task2-model.md):   Financial Model (.xlsx) + Valuation Analysis (.md)
                                                                                  ↓
Task 3 (SKILL-task3-report.md):  Final PDF Report (≥25 pages)
```

### L1 (Streamlined Version — 2 Tasks)

```
Task 1 (SKILL-equity-task1.md):  Phase 0 → Phase 1 → Phase 2 → Phase 3 → Research Document (.md)
                                                                                  ↓
Task 3 (SKILL-task3-report.md):  Final PDF Report (≥25 pages, L1 mode)
```

| Task | Entry File | Input | Output | Acceptance Gate |
|------|-----------|-------|--------|-----------------|
| **Task 1** | `SKILL-equity-task1.md` | User request + stock code | Research Document (≥6,000 words) | 13 completeness + 4 data quality checks |
| **Task 2** (L2 only) | `SKILL-task2-model.md` | Task 1 Research Document | Excel Model (8+ tabs) + Valuation Analysis | 10 model integrity checks |
| **Task 3** | `SKILL-task3-report.md` | Task 1 doc (+ Task 2 Excel + Valuation for L2) | PDF equity report (≥25 pages) | ≥10 number cross-checks vs Excel (L2) / research doc cross-check (L1) |

### Universal Task Rules (Apply to Both L1 and L2)
1. **Never chain Tasks automatically.** Each Task ends with delivery + STOP.
2. **User continues with a single word**: "下一步", "继续", or "continue" — no file uploads needed.
3. **Session context carries files.** The agent maintains the file list internally. When the user says "continue", the agent reads the previously generated files from the session automatically.
4. **Data flows via files, not memory.** Task 2 reads Task 1's document. Task 3 reads Task 2's Excel (L2) or Task 1's document (L1). All financial numbers in Task 3's PDF must tie back to either the Excel model (L2) or the research document (L1).

---

## File Index

**All paths are relative to this skill's root directory.**

### Entry Points
| File | Mode / Task | Purpose |
|------|-------------|---------|
| `SKILL.md` | Router | Determines output type, routes to mode-specific file |
| `SKILL-tearsheet.md` | Tear Sheet | Complete single-session workflow (Phase 0.1 → 5 → PDF) |
| `SKILL-equity-task1.md` | Equity Report Task 1 | Research + Analysis → produces Research Document |
| `SKILL-task2-model.md` | Equity Report Task 2 | Financial Model + Valuation → produces Excel model + Valuation Analysis |
| `SKILL-task3-report.md` | Equity Report Task 3 | Report Generation → produces final PDF equity report |

### Analysis Frameworks (read on-demand per Hard Gate)
| File | Content |
|------|---------|
| `analysis/six-dimension-analysis.md` | 六维分析 complete framework |
| `analysis/investment-logic.md` | Investment logic + thesis table spec |

> Moat classification, earnings-quality checks, management assessment, TAM/SAM/SOM, and competitive deep dive are all defined inline in the two handoff templates (`references/research-document-template.md` for equity reports, `references/analysis-brief-template.md` for tear sheets). No separate per-framework files.

### Deep Research Modules (Equity Report Only — Phase 2.7)
| File | Content |
|------|---------|
| `analysis/revenue-model.md` | Segment-level revenue decomposition, volume × price buildup |
| `analysis/projection-assumptions.md` | Margin bridge, CapEx/WC, assumption sensitivity tags |
| `analysis/scenario-deep-dive.md` | Quantified Bull/Base/Bear with probability weighting |
| `analysis/risk-framework.md` | 8-12 categorized risks with probability × impact scoring |

### Valuation Methods
| File | Level | Content |
|------|-------|---------|
| `valuation/comparable.md` | L1 (both) | Comparable companies + metric selection |
| `valuation/dcf-and-sensitivity.md` | L2 only | DCF methodology + historical valuation band + sensitivity matrix (single consolidated reference) |

### Report Module Specs
| File | Content |
|------|---------|
| `modules/stock-chart.md` | 52-week stock chart + trading data spec |
| `modules/company-overview.md` | Company overview module spec |
| `modules/valuation.md` | Valuation + catalyst calendar spec |
| `modules/industry-chain.md` | Supply chain + upstream/downstream spec |
| `modules/tables.md` | Table styles + data source attribution |
| `modules/equity-report-charts.md` | Chart specs for 5 data charts (revenue, margins, market share, PE band, scenarios) |

### References
| File | Content |
|------|---------|
| `references/data-sources.md` | Data source priority + API overview |
| `references/data-sources-detail.md` | API detailed parameters |
| `references/output-schema.md` | Output interface contract |
| `references/analysis-brief-template.md` | Analysis brief template (tear sheet handoff to Phase 4) |
| `references/research-document-template.md` | Research Document template (Task 1 output) — acceptance criteria + quality gate |
| `references/financial-model-spec.md` | Excel financial model specification — tab structure, line items, formulas, integrity checks |

### Output Layer (Phase 4 layout + Phase 5 QA + CSS)
| File                         | Content                                                    |
| ---------------------------- | ---------------------------------------------------------- |
| `output/tearsheet-layout.md` | Tear Sheet layout, modules, HTML, PDF generation           |
| `output/tearsheet-qa.md`     | Tear Sheet QA (8mm/12mm margins, 3-5 pages)                |
| `output/tearsheet.css`       | Compact dual-box CSS (tear sheet sole source)              |
| `output/report-layout.md`    | Equity Report layout, modules, PDF generation              |
| `output/report-qa.md`        | Equity Report QA (18mm/20mm margins, ≥25 pages)            |
| `output/report.css`          | Full-width research report CSS (equity report sole source) |

### Scripts
| File                               | Content                                                                                                                |
| ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `scripts/stock_chart_generator.py` | 52-week stock chart generator                                                                                          |
| `scripts/report_validator.py`      | Report structure validator                                                                                             |
| `scripts/chart_generator.py`       | Matplotlib chart generator (5 chart types: revenue_segment, margin_trends, market_share, pe_band, scenario_comparison) |
| `scripts/embed_charts.py`          | Chart embedding + chart counter                                                                                        |
