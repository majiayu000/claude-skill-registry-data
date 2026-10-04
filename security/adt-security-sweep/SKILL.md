---
name: security-sweep
description: Composite skill — full security pass across secrets, dependencies, code paths, and OWASP risks. Chains security-audit (broad) + socket-audit (npm supply chain) + semgrep (pattern scan) + code-security (code review for vulns) in parallel, reconciles into one severity-ranked report with remediation plan. Use quarterly per active repo or before any release of security-sensitive code.
triggers:
  - security-sweep
  - quarterly-per-repo
  - pre-security-release
  - post-incident
  - composite skill
  - release
  - security
---

# Security Sweep

Replaces "ran one security tool, called it done" with one workflow that runs all of
them in parallel and reconciles findings so duplicates and false positives don't
clutter the actionable list.

## Auto-invocation triggers

- User says "security audit", "check for vulns", "is this safe to deploy"
- Quarterly per active repo (manual cadence — not auto-scheduled to avoid noise)
- Before any release of security-sensitive code (auth, payments, PII, file uploads)
- Post-incident as part of `production-incident` Phase 6 if the incident was
  security-related

## Workflow

### Phase 1 — Parallel scan dispatch (always)
Invoke in parallel:
- `security-audit` — broad OWASP-style review (secrets, deps, code paths)
- `socket-audit` — npm supply chain (malicious packages, typosquats) — npm only
- `semgrep` — pattern-based scan (custom rules + community packs)
- `code-security` — review of recent diffs for unsafe patterns

Each returns structured findings.

### Phase 2 — Reconcile + dedupe (always)
Combine findings into one set:
- Same vulnerability flagged by multiple tools → keep one entry, list which tools
  caught it (high-confidence finding)
- Conflicting severity ratings → take the highest
- False positives the user has documented before (read memory) → suppress

Severity ranking:
- **CRITICAL** — exploitable now, in prod, no mitigation
- **HIGH** — exploitable but mitigated by other controls, or only on auth paths
- **MEDIUM** — limited exploitability, fix in the next release
- **LOW** — best-practice violations, no immediate risk
- **INFO** — track only

### Phase 3 — Remediation plan (always)
For each CRITICAL + HIGH:
- Specific fix with code snippet or command
- Estimated effort (5min / 30min / 2h / day+)
- Recommended skill to apply: `secrets-rotate` (if secrets), `refactor-pipeline`
  (if structural), direct edit (if simple)

Sort by impact-per-effort.

### Phase 4 — Capture
Write report to `~/.claude/projects/<slug>/memory/security_sweep_<repo>_<date>.md`.
Update MEMORY.md index. Trend visible across quarterly runs.

If CRITICAL findings: also create Linear ticket via `incident-response` (without
the full incident workflow — just ticket creation).

## Reconciliation

```
SECURITY SWEEP — <repo> — <date>

Tools run:   security-audit, socket-audit, semgrep, code-security
Total findings: N (after dedup)

CRITICAL (X):
  [tool1, tool2] <finding>
                 Fix: <action>, estimated <effort>

HIGH (Y):  ...
MEDIUM (Z): ...
INFO (W): ...

Remediation plan (impact-per-effort sorted):
  1. <action>  (5min, fixes 1 CRITICAL)
  2. <action>  (30min, fixes 2 HIGH)
  3. <action>  (2h, fixes 1 HIGH + 3 MEDIUM)

Linear: <ticket URL if CRITICAL findings>
Memory: <report path>
```

## Outputs / Evidence

- Per-tool raw verdicts
- Reconciled severity-ranked finding list
- Effort-sorted remediation plan
- Memory file for trend tracking
- Linear ticket if CRITICAL

## Failure / Stop Conditions

- Any single tool errors → mark partial, continue with the rest
- All tools clean → write a "no findings" memory; clean baseline is itself evidence
- Tool unavailable (e.g., semgrep not installed) → skip + note in report; don't
  block the rest

## Memory Hooks

- Read prior reports to surface trend (e.g., "secrets-in-config CRITICAL flagged
  3 quarters running — structural fix needed")
- Read documented false-positive list to suppress noise
- Write report as primary output
