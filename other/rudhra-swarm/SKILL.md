---
name: rudhra-swarm
description: Orchestrate multiple specialized agents or agent roles for a project. Use when the user says "rudhra swarm", "spin multiple agents", "orchestrate agents", "parallel agents", "agent team", "multi-agent review", or asks Rudhra to split work across mapper, researcher, implementer, tester, reviewer, and learning roles.
---

# Rudhra Swarm

Use this skill when one agent should coordinate several focused roles.

## Default Roles

Use only the roles needed for the task:

| Role | Job |
|---|---|
| `orchestrator` | Owns the plan, integration, final decisions, and user communication |
| `repo-mapper` | Reads repo structure, key configs, commands, architecture, and risk areas |
| `docs-researcher` | Checks official docs or source-backed references for current guidance |
| `implementer` | Makes the smallest complete code/doc/config changes |
| `test-runner` | Runs targeted checks, summarizes failures, and avoids noisy logs |
| `reviewer` | Reviews final diff for bugs, regressions, missing tests, and risk |
| `learning-capturer` | Drafts reusable lessons for `agent/PROMOTE.md`; never applies them silently |

## Workflow

1. Read `AGENTS.md`, `CLAUDE.md`, `agent/PROJECT_CONTEXT.md`, and `agent/WORKFLOW.md`.
2. Choose a swarm size:
   - `small`: orchestrator + repo-mapper + reviewer
   - `medium`: small + implementer + test-runner
   - `large`: medium + docs-researcher + learning-capturer
3. State the role split briefly before starting substantial work.
4. Run roles in parallel when the environment supports subagents. If real subagents are unavailable, simulate the roles sequentially with clear headings.
5. Integrate results in the orchestrator role. Do not let subagents independently commit, push, deploy, or edit the master template.
6. End with a learning capture pass:
   - project-specific lesson -> project `AGENTS.md`, `CLAUDE.md`, or `agent/PROJECT_CONTEXT.md`
   - reusable lesson -> draft row for `agent/PROMOTE.md`
   - master-template change -> only via `harvest-template-lessons` after approval

## Approval Rules

- Ask before deployment, DNS, production data changes, or destructive commands.
- Ask before adding dependencies.
- Ask before promoting lessons into the master template.
- Do not auto-commit or auto-push unless the user explicitly asks.

## Output Shape

Keep the final response short:

- roles used
- changes made
- checks run
- learnings drafted for approval
