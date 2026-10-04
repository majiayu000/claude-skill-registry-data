---
name: sk-project-docs
description: Scaffold, audit, or nudge a project's documentation structure. Use when the user says "set up docs", "project docs", "nudge docs", "init documentation", "update docs index", or when docs are redundant and scattered.
---

# Project Docs

Create the docs a project needs, prune the ones it does not, and keep `AGENTS.md` and `llms.txt` in sync.

## When to use

- User asks to set up, init, nudge, or update project docs.
- A project is missing `README.md`, `AGENTS.md`, or `docs/`.
- Existing docs have drifted from the index.
- Existing docs are redundant, overlapping, or scattered.

## Goal

Scaffold only the docs the project needs. Audit existing docs, move overlapping content to the right standard doc, and ask before removing files.

`AGENTS.md` and `CLAUDE.md` are agent-only. `AGENTS.md` must be three things: a docs index, an AI rules index, and a highly condensed version of the docs. `CLAUDE.md` is a symlink (or fallback `@AGENTS.md` file) to `AGENTS.md`.

Docs are human- and agent-facing. Agent-only rules go in `.agents/rules/` and are referenced explicitly in `AGENTS.md`/`CLAUDE.md` with `@.agents/rules/<file>.md`. Do not use globs like `@.agents/rules/*.md`.

## Output

These files may be created or updated:

- `README.md`
- `AGENTS.md`
- `CLAUDE.md`
- `llms.txt` (public projects)
- `LICENSE.md` (open or public projects)
- `docs/ARCHITECTURE.md`
- `docs/USAGE.md`
- `docs/CONTRIBUTING.md`
- `docs/SECURITY.md`
- `docs/CODE_OF_CONDUCT.md`
- `docs/CHANGELOG.md`
- `docs/TROUBLESHOOTING.md`

## Decision grid

Ask the user or infer from the repo:

| Field        | Values                                                  |
| ------------ | ------------------------------------------------------- |
| audience     | public, internal, personal                              |
| openness     | oss, proprietary, none                                  |
| project_type | cli, library, web-app, internal-tool, skill-repo, other |
| releases     | versioned, continuous, none                             |
| rules_dir    | does `.agents/rules/` exist?                            |

## File selection

| File                      | Default condition                                |
| ------------------------- | ------------------------------------------------ |
| `README.md`               | always                                           |
| `AGENTS.md`               | always                                           |
| `CLAUDE.md`               | always                                           |
| `llms.txt`                | `audience` is `public`                           |
| `LICENSE.md`              | `openness` is `oss` or user wants one            |
| `docs/ARCHITECTURE.md`    | project is non-trivial or user wants             |
| `docs/USAGE.md`           | `project_type` is `cli`, `library`, or `web-app` |
| `docs/CONTRIBUTING.md`    | project has contributors                         |
| `docs/SECURITY.md`        | project has users or contributors                |
| `docs/CODE_OF_CONDUCT.md` | `openness` is `oss` or corp policy               |
| `docs/CHANGELOG.md`       | `releases` is `versioned`                        |
| `docs/TROUBLESHOOTING.md` | project has common failure modes or user wants   |

Choose templates from `templates/` next to this `SKILL.md` (e.g. `README.md` → `templates/README.md`, `CONTRIBUTING.md` → `templates/CONTRIBUTING-oss.md` or `templates/CONTRIBUTING-internal.md`).

## Standard docs tree

A project should hold only these docs:

- `README.md` — human-facing overview, install, and usage.
- `AGENTS.md` — agent-only index: docs index, AI rules index, condensed docs.
- `CLAUDE.md` — symlink or `@AGENTS.md` fallback.
- `llms.txt` — public projects only.
- `LICENSE.md` — open/public projects.
- `docs/ARCHITECTURE.md` — structure and data flow.
- `docs/USAGE.md` — detailed usage.
- `docs/CONTRIBUTING.md` — setup, conventions, and PRs.
- `docs/SECURITY.md` — security policy.
- `docs/CODE_OF_CONDUCT.md` — open/corp policy.
- `docs/CHANGELOG.md` — versioned releases.
- `docs/TROUBLESHOOTING.md` — common problems.

Anything outside this tree that overlaps with a standard doc is a candidate for merging, not indexing.

## Placeholders

Substitute `{{project}}`, `{{repository}}`, `{{author}}`, `{{license}}`, `{{setup}}`, `{{run}}`, `{{format}}`, `{{rules_table}}`, `{{rules_includes}}`, `{{docs_table}}`, `{{what}}`, `{{how}}`, and `{{conventions}}` from `package.json`, git remote, or by asking/inferring.

- `{{rules_table}}` — full markdown table with columns `Rule`, `File`, `What it covers`.
- `{{rules_includes}}` — explicit `@.agents/rules/<file>.md` lines, one per rule file.
- `{{docs_table}}` — full markdown table with columns `Doc`, `Purpose`.
- `{{what}}` — one-paragraph summary of what the project is.
- `{{how}}` — short setup, conventions, common commands, and project layout.
- `{{conventions}}` — bullet list of the conventions an agent must follow.

## Conventions

- `AGENTS.md` is agent-only. No long prose, no human tutorial, no pull-request section. Just docs index, rules index, condensed docs.
- Agent-only rules live in `.agents/rules/`.
- Reference each rule file explicitly: `@.agents/rules/<file>.md`.
- Start `AGENTS.md` with a strong instruction to read the rules before doing any work.
- Docs are human- and agent-facing. Do not duplicate `AGENTS.md` content in `README.md` or `docs/*`.

## Steps

1. **Inspect** the repo for existing docs, rules, and source of truth.
2. **Audit** docs against the standard tree. Identify files that overlap, duplicate, or belong elsewhere (e.g. `docs/ai_guidelines.md` that should fold into `docs/CONTRIBUTING.md` or an `.agents/rules/` file).
3. **Propose** a list of docs and a cleanup plan. Ask which to create, update, move, or remove.
4. **Do not remove files** without explicit user approval. Move content first, then ask whether to delete the source.
5. **Read** the relevant templates from `templates/`.
6. **Substitute** placeholders.
7. **Write** each doc.
8. **Create or update** `AGENTS.md` from `templates/template-agents.md`. It must be a rules-first index, then a docs index, then a highly condensed version of the docs. Reference rule files explicitly with `@.agents/rules/<file>.md`.
9. **Create or update** `llms.txt` if `audience` is `public`.
10. **Create or update** `CLAUDE.md`: try `ln -s AGENTS.md CLAUDE.md`, fall back to a one-line `@AGENTS.md` file.
11. **Report** what changed and suggest using the `documentation` skill to fill prose.

Do not create rule files; only reference what already exists.

## CLAUDE.md

1. If `CLAUDE.md` exists and is already a symlink to `AGENTS.md`, leave it.
2. If it does not exist, try `ln -s AGENTS.md CLAUDE.md`.
3. If a text fallback is needed, write `@AGENTS.md`.
4. If a regular `CLAUDE.md` exists and is not the fallback, warn and ask before overwriting.

## llms.txt

If `audience` is `public`, create or update `llms.txt` with entry points, docs, skills, and rules (use raw GitHub URLs when `{{repository}}` is known; otherwise relative paths).

After creating each file, report the paths.
