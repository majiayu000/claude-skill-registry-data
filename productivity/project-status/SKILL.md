---
name: project-status
description: >
  Maintain machine-readable project status snapshots for instant context at the
  start of any session, eliminating the need to re-derive project state from
  package.json, Cargo.toml, or git history. A lightweight PROJECT.md convention
  in every project root: YAML frontmatter for machine parsing (status, phase,
  version, last_session, tech_stack, blockers, focus) plus a brief prose section
  for human context. Triggered: automatically at session start (read PROJECT.md
  first, then work), when starting work on a project after time away (check if
  last_session is stale), during handoffs (what's the current state?), when
  planning new work (what are the blockers?), and when onboarding to a codebase.
  Key capabilities: a single file that replaces reading package.json + git log +
  several docs, a focus list that tells you what to work on immediately, a blockers
  field that surfaces what genuinely stopped progress, and a derived-vs-human-
  maintained field table so contributors know when to update. Ideal for anyone
  working across multiple projects, anyone inheriting a codebase, and teams that
  want a shared understanding of project state without a project management tool.
  Also for writing better commit messages (know the phase/status), assessing build
  health at a glance before running tests, and quickly comparing tech stacks across
  a portfolio.
---

# Project Status — Instant Context

A lightweight convention for capturing project state in a single `PROJECT.md` file that an AI can read in one pass, eliminating the need for re-exploration on every session.

---

## Format

Every project should have a `PROJECT.md` in its root directory. The format uses YAML frontmatter for machine-readability, followed by a brief prose summary.

```yaml
---
name: [project-name]
status: active          # active | paused | archived | completed
phase: mvp             # bootstrap | mvp | feature | polish | maintenance
version: 0.1.0         # mirrors package.json/Cargo.toml

last_session: 2026-03-19

tech_stack:
  frontend: [React 19, TypeScript, Vite, Tailwind]
  backend: [Rust, Tauri 2, tokio, reqwest]
  packaging: [Tauri bundler, macOS app]

build: passing         # passing | failing | unknown

blockers: []           # empty = clear; list blockers only when present

focus:                 # current work in progress or next priority
  - Feature X
  - Feature Y
---

## What This Project Is

One-paragraph description of the project's purpose.

## Current Status

Brief status summary (2-3 sentences).

## Key Architecture

- `src/` — frontend
- `src-tauri/` — backend

## Open Questions

- Question 1
- Question 2
```

---

## When to Read PROJECT.md

**Before exploring any project for the first time in a session**, check for and read `PROJECT.md` in the project root. This is the single source of truth for project state — do not re-derive it from package.json, Cargo.toml, or git history unless the file is missing or stale.

---

## Session Workflow (Session Start)

1. Read `medium-term.md` at `~/.claude/memory/medium-term.md`
2. Identify the current project and its stacks from the Active Projects table
3. Read `{project}/PROJECT.md`
4. Sync lessons for all stacks: run `/lessons-sync` (all stacks)

## When to Update PROJECT.md

### At Session End
1. Update `last_active` in `medium-term.md` for the current project
2. Sync lessons: for each stack in the project, diff root `~/.claude/memory/lessons/{stack}.md` against `{project}/memory/lessons/{stack}.md`, append new entries from root
3. Append session log to `{project}/memory/sessions/YYYY-MM-DD.md`
4. Update `last_session` in `{project}/PROJECT.md` to today's date
5. Update `focus` if work shifted from what was listed
6. Update `status` or `phase` only if a genuine milestone was hit
7. Update `blockers` only if something genuinely blocked progress

### At Session Start
- Read PROJECT.md first
- Use `focus` to immediately understand what to work on
- If `last_session` is stale (more than a few days ago), ask if the file needs updating

### Never Update For
- Package version bumps (those live in package.json/Cargo.toml)
- Individual commits or minor code changes
- Git history (git log is the source of truth for activity)

---

## Derived vs. Human-Maintained Fields

| Field | Source | Update Frequency |
|-------|--------|-----------------|
| `name` | human | only on rename |
| `status` | human | on phase change |
| `phase` | human | on milestone |
| `version` | package.json / Cargo.toml | on release |
| `last_session` | human (session end) | every session |
| `tech_stack` | package.json / Cargo.toml | on stack change |
| `build` | human (after build) | after builds |
| `blockers` | human | only when present |
| `focus` | human | at session end |

---

## Adding a New Project

When a new project is created:

1. Create `{project}/PROJECT.md` with the standard format
2. Run `/skill-import` for the project's stack
3. Update `medium-term.md` at `~/.claude/memory/medium-term.md`: add the project to the Active Projects table with its stacks and location
4. Sync lesson files: `/lessons-sync`
