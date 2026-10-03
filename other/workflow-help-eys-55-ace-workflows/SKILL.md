---
name: workflow-help
description: Show the available ace-workflows skills, scripts, task states, AGENTS.md boundaries, and safe next actions. Use when the user asks what skills exist, how to start, why slash commands/prompts are unavailable, or which workflow skill to invoke next.
---

# Workflow Help

Use this skill to explain what the workflow repo can do right now. This is a
read-only guide surface.

## Skill-First Runtime Rule

Root `AGENTS.md` is the source of truth: this foundry builds skill-first
workflow packs for Codex, Claude Code, opencode, and Antigravity-style
environments. Lead with `$skill-name` surfaces. Treat scripts as state helpers
or validation support, not as the primary way to call skills.

## Required Reading

Before answering:

1. Read root `AGENTS.md`.
2. Read `references/matt-pocock-skills.md`.
3. Read `registry/agents-md.json`.
4. Inspect `.agents/skills/` and `scripts/` so the answer reflects the actual
   repo.
5. Load the derived skill catalog, project list, and registered project
   instructions through the read-only state helper when available.

Do not mutate project or task state from this skill.

## What To Show

Report the currently available surfaces in this order. Never reproduce a
hand-maintained skill inventory; render every row returned by the derived
catalog query.

```text
ACTIVE SKILL CATALOG
- $skill-name: trigger description; runtime visibility; runtime targets; bundle path
```

## Query Helper

These commands are deterministic validation and read-only query support. They
are not the operator-facing workflow invocation surface.

```text
node scripts/validate-workflow-state.mjs
node scripts/query-workflow-state.mjs --skill-catalog
node scripts/query-workflow-state.mjs --list-projects
node scripts/query-workflow-state.mjs --list-agents-md
node scripts/query-workflow-state.mjs --project <slug> --agents-md
node scripts/query-workflow-state.mjs --project <slug> --snapshot
node scripts/query-workflow-state.mjs --project <slug> --testing-sessions
node scripts/query-workflow-state.mjs --project <slug> --list-tasks
node scripts/query-workflow-state.mjs --project <slug> --task <task-id>
node scripts/query-workflow-state.mjs --project <slug> --task-readiness <task-id>
node scripts/testing-session-state.mjs action:start project:<slug> [goal:"..."]
node scripts/testing-session-state.mjs action:status session:<session-id>
node scripts/testing-session-state.mjs action:stop session:<session-id>
```

## Report Layout

```text

TASK FLOW
- setup project
- initiate task
- continue task
- review project state
- audit foundry state
- follow Matt Pocock phases inside the selected task

CONNECTED FLOW
- $workflow-help -> $setup-workflow-project -> $initiate-task -> $continue-task
- raw create/update-skill intent -> $initiate-task or $continue-task -> approved contract -> $build-workflow-skill
- $audit-foundry -> Markdown report artifact -> recommended next tracker action
- $audit-foundry -> $audit-review -> Markdown cleanup plan -> $audit-cleanup
- $testing-session -> captured project run state -> future preload discovery
- use $continue-task or $review-project-state when project state already exists
```

## Routing Guide

- Use the catalog trigger descriptions to choose an active skill. Do not infer
  availability from a remembered name or Markdown list.
- Use `$setup-workflow-project` only when the project workspace is absent.
- Use `$initiate-task` for a new typed deliverable contract and `$continue-task`
  for an existing task.
- Route a create-skill or update-skill request through lifecycle approval, then
  delegate only the implementation-ready contract to `$build-workflow-skill`.
- Route create-UI, revamp-UI, workflow-product, or local-sidecar intent through
  the existing or newly approved target-project `ui-application` plus callable
  skill contracts, then delegate the selected task to
  `$build-workflow-product`. Do not create a duplicate workflow task.
- Use the audit family for evidence-first reporting, review, and approved
  cleanup. Preserve each skill's mutation boundary.
- Use `$testing-session` for isolated read-only run capture and
  `$review-project-state` for complete state inspection.

## Matt Flow Reminder

`target:tracker` is not a Matt phase. It creates a `tracker-maintenance` task at
`intake` for auditable changes to `project.json`, `tasks/index.json`, task JSON
files, or `registry/agents-md.json`.

Matt Pocock phases are not separate repo-local skills:

```text
intake -> grilling -> prd -> issues -> implement -> code-review -> done
```

They happen inside the selected task. Do not create separate local helper skills
for PRD, issues, implementation, or review phases.

## AGENTS.md Boundary Reminder

Root `AGENTS.md` owns workflow-foundry mechanics: tasks, JSON state, Matt/ECC
flow, validation, file policy, and checkpoints.

Project `AGENTS.md` files live under `projects/<slug>/AGENTS.md` and are
project/domain-only. For example, a healthcare project AGENTS.md may define
healthcare vocabulary and lung-specific guidance, but it must not redefine task
tracking or root workflow mechanics.

Every live `AGENTS.md` must be registered in `registry/agents-md.json`.

## Safety Rules

- Python files are forbidden.
- JSON is the source of truth for project/task state.
- `.agents/skills` is the source of truth for skill instructions.
- Markdown is the source of truth for references, artifacts, reviews, and
  handoffs.
- `.mjs` is allowed only for JSON query/validation helpers.
- Do not present `npx`, `npm`, Python, or raw helper commands as the primary
  operator path for calling a workflow skill.
- Task work must load `project.json`, `tasks/index.json`, and every non-done
  task JSON first.
- Task work must load root `AGENTS.md`, the registry, and project `AGENTS.md`
  first.

## Output Contract

When invoked, answer in this shape:

```text
AVAILABLE SKILLS
- derived skill: trigger, visibility, runtime targets, and path

CONNECTED FLOW
- current recommended path

LIVE STATE
- projects and registered AGENTS.md files seen

STATE HELPERS
- script: what it shows or validates

RECOMMENDED NEXT ACTION
- one concrete next skill based on the user's request
```
