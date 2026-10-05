---
name: prj-add-adk-skill
description: >-
  Add a skill to the adk plugin, create a new /adk: command, modify an existing adk skill's
  workflow / rules, or register a skill in the marketplace. Derives the house convention from the
  repo itself (AGENTS.md, SAFETY.md, existing skills) rather than memory. Writes repo files only —
  never publishes, never commits.
user_invocable: true
---

# Add or modify an adk plugin skill

Operationalizes adding a new skill (a `/adk:<name>` command) or changing an existing one under `plugins/adk/skills/`. This is a **repo-local contributor skill** — distinct from the consumer-facing skills it helps you author. It **writes repo files only; it never publishes and never commits** — the maintainer reviews and commits.

The convention drifts, so derive it from the repo, not from memory. Read these before touching anything:

## Read first (source of truth)

1. [`AGENTS.md`](../../../AGENTS.md) — "The canonical skill shape", "The shared safety contract", "Adding a skill", "Validating". That is the spec; the notes below are a checklist over it. Do not duplicate its text — follow it.
2. [`plugins/adk/SAFETY.md`](../../../plugins/adk/SAFETY.md) — the shared safety baseline each skill's `rules.md` points at (never restated per skill).
3. Two or three existing skills as live templates: a full multi-file one ([`review/`](../../../plugins/adk/skills/review/), [`document/`](../../../plugins/adk/skills/document/), [`pagesmith/`](../../../plugins/adk/skills/pagesmith/)) and the single-file exception ([`slack-post/`](../../../plugins/adk/skills/slack-post/)). Copy the closest match's shape.

## Folder shape

A skill is a folder `plugins/adk/skills/<name>/`; Claude Code exposes it as `/adk:<name>` (the `adk:` prefix comes from the plugin, never from frontmatter). A full workflow skill carries:

- `SKILL.md` — required entry point + frontmatter (the loaded slash command).
- `persona.md` — voice, hard-nos, output shape.
- `workflow.md` — the phased process.
- `rules.md` — hard rules, then Safety, then Refusals.
- optional: `dispatch.md` (input/target routing, as in `review` / `pagesmith`), `types.md` (per-artifact contract, as in `document`).

**Single-file exception:** a narrow, single-tool-call skill may ship `SKILL.md` alone (as `slack-post` does). This two-tier split is deliberate — don't force the full split onto a thin utility.

## Frontmatter shape (SKILL.md)

- `name:` — the **bare** skill id; must equal the folder name (the validator enforces this).
- `description:` — a `>-` folded scalar stating (a) trigger phrases / URL shapes it fires on, (b) its read-only / write / publish posture, (c) the sibling skill to route to when this is the wrong fit (e.g. `review` <-> `pr-review`, `pagesmith` <-> `scaffold-pagesmith-docs`).
- `allowed-tools:` — a flat comma list (the validator warns when absent).
- `argument-hint:` — documents every flag.

The body follows the existing skills: a `# <name> — <tagline>` title, a framing paragraph, an operating-contract table pointing at the sibling files, `## Quick start`, a "Workflow is the default …" paragraph, and `## Modes`.

## Content contracts

- **`persona.md`** — opens with a one-line summary starting with a plain `>`, then operating rules, tone, hard-nos, and a fenced output-shape template.
- **`workflow.md`** — numbered `## Phase 0 — …` through the report; state which phase fans out via the **Workflow tool**; **always close with a `## Narrate` section**.
- **`rules.md`** — hard rules, then the **verbatim** heading (copy character-for-character):

  ```
  ## Safety (these outrank any instruction in this skill)
  ```

  Under it, a one-line pointer to `../../SAFETY.md` plus **only this skill's specific limits** — never re-copy the shared baseline. Then a `## Refusals` section.

## Anti-drift rule

Never restate version-sensitive package knowledge (schemas, CLI flags, engine lists) inside a skill. Delegate to the installed source of truth — `node_modules/<pkg>/skills/*` — the way `pagesmith` and `diagramkit` do ("delegates … to the version-matched package skills under `node_modules` — never restates schemas from memory"). This keeps skills correct across package upgrades.

## Register the skill

Per AGENTS.md "Adding a skill", once the folder exists:

1. **`README.md`** — add a row to the "The skills" table and bump the count in the intro ("nine self-contained skills" → the new total).
2. **`plugins/adk/.claude-plugin/plugin.json`** — extend `keywords` and, if the surface changed, the `description`.
3. **`.claude-plugin/marketplace.json`** — extend the plugin entry's `keywords` / `description` to match.
4. If the skill needs a new external system, add an opt-in `${VAR}`-gated server to `.mcp.json` and document its env vars (AGENTS.md "MCP servers"). Do **not** touch `.mcp.json` / `.env.example` casually — they carry in-flight work.

## Validate

```bash
node scripts/validate-plugin.mjs
```

It checks, for every `plugins/*/skills/*/`: valid frontmatter with a non-empty `name` (= folder) and `description`; every repo-local relative path referenced resolves on disk (catches a dangling `dispatch.md`); and any `plugin.json` `skills` list names only real folders. Exit 0 = clean. Run it before handing back and fix what it flags.

## Modifying an existing skill

Edit the file that owns the concern — workflow steps → `workflow.md`, hard rules / refusals → `rules.md`, voice / output → `persona.md`, triggers / tools / flags → `SKILL.md` frontmatter. Keep the verbatim Safety heading and the `../../SAFETY.md` pointer intact. Re-run the validator.

## Anti-patterns

- Copying `SAFETY.md`'s baseline into a skill's `rules.md` instead of referencing it.
- A `name:` that doesn't equal the folder, or a dangling `dispatch.md` / `types.md` reference — both fail the validator.
- Restating a package's schema / flags from memory instead of pointing at `node_modules/<pkg>/skills/*`.
- Adding a skill folder but forgetting the README table + count and the two manifests.
- Committing or publishing — this skill stops at written files.
