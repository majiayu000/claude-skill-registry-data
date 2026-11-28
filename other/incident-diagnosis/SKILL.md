---
name: incident-diagnosis
description: Live-system triage — read-only evidence first, establish what/since-when/how-wide, correlate onset with changes, trace one failing request, mitigate reversibly before root-causing. Use when production or a shared environment is broken now — outages, error-rate or latency spikes, "site is down", pager alerts, users reporting errors — and before restarting, redeploying, flushing, or deleting anything as a first move. Not for reproducible bugs in a dev checkout (see root-cause-debugging).
---

# Incident Diagnosis

Code debugging optimises for finding the cause. Incident work optimises for restoring service safely — the cause can wait; making things worse cannot. Weak incident work looks like: see an error → restart the thing → it seems better → close. Strong incident work reads first, changes one thing at a time with a reversal ready, and never confuses "went away" with "fixed".

## 0. Do not touch anything yet

The first moves are read-only: logs, metrics, status pages, process lists, config as deployed, the log of what shipped. Restarts, redeploys, cache flushes, and deletes destroy evidence AND can compound the failure (a restart storm on an overloaded dependency; a redeploy on top of a bad migration). Before any state-changing command, name the evidence that supports THAT action specifically — "a restart usually fixes it" is pattern-matching, not evidence. If you lack read access, say what you need rather than guessing.

## 1. Establish the three anchors

- **What exactly is failing, observably?** Error message/status/behaviour, verbatim — reproduce or observe it yourself if at all possible; second-hand reports compress the detail that matters.
- **Since when?** Find the onset in logs/metrics/monitors and write it down as a timestamp in one timezone (UTC) with its source. Confirm the clocks of the sources you compare agree; an hour of timezone skew yields a confident wrong correlation.
- **How wide?** One user / one endpoint / one region / everything? A single-tenant failure and a global failure have disjoint cause spaces. Check status pages and existing incidents before deep-diving.

**Baseline the noise.** For any error or log line you suspect, check its rate before the onset. An error that was already there at the same rate yesterday is not what changed — drop it and keep looking for the thing that starts at the onset.

## 2. Correlate the onset with changes

Most incidents are caused by a change. Diff the world at onset time: deploys, config and secret rotations, dependency/provider incidents, certificate expiries, cron jobs that fired, data that crossed a threshold (disk full, quota, integer/ID rollover, date boundaries). "Nothing changed" usually means "nothing I know about changed" — widen the search (adjacent teams, provider status, OS/infra auto-updates, scheduled scaling).

## 3. Localise by following one failing request

Pick ONE concrete failing request/job — a request ID, a job ID, a user — and trace it through the layers (edge → LB → service → dependency → data), checking at each hop: did it arrive, what did it return, how long did it take? The failure lives at the first layer where behaviour diverges from a known-good request of the same kind. Do not diagnose from aggregate dashboards alone — averages hide the failing path.

## 4. Mitigate first when impact justifies it

If users are hurting and a reversible mitigation exists — rollback, feature flag off, failover, rate-limit, scale up — propose/apply it BEFORE completing root-cause analysis. Rollback of the correlated change has the best prior.

Before applying any mitigation, write four lines: the action; the exact reversal; the signal that will show it worked (which metric, what value, checked when); and the evidence to capture first (logs, a heap/core dump, a copy of bad state). After applying, verify the signal — "command succeeded" is not "service restored". One mitigation at a time; if the signal doesn't move, reverse it before trying the next.

Never mitigate by deleting data or forcing state you can't restore.

## 5. Then root-cause properly

After service is restored, the investigation becomes ordinary root-cause-debugging (reproduce, bisect, falsifiable hypothesis). An incident closed at "restarted it and it went away" WILL recur — say so explicitly if that is where things stand, and name the instrumentation or alert that would catch it earlier next time.

## Report structure (during and after)

Timeline (UTC timestamps + facts + source, no speculation mixed in), current impact, confirmed vs suspected (labelled), actions taken with before/after evidence, next action and who owns it. Update as facts land. Never present a hypothesis as a finding — mislabelled confidence misroutes everyone downstream of your report.
