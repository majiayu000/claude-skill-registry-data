---
name: ai-capability-roadmap
description: "Builds the organization's AI capability map and roadmap from the current state to the target state across three horizons (0-6mo efficiency, 6-18mo transformation, 18-36mo new business), plus an AI Target Operating Model (ATOM) / Readiness Scorecard describing the division of labor between humans and AI."
---

# AI Capability Roadmap

## Purpose

Builds the organization's AI capability map and a scheduled roadmap from
the current state to the target state. Answers the question "WHEN does
each prioritized AI opportunity get implemented," complementing
`../ai-opportunity-portfolio/SKILL.md`, which answers "WHAT is worth doing
and WHAT TYPE of change is it."

## Anchored in research

- Market research — roadmaps and business capability maps
- Research digest "Methods, Frameworks, and Competencies for Identifying
  AI Opportunities and Capacity in Business" (2026) — the three-horizon
  Strategic AI Roadmap and the AI Target Operating Model (ATOM) /
  Readiness Scorecard concept, part of the deliverable material of
  large consulting firms' discovery engagements.

## Method

1. **Take the prioritized portfolio as input** from
   `../ai-opportunity-portfolio/SKILL.md`: the selected items with their
   scores, Value Play classification (if transformative), and
   Deploy/Reshape/Invent class.
2. **Place every item into one of three horizons:**
   - **Horizon 1 — Efficiency (0–6 months).** Fast, low-risk items.
     Typically corresponds to the "Quick Wins" category in the
     `ai-opportunity-portfolio` skill's 2x2 matrix and often the
     "Deploy" category in the Deploy-Reshape-Invent taxonomy (rolling
     out ready-made tools).
   - **Horizon 2 — Transformation (6–18 months).** Redesign of core
     processes. Often corresponds to the "Reshape" category — requires
     organizational change, not just tool adoption.
   - **Horizon 3 — New business (18–36 months).** Transformative
     items that create new revenue. Often corresponds to the "Invent"
     category and a "Strategic Bets" position in the 2x2 matrix.
   **Note:** the horizon and the Deploy/Reshape/Invent class CORRELATE
   but aren't the same thing — the same Reshape-level opportunity can
   land in Horizon 1 OR 2 depending on resources and dependencies.
   Don't automatically copy the class as the horizon; assess timing
   separately (dependencies, resources, the organization's capacity
   for change relative to other projects already underway).
3. **Build the AI Target Operating Model (ATOM) / Readiness
   Scorecard.** Describe for every horizon or key capability area:
   - **The human-AI division of labor** — which roles/tasks are
     Automate/Augment/Human-Only (see
     `../task-level-decomposition-and-automation-fit/SKILL.md`) AT
     this stage of the roadmap, and how the division of labor changes
     as the organization moves from one horizon to the next.
   - **The organization's readiness level** by capability area (e.g.
     data architecture, governance model, staff AI literacy, change-
     management capacity) — a rough scale (low/medium/high) is enough
     at this stage, a precise maturity model isn't needed.
   - **Critical missing capabilities** that need to be built BEFORE the
     next horizon's items can start (e.g. Horizon 2 often requires a
     data pipeline that Horizon 1 didn't yet need).
4. **Identify the dependencies between horizons explicitly.** Horizon
   2 and 3 items often rest on infrastructure or organizational
   learning built in Horizon 1 — mark these dependencies on the
   roadmap, don't treat the horizons as independent of each other.
5. Produce a structured output: a horizoned roadmap (item → horizon →
   dependencies → ATOM division-of-labor description) (see
   `../../references/` once added).
6. Validate the result with stakeholders or your own experience-based
   checklist. Make sure in particular that Horizon 1 implementations
   don't require more resources than the organization can supply
   alongside Horizon 2 planning.

## What this skill does NOT do

- Doesn't make the final decision for you — it produces a structured
  draft to support a human decision.
- Doesn't confirm figures, market data, or competitor data from
  memory — it uses the inputs you provide, or marks an assumption
  clearly (`[assumption — verify]`).
- Doesn't commit budget or resources — it produces a roadmap draft for
  approval.
- Doesn't do the prioritization itself — it uses the already-
  prioritized list produced by `../ai-opportunity-portfolio/SKILL.md`
  as input, it doesn't re-assess the value of opportunities.
- Doesn't build a full organizational AI maturity model — the ATOM/
  Readiness Scorecard here is a rough, roadmap-supporting description,
  not a separate maturity audit.

## Refinement notes

Areas to keep deepening with real practice:

- your own rules of thumb and heuristics for this technique — e.g.
  how many Horizon 1 items an organization can typically run in
  parallel
- concrete templates (into `../../references/`, e.g. an ATOM/Readiness
  Scorecard template)
- reference cases / your own examples
- what this skill deliberately does *not* do (guardrails, common
  mistakes) — add to the list above

Once this section is filled in and validated in practice, update the
`maturity` field in `skills_index.json` to `draft`, `validated`, or
`canonical` (see `../../../meta/maturity_levels.md`). **Don't add new
fields to the frontmatter** — `name` and `description` are the only
ones allowed (see `../../../meta/frontmatter_schema.md`).

## Continue from here

- Preceding skill in this pack: `../ai-opportunity-portfolio/SKILL.md`
  — produces the prioritized list that this skill schedules.
- Once this step is done, move to `../../../change-and-communication/skills/stakeholder-communication-plan/SKILL.md`
- Related skill in this pack: `../ai-discovery-engagement-design/SKILL.md`
  — if the roadmap is produced as part of a larger discovery
  engagement, this skill corresponds to the engagement's Phase 4.
- A ready-made skill chain for this situation: see `../../../playbooks/`
- This pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../references/` — the pack's shared background material
- `../../CLAUDE.md` — the pack's shared guardrails
