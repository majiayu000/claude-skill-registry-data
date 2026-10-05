---
name: diagramkit
description: >-
  Create, render, embed, and audit diagrams in any repo that uses diagramkit. Triggers on
  "draw / create / render / re-render / embed / audit a diagram", "fix diagram contrast /
  WCAG warnings", "run the repo-wide diagram health check", or any mention of a diagramkit
  engine (mermaid / excalidraw / draw.io / graphviz). Writes diagram sources, rendered SVGs,
  and the light/dark embed markup into the LOCAL repo and runs the local diagramkit CLI
  (doctor / skills install / render / validate); it never commits, pushes, or publishes —
  it stops at local files. Version-sensitive authoring detail (engine choice, palettes,
  readability budgets, config schema) is NEVER restated here — it is delegated to the
  consumer's installed copy at node_modules/diagramkit/skills/*. Routes broader Pagesmith
  content / site / deploy work to /adk:pagesmith; the repo-wide audit runs diagramkit's own
  review flow.
allowed-tools: Read, Edit, Write, Grep, Glob, Bash, Agent, Workflow
argument-hint: "<intent-or-path> [--engine mermaid|excalidraw|draw-io|graphviz] [--audit] [--embed <content-path>] [--scope-dir <dir>] [--fail-on <severity>] [-i|--interactive] [--deep]"
---

# diagramkit — create, render, embed, and audit diagrams

Owns the diagram lifecycle in **any** repo that has `diagramkit` installed: author a new diagram, re-render a source, embed a rendered diagram into content, or run a repo-wide audit that validates every diagram and fixes contrast/WCAG issues. **Writes to the local repo and runs the local diagramkit CLI — it never commits, pushes, or publishes.**

This skill is a thin router. It **does not restate diagramkit's version-sensitive knowledge** — engine selection, per-engine palettes, readability budgets, config schema, and the exact `<picture>` markup all live in the consumer's installed package and drift the moment a version ships. The real authoring is always delegated: *read and follow `node_modules/diagramkit/skills/diagramkit-<engine>/SKILL.md`*. Broader Pagesmith content/site/deploy work routes to `/adk:pagesmith`.

The full operating contract lives in this skill folder — read these as you need them:

| Aspect | File |
|---|---|
| How you work (voice, delegation discipline, output shape) | `persona.md` |
| The phased process + Workflow orchestration | `workflow.md` |
| Hard rules + refusals + safety | `rules.md` |
| Route dispatch (new-diagram / render / embed / audit) | `dispatch.md` |

## Quick start

1. **Verify + materialize** (Phase 0 in `workflow.md`). Confirm diagramkit is installed and Chromium is warm with `npx diagramkit doctor`. Materialize the per-engine skill stubs with `npx diagramkit skills install` — if that subcommand isn't in the installed version, fall back to following `node_modules/diagramkit/skills/diagramkit-setup/SKILL.md`.
2. **Read `dispatch.md`** and classify the input into one route: **new-diagram**, **render**, **embed**, or **audit**.
3. **Delegate the authoring.** For a new diagram, select the engine via `node_modules/diagramkit/skills/diagramkit-auto/SKILL.md`, then author by following that engine's `node_modules/diagramkit/skills/diagramkit-<engine>/SKILL.md`. **Never** invent a palette or budget here — the installed skill is the source of truth.
4. **Render + validate.** `npx diagramkit render` the source, then `npx diagramkit validate` (add `--fail-on <severity>` / `--scope-dir <dir>` if the installed version supports them; else fall back to a plain validate). A failing gate stops you (`rules.md`).
5. **Embed / report.** For the embed route, produce the light/dark `<picture>` markup per the installed skill's guidance and place it in the target content file. Report the sources, renders, validation results, and any embed — nothing is committed or published.

## Workflow is the default for the repo-wide audit

"Always have a workflow." The **repo-wide audit** gets the Workflow in `workflow.md`: fan out **one agent per engine (or per content area)**, each running `diagramkit validate` over its slice, applying contrast/WCAG fixes and re-rendering stale SVGs by following its engine's installed skill, then a final repo-wide `diagramkit validate` gate confirms the fixes held. A single new diagram or a one-source re-render is done inline by delegating to the one relevant engine skill — say you skipped the Workflow.

## Modes

- **default** — infer the route from the input (`dispatch.md`): author a new diagram, re-render a source, embed into content, or audit the repo. Verify → delegate → render → validate → report. Writes local files only.
- **`--engine <name>`** — skip auto-selection; author with the named engine by following `node_modules/diagramkit/skills/diagramkit-<engine>/SKILL.md`.
- **`--audit`** — force the repo-wide audit: fan out per engine/content area via the Workflow tool, fix contrast/WCAG, re-render stale SVGs, re-validate. Follows diagramkit's own review flow (`node_modules/diagramkit/skills/diagramkit-review/SKILL.md`).
- **`--embed <content-path>`** — produce the light/dark `<picture>` embed for the target content file per the installed skill; route broader page authoring to `/adk:pagesmith`.
- **`--scope-dir <dir>` / `--fail-on <severity>`** — passed through to `diagramkit validate` when the installed version supports them; otherwise fall back to a plain validate scoped to that subtree, and say so.
- **`-i`** — confirm the engine choice, the audit scope, and each contrast/WCAG fix before applying it.
- **`--deep`** — use a stronger reasoning profile; auto-select for a large audit or an ambiguous engine choice.
