---
name: scaffold-pagesmith-docs
description: >-
  Stand up a brand-new Pagesmith documentation site from nothing — @pagesmith/docs wired to
  diagramkit, sample content, package skills installed, ending on a running preview. Triggers on
  "scaffold / bootstrap / stand up / start / create a new docs site", "new Pagesmith docs from
  scratch", "set up a docs site with diagrams". Writes to disk and runs local tooling (npm install,
  skills install, site build, dev server) — it configures a deploy target but NEVER deploys, pushes,
  or opens a PR; it prints the deploy command for a human to run. Confirms before touching an
  existing pagesmith.config. This is the greenfield counterpart to /adk:pagesmith (use that for an
  EXISTING site) and hands diagram-only work to /adk:diagramkit. It restates no package config
  schema, no engine flags, no palette — every version-sensitive authoring detail is delegated to the
  consumer's installed skills under node_modules.
allowed-tools: Read, Edit, Write, Grep, Glob, Bash, WebFetch, Agent, Workflow
argument-hint: "<target-dir> [--name <project>] [--base-path <path>] [--deploy gh-pages|none] [--engine <name> ...] [--preset docs|core-native] [-i|--interactive] [--deep] [--dry-run]"
---

# scaffold-pagesmith-docs — stand up a new Pagesmith docs site

The flagship end-to-end scaffold. From an empty (or non-docs) directory it installs `@pagesmith/docs` + `diagramkit`, applies the package's own setup, materializes the package skills into the repo, seeds real sample content (one guide, one reference page, one diagram per requested engine), then validates and hands you a **running preview**. It stops at previewable and configured-for-deploy — it never deploys, pushes, or opens a PR.

This skill is **greenfield only**. For an existing Pagesmith site — adding pages, restyling, deploying, package work — use `/adk:pagesmith`. For diagram-only work in any repo, use `/adk:diagramkit`.

**Critical delegation rule:** this skill is a thin orchestrator. It does **not** carry Pagesmith's config schema, diagramkit's engine list, or any palette — those are version-sensitive and drift the instant a package ships. Every step that authors real content reads and follows the matching skill in the **consumer's** `node_modules` (`node_modules/@pagesmith/docs/skills/…`, `node_modules/diagramkit/skills/…`). If this skill and an installed skill ever disagree, the installed skill wins.

The full operating contract lives in this skill folder — read these as you need them:

| Aspect | File |
|---|---|
| How you scaffold (voice, discipline, output shape) | `persona.md` |
| The phased process + Workflow orchestration | `workflow.md` |
| Hard rules + refusals + safety | `rules.md` |

## Quick start

1. **Gather (Phase 0 in `workflow.md`)** — target dir, project name, base path, deploy target (GitHub Pages?), and the primary diagram engine(s). Detect the target's state first: is it a git repo, is there a `package.json`, and — the hard gate — does a `pagesmith.config.*` already exist? If it does, **stop and confirm** before writing anything (`rules.md`).
2. **Advise (Phase 1)** — present the docs-preset (`@pagesmith/docs`) vs core-native (`@pagesmith/core` + `@pagesmith/site`) choice. Default to `@pagesmith/docs` for a docs site; state why and, in `-i`, confirm.
3. **Read `persona.md`** and adopt the careful-scaffolder stance: narrate each step, never overwrite silently, prefer the package's own tooling over hand-rolled config.
4. **Scaffold (Phase 2)** — install the packages, follow the installed `pagesmith-docs-setup` skill for config + the GitHub Pages workflow, materialize skills with the `skills install` CLI, then **fan out via the Workflow tool** to author the sample guide, reference page, and one diagram per engine (each diagram via the installed `diagramkit-auto` skill).
5. **Validate (Phase 3)** — `skills install --check`, the site build, `diagramkit validate`, and a dev-server preview smoke check. **Report (Phase 4)** — the tree created, the dev/build/deploy commands, and the skills now available. Deploy is recommended, never run.

## Workflow is the default for a real scaffold

"Always have a workflow." A real scaffold seeds several independent artifacts — the sample guide, the reference page, and one diagram per requested engine — so **Phase 2 fans them out through the Workflow tool** (parallel authors, each delegating to the installed package skill), then a verify pass confirms each artifact builds/renders before it survives. The sequential spine (install → config → skills install) runs in order; only the content authoring parallelizes. A single-engine, single-page scaffold may be authored inline — say you skipped the fan-out.

## Modes

- **default** — gather (state sensible defaults), advise, scaffold, validate, report. Confirms before overwriting an existing config; ends on a running preview. Nothing is deployed or pushed.
- **`--dry-run`** — print the full plan (packages to install, the target tree, the commands, the sample content) and touch nothing. Use this to preview before committing to disk.
- **`-i`** — confirm each Phase 0 choice and the Phase 1 preset before scaffolding; walk the seeded content before the validate pass.
- **`--deep`** — stronger reasoning profile; auto-select for a multi-engine scaffold or a custom (`core-native`) preset.
- **`--preset docs|core-native`** — force the site flavor instead of advising it (default `docs`).
- **`--deploy gh-pages|none`** — the deploy target to configure (base path follows). `none` skips the deploy workflow.
- **`--engine <name> ...`** — the diagram engine(s) to seed a sample for; one sample diagram per engine, authored via the installed `diagramkit-auto` skill.
