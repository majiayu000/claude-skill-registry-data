---
name: setup-workflow-project
description: Set up a new workflow project in this repo by creating the JSON project state, task index, artifact folders, and project-level ECC concept notes under projects/<project-slug>/. Use when the user asks to create, initialize, or set up a workflow project.
---

# Setup Workflow Project

Use this skill to initialize a project workspace. It creates project-level JSON
state; it does not create a task unless the user also invokes task initiation.

## Skill-First Runtime Rule

Follow root `AGENTS.md`: workflow projects are built as skill-first packages for
agent runtimes. Use `$skill-name` workflow surfaces for operator actions.
Command helpers may support validation or setup internals, but they are not the
primary skill-calling surface.

## Required Reading

Before acting:

1. Read root `AGENTS.md`.
2. Read `references/matt-pocock-skills.md`.
3. Read `.agents/skills/initiate-task/SKILL.md` for the task state contract.
4. Read `registry/agents-md.json`.

## Inputs

Require:

- `project:<slug>`

Accept:

- `name:"..."`
- `goal:"..."`
- `domain:"..."`

If `project:<slug>` is missing, ask for it and stop.

## Project Scaffold

Create:

```text
projects/<project-slug>/
  AGENTS.md
  project.json
  tasks/
    index.json
  artifacts/
    prds/
    issues/
    reviews/
    handoffs/
```

Do not overwrite existing project files. If the project already exists, load it,
report its state, and hand off to `$review-project-state` before changing it.
Do not modify an existing project from this skill unless the user explicitly
asks after reviewing the project state.

Register `projects/<project-slug>/AGENTS.md` in `registry/agents-md.json` with:

```json
{
  "path": "projects/health/AGENTS.md",
  "role": "project-domain",
  "scope": "projects/health",
  "owning_project": "health",
  "live": true,
  "allowed_content": [
    "project domain behavior",
    "project vocabulary",
    "project source rules",
    "project agent workflow guidance"
  ]
}
```

Project `AGENTS.md` is domain-only. Root `AGENTS.md` owns workflow/task
mechanics.

## JSON Contract

Create `project.json`:

```json
{
  "project_slug": "health",
  "name": "Health",
  "project_state": "active",
  "goal": "",
  "domain": "",
  "agents_md": "projects/health/AGENTS.md",
  "active_conventions": [],
  "ecc_concepts_applied": [
    "workflow contract",
    "human boundary",
    "project state preload"
  ],
  "created_at": "YYYY-MM-DD",
  "updated_at": "YYYY-MM-DD"
}
```

Create `AGENTS.md`:

```markdown
# Health Project AGENTS.md

This file contains live project/domain instructions for the `health` workflow
project only.

Root `AGENTS.md` owns task tracking, JSON state, Matt Pocock flow, ECC workflow
rules, validation, and repo-wide safety. Do not redefine those mechanics here.

Use this file for:

- domain vocabulary
- project-specific source rules
- project-specific output expectations
- agent behavior for this project domain
```

Create `tasks/index.json`:

```json
{
  "project_slug": "health",
  "tasks": []
}
```

## Output Contract

Report:

```text
PROJECT
- slug
- project_state
- files created or already present
- registered AGENTS.md path

ECC CONCEPTS
- concepts recorded

NEXT ACTION
- initiate a task with $initiate-task
```

For a newly created project, the next surface is:

```text
$initiate-task project:<project-slug> title:"..."
```

For an existing project, the next surface is:

```text
$review-project-state project:<project-slug>
```

## Developer Verification

Run:

```bash
node scripts/validate-workflow-state.mjs
```
