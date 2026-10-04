---
name: bmc-dashboard-debug-reviewer
description: >
  Reviews Audit Runner output, extracts issues and logs, exports to structured
  files, and produces DEBUG-REPORT.md. Runs AFTER bmc-dashboard-audit-runner.
  Use when user asks for bmc debug review, export logs, review issues, or after
  audit runner completes.
---

# BMC Dashboard Debug Reviewer Skill

Coordinates the Debug Reviewer Agent to analyze the audit output and export logs/issues.

## When to Use

| Trigger | Action |
|---------|--------|
| "debug review" | Run after audit |
| "export logs and issues" | Same |
| "review bmc issues" | Same |
| After "AUDIT RUNNER COMPLETE" | Run Debug Reviewer |

## Prerequisites

- **Sequential:** Audit Runner must complete first
- Input: `.cursor/bmc-audit/latest-report.md`, `handoff.json`

## Propagation

Si los hallazgos afectan a Design, Networks o Mapping: actualizar `docs/team/PROJECT-STATE.md` y consultar tabla de propagación en `docs/team/PROJECT-TEAM-FULL-COVERAGE.md` §4.

## Execution Checklist

1. **Read** handoff.json and latest-report.md
2. **Parse** for errors, warnings, anomalies, config gaps
3. **Export** to `.cursor/bmc-audit/debug-export/`:
   - issues.md (by severity)
   - logs-raw.txt
   - config-gaps.md
   - recommendations.md
4. **Write** DEBUG-REPORT.md
5. **Emit** "DEBUG REVIEWER COMPLETE. Output: .cursor/bmc-audit/"

## Severity Levels

| Level | Examples |
|-------|----------|
| Critical | API down, service-account missing, .env missing |
| High | 503 on cotizaciones, auth failures, Sheets not configured |
| Medium | npm audit findings, ngrok not running |
| Low | No persistent logs, minor config suggestions |

## Output Structure

```
.cursor/bmc-audit/
├── latest-report.md      (from Audit Runner)
├── handoff.json         (from Audit Runner)
├── DEBUG-REPORT.md      (from Debug Reviewer)
└── debug-export/
    ├── issues.md
    ├── logs-raw.txt
    ├── config-gaps.md
    └── recommendations.md
```

## Reference

- [bmc-dashboard-audit-runner](../bmc-dashboard-audit-runner/SKILL.md) — upstream agent
