---
name: debug-and-logging
description: "Use when diagnosing Apex behavior with debug logs, choosing log levels, or replacing `System.debug` habits with structured production logging and async job monitoring. Triggers: 'debug log', 'System.debug', 'logging framework', 'AsyncApexJob monitoring', 'production logs', 'log truncated', 'publish immediately', 'correlation id', 'Limits snapshot', 'log lost on rollback', 'Test.getEventBus().deliver()'. NOT for trace flag setup, reading a log, or the Developer Console — use apex/debug-logs-and-developer-console. NOT for building a custom Log__c framework — use apex/custom-logging-and-monitoring."
category: apex
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Operational Excellence
  - Reliability
tags:
  - debug-logs
  - system-debug
  - logging-framework
  - asyncapexjob
  - observability
triggers:
  - "how should I debug Apex in production-safe ways"
  - "too many System.debug statements in code"
  - "custom logging framework for Apex"
  - "AsyncApexJob monitoring and failure logs"
  - "which debug log levels should I use"
  - "we're having issues with debug logs"
  - "my debug log is truncated and the line I need is missing"
  - "log record disappeared when the transaction rolled back"
  - "capture the exception before the rollback discards it"
  - "replace System.debug with a real logging framework"
  - "publish immediately vs publish after commit for logging"
  - "correlate an Apex error to a debug log after the fact"
  - "trace flags stopped generating logs"
  - "no debug log for my platform event trigger"
  - "add a correlation id to Apex logs"
  - "log the governor limits at the point of failure"
  - "system.debug best practices and logging levels in apex"
inputs:
  - "execution context such as synchronous request, trigger, Queueable, Batch, or REST"
  - "whether the issue is development-time debugging or production-time observability"
  - "current logging destination such as debug logs, custom object, or platform event"
outputs:
  - "logging strategy recommendation"
  - "review findings for observability gaps or noisy debug usage"
  - "Apex logging pattern with retention and escalation guidance"
  - "deployable LogService class, Log_Event__e platform event, subscriber trigger and test class"
  - "package.xml, deploy order, and ApexLog verification queries"
dependencies: []
version: 1.1.0
author: Pranav Nagrecha
updated: 2026-09-05
---

Use this skill when the question is not merely “where do I put a debug line?” but “how do I make Apex diagnosable in the environments that matter?” Debug logs are useful in development and targeted troubleshooting. Structured logs, async job monitoring, and durable records are what keep production support workable.

## Before Starting

- Is the need short-lived debugging in a lower environment or persistent production observability?
- Which contexts fail today: synchronous requests, triggers, Queueables, Batch jobs, or event subscribers?
- What can safely be logged without leaking secrets, tokens, or sensitive business data?

## Questions to Ask Before Configuring

Ask these before writing a logger; the answers decide the sink, and an LLM that skips them produces a
`Log__c` insert that is rolled back by the very failure it was built to record.

| Ask | Why it matters | What a good answer adds |
|---|---|---|
| "When this fails, does the transaction roll back?" | A DML log row and a publish-after-commit event both vanish with the rollback; only `PublishImmediately` survives it (api_meta L42222–42227) | The sink decision per severity, and whether `Log_Event__e` is needed at all |
| "How many log calls will one transaction make, worst case?" | Publish-immediately events are metered at 150 per transaction, separately from DML (Apex Developer Guide L19598–19599) | The severity threshold for the event path, so breadcrumbs stay on the cheap DML path |
| "Which log do you expect to read during the incident — the debug log, or a record?" | System debug logs live 24 hours, monitoring logs seven days (L38118), and anything over 20 MB is trimmed from the middle (L38115–38117) | Whether this is a trace-flag exercise or a durable-logging build |
| "Does any traced code path touch credentials or personal data?" | At `FINEST` the log "includes details of all Apex variable assignments" (L38171–38175); only session IDs are scrubbed (L38133) | The maximum log level allowed on that class, written down |
| "Who owns the alert when this fires at 3 a.m.?" | Unhandled-exception mail defaults to the class's `LastModifiedBy`, is throttled to 10/hour/app-server, is suppressed for duplicates, and is never sent for `@AuraEnabled` calls (L39599–39612) | A deployed `ApexEmailNotifications` file with a monitored address, and a decision not to rely on it |
| "What do you need to join a log row back to — the async job, or the request?" | `getAsyncApexJobId()` correlates to `AsyncApexJob`; `getRequestId()` correlates to Event Monitoring and to `ApexLog.RequestIdentifier` (L16327–16329) | The correlation field on the log object, and the query support will actually run |
| "Who runs the subscriber trigger?" | A platform event trigger runs as the Automated Process entity by default, which owns its debug log, cannot send email, and cannot do FLS checks without explicit permission sets (api_meta L96454–96462; Apex Developer Guide L11921–11922) | A `PlatformEventSubscriberConfig` with an explicit `user`, deployed with the trigger |

What a proper logging design adds over scattering `System.debug`: the record that explains a failure
still exists after the rollback that caused it, it carries the request id that joins it to `ApexLog`
and to Event Monitoring, and the verbosity dial is a custom metadata record rather than a redeploy.

---

## Core Concepts

### `System.debug` Is A Development Tool First

`System.debug` is valuable for temporary investigation and lower-environment diagnosis, especially when paired with the right debug categories and levels. It is not a durable production logging strategy. Teams that rely on `System.debug` alone usually discover too late that the information they need was never retained or queryable.

### Structured Logging Needs A Durable Sink

For production support, use a real destination such as a custom log object, platform event, or external observability system. The important properties are durability, correlation, and queryability. A useful log record usually includes operation name, record IDs or correlation ID, severity, outcome, and normalized error details.

### Log Levels Should Reflect Actionability

Debug levels are not decorative. Excessive low-value logging creates noise and storage pressure. Use lower-detail debug traces during focused diagnosis, but keep persistent production logging targeted toward warnings, errors, and key workflow checkpoints that support can actually act on.

The levels, lowest to highest, are `NONE`, `ERROR`, `WARN`, `INFO`, `DEBUG`, `FINE`, `FINER`, `FINEST`,
and they are cumulative — "if you select FINE, the log also includes all events logged at the DEBUG,
INFO, WARN, and ERROR levels" (Apex Developer Guide L38389–38408). Each level applies per *category*,
not globally: Database, Database Access, Workflow, NBA, Validation, Callout, Apex Code, Apex Profiling,
Visualforce, System (L38341–38387). The lever that keeps a log under 20 MB is dropping the categories
you are not asking about to `NONE`, not lowering `APEX_CODE`.

Precedence is fixed and worth knowing before you wonder why your setting did nothing: trace flags
override everything, then default test logging levels, then the API header, then the entry point's
own level — "If none of these cases apply, logs aren't generated or persisted" (L39539–39575).
Note also that the Developer Console "sets a trace flag when it loads, and that trace flag remains in
effect until it expires" (L39543–39544), which is why an open Developer Console changes the logs of a
deployment running in another window.

### Async Monitoring Is Part Of Logging

If Queueable or Batch work matters to the business, `AsyncApexJob` status and job metrics are part of observability. Logging should connect the initiating action to job IDs, job outcomes, and error counts instead of leaving async failures orphaned.

## Common Patterns

### Temporary Debug Logging With Removal Discipline

**When to use:** A developer is tracing a bug in a sandbox or lower environment.

**How it works:** Add targeted `System.debug` statements with clear labels and remove them after diagnosis.

**Why not the alternative:** Leaving broad debug noise in production code makes future diagnosis harder.

### Structured Logger Wrapper

**When to use:** A service, integration, or async worker needs durable support diagnostics.

**How it works:** Centralize logging through one utility or service that writes severity, context, and identifiers to a durable sink.

### Async Job Correlation

**When to use:** Batch or Queueable work drives business-critical outcomes.

**How it works:** Log the initiating business context alongside the enqueued job ID, then monitor `AsyncApexJob` for failures and throughput.

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Sandbox-only debugging session | Targeted `System.debug` with clear labels | Fastest way to inspect runtime state temporarily |
| Production support needs durable diagnostics | Structured log object or event | Queryable and retained beyond transient debug logs |
| Async worker must be monitored | Correlate to `AsyncApexJob` and log job outcomes | Required for real operational visibility |
| Sensitive integration flow | Minimal structured logs with secret-safe fields | Avoids leaking tokens or payload secrets |
| The failure rolls the transaction back | `Log_Event__e`, `publishBehavior` `PublishImmediately` | Published regardless of whether the transaction succeeds (api_meta L42225–42227) |
| Breadcrumbs in a transaction that commits | Buffered `Application_Log__c` insert via `ApplicationLogger` | One DML; publish-immediate calls are capped at 150 per transaction and should be reserved for errors |
| Queueable that may die on a limit exception | Finalizer that flushes both sinks | The finalizer runs on `SUCCESS` and `UNHANDLED_EXCEPTION` alike (Apex Developer Guide L16337–16340) |
| One-off reproduction in a sandbox | Class-scoped trace flag, other categories `NONE` | `CLASS_TRACING` overrides user-level levels without generating org-wide volume (L38297–38299) |
| Log for a platform event trigger | `PlatformEventSubscriberConfig` with an explicit `user` | Otherwise the trigger's debug log is filed under the Automated Process entity (api_meta L96454–96462) |


## Recommended Workflow

1. **Classify the need.** Answer the Questions table above. If nothing needs to outlive the request,
   stop here and set a class-scoped trace flag (`references/examples.md`, Example 3) — do not build a
   logger for a one-off reproduction.
2. **Pick the sink per severity** from the table in `references/well-architected.md`. INFO/WARN take the
   buffered DML path; ERROR/FATAL take `Log_Event__e` with `publishBehavior` `PublishImmediately`.
3. **Deploy the canonical logger, do not rewrite it.** `templates/apex/ApplicationLogger.cls` plus
   `templates/apex/custom_objects/Application_Log__c.object-meta.xml` and its `fields/`, and a
   `Logger_Setting__mdt` `Default` record. Extend it with `LogService` from
   `references/code-examples.md` — correlation id, `Limits` snapshot, publish fallback.
4. **Build the event side** — `Log_Event__e`, `LogEventTrigger`, and the
   `PlatformEventSubscriberConfig` that names the running user. All three XML files are in
   `references/code-examples.md` with the package.xml and the deploy order.
5. **Test the delivery, not just the publish.** `LogServiceTest` asserts the subscriber's row with
   `Test.getEventBus().deliver()` inside `Test.startTest()`/`Test.stopTest()`. A test that omits
   `deliver()` asserts against an empty table (`references/llm-anti-patterns.md`, Anti-Pattern 8).
6. **Run the checker** over the source tree before deploying:
   `python3 skills/apex/debug-and-logging/scripts/check_debug_and_logging.py --manifest-dir force-app/main/default`
   It flags debug-only catch blocks, logging in loops, and missing `publishBehavior`.
7. **Close the loop with the fence.** Deploy `apexEmailNotifications` to a monitored address — retrieve
   first, because deploying replaces the org's whole list (api_meta L22458–22461) — then verify with the
   `ApexLog` and `Application_Log__c` queries at the end of `references/code-examples.md`.

---

## Review Checklist

- [ ] `System.debug` usage is targeted and justified, not left as permanent noise.
- [ ] Durable logging exists for production-critical failures.
- [ ] Logged fields exclude secrets, tokens, and unnecessary sensitive payload data.
- [ ] Async processes can be traced through job IDs or equivalent correlation.
- [ ] Log severity and volume are aligned to support actionability.
- [ ] Teams know where logs are retained and how they are purged.

## Salesforce-Specific Gotchas

1. **Debug logs are temporary and operationally fragile** — they are not a replacement for durable production logs.
2. **Overlogging can hide the signal you actually need** — a flood of low-value debug lines makes incidents slower to diagnose.
3. **Async failures often need both logs and `AsyncApexJob` inspection** — one without the other leaves blind spots.
4. **Logging secrets is still a security defect even if the log helps debugging** — sanitize outbound request data and auth fields.
5. **A rollback discards the log row that explains it** — unless the event is `PublishImmediately`.
6. **A log over 20 MB loses lines from anywhere, not the end** — narrow the trace before reproducing.
7. **`System.debug` is invisible to code coverage** — a debug-only `catch` block still passes the gate.
8. **A platform event trigger's debug log belongs to Automated Process** — until you deploy the subscriber config.

Full detail with sources in `references/gotchas.md`.

## Output Artifacts

| Artifact | Description |
|---|---|
| Logging review | Findings on debug noise, missing durable logs, and async visibility gaps |
| Logging strategy | Recommendation for debug usage, structured logging, and retention |
| Correlation pattern | Guidance for linking business actions, exceptions, and async job IDs |

## Reference Files

| File | Read it when |
|---|---|
| `references/code-examples.md` | You are building the thing: `LogService`, `Log_Event__e`, the subscriber trigger, the subscriber config, the test class, package.xml, deploy order, verification queries |
| `references/gotchas.md` | A log is missing, truncated, expired, misfiled, or rolled back — 14 platform behaviours with guide citations |
| `references/llm-anti-patterns.md` | Reviewing generated logging code; eight failure shapes with detection hints |
| `references/examples.md` | You need the Queueable/Finalizer pattern, or you are triaging from `ApexLog` after the debug log expired |
| `references/well-architected.md` | Choosing a sink, or justifying the cost of one to a reviewer |
| `templates/debug-and-logging-template.md` | Running a logging review over someone else's code |
| `scripts/check_debug_and_logging.py` | Before deploying — six rules over the `.cls`, `.trigger`, and `.object-meta.xml` files this skill produces |

## Related Skills

- `apex/exception-handling` — owns the exception hierarchy, `DmlException` behaviour, and rethrow policy. This skill assumes you have already decided *what* to catch; it decides where the record goes.
- `apex/custom-logging-and-monitoring` — owns the `Log__c` schema in depth, retention policy, purge batch jobs, and forwarding to Splunk/Datadog. Go there when the question is the log store's lifecycle rather than the write path.
- `apex/debug-logs-and-developer-console` — owns trace flag setup, reading log output, anonymous Apex, and the Apex Replay Debugger. Go there for the "how do I turn logging on" mechanics this skill only fences.
- `apex/salesforce-debug-log-analysis` — owns reading a captured log: event types, cumulative limit blocks, and finding the slow code unit.
- `apex/platform-events-apex` — owns platform event design, replay, and high-volume behaviour. This skill uses one event for one purpose; do not design your event bus from here.
- `apex/apex-limits-monitoring` — owns `Limits`-class guard clauses and in-transaction limit defence. This skill only *records* the reading.
- `apex/batch-apex-patterns` — use when observability issues center on Batch lifecycle and `AsyncApexJob` monitoring.
- `apex/callouts-and-http-integrations` — use when logs need to support outbound API troubleshooting safely.
