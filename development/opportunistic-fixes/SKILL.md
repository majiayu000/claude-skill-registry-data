---
name: opportunistic-fixes
description: Use when noticing an incidental correctness problem - a stale comment, a wrong doc line, a drifted reference - in the area already being edited.
---

## The rule

While you're already working in an area, you'll spot small things that are wrong but aren't your task. A comment that describes old behavior, a doc line that drifted from the code. Don't silently ignore them, and don't silently fix them either: point them out, ask if the fix belongs in this change, and only then do it, staying inside the area you're already in. This is not a license to go hunting for unrelated refactors — it's a refusal to leave a known-wrong thing behind without saying so.

## Fires when

You're editing a file or area for one task and notice a separate, incidental correctness problem nearby.

## How to apply

Name the thing you noticed and where it is. Ask whether to fix it as part of the current change. On a yes, fix it and say what you changed. Keep it to the area you're already touching. If the fix would pull you into unrelated code, that's a new task, not an opportunistic fix. A bug you hit in your own shared code isn't opportunistic either — that's fix-in-the-shared-layer. Check the thing is actually wrong against the code before you flag it, so you don't "correct" something that was already right.

## Worked example

You're editing a function to add a parameter. Right above it, the doc comment still says it returns a list, but the code has returned a map for two versions. You're already here, so it's cheap. Say so: "While I'm in this function, the comment above it is stale. It says list, the code returns a map. Want me to fix it in this change?" On a yes, fix it and mention it. Leaving a known-wrong comment because it wasn't the task is how a codebase rots, one ignored line at a time. Silently rewriting nearby code without asking is how a small change turns into a surprise diff the user didn't want. Surfacing it first avoids both.

## Red flags

| Thought | Reality |
|---|---|
| "Not my task, leave it" | A known-wrong line you ignore is rot you chose to keep. |
| "I'll just fix it while I'm here" (silently) | Surface it and ask first. A surprise diff erodes trust. |
| "While I'm at it, let me refactor this whole module" | That's a new task, not an opportunistic fix. Stop. |
