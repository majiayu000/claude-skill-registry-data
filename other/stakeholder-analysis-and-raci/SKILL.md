---
name: stakeholder-analysis-and-raci
description: "Maps every stakeholder or stakeholder group on a power/interest grid, assigns RACI roles per activity with exactly one Accountable each, and cross-checks the map against the RACI for gaps. Use when an initiative needs clarity on who to engage, how intensively, and who is actually accountable for each deliverable."
---

# Stakeholder Analysis & RACI

## Purpose

Maps stakeholders on a power/interest matrix and assigns responsibilities with RACI.

## Anchored in research

- BABOK — stakeholder analysis
- 45ck — raci-matrix / power-interest-grid

## Method

1. **List every stakeholder or stakeholder group touched by the
   initiative** — BABOK's categories are a useful checklist: sponsor, domain
   SME, end user, operational support, supplier, regulator. Don't stop at the
   obvious names already in the room.
2. **Score each stakeholder on power** (ability to affect the outcome) **and
   interest** (how much the outcome affects them), **and place them on the
   resulting 2×2 grid** (Mendelow's power/interest matrix): manage closely
   (high power/high interest), keep satisfied (high power/low interest),
   keep informed (low power/high interest), monitor (low power/low
   interest). The quadrant — not a general impression — determines how much
   engagement effort each stakeholder gets.
3. **For each in-scope activity or deliverable, assign RACI roles** — exactly
   one Accountable per item (never zero, never more than one), any number of
   Responsible, Consulted, and Informed. A RACI with two Accountables, or an
   item with none, is a design flaw to fix before publishing, not a detail to
   gloss over.
4. **Cross-check the RACI against the power/interest grid:** a "manage
   closely" stakeholder who isn't Accountable or Consulted for anything is a
   signal that something's missing.
5. **Flag any stakeholder position that's inferred rather than confirmed**
   (`[assumption — verify]`) — stakeholder maps built on the analyst's guess
   about who actually holds power are a common source of failed buy-in.
6. **Revisit the map at key milestones** — power and interest shift as a
   project moves from planning to delivery, and a map validated once at
   kickoff goes stale.

## What this skill does NOT do

- Doesn't make the final decision for you — it produces a structured draft to
  support a human decision.
- Doesn't confirm figures, market data, or competitor data from memory — it
  uses the inputs you provide, or marks an assumption clearly
  (`[assumption — verify]`).
- Doesn't identify an organization's stakeholders for you without you naming
  the real actors involved.

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

- Next in this pack: [`../assumption-and-evidence-audit/SKILL.md`](../assumption-and-evidence-audit/SKILL.md) — Tests assumptions and identifies evidence gaps before a recommendation is locked in.
- For a public-sector, municipal, or non-profit client: extend this
  method with
  [`../../../specialisation-packs/public-sector-ai-service-design/skills/ps-stakeholder-and-political-landscape-mapping/SKILL.md`](../../../specialisation-packs/public-sector-ai-service-design/skills/ps-stakeholder-and-political-landscape-mapping/SKILL.md)
  — public-sector stakeholders split across distinct actor types
  (elected officials, civil servants, unions, oversight bodies) with
  different veto points that a generic power/interest grid doesn't
  distinguish on its own.
- A ready-made skill chain for this situation: see [`../../../playbooks/`](../../../playbooks/)
- This pack's shared guardrails: [`../../CLAUDE.md`](../../CLAUDE.md)

## References

- [`../../references/`](../../references/) — the pack's shared background material
- [`../../CLAUDE.md`](../../CLAUDE.md) — the pack's shared guardrails
