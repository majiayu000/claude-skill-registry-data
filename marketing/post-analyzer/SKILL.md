---
skill_id: post-analyzer
name: Post Analyzer — why a post worked or flopped + what to change
description: "Diagnose why a social post performed — \"analyze this post\", \"why did this post flop\", \"why did this post do well\", \"what should I change\". Scores hook strength, clarity, tension and call to action."
version: 1.0.0
category: content
office: cmo
lead_agent: content-strategist
everyday_skill: true
triggers:
  - "analyze this post"
  - "why did this post flop"
  - "why did this post do well"
  - "what should I change about this post"
collaborates_with:
  - content-strategist
  - experiment-tracker    # turn the fix into a testable hypothesis
references:
  wraps_skill: .claude/skills/marketing/SKILL.md     # CRO diagnostic mode
  adr_moat_framing: documents/ADRs/ADR-007-behavioral-moat-framing-doctrine.md
  adr_confidence: documents/ADRs/ADR-010-confidence-tag-technical-educator-rubric.md
confidence_default: 🟢 HIGH
---

# Post Analyzer

> **Does:** breaks down why a post worked or didn't and tells you exactly what to change.
> **Solves:** posting blind without knowing what's actually driving results.
> **Triggers on:** *"analyze this post"* · *"why did this post flop"*

## How Maxim does this (diagnostic, not vibes)

Wraps the `marketing` CRO diagnostic discipline applied to social. Scores the post across the levers that actually move engagement — **hook strength, scannability, specificity, emotional/identity trigger, CTA clarity** — and returns the *one or two* changes with the highest expected lift, then frames them as a test via `experiment-tracker`.

## Behavioral overlay

- **Frameworks (cited per ADR-007):** **Fogg Behavior Model** (B=MAP — was the action easy + motivated + prompted?) · **AIDA** · **Hook Model** · **Peak-End** (how it opened and closed).
- **No-fabrication:** if performance metrics are supplied, the analysis uses them and cites them; if not, it says so and analyzes structure only (never invents a "why it flopped" from missing data).
- **Confidence tag (ADR-010)** — 🟡 when metrics are absent.

## Output

Diagnosis (what worked / what hurt, by lever) · the 1–2 highest-leverage changes · a testable rewrite + hypothesis.
