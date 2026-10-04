---
name: ux-onboarding
description: This skill should be used when someone wants to get familiar with an existing project's UX/design choices and patterns — e.g. "walk me through how this app does UX", "onboard me onto the design system", "explain this project's UI patterns", "I'm new to this codebase, show me the design layer", or runs /ux-onboarding. It builds a working mental model by surveying the design layer, teaching it part by part (explaining, sending the user to read the real code, and checking comprehension with questions), then having the user reimplement a small recent UX change picked from history. Familiarization — not scaffolding (ux-foundations) or scoring (ux-audit).
version: 0.1.0
---

# UX Onboarding

Build a working mental model of **how this project does UX** — its design tokens, component patterns, accessibility conventions, interaction-feedback states, and copy voice — by being walked through the real code, not by reading a summary. This is familiarization, not scaffolding (the `ux-foundations` skill / `/ux-bootstrap`) or scoring (the `ux-audit` skill / `/ux-audit`). Lean on the `ux-foundations`, `design-tokens`, `accessible-components`, `interaction-feedback`, and `ux-audit` skills for what "good" looks like in each area.

## When to use

The user wants to understand an existing UX/design layer they did not build — joining a new repo, picking up an unfamiliar frontend, or learning a team's conventions. Phrases like "walk me through this app's UX", "onboard me onto the design system", or "explain how this project handles components/tokens/a11y". If they instead want to *create* a baseline, use `ux-foundations`; to *score* one, use `ux-audit`.

Optional focus: a path or an area (e.g. "tokens", "the dialog component"). If none is given, cover the design layer end to end.

## Procedure

1. **Detect the stack and survey the design layer.** Read `../ux-foundations/references/stack-detection.md` and run it; report framework, styling approach, and language in one line. Then build a short map: where tokens/theme live, the component library and its primitives, styling conventions, the accessibility patterns in use, the interaction-feedback patterns (loading / empty / error / success, toasts), and copy/voice conventions. Skim recent history (`git log`, recently merged PRs) for changes to use in step 4.
2. **Confirm the path.** List the parts you'll walk through — dependencies first, usually **tokens → primitives → composed components → app screens** — and confirm scope. Honor any focus the user gave.
3. **Walk it part by part** — one part at a time, never a wall of text. For each:
   - **Explain** how *this* project handles it and the pattern/convention it follows.
   - **Send the user to the code** — name concrete files/components to open and read (e.g. *"open `tokens.css` and `Button.tsx`"*), rather than pasting them.
   - **Ask questions to answer** — a few comprehension/prediction questions (*"which token drives the focus-ring color?"*, *"what makes this dialog's focus trap correct?"*), then check the answers, correct misconceptions, and push deeper before moving on.
4. **Reimplement a recent change.** From recent history, pick **a few smaller UX/design changes** — a new component variant, a token change, an added interaction state, a copy fix — each small enough to redo in one sitting and ideally in a part already walked. Present them as an **interactive choice**; the user picks one (or asks for different candidates). Stub out or revert it in a **scratch copy** (without showing the original diff), state the change's intent and acceptance criteria, and have the user reimplement it. Then review against what the project actually shipped — convention fit, accessibility, and which approach is better and why.
5. **Wrap up.** Summarize the parts covered and the user's comprehension, the reimplementation outcome, and suggest the `ux-audit` skill (to score what they now understand) or a focused component review as next steps.

## Notes

- Read-only by default — do not modify the project's real files; the user's reimplementation happens in a scratch copy.
- Keep each part short and interactive: the user reading the real code and answering is the point.
- In Claude Code this skill backs the `/ux-onboarding` command; it also triggers from natural language on both Claude Code and Codex.
