---
name: screening-engine
description: >
  Activate when the user needs to systematically screen papers for a Systematic
  Literature Review (SLR). Implements the PRISMA-compliant screening pipeline:
  define inclusion/exclusion criteria, title/abstract screening, full-text screening,
  quality assessment, and PRISMA flow diagram generation. Takes the literature_base.csv
  from Phase 1 (Reconnaissance) and produces a filtered, documented, auditable
  set of included studies.
---

> **Orchestration Log**: When this skill is activated, append a log entry to `outputs/orchestration_log.md`:
> ```
> ### Skill Activation: Screening Engine
> **Timestamp:** [current date/time]
> **Actor:** AI Agent (screening-engine)
> **Input:** [N] papers from literature_base.csv, [N] inclusion criteria, [N] exclusion criteria
> **Output:** [N] papers included after screening, PRISMA diagram generated, screening_log.md saved
> ```

# Screening Engine

## Core Principle

A systematic literature review without documented screening is not systematic. This
engine transforms the raw search results from Phase 1 (Reconnaissance) into a
defensible, reproducible set of included studies. Every inclusion and exclusion
decision is documented with a reason, producing the audit trail that reviewers and
editors expect.

The screening process follows PRISMA 2020 (Page et al., 2021) and adapts the
guidelines of vom Brocke et al. (2009, 2015) for IS research.

## When to Activate

- User is conducting a Systematic Literature Review (SLR)
- User says "screen papers", "filter papers", "apply inclusion criteria"
- User says "PRISMA", "screening process", "title/abstract screening"
- After Phase 1 (Reconnaissance) when method is SLR
- When `literature_base.csv` exists and needs systematic filtering
- User runs `/screen-papers`

## Prerequisites

- `literature_base.csv` exists (from Phase 1 / literature-engine)
- Research questions are defined (from Phase 2 / framing.md)
- Target method is SLR (confirmed in Phase 2 or by user)

---

## Step 1: DEFINE Inclusion/Exclusion Criteria

### Criteria Template

Before screening begins, establish and document clear criteria:

```markdown
## Screening Protocol

### Inclusion Criteria (IC)

| ID  | Criterion | Rationale | Operationalization |
|-----|-----------|-----------|-------------------|
| IC1 | Peer-reviewed journal article or conference paper (ICIS, ECIS, HICSS, AMCIS, or equivalent) | Quality assurance | Check venue against VHB-JOURQUAL, AIS proceedings, or established CS venues |
| IC2 | Focuses on [topic] in [context] | Scope alignment | Title/abstract must explicitly address [specific keywords] |
| IC3 | Published between [year] and [year] | Recency/coverage | Check publication date |
| IC4 | Available in English or German | Accessibility | Check language field |
| IC5 | Empirical or conceptual contribution | Substance | Must present findings, framework, or theory — not just opinion |

### Exclusion Criteria (EC)

| ID  | Criterion | Rationale | Operationalization |
|-----|-----------|-----------|-------------------|
| EC1 | Purely technical paper with no organizational/social dimension | Out of scope | No mention of users, organizations, processes, or adoption |
| EC2 | Editorial, book review, workshop abstract, poster, or abstract-only | Insufficient depth | Less than 4 pages or no methodology section |
| EC3 | Duplicate or earlier version of an included paper | Avoid double-counting | Same authors + overlapping content → keep most recent/complete |
| EC4 | Not accessible (no abstract, no full text, no DOI) | Cannot assess | Exhausted all retrieval options |
```

### Criteria Derivation

Criteria should be derived from:
1. **Research questions** — IC2 must map directly to what the RQs ask
2. **Scope boundaries** — What explicitly falls outside the study
3. **Quality thresholds** — Minimum venue quality, minimum methodological rigor
4. **Practical constraints** — Language, accessibility, date range

Present the criteria table to the user for approval before proceeding. This is a
**quality gate** — criteria should not change after screening begins (or changes
must be documented as protocol amendments).

---

## Step 2: TITLE/ABSTRACT SCREENING

### Process

For each paper in `literature_base.csv`:

1. **Read title and abstract** (abstract from CSV or fetched via API)
2. **Apply each criterion** in sequence (IC1 → IC5, then EC1 → EC4)
3. **Decision:** INCLUDE, EXCLUDE, or UNCERTAIN
4. **Record reason** for exclusion (cite the specific criterion ID)

### Decision Rules

- **INCLUDE if:** Title and abstract suggest the paper meets ALL inclusion criteria AND violates NO exclusion criteria
- **EXCLUDE if:** Title and abstract clearly violate at least one criterion
- **UNCERTAIN if:** Cannot determine from title/abstract alone → move to full-text screening
- **When in doubt, include** — it's better to over-include at this stage and exclude during full-text review

### Handling Missing Abstracts

If a paper has no abstract in `literature_base.csv`:
1. Attempt to fetch via Semantic Scholar API (by DOI or title)
2. Attempt to fetch via OpenAlex API
3. If still no abstract: mark as UNCERTAIN → include for full-text screening
4. If no full text available either: mark as EXCLUDE with reason EC4

### Output Format

For each paper, record:

```
{
  "id": "[CSV row or bib_key]",
  "title": "[paper title]",
  "authors": "[first author et al.]",
  "year": [year],
  "venue": "[venue]",
  "screening_decision": "INCLUDE" | "EXCLUDE" | "UNCERTAIN",
  "exclusion_reason": "EC2" | null,
  "exclusion_detail": "Workshop abstract, 2 pages, no methodology" | null,
  "screener_note": "[optional note]"
}
```

### Batch Processing

Process papers in batches of 20-30. After each batch:
- Report progress: "Screened [N]/[total]. Included: [n], Excluded: [n], Uncertain: [n]"
- Save intermediate results to `screening/title_abstract_screening.csv`
- Continue unless the user intervenes

---

## Step 3: FULL-TEXT SCREENING

### When to Apply

Full-text screening is performed on:
1. All papers marked INCLUDE after title/abstract screening
2. All papers marked UNCERTAIN after title/abstract screening

### Process

For each paper:

1. **Obtain full text:**
   - Check if PDF is available (open access, arXiv, institutional access)
   - If PDF available: read introduction, methodology, and conclusion sections
   - If only abstract available: make decision based on abstract + metadata

2. **Apply criteria with full context:**
   - Does the paper actually address the topic (not just mention keywords)?
   - Does it have a clear methodology section?
   - Does it present findings relevant to the RQs?
   - Is the venue quality sufficient?

3. **Decision:** INCLUDE or EXCLUDE (no more UNCERTAIN at this stage)
4. **Record reason** for exclusion with specific detail

### Exclusion Reason Categories for Full-Text

Track exclusion reasons to report in the PRISMA diagram:

| Reason Category | Example |
|----------------|---------|
| Wrong population/context | Studies AI in healthcare, not enterprise context |
| Wrong intervention/topic | Focuses on AI ethics, not implementation |
| Wrong outcome | Measures technical performance, not organizational impact |
| Wrong study type | Opinion piece, no empirical or conceptual contribution |
| Insufficient quality | No clear methodology, weak evidence base |
| Duplicate/superseded | Earlier version of an already-included paper |
| Not accessible | Cannot obtain full text despite best efforts |

### Output

Save to `screening/full_text_screening.csv` with the same format as title/abstract
screening, plus:
- `full_text_available`: true/false
- `full_text_exclusion_category`: one of the categories above

---

## Step 4: QUALITY ASSESSMENT

### Purpose

After the final set of included papers is determined, assess their methodological
quality. This is NOT an inclusion/exclusion step — it's a characterization that
informs the synthesis (e.g., weighting findings from high-quality studies more).

### Quality Checklist (adapted for IS research)

For each included paper, assess:

| Criterion | Assessment | Notes |
|-----------|-----------|-------|
| Q1: Clear research objective/question stated? | Yes / Partial / No | |
| Q2: Appropriate methodology for the research goal? | Yes / Partial / No | |
| Q3: Data collection described adequately? | Yes / Partial / No / N/A | |
| Q4: Data analysis described adequately? | Yes / Partial / No / N/A | |
| Q5: Findings clearly linked to evidence? | Yes / Partial / No | |
| Q6: Limitations acknowledged? | Yes / Partial / No | |
| Q7: Contribution clearly stated? | Yes / Partial / No | |
| Q8: Published in a reputable venue? | A+/A / B / C / Other | VHB-JOURQUAL or equivalent |

### Scoring

- **Yes** = 1 point, **Partial** = 0.5, **No** = 0
- Maximum: 8 points (Q8 normalized: A+/A=1, B=0.75, C=0.5, Other=0.25)
- Papers scoring below 4 should be flagged for potential exclusion or careful handling in synthesis

### Output

Save to `screening/quality_assessment.csv`:

```
bib_key, title, Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8_venue, Q8_score, total_score, quality_tier
wang2024, "Wang et al. 2024", Yes, Yes, Yes, Partial, Yes, Yes, Yes, A, 1.0, 7.5, High
smith2023, "Smith et al. 2023", Yes, Partial, No, No, Partial, No, Yes, C, 0.5, 3.5, Low
```

Quality tiers: High (>6), Medium (4-6), Low (<4)

---

## Step 5: GENERATE PRISMA Flow Diagram

### PRISMA 2020 Template

Generate both a text-based PRISMA diagram and a visual diagram via figure-engine.

#### Text-Based PRISMA (always generate):

```markdown
## PRISMA Flow Diagram

### Identification
- Records identified through database searching: [N]
  - Semantic Scholar: [n]
  - OpenAlex: [n]
  - CrossRef: [n]
  - arXiv: [n]
- Additional records from snowballing: [n]
- **Total records identified: [N]**
- Duplicate records removed: [n]
- **Records after deduplication: [N]**

### Screening
- Records screened (title/abstract): [N]
- Records excluded: [n]
  - [Reason 1]: [n]
  - [Reason 2]: [n]
  - [Reason 3]: [n]

### Eligibility
- Full-text articles assessed: [N]
- Full-text articles excluded: [n]
  - Wrong population/context: [n]
  - Wrong intervention/topic: [n]
  - Wrong outcome: [n]
  - Wrong study type: [n]
  - Insufficient quality: [n]
  - Duplicate/superseded: [n]
  - Not accessible: [n]

### Included
- **Studies included in synthesis: [N]**
  - Journal articles: [n]
  - Conference papers: [n]
  - Preprints: [n] (if included)
```

#### Visual PRISMA Diagram:

Generate via figure-engine / PaperBanana direct Python API:

```
Use the generate_diagram tool with:
- source_context: The PRISMA text above with all numbers filled in
- caption: "PRISMA 2020 flow diagram of the systematic search and screening process"
```

Save as `figures/fig_prisma_flow.png`.

---

## Step 6: SAVE & DOCUMENT

### Output Files

| File | Content |
|------|---------|
| `screening/screening_protocol.md` | Criteria, process description, dates |
| `screening/title_abstract_screening.csv` | All papers with T/A screening decisions |
| `screening/full_text_screening.csv` | Full-text screening decisions |
| `screening/quality_assessment.csv` | Quality scores for included papers |
| `screening/screening_summary.md` | PRISMA counts, summary statistics |
| `figures/fig_prisma_flow.png` | Visual PRISMA diagram |
| `literature_base_screened.csv` | Final set of included papers (filtered CSV) |

### Update references.bib

After screening, update `references.bib` to contain ONLY the included papers
(keep the original as `references_full.bib` for audit).

### Screening Summary

```markdown
# Screening Summary

**Date:** [ISO 8601]
**Total identified:** [N] papers
**After deduplication:** [N] papers
**After title/abstract screening:** [N] papers (excluded: [n])
**After full-text screening:** [N] papers (excluded: [n])
**Final included:** [N] papers

## Included Papers by Characteristic

### By Year
| Year | Count |
|------|-------|
| 2024 | [n]   |
| 2023 | [n]   |
| ...  | ...   |

### By Method
| Method | Count |
|--------|-------|
| Survey | [n]   |
| Case Study | [n] |
| ...    | ...   |

### By Venue Type
| Type | Count |
|------|-------|
| Journal (A+/A) | [n] |
| Journal (B)    | [n] |
| Conference     | [n] |
| Preprint       | [n] |

### Quality Distribution
| Tier | Count | % |
|------|-------|---|
| High (>6)   | [n] | [%] |
| Medium (4-6)| [n] | [%] |
| Low (<4)    | [n] | [%] |
```

---

## Error Recovery

- **Too many papers after dedup (>200):** Tighten search queries or add stricter criteria before screening. Report to user.
- **Too few papers after screening (<10):** Loosen criteria or expand search scope. Report to user with options.
- **No abstracts available for many papers:** Use title-only screening for those papers, flag as lower confidence.
- **User changes criteria after screening started:** Document as protocol amendment. Re-screen affected papers. Note in screening_protocol.md.

---

## Integration with Pipeline

| Phase | Integration |
|-------|-------------|
| Phase 1 (Reconnaissance) | Takes `literature_base.csv` and `references.bib` as input |
| Phase 2 (Framing) | Screened set informs theory selection and gap formulation |
| Phase 3 (Architecture) | Concept matrix built from screened papers only |
| Phase 4 (Production) | Only screened papers cited in the paper text |
| Method-engine | PRISMA numbers populate the method section template |
| Figure-engine | PRISMA flow diagram generated as figure |
