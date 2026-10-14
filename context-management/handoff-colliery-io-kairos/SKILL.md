---
name: handoff
description: Bring active Kairos items current, then compact this conversation's leftover context into a short note for the next session.
argument-hint: "What will the next session be used for?"
disable-model-invocation: true
---

Kairos is the persistent memory: durable state — findings, decisions, progress, blockers — belongs on the work items, where any teammate or agent reads it. First bring the active items current (`edit_item`, `transition_item` if a column changed) so the boards tell the true story.

Only then compact what remains — context this conversation alone holds: dead ends already ruled out, in-flight reasoning, environment quirks, the intended next move. Open the note with the short codes the next session should `get_item` first; the note is read alongside the board state, never instead of it. Save it as `kairos-handoff-<workspace-name>.md` in the OS temporary directory (not the workspace), replacing any previous note for this workspace, and finish by telling the user its absolute path. If nothing remains once the items are current, say so and skip the note.

Reference other artifacts (items, commits, diffs, files) by short code or path rather than restating them. Redact secrets. If the user passed arguments, treat them as what the next session will focus on and tailor the note to it.
