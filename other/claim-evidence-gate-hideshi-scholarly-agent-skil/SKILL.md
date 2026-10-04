---
name: claim-evidence-gate
version: 1.4.1
description: Use when validating claims against primary sources, empirical data, or citation evidence prior to submission or peer review
---

# Claim & Evidence Gate Skill

## Purpose
Apply invariant validation discipline to verify that every thesis claim in the manuscript is directly backed by primary sources, empirical data, or validated citations. This gate prevents unevidenced assertions, quote mining, and modality-evidence misalignment from reaching submission.

## Trigger Conditions
- After completing a draft of each chapter or major section
- During the final pre-submission review phase
- When a reviewer or collaborator raises concerns about evidentiary support

For diachronic claims (transmission, juxtaposition, continuity, novelty), check the [`diachronic-claim-typing`](../diachronic-claim-typing/SKILL.md) inventory. Do not PASS transmission (T3) on similarity alone.

## Evaluation Steps

### Step 0: Literature Grounding Prerequisite (added in v1.3.2)
- **If `python3 scripts/check_literature_grounding.py` returns FAIL, halt this gate** and return to `citation-traceability-audit` Step 2.5 (literature ingestion).
- WARN-only results may proceed (full-text grounding recommended before submission).

### Step 1: Extract Claim–Evidence Pairs
1. Identify paragraph blocks containing claims, statistical figures, or calculated values (ratios, percentage changes, growth rates).
   - *Note: Execute `python3 scripts/check_fact_grounding.py` as a pre-filter candidate extractor.*
2. Pair each claim with its corresponding primary data, citation, footnote, or `docs/data/` table ID.

### Step 2: Seven-Axis Rubric & Scoring

Score each claim–evidence pair into **PASS**, **WARN**, **FAIL**, or **N/A** across seven axes:

| Evaluation Axis | PASS (Valid) | WARN (Tone Adjustment Needed) | FAIL (Unsubstantiated / Rejected) |
|---|---|---|---|
| **Direct Match** | Cited data directly substantiates claim, and calculated figures have source markers and raw values recorded in text, footnotes, or `docs/data/` | Evidence is indirect, or raw figure reference is partially ambiguous | Cited evidence contradicts claim, calculated figure lacks source marker, or figure source is unidentifiable |
| **Terminological Precision** | Key terms and numbers are accurately represented | Terminology interpretation is slightly stretched | Data/text is distorted or over-interpreted |
| **Context Safety** | Source context is fully preserved | Contextual framing is partially insufficient | Claim relies on decontextualized quote mining |
| **Modality Alignment** | Claim tone matches evidence strength | Modality is slightly too strong for sample size | Overgeneralized despite weak sample without hedging |
| **Benchmark Grounding** | Comparative or degree evaluation terms include objective benchmarks at first occurrence | Comparative benchmark is partially insufficient or reference is ambiguous | Evaluative terms used (e.g. "high", "pronounced") without any benchmark |
| **Internal Heterogeneity** | Internal differentiation of the analyzed group (skill level, region, gender, etc.) is appropriately addressed | Group is treated as homogeneous but heterogeneity is acknowledged in footnotes | Macro aggregates only; internal group differentiation is ignored |
| **Field Disagreement** | Contested claims acknowledge opposing views in the text, or the proposition is confirmed as `consensus` / `replicated` in `literature-matrix.md` | The point is contested (`contested` / `contradicted`) but opposing views appear only in footnotes, or tone remains slightly too strong despite acknowledgment | A contested proposition is asserted on a single paper with no mention of opposing views, or a `contradicted` / `retraction-watch` source is cited as established knowledge |

#### ⚠️ N/A (Not Applicable) Rules
- **Internal Heterogeneity Axis**: For claims that do not target social groups or specific categories (e.g., conceptual analysis, textual/philological interpretation, chronological dating, mathematical proofs), score this axis as **N/A**.
- **Benchmark Grounding Axis**: For purely factual descriptive statements that contain no degree or comparative evaluative terms (e.g., "The treaty was signed in 1945"), score this axis as **N/A**.
- **Field Disagreement Axis**: For factual statements where dispute cannot arise (dates, reported values from official statistics, etc.) or for claims proposing genuinely novel concepts with no prior literature, score this axis as **N/A**. Also score N/A when the contestation status is `unknown`; however, if a load-bearing claim (research question, core causal claim) remains `unknown`, recommend running `literature-search` Step 1.5 (Faction Discovery).

#### Benchmark Grounding Axis Detailed Rules
When using comparative or degree terms such as "high", "low", "significant", "pronounced", "substantial", "large", "majority", or "pronounced increase" at first occurrence, at least one of the following benchmarks must be explicitly specified:
- **Social Sciences / Development Economics**: International institutional thresholds (e.g., World Bank / UNDP warning line of 40.0 Gini), regional/national averages (e.g., ASEAN mean).
- **Natural Sciences / Empirical Data**: Statistical significance thresholds (e.g., $p < 0.05$), effect sizes (e.g., Cohen's $d > 0.8$), control group baseline values.
- **Humanities / History**: Standard critical edition text baseline, recognized periodization/baseline indicators.
- **Reference Formats**: Section anchor (`#1.2.3`), section cross-reference (`cf. Section X.X.X`), or footnote (`[^1]`). Subsequent occurrences may refer back to the initial benchmark.

### Step 3: Quality Gate Thresholds & Low Confidence Criteria

- **Active Axes Definition**: All axes excluding those marked N/A.
- **Low Confidence Criterion**: Flagged if 1 or more active axes receive WARN or FAIL.
- **Overall Gate Pass/Fail Rules**:
  - 🟢 **PASS**: All active axes PASS. No changes required.
  - 🟡 **WARN (Soften Tone / Add Benchmark)**: 0 FAILs, but 1+ WARNs. Specify the exact reason (e.g., Tone Mismatch vs Missing Benchmark) and recommend revisions.
  - 🔴 **FAIL (Requires Evidence / Revision)**: 1+ FAILs. Identify the specific failure mode (Direct Match failure, ungrounded figure, Tone vs Benchmark) and require supplementary data, citation replacement, or claim removal.

### Step 4: Generate Remediation Report
Produce `docs/design/evidence-gate-report.md` detailing scores and actionable recommendations.

## ⚠️ Output Boundary Rule
In manuscript text (`docs/chapters/`), inline citations MUST use standard academic styles (e.g., `(PSA, 2024)` or `(World Bank, 2026)`, footnotes `[^1]`).

- **Prohibition**: Printing local repository file paths (such as `data: docs/data/filename.md#tbl-1`) inside citation parentheses in manuscript text (`docs/chapters/`) is strictly forbidden.
- **Data Path Storage**: Local file paths and table IDs must be recorded and managed exclusively in `docs/data/*.md` table notes or inside `docs/design/evidence-gate-report.md`.

## Outputs
- `docs/design/evidence-gate-report.md` (Evidence Integrity Audit Report)
