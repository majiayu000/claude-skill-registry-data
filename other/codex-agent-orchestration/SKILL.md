---
name: codex-agent-orchestration
description: Set up and run Codex custom subagent orchestration for software projects. Use when a user wants a project-local `.codex/agents/*.toml` team, an `AGENTS.md` orchestration contract, a software-factory workflow, parallel Codex subagents, or reusable agent chains such as architect to backend/frontend to tester/security/reviewer.
metadata:
  short-description: Orchestrate project Codex subagents
---

# Codex Agent Orchestration

## Overview

Use this skill to turn any repository into a Codex-orchestrated software team. The project-local layer is `.codex/agents/*.toml`; the reusable workflow layer is this skill; the repo instruction layer is `AGENTS.md`.

Generated agents are named by project, role, and job so their purpose is clear at a glance, for example `companyos_backend_api_service_builder` or `companyos_tester_regression_checker`.

Prefer the bundled generator for new or updated projects:

```bash
python /path/to/codex-agent-orchestration/scripts/generate_project_agents.py --project .
```

If the skill is installed in Codex, the generator usually lives at:

```bash
python ~/.codex/skills/codex-agent-orchestration/scripts/generate_project_agents.py --project .
```

Read [agent-team-template.md](references/agent-team-template.md) only when manually customizing the generated files.

## Setup Workflow

1. Inspect the repository shape and existing instructions.
2. Run `generate_project_agents.py --project <repo>` to synthesize the agent team from detected project signals.
3. Review the generated plan in the script output. Re-run with `--dry-run` first when the repository already has hand-written `.codex` files or an `AGENTS.md`.
4. Keep or tune the generated agents. Default names use `<project>_<role>_<job>`. Use `--generic-names` only when the user prefers portable names such as `architect_plan_mapper` and `reviewer_quality_gate_reviewer`.
5. Validate TOML syntax and confirm every custom agent defines `name`, `description`, and `developer_instructions`.

## Running The Team

For substantial work, orchestrate this default chain:

1. Spawn architect or explorer to inspect the repo and produce a plan.
2. Wait for the plan.
3. Spawn independent implementers in parallel only when they can avoid editing the same files.
4. Wait for implementers and reconcile their results in the parent session.
5. Spawn tester and reviewer. Add security when auth, permissions, payments, secrets, untrusted input, deployment, or compliance are involved.
6. Route critical or high findings back to the smallest relevant implementation agent.
7. Rerun tester and reviewer after fixes.
8. Return a parent-session final summary with changed files, verification, risks, and unresolved items.

Use direct instructions such as:

```text
Use the project Codex agent team. Have the architect map the work first, then delegate backend and frontend changes in parallel if they do not touch the same files. Run tester and reviewer before the final summary.
```

## Guardrails

- Do not spawn write-capable agents against overlapping files at the same time.
- Do not let subagents commit, push, publish, deploy, rotate secrets, or change permissions unless the user explicitly requested that outcome and the parent session handles approval.
- Keep raw logs and broad exploration in subagents; return distilled results to the parent.
- Keep the parent session responsible for structured output schemas, final user-facing decisions, and cross-agent conflict resolution.
- Prefer high-reasoning models for architect, security, reviewer, and ambiguous fixes. Prefer faster models for read-heavy scans and narrow repetitive work when configured by the project.
