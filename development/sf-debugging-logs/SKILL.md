---
name: sf-debugging-logs
description: Salesforce debug logging and diagnostics - trace flags and debug levels via TraceFlag and DebugLevel Tooling API objects or sf data create record --use-tooling-api, log categories and levels, the 20 MB log and 1000 MB trace-flag limits, sf apex list log, sf apex get log, sf apex tail log and sf apex run for anonymous Apex, reading execution units, CODE_UNIT_STARTED, SOQL_EXECUTE_BEGIN/END, DML_BEGIN, LIMIT_USAGE_FOR_NS, CUMULATIVE_PROFILING and FLOW_* lines, diagnosing CPU time and heap, Apex Replay Debugger with checkpoints and heap dumps, Developer Console Log Inspector and Query Plan, AsyncApexJob and batch/queueable failures, Flow debugging, LWC browser debugging, callout and Named Credential errors, and safe production diagnostics with Event Monitoring. Use when a test or transaction fails, a limit is exceeded, an async job silently fails, or when running vf-check smoke, vf-check apex, or vf-check verify.
---

# Debugging and Debug Logs

## When to use

- An Apex test, trigger, batch, queueable, Flow, or LWC action fails and the error message is not
  sufficient.
- A governor limit is hit (`Apex CPU time limit exceeded`, `Apex heap size too large`, too many SOQL
  queries) and you need the transaction's actual consumption.
- An async job reports failure with no stack trace.
- A callout fails and you need the request/response.
- Post-deploy verification fails in a real org and diagnostics must be captured into
  `.vibeforce/reports/`.

## Pipeline

```
DebugLevel (set of category levels)
    |
TraceFlag (LogType + TracedEntityId + StartDate/ExpirationDate) -> references a DebugLevel
    |
transaction runs -> ApexLog record (Location = SystemLog | Monitoring)
    |
sf apex list log / sf apex get log / sf apex tail log   or   REST /sobjects/ApexLog/<id>/Body/
```

## Limits that bite

| Limit | Value | Consequence |
| --- | --- | --- |
| Single debug log size | 20 MB | larger logs are reduced by removing older log lines, from anywhere in the log, not just the start; a truncated log silently loses `System.debug` output |
| System log retention | 24 hours | `Location = SystemLog`, visible only to you |
| Monitoring log retention | 7 days | `Location = Monitoring`, visible to all administrators |
| Log generation rate | 1000 MB per 15-minute window | trace flags are disabled automatically and an email is sent to the last user who modified them; re-enable after 15 minutes |
| Org log accumulation | 1000 MB | users can no longer add or edit trace flags until debug logs are deleted |
| Trace flag duration | `ExpirationDate` must be less than 24 hours after `StartDate` | expired flags stop logging |
| Active trace flags | one per traced entity | a second flag for the same user or class conflicts |

A trace flag on a frequently executed class or a busy user can make requests fail outright,
regardless of the window and log sizes. Scope trace flags to one user, one short window.

## Order of precedence for log levels

1. Active trace flags override everything. The Developer Console sets a `DEVELOPER_LOG` trace flag
   when it loads, which stays in effect until it expires.
2. With no active trace flags, synchronous and asynchronous Apex tests run at the default levels:
   `DB=INFO`, `APEX_CODE=DEBUG`, `APEX_PROFILING=INFO`, `WORKFLOW=INFO`, `VALIDATION=INFO`,
   `CALLOUT=INFO`, `VISUALFORCE=INFO`, `SYSTEM=DEBUG`.
3. With no relevant trace flags and no tests running, the API request's debugging header sets the
   levels. Requests without a debugging header produce transient (unsaved) logs.
4. If the entry point sets a level (a Visualforce debugging parameter, for example), that wins.
5. Otherwise no log is generated or persisted.

Class and trigger trace flags (`LogType = CLASS_TRACING`) override other levels, including user
trace flag levels, but they do not themselves cause logging to happen.

## Core patterns

### 1. Tail a live org while reproducing

```bash
# auto-creates a trace flag, streams logs, colourised
sf apex tail log --color --target-org vf-dev

# reuse an existing DebugLevel instead of the default
sf apex tail log --debug-level VF_Apex_Fine --target-org vf-dev

# do not touch trace flags at all (respect what is already configured)
sf apex tail log --color --skip-trace-flag --target-org vf-dev
```

### 2. List and fetch logs

```bash
sf apex list log --target-org vf-dev

sf apex get log --log-id 07L... --target-org vf-dev

# the two most recent logs, written to files
sf apex get log --number 2 --output-dir .vibeforce/reports/logs --target-org vf-dev
```

`--number` fetches the N most recent logs; `--output-dir` writes them as files instead of printing.

### 3. Run anonymous Apex and read its log

```bash
cat > /tmp/probe.apex <<'APEX'
Integer open = [SELECT COUNT() FROM Case WHERE IsClosed = false WITH USER_MODE];
System.debug(LoggingLevel.ERROR, 'VF_PROBE open_cases=' + open);
APEX

sf apex run --file /tmp/probe.apex --target-org vf-dev
```

Anonymous Apex always runs `with sharing`. Its log appears under
`CODE_UNIT_STARTED|[EXTERNAL]|execute_anonymous_apex`. Use `LoggingLevel.ERROR` for probe output so
the line survives a low `APEX_CODE` level, and prefix a grep-able token (`VF_PROBE`).

### 4. Set a trace flag deterministically from the CLI

```bash
# 1. find or create a DebugLevel
sf data query --use-tooling-api --target-org vf-dev \
  --query "SELECT Id, DeveloperName FROM DebugLevel WHERE DeveloperName = 'VF_Apex_Fine'"

sf data create record --use-tooling-api --target-org vf-dev --sobject DebugLevel \
  --values "DeveloperName=VF_Apex_Fine MasterLabel=VF_Apex_Fine ApexCode=FINE ApexProfiling=INFO Callout=INFO Database=INFO System=DEBUG Validation=INFO Visualforce=INFO Workflow=INFO"

# 2. find the user (or class) to trace
sf data query --target-org vf-dev --query "SELECT Id FROM User WHERE Username = 'me@example.com'"

# 3. create the trace flag (ExpirationDate < StartDate + 24h)
sf data create record --use-tooling-api --target-org vf-dev --sobject TraceFlag \
  --values "DebugLevelId=7dl... LogType=USER_DEBUG TracedEntityId=005... StartDate=2026-09-12T09:00:00.000+0000 ExpirationDate=2026-09-12T10:00:00.000+0000"

# 4. delete it when finished
sf data delete record --use-tooling-api --target-org vf-dev --sobject TraceFlag --record-id 7tf...
```

`LogType` values: `USER_DEBUG` (trace one user), `CLASS_TRACING` (override levels for one Apex class
or trigger; does not itself generate logs), `DEVELOPER_LOG` (what the Developer Console sets),
`PROFILING` (reserved for future use). Field-by-field reference:
`references/debug-log-reference.md`.

### 5. Read a log in the right order

For a failing transaction, read bottom-up then top-down:

| Step | Look for | Tells you |
| --- | --- | --- |
| 1 | `FATAL_ERROR` | exception type, message, stack trace |
| 2 | `CUMULATIVE_LIMIT_USAGE` / `LIMIT_USAGE_FOR_NS` | which limit was near or over |
| 3 | `EXECUTION_STARTED` ... `EXECUTION_FINISHED` | transaction boundary |
| 4 | `CODE_UNIT_STARTED` / `CODE_UNIT_FINISHED` nesting | which trigger, Flow, batch chunk, or async entry point ran, and in what order |
| 5 | `SOQL_EXECUTE_BEGIN` / `SOQL_EXECUTE_END` | query text, row counts, duration |
| 6 | `DML_BEGIN` / `DML_END` | operation, object, row count |
| 7 | `CUMULATIVE_PROFILING` | expensive queries and DML aggregated for the transaction |
| 8 | `FLOW_ELEMENT_*`, `FLOW_ELEMENT_ERROR`, `FLOW_ELEMENT_FAULT` | declarative automation in the same transaction |

Log line format is `timestamp|event identifier|...`, pipe-delimited. The timestamp's parenthesised
value is nanoseconds elapsed since the start of the request, which is how you find the slow section.
The Developer Console Execution Log view hides elapsed time; open the Raw Log view to see it.
`[EXTERNAL]` replaces a line number for built-in Apex or managed-package code. Trigger code units
carry a `typeRef` of `__sfdc_trigger/YourTrigger` or `__sfdc_trigger/YourNamespace/YourTrigger`.

Symptom-driven recipes with real log excerpts: `references/log-analysis-playbook.md`.

### 6. Diagnose CPU time and heap

```text
16:06:58.49 (49590539)|LIMIT_USAGE_FOR_NS|(default)|
  Number of SOQL queries: 0 out of 100
  Number of query rows: 0 out of 50000
  Number of DML statements: 0 out of 150
  Maximum CPU time: 0 out of 10000
  Maximum heap size: 0 out of 10000000
```

- CPU time: subtract the elapsed nanoseconds between the `CODE_UNIT_STARTED` and
  `CODE_UNIT_FINISHED` of each unit to find which unit consumes it. `CUMULATIVE_PROFILING` names the
  expensive queries. Callout wait time does not count toward CPU time; loops, collection work,
  describes, and JSON serialization do.
- Heap: heap usage is reported accurately in the log and an exception is thrown when an Apex heap
  size error occurs. At other times the reported heap size is the largest calculated during the
  transaction, and minimal usage is reported as `0` to reduce overhead on small transactions. Set
  `APEX_CODE` to `FINER` or higher to see `HEAP_ALLOCATE` lines with byte counts per line number.
- Limit remediation itself: skill `sf-governor-limits`; query tuning: skill
  `sf-soql-sosl-optimization`.

### 7. Async job debugging

```bash
sf data query --target-org vf-dev --query "SELECT Id, JobType, Status, ApexClass.Name, MethodName, NumberOfErrors, JobItemsProcessed, TotalJobItems, ExtendedStatus, ParentJobId, CompletedDate FROM AsyncApexJob WHERE CreatedDate = TODAY ORDER BY CreatedDate DESC LIMIT 20"
```

`JobType` values: `ApexToken`, `BatchApex`, `BatchApexWorker`, `Future`, `Queueable`,
`ScheduledApex`, `SharingRecalculation`, `TestRequest`, `TestWorker`. `Status` values: `Aborted`,
`Completed`, `Failed`, `Holding` (flex queue), `Preparing`, `Processing`, `Queued`.
`ExtendedStatus` holds a short description of the **first** error only; the rest is emailed to the
last user who modified the batch class. `NumberOfErrors` counts failed batches, not failed records -
a batch is transactional, so one unhandled exception fails the whole chunk. Chunked batch jobs create
`BatchApexWorker` children carrying `ParentJobId`.

Each async execution is a separate transaction and produces its own debug log, so a batch with 50
chunks produces up to 50 logs. Attach a `Finalizer` to a Queueable so failures are observable even
when the job dies (skill `sf-async-apex-patterns`).

### 8. Replay debugging

```
SFDX: Toggle Checkpoint                (up to 5, in .cls or .trigger)
SFDX: Update Checkpoints in Org        (uploads them; heap dumps collected at those lines)
SFDX: Turn On Apex Debug Log for Replay Debugger
   ... reproduce in the org ...
SFDX: Get Apex Debug Logs              (pick the log)
SFDX: Launch Apex Replay Debugger with Current File
```

Or, for a test or anonymous Apex file, `SFDX: Launch Apex Replay Debugger with Current File`
directly: it updates checkpoints, sets and then deletes trace flags, and generates a fresh log.
Checkpoints expire after 30 minutes and heap dumps after about a day; only one log can be replayed at
a time, which makes async debugging awkward. Full capability and limitation list:
`references/debugging-tools.md`.

### 9. Flow and declarative automation

Flow execution appears in the same transaction log under `FLOW_*` events at the `Workflow` category.
`FLOW_ELEMENT_BEGIN` / `FLOW_ELEMENT_END` bracket each element, `FLOW_VALUE_ASSIGNMENT` shows
variable writes, `FLOW_BULK_ELEMENT_LIMIT_USAGE` and `FLOW_ELEMENT_LIMIT_USAGE` show the limits a
Flow consumed inside your transaction, and `FLOW_ELEMENT_ERROR` / `FLOW_ELEMENT_FAULT` mark failures
and fault-path transitions. When an Apex trigger appears to burn queries it did not issue, look for
interleaved `FLOW_*` units. Flow design: skill `sf-flow-automation`.

### 10. Client-side (LWC) debugging

- Enable Debug Mode for the specific user in Setup so the framework ships unminified code with
  source maps; keep it off for everyone else because it slows the app.
- Use browser devtools: breakpoints in the component's `.js`, the Network tab for
  `aura` / `apex` XHRs, and the Lightning Component Inspector for component trees and wire state.
- Wire errors surface in the `error` member of the wire result, not in a debug log; log them in the
  component during development, never in shipped code.
- `console` policy: `console.error` is permitted for genuine failures; other `console` calls are
  ESLint errors outside `__tests__` (skill `sf-code-analyzer-quality`).
- Server-side behaviour of an `@AuraEnabled` call is still diagnosed with a debug log on the calling
  user; the code unit name identifies the Apex method.

## Anti-patterns

| Anti-pattern | Consequence | Instead |
| --- | --- | --- |
| Leaving `APEX_CODE=FINEST` on | logs every variable assignment, leaks PII, blows the 20 MB and 1000 MB limits, slows deployments | raise to `FINE`/`FINER` for the shortest possible window; the docs explicitly warn to verify `APEX_CODE` is not `FINEST` before deploying |
| Trace flag on a hot class or a busy integration user | requests can fail outright | trace one developer user, short expiry |
| `System.debug` of an sObject or a user record | PII in a log administrators can read for 7 days | log ids and status codes only |
| Debugging by adding `System.debug` everywhere | consumes Apex CPU time even with logs off (`AvoidDebugStatements`) | checkpoints + replay debugger, or a logging framework gated by configuration |
| Reading a truncated log and concluding the code did not run | 20 MB logs drop older lines from anywhere | narrow the trace flag categories, or reproduce with less data |
| Using the Developer Console while diagnosing a deployment | its `DEVELOPER_LOG` trace flag affects all logs, including deployment logs | close it, or use CLI trace flags |
| Assuming one log per batch job | each chunk is its own transaction and log | query `AsyncApexJob`, then fetch logs per chunk |
| `sf apex tail log` without `--skip-trace-flag` when a flag is already configured | overwrites the intended configuration | `--skip-trace-flag` |
| Diagnosing production by turning on logs broadly | breaches the 1000 MB window, risks request failures, exposes PII | Event Monitoring, targeted trace flag, `references/production-diagnostics.md` |

## Verification

```bash
# a fresh log exists for the reproduction
sf apex list log --target-org vf-dev

# fetch it into the report folder the harness reads
sf apex get log --number 1 --output-dir .vibeforce/reports/logs --target-org vf-dev

# confirm the limit that was hit
grep -n "LIMIT_USAGE_FOR_NS" -A 20 .vibeforce/reports/logs/*.log

# re-run the failing test synchronously with the fix
sf apex run test --tests ExpenseServiceTest --synchronous --target-org vf-dev

# post-deploy diagnostics bundle (anonymous Apex probes, data queries, limits, deploy report)
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" smoke --target-org vf-uat
```

`vf-check smoke` writes `<project>/.vibeforce/reports/smoke-<ISO>.json` containing the probe results,
limit snapshot, and the ids of any logs it fetched, so a failed verification is reproducible without
re-running the scenario. Exit codes: `0` pass, `1` gate failed, `2` misconfiguration, `3` org or
network error.

A bug fix is proven when the reproduction that produced the `FATAL_ERROR` no longer produces it, and
the assertion that failed now passes - not when the log merely looks different.

## References

- `references/debug-log-reference.md` - category, level, and event tables; `TraceFlag` and
  `DebugLevel` fields; `ApexLog` fields; header format.
- `references/log-analysis-playbook.md` - symptom to log lines to conclusion, with excerpts.
- `references/debugging-tools.md` - Replay Debugger, checkpoints, Log Inspector, Query Plan,
  interactive and ISV debuggers, devtools setup.
- `references/production-diagnostics.md` - safe diagnosis in production, Event Monitoring, PII rules,
  what `vf-check smoke` captures.
- Apex Developer Guide: [Debug Log](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_debugging_debug_log.htm), [Debug Log Order of Precedence](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_debugging_debug_log_precedence.htm), [Working with Logs in the Developer Console](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_debugging_system_log_console.htm)
- Tooling API: [TraceFlag](https://developer.salesforce.com/docs/atlas.en-us.api_tooling.meta/api_tooling/tooling_api_objects_traceflag.htm), [DebugLevel](https://developer.salesforce.com/docs/atlas.en-us.api_tooling.meta/api_tooling/tooling_api_objects_debuglevel.htm), [ApexLog](https://developer.salesforce.com/docs/atlas.en-us.api_tooling.meta/api_tooling/tooling_api_objects_apexlog.htm)
- Object Reference: [AsyncApexJob](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_asyncapexjob.htm), [EventLogFile](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_eventlogfile.htm)
- CLI reference: [apex commands](https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/cli_reference_apex_commands_unified.htm), [data commands](https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/cli_reference_data_commands_unified.htm)
- VS Code: [Apex Replay Debugger](https://developer.salesforce.com/docs/platform/sfvscode-extensions/guide/replay-debugger.html), [ISV Customer Debugger](https://developer.salesforce.com/docs/platform/sfvscode-extensions/guide/isv-debugger.html), [SOQL query plans](https://developer.salesforce.com/docs/platform/sfvscode-extensions/guide/soql-plans.html)
- Sibling skills: `sf-apex-development`, `sf-apex-testing`, `sf-async-apex-patterns`,
  `sf-governor-limits`, `sf-soql-sosl-optimization`, `sf-lwc-development`, `sf-flow-automation`,
  `sf-integration-patterns`, `sf-security-model`, `sf-post-deploy-verification`.
