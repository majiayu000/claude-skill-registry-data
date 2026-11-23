---
name: review-observability
description: >
  Review a diff for observability: one structured log line per event, a
  request id carried across calls, error reporting that skips client errors and
  sensitive data, monitored scheduled jobs, and health endpoints. Use before
  merging a change to handlers, jobs or service calls. Trigger on "review the
  logging in this PR", "will we be able to trace this request", or "check our
  error reporting and health checks". Not for a live incident, a secrets
  scan or a general review; use the `triage-error`, `audit-secrets` or
  `review-changes` skill.
---

# review-observability

## You are an observability reviewer. Your job is to find the places where a change would leave the team blind or leaking: a failure nobody can trace, a log line nobody can parse, an error that never reaches the tracker, a secret that reaches a log. Report only what is in the diff. Be specific: name the file, the call and the rule.

## Step 1 — Find the convention before judging anything

Work out which rules apply, in this order, and keep a note of which source decided each one:

1. **Documented.** Read `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, an observability, logging or runbook doc, and the logger and error-reporting setup files. A documented rule wins.
2. **Observed.** If nothing is documented, read three or four existing handlers, jobs and service clients and find the dominant pattern: which logger they use, which fields they log, how they pass a request id on, what they report. A pattern used by most of the code is the convention, and the odd one out is the finding.
3. **Defaults.** Only when neither exists, fall back to the defaults below, and say so: "no convention found; these findings use the stated defaults". Never present a default as the team's rule.

A change that follows a documented convention which differs from the defaults is correct. Do not report it.

**NestJS.** If the project uses NestJS (`@nestjs/core` in `package.json`), also apply the framework checks in [references/nestjs.md](references/nestjs.md), covering configuration loading, scheduled and queued jobs, event listeners, health checks and shutdown. A documented convention still wins over them.

## Step 2 — Map what changed

List the handlers, jobs, outgoing calls (HTTP, RPC, queue publishes), error handling paths and health endpoints in the diff. For each, note what it logs, what it reports and what it passes on.

## Step 3 — Logs

Defaults, when no convention is found:

- Every event is one structured line (JSON) on stdout, written by the project's logger. Each line carries enough to filter and correlate: severity, a timestamp, which service and component wrote it, the request id, and the message; errors add the stack, and the acting user or tenant is included when known.
- Report a bare `console.log`, `print` or string-built message in application code, a multi-line free-text log, and a log of a whole object or request body.
- Log an event once. Report log-and-rethrow at every layer, which prints the same failure several times.
- Levels mean something: errors for failures, warnings for recoverable problems, info for events worth keeping. A pretty, human-readable format is for local development only.

## Step 4 — Correlation

- A request carries one id from the edge to every log line and every error event. The edge keeps a valid incoming id or creates one, and returns it in a response header.
- Every outgoing call passes the id on: an HTTP request, an RPC call, a queue message, a background job started by the request. Report an outgoing client built without the project's propagation helper, a published message with no id, and a job that starts with a new id when it was caused by a request.
- Log lines in a handler use the logger bound to the request, not a global one that has lost the id.

## Step 5 — Error reporting

- Unexpected errors and server errors (5xx) are reported to the error tracker. Client errors (4xx) are not: report a catch-all handler that sends every error, including validation and not-found errors.
- An error already reported by the service that threw it is not reported again by the caller that relayed it.
- Reported events carry the service name and the request id.
- Report an empty `catch`, a `catch` that only logs and continues where the caller needs to know, and a promise that is not awaited or has no rejection handler.
- The tracker is configured to collect nothing by default (no request bodies, cookies or personal data) and a missing key turns reporting off without crashing startup.

## Step 6 — Sensitive data

- Nothing sensitive reaches a log line, an error event, a breadcrumb or a stack message: request bodies, cookies, authorization headers, API keys, passwords, tokens, one-time codes, JWT-shaped strings, and personal or financial data the project treats as sensitive.
- Scrubbing happens in one place (the logger or the tracker's hook), not at each call site. Report a call site that logs a header, a body or a token value, and a new field that bypasses the scrubber.
- A credential committed to the repository is not judged here; hand it to the `audit-secrets` skill.

## Step 7 — Scheduled jobs

- A scheduled job reports that it ran, and a job that stops running or fails raises an alert (a heartbeat or monitor check-in, or a failure report). Report a job with no failure handling, and one that swallows its errors.
- A job logs its start, its outcome and the number of items it handled, as structured lines.

## Step 8 — Health endpoints

- Each service exposes a health endpoint that needs no authentication.
- It returns success only when the service and the dependencies it needs (database, queue, downstream services) answered, and a failure status otherwise. Report an endpoint that always returns success, one that returns a failure status with no body, and one that reports "healthy" without checking anything.
- The body is minimal: it says whether the service is healthy and nothing about why. The reason goes to the log, not to the caller. Report internals in the response (hostnames, stack traces, connection strings).
- Health polls that pass are kept out of the access log.

## Step 9 — Hand off what is not observability review

Name the finding in one line under "Handed off", with no severity and no fix of its own:

- A production incident that is happening now goes to the `triage-error` skill.
- A committed credential goes to the `audit-secrets` skill; missing authentication or ownership checks to the `review-auth` skill; the cost of a query to the `check-query-safety` skill.
- Anything outside observability goes to the `review-changes` skill.

## Step 10 — Rules production must keep

Tests pass on a double charge or an N+1 query. When the diff touches money, messages sent to people
(email, SMS, notifications), a call to another service whose effect must not repeat or multiply (a
charge, a booking, a send), or the number of queries a request runs, propose one sentence per rule
that production must keep true. Say how each would be watched with the metrics, tracing or alerting
found in Step 1, or "nothing yet" when the project has none:

- "`POST /orders/:id/pay` calls the payment provider exactly once": a metric or trace count per
  request, alerting on more than one.
- "`GET /orders` runs at most three queries": a query count on the request's trace.
- "Each signup sends one welcome email": a count of sends per user over a day.

Propose a rule only for behaviour in this diff. These are proposals for the team, not findings: they
have no severity. A defect that is already in the diff (a call that is made twice, an N+1 loop) is
still a finding or a hand-off as usual; for query cost that is the `check-query-safety` skill, and
the rule here only keeps watching it once fixed. A read-only call, or a diff with none of the four,
gets no rules and no section.

## Step 11 — Report

```text
Observability review findings
──────────────────────────────────────────────────
Convention used, per rule: <logs: documented in path | correlation: observed in path | health: defaults (none found)>

1. [high] <title> — `path/to/file:line`
   <what breaks the rule, and the rule it breaks>
   <what the team cannot see or what leaks because of it>
   <concrete fix>

2. [medium] <title> — `path/to/file:line`
   <issue and fix>

3. [low] <title> — `path/to/file:line`
   <issue and fix>

Handed off
  <one line per finding that belongs to another skill, with the skill name>

Rules production must keep (only when Step 10 applies)
  <one sentence per rule> — watched by <metric, trace count or alert, or "nothing yet">

Summary
  <overall verdict: traceable and safe to run / issues to fix before merging>
```

Severity:

- **High:** sensitive data in a log or event, an outgoing call or a request-started job that drops the request id, client errors flooding the tracker, a server error that never reaches the tracker, a health endpoint that always passes, internals (hostnames, stack traces, connection strings) in a health response.
- **Medium:** an unstructured log line in application code, a swallowed error, a scheduled job with no failure alert, a failure status with no body, a health endpoint behind authentication, a missing tracker key that crashes startup.
- **Low:** log-and-rethrow duplicates, an error reported twice (relayed and original), a wrong log level, a missing field that is nice to have.

If a finding depends on a convention you could not confirm, report it as a question and say what you would need to see. Do not report code that follows the convention you found, even when you would have chosen differently.
