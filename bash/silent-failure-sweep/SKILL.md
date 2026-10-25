---
name: silent-failure-sweep
description: "Periodically sweep an agent's cron jobs, scripts, and pipelines for silent failures: swallowed stderr, existence-only success checks, stale artifacts, dead probes. Companion to secure-addon-install."
license: MIT
metadata:
  category: security
  compatibility: "Any agent runtime with scheduled jobs or pipelines"
  version: 1.0.0
---

# Silent-Failure Sweep for Scheduled Jobs & Pipelines

Run this sweep **periodically** (monthly is a good cadence) over every cron job, scheduled task, and data pipeline in your agent runtime. Its premise: **any pipeline that can fail silently will**, and the older the pipeline, the more likely something upstream already broke without anyone noticing.

## The five silent-failure signatures

### 1. Swallowed stderr
`grep` every cron-invoked script for `2>/dev/null` and bare `|| true`:

```bash
grep -rn "2>/dev/null" ~/scripts/ /etc/cron*/ 2>/dev/null
```

Each hit is a place where a loud failure was converted into silence. **Fix**: redirect stderr to a log file. If the command is "allowed to fail", say so explicitly with a fallback action, not with the void.

**Real incident**: a system `sqlite3` CLI was hijacked by a third-party drop-in library and died on launch; every calling script had `2>/dev/null`, so the breakage was invisible for days until a human ran the binary manually.

### 2. Existence-only success checks
`grep` your job scripts for success logic that checks *presence*, not *freshness*:

```bash
# BAD: file exists = success
[ -f /data/output/today.json ] && echo OK

# GOOD: calendar-forward check — artifact must be newer than the last expected window
find /data/output -name "today.json" -mmin -1440 | grep -q . && echo OK || echo "STALE"
```

**Real incident**: a nightly data-refresh job reported success for months because "output file exists" was the check — the upstream source had been frozen for over a year.

### 3. Dead probes (health check that can't fail)
For every "health check" ask: **what input would make it fail?** A check that returns OK regardless of upstream state (`curl` without `--fail`, a process-alive check for a process whose endpoint is dead, a ping to a load balancer) is decoration, not monitoring.

```bash
# BAD: always exits 0 if server is up, even when app is 500ing
curl -s http://svc/health

# GOOD: fails on HTTP errors and validates content
curl -sf --max-time 10 http://svc/health | grep -q '"status":"ok"'
```

### 4. Fire-and-forget writes
Any POST/publish/send without a read-back. An HTTP 200 doesn't mean the payload landed intact (truncation, encoding, dropped fields). **Fix**: read the object back after writing and compare length/key fields against what you sent.

### 5. Unverified third-party send paths
SMS, social APIs, notification platforms: some silently rate-limit or block ("page says sent, nothing arrives, no error anywhere"). Sweep for jobs that trigger external sends and verify: does the job check *receipt* through a second channel? **Rule**: after repeated silent failure, stop retrying — retries extend silent blocks.

## Sweep procedure (monthly)

1. List all scheduled jobs (`crontab -l`, `systemctl --user list-timers`, your agent's cron registry).
2. For each, classify: what is its success check? Tag each with the first signature above it exhibits.
3. For data pipelines: verify the newest artifact is within the expected freshness window **right now**. Anything stale → investigate upstream, don't just re-run.
4. For external-sending jobs: check the last N sends were actually received (platform-side read-back or a second channel).
5. Log the sweep result with a date. The sweep itself follows the calendar-forward rule: no sweep record newer than 35 days = your monitoring has silently failed too.

## Meta-lesson

Monitoring systems fail silently like everything else. Your sweep must itself have a freshness check, and its records must be written somewhere that itself gets looked at. Otherwise you have built a smoke detector with a dead battery that reports "no smoke" every day.
