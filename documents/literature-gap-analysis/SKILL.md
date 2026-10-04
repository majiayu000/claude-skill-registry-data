---
name: literature-gap-analysis
version: 1.1.0
description: Use during literature review or introduction drafting to extract gaps between current literature (AS-IS) and proposed contribution (TO-BE)
---

# Literature Gap Analysis Skill

## Purpose
Apply Spec Gap Analysis discipline to compare existing literature (AS-IS) with the proposed paper's novelty (TO-BE), clearly defining the research gap and contribution for Introduction and Related Work sections.

## Trigger Conditions
- When drafting the Introduction or Related Work section
- When defining the paper's novel contribution after completing the literature review
- When a reviewer questions the paper's originality

## Workflow

### Step 1: Summarize Prior Art (AS-IS)
Extract key findings, methods, and datasets from `docs/literature/literature-matrix.md` to establish the current state of knowledge.

### Step 2: Construct the Gap Matrix (TO-BE vs AS-IS)
Create a structured comparison matrix highlighting the specific gaps this paper fills:

```markdown
| Research Dimension | Existing Literature (AS-IS) | Proposed Paper (TO-BE) | Novel Contribution (Gap) |
|---|---|---|---|
| Dataset / Sources | Public macro statistics | Micro-level archival records | Data granularity expansion |
| Methodology | Qualitative case study | Mixed-methods NLP analysis | Methodological framework renewal |
| Scope / Conclusion | Domain-specific validity only | Cross-domain applicability demonstrated | Scope extension & theoretical revision |
```

### Step 2.5: Evidence Standard for Closest-Neighbor Difference Records (v1.1.0)

When recording differences from literature rated "highest (closest neighbor)":

1. **Section-level trace for negative differences**: every negative difference claim ("X lacks ...", "... not presented") must cite the sections, tables, or figures checked (e.g., "no MHC connection → corrected after finding tracking/tracing cited in §3"). Negative claims without traces are provisional.
2. **Record convergence points too**: note where the prior work contains concepts isomorphic to your own, not only differences — convergences become reinforcement material via citation.
3. **Pre-propagation gate**: before copying difference records into SoT artifacts (abstract, paper outline), re-verify against the full text once.

### Step 3: Generate Contribution Statement
Based on the extracted gaps, compose a positioning statement for the Introduction: "While prior work has focused on X using method Y, this paper employs Z to reveal W, thereby addressing the gap of..." If the novelty is a genealogical connection and T3 in [`diachronic-claim-typing`](../diachronic-claim-typing/SKILL.md) has not passed, downgrade it to juxtaposition/comparison. Negative novelty claims ("no prior work ...") based only on title searches must be marked "provisional" and confirmed via citation-network search and full-text reading of closest neighbors before being finalized (v1.1.0).

## Outputs
- `docs/literature/literature-gap-report.md` (Literature Gap Report)

