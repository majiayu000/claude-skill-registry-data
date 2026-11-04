---
name: agent-system-output-hygiene-ops
description: Audit and remediate AgentSystem cron output hygiene by detecting raw tool logs, stack traces, and noisy summaries. Use when jobs leak 403/429/internal details, summaries are not user-safe, or post-change validation is required.
---

# AgentSystem Output Hygiene Ops

Run this skill when cron summaries must stay concise and safe for user-facing channels.

## Quick Start

1. Run hygiene audit:
```bash
bash scripts/hygiene_audit.sh --run-suite
```

2. If leaks exist, patch top leaking jobs using `references/prompt-remediation.md`.

3. Smoke-test patched jobs:
```bash
agent-system cron run <job-id> --expect-final --timeout 480000
agent-system cron runs --id <job-id> --limit 2 --expect-final
```

## Workflow

1. Run `scripts/hygiene_audit.sh` and identify highest-frequency leaking job IDs.
2. Prioritize jobs leaking raw tool output (`Exec`, `stack trace`, `raw JSON`, `403/429` payloads).
3. Apply strict output contract to prompt:
- ban raw logs and internal diagnostics
- force compact final format or `NO_REPLY`
- prefer deterministic local fallback over noisy web-search errors
4. Re-run patched jobs and confirm the latest run is clean.
5. Re-run health suite and record report paths.

## Resources

- `scripts/hygiene_audit.sh`: summarizes leak-heavy jobs from latest health report.
- `references/prompt-remediation.md`: safe prompt patch template and command pattern.
