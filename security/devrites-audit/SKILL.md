---
name: devrites-audit
description: Audit one feature read-only for security, performance, or simplification risks. Use for one bounded audit axis; not for code changes.
argument-hint: "<security | perf | simplify>"
user-invocable: false
---
<!-- loads: {"always":["devrites-lib/reference/standards/core.md","devrites-lib/reference/standards/code-navigation.md","devrites-lib/reference/standards/code-index.md","devrites-lib/reference/parallel-dispatch.md","devrites-lib/reference/standards/agents.md"],"triggers":{"audit-coverage":["devrites-lib/reference/standards/audit-coverage.md"],"architecture-health":["devrites-lib/reference/standards/architecture-health.md"]},"workspace":["spec.md","plan.md","tasks.md","touched-files.md","evidence.md","state.md","decisions.md"],"workspaceByRole":{"performance-reviewer":["spec.md","plan.md","tasks.md","state.md","touched-files.md","evidence.md"],"security-auditor":["spec.md","plan.md","tasks.md","state.md","touched-files.md","evidence.md"],"simplifier-reviewer":["spec.md","plan.md","tasks.md","state.md","touched-files.md"]},"rootOnly":["devrites-lib/reference/standards/code-index.md","devrites-lib/reference/parallel-dispatch.md"]} -->
> Read-set manifest: `devrites-engine context <slug> --skill devrites-audit` (no workspace: `--out <path>`) bundles every file named below into one deduplicated read.

# devrites-audit: read-only audit dispatch

Dispatch one fresh-context, read-only review axis for the active feature. The caller
decides how to use the report; this skill never edits.

## Axis

| Argument | Role | Discipline |
|---|---|---|
| `security` | `devrites-security-auditor` | trust boundaries, OWASP, secrets, dependencies |
| `perf` | `devrites-performance-reviewer` | measure-first hot paths, N+1, payload/bundle and stated budgets |
| `simplify` | `devrites-simplifier-reviewer` | behavior-preserving deletion/simplification; Suggestion/Nit/FYI only |

If no axis is supplied, infer only when intent is unambiguous; otherwise the root asks
the human before dispatch.

When scope is a surface larger than the feature diff — subsystem, protocol surface,
repo sweep — apply [`audit-coverage.md`](../devrites-lib/reference/standards/audit-coverage.md)
(trigger `audit-coverage`). When the audit calls for a whole-codebase structural
score and a code index is present, apply
[`architecture-health.md`](../devrites-lib/reference/standards/architecture-health.md)
(trigger `architecture-health`).

## Gather and dispatch

1. Resolve `.devrites/ACTIVE`; require `spec.md` and `touched-files.md`.
2. Follow the bounded fresh-context native dispatch contract in
   [`agents.md`](../devrites-lib/reference/standards/agents.md).
3. Include `spec.md`, `decisions.md` when present,
   `evidence.md` for performance, `touched-files.md`, and the immutable diff.
4. Objective: derive expected behavior independently, apply the role's documented
   discipline, and return one labeled finding per line with `file:line`.
5. Wait for, validate, and pass the role result to the caller. The root
   reconciles and decides what to accept. A failed validation, timeout, or empty
   return reaches the caller as `Outcome: gap` naming the cause — never as no findings.

Use one task per axis. If several axes are requested, keep their inputs separate with
no cross-pollination; batch or serialize per
[`parallel-dispatch.md`](../devrites-lib/reference/parallel-dispatch.md) when readers
exceed ~3 per wave.

## Fallback and scope

If an exact named read-only role is unavailable, stop for HITL. Use these role contracts:

- `.claude/agents/devrites-security-auditor.md`
- `.claude/agents/devrites-performance-reviewer.md`
- `.claude/agents/devrites-simplifier-reviewer.md`

Stay inside the active feature. Critical findings block seal; simplification never
changes behavior.
