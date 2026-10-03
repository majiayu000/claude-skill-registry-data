---
skill_id: company-teardown
name: Company Teardown — model, revenue signals, weak points on a template
description: "Tear down a company on request — \"do a teardown of\", \"break down this company\", \"analyze this competitor's business\". Fixed-template output: business model, how they make money, positioning, and where they are exposed."
version: 1.0.0
category: research
office: cino
lead_agent: innovation-researcher
everyday_skill: true
triggers:
  - "do a teardown of"
  - "break down this company"
  - "analyze this competitor's business"
collaborates_with:
  - innovation-researcher
  - competitive-intel-analyst   # the depth this skill exposes
references:
  lifted_from: agents/MXM/cino/competitive-intel-analyst.md   # standalone surface over the CINO analyst
  adr_moat_framing: documents/ADRs/ADR-007-behavioral-moat-framing-doctrine.md
  adr_confidence: documents/ADRs/ADR-010-confidence-tag-technical-educator-rubric.md
confidence_default: 🟡 MEDIUM
---

# Company Teardown

> **Does:** breaks down a company's model, revenue signals, and weak points on a fixed template.
> **Solves:** half a day of scattered research per target.
> **Triggers on:** *"do a teardown of [company]"*

## How Maxim does this (one named skill over the CINO analyst)

Surfaces the `competitive-intel-analyst` as a one-shot, fixed-template teardown: **business model · how they make money (revenue signals) · positioning · pricing · moat (and its source) · weak points · the opening for you**. Same template every time, so teardowns are comparable across targets.

## Behavioral overlay

- **Frameworks (cited per ADR-007):** **Porter's Five Forces** · **7 Powers** (Helmer — what kind of moat) · **Wardley Mapping** (where they sit on the value chain) · **Business Model Canvas**.
- **No-fabrication is load-bearing here:** public/verifiable facts are stated as facts with the source; anything inferred is explicitly marked **inference**, not fact. Revenue figures for private companies are flagged as estimates. This is why the default tag is **🟡 MEDIUM** — a teardown mixes verified and inferred signal, and Maxim labels which is which (the discipline a generic "research this company" prompt skips).
- **Confidence tag (ADR-010)** per section, not just overall.

## Output

A fixed-template teardown: model · revenue signals · positioning · pricing · moat + source · weak points · your opening — every claim marked fact vs. inference.
