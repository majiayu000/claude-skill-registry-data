---
name: help
description: This skill should be used when the user asks for help with the ux-design plugin — what it does, which skills, commands, agent, or bundled tools it ships, or how to use a specific one. Triggers on the /ux-help command and on phrases like "help with ux-design", "what can ux-design do", "list the ux-design commands", "how do I use ux-audit", "explain design-tokens". With no specific topic, give the full overview of everything the plugin offers; with a named skill, command, agent, or tool, explain just that one in depth. Do not use for actually running an audit or scaffolding work — that's the individual capability skills.
version: 0.1.0
---

# ux-design help

Explain the **ux-design** plugin to the user. This skill is the plugin's built-in guide: it answers "what can this do?" and "how do I use X?" without the user needing to read the docs tree.

## How to respond

Look at what the user asked for (the `$ARGUMENTS` from `/ux-help`, or the topic named in natural language):

- **No topic given** → give the **full overview** below: the three modes, every skill, every command, the agent, and the bundled tools, each in one line, then point to the docs and the natural next step.
- **A specific topic given** (a skill, command, agent, tool, or concept like "tokens", "accessibility", "contrast") → resolve it to the matching item(s) and explain **just that**: what it does, when it triggers, how to invoke it (both the Claude Code command/skill and the Codex `/ux-design:<skill>` form), and what it produces. Then read that item's detailed doc under `docs/` (or its `SKILL.md`) and fold in the specifics. If the topic is ambiguous, list the close matches and ask which they meant.

Keep it skimmable: lead with a one-line answer, then the detail. Don't dump file contents — summarize and link.

## Full overview (use when no topic is named)

**ux-design** helps you *guide, measure, and implement* UX best practices, across three modes:

- **Guide** — explain the right pattern while you work.
- **Measure** — score what exists, qualitatively and quantitatively.
- **Implement** — scaffold best practices into your codebase, adapted to its stack.

### Skills (the cross-agent surface)

| Skill | Mode | What it does |
|---|---|---|
| `ux-foundations` | Implement | Orchestrates a full UX baseline (tokens + accessible primitives + a11y lint + metrics + `UX-CHECKLIST.md`); owns the shared stack-detection convention. |
| `ux-onboarding` | Guide | Guided, part-by-part walkthrough of an existing project's UX/design patterns, ending in a reimplement-a-recent-change exercise. |
| `ux-audit` | Measure / Guide | Nielsen's 10 heuristics + IA + task-flow review → scored report. |
| `accessibility-audit` | Measure | WCAG 2.2 AA, per-criterion severity scoring; bundled zero-dep contrast checker. |
| `ux-metrics` | Measure | Core Web Vitals, Lighthouse/axe scores, analytics taxonomy, SUS survey scoring. |
| `design-tokens` | Implement | Scaffold/refactor tokens (color, type, space, radius, shadow, motion); migrate hardcoded values. |
| `accessible-components` | Implement | Accessible WAI-ARIA patterns (dialog, tabs, menu, combobox, disclosure, fields, tooltip) + a11y linting. |
| `interaction-feedback` | Implement / Guide | Empty/loading/error/success states, `aria-live` toasts, inline validation, optimistic UI, reduced-motion. |
| `ux-copy` | Guide | Microcopy, error messages, empty states, CTAs, voice & tone. |
| `help` | — | This guide. |

Skills trigger automatically from natural language — you rarely name them.

### Commands (Claude Code conveniences)

- **`/ux-audit [path\|url]`** → runs `ux-audit` + `accessibility-audit` → one consolidated scored report.
- **`/ux-bootstrap`** → runs `ux-foundations` (tokens, primitives, a11y lint, metrics, checklist).
- **`/ux-onboarding [path\|area]`** → guided walkthrough of the project's existing UX/design patterns.
- **`/ux-review [file\|url]`** → launches the `ux-reviewer` agent for a fast scored review of one artifact.
- **`/ux-help [topic]`** → this help.

### Agent

- **`ux-reviewer`** — scores a single component or screen across four lenses (usability heuristics, accessibility, visual hierarchy, interaction feedback), from code, a screenshot, or a live page. Invoked by `/ux-review`, or ask to "review this component".

### Bundled tools (zero dependencies, run standalone)

```sh
node skills/accessibility-audit/scripts/contrast.mjs "#777" "#ffffff"
node skills/design-tokens/scripts/type-scale.mjs 16 1.25
node skills/ux-metrics/scripts/sus-score.mjs 4 2 5 1 5 1 4 2 5 1
```

### Claude Code & Codex

The **skills are the shared, cross-agent surface**. On Codex they're exposed as slash commands (`/ux-design:ux-audit`, `/ux-design:help`, …) and trigger from natural language on either agent. The `/ux-*` commands and the `ux-reviewer` agent are Claude-Code conveniences over those skills; on Codex, invoke the skills directly.

### Where to go next

- Full per-skill guides: `docs/README.md` and the per-skill pages in `docs/`.
- Plugin overview and install: `README.md`.
- A typical loop: `/ux-onboarding` (understand) → `/ux-bootstrap` (lay foundation) → build with the implement skills → `/ux-audit` (measure) → `/ux-review` (spot-check).

## Resolving a named topic

Map the user's word to the right item before explaining:

- **"tokens", "design system", "colors", "type scale", "spacing"** → `design-tokens` (+ `type-scale.mjs`).
- **"accessibility", "a11y", "wcag", "contrast", "screen reader"** → `accessibility-audit` (+ `contrast.mjs`); for building accessible UI, `accessible-components`.
- **"audit", "heuristics", "usability"** → `ux-audit` (and `/ux-audit` which also runs `accessibility-audit`).
- **"metrics", "web vitals", "sus", "lighthouse"** → `ux-metrics` (+ `sus-score.mjs`).
- **"states", "loading", "error", "toast", "feedback", "validation"** → `interaction-feedback`.
- **"copy", "microcopy", "wording", "cta", "voice", "tone"** → `ux-copy`.
- **"bootstrap", "set up", "scaffold", "foundation", "baseline"** → `ux-foundations` / `/ux-bootstrap`.
- **"onboard", "walk me through", "learn this project"** → `ux-onboarding` / `/ux-onboarding`.
- **"review this component/screen"** → `ux-reviewer` / `/ux-review`.

Then open the matching `docs/<item>.md` (or `skills/<item>/SKILL.md`) and explain from it.
