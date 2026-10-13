---
name: agent-based-development
description: "Full async multi-agent development workflow: Planning → Design → Dev → Security/Tech Review loop with file-based handoffs and release-branch Git model."
effort: high
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Agent-Based Development — Async Multi-Agent Workflow

Run a full async multi-agent software development workflow using file-based artifact handoffs. Each invocation adopts a specific agent role and operates according to that role's responsibilities.

This is the orchestrator skill. **Identify your single assigned role first** (from the slash command used or the latest plan artifact), then follow that role's skill. Do not attempt to act as multiple roles in one invocation.

## Framework Overview

This is an async, artifact-driven workflow. Agents do not communicate in real time — they communicate via JSON files in a `handoffs/` directory. The flow is:

```
Planning → Design → Dev (Senior / Junior)
       ↓                        ↓
  Documentation ← Security + Tech Review
       ↓                        ↓
  Planning (triage) ← findings with severity
```

All agents must follow the Golden Rules (see `CLAUDE.md` or run `/golden-rules`).

## Agent Roster

Role skills are namespaced by this plugin (e.g. `/agent-based-development:abd-plan`). Where your Claude Code resolves unambiguous bare names, the short form also works.

| Agent | Skill | When to Include |
|-------|-------|-----------------|
| Planning | [abd-plan](../abd-plan/SKILL.md) | Almost always — assigns tasks, triages reviews |
| Design | [abd-design](../abd-design/SKILL.md) | When the project has a design phase; omit for simple/script-only work |
| Dev Senior | [abd-dev-senior](../abd-dev-senior/SKILL.md) | When there is higher-complexity implementation work |
| Dev Junior | [abd-dev-junior](../abd-dev-junior/SKILL.md) | For routine tasks; omit for small teams |
| Security | [abd-security](../abd-security/SKILL.md) | Recommended for all projects |
| Tech Review | [abd-review](../abd-review/SKILL.md) | Recommended for all projects |
| Documentation | [abd-docs](../abd-docs/SKILL.md) | Almost always — docs, ToDo, changelogs, assumptions |
| Planning Triage | [abd-triage](../abd-triage/SKILL.md) | After reviews land — rework assignments |
| Testing | [abd-test](../abd-test/SKILL.md) | When the project has automated tests |
| DevOps | [abd-devops](../abd-devops/SKILL.md) | When the project has CI/CD or a formal release process |
| Status | [abd-status](../abd-status/SKILL.md) | At any time — shows project-wide task and finding status |

Active agents are defined in `docs/agentRoster.md`. If that file does not exist, Claude creates it at project start.

## Shared References

Every role reads these before acting:

- [shared/envelope.md](../../shared/envelope.md) — handoff directory structure, envelope schema, artifact rules, prompt-injection guard, assumptions log, output format
- [shared/git-rules.md](../../shared/git-rules.md) — release-branch Git model and responsibilities
- [shared/mvp-gate.md](../../shared/mvp-gate.md) — readiness checks before marking any task complete
- [shared/project-start.md](../../shared/project-start.md) — bootstrap procedure and prompt examples

## How to Use This Skill

**Step 1 — Determine context.** Use Glob to check if `handoffs/` exists in the current working directory.

**Step 2 — If no `handoffs/` directory exists (project start):** follow [shared/project-start.md](../../shared/project-start.md) — adopt the Planning role and bootstrap the project.

**Step 3 — If `handoffs/` exists (ongoing project):** read the latest artifact in `handoffs/plans/` using Read and Glob, determine which role is assigned, and follow that role's skill from the roster table above.

**Step 4 —** Follow the artifact rules, assumptions log, and output format in [shared/envelope.md](../../shared/envelope.md), and the Git rules in [shared/git-rules.md](../../shared/git-rules.md). Verify the [MVP gate](../../shared/mvp-gate.md) before marking any task complete.
