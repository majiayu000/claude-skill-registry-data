---
name: design-science-research
version: 1.0.0
description: Supports structuring DSR (Design Science Research) papers, distinguishing existence proofs from causal claims, and managing process evidence such as Git logs and AI session logs. Use when designing or writing a paper that adopts the DSR paradigm.
---

# Design Science Research Skill

## Purpose
Supports DSR papers by structuring research per Hevner et al. (2004), enforcing the distinction between **existence proofs** and **causal claims**, and managing **process evidence** (Git commits, AI session logs, artifact versioning). Tracks co-evolution of artifact and manuscript, and keeps modality (claim strength) consistent.

## When to Use
- When designing or writing a paper that adopts the DSR paradigm
- When developing an artifact (tool, skill, system) alongside the paper
- When you need to distinguish "this was constructible" from "this caused improvement"
- When reviewers flag conflation of existence proof and empirical demonstration

## Prerequisites
- [`research-plan-workshop`](../research-plan-workshop/SKILL.md) completed
- [`scholarly-concept-modeling`](../scholarly-concept-modeling/SKILL.md) completed

## Procedure

### Step 1: DSR Guidelines Check
Map the study to Hevner et al. (2004)'s seven guidelines:

| Guideline | Check |
| :--- | :--- |
| 1. Design as an Artifact | What is the artifact (skill, tool, method)? |
| 2. Problem Relevance | What practical/theoretical problem does it solve? |
| 3. Design Evaluation | How is it evaluated (existence proof, case study, experiment)? |
| 4. Research Contributions | Contribution type: design proposition, existence proof, or empirical demonstration? |
| 5. Research Rigor | How is rigor ensured in construction and evaluation? |
| 6. Design as a Search Process | How is the search process recorded? |
| 7. Communication of Research | How is it communicated to both practitioners and researchers? |

### Step 2: Existence Proof vs Causal Claim
Classify each claim in the manuscript:

| Type | Definition | Example wording |
| :--- | :--- | :--- |
| **Design proposition** | A proposal for how to design | "should be...", "it is desirable to..." |
| **Existence proof** | That it was constructible/observable | "was constructible", "was observed" |
| **Causal claim** | That it caused improvement | "improved by...", "led to..." |
| **Generalization** | Applicability to other contexts | "generalizes to...", "universal" |

**Invariant**: Do not use causal wording for existence proofs. Do not claim statistical generalization from n=1 or single-case studies.

### Step 3: Process Evidence Management
In DSR, the design and construction process itself is evidence. Structure and record:

| Evidence | Management |
| :--- | :--- |
| Git commit history | Audit index table (timestamp, milestone, hash) |
| AI session logs | Dialogue logs with redaction policy (local paths, PII) |
| Execution environment | Verify `Agent:`/`Model:` trailers |
| Negative cases (rejections, failures) | Structured NC-XX records |

### Step 4: Artifact ↔ Manuscript Mapping
Track artifact versions against manuscript descriptions:

```markdown
| Artifact version | Manuscript section | Commit |
| :--- | :--- | :--- |
| v2.0.0 | Ch.4 §4.2 reference implementation | `abc1234` |
| v2.4.0 | Ch.4 §4.3 co-adaptation | `def5678` |
```

### Step 5: Modality Calibration Report
Output to `docs/design/dsr-structure.md`:
- DSR guidelines mapping
- Existence proof / causal claim classification
- Process evidence index
- Artifact-manuscript mapping table

## Outputs
- `docs/design/dsr-structure.md` (DSR structuring report)
