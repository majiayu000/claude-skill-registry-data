---
name: project-hardness
description: Turn any local project into an AI-readable, maintainable, verifiable causal layer under the project's `.agent/` directory, and harden vague requirements into concrete task specs before editing. Use when (a) starting work on an unfamiliar or large project, (b) you need to know a change's blast radius / do-not-modify boundaries, or (c) a requirement is vague and you need clarified goal + involved modules + edit paths + risks + acceptance criteria + test commands. Not a grep/index/chat-memory; it is a static, source-backed project model. Applies to every agent (Claude Code, Codex, OpenCode, etc.).
allowed-tools: Bash(*), Read, Glob, Grep
---

# project-hardness

A per-project **causal layer**: a static, source-backed model of a project written to
`<project>/.agent/`. It answers "what does this project do, what depends on what, what
breaks if I change X, what must I not touch, and why was it built this way" — without
re-reading the whole repo every session.

The **engine lives in WEIPING_WIKI** (`scripts/hardness/`, invoked via `python scripts/wiki.py hardness`).
The **artifacts live in the target project** (`.agent/`, git-ignored by default).
Only **cross-project lessons** are ever synced to agentmemory — project facts stay local.

## When to use

- Starting work on an unfamiliar, large, or long-dormant project → `scan` first.
- About to change something and unsure of impact → `impact <module>` or read `modules/<m>.md`.
- A requirement is vague → `harden` it into a task spec BEFORE writing code.
- After completing work → update `.agent/` (re-`scan`) and `sync` only reusable lessons.

## Commands

Run from the root of a WEIPING_WIKI checkout:

```bash
# 1. Build / refresh the causal layer for a project
python scripts/wiki.py hardness scan <project-path> [--name NAME] [--json]

# 1b. Discover and scan every important project on the machine (de-duped, safety-excluded)
python scripts/wiki.py hardness scan-all [--dry-run] [--json]

# 2. Harden a vague requirement into a concrete task spec (.agent/tasks/<id>.md)
python scripts/wiki.py hardness harden <project-path> "the requirement text" [--id ID]

# 3. Blast radius of a single module
python scripts/wiki.py hardness impact <project-path> <module-name>

# 4. Sync ONLY cross-project lessons to agentmemory (project facts are auto-rejected)
python scripts/wiki.py hardness sync <project-path> --lesson "general reusable lesson" [--commit]
```

`sync` is dry-run by default; pass `--commit` to actually send. It refuses any text that
names concrete files, paths, or line numbers (those are project facts, not lessons).

## What `.agent/` contains

| Artifact | Purpose |
| --- | --- |
| `architecture.md` | Module table, responsibilities, dependency hotspots |
| `glossary.md` | Domain terms, entities, frameworks |
| `constraints.md` | Do-not-modify boundaries (secrets, lockfiles, migrations, markers) |
| `decisions.md` | Decision-flavored git history (manual additions preserved on regen) |
| `modules/*.md` | Per-module detail + blast radius + files |
| `flows/*.flow.md` | Business/process flows (route → handler → deps → entities) |
| `entities.json` | Entities and their lifecycle / touching modules |
| `causal-graph.json` | Full node/edge graph (imports, routes-to, reads/writes) |
| `tasks/*.md` | Hardened task specs |
| `index.json` | Manifest + provenance |

## Standard workflow

1. **First contact**: `scan` the project. Read `architecture.md` and `constraints.md`.
2. **Per requirement**: `harden` it. Read the generated `tasks/<id>.md` — it lists the
   clarified goal, involved modules, likely edit paths, risk points, acceptance criteria,
   and test commands. Refine it if the match confidence is LOW.
3. **Before editing**: check `impact` / the module's blast radius; never touch `block`
   constraints without explicit user approval.
4. **After completing**: re-`scan` to refresh `.agent/`; run the acceptance test commands;
   then `sync` only generalizable lessons to agentmemory.

## Boundary rules (hard)

- Project-specific facts stay in `.agent/`. Never write them to global agentmemory.
- The engine **never reads secret files** (`.env`, `*.key`, credentials.*) — it records
  their existence as a `block` constraint and moves on.
- `.agent/` is git-ignored by default (it is a derived artifact, regenerable any time).
- The engine is stdlib-only and fails gracefully if agentmemory is unreachable.

See the full design at `wiki/concepts/project-hardness-system.md` in WEIPING_WIKI.
