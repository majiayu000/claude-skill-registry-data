---
name: audit-deep
description: Composite skill — full project health check across testing, config, hooks, performance, security, MCP, and plugins. Runs the audit skills in parallel and reconciles into one severity-ranked report with prioritized remediation plan. Use weekly per active project, before major releases, or as part of quarterly tech-debt review.
triggers:
  - audit-deep
  - weekly-per-repo
  - pre-release
  - tech-debt-review
  - composite skill
  - audit
---

# Audit Deep

Runs every audit skill in parallel against one repo, reconciles findings by severity,
and proposes a single prioritized remediation plan. Replaces the "run six audits
manually and try to remember what each said" pattern.

## Auto-invocation triggers

- User asks "is this project healthy", "audit this repo", "tech debt review"
- Weekly per-active-repo via launchd (combine with diagnostic-skills schedule)
- Pre-release (before any version bump on a production-bound repo)
- After significant architecture change or new team member onboarding

## Workflow

### Phase 1 — Parallel audit dispatch (always)
Invoke in parallel via Agent tool or sequential Skill calls:
- `test-health` — suite proportionality, coverage, runtime
- `config-drift-detect` — gate compatibility
- `hook-effectiveness` — hooks fire/exit/latency stats
- `performance-audit` or `performance-test` — runtime perf
- `security-audit` — secrets, deps, OWASP
- `mcp-audit` — MCP server usage
- `plugin-audit` — plugin enabled-vs-used
- `socket-audit` — supply chain (npm only)
- `forge-audit` — if Forge ecosystem repo

Each returns a structured verdict + findings.

### Phase 2 — Reconcile by severity
Aggregate all findings into one ranked list:
- CRITICAL — blocks merge / release / production safety
- HIGH — degrades workflow significantly
- MEDIUM — measurable but not blocking
- INFO — track but no action

Cross-reference: a HIGH from `config-drift` that explains a HIGH from `test-health`
is reported as one root cause, not two findings.

### Phase 3 — Remediation plan
For each CRITICAL + HIGH:
- Recommend the specific composite skill to fix it (`fix-the-suite`,
  `secrets-rotate`, `gate-relax`, etc.)
- Estimate the effort
- Sort by impact-per-effort

### Phase 4 — Memory + handoff
Write the report to `~/.claude/projects/<slug>/memory/audit_deep_<repo>_<date>.md`
so trends are visible across audits. Update MEMORY.md index.

## Reconciliation

Single report:
```
AUDIT DEEP — <repo> — <date>

Overall health:  <SCORE/100>

CRITICAL (N):
  [test-health]    1467 tests vs target 40-150 (37x ceiling)
                   Root cause: [config-drift] 99% functions gate
                   Fix: /fix-the-suite (estimated 2-4h)

HIGH (N):
  [hook-effectiveness] turn-counter spam every 10 turns
                       Fix: applied 2026-05-08 (commit 04ec576)

  [security-audit] 2 high-severity vulns in transitive deps
                   Fix: /dependency-update-batch (estimated 30min)

MEDIUM (N): ...
INFO (N):   ...

REMEDIATION PLAN (ranked by impact-per-effort):
  1. /fix-the-suite (resolves 1 CRITICAL + 2 MEDIUM)
  2. /dependency-update-batch (resolves 1 HIGH)
  3. /secrets-rotate ANTHROPIC_API_KEY (it's been 90 days)
```

## Outputs / Evidence

- Per-audit raw verdicts
- Reconciled severity-ranked findings
- Effort-sorted remediation plan
- Memory file written for trend tracking

## Failure / Stop Conditions

- Any audit skill errors → mark as PARTIAL, continue with the rest
- All audits return CLEAN → write a "no findings" memory; a clean baseline is
  itself valuable evidence
- If user invokes during active development → defer non-blocking audits to next
  scheduled run; only run the ones gating immediate work
