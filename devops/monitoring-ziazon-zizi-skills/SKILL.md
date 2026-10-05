---
name: monitoring
description: >
  Use when you need observability into running code — adding or improving logging so
  you (and the user) can see what the system is actually doing. Invoke whenever you:
  add logging/instrumentation to a feature, diagnose a running service ("why is this
  failing", "watch the logs", "what is it actually doing"), standardize log output,
  or must confirm a change by observing the live app because reading the code or unit
  tests can't prove it. Also load it whenever another task needs proof from a running
  system (boot smoke check, live verification of a fix). Do NOT use for deploy/CI/
  alerting-stack or Nomad/Consul work — that's the infrastructure skill; do NOT use
  for writing tests — that's tdd-skill (this skill is the "eyes on live behavior"
  half that covers what tests can't reach).
---

# Monitoring & Logging

Goal: make running code legible. You should be able to answer "what is it doing, and
where did it break?" from logs alone, without a debugger. Two jobs: (1) instrument code
so its behavior is observable, (2) use that output as evidence — never declare live
behavior "working" without having observed it.

## Workflow

Follow in order — each step gates the next.

### 1. Discover the stack's logger and conventions first

Before adding a single log line, find how THIS codebase logs — otherwise you create a
style island that the team's grep habits, log shippers, and alerting all miss.

- Grep neighboring files for the logger in use (`this.logger`, `slog`, `Rails.logger`,
  `message()`, …) and read 2–3 existing call sites: level vocabulary, context/prefix
  convention, structured vs plain.
- Check `LEARNINGS.md` beside this skill, when your copy keeps one, for this stack — the
  logger and its stable markers may already be recorded (e.g. a NestJS app: injected
  `ConsoleLogger` + `setContext(this.constructor.name)`; boot marker
  `Nest application successfully started`).
- Gate: do not add instrumentation until you know the logger, the levels, and the
  context convention. A bare `console.log`/`print`/`fmt.Println` is never the answer in
  a codebase that has a logger — it bypasses levels, context, and transports.

### 2. Instrument at boundaries and decisions

Log where behavior branches or crosses a boundary — that is where diagnosis happens:
startup/shutdown, inbound request + outcome, external calls (target + status + latency),
state transitions, and every branch that ends in an error or early return.

- **Greppable markers:** emit stable, searchable phrases for key lifecycle points (a
  consistent "started"/"ready" line, a consistent failure prefix). Verification and
  alerting key off these — changing the wording silently breaks both.
- **Structured + contextual:** attach the IDs that matter (request id, user/entity id,
  service name) so one line is actionable on its own, without hunting for its neighbors.
- **Fail loud with cause:** on caught errors log what was attempted, against what, and
  the error/stack — never swallow silently. An intentionally-tolerated degraded path
  still logs that it degraded, or the degradation is invisible until it matters. When a
  failure triggers a compensating action (rollback, cleanup), log the failure AND the
  compensation's outcome — a half-rolled-back state must be diagnosable from logs alone.
- **Tri-state for idempotent startup/maintenance tasks:** log success / no-op ("already
  up to date") / failure as distinct messages, so "did nothing" is never mistaken for
  "failed" (or vice versa).
- **Levels with intent:** error = needs attention, warn = degraded/recoverable,
  log/info = lifecycle milestones, debug = detail off by default.
- **Skip hot paths:** no per-iteration logs inside loops or per-row logs in query paths
  — they drown the signal and cost real latency. Log the batch summary instead.
- **Never log secrets/PII:** redact tokens, passwords, auth headers, and full payloads
  that carry credentials — logs outlive the request and get shipped to third parties.

### 3. Run it and capture the output

Observing means capturing, not glancing at scrollback.

- Redirect stdout/stderr to a file (`… > /tmp/boot.log 2>&1`) so you can grep it and
  quote exact lines as evidence.
- Exercise the actual path you changed (hit the endpoint, trigger the job) — a clean
  boot proves wiring, not behavior.
- Gate: if you cannot run the system, say so explicitly and fall back to static checks
  — do not present unexecuted code as observed behavior.

### 4. Assert on stable markers, then probe externally

- Assert the success marker is PRESENT and the failure markers are ABSENT (grep for
  `error`, stack traces, the framework's dependency-failure signatures). Presence-only
  checks pass on a service that started and then blew up.
- Probe from outside the process too: HTTP status/headers on the route, the written DB
  row, the enqueued job. Logs say what the code believes; the probe says what happened.

### 5. Report what you observed

State the evidence, not a vibe: which markers you saw, which probes returned what, and
what remains unverified. "Started clean, `POST /x` returned 201, row present" beats
"it works."

## Metrics & alerting (when the stack grows them)

Logging above is the default; reach for metrics/tracing when a service needs aggregate
health, not just per-event evidence. This is design rules only — the alerting *plumbing*
is infrastructure.

- **Define the questions first.** Before instrumenting, write the 2–4 things on-call must
  answer about this feature (e.g. "what fraction of payments retry?", "is the provider
  slow?"). No question → you log everything and learn nothing.
- **Metrics:** RED (rate / errors / duration) per endpoint and per external dependency;
  USE (utilization / saturation / errors) for resources. Always histograms/percentiles
  (p50/p95/p99) — an average hides the 1% having a terrible time.
- **Cardinality:** metric labels only from small fixed sets (route template, status class,
  provider) — NEVER user IDs, raw URLs, or error text. That detail belongs in logs/traces.
- **Alert on symptoms users feel** (error rate, p99, queue age); causes (CPU, a restart)
  go on dashboards, not the pager. Every alert must be actionable, link a runbook, and have
  a justified threshold + duration. Two severities only (page / ticket). Test-fire each new
  alert once.
- **Tracing (if ever added):** use OpenTelemetry and propagate context across every async
  boundary, or the trace dies at the gap.

## Common failure modes

- **Declaring success without observing the running behavior** — the #1 miss. If the
  change affects runtime behavior, step 3–4 are mandatory, not optional polish.
- **Bare `console.log`/`print` debugging left in** — use the project logger at debug
  level, or remove the line before finishing.
- **Logging a secret while diagnosing auth** — dumping headers/env/payloads to "see
  what's being sent" leaks credentials into the transcript and log files. Log presence
  and shape, never values.
- **Noisy hot-path logs** shipped as "instrumentation" — per-row/per-iteration lines
  bury the markers step 4 depends on.
- **Unstable markers:** rewording an existing lifecycle line breaks whatever greps it.
  Add new lines; don't casually rephrase established ones.
- **Swallowed catch blocks** (`catch {}`) — the exact branch you'll later need eyes on
  is the one that logs nothing.

## Before you call this done

- [ ] Used the project's logger + conventions (no bare print/console.log left behind).
- [ ] Errors and degraded paths log cause + context; nothing swallowed silently.
- [ ] No secrets/PII in any added log line.
- [ ] Ran the affected path and captured output to a file (or explicitly stated why not).
- [ ] Asserted success markers present AND failure markers absent; probed externally.
- [ ] Reported the concrete evidence observed, and what remains unverified.

## Related skills

- [debugging-and-error-recovery](../debugging-and-error-recovery/SKILL.md): diagnosing a failure this skill's logs and signals surfaced.

## Capturing learnings (session-handoff protocol)

Accumulate project knowledge in `LEARNINGS.md` beside this skill, when your copy keeps one.
On handoff / "update skills" / after observability work: record this stack's logger + conventions, the stable log
markers that exist, recurring failure signatures and what they mean, and effective probes.
Dedupe/merge, tag stack-specific items, and read it before instrumenting a matching stack.
