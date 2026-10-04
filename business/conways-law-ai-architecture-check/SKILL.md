---
name: conways-law-ai-architecture-check
description: "Diagnoses whether an organization's communication structure will get mirrored in whatever AI system it builds — fragmented teams produce fragmented, siloed AI tools with no shared capability — and applies the resequencing rule: decide on org structure before building the AI architecture, not after."
---

# Conway's Law AI Architecture Check

## Purpose

Melvin Conway's 1967 observation — organizations design systems that
mirror their own communication structure — applies to AI systems with
unusual force, because AI value depends on data and capability flowing
freely across whatever boundaries already exist. A company that builds
AI on top of its existing silos, without addressing this first, doesn't
get an AI-native business; it gets several disconnected AI tools, one
per silo, that reflect and often amplify the fragmentation that was
already there. Use this check early in any significant AI initiative —
before the technical architecture is designed, not after.

## Anchored in research

Conway's Law itself (Melvin Conway, 1967) is a well-established,
uncontested base concept. Its extension to AI specifically is an
active, independently-arrived-at 2026 discourse theme across multiple
unrelated sources making the same point: organizations tend to design
systems that mirror their own communication structures, and AI systems
make this reflection louder, faster, and harder to ignore. A commonly
cited supporting data point: AI projects fail at roughly twice the rate
of non-AI technology projects (RAND Corporation research), with
miscommunication about a project's intent and purpose cited as the most
frequent cause — directly consistent with a structural, not
technical, root cause.

## Method

1. **Map the current communication structure**, not the org chart —
   who actually talks to whom regularly, who shares data and tooling
   decisions, and where the real boundaries sit (these often don't
   match the formal reporting lines).
2. **Predict the AI architecture this structure will produce if nothing
   changes.** The common failure pattern to check for explicitly: each
   team buys or builds its own AI tool independently — marketing runs
   one assistant, sales another, operations a third — each reflecting
   the data, language, and assumptions of the team that built it, with
   no shared capability visible anywhere in the organization. If the
   current initiative looks like this pattern already forming, name it
   now, before more is built on top of it.
3. **Check whether the operating model is actually ready for the
   INTENDED AI architecture**, not just whether the technology is
   ready. If the intended architecture requires data or capability to
   flow across a boundary that today's communication structure doesn't
   cross, the AI system will inherit that gap and reproduce it at
   machine speed — this is the core mechanism, not just an analogy.
4. **Apply the resequencing rule directly: decide on structure before
   building, not after.** Reorganizing communication structure,
   decision rights, or team boundaries is comparatively easy before an
   AI architecture has been built around the current structure — and
   very hard afterward, because by then the technical architecture
   has calcified around exactly the boundaries that needed to change.
   If a structural fix is needed and is being deferred "until after
   the AI project," name this explicitly as a decision with a cost, not
   a neutral sequencing choice.
5. **Use `../../../business-design-frameworks/skills/layer-based-business-structuring/SKILL.md`
   as the complementary structuring tool once this check identifies a
   genuine need to redesign boundaries** — that skill designs the
   modular layer structure and build/partner interfaces; this skill's
   job is narrower: diagnosing that the CURRENT communication structure
   will distort the AI architecture, and forcing the sequencing
   decision about when to fix it.
6. **Revisit the check at major milestones**, not just at the start —
   an organization's communication structure can shift during a
   multi-quarter AI initiative (team reorganizations, new hires, a
   department gaining or losing authority), and a structure that passed
   this check at kickoff can silently fail it by the time the system
   ships.

## What this skill does NOT do

- Doesn't redesign the organization — it diagnoses whether the current
  structure will distort the AI architecture and names the sequencing
  decision; the actual reorganization is a leadership and change-
  management decision (see `../../../change-and-communication/README.md`
  for the communication side of executing a structural change).
- Doesn't replace `layer-based-business-structuring` for designing the
  target modular structure — it identifies that a structural problem
  exists and needs resequencing, that skill designs the actual layers.
- Doesn't guarantee restructuring first will prevent every AI project
  failure — RAND's finding is that miscommunication is the MOST
  frequent cause, not the only one; this check addresses a common,
  specific failure mode, not every failure mode.

## Refinement notes

- What's a real case where this check caught a silo problem before an
  AI project calcified around it — and what happened when a client
  chose to defer the structural fix anyway?
- How do you get a client's leadership to take on a reorganization
  BEFORE the AI project, when the natural instinct is always to build
  first and fix structure later?
- Is there a lighter-weight version of this check for a smaller
  initiative, where a full communication-structure mapping (Step 1) is
  disproportionate?

## Continue from here

- Use early: before the technical architecture of a significant AI
  initiative is designed.
- Related: `../../../business-design-frameworks/skills/layer-based-business-structuring/SKILL.md`
  — designs the target modular structure once a redesign need is
  identified here.
- Related: `../ai-reshuffle-opportunity-framing/SKILL.md` — a 3rd-order
  reshuffle opportunity often requires exactly the kind of structural
  change this check is designed to surface.
- This pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../references/ai-native-reshuffle-heuristics-research.md` —
  selection and grounding notes for this skill and its siblings
- `../../references/` — the pack's shared background material
- `../../CLAUDE.md` — the pack's shared guardrails
