---
name: frontend-design
description: Sets a design direction and a quality floor before UI code, builds with design tokens and every interaction state, then checks the result with real screenshots and an independent design-reviewer. Use when building, styling or redesigning a web UI such as a page, component, form, landing page or dashboard. Not for backend work or a logic bug that happens to live in a UI file.
---

# Frontend design

**Announce at start:** "Using opm-design:frontend-design: direction, build, then a screenshot check."

`P/` below is `${CLAUDE_PLUGIN_ROOT}`. Read `P/shared/craft-floor.md` before building and cite
its rules by ID.

## Size first

- **Small** (one component, a style fix): skip step 1. Build, then run only step 3 items 1-3.
  No reviewer.
- **Anything larger:** all three steps.

## 1. Direction

1. Classify the surface as persuade, operate, read or experience. The class sets the defaults
   in `references/direction.md`.
2. If `DESIGN.md` exists, read it; its tokens are the only colours, fonts and spacing you use.
   If not, offer `/opm-design:design-system` once. On a no, continue without it and do not ask
   again.
3. Ask at most 3 intake questions with AskUserQuestion: audience, the one action that matters,
   references they like. A vague adjective ("clean and modern") gets one follow-up asking for an
   example. Never infer facts: names, numbers, customers and claims come from the user or stay
   `[placeholder]` (F-06).
4. Write the direction in 5-8 lines. Score it 1-5 on Philosophy, Hierarchy, Execution,
   Specificity, Restraint and Variety with the anchors in `references/direction.md`. Revise any
   axis under 3 before code. Never invent a weakness to look rigorous.

## 2. Build

- Colours, type, spacing and radius come from `DESIGN.md` tokens, never raw hex (F-10).
- Every control carries the 8 states in `references/interaction-states.md`.
- A redesign follows `references/redesign.md` first: inventory every link, field, handler and
  `data-testid`, choose one depth and never blend depths. An inventory item missing afterwards
  fails the redesign. Never edit a test to make it pass.
- Flutter: map the tokens with `references/flutter.md`. Visual QA is web only for now.
- A reflex rule (R-*) kept on purpose needs a waiver line in the craft-floor format.

## 3. Check

1. Self-check every floor rule, F-01 to F-10, against your diff.
2. Run visual QA as `references/visual-qa.md` says:
   `node P/skills/frontend-design/scripts/visual-qa.mjs <url-or-file> <out-dir>`. The out-dir is
   in the scratchpad or OS temp, never the repo. Exit code 2 means ask the user before
   `--install`.
3. Read every screenshot the report lists and fix what you see.
4. Write the diff to `<out-dir>/change.diff`, then dispatch `opm-design:design-reviewer` with
   only: that diff path, the `DESIGN.md` path or "none", the screenshot paths and the
   `visual-qa.json` path. Never your reasoning.
5. Act on the verdict: `ship` ends the step; `fix` means fix the findings and repeat 2-4;
   `rebuild` goes back to step 1; `recapture` means rerun visual QA, then the reviewer.

Report the verdict, the visual-QA `summary` line and a `Design waivers` section (or "none").

## Red flags

| Thought | Reality |
|---|---|
| "The page looks fine in my head" | Run visual QA and Read the screenshots. |
| "Tools are missing, I'll call it passed" | Missing tools means manual mode, reported as such. |
| "This waiver reason is obvious" | Write it down with evidence, or fix the reflex. |
| "I'll put a realistic stat here" | F-06: placeholder, never an invented fact. |
| "The redesign dropped a link but looks better" | The redesign inventory fails it. |
