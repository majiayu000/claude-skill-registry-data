---
name: agent-harness-engineering
description: Bootstrap or upgrade a software repository for agent-first engineering. Use when a user wants to improve project-wide development discipline around `AGENTS.md`, progressive-disclosure docs, agent-readable architecture/context, mechanical quality checks, CI-enforced structure, or optional garbage-collection/maintenance loops.
---

# Agent Harness Engineering

Use this skill when the goal is to make a repository easier for coding agents to understand, change, and maintain over time.

This skill turns the main ideas from OpenAI's harness-engineering article into a reusable project pattern:

- `AGENTS.md` stays short and acts as a router
- durable knowledge moves into `docs/`
- context is disclosed progressively instead of dumped all at once
- quality rules become mechanical checks instead of tribal knowledge
- optional garbage collection keeps agent-generated entropy under control

## When to use it

Use this skill when the user asks to:

- create a reusable engineering skill for many repos
- bootstrap a repo for agent-first or AI-assisted development
- redesign `AGENTS.md` so it routes to structured docs
- add repo-readable architecture, spec, quality, reliability, or security docs
- add mechanical checks for doc freshness, structure, and agent guardrails
- add a low-friction cleanup loop for drift, stale docs, and code sprawl

## Choose a rollout mode

Pick the least invasive mode that still improves the repo.

- **`overlay`**: Default for existing repos. Add `docs/agent/` as an agent-readable overlay without rewriting existing docs.
- **`full`**: Use for greenfield repos or when the user explicitly wants a broader doc reorganization.

For most mature repos, start with `overlay`.

## First-use workflow

When applying this pattern to a repo for the first time, do the following in order:

1. Inspect the repo's current `AGENTS.md`, `docs/`, CI, and lint/test commands.
2. Run the bundled bootstrap script in `overlay` or `full` mode.
3. Review the generated `AGENTS.md` block and adapt command names to the repo.
4. Keep existing project-specific instructions, but move durable detail from `AGENTS.md` into the generated docs.
5. Wire the generated validation script into the repo's native check flow.
6. If the repo moves fast or uses many agents, optionally enable garbage collection.

## Bootstrap command

Run the bundled script from this skill directory:

```bash
python3 scripts/bootstrap_project.py --repo /path/to/repo --mode overlay
```

Optional flags:

- `--mode overlay|full`
- `--with-gc` to scaffold the garbage-collection report
- `--dry-run` to preview changes
- `--force` to overwrite generated files
- `--no-claude-link` to skip the `CLAUDE.md -> AGENTS.md` symlink

## What the bootstrap adds

On first application, the scaffold normally creates or updates:

- `AGENTS.md` with a short agent-navigation block
- `CLAUDE.md` symlink to `AGENTS.md` unless disabled
- `docs/agent/index.md`
- `docs/agent/architecture.md`
- `docs/agent/specs.md`
- `docs/agent/plans.md`
- `docs/agent/quality.md`
- `docs/agent/reliability.md`
- `docs/agent/security.md`
- `scripts/agent_repo_check.py`
- optionally `docs/agent/garbage-collection.md`
- optionally `scripts/agent_gc_report.py`

## Operating rules

### 1. `AGENTS.md` is a router

Do not turn `AGENTS.md` into a giant handbook.

- keep it short
- link outward to durable docs
- update links when docs move
- reserve `AGENTS.md` for task-routing instructions and repo-specific operational constraints

### 2. Durable knowledge lives in docs

Put medium- and long-lived repo knowledge in `docs/agent/` or the repo's main docs tree.

Examples:

- architecture boundaries
- product or integration specs
- current plans
- quality gates and invariants
- reliability expectations
- security assumptions and trust boundaries

### 3. Progressive disclosure beats giant prompts

Only read the docs needed for the task.

- start at `docs/agent/index.md`
- open the relevant leaf docs
- avoid loading unrelated docs into context
- add new docs to the index so future agents can discover them quickly

### 4. Mechanical checks beat soft reminders

Prefer checks that can fail fast in CI or local validation:

- missing required docs
- missing frontmatter fields
- stale review dates
- docs not linked from the index
- `AGENTS.md` missing navigation links

### 5. Garbage collection is optional but useful

Enable the GC loop when the repo has high change velocity, many generated edits, or recurring drift.

The default GC report looks for:

- stale docs
- oversized files
- suspicious filenames like `final-final` or `v2`
- lingering `TODO` or `FIXME` clusters
- docs that are not linked from the index

## References to read only when needed

- Read `references/bootstrap-playbook.md` when planning the first rollout for a repo.
- Read `references/docs-blueprint.md` when adapting the doc taxonomy or frontmatter.
- Read `references/quality-gates.md` when wiring checks into CI or repo-native tooling.
- Read `references/garbage-collection.md` when enabling scheduled cleanup or review loops.

## Acceptance checklist

Before you finish a rollout, confirm:

- `AGENTS.md` routes to docs instead of duplicating them
- `docs/agent/index.md` points to every active leaf doc
- the generated docs have owners and `last_reviewed` dates
- `scripts/agent_repo_check.py` passes
- the repo's native check command includes the validation script or an equivalent wrapper
- garbage collection is either enabled intentionally or documented as deferred

## Do not do this

- do not rewrite a mature doc system unless the user asks
- do not duplicate the same guidance in `AGENTS.md` and `docs/agent/*`
- do not add stack-specific CI assumptions without checking the repo
- do not enable automatic destructive cleanup; GC should surface candidates, not delete code blindly
