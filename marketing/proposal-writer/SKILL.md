---
skill_id: proposal-writer
name: Proposal Writer — brief → proposal with scope, price, timeline
description: "Draft a client proposal — \"write a proposal for\", \"draft a proposal\", \"turn this brief into a proposal\". Produces executive summary, understanding of their problem, approach, scope, and pricing."
version: 1.0.0
category: operational
office: cmo
lead_agent: content-strategist
everyday_skill: true
triggers:
  - "write a proposal for"
  - "draft a proposal"
  - "turn this brief into a proposal"
collaborates_with:
  - content-strategist
  - gtm-strategist
  - nk-writer            # voice-match the prose if a voice DNA is set
references:
  lifted_from: .claude/skills/ceo-automation/sales/SKILL.md   # the "Proposal first draft" prompt, as a standalone skill
  adr_moat_framing: documents/ADRs/ADR-007-behavioral-moat-framing-doctrine.md
  adr_confidence: documents/ADRs/ADR-010-confidence-tag-technical-educator-rubric.md
confidence_default: 🟢 HIGH
---

# Proposal Writer

> **Does:** turns a short brief into a clean proposal with scope, price, and timeline.
> **Solves:** rewriting the same proposal structure for every prospect.
> **Triggers on:** *"write a proposal for [client]"*

## How Maxim does this (standalone, persuasion-structured)

Lifts the CEO-automation "Proposal first draft" into a one-shot skill. From a short brief it produces: **executive summary → understanding of their pain → proposed solution → scope → timeline → pricing → ROI → next step**. Pricing is **anchored** (good/better/best where it fits), and the prose matches your saved voice if one is set.

## Behavioral overlay

- **Frameworks (cited per ADR-007):** **Minto Pyramid** (lead with the answer) · **AIDA** · **Anchoring** (price framing) · **Cialdini** (social proof + scarcity on terms) · **Loss Aversion** (cost of inaction in the ROI section).
- **No-fabrication:** numbers/case-studies are placeholders the operator fills — never invented client results.
- **Confidence tag (ADR-010).**

## Output

A complete proposal (summary · pain · solution · scope · timeline · pricing · ROI · next step), ready to edit and send.
