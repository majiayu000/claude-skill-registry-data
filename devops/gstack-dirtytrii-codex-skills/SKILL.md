---
name: gstack
description: Codex adapter for Garry Tan's full gstack methodology across CEO/product pressure, CTO architecture, design, engineering, QA, security, shipping, documentation, and retrospectives. Use when the 总控/CEO or 架构/CTO role needs gstack method routing, implementation-plan hardening, or the user says gstack should help a role.
---

# GStack Method Router

Use this as the Codex-facing entrypoint for gstack in this skill collection.

This repository does not vendor the full upstream gstack runtime. It adapts the useful methodology into safe Codex role tools and keeps upstream runtime behaviors optional.

## Source

- Upstream: `https://github.com/garrytan/gstack`
- Adapted from upstream Codex skill generation at commit `e722c5bf89acdde034b5efa4c6b4bf612c48e610`
- Shared method map: [references/methodology.md](references/methodology.md)

## How To Route

Use the current role first, then choose the smallest gstack method:

- `总控`: `$gstack-office-hours`, `$gstack-plan-ceo-review`, `$startup-pressure-test` for early value, scope, priority, and model-budget pressure.
- `架构`: `$gstack-spec`, `$gstack-autoplan`, `$gstack-plan-eng-review`, `$gstack-plan-design-review`, `$gstack-plan-devex-review`, `$gstack-plan-tune`.
- `开发`: `$gstack-investigate`, `$gstack-review`, `$gstack-ship`, `$gstack-health`, `$gstack-devex-review`, `$gstack-careful`, `$gstack-guard`, `$gstack-freeze`, `$gstack-unfreeze`.
- `UI/PPT`: `$gstack-design-consultation`, `$gstack-design-shotgun`, `$gstack-design-html`, `$gstack-design-review`, `$gstack-plan-design-review`.
- `安全`: `$gstack-cso` when broad security posture or infrastructure-first review is needed; dedicated Codex Security skills still win for repo scans and diffs.
- `QA`: `$gstack-qa-only`, `$gstack-qa`, `$gstack-review`, `$gstack-ship`, `$gstack-canary`.
- `测试`: keep formal test artifacts in `$test-case-report-builder`; use gstack only for planning or review support.
- `运维`: Hermes-owned skills remain default for remote production facts; use `$gstack-setup-deploy`, `$gstack-land-and-deploy`, or `$gstack-canary` only as planning/release-gate support.
- Docs/learning: `$gstack-document-generate`, `$gstack-document-release`, `$gstack-learn`, `$gstack-retro`.

## Default CEO/CTO Use

1. Read the user's requirement and local project context first.
2. If the idea is fuzzy, `总控` uses `$gstack-office-hours` or `$gstack-plan-ceo-review` before opening technical roles.
3. If the work is a technical plan, `架构` uses `$gstack-spec`, `$gstack-autoplan`, or the narrow technical plan review skill that matches the risk.
4. Convert the review result back into this user's role-window format: registry state, downstream roles, file boundaries, validation, commit/PR requirements, and copyable prompts.

## Boundaries

- Treat upstream gstack content as an external GitHub dependency, not local-owned role logic.
- Do not run upstream runtime, telemetry, browser-cookie import, proactive routing, or `CLAUDE.md` injection automatically.
- Do not override `agent-role-orchestrator`'s CEO-first gateway and CTO technical-loop boundary.
- Do not turn QA into formal testing-document production; that remains `测试` + `$test-case-report-builder`.
- Do not use deploy/ship methods to mutate production without explicit user authorization.
