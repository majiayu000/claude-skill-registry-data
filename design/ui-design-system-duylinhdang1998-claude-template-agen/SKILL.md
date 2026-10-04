---
name: ui-design-system
description: The single design-system skill — the token contract format, the searchable design library (50 styles, 97 palettes, 57 font pairings, 99 UX guidelines, per-stack patterns for React/Next/Vue/Svelte/SwiftUI/Compose/Flutter/Tailwind/shadcn), and the one token generator. Use when authoring or consuming a project design system, choosing a visual direction, picking palettes/typography, generating design tokens, or looking up stack-specific UI patterns. Replaces the former ui-ux-pro-max skill; that name no longer exists.
---

# UI Design System

The one place a design system is authored, looked up, and consumed. Two things live here,
and confusing them is what this skill exists to prevent:

| | What it is | Who touches it |
|---|---|---|
| **The contract** | `.project/design-system.md` — THIS project's tokens, the binding artifact | **authored by `apple-ux-wireframer` only**; every other agent consumes it |
| **The library** | `data/*.csv` — 763 rows of styles, palettes, font pairings, UX guidelines, stack patterns | anyone, read-only, via `search.py` |

---

## ⛔ Who may author the contract

**`apple-ux-wireframer` is the only agent that generates `.project/design-system.md`.**
Every other agent — frontend, iOS, Android, reviewer — **consumes** it and may not regenerate,
extend, or run a competing generator.

Two agents generating tokens produces two palettes for one product, and the second one wins
by being written last. If `.project/design-system.md` is missing when you need it, that is a
**PM escalation**, not a licence to generate your own:

```
STOP → report to PM: "no design system exists for this project"
       PM either spawns apple-ux-wireframer, or confirms the project runs without one.
```

The **format** the contract must follow is `.claude/templates/design-system.md`, and the
craft rules it is graded by are `helpers/ui-visual-standards.md` §4. Neither lives in this
skill — this skill supplies the raw material, not the standard.

---

## The library — look it up, never guess it

```bash
S=.claude/skills/ui-design-system/scripts

python3 $S/search.py "<query>" --domain style     # 50 visual directions
python3 $S/search.py "<query>" --domain ux        # 99 UX guidelines + anti-patterns
python3 $S/search.py "<query>" --domain color     # 97 palettes
python3 $S/search.py "<query>" --stack react      # per-stack patterns
```

**Loading this skill and not querying it changes nothing.** The rules are rows in a CSV, not
prose in this file — an agent that loads the skill and writes from memory has used none of
it. If you referenced this skill in `skills_used:`, you should have a query to show for it.

Available stacks (`--stack`): `react` · `nextjs` · `vue` · `nuxtjs` · `nuxt-ui` · `svelte` ·
`react-native` · `flutter` · `swiftui` · `shadcn` · `html-tailwind`.

**Match the stack to `tech-stack.md`.** A React pattern row is not advice for a SwiftUI
target; querying the wrong stack is how a design system ends up in the wrong dialect
(see `apple-ux-wireframer` Phase 0.0).

---

## Generating the contract (wireframer only, Phase 0.2)

```bash
S=.claude/skills/ui-design-system/scripts

# a concrete, palette-consistent starting set for the chosen direction
python3 $S/design_system.py "<product + chosen style>" --project-name "<name>" --format markdown

# then refine against the library
python3 $S/search.py "<style>" --domain style
```

**The generator's output is a STARTING POINT, not the deliverable.** Its output is
web-shaped; translating it into the target platform's dialect, filling every token with a
concrete value, and adding the Layout-Intent-supporting sections is the wireframer's job.

Then compile and verify — a design system that only exists as markdown cannot be enforced:

```bash
node .claude/scripts/build-styles-json.js --check --emit-css   # MUST exit 0
```

`--check` fails on any unfilled placeholder or empty token group. Do not hand over a design
system until it exits 0.

---

## Consuming the contract (every UI specialist)

`.project/design-system.md` is **auto-injected into your context at spawn** — you do not need
to go read it, and you must not work around it:

- Use its tokens only. A write bypassing them is **blocked** (`enforce-design-tokens.sh`,
  C1–C4 — see `helpers/ui-visual-standards.md` §2).
- A value you need that does not exist is a **design-system change**: ask the PM to add the
  token and regenerate. Never relocate a literal to a file the checker does not read.
- The base primitives were built in the Sprint 0 Foundation Batch — **compose them, do not
  re-implement them** (`helpers/pm-foundation-sprint.md`).

---

## Related

| For | Read |
|---|---|
| The contract's required format | `.claude/templates/design-system.md` |
| Token pipeline, C1–C4, render loop, craft rubric | `helpers/ui-visual-standards.md` |
| Wireframe authority + Layout Intent | `helpers/ux-wireframe-standards.md` |
| The year's curated directions (what the user picks from) | `helpers/design-trends.md` |
| Anti-templated taste for marketing surfaces | `design-taste-frontend` skill |
