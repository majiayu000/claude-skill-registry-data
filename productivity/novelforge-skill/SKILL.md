---
name: novelforge
description: Create, continue, revise, audit, and manage long-form fiction projects with explicit canon, outlines, chapter context, continuity checks, style controls, version precedence, and handoff packages. Use for novels, serialized web fiction, story bibles, chapter drafting, plot repair, or cross-session continuation; do not use for isolated non-fiction or generic copywriting.
---

# NovelForge

Treat every novel as a stateful project, not a sequence of unrelated prompts. Preserve the author's explicit choices and confirmed prose. Never silently replace canon, invent missing prior events, or present an outline as a full chapter.

## Route the request

Read only the references needed for the current operation:

- New idea, positioning, or project: [project-workflow.md](references/project-workflow.md)
- Worldbuilding, characters, powers, items, or factions: [story-bible.md](references/story-bible.md)
- Synopsis, volume, arc, event, chapter, or scene planning: [planning.md](references/planning.md)
- Drafting or continuing prose: [chapter-writing.md](references/chapter-writing.md)
- Revising, splitting, merging, renaming, or rewriting: [revision.md](references/revision.md)
- Logic, timeline, canon, knowledge, clue, prop, or foreshadowing audit: [continuity.md](references/continuity.md)
- Voice, dialogue, pacing, payoff, or AI-tell cleanup: [style-and-pacing.md](references/style-and-pacing.md)
- Serialization, feedback, analytics, trend adaptation, export, or handoff: [serialization-and-handoff.md](references/serialization-and-handoff.md)
- Project file fields or machine-readable formats: [project-schema.md](references/project-schema.md)
- Genre-specific decisions: read only the matching file under `references/genre-presets/`.

## Establish authority before writing

For an existing project, resolve the project root and read, when present: `canon.yaml`, `constraints.md`, `change-log.yaml`, relevant story-bible records, the current plan, the previous chapter, recent summaries, and relevant open threads.

Use this precedence:

1. current explicit user instruction
2. latest active canon entry
3. user-confirmed manuscript
4. latest accepted handoff
5. current outline
6. superseded material
7. inference

When sources conflict, report the exact conflict and proposed authority. Use a clearly newer explicit rule when provenance is sufficient; otherwise ask one focused question. Never blend incompatible versions.

## Operating invariants

- Distinguish fact, plan, option, inference, and superseded material.
- Do not promote brainstorming into canon without acceptance.
- Preserve locked text and out-of-scope content during revisions.
- Track character knowledge separately from reader knowledge.
- Give important reversals a cause, setup, mechanism, consequence, and aftermath.
- Record new canon after accepted prose, not before.
- Keep projects isolated; never import names or rules from another novel unless asked.
- For real-world incidents, separate verified facts from allegations and fictionalize identifiable details when adapting them.
- Do not imitate a living author's distinctive style. Translate style requests into high-level traits.

## Default execution loop

1. Classify the request and load the minimum relevant project context.
2. State only blocking conflicts or assumptions; do not re-interview the author about known facts.
3. Make an internal task card with continuity inputs, required beats, protected material, target length, and stopping point.
4. Produce the requested deliverable at the requested completeness.
5. Run deterministic checks when project files are available: `python scripts/novelforge.py validate PROJECT`, `audit PROJECT`, or `context PROJECT --chapter N`.
6. Perform the relevant literary audit.
7. Show material uncertainty instead of hiding it.
8. Update project state only when the user requested file changes or accepted the generated material.

## Output contract

- If asked for a full chapter, deliver complete prose within the target range, not notes or a compressed substitute.
- If asked for alternatives, keep them non-canon until selected.
- If asked for an audit, lead with concrete issues and evidence, then propose minimal repairs.
- If asked for a local modification, identify `must_change`, `may_adjust`, and `protected` scope before editing.
- If no files exist and the request is small, work in chat; do not force project scaffolding.
