---
name: assumption-and-evidence-audit
description: "Extracts every load-bearing assumption behind a recommendation, traces each to its source, grades the strength of the evidence, and ranks the gaps by leverage times weakness. Use before a business case, analysis, or recommendation is locked in, to see which unverified claims could actually change the conclusion if they turned out false."
---

# Assumption & Evidence Audit

## Purpose

Tests assumptions and identifies evidence gaps before a recommendation is locked in.

## Anchored in research

- 45ck — assumption-extractor / evidence-gap-review
- WEF Future of Jobs 2025 — analytical thinking #1

## Method

1. **Extract every load-bearing assumption from the analysis or
   recommendation** — not just the numeric ones. An assumption is
   load-bearing if the conclusion would change had it gone the other way;
   test this by asking "what if this were false?" for each claim.
2. **Trace each assumption to its source:** a cited fact, a
   stakeholder-provided figure, an inference from other data, or an unstated
   guess. Anything without a traceable source gets flagged
   `[assumption — verify]`, regardless of how confident it sounds.
3. **Grade the evidence behind each sourced assumption on strength, not just
   presence** — a single anecdote, a small sample, an internal estimate, and
   a validated external benchmark are not the same tier of evidence, and the
   grade should say so explicitly.
4. **Rank the assumption list by leverage (how much the conclusion depends on
   it) × evidence weakness** — this is the analytical-thinking discipline the
   WEF's 2025 Future of Jobs report ranks as the top core skill: identifying
   which unverified claims actually matter, rather than treating every gap
   as equally important.
5. **For each high-leverage, low-evidence assumption, specify exactly what
   evidence would resolve it and how hard it would be to obtain** — not just
   that it's missing.
6. **Produce a gap list ordered by priority, separate from the analysis
   itself**, so a reviewer can see at a glance which unresolved assumptions
   should block sign-off versus which can proceed with the risk noted.

## What this skill does NOT do

- Doesn't make the final decision for you — it produces a structured draft to
  support a human decision.
- Doesn't confirm figures, market data, or competitor data from memory — it
  uses the inputs you provide, or marks an assumption clearly
  (`[assumption — verify]`).
- Doesn't produce new evidence — it reveals what evidence is missing and what
  needs to be obtained.

## Refinement notes

Areas to keep deepening with real practice:

- your own rules of thumb and heuristics for this technique
- concrete templates (into [`../../references/`](../../references/))
- reference cases / your own examples
- what this skill deliberately does *not* do (guardrails, common mistakes) —
  add to the list above

This is an internal working note, not a claim about the skill's current
usability. Track depth privately via the `maturity` field in
`skills_index.json` (see
[`../../../meta/maturity_levels.md`](../../../meta/maturity_levels.md)).
**Don't add new fields to the frontmatter** — `name` and `description` are
the only ones allowed (see
[`../../../meta/frontmatter_schema.md`](../../../meta/frontmatter_schema.md)).

## Continue from here

- Next in this pack: [`../business-case-builder/SKILL.md`](../business-case-builder/SKILL.md) — Builds a full business case: problem, solution, economics (ROI/NPV/IRR), risks, timeline, stakeholders, recommendation.
- A ready-made skill chain for this situation: see [`../../../playbooks/`](../../../playbooks/)
- This pack's shared guardrails: [`../../CLAUDE.md`](../../CLAUDE.md)

## References

- [`../../references/`](../../references/) — the pack's shared background material
- [`../../CLAUDE.md`](../../CLAUDE.md) — the pack's shared guardrails
