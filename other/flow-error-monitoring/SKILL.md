---
name: flow-error-monitoring
description: "Set up monitoring + alerting for Flow runtime errors at org scale: routing fault emails, Flow runtime error reports, custom centralized logging (Integration_Log__c), escalation thresholds, and trend detection. NOT for diagnosing a specific flow error (use flow-runtime-error-diagnosis). NOT for debug-mode setup (use flow-debugging)."
category: flow
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Reliability
  - Operational Excellence
tags:
  - flow
  - monitoring
  - alerting
  - error-reports
  - integration-log
  - ops
  - dashboards
triggers:
  - "flow error monitoring"
  - "flow fault email routing"
  - "flow runtime error report"
  - "centralized flow error logging"
  - "flow error dashboard"
  - "flow error alerting ops"
inputs:
  - Flow portfolio scope (single org, org set, multi-business-unit)
  - Volume of flow executions per day
  - Existing observability stack (Splunk, Datadog, etc.)
  - SLA for error response
outputs:
  - Fault-email routing policy
  - Centralized error-log object design
  - Runtime error report + dashboard
  - Alerting rule set with thresholds
  - Escalation flow for P0 failures
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-17
---

# Flow Error Monitoring

## When to use this skill

Activate when:

- An org has > 50 active flows and fault emails are flooding one inbox.
- You need org-wide visibility into flow-failure trends.
- A specific flow is failing intermittently and you want to establish a baseline before tuning.
- You're setting up ops rotations and need a paging policy for flow failures.
- You're integrating Salesforce with an external observability platform (Splunk, Datadog).

Do NOT use this skill for:
- Diagnosing a specific flow error in isolation (use `skills/flow/flow-runtime-error-diagnosis`).
- Enabling debug mode for step-by-step tracing (use `skills/flow/flow-debugging`).
- Post-mortem root-cause analysis for a critical flow failure (diagnosis + `skills/devops/incident-response`).

## Core concept — three error surfaces

Salesforce exposes flow errors through three independent surfaces. A mature monitoring setup uses all three.

| Surface | Source | Best for |
|---|---|---|
| **Fault emails** | Default Apex fault notifications | Human notification at failure time |
| **Flow Runtime Error report** | `FlowInterviewLog` / Reports tab | Trend analysis, dashboard visualization |
| **Custom log object** (`Integration_Log__c` or similar) | Emit from fault paths in each flow | Centralized, queryable, exportable to external observability |

Fault emails are the default; they're necessary but not sufficient. A monitoring-first org uses all three surfaces, routed by severity.

## Recommended Workflow

1. **Inventory the flow portfolio.** Use Flow Trigger Explorer + `tooling_query('SELECT DeveloperName, Status FROM Flow WHERE Status IN (\'Active\')')` to enumerate active flows.
2. **Decide default fault-email recipient policy.** Most orgs default to the flow creator; route them instead to a shared ops alias or by domain (sales-ops, service-ops).
3. **Classify flows by severity.** P0 (revenue-impacting), P1 (operational), P2 (convenience). Different surfaces + thresholds per severity.
4. **Design the central log object.** Fields: severity, source, message, record Id context, timestamp, correlation Id.
5. **Wire every flow's fault connectors** to write to the log AND (for P0) send a targeted alert. Existing flows: audit via a script that checks for missing fault paths.
6. **Build the runtime error report + dashboard.** Group by flow, by day, by error type. Publish to the ops Slack channel or email.
7. **Set alerting thresholds.** P0: 1 failure = immediate page. P1: 5/hour = email. P2: daily digest.
8. **Schedule a quarterly review** of error trends. Declining P1 rates = flow portfolio getting healthier; growing = something's rotting.

## Key patterns

### Pattern 1 — Central log object design

```
Integration_Log__c
  - Source__c           (Text) — e.g. "Opportunity_StageChange_Flow"
  - Severity__c         (Picklist: CRITICAL, ERROR, WARNING, INFO)
  - Message__c          (Text Long)
  - Record_Id__c        (Text 18) — the record that triggered the failure
  - User_Id__c          (Lookup User)
  - Correlation_Id__c   (Text 64) — for grouping related failures
  - Flow_Name__c        (Text)
  - Flow_Version__c     (Number)
  - Stack_Trace__c      (Text Long)
  - Created_Date        (standard)
```

Index: Severity + Created_Date for the monitoring dashboard query.

### Pattern 2 — Fault path template for every flow

Every flow should terminate every fault connector with the same skeleton:

```
[Critical element — e.g. Create Records]
        │
        fault path
        ▼
[Assignment — build log payload]
        │
        ▼
[Create Records — Integration_Log__c]
        │
        ▼
[Decision — severity = CRITICAL?]
        │
        ├── Yes  → [Send Email Alert] → [End]
        └── No   → [End]
```

Use `templates/flow/FaultPath_Template.md` as the baseline.

### Pattern 3 — Runtime error report

Report type: Flow Interviews with Status = "Error"
- Filter: Last 7 days
- Group by: Flow Name
- Summarize: Count of errors, Last error time
- Subscribe: daily email to ops alias

Add a dashboard component showing weekly trend.

### Pattern 4 — External observability bridge

For orgs with Splunk / Datadog:

```
Integration_Log__c (Create after Insert trigger)
     │
     ▼
[Apex trigger / flow → Platform Event: Integration_Error__e]
     │
     ▼
[Pub/Sub API subscriber in Splunk / Datadog]
     │
     ▼
Dashboards + alerting in external platform
```

Don't pull from Salesforce on a schedule (rate-limited, laggy); push via Platform Event instead.

### Pattern 5 — Alerting thresholds

| Severity | Immediate | Hourly rollup | Daily digest |
|---|---|---|---|
| CRITICAL | Page on-call | — | — |
| ERROR | — | Email if > 5/hour | Always |
| WARNING | — | — | Always |
| INFO | — | — | Only on trend anomaly |

## Bulk safety

- The fault-path log write should be a Create Records (single record per failure), never a Create Records inside a Loop over the failing records — that would compound the failure.
- Bulk-processed flows (record-triggered, scheduled) may log multiple records per transaction; ensure the log object is write-scalable (no required references to other objects that might be missing).

## Error handling

- The fault-path log write can itself fault. Don't infinite-loop: set a max-recursion boundary, or use a second-tier fault path that routes to a raw email.
- If Integration_Log__c fills up, archive to BigObject or dump to external observability — don't delete.

## Well-Architected mapping

- **Reliability** — without monitoring, flow failures accumulate as unnoticed data corruption. Monitoring makes failure visible, which is the precondition for fixing it.
- **Operational Excellence** — ops teams can't run flow portfolios by reading individual fault emails. Centralized logging + trend dashboards are the force multiplier.

## Gotchas

See `references/gotchas.md`.

## Testing

Test each flow's fault path by forcing a known failure in a test class:

```apex
@IsTest
static void testFaultPathLogsCorrectly() {
    // Force a DML failure.
    insertConflictingRecordBeforeFlow();

    Test.startTest();
    // Invoke flow; expect it to take the fault path.
    ...
    Test.stopTest();

    Integration_Log__c log = [SELECT Severity__c, Source__c FROM Integration_Log__c LIMIT 1];
    System.assertEquals('ERROR', log.Severity__c);
    System.assertEquals('Opportunity_StageChange_Flow', log.Source__c);
}
```

## Official Sources Used

- Salesforce Help — Troubleshoot Flows with Flow Runtime Error Reports: https://help.salesforce.com/s/articleView?id=sf.flow_troubleshoot_runtime.htm
- Salesforce Help — Set Flow Apex Exception Email Recipients: https://help.salesforce.com/s/articleView?id=sf.flow_admin_exception_email.htm
- Salesforce Developer — FlowInterviewLog sObject: https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_flowinterviewlog.htm
- Salesforce Architects — Observability Patterns: https://architect.salesforce.com/
