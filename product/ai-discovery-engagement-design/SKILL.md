---
name: ai-discovery-engagement-design
description: "Designs and productizes AI opportunity identification (the discovery phase) into a paid consulting engagement — a 4-phase engagement structure, fixed-price service products, and standardized deliverables (Portfolio, Business Case, ATOM/Readiness Scorecard, Roadmap)."
---

# AI Discovery Engagement Design

## Purpose

Helps an AI Business Designer (as an internal actor or an external
consultant) package this pack's other skills (task decomposition,
opportunity portfolio, feasibility, roadmap) into one clearly bounded,
sellable or internally justified **discovery engagement**: what phases,
how long, what's delivered, and in what product form. This is this
pack's "meta-skill" — it doesn't produce the analysis itself, it
STRUCTURES the process during which the pack's other skills are run.

## Anchored in research

- Research digest "Methods, Frameworks, and Competencies for Identifying
  AI Opportunities and Capacity in Business" (2026) — professional-
  services firms' sales and service models, productized services,
  deliverables. The model is generalized from large consulting firms'
  publicly known AI-discovery practice, not an exact copy of any single
  firm.

## Method

1. **Choose the product form based on scope.** Two typical fixed-price
   service products:
   - **AI Opportunity Sprint / Mapping (2–4 weeks)** — lighter: 2–3
     workshops, a process walkthrough, a prioritized AI roadmap. Fits
     when the client doesn't yet have a clear sense of where the AI
     opportunities are.
   - **AI Maturity & Opportunity Audit (4–6 weeks)** — deeper:
     combines opportunity identification with technical data/
     infrastructure readiness and a governance model (AI Governance).
     Fits when the client also needs an assessment of their own
     readiness, not just an opportunity list.
   Don't sell/scale either product form larger than the client
   organization's size and decision-making speed can sustain — an
   oversized discovery phase is itself a risk (analysis paralysis).
2. **Structure the engagement in four phases:**
   - **Phase 1 — Kickoff & intent.** Executive interviews, setting the
     ambition level and the AI ambition. Output: a shared
     understanding of what "success" means for this engagement.
   - **Phase 2 — Discovery workshops & task analysis.** Process and
     data audits, mapping the value chain with stakeholders. In this
     phase, use
     `../task-level-decomposition-and-automation-fit/SKILL.md` to
     produce the raw list and
     `../../../business-design-frameworks/skills/value-chain-mapping/SKILL.md`
     for process-level mapping.
   - **Phase 3 — Scoring, calculation & portfolio.** Identifying use
     cases, 5D scoring, and business-case modeling. Use
     `../ai-opportunity-portfolio/SKILL.md` and, where needed,
     `../../../business-case-and-analysis/skills/business-case-builder/SKILL.md`.
   - **Phase 4 — AI roadmap & delivery.** Prioritized AI Backlog,
     investment calculations, architecture guidance. Use
     `../ai-capability-roadmap/SKILL.md`.
3. **Define the deliverables up front, before the engagement
   starts** — the client knows exactly what they're getting:
   - **AI Opportunity Portfolio / Backlog** — a list of classified and
     scored items (see `../ai-opportunity-portfolio/SKILL.md`).
   - **Detailed Business Cases** — ROI and savings calculations,
     accounting for total cost of ownership (TCO — includes model
     inference costs and maintenance, not just build cost).
   - **AI Target Operating Model (ATOM) / Readiness Scorecard** — see
     `../ai-capability-roadmap/SKILL.md`'s "ATOM/Readiness Scorecard"
     section — a description of the human-AI division of labor and the
     organization's readiness level.
   - **Strategic AI Roadmap** — a scheduled plan across three
     horizons (see `../ai-capability-roadmap/SKILL.md`).
4. **Match the engagement's depth to the client's decision-making
   maturity.** If the client doesn't yet have an empowered
   decision-maker for the results, shorten it to the Sprint form and
   don't sell the full Audit — a full Audit without a clear
   decision-maker produces a good report that ends up on a shelf.
5. **Set a clear scope boundary (out of scope) already at the sales
   stage.** A discovery engagement does NOT include implementation,
   PoC building, or technical architecture design — these are
   separate engagements that come AFTER discovery. Mixing them leads
   to scope creep and unclear pricing.
6. **Record the engagement's success criteria before starting:** is a
   prioritized backlog delivered, is it approved by the leadership
   team, and does at least one funded investment decision result from
   it. A discovery engagement that doesn't lead to a decision has
   failed regardless of the quality of the analysis.

## What this skill does NOT do

- Doesn't do the analysis itself — it organizes the PROCESS during
  which the pack's other skills (task-level-decomposition,
  ai-opportunity-portfolio, ai-use-case-feasibility-and-poc-scoping,
  ai-capability-roadmap) produce the actual content.
- Doesn't include pricing recommendations or fixed euro amounts — they
  depend on the market, the industry, and your own cost base; always
  mark them `[assumption — verify]` if they need to be estimated.
- Doesn't replace `../../../opportunity-recognition/skills/opportunity-brief-writing/SKILL.md`
  for documenting a single opportunity — this skill operates at a
  higher level: it structures the whole engagement, not one
  opportunity.
- Doesn't fit every situation — if AI opportunities have already been
  identified and only one analysis is needed (not a whole multi-phase
  engagement), use the individual skills directly without this
  framework around them.

## Refinement notes

Areas to keep deepening with real practice:

- your own pricing models and principles (fixed-price vs. time-based,
  what's included in which product form)
- concrete sales materials/proposal templates (into
  `../../references/`)
- your own experience of when a Sprint is enough and when a full Audit
  is needed
- reference cases from your own engagements

Once this section is filled in and validated in practice, update the
`maturity` field in `skills_index.json` to `draft`, `validated`, or
`canonical` (see `../../../meta/maturity_levels.md`). **Don't add new
fields to the frontmatter** — `name` and `description` are the only
ones allowed (see `../../../meta/frontmatter_schema.md`).

## Continue from here

- Uses as sub-skills (in phase order):
  `../task-level-decomposition-and-automation-fit/SKILL.md` →
  `../ai-opportunity-portfolio/SKILL.md` →
  `../ai-use-case-feasibility-and-poc-scoping/SKILL.md` →
  `../ai-capability-roadmap/SKILL.md`
- Related skill in another pack (business case deep-dive):
  `../../../business-case-and-analysis/skills/business-case-builder/SKILL.md`
- Related skill in another pack (if the engagement concerns the public
  sector): see the `julkiset-hankinnat` plugin for tender and
  procurement procedures.
- A ready-made skill chain for this situation: see `../../../playbooks/`
- This pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../references/` — the pack's shared background material
- `../../CLAUDE.md` — the pack's shared guardrails
