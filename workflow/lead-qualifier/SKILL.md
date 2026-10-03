---
skill_id: lead-qualifier
name: Lead Qualifier — score an inbound → call or skip
description: "Qualify an inbound lead — \"is this lead worth my time\", \"qualify this lead\", \"should I take this client\". Applies MEDDIC and SPIN scoring and returns a verdict with reasoning."
version: 1.0.0
category: operational
office: cmo
lead_agent: content-strategist
everyday_skill: true
triggers:
  - "is this lead worth my time"
  - "qualify this lead"
  - "should I take this client"
collaborates_with:
  - content-strategist
  - gtm-strategist           # MEDDIC/SPIN depth (lifted from ceo-automation/sales)
references:
  lifted_from: .claude/skills/ceo-automation/sales/SKILL.md   # standalone surface over the CEO-automation sales catalog
  adr_moat_framing: documents/ADRs/ADR-007-behavioral-moat-framing-doctrine.md
  adr_confidence: documents/ADRs/ADR-010-confidence-tag-technical-educator-rubric.md
confidence_default: 🟢 HIGH
---

# Lead Qualifier

> **Does:** scores an inbound message on budget, fit, and intent, then tells you call or skip.
> **Solves:** wasting hours on people who were never going to pay.
> **Triggers on:** *"is this lead worth my time"* + the message

## How Maxim does this (standalone — no CRM scaffolding required)

Lifts the MEDDIC/SPIN qualification logic out of the CEO-automation sales catalog into a one-shot skill: paste the inbound, get a verdict. Scores **Budget · Fit · Intent · Effort** and returns **call / nurture / skip** with the reasoning and the single best next question to ask them.

## Behavioral overlay

- **Frameworks (cited per ADR-007):** **MEDDIC** (Metrics·Economic-buyer·Decision-criteria·Decision-process·Pain·Champion) · **BANT** (Budget·Authority·Need·Timeline) · **Prospect Theory** (weigh the downside of a bad-fit client, not just upside).
- **No-fabrication:** it scores only on what the message reveals; unknowns are flagged as "ask," not guessed.
- **Confidence tag (ADR-010)** on the verdict.

## Output

Score (Budget/Fit/Intent/Effort) · verdict (call / nurture / skip) · the reasoning · the one qualifying question to send back.
