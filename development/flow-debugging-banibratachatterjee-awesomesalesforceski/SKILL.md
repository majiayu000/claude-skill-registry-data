---
name: flow-debugging
description: "Use when diagnosing a Flow that does not run, runs but produces wrong results, fails silently, or shows an unexpected fault email. Triggers: 'flow debug mode', 'flow not running', 'flow interview log', 'fault email', 'record-triggered flow not firing', 'debug run as user', 'flow test suite'. NOT for Apex debugging (use debug-and-logging), NOT for designing fault connectors (use fault-handling), NOT for fixing governor-limit failures caused by bulk volume (use flow-bulkification)."
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
tags:
  - flow-debugging
  - debug-mode
  - flow-interview-log
  - fault-email
  - record-triggered-flow
  - flow-test-suite
inputs:
  - "Flow API name or label"
  - "Symptom: not running, wrong output, error email, or incorrect behavior"
  - "Flow type: record-triggered, screen, scheduled, or autolaunched"
  - "Whether the issue is reproducible in sandbox or only in production"
outputs:
  - "Step-by-step debug plan matched to the symptom"
  - "Root-cause identification from debug run output or fault email"
  - "Checklist of trigger-condition, entry-criteria, and element-level findings"
  - "Recommended fix with supporting configuration guidance"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-04
---

# Flow Debugging

This skill activates when a practitioner needs to diagnose why a Salesforce Flow is not running, is producing wrong results, or is failing with an error. It provides structured debug procedures for Flow Builder debug mode, the Flow Interview Log, fault emails, debug-as-user runs, and the Flow Test Suite.

---

## Before Starting

Gather this context before working on anything in this domain:

- **Flow type**: Record-triggered (before/after save), screen, scheduled, or autolaunched. Each type has distinct debugging entry points.
- **Symptom category**: The flow is not firing at all, it fires but takes the wrong path, it fails with a fault email, or its output is incorrect.
- **Environment**: Is the issue in sandbox (where you can run Debug directly in Flow Builder) or production (where you must rely on Interview Logs and fault emails)?
- **Recent changes**: Was the flow recently activated, versioned, or had entry criteria changed? Flow activation creates a new version — an inactive version or wrong active version is a frequent hidden cause.
- **Invocation context**: Is the flow called from Apex, a process, a subflow, or directly from a record trigger? Each path requires a different diagnostic starting point.

---

## Core Concepts

### Debug Mode in Flow Builder

Flow Builder has a built-in debug tool accessed via the **Debug** button in the toolbar. It runs the flow step by step in the current org, showing input variable values, decision branch outcomes, element results, and variable state at each node. Debug mode is the primary tool for diagnosing screen flows and autolaunched flows.

Key options at debug launch:
- **Run as a different user**: Reproduces user-specific permission or sharing failures without impersonating the user in production.
- **Set variable values**: Pre-populate input variables so you can simulate a specific scenario.
- **Entry conditions**: For record-triggered flows, you can set the triggering record's field values to test specific condition combinations.

Subflows can be stepped into during a debug session. Debug runs do not commit DML unless the flow reaches a commit boundary in a before-save context.

### Flow Interview Log

The **Flow Interview Log** (Setup > Flows > Flow Interview Log) stores details of recent debug and runtime flow executions for approximately 7 days. Each log entry records:

- Flow API name and version
- Entry timestamp and running user
- Element-by-element execution trace
- Final status: completed, faulted, or paused

Interview logs are the primary diagnostic tool for production flow failures and for record-triggered flows that cannot be easily replicated in a debug session. They also capture paused flow interviews that are waiting on a scheduled path.

### Fault Emails

When a flow element fails and no fault connector routes the error, Salesforce sends a **fault email** to the org admin (defined in Setup > Process Automation Settings > Send Flow Error Email). The email contains:

- Flow API name and the element that failed
- `FLOW_ELEMENT_ERROR` category
- The underlying Salesforce error message (e.g., validation rule name, required field, DML error)

Fault emails are the first diagnostic signal for production record-triggered flows. The element name in the email directly identifies where the flow failed. If you find a fault email, immediately cross-reference that element against its configuration — it is rarely a flow logic problem and almost always a data-validation or permission issue.

### Flow Test Suite

Flow Builder supports automated test assertions through the **Test** menu > **New Test**. A test defines:

- A triggering record or input variable set
- Expected variable values or element execution outcomes at specific points

Tests run on demand in Flow Builder and can be included in deployment validation. They are not the same as Apex unit tests but provide structured regression coverage for critical flow paths.

---

## Common Patterns

### Mode 1: Build Debug Into the Flow From the Start

**When to use:** Authoring a new flow or adding significant logic to an existing one.

**How it works:**
1. Add descriptive labels to every decision element and outcome branch. The Interview Log and debug trace use element labels — "Decision_2" tells you nothing when debugging at 2am.
2. Use `$Flow.FaultMessage` in fault paths so any unhandled error propagates a readable diagnostic.
3. Add at least one fault connector from every DML and action element to a terminal path that logs `$Flow.FaultMessage` to a custom object or sends it to an admin.
4. Create at least one Flow Test that covers the happy path and one that covers the most likely error condition.
5. Run the Flow Test Suite after every material change before activating.

**Why not the alternative:** Debugging a flow without labels in an Interview Log is extremely slow. Adding debug capability after the fact costs more time than building it in.

### Mode 2: Diagnose a Flow That Is Not Running

**When to use:** A record-triggered flow is expected to fire on save but nothing happens — no changes, no email, no error.

**How it works:**
1. Open the flow in Flow Builder and confirm the correct version is **Active**. Multiple versions can exist; only one is active.
2. Check the **Start element**: object, trigger type (before/after save), and trigger event (create, update, or create/update). An "Update" trigger will not fire on new record creation.
3. Verify the **Entry Conditions** (formerly "Filter Criteria"). If set to "Only when a record is updated to meet the conditions," the flow only runs when the tracked field changes from a non-matching to a matching value. It does not fire if the record was already in the matching state.
4. Check **Run As**: confirm the flow is set to run in the context consistent with the invoking user or system context (system context bypasses permission checks but may behave differently than expected for user-owned records).
5. Use **Debug mode** in a sandbox to simulate a matching record update and step through the entry conditions.

**Why not the alternative:** Looking at the flow logic before confirming entry conditions is the most common time-wasting debugging mistake. Entry criteria problems account for the majority of "flow not firing" reports.

### Mode 3: Diagnose a Fault Email or Runtime Error

**When to use:** The org admin receives a fault email, or users report an error when saving a record that a flow processes.

**How it works:**
1. Read the fault email: identify the **flow name**, **element name**, and **error message**.
2. Open that flow in Flow Builder and navigate to the named element.
3. Map the error message to a known failure category:
   - `FIELD_INTEGRITY_EXCEPTION` — field-level validation rule or required field is blocking the DML.
   - `CANNOT_INSERT_UPDATE_ACTIVATE_ENTITY` — another trigger or validation on the related object is firing.
   - `DUPLICATE_VALUE` — a unique field or duplicate rule is blocking the record.
   - `INSUFFICIENT_ACCESS_ON_CROSS_REFERENCE_ENTITY` — the running user does not have access to a related record.
   - `FLOW_ELEMENT_ERROR` — the element's configuration is internally inconsistent (check for missing required field mappings in the element itself).
4. Use **Debug mode** (in sandbox) with the same field values as the failing record to reproduce.
5. Fix the root cause — usually the underlying data or a missing fault connector — before re-activating.

---

## Decision Guidance

| Symptom | Recommended Starting Point | Reason |
|---|---|---|
| Flow is not firing at all | Check active version, start element, trigger event, and entry conditions | Majority of "not firing" issues are configuration problems, not logic problems |
| Flow fires but takes the wrong path | Use Debug mode and step through decision elements with matching test data | Decision outcome logic is visible step-by-step only in debug |
| Fault email received | Read the fault email element name and error message first | The email directly identifies the failing element — no guessing |
| Flow worked yesterday, broken today | Check for recent activations, formula field changes, and upstream data changes | Version changes and data-layer changes are the most common silent breakers |
| Debugging a production flow | Use Flow Interview Log (7-day retention) | Debug mode is only available in non-production flows or sandboxes |
| Testing before deployment | Build and run Flow Test Suite assertions | Automated tests catch regressions faster than manual debug runs |
| User sees different behavior than admin | Use Debug > Run As a specific user | Sharing rules, record access, and field-level security all affect flow runtime |

---


## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner activating this skill:

1. Gather context — confirm the org edition, relevant objects, and current configuration state
2. Review official sources — check the references in this skill's well-architected.md before making changes
3. Implement or advise — apply the patterns from Core Concepts and Common Patterns sections above
4. Validate — run the skill's checker script and verify against the Review Checklist below
5. Document — record any deviations from standard patterns and update the template if needed

---

## Review Checklist

Run through these before marking a debugging session complete:

- [ ] Confirmed the correct flow version is active
- [ ] Verified trigger object, trigger event, and entry conditions match the expected firing scenario
- [ ] Ran or reviewed a debug session with field values that reproduce the failing case
- [ ] Mapped the fault email element name to the exact element and confirmed the root cause
- [ ] Checked that the fix addresses the data or configuration issue, not just adds a workaround fault path
- [ ] Confirmed the fix does not introduce a regression by re-running the Flow Test Suite
- [ ] Checked Flow Interview Log (if production) to confirm the fix resolved the failing interview pattern

---

## Salesforce-Specific Gotchas

1. **Entry Conditions "Only when updated to meet" vs "When conditions are met"** — "Only when updated to meet" fires once when a record transitions from non-matching to matching. If the record is created already in the matching state, the flow will never fire on creation. Choose "When conditions are met" if the flow must also fire on create.

2. **Flow Interview Log retention is 7 days** — If a production fault is reported more than a week after it occurred, the Interview Log entry may already be purged. Fault emails are the only persistent record unless the org has Event Monitoring or a custom error-logging fault path.

3. **Debug mode DML behavior depends on flow type** — In after-save record-triggered flows debugged in Flow Builder, DML operations execute and commit to the org unless you use the "Rollback Changes" option. Forgetting to check "Rollback" during a debug run on a production-adjacent sandbox can create real data side effects.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Debug session findings | Step-by-step element trace, identified branching point, and root-cause element |
| Fault email analysis | Mapped error category, responsible element, and recommended fix |
| Entry condition review | Documented trigger event, entry criteria, and confirmed firing conditions |
| Flow Test Suite run result | Pass/fail per test assertion after a fix is applied |

---

## Related Skills

- **flow/fault-handling** — Use when the diagnosis reveals missing fault connectors or poor error routing design; fault-handling covers how to build the error path correctly
- **flow/record-triggered-flow-patterns** — Use when the flow fires correctly but the business logic or trigger design needs rework
- **flow/flow-bulkification** — Use when the fault email indicates governor limit failures under data-load volume
- **apex/debug-and-logging** — Use for Apex debug logs and Developer Console analysis; this skill does NOT cover Apex debugging
