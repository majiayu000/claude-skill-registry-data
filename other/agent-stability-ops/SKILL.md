---
name: agent-system-stability-ops
description: Audit and harden AgentSystem scheduler reliability, cron contract compliance, and agent consistency. Use when bots skip jobs, show timeout spikes, leak raw logs, or run with wrong agent identity/session.
---

# AgentSystem Stability Ops

Run fast reliability checks before changing cron/model/memory behavior.

## Quick Start

1. Run reliability audit:
```bash
python3 scripts/reliability_audit.py --hours 24
```

2. Run scheduler contract audit:
```bash
bash ~/.agent-evolution/scripts/agent-system-cron-audit.sh --json
```

3. Regenerate health report:
```bash
bash ~/scripts/cron-health-monitor.sh
```

## Workflow

1. Check scheduler contract first.
If `isolated + payload.kind != agentTurn` exists, fix or remove those jobs before any other tuning.

2. Check agent consistency.
If `runAgent != job.agentId`, treat as high severity and verify session routing + explicit `agentId` for every enabled job.

3. Check failure quality.
Separate transport/provider failures from logic failures. Timeout-heavy clusters usually require timeout/model/prompt changes, not blind retries.

4. Enforce output hygiene.
Any summary containing raw tool logs (`Exec`, stack trace, raw JSON) is a regression.

5. Re-run audits after changes.
Do not declare stable until the last 6-12h window has zero contract violations and zero agent mismatches.

## Resources

- `scripts/reliability_audit.py`: Computes reliability metrics from `jobs.json` + run logs.
- `references/runbook.md`: Safe remediation order and command cookbook.
