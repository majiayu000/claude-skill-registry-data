---
name: audit-foundry
description: Write a Markdown audit report for the ace-workflows foundry or project trackers. Use when the operator asks to audit the foundry, explain current workflow state, review all foundry tasks, generate a foundry report, inspect project tracker health, or produce a durable state-of-everything report.
---

# Audit Foundry

Use this skill to write a durable Markdown audit report, then summarize the
report in chat. The audit is read-only against workflow source state. The only
normal write is the audit report artifact.

## Skill-First Runtime Rule

Follow root `AGENTS.md`: this audit reports whether the foundry remains
skill-first and agent-runtime-first. Query helpers may support evidence
gathering, but audit usage starts from `$audit-foundry`, not command-first
workflow invocation.

## Invocation

Supported forms:

```text
$audit-foundry
$audit-foundry scope:foundry-projects
$audit-foundry scope:projects
$audit-foundry project:<slug>
```

Default to foundry-only when no scope or project slug is provided.

## Required Reading

Always start from the repo root and read:

1. Root `AGENTS.md`.
2. `references/matt-pocock-skills.md`.
3. `registry/agents-md.json`.
4. `projects/workflow-foundry/AGENTS.md`.
5. `projects/workflow-foundry/project.json`.
6. `projects/workflow-foundry/tasks/index.json`.
7. Every non-done `projects/workflow-foundry/tasks/<task-id>.json`.
8. `.agents/skills/workflow-help/SKILL.md`.
9. `.agents/skills/review-project-state/SKILL.md`.
10. `scripts/query-workflow-state.mjs`.
11. `scripts/validate-workflow-state.mjs`.

## Query Helper

Use the query helper as internal evidence support when available:

```bash
node scripts/query-workflow-state.mjs --project workflow-foundry --list-tasks
node scripts/query-workflow-state.mjs --project workflow-foundry --agents-md
node scripts/query-workflow-state.mjs --project workflow-foundry --testing-sessions
```

## Scope Branches

### Foundry Only

Use for `$audit-foundry`.

Audit the workflow-foundry control plane:

- root and workflow-foundry `AGENTS.md` boundaries
- registry alignment
- workflow-foundry `project.json`
- workflow-foundry task index and every non-done task JSON
- Codex-discoverable skills under `.agents/skills`
- derived canonical skill catalog completeness and invocation identity
- open-task deliverable migration, contract, artifact binding, eval, and
  dependency readiness blockers
- validation and query helper surfaces
- generated tracker UI state by reading linked task/artifact pointers
- testing-session index summaries when present

### Foundry Plus Projects

Use for `scope:foundry-projects`.

Complete the foundry-only audit, then load each discoverable project:

1. Query the registered project list through the read-only state helper.
2. For each project, read `AGENTS.md`, `project.json`, `tasks/index.json`, and
   every non-done task JSON.
3. Run project `--agents-md`, `--list-tasks`, and `--testing-sessions` helper
   calls when available.

Do not load full project artifacts, full testing-session event streams, or
quarantined import bodies unless a finding needs exact evidence.

### Projects Only

Use for `scope:projects`.

Load discoverable project trackers as in the project branch, but keep the report
focused on project health instead of foundry control-plane analysis.

### Specific Project

Use for `project:<slug>`.

Require the named project to exist. Read its `AGENTS.md`, `project.json`,
`tasks/index.json`, every non-done task JSON, and testing-session index summary
when present. Use exact evidence only when a finding needs it.

## Report Artifact

Always write a Markdown report before final chat response.

Store reports under:

```text
projects/workflow-foundry/artifacts/reviews/
```

Use these filename patterns:

```text
audit-foundry-YYYY-MM-DD-foundry.md
audit-foundry-YYYY-MM-DD-foundry-projects.md
audit-foundry-YYYY-MM-DD-projects.md
audit-foundry-YYYY-MM-DD-project-<slug>.md
```

If a file already exists for the same day and scope, append a short timestamp
before `.md`.

## Report Template

Every report must include:

```text
# Audit Foundry Report

Task/Invocation:
Generated:
Scope:

## Executive Summary
## Loaded Sources
## Foundry State
## Project State
## Skill Surface
## Tracker And Registry Health
## Validation Status
## Generated UI And Testing State
## Findings
## Recommended Next Tracker Actions
## Boundaries And Deferred Work
```

Use `Not in scope for this report.` for sections that do not apply.

## Findings

Classify findings as:

```text
critical, high, medium, low, note
```

Each finding should include:

- what is wrong or worth noting
- evidence file or command
- impact
- recommended next tracker action

Report missing contracts, pending migrations, unbound phase approvals, missing
primary artifacts, missing eval evidence, incomplete dependency outcomes, and
catalog bundle errors. Do not repair, classify, or migrate tasks from this
read-only skill; route those actions through the owning task and tracker
maintenance authority.

Do not fix findings inside this skill.

## Boundaries

- Do not edit source state except for the audit report artifact.
- Do not change task status, task phase, registry entries, skills, scripts,
  project files, generated UI, or testing-session state as part of an audit.
- Do not create or continue follow-up tasks from this skill.
- Recommend `$initiate-task` or `$continue-task` for follow-up work.
- Do not treat quarantined imports as active skills.

## Final Response

After writing the report, respond with:

```text
REPORT
- path
- scope

SUMMARY
- highest-signal findings
- recommended next tracker action

VALIDATION
- commands run, or not run with reason
```
