---
name: wireframe
description: >
  Turn a planned feature into a low-fidelity screen spec before building UI: ASCII layout per
  screen and state, components to reuse, and interactions. Use after plan-feature when the plan
  has UI scope, or when the user says "wireframe", "design the screen", "what should this page
  look like", or "define the UI".
argument-hint: "[issue number]"
---

# wireframe

Answers one question: **what does the user see and do?** Architecture and data flow stay in the
plan. Read the project's `CLAUDE.md` **Skill settings** first: where the spec goes and the **UI
target** (device, viewport, usage conditions) are there.

## 1. Find the plan

Load the plan for the issue (from where Skill settings says plans go). If the plan has no UI
scope, say so in one line and stop. If there is no plan, ask whether to run `plan-feature`
first or wireframe from the issue alone.

If a wireframe for this issue already exists, only fill the screens that are missing or
skeletal.

## 2. Look at what exists

Read the 1–3 closest existing views and the shared components/styles they use. The new screen
should look like it belongs to the app. List components to reuse; mark anything new as
"new component".

## 3. Ask about real choices only

Skip this step when the screen just follows an existing pattern. Otherwise at most 2 rounds of
`AskUserQuestion`, 2–3 options each with an ASCII preview, recommended option first. Typical
questions: information hierarchy (what is biggest), page vs sheet vs dialog, where the primary
action sits, what the empty state shows.

## 4. Write the spec

For each screen:

```markdown
### <Screen name> (<route or entry point>)

<ASCII wireframe at the target viewport width; one per meaningful state>

States: default / empty / loading / error / <feature-specific, e.g. paused, GPS lost>
Components: <reused: Name (path)> · <new: Name, one-line purpose>
Interactions:
- <trigger> → <result> (<which plan acceptance criterion this serves>)
```

Then one short **Open questions** list, if any. Keep it to what someone building or checking the
screen needs. Store it where Skill settings says.

## 5. Self-check before handing over

- Every acceptance criterion that a user can see maps to a screen or interaction.
- Every screen has its empty, loading and error states, or says why one can't happen.
- The UI target's conditions are met (e.g. touch target size, glanceability, dark mode).
- Reused components exist (grep them).

Fix gaps, then show the user the result in a few lines and offer to start implementing.
Only build an HTML mockup if the user asks for one; ASCII is enough to agree on layout.
