---
name: computer-health-check
description: "Perform a bounded, read-only health check of a Windows, macOS, or Linux computer, covering storage, memory pressure, CPU activity, startup load, battery where available, updates, and obvious errors. Use when asked to check PC health, diagnose a slow computer, inspect disk/RAM/CPU, or summarize system condition; request approval before any cleanup, install, update, or configuration change. Turkish triggers: bilgisayarı kontrol et, PC yavaş veya donuyor, CPU RAM disk ve hata kayıtları."
---

# Computer Health Check

Diagnose first; do not repair by default.

## Scope and safety

Confirm the operating system and whether commands may run locally. Start with non-destructive inspection only. Never delete files, disable startup items, install updates, change drivers, or alter settings during the health check.

## Workflow

1. Collect a bounded snapshot of uptime, CPU load, memory pressure, storage free space and errors, top active processes, startup load, battery health when present, and recent system/application errors.
2. Use OS-appropriate measurements. On Windows, calculate CPU utilization from two time-separated samples or a performance counter; do not present cumulative process CPU time as a percentage.
3. Treat unavailable sensors and unknown SMART/physical-disk status as unknown, not a failure.
4. Separate observations, likely causes, confidence, and safe next checks.
5. Prioritize at most five actions by impact and risk. Offer cleanup or change steps only as separate, opt-in actions with expected impact and rollback.

## Output

```text
Snapshot and coverage
Findings: evidence | likely cause | confidence
Healthy / watch / investigate areas
Top 3–5 next actions
What was not checked and why
```

## Guardrails

- Do not run network update checks, package upgrades, malware scans, or cleanup without explicit permission.
- Avoid a misleading single health score; report uncertainty instead.
- Redact user names, paths, serials, product keys, and process arguments when they are not needed.
