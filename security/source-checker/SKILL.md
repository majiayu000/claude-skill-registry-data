---
skill_id: source-checker
name: Source Checker — verify a claim and rate the evidence
description: "Verify a factual claim — \"check this claim\", \"verify this\", \"is this true\", \"how solid is this\". Finds primary sources and rates the evidence as supported, mixed, unsupported or unverifiable, with citations."
version: 1.0.0
category: research
office: cino
lead_agent: innovation-researcher
everyday_skill: true
triggers:
  - "check this claim"
  - "verify this"
  - "is this true"
  - "how solid is this"
collaborates_with:
  - innovation-researcher
  - security-analyst     # misinformation / regulated-claim sensitivity
references:
  adr_moat_framing: documents/ADRs/ADR-007-behavioral-moat-framing-doctrine.md
  adr_confidence: documents/ADRs/ADR-010-confidence-tag-technical-educator-rubric.md
confidence_default: 🟢 HIGH
---

# Source Checker

> **Does:** verifies a claim and tells you how solid the evidence really is.
> **Solves:** repeating something confident that turned out wrong.
> **Triggers on:** *"check this claim"* + the statement

## How Maxim does this (researcher-writer separation, structurally)

Isolates the exact claim, finds **primary sources** (web/research), and rates the evidence — **supported / mixed / unsupported / unverifiable** — citing what it found. It separates *gathering* from *asserting* (the researcher-writer split): it reports what the sources say, not what it "believes."

## Behavioral overlay

- **Frameworks (cited per ADR-007):** **CRAAP test** (Currency, Relevance, Authority, Accuracy, Purpose) · **Bayesian evidence weighting** (how much this should move your prior) · the Maxim **no-fabrication** rule.
- **Confidence tag (ADR-010)** is the whole point: the verdict *is* a confidence rating, and it names **what would change it**.
- **CSO-adjacent:** for medical/legal/financial claims, `security-analyst` is looped — it flags regulated claims rather than ruling on them.

## Output

Verdict (supported / mixed / unsupported / unverifiable) · evidence quality per source · the citations · what would change the verdict.
