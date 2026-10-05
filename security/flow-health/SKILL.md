---
name: flow-health
description: Diagnose repository and PWDEV Flow health without changing the project. Use when the user asks for a health check, workspace consistency check, dependency assessment, readiness report, or evidence-based scorecard.
---

# Diagnose PWDEV Flow Health

Read [health](../../references/health.md), [artifacts](../../references/artifacts.md), [audit](../../references/audit.md), and [safety](../../references/safety.md) before collecting evidence.

## Route

Choose exactly one mode from the request:

- `full` for repository, Flow workspace, local quality checks, documentation, Git, dependencies, and locally available security checks;
- `workspace` for Flow structure, state, gates, links, memory, audit, and migration consistency;
- `deps` for manifests, lockfiles, locally available dependency checks, and freshness evidence.

Default to `full` only when the user asks for a general health check. State the selected mode before running commands.

## Procedure

1. Read applicable `AGENTS.md`, then inspect Flow config, state, manifests, and relevant artifacts without opening secret files.
2. Discover verification commands from repository governance and manifests. Do not invent package-manager commands.
3. Run only read-only or non-mutating checks already available locally. Keep network-backed checks separate and request authorization before using them.
4. For `workspace`, validate links, phase/state agreement, gate evidence, memory index targets, migration records, and audit integrity with [flow_audit.py](../../scripts/flow_audit.py) when a trail exists.
5. Classify findings by severity and grade each applicable area `A` through `F` using the health contract. Use `N/A` for unavailable evidence, never as a passing grade.
6. Recommend bounded next actions but do not implement them.

## Constraints

- Remain read-only: do not install packages, update lockfiles, repair audit data, edit state, or apply findings.
- Do not treat a missing optional tool, unavailable network, or stale external database as a product failure; report the limitation and confidence.
- Persist a report only when the user requests it or an active Flow contract already authorizes it.

## Output

Return `MODE`, urgent findings first, a scorecard with evidence and confidence, limitations, `OVERALL`, and `NEXT`. Link persisted reports with absolute local paths.
