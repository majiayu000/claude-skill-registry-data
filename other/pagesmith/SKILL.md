---
name: pagesmith
description: >-
  Build, extend, or maintain an EXISTING Pagesmith site (or a @pagesmith/* package itself) — author
  pages, configure nav / theme / search, validate, and deploy. Triggers on "add a docs page / write
  a guide / document this in Pagesmith", "configure the sidebar / nav / theme / search", "build /
  validate / deploy the Pagesmith site", or working on @pagesmith/core|site|docs. Detects the site
  flavor (docs-preset via `pagesmith.config.json5` vs core-native via `site.config.json5`) and then
  delegates the deep authoring to the CONSUMER'S version-matched package skills under node_modules —
  it NEVER restates package config schemas, frontmatter fields, or CLI flags from memory. Writes
  content + config and can deploy, but is read-only until a plan is confirmed and the gh-pages push
  is gated. Routes diagram work to /adk:diagramkit and greenfield scaffolding to
  /adk:scaffold-pagesmith-docs.
allowed-tools: Read, Edit, Write, Grep, Glob, Bash, WebFetch, Agent, Workflow
argument-hint: "<task-or-target> [--flavor docs|core|auto] [--plan|--act] [--deploy] [-i|--interactive] [--deep]"
---

# pagesmith — build & maintain an existing Pagesmith site

Works on a Pagesmith site (or a `@pagesmith/*` package) that **already exists** — new pages, nav/theme/search config, a validate pass, a deploy. It does **not** author the deep task from memory: it detects the site flavor, makes sure the installed package's own skills are present, and **delegates to the version-matched copy under `node_modules`**. For a brand-new site with no config yet, that's `/adk:scaffold-pagesmith-docs`; for diagrams, `/adk:diagramkit`.

The full operating contract lives in this skill folder — read these as you need them:

| Aspect | File |
|---|---|
| How you build (delegation discipline, voice, output shape) | `persona.md` |
| The phased process + Workflow orchestration | `workflow.md` |
| Hard rules + refusals + safety | `rules.md` |
| Task routing (flavor detection + which node_modules skill) | `dispatch.md` |

## Quick start

1. **Detect the flavor** (Phase 0 in `workflow.md`). `pagesmith.config.json5` at the repo root → **docs-preset** (`@pagesmith/docs`). `site.config.json5` → **core-native** (`@pagesmith/site` + `@pagesmith/core`). Neither → greenfield: stop and route to `/adk:scaffold-pagesmith-docs` (`rules.md`). `--flavor` overrides detection.
2. **Read `dispatch.md`** and classify the task → the sub-flow + the matching installed skill(s).
3. **Materialize the package skills** in the consumer so the deep guidance is present and version-matched: `npx pagesmith skills install` (diagrams: `npx diagramkit skills install`). If that subcommand isn't available yet, follow `node_modules/<pkg>/skills/<pkg>-setup/SKILL.md` as the fallback. The exact bin follows the installed package (`pagesmith-docs` / `pagesmith-core`).
4. **Delegate.** Read and follow `node_modules/<pkg>/skills/<name>/SKILL.md` for the matched task — it points at the version-matched `node_modules/<pkg>/REFERENCE.md` / schemas that are authoritative for this install. **Never restate config schema, nav keys, theme tokens, frontmatter fields, or CLI flags from memory** (`persona.md`).
5. **Validate + report.** Run the repo's **own** build/validate scripts (read `package.json`; don't assume a command). Report the flavor, the route, and the skill delegated to. Deploy is gated (`rules.md`).

## Workflow is the default for multi-surface changes

"Always have a workflow." A change that spans more than one page or surface — seeding several doc pages, a combined nav + theme + search change, generating a docs set — gets the Workflow in `workflow.md`: fan out one agent per page/surface (each following the *same* matched node_modules skill) in parallel, then run a completeness/consistency critic (frontmatter present, nav resolves, no orphan pages) before the set survives. A single page or a single config key is done inline — say you skipped the Workflow.

## Modes

- **default (`--plan` then confirm then `--act`)** — detect, route, materialize, delegate, write the plan, **stop and confirm**, then execute + validate + report. Read-only until the plan is confirmed.
- **`--plan`** — stop after the plan (flavor + route + the matched skill + the file-level change list); touch nothing.
- **`--act`** — skip the confirm gate and execute the matched skill directly (still validates, still gates the deploy).
- **`--flavor docs|core|auto`** — override flavor detection (`auto` is the default: read the config file).
- **`--deploy`** — after a green validate, run the repo's own gh-pages deploy path; the `git push` / PR is confirmed first, never force, never to a protected branch (`rules.md`).
- **`-i`** — confirm flavor, route, and outline with the user before writing; walk multi-page work page-by-page.
- **`--deep`** — stronger reasoning profile; auto-select for a package-development task, a cross-surface migration, or a full docs generation.
