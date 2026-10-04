---
name: ai-capability-pattern-matching
description: "Uses a ready-made, research-based library of 13 AI capability patterns (see ../../references/ai-capability-pattern-library.md) to pose diagnostic questions to a new client/industry, to assemble a raw list of AI opportunity candidates — an alternative or complement to task-level decomposition."
---

# AI Capability Pattern Matching

## Purpose

Produces a raw list of AI opportunity candidates **top-down,
hypothesis-driven**, using a ready-made capability pattern library — as a
counterweight to the **bottom-up, data-driven** approach of
`../task-level-decomposition-and-automation-fit/SKILL.md` (process/task
mining one task at a time). The two are complementary:

- **Bottom-up** (task-level-decomposition): works through an existing
  process/role one task at a time and classifies each one. Strong when
  the process is already precisely described, but won't surface
  opportunities that would only emerge from *redesigning* the process.
- **Top-down** (this skill): poses the client the diagnostic questions
  of 13 patterns before the process has been precisely described.
  Faster first-pass mapping, surfaces opportunities the client wouldn't
  have named themselves ("we hadn't thought about it that way"), but
  requires validation (point 4) before a candidate goes to scoring.

Use this skill especially at the **start** of a discovery workshop/
interview, before detailed process description has been done — and use
`../task-level-decomposition-and-automation-fit/SKILL.md` afterward, once
a specific process has been selected for closer examination.

## Anchored in research

- `../../references/ai-capability-pattern-library.md` — 13 patterns,
  abstracted from 81 verified use cases in a broad industry report
  (2026) and cross-checked against a second, independent AI use-case
  digest (63 cases, 16 functions).
- `../../../opportunity-recognition/skills/pattern-and-analogy-connector/SKILL.md`
  — the general Capability Pattern Mapping abstraction method, of
  which the pattern library is the concrete AI application.

## Method

1. **Before the meeting: select the 4–6 most relevant patterns** from
   the pattern library based on the client's industry/situation (not
   all 13 at once — too many questions at once drowns the
   conversation). Use the source material's industry-specific function
   weighting as a rough guide (e.g. manufacturing → patterns 4, 5, 6,
   11; professional services → patterns 2, 3, 9).
2. **Pose each selected pattern's diagnostic question to the client as
   written**, don't turn it into something more technical or AI-jargon
   heavy. The questions are deliberately phrased in business language,
   not technology language (e.g. "where does a highly paid expert have
   to search for anomalies..." not "could an LLM read documents...").
3. **Log every "yes, we have a situation like that" answer as a
   structured candidate:** pattern name, the client's own description
   of the situation, who does the work today, estimated volume/
   frequency (if known). Don't score it yet at this stage — that
   happens in point 5.
4. **Validate every candidate before further processing, with three
   checks:**
   - Is the situation genuinely recurring/high enough volume to be an
     opportunity, or a one-off exception case?
   - Does the pattern's assumed AI type (Agentic/Physical/other) match
     the organization's current maturity level, or is there a gap risk
     (e.g. a Physical AI pattern in an organization with no sensor
     data at all)?
   - Is there an obvious reason why this would NOT work in this
     particular context (regulation, union agreement, safety
     criticality)? If so, flag it visibly, don't hide it.
5. **Move validated candidates into `../ai-opportunity-portfolio/SKILL.md`**
   for 5D scoring and 2x2 prioritization — this skill only produces
   the raw list, it doesn't prioritize.
6. **If the client doesn't recognize any pattern as their own**, that's
   information in itself: either the organization is already highly
   automated in these areas, or the conversation hasn't reached the
   right level in the organization (try a different role/team) — don't
   force a fit.

## What this skill does NOT do

- Doesn't replace `../task-level-decomposition-and-automation-fit/SKILL.md`
  — it produces a fast, hypothesis-driven raw list, not a precise
  task-level classification. It's worth using both in the same
  engagement, at different stages.
- Doesn't score or prioritize candidates — that's
  `../ai-opportunity-portfolio/SKILL.md`'s job.
- Doesn't claim that all 13 patterns fit every client — some patterns
  are clearly more industry-specific (e.g. the Physical AI patterns)
  than others.
- Doesn't expand the pattern library's examples with details that
  aren't in `../../references/ai-capability-pattern-library.md` — if
  you need a deeper example, refer to the original sources rather than
  filling in from memory.
- Isn't an exhaustive listing of every possible AI opportunity — the
  13 patterns are a curated sample, not a comprehensive taxonomy. New
  patterns will be found over time; add them to the library using the
  same method (see the final section of
  `../../references/ai-capability-pattern-library.md`).

## Refinement notes

The pattern library is built on a research basis (from two independent
industry AI use-case reports). Areas to keep deepening with real practice:

- your own observations on which patterns resonate most often with
  which types of clients
- new patterns you've identified yourself but that aren't in the
  sources — add them to
  `../../references/ai-capability-pattern-library.md` in the same
  format
- a concrete workshop template/question sheet (into `../../references/`)

Once this section is filled in and validated in practice, update the
`maturity` field in `skills_index.json` to `draft`, `validated`, or
`canonical` (see `../../../meta/maturity_levels.md`). **Don't add new
fields to the frontmatter** — `name` and `description` are the only
ones allowed (see `../../../meta/frontmatter_schema.md`).

## Continue from here

- Before this (the general method): `../../../opportunity-recognition/skills/pattern-and-analogy-connector/SKILL.md`
- A parallel, bottom-up approach: `../task-level-decomposition-and-automation-fit/SKILL.md`
- Next in this pack: `../ai-opportunity-portfolio/SKILL.md` —
  scores and prioritizes the validated candidates this skill produces.
- If the whole process is run as a paid engagement:
  `../ai-discovery-engagement-design/SKILL.md`
- A ready-made skill chain for this situation: see `../../../playbooks/`
- This pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../references/ai-capability-pattern-library.md` — the library of
  13 patterns with examples
- `../../references/` — the pack's shared background material
- `../../CLAUDE.md` — the pack's shared guardrails
