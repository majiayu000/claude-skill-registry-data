---
name: support
description: Use this skill during Phase 7 after a successful deployment to generate or update monitoring, logging, alerting, and observability artifacts that catch exceptions and issues in the deployed code. Produces platform-neutral scripts when no observability platform is configured, and integrates with Grafana/Datadog/CloudWatch via MCP when configured. Trigger after deploy, or when the user says "add monitoring", "observability", "alerts", "dashboards", or "what should we watch for?".
next_suggestions:
  - when: support_gate_signed
    suggest: "run /docs to refresh the artifact index and traceability matrix"
---

# Support (Phase 7)

Make the change observable in production.

## Prerequisite

`.claude/sdlc/gates/deploy-<task-slug>.md` must exist and be signed.

## Step 1 — Identify what to watch

From the plan's in-scope surface and the security/NFR sections of the architecture, enumerate:

- New code paths → structured log events at key decision points
- New endpoints or RPCs → request count, error rate, latency (p50/p95/p99)
- New background jobs → run count, duration, failure rate
- New external calls → timeout, failure, retry counters
- New failure modes from the threat model → alerts

For each, write: what to measure, why, threshold for alert, who is paged, runbook link.

## Step 2 — Produce artifacts

Write to `.claude/sdlc/monitoring/<task-slug>/`:

- **Logging changes** — code deltas (in a follow-up PR, not this build's PR) or config changes
- **Metrics** — platform-appropriate config (Prometheus rules, Datadog monitors, CloudWatch alarms)
- **Dashboards** — JSON or TOML for the configured platform; a README if none is configured
- **Alerts** — with routing (oncall rotation / channel), severity, auto-resolve conditions
- **Runbook stub** — `runbook.md` with symptom → diagnostic → mitigation

## Step 3 — Integrate (when configured)

If an observability platform is configured in `.claude/sdlc/env.json`:

- Grafana/Datadog via MCP → propose dashboard and alert changes as pull requests or API calls; never auto-apply production alert changes without human confirmation
- CloudWatch → propose IaC changes

Never silently mutate production monitoring.

## Step 4 — Validate

- Generate a synthetic failure in a non-production environment and confirm the alert fires.
- Confirm the runbook entry matches what an on-call engineer would need at 3am.

## Human gate

Summarize: what's now being watched, what's alerted, runbook status. Sign-off → `.claude/sdlc/gates/support-<task-slug>.md`.

## What this skill must NOT do

- Do not auto-apply changes to production alerting.
- Do not skip a runbook entry ("we'll document later" is how silent outages happen).

## References

- `docs/SDLC.md` Support

## Next step hint

After writing the gate file, pipe the `next_suggestions` conditions to `skills/_shared/next-hint.sh` and print any output:

```bash
printf '%s\n' \
  'support_gate_signed|run /docs to refresh the artifact index and traceability matrix' \
  | bash skills/_shared/next-hint.sh
```

Print any output verbatim. If the script outputs nothing, add nothing.
