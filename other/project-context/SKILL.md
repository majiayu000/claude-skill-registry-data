---
name: mk:project-context
description: Generate or update docs/project-context.md — the single source of truth for project conventions, tech stack, and anti-patterns. Loaded by all agents as a "constitution" to ensure consistent behavior.
triggers:
  - generate context
  - project context
  - init docs
actions:
  - generate
  - update
  - init
argument-hint: '[generate|update|init]'
source: local
keywords:
  - project-context
  - agent-constitution
  - tech-stack
  - conventions
  - anti-patterns
  - docs-init
when_to_use: Use when generating or updating docs/project-context.md — single source of truth for project conventions, tech stack, anti-patterns.
user-invocable: true
owner: docs
criticality: medium
status: active
runtime: claude-code
---

# Project Context Generator

Creates `docs/project-context.md` — the agent "constitution" that every agent loads on activation.

> To generate the full documentation suite (README, architecture, code standards, etc.), use `mk:docs-init` instead. `mk:project-context` generates only the agent constitution.

## Purpose

Eliminate context drift between agents. Without a single authoritative file, agents infer conventions independently and make conflicting decisions. Project context solves this by providing one document all agents read first.

## Actions

### generate

Scan the codebase and create `docs/project-context.md` from scratch.

**Scan targets:**

- `package.json` / `Cargo.toml` / `go.mod` / `pyproject.toml` → tech stack
- `tsconfig.json` / `eslint.*` / `prettier.*` → code conventions
- `**/test/**` / `**/*.test.*` / `**/*.spec.*` / `**/*.cy.*` → testing patterns
- Existing `docs/` → architecture decisions, prior context
- `.env.example` → environment variables (names only, not values)

**Output:** `docs/project-context.md` using `templates/project-context-template.md`

### update

Re-scan codebase and update existing `docs/project-context.md`. Preserves manual edits in sections marked `<!-- manual -->`.

### init

Write a TODO-filled skeleton to `docs/project-context.md` for greenfield projects
where `generate` would produce empty sections (no codebase to scan yet).

**Behaviour:**
- If `docs/project-context.md` already exists → **refuse with error**. Use `update` instead.
- If absent → write `templates/skeleton.md` to `docs/project-context.md`.
- Creates `docs/` directory if it does not exist.

**When to use `init` vs `generate`:**
| Situation | Action |
|-----------|--------|
| Empty or near-empty project, < 5 source files | `init` — fill manually |
| Established project with real code | `generate` — auto-derive |
| Existing `docs/project-context.md` is stale | `update` — re-scan, preserve manual edits |

## When to Run

- **First time:** After `mk:bootstrap` or `mk:docs-init`
- **After architecture changes:** New framework, new database, major refactor
- **Periodically:** When agents produce inconsistent code (symptom of stale context)

## Focus on the Unobvious

The template emphasizes facts agents **cannot infer from code**:

- WHY a framework was chosen (not just what it is)
- Rejected alternatives ("use Zustand, NOT Redux")
- Anti-patterns specific to this project
- Testing boundaries (what to unit test vs e2e)

## Template

See `templates/project-context-template.md` for the full structure.

## Gotchas

- Stale context is worse than no context — re-run `update` after major architecture changes
- The template asks for "rejected alternatives" — this is the highest-value content. If you chose Zustand over Redux, say WHY
- Don't list every file path — agents can Glob for that. Focus on RULES and CONVENTIONS
- `<!-- manual -->` sections survive `update` action but NOT `generate` — backup before regenerating from scratch
- If project-context.md conflicts with CLAUDE.md, CLAUDE.md wins (it's the higher-priority document)
- `init` refuses to overwrite an existing `docs/project-context.md` — this is intentional. Delete the file manually if you truly want to reset to a blank skeleton.

## Integration

All agents load `docs/project-context.md` in their Required Context section. If the file doesn't exist, agents behave exactly as before (graceful degradation).

## Files in this skill

- `SKILL.md` — you are here
- `templates/project-context-template.md` — output template used by `generate` action
- `templates/skeleton.md` — TODO-placeholder constitution template used by `init` action
