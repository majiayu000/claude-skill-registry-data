---
name: flow-debugging
description: "Use when diagnosing a Flow that does not run, runs but produces wrong results, fails silently, or shows an unexpected fault email. Triggers: 'flow debug mode', 'flow not running', 'flow interview log', 'fault email', 'record-triggered flow not firing', 'debug run as user', 'flow test suite', 'FLOW_ELEMENT_ERROR', 'FLOW_ELEMENT_FAULT', 'Workflow debug log category', 'trace flag for a flow', 'DebugLevel Workflow FINER', 'FlowInterview CurrentElement', 'flow debug log is empty'. NOT for designing the fault path itself — use flow/fault-handling. NOT for Apex debug logs, trace flags, or the Developer Console — use apex/debug-and-logging."
category: flow
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Operational Excellence
  - Reliability
triggers:
  - "my record-triggered flow is not firing when a record is saved"
  - "flow is running but not producing the expected output or field values"
  - "I received a flow fault email and need to find the root cause"
  - "how do I debug a flow step by step in Flow Builder"
  - "how do I check the flow interview log for a failed flow run"
  - "my flow fails silently and I cannot find any error message"
  - "how do I run a flow as a different user to test permissions"
  - "how do I create a flow test to validate expected outputs automatically"
  - "flow debugging isn't working"
  - "capture a debug log that shows which flow element failed"
  - "set the Workflow debug log category to FINER for a flow"
  - "read FLOW_ELEMENT_BEGIN and FLOW_ELEMENT_END in a debug log"
  - "my debug log has no FLOW_ lines in it at all"
  - "find which element a paused flow interview is stuck on"
  - "reproduce a flow fault with a FlowTest instead of a manual save"
  - "trace a flow that only fails for some records and not others"
  - "tell FLOW_ELEMENT_ERROR apart from FLOW_ELEMENT_FAULT"
  - "query FlowInterview for failed or paused interviews"
tags:
  - flow-debugging
  - debug-mode
  - flow-interview-log
  - fault-email
  - record-triggered-flow
  - flow-test-suite
  - debug-log
  - trace-flag
  - workflow-log-category
inputs:
  - "Flow API name or label"
  - "Symptom: not running, wrong output, error email, or incorrect behavior"
  - "Flow type: record-triggered, screen, scheduled, or autolaunched"
  - "Whether the issue is reproducible in sandbox or only in production"
  - "One concrete failing case: record Id, saving user, and timestamp"
  - "Whether the flow's DML elements carry fault connectors"
outputs:
  - "Step-by-step debug plan matched to the symptom"
  - "Root-cause identification from debug run output or fault email"
  - "Checklist of trigger-condition, entry-criteria, and element-level findings"
  - "Recommended fix with supporting configuration guidance"
  - "A DebugLevel/TraceFlag pair scoped to the failing user and Workflow category"
  - "An annotated FLOW_* event sequence localising the failure to one element"
  - "A FlowTest that reproduces the failure without a manual save"
dependencies: []
version: 1.1.0
author: Pranav Nagrecha
updated: 2026-09-05
---

# Flow Debugging

This skill activates when a practitioner needs to diagnose why a Salesforce Flow is not running, is producing wrong results, or is failing with an error.

**This skill owns the method, not the surfaces.** The method is six steps, and each one has
a documented artefact behind it:

> **reproduce** → **capture** (which trace-flag level yields which `FLOW_*` events, without
> truncation) → **read the log** (event sequence, element boundaries, value assignments,
> limit usage) → **localise** (element name; fault vs error vs limit) → **fix** →
> **prove with a `FlowTest`**

Neighbouring skills own the surfaces this method points at, and this skill does not repeat them:

| It is really about | Go to |
|---|---|
| Designing the fault route the log will show you | `flow/fault-handling` |
| A fault email you already have, mapped to an error code | `flow/flow-runtime-error-diagnosis` |
| Org-wide error alerting, thresholds, trend detection | `flow/flow-error-monitoring` |
| Paused screen-flow interview state and resume mechanics | `flow/flow-interview-debugging` |
| Test strategy, path matrices, coverage | `flow/flow-testing` |
| `Flow.settings`, versioning discipline, who owns the flow | `flow/flow-governance` |
| Trace flags, log retention, `ApexLog`, log-size management as a subject | `apex/debug-and-logging` |

---

## Before Starting

Gather this context before working on anything in this domain:

| Context | Why it matters |
|---|---|
| Flow type | Record-triggered (before/after save), screen, scheduled, or autolaunched. Each type has distinct debugging entry points — and `FlowInterviewLog` covers only screen flows. |
| Symptom category | Flow is not firing at all, fires but takes the wrong path, fails with a fault email, or produces wrong output. |
| Environment | Sandbox (a debug run is available) vs production (rely on trace-flag capture, `FlowInterview` SOQL, and fault emails). |
| Recent changes | Was the flow recently activated, versioned, or had entry criteria changed? An inactive or wrong active version is a frequent hidden cause. |
| Invocation context | Called from Apex, a process, a subflow, or directly from a record trigger? Each path requires a different diagnostic starting point. |
| Trace-flag headroom | Whether the org can still create a trace flag at all — logs accumulate against a hard org ceiling. |

---

## Questions to Ask Before Configuring

| Ask | Why it matters | What a good answer adds |
|---|---|---|
| **Which single record, which user, and which timestamp reproduces it?** | Capture is prospective. A trace flag records the *next* occurrence, not the last one, and both log-retention windows are short. Without a repeatable save you cannot aim it. | Turns "the flow is broken" into a save you can perform on demand with a trace flag already live — the difference between a one-hour and a one-week investigation. See gotcha 2 for the retention windows you are racing. |
| **Do the flow's DML and Get elements carry fault connectors, or none?** | It decides which event you are hunting and therefore which log level you must set. A caught failure emits `FLOW_ELEMENT_FAULT` (WARNING+); an uncaught one emits `FLOW_ELEMENT_ERROR` (ERROR+). | Prevents the most common dead end in this skill: setting `Workflow` to `ERROR`, seeing an empty log, and concluding the flow is innocent. See gotcha 6. |
| **Is this a screen flow, or a record-triggered / autolaunched / scheduled flow?** | It determines every downstream surface. `FlowInterviewLog` and `FlowInterviewLogEntry` are documented as **screen flow** logs; `FlowTest` is documented for record-triggered, autolaunched and Data Cloud-triggered flows. | Stops an hour spent querying a log object that structurally cannot hold rows for the flow in question. See gotcha 2. |
| **Who receives this org's process and flow error emails today?** | The default recipient is the user who last modified the flow, not an admin or an ops inbox. A "no email was sent" report is usually "the email went to someone who left". | Recovers the fault email that already exists before you build any capture at all — often the fastest possible localisation. See gotcha 9. |
| **Which version is actually active, and does the repo contain a `flowDefinition` for this flow?** | A deployed `flowDefinition` pins the active version and overrides the `status` inside the flow files. You can spend a day reading version 4 while version 3 runs. | Confirms the artefact you are reading is the artefact executing — the precondition for every other step. See gotcha 10. |
| **Does it fail on one record, or only under a bulk save or data load?** | A record-triggered flow bulkifies. `FLOW_START_INTERVIEWS_BEGIN` logs the request count once for the whole DML, and limit usage is per transaction, not per record. | Routes a limit-shaped failure to `flow/flow-bulkification` instead of burning the session on element logic that is fine. See gotcha 12. |
| **Can we create a trace flag in this org right now, and for how long may it stay on?** | Log volume is capped org-wide, and exceeding it both disables existing trace flags and blocks new ones. A busy integration user under a long-lived flag will consume the ceiling before your repro. | Produces a scoped, expiring flag on one user rather than an org-wide one — and avoids the outcome where the *next* investigation cannot capture anything. See gotchas 8 and 11. |

**What a proper configuration adds over just doing it:** a capture rig that is scoped to one
user, set to the one category and level that actually emits `FLOW_*` element events, and
expired on purpose — so the log you read is complete, attributable, and reproducible by a
`FlowTest` afterwards, instead of a truncated org-wide dump that answers a question nobody asked.

---

## Core Concepts

### The Two Failure Events, and Why the Level You Pick Decides What You See

Every flow failure surfaces as one of two debug events, and they log at different levels:

| Event | Guide's description | Category / level | Line |
|---|---|---|---|
| `FLOW_ELEMENT_FAULT` | "Message, element type, and element name (fault path taken)" | Workflow / **WARNING+** | `apexdev.txt` L38792 |
| `FLOW_ELEMENT_ERROR` | "Message, element type, and element name (flow runtime exception)" | Workflow / ERROR+ | `apexdev.txt` L38777 |

The levels run "from lowest to highest… NONE, ERROR, WARN, INFO, DEBUG, FINE, FINER, FINEST"
and are cumulative (`apexdev.txt` L38389–L38403). `ERROR` therefore does **not** include
`WARN`. A flow that handles its faults properly logs nothing at `Workflow=ERROR`.

`references/metadata-examples.md` §2 carries the full event table, the level matrix, and an
annotated excerpt of the sequence a caught fault produces.

### The Capture Is a Tooling API Object, Not Metadata

Trace flags are set "in the Developer Console or in Setup or by using the `TraceFlag` and
`DebugLevel` Tooling API objects" (`apexdev.txt` L39543–L39546). They have no Metadata API
type, so they cannot be deployed in `package.xml` and cannot be version-controlled with the
flow. `apex/debug-and-logging` owns the general mechanics; the flow-shaped configuration —
`Workflow: FINER`, everything else `NONE` — is in `references/metadata-examples.md` §3.

With no active trace flag, the defaults apply, and they include `WORKFLOW: INFO`
(`apexdev.txt` L39553–L39560). At `INFO` you get interview start and end and **no element
events at all**.

### Debug Runs in Flow Builder

Flow Builder's **Debug** button runs the flow in the current org, showing input values,
branch outcomes and element results, with options to run as another user, set variable
values, and supply the triggering record's field values.

**UNVERIFIED (2026-09-05): the Debug window, its "Run as a different user" and
"Roll back changes after the debug run" options, and the per-element "Show Details" panel
are documented only on help.salesforce.com, which cannot be fetched.** None of these
appears in `api_meta.txt`, `apexdev.txt` or `object_reference.txt`. Everything this skill
asserts about the *log* is grounded; treat the Debug window's behaviour as field knowledge
and verify each option in the org before relying on it — particularly the rollback checkbox,
which governs whether a debug run writes real data.

A debug run and a captured log answer different questions. The debug run shows what happens
*now* with values *you* chose. The log shows what happened *then* with the values the
platform actually had. When a bug is data-dependent, only the second one can find it.

### `FlowInterview` vs `FlowInterviewLog`

These are different objects with different scopes, and conflating them wastes more time in
this domain than any other single mistake.

| Object | The guide's first sentence | Scope | Line |
|---|---|---|---|
| `FlowInterview` | "Represents a flow interview. A flow interview is a running instance of a flow." | Any flow. Holds `CurrentElement`, `InterviewStatus`, `Error` (API 62.0+), `InterviewLabel` | `object_reference.txt` L139861 |
| `FlowInterviewLog` | "Represents the logs of a **screen flow** interview." | Screen flows only | `object_reference.txt` L140059 |
| `FlowInterviewLogEntry` | "Represents the log of a specific element that's executed by a **screen flow** interview." | Screen flows only | `object_reference.txt` L140207 |

The queries for all three, plus `FlowRecordRelation`, are in
`references/metadata-examples.md` §4.

### Reproducing a Fault Deterministically

`FlowTest` is the artefact that turns "it failed once in production" into a repeatable
check: "before you activate a record-triggered, autolaunched, or Data Cloud-triggered flow,
you can test it to verify its expected results and identify flow run-time failures"
(`api_meta.txt` L73961–L73962). The `HasError` comparison operator (API 64.0 and later,
`api_meta.txt` L74203) is what lets a test assert that a failure *did* happen.

Test points can only be placed at `Start` and `Finish` (`api_meta.txt` L74139–L74147), so a
`FlowTest` proves *that* the flow failed and the log proves *where*. You need both.
`flow/flow-testing` owns strategy; §5 of `references/metadata-examples.md` has the two
tests this method needs.

---

## Common Patterns

### Mode 1: Build Debug Into the Flow From the Start

**When to use:** Authoring a new flow or adding significant logic to an existing one.

**How it works:**
1. Give every element a descriptive label. The element **name** is what
   `FLOW_ELEMENT_BEGIN` / `_END` / `_FAULT` print (`apexdev.txt` L38768, L38774, L38792) —
   `Decision_2` in a log at 2am tells you nothing.
2. Set `interviewLabel` on the flow. It is the only human-readable handle on
   `FlowInterview.InterviewLabel` (`object_reference.txt` L139951) and on the paused
   interviews list. A flow with waits or scheduled paths and no `interviewLabel` produces
   an untriageable queue.
3. Add a fault connector to every fault-capable element and capture `$Flow.FaultMessage`
   into a durable log record. `flow/fault-handling` owns the route design; this skill needs
   it to exist so the log emits `FLOW_ELEMENT_FAULT` rather than `FLOW_ELEMENT_ERROR`.
4. Write one `FlowTest` for the happy path and one for the most likely failure, using
   `HasError` for the second.
5. Run the checker before every deploy: `python3 scripts/check_flow_debugging.py --manifest-dir <src>`.

**Why not the alternative:** adding debuggability after the incident costs more than adding
it during authoring, and the incident is exactly when you cannot afford it.

### Mode 2: Diagnose a Flow That Is Not Running

**When to use:** A record-triggered flow is expected to fire on save but nothing happens — no changes, no email, no error.

**How it works:**
1. Confirm which version is **actually active**. If the repo contains a `flowDefinition`
   for this flow, its `activeVersionNumber` wins over the `status` in the flow files
   (`api_meta.txt` L73929–L73931). Read the version that is running, not the latest one.
2. Check the **Start element**: `object`, `triggerType`, `recordTriggerType`. `Update` will
   not fire on create — the enum values are `Create`, `Update`, `CreateAndUpdate`,
   `Delete` (API 50.0+), `None` (API 55.0+) (`api_meta.txt` L72448–L72457).
3. Verify the **entry conditions** and, critically, `doesRequireRecordChangedToMeetCriteria`:
   when `true`, "conditions evaluate to true only if the record didn't meet the required
   conditions before the triggering update but now meets the conditions after the update"
   (`api_meta.txt` L71320–L71322).
4. Check `runInMode` — `DefaultMode`, `SystemModeWithSharing`, `SystemModeWithoutSharing`
   (`api_meta.txt` L68374–L68390) — against the failing user's access.
5. **Then** capture. Set `Workflow` to `INFO` or above and look for
   `FLOW_START_INTERVIEWS_BEGIN` (`apexdev.txt` L38856). If it is absent, the flow genuinely
   never started and no amount of element-level logging will help.

**Why not the alternative:** reading flow logic before confirming the active version and the
entry conditions is the most common time-wasting mistake in this domain.

### Mode 3: Diagnose a Fault Email or Runtime Error

**When to use:** Someone receives a fault email, or users report an error on save.

**How it works:**
1. Find out who *should* have received it. On a default org
   (`enableFlowUseApexExceptionEmail` = `false`) it went to "the user who last modified the
   process or flow" (`api_meta.txt` L116961–L116967) — check with them before assuming no
   email was sent.
2. Take the element name from the email and hold it. That is your localisation until the log
   confirms it.
3. Set the capture rig (`references/metadata-examples.md` §3), reproduce, and pull the log.
4. Read in the order given in §2 of the same file: interview started? → fault or error line?
   → value assignments and rule details → limit usage.
5. Fix the underlying cause — data, permission, or field definition — then write the
   `FlowTest` that would have caught it, and only then re-activate.

### Mode 4: Diagnose "It Ran and Did the Wrong Thing"

**When to use:** No error, no email, no fault. The flow completed and the data is wrong.

**How it works:**
1. This case needs `FINER`, not `FINE`. The two events that answer it are
   `FLOW_RULE_DETAIL` — "interview ID, rule name, and result" — and `FLOW_VALUE_ASSIGNMENT`
   — "interview ID, key, and value" (`apexdev.txt` L38847, L38896). Both are FINER+.
2. Walk the `FLOW_RULE_DETAIL` lines in order and find the first rule whose result is not
   what you expected. That decision is the branch point.
3. Walk back through `FLOW_VALUE_ASSIGNMENT` to the last write of each variable the rule
   reads. The value is printed; you do not have to infer it.
4. If a `recordLookup` returned the wrong record, `FLOW_BULK_ELEMENT_DETAIL` carries the
   record count (`apexdev.txt` L38724) — a count of 0 with a downstream null is the
   signature.
5. Encode the corrected expectation as a `FlowTest` assertion at `Finish`, so the wrong
   branch cannot come back silently.

---

## Decision Guidance

| Symptom | Recommended Starting Point | Reason |
|---|---|---|
| Flow is not firing at all | Active version (and any `flowDefinition`), start element, trigger event, entry conditions — then `Workflow=INFO` and look for `FLOW_START_INTERVIEWS_BEGIN` | Majority of "not firing" issues are configuration, and one INFO-level event settles whether the flow started |
| Flow fires but takes the wrong path | `Workflow=FINER`; read `FLOW_RULE_DETAIL` then `FLOW_VALUE_ASSIGNMENT` | Branch results and variable values are printed at FINER and nowhere else |
| Fault email received | The element name in the email, then a log capture to confirm it | The email localises for free; the log confirms and shows what preceded it |
| Log is empty despite a known failure | Check the log header for `WORKFLOW,<level>` | `ERROR` drops every `FLOW_ELEMENT_FAULT`; `INFO` drops every element event |
| Flow worked yesterday, broken today | Active version, `flowDefinition`, formula and field changes, upstream data | Version pinning and data-layer changes are the most common silent breakers |
| Debugging a production flow you cannot re-save | `FlowInterview` SOQL on `InterviewStatus` and `Error` | `Error` is queryable from API 62.0; it survives when the log does not |
| Screen flow, user reported a step | `FlowInterviewLog` + `FlowInterviewLogEntry` | These objects are documented for screen flows specifically |
| Record-triggered flow, no rows in `FlowInterviewLog` | Expected — query `FlowInterview` instead | `FlowInterviewLog` is the screen-flow log; zero rows is not evidence of anything |
| Only fails at volume | `FLOW_*_LIMIT_USAGE` lines, then `flow/flow-bulkification` | Limit usage is per transaction; the shape of the failure is not element logic |
| Testing before deployment | `FlowTest` with `HasError` for the negative case | Repeatable proof that survives the next deploy |

---

## Recommended Workflow

1. **Pin the reproduction.** Answer the Questions table above — specifically the failing
   record Id, the saving user, the flow type, and which version is active (checking for a
   `flowDefinition` that overrides `status`). Do not capture anything yet.
2. **Choose the level from the fault-connector answer, then build the rig.** Create the
   `DebugLevel` / `TraceFlag` pair from `references/metadata-examples.md` §3 — `Workflow`
   at `FINER`, every other category `NONE`, scoped to the one failing user, expiring within
   the hour. Confirm the header reads `WORKFLOW,FINER` before you trust the log.
3. **Reproduce and pull the log**, then read it in the fixed order in §2 of the same file:
   interview started → `FLOW_ELEMENT_FAULT` or `FLOW_ELEMENT_ERROR` → `FLOW_RULE_DETAIL`
   and `FLOW_VALUE_ASSIGNMENT` → `*_LIMIT_USAGE`. Match on event names, never on column
   positions.
4. **Localise to one element and one category.** Name the element, and classify the failure
   as caught fault, uncaught error, wrong branch, or limit. Hand off limit-shaped failures
   to `flow/flow-bulkification` and fault-route-design failures to `flow/fault-handling`
   rather than fixing them here.
5. **If the log expired or the flow cannot be re-saved**, fall back to §4: `FlowInterview`
   (`InterviewStatus`, `Error`, `CurrentElement`), `FlowRecordRelation` for the related
   record, and — for screen flows only — `FlowInterviewLog` / `FlowInterviewLogEntry`.
6. **Fix, then prove it.** Write the two `FlowTest` components from §5: one that reproduces
   the fault via `HasError`, one that proves the fix. Run
   `python3 scripts/check_flow_debugging.py --manifest-dir <src> --strict` and deploy in the
   order in §7.
7. **Take the trace flag down.** Delete it, or confirm its `ExpirationDate` has passed.
   Record what the log showed in `templates/flow-debugging-template.md` so the next person
   does not repeat the capture.

---

## Review Checklist

Run through these before marking a debugging session complete:

- [ ] Confirmed the correct flow version is active, including any `flowDefinition` that pins it
- [ ] Verified trigger object, trigger event, and entry conditions match the expected firing scenario
- [ ] The log header was read and confirms the `WORKFLOW` level actually applied
- [ ] The failure was localised to a named element by a `FLOW_ELEMENT_FAULT` or `FLOW_ELEMENT_ERROR` line
- [ ] Classified as caught fault / uncaught error / wrong branch / limit — and routed to the owning skill if it is not this skill's fix
- [ ] Checked `LogLength` against the 20 MB ceiling before treating the log as complete
- [ ] Root cause is a data, permission or definition problem that was fixed — not a fault path added to hide it
- [ ] A `FlowTest` reproduces the original failure and fails on the pre-fix flow
- [ ] The checker script passes with `--strict`
- [ ] The trace flag is deleted or expired, and the org's log ceiling was not exhausted

---

## Salesforce-Specific Gotchas

Twelve documented behaviours with guide line ranges are in `references/gotchas.md`. The
three that most often decide whether a session succeeds:

1. **`Workflow` at `ERROR` shows you nothing on a well-built flow.** `FLOW_ELEMENT_FAULT`
   logs at WARNING and above; the levels are cumulative upward, so `ERROR` excludes it.
2. **`FlowInterviewLog` is the screen-flow log.** Zero rows for a record-triggered flow is
   the documented behaviour, not evidence the flow did not run.
3. **The fault email default recipient is the last person who modified the flow.** Not an
   admin, not an ops alias.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Capture rig | `DebugLevel` + `TraceFlag` JSON bodies, scoped to one user, `Workflow=FINER`, with an expiry |
| Annotated log excerpt | The `FLOW_*` sequence for the failing save, with the localising line marked |
| Localisation statement | Element name + failure class (caught fault / uncaught error / wrong branch / limit) |
| Interview SOQL results | `FlowInterview` rows with `InterviewStatus`, `Error`, `CurrentElement` when the log is gone |
| Reproduction `FlowTest` | A `.flowtest-meta.xml` that fails on the broken flow and passes on the fixed one |
| Checker output | `check_flow_debugging.py --strict` result over the deploy manifest |

---

## Reference Files

| File | Read it when |
|---|---|
| `references/metadata-examples.md` | You are building the artefacts: the flow with a data-dependent fault, the annotated `FLOW_*` log sequence and its level matrix, the Tooling API `DebugLevel`/`TraceFlag` bodies, the `FlowInterview` / `FlowInterviewLog` / `FlowRecordRelation` SOQL, the two `FlowTest` components, `package.xml`, deploy order and verification. |
| `references/gotchas.md` | The log is empty, the log is truncated, the email never arrived, or the version you are reading is not the version running. Twelve platform behaviours with guide line ranges. |
| `references/llm-anti-patterns.md` | You are reviewing generated flow-debugging advice — nine failure modes, including "enable debug logs" as step one and inventing `FlowExecutionErrorEvent` field names. |
| `references/examples.md` | You want the method walked end to end on three worked symptoms, including the wrong-branch case that produces no error at all. |
| `references/well-architected.md` | You are arguing about how much debuggability to build in up front, or need the sourced claim behind a statement in this package. |
| `templates/flow-debugging-template.md` | You are running a session and want the capture plan, log-reading record and root-cause summary in one place. |
| `scripts/check_flow_debugging.py` | Before deploying — lints flows and any `DebugLevel` JSON for the shapes that make a flow undebuggable. |

---

## Related Skills

- **flow/fault-handling** — owns fault-route design, `$Flow.FaultMessage` capture, and rollback scope. Go there once the log tells you the fault path is missing or wrong.
- **flow/flow-runtime-error-diagnosis** — owns mapping a specific error code from a fault email to its cause. Go there when you have the message and need the meaning; come here when you need the message.
- **flow/flow-error-monitoring** — owns org-scale alerting, routing, thresholds and trend detection. Go there when the answer is "we should have known sooner", not "why did this one fail".
- **flow/flow-interview-debugging** — owns paused-interview state and instrumenting flows for triage.
- **flow/flow-testing** — owns test strategy, path matrices and coverage. This skill borrows exactly two tests from it.
- **flow/flow-governance** — owns `Flow.settings` (including the error-email recipient setting), naming, versioning and retirement.
- **flow/flow-bulkification** — owns the fix when `FLOW_*_LIMIT_USAGE` is the finding.
- **flow/record-triggered-flow-patterns** — owns `triggerType` / `recordTriggerType` selection and the guide's narrower availability wording.
- **apex/debug-and-logging** — owns trace flags, `ApexLog`, log retention and log-size management as subjects in their own right; this skill only configures them for the `Workflow` category.
