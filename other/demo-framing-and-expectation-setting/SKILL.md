---
name: demo-framing-and-expectation-setting
description: "Frames a demo/prototype/PoC for the customer before presenting it with the right term (PoC vs. Pilot vs. MVP) and the right promise — what this demo PROVES, what it does NOT prove, and what happens next if it succeeds. Use before every demo or PoC presentation, especially when there's a risk the customer will over-interpret the demo as production-ready or as automatically progressing to production."
---

# Demo Framing & Expectation Setting

## Purpose

Prevent the most common, expensive-to-fix mistake in demo delivery: **the
wrong frame before the first slide.** If a customer walks out of a demo
believing a production-ready solution is three weeks away, and reality is
six months of development work, the problem isn't the quality of the demo —
the problem is that no one framed the demo correctly before it started. This
skill produces that frame: what term correctly describes what's being shown
today, what this demo proves and what it does NOT prove, and what
concretely happens next if the demo succeeds.

This is a **different question** than
[`../../../ai-strategy-and-governance/skills/ai-use-case-feasibility-and-poc-scoping/SKILL.md`](../../../ai-strategy-and-governance/skills/ai-use-case-feasibility-and-poc-scoping/SKILL.md),
which defines a PoC's TECHNICAL boundaries (what data, what success
criteria, what scope limits). This skill answers the **customer
communication** question: how is that same PoC framed in conversation so
that no false expectations are created. Use both together — technical
scoping first, then this communication frame.

## Anchored in research

- The PoC / Pilot / MVP distinction (synthesis of multiple 2026 sources, see
  References): three different stages that answer three different types of
  uncertainty (technical feasibility / operational fit / product
  development direction).
- "Pilot purgatory" research (McKinsey, BCG, IDC, MIT syntheses, see
  References): a large share of enterprise AI pilots never reach
  production, and the bottleneck is typically operational (management
  commitment, workflow redesign, scale-up investment) — not the technical
  success or failure of the demo/PoC stage.

## Method

1. **Name precisely what's being shown today, with the right term, and
   don't use the terms as synonyms** (see the pack's
   [`../../CLAUDE.md`](../../CLAUDE.md)):
   - **PoC**, if the question is "does this work technically with
     representative data" — no real users yet, no production load.
   - **Pilot**, if the question is "does this work with real people and
     real operational conditions" — technical feasibility has already been
     demonstrated.
   - **MVP**, if the question is "what should be built next, based on real
     user feedback" — a product-development stance, not a proof stage.
   If you're not sure which, ask yourself: "which ONE uncertainty does this
   answer today?" If there's more than one answer, you're probably merging
   stages — separate them.
2. **Write a one-sentence "proves/doesn't prove" pair before the demo:**
   - "This demo proves that ___ [a precise, narrow claim, e.g. 'the model
     extracted the supplier business ID from 20/20 test invoices']."
   - "This demo does NOT prove that ___ [anything outside the test scope,
     e.g. 'it works with all invoice formats', 'it's secure for
     production use', 'it scales to 10,000 invoices a month']."
   Present both to the customer before the demo, not only if someone asks.
3. **Tie the frame back to the technical scoping done in
   [`../../../ai-strategy-and-governance/skills/ai-use-case-feasibility-and-poc-scoping/SKILL.md`](../../../ai-strategy-and-governance/skills/ai-use-case-feasibility-and-poc-scoping/SKILL.md)**
   if that's already been done — use the same success criteria, don't
   invent new ones at demo time.
4. **State up front what concretely happens NEXT if the demo succeeds** —
   who decides, on what timeline, what resources the pilot/production
   stage would require. This is a direct countermeasure against "pilot
   purgatory" risk: if no one has agreed in advance what a successful demo
   leads to, it leads to nothing, regardless of the demo's quality.
5. **State out loud what the demo does NOT yet resolve organizationally** —
   workflow change, user training, management commitment, budget for
   full scale. Technical success in the demo doesn't mean these are solved.
6. **Choose the tone of the frame based on the audience:** for a technical
   audience you can emphasize accuracy figures and limitations directly;
   for an executive audience, route the frame through
   [`../../../change-and-communication/skills/executive-narrative-and-storyline/SKILL.md`](../../../change-and-communication/skills/executive-narrative-and-storyline/SKILL.md)
   before the demo, so the technical "proves/doesn't prove" pair translates
   into business language.
7. **Document the frame in writing before the demo** (one paragraph is
   enough) and share it with participants — this reduces the risk that
   the post-demo memory drifts (people forget most of a demo's content
   quickly, but a written frame stays).

## What this skill does NOT do

- Doesn't do the PoC's technical scoping — that's the job of
  [`../../../ai-strategy-and-governance/skills/ai-use-case-feasibility-and-poc-scoping/SKILL.md`](../../../ai-strategy-and-governance/skills/ai-use-case-feasibility-and-poc-scoping/SKILL.md).
  This skill frames that same scoping for customer communication.
- Doesn't build the demo or prototype itself — use
  [`../rapid-prototype-and-vibe-coding-craft/SKILL.md`](../rapid-prototype-and-vibe-coding-craft/SKILL.md)
  before this.
- Doesn't guarantee that the right frame alone prevents "pilot purgatory"
  — it reduces the risk of misunderstanding, but progressing to production
  always requires organizational decisions outside this skill's scope.
- Doesn't calculate ROI or build a business case — see
  [`../demo-to-business-case-bridge/SKILL.md`](../demo-to-business-case-bridge/SKILL.md).

## Refinement notes

Areas to keep deepening with real practice:

- your own examples of how you've framed a demo successfully (or
  unsuccessfully) with a specific customer
- your own standard-phrase/slide template for the "proves/doesn't prove"
  pair (into [`../../references/`](../../references/))
- rules of thumb for when a customer typically over-interprets a demo —
  which signals predict this

This is an internal working note, not a claim about the skill's current
usability. Track depth privately via the `maturity` field in
`skills_index.json` (see
[`../../../meta/maturity_levels.md`](../../../meta/maturity_levels.md)).
**Don't add new fields to the frontmatter** — `name` and `description` are
the only ones allowed (see
[`../../../meta/frontmatter_schema.md`](../../../meta/frontmatter_schema.md)).

## Continue from here

- Before this (prototyping): [`../rapid-prototype-and-vibe-coding-craft/SKILL.md`](../rapid-prototype-and-vibe-coding-craft/SKILL.md)
- Before this (technical scoping): [`../../../ai-strategy-and-governance/skills/ai-use-case-feasibility-and-poc-scoping/SKILL.md`](../../../ai-strategy-and-governance/skills/ai-use-case-feasibility-and-poc-scoping/SKILL.md)
- Next in this pack: [`../demo-delivery-and-storytelling/SKILL.md`](../demo-delivery-and-storytelling/SKILL.md)
- For an executive audience: [`../../../change-and-communication/skills/executive-narrative-and-storyline/SKILL.md`](../../../change-and-communication/skills/executive-narrative-and-storyline/SKILL.md)
- If the demo succeeds and the next step is a business case:
  [`../demo-to-business-case-bridge/SKILL.md`](../demo-to-business-case-bridge/SKILL.md)
- A ready-made skill chain for this situation: see [`../../../playbooks/`](../../../playbooks/)
- This pack's shared guardrails: [`../../CLAUDE.md`](../../CLAUDE.md)

## References

- The PoC vs. Pilot vs. MVP distinction — synthesis of multiple 2026
  sources on the staging of enterprise AI projects
- "Pilot purgatory" research — McKinsey/BCG/IDC/MIT syntheses on why a
  large share of AI pilots never reach production
- [`../../references/`](../../references/) — the pack's shared background material
- [`../../CLAUDE.md`](../../CLAUDE.md) — the pack's shared guardrails
