---
name: ux-foundations
description: This skill should be used when the user wants to bootstrap or set up a UX baseline in a project — e.g. "bootstrap UX best practices", "set up our UX foundations", "scaffold a design system starting point", "establish UX standards for this repo", or runs /ux-bootstrap. It detects the project's stack and lays down design tokens, accessible base primitives, a11y linting, lightweight metrics, and a UX-CHECKLIST. It is the orchestrator that other implement skills (design-tokens, accessible-components, interaction-feedback) build on.
version: 0.1.0
---

# UX Foundations

Establish a coherent UX baseline in a project, adapted to whatever stack is present. This skill is the entry point for bootstrapping and the owner of the **stack-detection** convention every other implement skill reuses.

## When to use

- Starting UX work in a new or existing repo with no established system.
- The user asks to "bootstrap", "set up", "establish", or "scaffold" UX/design foundations.
- Invoked by the `/ux-bootstrap` command.

For narrower work, defer to the specialized skills: `design-tokens`, `accessible-components`, `interaction-feedback`, `ux-copy`. For evaluation rather than setup, use `ux-audit`, `accessibility-audit`, or `ux-metrics`.

## Workflow

Always run these in order. Do not generate code before detection.

### 1. Detect the stack

Read `references/stack-detection.md` and follow it. Determine, in this order:
- **Framework** (React / Vue / Svelte / Angular / none)
- **Styling approach** (Tailwind / CSS Modules / styled-components or Emotion / vanilla CSS)
- **Token output format** that matches the above
- **TypeScript** yes/no

If nothing is detected (no `package.json`, no source), fall back to **framework-agnostic HTML + CSS custom properties**. Tell the user what you detected before writing anything.

### 2. Confirm scope

State a short plan and confirm the target. By default the baseline includes all five layers below; let the user opt out of any. Never overwrite existing files without showing a diff and confirming.

### 3. Lay the baseline (five layers)

1. **Design tokens** — delegate to the `design-tokens` skill. Produce a single source of truth (color with verified contrast, type scale, spacing scale, radius, shadow, motion durations/easings) in the format the stack expects.
2. **Accessible base primitives** — delegate to `accessible-components`. Scaffold at minimum: an accessible Button, a labelled form Field, and a Dialog/Modal with focus management. Wire them to the tokens.
3. **A11y linting** — set up automated guardrails appropriate to the stack (e.g. `eslint-plugin-jsx-a11y` for React, `eslint-plugin-vuejs-accessibility` for Vue, `svelte-check`/a11y warnings for Svelte). Add the config and a script entry; do not silence existing warnings.
4. **Lightweight metrics** — delegate to `ux-metrics` to add a minimal Core Web Vitals reporter (the `web-vitals` snippet) wired to the console or the project's analytics, so regressions are observable.
5. **Interaction-feedback defaults** — delegate to `interaction-feedback` to establish the empty/loading/error/success state pattern and an accessible toast/`aria-live` region the app can reuse.

### 4. Write the project UX checklist

Create `UX-CHECKLIST.md` at the project root from `assets/UX-CHECKLIST.md`, trimmed to what applies. This is the durable artifact the team uses on every PR.

### 5. Summarize

Report what was created/changed as a short list, note any decisions deferred to the user (e.g. brand colors to replace placeholders), and suggest the natural next step (usually running `/ux-audit` to baseline the current state).

## Principles

- **Adapt, don't impose.** Match existing naming, file layout, and idioms. Prefer the project's current libraries over adding new ones.
- **Tokens first.** Everything downstream references tokens, not raw values.
- **Accessibility is non-negotiable baseline,** not an add-on layer.
- **Make quality observable.** A baseline that can't be measured will regress; that is why metrics and a checklist are part of foundations.
- **Small, reversible steps.** Show diffs, confirm before overwriting, keep each layer independently useful.

## References

- `references/stack-detection.md` — the canonical detection procedure (shared across skills).
- `assets/UX-CHECKLIST.md` — the per-project checklist template.
