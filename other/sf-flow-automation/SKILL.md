---
name: sf-flow-automation
description: Record-triggered and autolaunched Flow as a first-class automation layer - the FlowTriggerType and RecordTriggerType matrix, before-save versus after-save placement inside the order of execution, entry conditions and re-entry control, scheduled paths and asynchronous paths, choosing Flow versus Apex trigger and never both on one object, calling Apex from Flow with @InvocableMethod and @InvocableVariable, FlowTest metadata for automated flow tests, flow versioning and the flows/ plus flowDefinitions/ metadata shape, activation on deploy and flow test coverage, and the governor limits flows share with Apex. Use when adding or reviewing a record-triggered flow, deciding between declarative and code automation, writing an invocable Apex action, or when a deploy fails on flow activation or flow coverage.
---

# Flow Automation

## When to use

- A story asks for record automation and no Apex exists on that object yet.
- Reviewing or changing anything under `force-app/main/default/flows/`.
- Writing an `@InvocableMethod` so a flow can call Apex.
- A deploy failed on flow activation or on flow test coverage.
- Wave 1 of the vibe-force workflow: `sf-metadata-engineer` owns `flows/**` (see
  `scripts/lib/sf-paths.js`); `sf-apex-engineer` owns the invocable class it calls.

Flow and Apex are not two styles of doing the same thing. They occupy **different slots in the
order of execution** and they interleave by that order, not by your intent.

## Decision table: Flow, Apex trigger, or neither

| Situation | Use | Why |
| --- | --- | --- |
| Set a field on the record being saved, from data on that same record | **Before-save record-triggered flow** | No extra DML, no extra save cycle. The cheapest automation the platform has |
| Create or update a *related* record when this one changes | **After-save record-triggered flow** | The record has an Id by then |
| Delete-time side effects | **Record-triggered flow, `RecordBeforeDelete`** | Runs before the row leaves the database |
| Work on a schedule | **Scheduled flow** (`triggerType` `Scheduled`), or scheduled Apex | Flow first; Apex when the logic is not expressible |
| React to a platform event | **Platform event-triggered flow** (`triggerType` `PlatformEvent`) or an Apex trigger on the event | Flow when the handler is simple routing |
| Complex branching, recursion, callouts, bulk algorithms | **Apex** | Flow has no good answer for these |
| Anything needing an exact execution order relative to other logic on the same object | **One mechanism, chosen deliberately** | Flows and Apex triggers interleave by order of execution |
| The object already has an Apex trigger doing this domain's work | **Apex** | Two owners on one object is the defect, not the technology |
| A rollup, a formula, a validation rule, or a standard feature covers it | **Neither** | See skill `sf-minimal-change` |

**The rule that matters:** decide one owner per rule per object. A field maintained by both a flow
and a trigger is a race you will debug at 3am.

## Where flows sit in the order of execution

| Step | What runs |
| --- | --- |
| 3 | **Record-triggered flows configured to run before the record is saved** |
| 4 | All `before` triggers |
| 5 | System validation and custom validation rules |
| 6 | Duplicate rules |
| 7 | Record saved to the database, not committed |
| 8 | All `after` triggers |
| 11 | Workflow rules |
| 13 | Processes and flows launched by workflow rules, **in no guaranteed order** |
| 14 | **Record-triggered flows configured to run after the record is saved** |
| 16-17 | Roll-up summary recalculation on parent, then grandparent |
| 19 | Commit |
| 20 | Post-commit: email, enqueued async Apex, **asynchronous paths in record-triggered flows** |

Two consequences:

1. A before-save flow mutates the **same in-memory record** as a before trigger, and runs *first*.
   If a before trigger later overwrites the same field, the trigger wins.
2. An after-save flow runs **after** every after trigger. Anything it writes goes through the whole
   save procedure again.

The full annotated sequence is in
[references/order-of-execution-for-flows.md](references/order-of-execution-for-flows.md).
Trigger-side detail lives in skill `sf-apex-development`.

## Core patterns

### 1. Before-save flow for same-record field updates

Set `triggerType` to `RecordBeforeSave` and `recordTriggerType` to `Create`, `Update` or
`CreateAndUpdate`. Assign to the `$Record` variable. Do **not** add an Update Records element for
the triggering record - that would turn a free field assignment into a second save.

Metadata shape:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Flow xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>67.0</apiVersion>
    <label>Opportunity Set Renewal Date</label>
    <processType>AutoLaunchedFlow</processType>
    <status>Active</status>
    <start>
        <object>Opportunity</object>
        <triggerType>RecordBeforeSave</triggerType>
        <recordTriggerType>CreateAndUpdate</recordTriggerType>
        <filterLogic>and</filterLogic>
        <filters>
            <field>StageName</field>
            <operator>EqualTo</operator>
            <value><stringValue>Closed Won</stringValue></value>
        </filters>
        <doesRequireRecordChangedToMeetCriteria>true</doesRequireRecordChangedToMeetCriteria>
    </start>
</Flow>
```

### 2. Entry conditions, always

`filters` on the `start` element are the flow equivalent of an early `return` in a trigger handler.
`doesRequireRecordChangedToMeetCriteria` set to `true` means the flow runs only on the save where
the record *became* matching, not on every subsequent save while it still matches. That single
element is the difference between an idempotent flow and one that fires forever.

### 3. After-save flow for related records

`triggerType` `RecordAfterSave`. The triggering record has an Id, so you can create children,
update a parent, or publish a platform event. Everything it writes re-enters the save procedure
at step 1, which is how flow-to-trigger recursion happens.

### 4. Asynchronous path when the work can wait

A record-triggered flow can define an asynchronous path that runs **after commit** (step 20). Use
it for callouts and for anything that must not extend the user's save. It is the declarative
equivalent of a queueable and it does not need `callout=true` plumbing.

Scheduled paths (`scheduledPaths`, API 51.0 and later) run at a defined offset from a date field
or from the trigger - a declarative alternative to a scheduled job for "3 days after close".

### 5. Calling Apex from a flow

```apex
public with sharing class RenewalReminderAction {
    public class Request {
        @InvocableVariable(required=true label='Opportunity Id')
        public Id opportunityId;

        @InvocableVariable(label='Days before expiry')
        public Integer leadDays;
    }

    public class Result {
        @InvocableVariable(label='Reminder created')
        public Boolean created;
    }

    @InvocableMethod(
        label='Create Renewal Reminder'
        description='Creates a renewal reminder task for each opportunity'
        category='Renewals'
    )
    public static List<Result> run(List<Request> requests) {
        List<Task> tasks = new List<Task>();
        for (Request r : requests) {
            tasks.add(new Task(
                WhatId = r.opportunityId,
                Subject = 'Renewal reminder',
                ActivityDate = Date.today().addDays(r.leadDays == null ? 30 : r.leadDays)
            ));
        }
        insert as user tasks;

        List<Result> results = new List<Result>();
        for (Integer i = 0; i < requests.size(); i++) {
            Result res = new Result();
            res.created = true;
            results.add(res);
        }
        return results;
    }
}
```

Hard rules from the Apex Developer Guide:

- The method must be `static` and `public` or `global`, and its class must be an **outer class**.
- **Only one method per class** can carry `@InvocableMethod`.
- The only annotation that may accompany it is `@Deprecated`.
- At most **one input parameter**, and it must be a `List` - of a primitive, an sObject, the generic
  `sObject`, a list of those lists, or a user-defined type whose members carry `@InvocableVariable`.
- The return type, if not null, follows the same list rules.
- `@InvocableVariable` fields of type `List<List<sObject>>` are **not supported** in user-defined
  classes and cause a runtime error. Use that type only as a direct `@InvocableMethod` return type.
- Add `callout=true` when the method calls an external system.

The list-in, list-out signature is not a style choice. It is how the platform bulkifies the action
when the flow processes many records. Write the body to match: never loop a DML statement inside it.

Prefer `@InvocableMethod` over the older `Process.Plugin` interface. The guide is explicit: the
interface does not support `Blob`, collection or sObject data types and does not support bulk
operations, and a class implementing it can only be referenced from flows.

### 6. Test the flow, not just the Apex it calls

`FlowTest` is real metadata (API 55.0 and later), suffix `.flowtest`, stored in the `flowtests`
folder:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<FlowTest xmlns="http://soap.sforce.com/2006/04/metadata">
    <label>Renewal reminder is created on Closed Won</label>
    <flowApiName>Opportunity_Set_Renewal_Date</flowApiName>
    <description>Covers the Closed Won entry condition</description>
    <testType>WithAssertion</testType>
    <testPoints>
        <!-- FlowTestPoint entries: parameters and assertions -->
    </testPoints>
</FlowTest>
```

`testType` `WithAssertion` means the test compares the actual flow outcome against the expected
outcome that the assertions define. Flow tests cover record-triggered, autolaunched and Data
Cloud-triggered flows.

Apex called by a flow still needs ordinary Apex tests: a `FlowTest` does not produce Apex coverage.

## Metadata and deployment

| Concern | Fact |
| --- | --- |
| Directory | `flows/`, file `Foo.flow-meta.xml`. The file is the definition; the org holds the versions |
| Active version | `<status>Active</status>` in the flow file is the modern mechanism |
| `FlowDefinition` | `flowDefinitions/`, suffix `.flowDefinition`, field `activeVersionNumber`. **Legacy** |
| Conflict rule | If you deploy flow definitions, `activeVersionNumber` **overrides** the `status` field in the flow. Deploying definition v3 alongside flow v4 marked Active leaves v3 active |
| Recommendation | Since API 44.0 Salesforce recommends flow file names without version numbers, discontinuing `FlowDefinition` for activation, and using the `Flow` object instead |
| Wildcards | `FlowDefinition` supports `*` in `package.xml` |

Because `FlowDefinition` silently wins over `status`, a repository that contains both is a repository
where nobody can predict which version goes live. Pick the `Flow` object and delete the definitions.

Deploying an **active** flow into production can require flow test coverage depending on org
configuration. Two ways out: ship `FlowTest` metadata, or deploy the flow inactive and activate it
afterwards. Details and the error text are in skill `sf-deployment-strategies`.

## Limits

Flows run **inside the same transaction** as the DML that triggered them and share the Apex
per-transaction governor limits. A record-triggered flow doing a Get Records inside a loop burns
the same 100 SOQL queries an Apex loop would. CPU time is calculated for the executing code *and*
for processes called from it.

Code Analyzer's Flow rule `DbInLoop` detects Get, Create, Update and Delete Records elements
inside loops and names the 150 DML and 100 SOQL ceilings directly. The fix is the same as in Apex:
collect into a collection variable, act once outside the loop, use the `In` operator to fetch by a
collection of ids.

Full limit tables: skill `sf-governor-limits`.

## Anti-patterns

### Update Records on the triggering record in a before-save flow

The whole value of a before-save flow is that assigning to `$Record` costs nothing. Adding an
Update Records element for that same record converts it into an extra save cycle and re-enters the
order of execution. Assign to `$Record` and finish.

### A flow and a trigger both maintaining one field

```
Flow:    Opportunity.Renewal_Date__c = CloseDate + 365   (step 3, before save)
Trigger: Opportunity.Renewal_Date__c = CloseDate + 180   (step 4, before)
```

The trigger wins, today. Change the flow's step and the answer changes. Decide one owner.

### No entry condition

A record-triggered flow with no `filters` runs on every save of every record of that object,
forever, including saves caused by unrelated automation. Add `filters` and
`doesRequireRecordChangedToMeetCriteria`.

### Get Records inside a loop

```
Loop over Opportunities
  Get Records: Line Items where OpportunityId = current item Id   <-- one query per iteration
```

Fix: one Get Records with the `In` operator over a collection of ids before the loop, then work in
memory. Detected by Code Analyzer rule `DbInLoop`; `vf-check analyzer` fails on it.

### An invocable method that loops DML

```apex
@InvocableMethod(label='Bad')
public static void run(List<Request> requests) {
    for (Request r : requests) {
        insert new Task(WhatId = r.recordId);   // one DML per request
    }
}
```

The platform hands you a list precisely so you can do one DML. Build the list, insert once.

### `Process.Plugin` in new code

No bulk support, no sObject or collection types, referenceable only from flows. Use
`@InvocableMethod`.

### Shipping `FlowDefinition` files alongside active flows

The definition's `activeVersionNumber` overrides the flow's `status`. Remove `flowDefinitions/`
from the package unless you are maintaining a pre-API-44 org deliberately.

## Verification

```bash
# Static analysis, including the Flow rules
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" analyzer --changed

# Metadata XML shape and api version drift, plus the whole local gate
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" local --changed

# Deploy validation before touching a shared org
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" deploy-validate --target-org <alias>

# Which flows exist in the org, and which version is active
sf data query --query "SELECT Id, MasterLabel, ProcessType, TriggerType, Status, VersionNumber FROM FlowDefinitionView" --use-tooling-api --target-org <alias>

# Retrieve one flow to compare the org against the repository
sf project retrieve start --metadata Flow:Opportunity_Set_Renewal_Date --target-org <alias>

# After deploy: did the flow actually run?
sf apex get log --number 1 --target-org <alias> | grep -E "FLOW_|CODE_UNIT_STARTED"
```

Debug logs record flow execution under `FLOW_*` markers; log setup is in skill
`sf-debugging-logs`. Post-deploy probes are in skill `sf-post-deploy-verification`.

## References

- [references/flow-metadata-reference.md](references/flow-metadata-reference.md) - `Flow`, `FlowDefinition`, `FlowTest` fields, trigger type enumerations
- [references/order-of-execution-for-flows.md](references/order-of-execution-for-flows.md) - the full save sequence, annotated for flow authors
- [references/invocable-apex.md](references/invocable-apex.md) - `@InvocableMethod` and `@InvocableVariable` rules, recipes, testing
- [references/workflow-to-flow-migration.md](references/workflow-to-flow-migration.md) - workflow rule to flow mapping tables, the before/after split, `/vf-migrate-workflow`

Process Builder is a separate migration with separate rules: skill `sf-process-builder-migration`
(criteria-node chaining, scheduled actions, `/vf-migrate-process`).

Sibling skills: `sf-apex-development` (triggers, handler shape, order of execution),
`sf-minimal-change` (declarative versus code, standard features first), `sf-governor-limits`
(the limits flows share with Apex), `sf-code-analyzer-quality` (the Flow rule set),
`sf-deployment-strategies` (flow activation and coverage on deploy), `sf-project-structure`
(`flows/` in the metadata directory map), `sf-debugging-logs` (`FLOW_*` log markers),
`sf-async-apex-patterns` (when the async path needs to be Apex instead).

Sources: Apex Developer Guide "Triggers and Order of Execution", "InvocableMethod Annotation",
"Passing Data to a Flow Using the Process.Plugin Interface"; Metadata API Developer Guide `Flow`,
`FlowDefinition`, `FlowTest`; Salesforce Code Analyzer Flow rule `DbInLoop`. All Summer '26 /
API version 67.0.
