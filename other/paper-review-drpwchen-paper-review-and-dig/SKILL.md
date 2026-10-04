---
name: paper-review
description: >
  Deep single-paper academic analysis — journal credibility, author profiling, reference verification,
  citation impact, and critical appraisal. Like a teaching hospital journal club report. Use this skill
  whenever the user wants to deeply review, evaluate, or dissect a single academic paper, prepare a
  journal club presentation, verify a paper's references, check an author's track record, or do any
  thorough paper-level analysis. Also trigger when the user says "review this paper", "深度評讀",
  "journal club", "論文評讀", "幫我看這篇", or provides a DOI/PMID asking for analysis.
  NOT for multi-paper systematic reviews or standalone evidence grading.
---

# Paper Review — 單篇論文深度評讀

## Overview

This skill performs a 360-degree deep dive into a single academic paper, covering journal credibility,
author backgrounds, publication history, historical context, reference verification, critical appraisal,
and citation impact analysis. The output is a structured Obsidian note in `${vault.papers_dir}` plus a
daily note entry under `${vault.daily_section}`.

Reviews should be clinically grounded, teachable (journal-club ready), and honest about what the
evidence can and cannot support. Tone, language, specialty framing, and external-validity checks are
driven by `${persona}` (see Configuration).

## Configuration (read FIRST, every run)

Before Phase 0, read **`config.yaml`** in this skill's directory (copy `config.example.yaml` →
`config.yaml` on first setup). It defines the values this document references as `${section.key}`:

- `${vault.papers_dir}`, `${vault.medicine_dir}`, `${vault.inbox_note}`, `${vault.daily_section}`
- `${fulltext.*}` (inbox, Zotero, Elsevier, SFX resolver, institution) — consumed via
  `fulltext-acquisition.md`
- `${secrets.backend}` — how bundled scripts read API keys
- `${persona}` — language, specialty, audience, locale, reimbursement system. **This is user-authored**;
  it sets whether output is 繁體中文/English, which clinical lens, and whether coverage lookups run.

Wherever this SKILL writes `${...}`, substitute the config value. A blank/placeholder value means
"skip that route". The bundled scripts (`grade_judge.py`, `argdown_lint.py`) need no config.

## Input

Accepts any of:
- **DOI** (e.g., `10.1097/PHM.0000000000002700`)
- **PMID** (e.g., `39056432`)
- **Paper title** (partial or full)
- **PDF file path** (local file)
- **Pasted content** (abstract or full text in the conversation)

## Effort tiers (pick before starting — token budget)

- **Quick** (daily-note `[x]` checkbox): Phases 1 + Critical Appraisal + `白話導讀` only. No
  author/journal deep-dive, no citation analysis, no reference verification. ~1 model, cheap.
- **Deep** (`/paper-review`): all 7 phases. Token-heavy (many MCP + WebFetch calls). Before starting,
  offer the user a **focused deep**: "全跑 (Phases 1-7) 還是只跑關鍵幾關 (2 期刊/6 引用查核/appraisal)?"
  Respect a "skip" after any phase. Don't silently run all 7 if the user wanted a spot-check.
- Either tier: reuse `journal_cache.json` / `author_cache.json` before any WebSearch.

## Delegation (deep tier — added 2026-07-07 per dispatch-protocol)

The main context keeps what is intelligence-bound: reading the paper itself ONCE, the Critical
Appraisal, GRADE domain ratings, and final synthesis. Everything that is fan-out lookup work gets
delegated so raw search dumps never enter main context:

- **Phase 3 (author profiling)** → ONE subagent per key author (parallel, same message,
  `model: "haiku"`): given name + affiliation, run the S2 author tools + WebSearch, return a
  ≤6-bullet profile (h-index, top papers, COI/retraction flags). Main context never sees raw
  search results.
- **Phase 6 Steps 2-3 (reference verification)** → batch the selected references into 1-2
  subagents (`model: "sonnet"`), each returns verification-table rows only (the exact columns of
  Step 4). Give each agent the claim text + citation; NOT your appraisal reasoning.
- **Phase 7 (citation categorization + PubPeer/social sweep)** → one subagent (`model: "sonnet"`)
  returns the 🟢🔴🔵🟡 categorized list + any PubPeer/news hits with links.
- Every delegation prompt includes: "If you cannot meet the criteria, say FAILED and list what you
  tried — do not return a best guess as verified." Failed lookups are reported as gaps, never
  silently dropped.
- Quick tier: no delegation (overhead exceeds benefit).

## Phase 0: Full Text Acquisition

Follow the shared protocol: **`~/.claude/skills/paper-review/fulltext-acquisition.md`**
(check order, OA auto-fetch rule, Elsevier TDM, institutional SFX resolver, Zotero bookkeeping + citekey).

**Review-specific policy**: if NO full text is obtainable from any route, proceed with
abstract-only review — mark "⚠️ Abstract-level review" at the top of Deep Review, and every
section limited by this notes「abstract 未報告，需全文確認」. (Contrast: /paper-digest hard-stops.)
For figures/tables when working from a Zotero PDF: point the user to the PDF in Zotero.

## Phase 1: Paper Identification & Metadata

Use **Semantic Scholar MCP as primary** (more reliable), PubMed MCP as supplement:

**Semantic Scholar MCP (primary):**
- `search_papers` or `get_paper_details` → citation count, fields of study, TL;DR, DOI
- Semantic Scholar's paper ID is needed for later phases (citations, references, authors)

**PubMed MCP (supplement — may be flaky, session errors common):**
- `search_articles` → find PMID if not already known
- `get_article_metadata` → MeSH terms, publication dates, abstract
- If PubMed MCP fails (session terminated / invalid content), fall back to WebSearch
  `site:pubmed.ncbi.nlm.nih.gov "{title}"` to get PMID

Extract and confirm: title, all authors (with affiliations), journal, DOI, PMID, study type,
received/accepted/published dates, keywords/MeSH terms.

**After this phase, show the user a brief summary** — confirm this is the right paper before
proceeding with the deep dive.

## Phase 2: Journal Credibility

Assess the journal's trustworthiness and standing:

- **Impact metrics**: WebSearch for current Impact Factor, SJR ranking, CiteScore
- **Indexing**: Confirm presence in PubMed/MEDLINE, Scopus, Web of Science
- **Peer review process**: Single-blind, double-blind, or open review
- **Reputation in field**: Where does this journal sit in the specialty hierarchy?
  (e.g., for PM&R: AJPMR > Archives PMR > J Rehabil Med > smaller specialty journals)
- **Red flags**: WebSearch `"{journal name}" retraction watch` and `"{journal name}" predatory`
  to check for controversy, inclusion in Beall's list, or unusual retraction rates
- **Retraction/correction check (this paper) — SINGLE authoritative check, done once here**:
  `mcp__zotero__scite_check_retractions` on the DOI catches retractions, expressions of concern,
  and corrections in one call. This is the canonical paper-level integrity check; Phase 4 reuses
  this result instead of re-searching. Only if scite is unavailable, fall back to one WebSearch
  `"{DOI}" retraction OR "expression of concern" OR erratum`.

Output: 2-4 bullet points summarizing journal credibility with specific metrics.

## Phase 3: Author Profiling

Focus on **first author** and **corresponding author** (often the senior PI). For other authors,
brief mentions only.

**Delegate this phase** (see §Delegation) — one parallel `model: "haiku"` agent per key author.
Each agent runs, and returns only a ≤6-bullet profile from:
- `search_authors` + `get_author_details` → h-index, total citations, paper count
- `get_author_top_papers` → their most-cited works (shows research trajectory)
- WebSearch → institutional affiliation, lab/research group, recent grants
- Check for COI: look at the paper's COI declaration section + WebSearch for industry ties
- Red flags: WebSearch `"{author name}" retraction` to check history
- Any tool failure → the agent reports "FAILED: <tool> <what was tried>" for that bullet, not a guess

Output: a brief profile for each key author — credentials, expertise match to this paper's topic,
and any concerns.

## Phase 4: Publication Timeline

From metadata already gathered:
- Received → Revised → Accepted → Published dates
- Calculate review duration (received to accepted). Flag if unusually fast (<30 days for a
  non-letter/editorial) or slow (>12 months)
- Reuse the Phase 2 scite retraction/correction result — do NOT re-search. Note here only if a
  correction/erratum post-dates publication (relevant to the timeline).
- Check if there's a related commentary or editorial in the same journal issue

Output: timeline with any notable observations.

## Phase 5: Historical Context & Background

This phase explains *why this paper exists* — the research landscape that motivated it:

- Read the paper's Introduction carefully for the narrative arc
- Use Semantic Scholar `get_related_papers` and `get_paper_references` to map the intellectual lineage
- Identify:
  - The specific research gap or controversy this paper addresses
  - 3-5 key prior works that directly led to this study
  - The field's trajectory — is this an emerging area, a mature debate, or a paradigm shift?
- For each key prior work, get a one-line summary via `get_paper_details`

Output: a narrative (in bullet form) tracing the intellectual path from prior work to this paper.

## Phase 6: Reference Verification (Key Claims Only)

This is the most distinctive part of this review. The goal is to check whether the paper
accurately represents its sources — a common and often undetected problem in the literature.

### Step 1: Identify key claims
Read through the paper and identify 5-10 claims that are central to the paper's argument.
These are typically in the Introduction (establishing the rationale) and Discussion (comparing results).

If the paper has >20 references, **ask the user** which claims or sections to focus on.
Don't auto-select all.

### Adaptation for Systematic Reviews / Umbrella Reviews
For SR/meta-analysis/umbrella reviews, Reference Verification takes a different form:
- Instead of checking individual citation accuracy, assess the **quality of included studies**
- Check whether the search strategy was comprehensive (databases, date range, grey literature)
- Verify the quality assessment tool used (AMSTAR-2 for SRs, Cochrane RoB for RCTs)
- Flag if conclusions are stronger than the quality of included evidence supports
- Check for overlap in primary studies across included SRs (umbrella reviews)
- **Run the actual PRISMA 2020 checklist against this paper** (not just "did they cite PRISMA") —
  walk the 27 items (title/abstract/introduction/methods/results/discussion/funding sections;
  full item list at `prisma-statement.org` if needed) and mark each Reported / Partial / Missing.
  Report only the gaps (don't pad a table of 27 ✅ rows) — missing protocol registration,
  incomplete search strategy reporting, or no risk-of-bias-across-studies assessment are the
  highest-yield flags. This is a reporting-completeness check on the paper's OWN methods
  section, separate from AMSTAR-2 (which judges methodological rigor).

### Step 2: CrossRef existence gate (anti-hallucination, do this FIRST)
Before any semantic comparison, run a cheap deterministic existence check per selected reference —
this catches fabricated DOIs and "right DOI, wrong paper" swaps that a purely semantic read misses
(ported from htlin222/robust-lit-review's `crossref.py`, the same anti-hallucination gate DeepTRACE
found necessary — LLM-written citations run 40–80% accuracy unaudited):
- WebFetch `https://api.crossref.org/works/{doi}` (no key needed). 404 / no `message` → **does not
  exist** — flag ❌ **fabricated/unresolvable DOI**, do not proceed to semantic comparison for it.
- If it resolves, compare the returned `title` against the reference's title as cited in the paper
  (simple token-overlap read, not exact-match — journals reformat titles). Low overlap → flag
  ⚠️ **DOI resolves to a different paper** before trusting the citation at all.
- No DOI given for a reference → note "no DOI, existence unverified" and rely on Semantic
  Scholar/PubMed title search as the fallback existence check.
- **Hard rule — existence pass is never a claim-level pass**: machines catch nonexistence,
  not misquotation. A CrossRef pass only unlocks Step 3; it must never shortcut or
  substitute the semantic comparison. If CrossRef itself is down, mark "existence gate
  skipped" on affected rows and still run Step 3 — degrade to explicit uncertainty,
  never to a silent pass.

### Step 3: Verify each claim (semantic layer, only for references that passed Step 2)

**Delegate Steps 2-3 as a batch** (see §Delegation): split the selected references across 1-2
`model: "sonnet"` agents; each returns only completed Step-4 table rows (+ explicit "FAILED" rows
where a lookup died). Main context assembles the table and judges borderline verdicts.

For each key claim and its cited reference:
- Use Semantic Scholar `get_paper_details` or PubMed MCP `get_article_metadata` to get the reference's abstract
- Compare what the paper says the reference found vs. what the reference actually says
- Classification:
  - ✅ **Accurate** — faithful representation
  - ⚠️ **Minor discrepancy** — slightly overstated, simplified, or missing nuance
  - ❌ **Misrepresented** — the reference doesn't support the claim, says something different,
    or is taken out of context
- If a reference looks suspicious at abstract level, try to get full text (same acquisition
  strategy, but only for suspicious ones)

### Step 4: Output verification table

| # | Reference | CrossRef | Claim in Paper | Reference Actually Says | Verdict |
|---|-----------|----------|---------------|------------------------|---------|
| 1 | Author2020 | ✅ exists, title matches | "X causes Y" | "X correlates with Y in subset" | ⚠️ overstated |

## Critical Appraisal (integrated after Phase 5-6)

### Step 1 — Route by study design (MANDATORY, do not use a generic checklist)

Identify the design first, then appraise domain-by-domain with the matching tool. Each domain gets
🟢/🟡/🔴 + a one-line justification, then an overall risk-of-bias judgement.

| study_type | Tool | Domains to walk through |
|---|---|---|
| RCT | **Cochrane RoB 2** | randomization process / deviations from intended interventions / missing outcome data / outcome measurement / selective reporting |
| Cohort / case-control / cross-sectional | **ROBINS-I** (interventions) or **Newcastle-Ottawa** (etiologic) | confounding / selection / classification of exposure / missing data / outcome measurement / selective reporting |
| SR / MA | **AMSTAR-2** critical domains + **GRADE per outcome** | protocol registration / search adequacy / RoB of included studies / meta-analysis methods / publication bias / heterogeneity handling |
| Diagnostic accuracy | **QUADAS-2** | patient selection / index test / reference standard / flow & timing |
| Prediction model | **PROBAST** | participants / predictors / outcome / analysis (EPV, validation) |
| Guideline | **AGREE II** (精簡: rigor of development + editorial independence) | evidence base / recommendation-evidence link / COI management / update policy |
| Narrative review | **SANRA** + cherry-picking check | justification / literature search description / referencing of key statements / are contradicting studies acknowledged? |
| Case series / report | **JBI checklist** | consecutive inclusion / clear criteria / complete reporting |

**Observational studies additionally**: read the bundled **`causal-appraisal.md`** (35 Hernán +
Users' Guide doctrines, folded into this skill — no external dependency) and check the applicable
ones explicitly (confounding by indication, immortal time bias, selection into study, time-zero
misalignment, collider bias…). Name the doctrine when flagging a problem — teachable output.

### Step 2 — Statistical & spin review

- **Statistical significance ≠ clinical significance**: for each primary outcome, compare the
  effect size against the **MCID** of the instrument (search vault/textbook-md for the MCID of
  common `${persona.specialty}` scales; cite the source). p<0.05 but < MCID → say so explicitly.
- **RCT extras**: ITT vs per-protocol (which was used, does it matter here), multiplicity
  correction for multiple outcomes/timepoints, **fragility index** when computable from a 2×2
  (events small → quote it), sample size calculation vs actual enrollment.
- **Trial registration check** (RCTs; prospective SRs → PROSPERO): WebFetch the
  ClinicalTrials.gov / registry record and compare **registered primary outcome vs published
  primary outcome**. Outcome switching or unreported registered outcomes → 🔴 flag. No
  registration for a modern RCT → 🔴.
- **Spin detection**: put the abstract conclusion side-by-side with the actual results. Flag when
  the conclusion (a) claims benefit off a non-significant primary outcome via secondary/subgroup
  emphasis, (b) generalizes beyond the studied population, or (c) omits harms.
- **Argument-structure check** (does the conclusion follow from the paper's own premises?) — run it
  through the bundled **`argdown_lint.py`** so the verdict is a deterministic gate, not an impression:
  1. Read the paper's conclusion sentence → `claim` + `claim_type` (causal / hard_endpoint /
     consistency / general).
  2. List each primary/secondary finding meant to support it as a premise, TAGGING its type
     (`direct_rct` / `association` / `surrogate_outcome` / `single_study` / `subgroup` /
     `secondary_outcome` / `mechanistic` / `expert_opinion`).
  3. `python argdown_lint.py argmap.json` — it flags the illicit jumps deterministically
     (surrogate→hard-endpoint, association→causal, single-study→"consistently shows",
     subgroup/secondary-only→benefit). Exit 1 = a gap exists.
  The LLM does the semantic tagging; the script does the logic. Write the flagged gap(s) inline in
  this section; when the linter returns clean (exit 0), skip silently (don't pad every paper).
- **Funding & COI**: funding source, sponsor role in design/analysis, author COI vs the
  direction of conclusions.

### Step 3 — Grade and summarize

- **GRADE** (per main outcome where applicable) — **recompute the certainty with the bundled
  `grade_judge.py`, don't let a holistic LLM impression stand.** The model rates the domains; the
  script computes the authoritative final grade (its value, not your gut-call label, goes in the note):
  1. Starting level: RCT-dominant evidence → `high`; observational-dominant → `low`.
  2. Rate each of the 5 domains — risk_of_bias / inconsistency / indirectness / imprecision /
     publication_bias — as `not_serious` (0) / `serious` (−1) / `very_serious` (−2), one-sentence
     justification each.
  3. Observational + no downgrade applied → add `upgrades` (large_effect RR>2 or <0.5 → +1, RR>5 or
     <0.2 → +2; dose_response; opposing_confounding). The script enforces the GRADE rule that
     upgrades apply only to observational evidence with no downgrade — don't pre-filter, just list them.
  4. Write the ratings to `grade_input.json` and run
     `python grade_judge.py grade_input.json`. The printed FINAL CERTAINTY is authoritative and goes
     into the `品質快照` + Critical Appraisal. If your holistic impression disagrees with the computed
     value, that's a signal to re-examine a domain rating, not to override the number.
     (Deterministic core ported from htlin222/robust-lit-review's `grade_judge.py`.)
- **Limitations**: authors' own AND unacknowledged ones.
- Fill the note's `## Critical Appraisal` section (domain table) **and** the `品質快照` callout
  (see note template) — the snapshot is the 10-second verdict, the section is the evidence.

## Phase 7: Citation & Impact Analysis

Evaluate how the paper has been received by the academic community and public:

**Academic citations:**
- **scite first**: `mcp__zotero__scite_enrich_item` (or `scite_enrich_search`) → supporting /
  mentioning / **contrasting** citation counts. A non-trivial contrasting count is the signal to
  dig — deep-read only the contrasting/critical citers instead of sampling blindly.
- `get_paper_citations` → list of citing papers
- Categorize the top 5-10 most relevant citing papers:
  - 🟢 **Supporting**: builds on or confirms findings
  - 🔴 **Contradicting**: presents opposing evidence
  - 🔵 **Extending**: takes the work in a new direction
  - 🟡 **Methodological critique**: questions the methods or analysis
- Note total citation count and trend (increasing? plateaued?)

**Public/social discussion** (part of the Phase-7 delegated agent, see §Delegation):
- WebSearch: `"{title}" OR "{DOI}" site:pubpeer.com`
- WebSearch: `"{title}" OR "{DOI}" twitter OR reddit OR blog`
- Look for news coverage, especially in medical/science news outlets
- Note any notable commentary, criticism, or endorsement
- WebSearch/WebFetch failure or zero hits → state "PubPeer/social sweep: no hits / FAILED (<reason>)" in the note — an unrun sweep must not read as "no criticism found"

Output: impact assessment relative to field norms and paper age.

## Output: Obsidian Note

Write to `${vault.papers_dir}{FirstAuthorYear} - {Short Title}.md`

If a note for this paper already exists (check by DOI or PMID), **merge** the deep review
sections into the existing note rather than creating a duplicate. Show the user a diff of
changes before writing (per CLAUDE.md rules). **Brand-new note → show the full draft before
writing** (CLAUDE.md tiered approval — new notes are draft-first, same as merges are diff-first).

### Note template — 三塊結構

筆記分為三塊邏輯：(1) 讀完能用 (2) 可不可信 (3) 連結與來源

Quick review（`[x]` checkbox 觸發）只寫前兩塊 + Resource。
Deep review（`/paper-review` 觸發）加入 `# Deep Review` 段落。

**`## 白話導讀` 一律要寫（quick 與 deep 都寫）**：放在 `## Summary` 之後、`## Clinical Application` 之前，
用一個 `> [!abstract]` callout 把整篇用繁體中文白話「講一遍」，讓使用者不必讀完深度評讀就能掌握全篇在說什麼。
這是「導讀／意譯」不是逐句翻譯。外框固定三段（一句話 / 為什麼做 / 所以呢），**中間「主體」依 `study_type` 分流**：

- **RCT**：逐組講清楚——實驗組 vs 對照組各自的 protocol（具體介入、劑量、頻率、療程；對照是 sham 還是 standard care），
  且每個 outcome 要給**兩組的實際數值與組間差異**（mean±SD / Δ / 95% CI / p），不可只寫「有顯著差異」。
- **SR/MA**：逐 outcome 講——每個 outcome 的**納入族群定義**（PICO）+ pooled effect（SMD/RR/OR + 95% CI、I²、納入篇數/人數）。
- **Narrative review**：逐組別/主題講——他把主題分成哪幾組，每組整理了什麼重點（一組一行）。
- **觀察性研究（cohort/case-control/cross-sectional）**：逐組講——各組的**定義**、各組的**結果（關鍵數值）**、
  以及作者**推測的原因/機轉**（明確標示為 inference，不是因果證實）。

醫學名詞、藥名、參數、量表保留英文，關鍵數值用 ==highlight==，其餘用白話中文。
abstract-only 時就依摘要能取得的範圍寫，缺的數值標「abstract 未報告，需全文確認」，並沿用 `## Summary` 的 ⚠️ 標記。

```markdown
---
tags:
  - source/journal
  - med/{specialty}      ← 只用已存在的 med/ tag，新 tag 需更新 registry
citekey: "{BBT citation key}"
doi: "{DOI}"
zotero: "zotero://select/items/@{citekey}"
journal: "{Journal}"
year: {YYYY}
authors: "{All authors}"
study_type: "{RCT/SR+MA/cohort/etc.}"
pmid: "{PMID}"
review_depth: "quick"   ← 或 "deep"
---

> [!info] 品質快照
> **設計**：{RCT / cohort / SR+MA…}｜**n**：{樣本數}｜**RoB**（{RoB 2/ROBINS-I/AMSTAR-2…}）：{🟢低/🟡中/🔴高}
> **GRADE**：{High/Moderate/Low/Very Low}（主要 outcome）｜**Registration**：{✅一致 / 🔴 outcome switching / ❌未註冊 / n.a.}
> **一句話 verdict**：{可信度＋最關鍵的 1-2 個弱點，例：可信度中等——隨機化健全但 open-label、primary outcome 未達 MCID}

# Key Points

## Summary

> ⚠️ Based on abstract only  （或 > ✅ Full text reviewed）

- 一句話重點，==highlight== 最重要數值

## 白話導讀

> [!abstract] 整篇講給你聽（繁體中文白話）
> - **一句話**：這篇到底在說什麼
> - **為什麼做**：背景動機、想補的研究缺口
> - **主體**（依研究類型，見下方規則填對應結構）
> - **所以呢**：臨床/實務上的意義 + 最重要的 1-2 個限制

> [!example]- 主體結構範例（依 study_type 擇一，實際只留對應那種）
> **RCT** — 逐組講清楚 + outcome 實際展現：
> - 組別 protocol：實驗組（介入、劑量/頻率/療程）vs 對照組（sham/standard care 具體是什麼）
> - 每個 outcome：實驗組 vs 對照組 的==實際數值與組間差異==（不只寫「有顯著」；給 mean±SD / Δ / 95% CI / p）
>
> **SR/MA** — 逐 outcome 講：
> - 每個 outcome：納入的==族群定義==（誰、什麼介入、什麼比較）+ pooled effect（==SMD/RR/OR + 95% CI==、I² 異質性、納入幾篇/幾人）
>
> **Narrative review** — 逐組別/主題講：
> - 他把主題切成哪幾個組別/段落，==每一組整理了什麼重點==（一組一行）
>
> **觀察性研究（cohort / case-control / cross-sectional）** — 逐組講：
> - 各組的==定義==（暴露/非暴露、case/control 怎麼分）
> - 各組的結果（==關鍵數值==）
> - 作者推測的原因/機轉（標明這是 inference，非因果證實）

## Clinical Application

- **適應症：**（具體 condition、severity）
- **Protocol：**（full text 時補充：頻率、pulse 數、coil 類型、治療天數、時機）
- **禁忌/注意：**
- **實務 tips：**
- **在地適用性 / external validity：** 研究族群能否外推到 `${persona.locale}` 的
	`${persona.specialty}` 病人。**給付/自費查詢為 OPTIONAL**：只在 `${persona.reimbursement_system}`
	非空、且使用者問到給付或介入明顯涉及給付決策時才查（用你設定的給付資料庫工具）；否則略過此 bullet。

# Paper Details

## Methods

- 研究設計、收案條件、介入方式
- （full text 時補充：statistical methods、sample size calculation、具體 protocol）

## Critical Appraisal

- **RoB 工具逐 domain**（依 study_type 路由表選工具）：
	| Domain | 判定 | 理由 |
	|---|---|---|
	| {domain 1} | 🟢/🟡/🔴 | 一句理由 |
- **統計/Spin**：MCID 比對、ITT vs PP、multiplicity、fragility index、registration 比對、abstract 結論 vs 實際結果
- **Funding/COI**：
- **GRADE（逐主要 outcome）**：等級 + 升降級理由
- 🟢 優點 / 🔴 風險限制 / 🟡 需注意
- （沒有資訊不硬評，標記「abstract 未報告，需全文確認」）

### Reference Verification          ← deep review 時才加
| # | Reference | Claim | Actually Says | Verdict |
|---|-----------|-------|---------------|---------|

## Key Findings

- 結構化結果，==highlight== 關鍵數值
- （full text 時補充：secondary outcomes、subgroup、tables）

# Deep Review                       ← /paper-review 觸發時才加

## Background & Context             ← Phase 5
## Citation & Impact                ← Phase 7
## Publication Details
### Journal Credibility             ← Phase 2（查 journal_cache.json）
### Author Profile                  ← Phase 3（查 author_cache.json）
### Publication Timeline            ← Phase 4

# Resource

## Vault Integration

- 相關筆記：（vault-search 結果）
- 補充到：（`${vault.medicine_dir}` 目標）

## Source

- [Zotero](zotero://select/items/@{citekey})
- [DOI](https://doi.org/{DOI})
- [PubMed](https://pubmed.ncbi.nlm.nih.gov/{PMID}/)
- [全文 (link resolver)](${fulltext.sfx_base})   ← 用 config 的 sfx_base，{DOI} 代入；sfx_base 空則省略此行
```

### 格式規範

- 檔名：`AuthorYear - Short Title.md`（如 `Portaro2025 - Neuromodulation for SCI Pain.md`）
- 無 aliases
- Tab 縮排
- 繁體中文 + English 醫學術語
- ==highlight== 關鍵數值，**bold** 重要術語
- Journal/Author 優先查 `~/.claude/skills/paper-review/journal_cache.json` 和 `author_cache.json`，避免重複 WebSearch
- Hook `check-note-format.py` 檢查 12a-h 會硬擋格式錯誤

## Output: Daily Note Entry

完成 review 後，append 到今天 daily note 的 `${vault.daily_section}`（如 `## 論文評讀`）：

```markdown
- [x] N. **{Title}** — {Journal} → [[{AuthorYear} - {Short Title}]]
  - 📎 `{citekey}` | {study_type} | {sample}
  - 🔑 {一句重點發現}
```

**觸發來源：**
- Daily note `[x]` checkbox → Quick review
- 用戶說 `/paper-review` 或「review {citekey}」→ Deep review
- 用戶手動指定論文（不在 daily note 裡的）→ 同樣 append 到 daily note `${vault.daily_section}`
- 用戶說「更新全文」→ Upgrade（⚠️→✅，補充 Methods/Findings/Appraisal）
- 用戶說「深入這篇」→ Quick→Deep（插入 # Deep Review）

## Workflow Interaction

- **Show progress after each phase**. After Phase 1, confirm the paper identity with the user.
  After each subsequent phase, briefly show key findings so the user can say "skip" or "go deeper".
- **Phase 6 collaboration**: If >20 references, present the paper's key claims and ask the user
  which to verify. This saves time and focuses on what matters to them.
- **Merge with existing notes**: Always check if `${vault.papers_dir}` already has a note for this paper
  before creating a new file. Use Glob to search by author+year pattern.
- **Vault linking**: Use `vault_search` MCP to find related notes in `${vault.medicine_dir}` and add
  `[[internal links]]` in the Clinical Relevance section.

## Error Handling

- If full text is unavailable from all sources: proceed with abstract + whatever metadata is
  available, but clearly note "⚠️ Abstract-level review only — full text not obtained" at the
  top of the Deep Review section. Reference verification will be limited.
- If Semantic Scholar returns no results: fall back to PubMed-only data. Citation analysis will
  be limited.
- If Zotero is not running: remind user to open Zotero (Local API needs it running).
- If Zotero MCP fails: fall back to Semantic Scholar abstract + WebSearch for available info.

## Self-Check (before finalizing note)
- [ ] `品質快照` callout 已寫（設計/n/RoB/GRADE/registration/一句話 verdict）
- [ ] Critical Appraisal 用了 study_type 對應的 RoB 工具、逐 domain 給判定（不是泛用 checklist）
- [ ] 統計/Spin 檢查：主要 outcome 有 MCID 比對；RCT 有 registration 比對
- [ ] GRADE 由 `grade_judge.py` 算出（餵 domain ratings → 取印出的 FINAL CERTAINTY），非整體印象單一給分
- [ ] 有 spin/因果爭議時，argument-structure 有跑 `argdown_lint.py`（premise 已標 type，gap 有寫進 note）
- [ ] `## 白話導讀` callout 已寫（5 面向齊全，白話中文 + 術語保留英文）
- [ ] All phases have content (or explicit "skipped — reason")
- [ ] Reference Verification table has ≥3 checked references (deep review), each with a CrossRef
      existence check before the semantic verdict — no reference marked ✅/⚠️ without first passing
      (or explicitly failing) the CrossRef gate
- [ ] SR/MA 論文：PRISMA 2020 27 項有跑過、缺項有列出（非只寫「有用 AMSTAR-2」）
- [ ] Author profile includes h-index + top papers for first/corresponding author
- [ ] Journal credibility has specific metrics (IF, SJR, indexing) + scite retraction check
- [ ] Clinical Application section is filled (not just methods summary)
- [ ] Frontmatter complete: citekey, doi, zotero, journal, year, study_type, review_depth
