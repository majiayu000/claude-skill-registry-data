---
name: flow-bulkification
description: "Use when designing, reviewing, or troubleshooting Salesforce Flows that must survive data loads, integrations, or high-volume record changes without hitting transaction limits. Triggers: 'Get Records in loop', 'Flow bulkification', 'data loader causing flow errors', 'DML in loop', 'record-triggered flow scale', 'collection variable', 'noMoreValuesConnector', 'Collection Filter', 'Collection Sort', 'Too many SOQL queries: 101', 'Too many DML statements: 151', 'bulk-safe flow XML'. NOT for 'Too many query rows' at LDV scale — use flow/flow-large-data-volume-patterns. NOT for refactoring one Loop element — use flow/flow-loop-element-patterns."
category: flow
salesforce-version: "Spring '25+'"
well-architected-pillars:
  - Scalability
  - Performance
  - Reliability
tags:
  - flow-bulkification
  - governor-limits
  - record-triggered-flow
  - collections
  - scalability
triggers:
  - "flow is failing during data loads or imports"
  - "get records inside a loop in flow"
  - "record triggered flow hitting governor limits"
  - "how do I bulkify a flow for 200 records"
  - "after save flow creates too many updates"
  - "flow bulkification collection update import"
  - "flow hitting SOQL limits"
  - "too many SOQL queries in a flow"
  - "flow query limit exceeded"
  - "System.LimitException: Too many SOQL queries from a flow"
  - "move get records outside the loop in my flow"
  - "build a collection variable and update it once after the loop"
  - "dml inside a flow loop - collect records and update once"
  - "check whether this flow is bulk safe before the integration go live"
  - "flow worked in sandbox but failed on the 200 record data load"
  - "why did only the first child record update in my flow"
  - "bound a scheduled flow so it does not process every record"
  - "review flow-meta.xml for get or update inside a loop"
  - "convert an update records element to a collection update"
  - "flow error too many DML statements 151"
  - "does flow bulkify automatically across interviews"
inputs:
  - "flow type and trigger context"
  - "expected record volume per transaction or schedule"
  - "whether the flow queries or updates related records"
outputs:
  - "bulkification review findings"
  - "collection-based flow redesign guidance"
  - "decision on whether Flow should stay Flow or move to Apex"
dependencies: []
version: 2.1.0
author: Pranav Nagrecha
updated: 2026-09-05
---

Use this skill when a Flow works for one record in a sandbox but becomes dangerous when data arrives in volume. A Flow that a user triggers with a button click may run ONCE with 100 SOQL queries available. The same Flow triggered by a 200-record Bulk API insert runs 200 times in the SAME transaction — with the SAME 100 SOQL budget. A `Get Records` inside a loop that worked fine during UI testing will exhaust the budget on row 50 of the bulk insert and roll back the remaining 150.

The objective of this skill is to redesign Flow automation around collection handling, low-query patterns, and safe transaction scope BEFORE imports, integrations, or mass updates expose the design failure. Fault handling (`flow/fault-handling`) tells you how to survive failures; bulkification tells you how to avoid the most common class of failures in the first place.

## Before Starting

Check for `salesforce-context.md` in the project root. If present, read it first.

Gather if not available:
- What is the maximum expected volume: user save (1 at a time), API batch (200), scheduled run (variable), or bulk data load (up to 10k)?
- Is the flow record-triggered, scheduled, auto-launched, or a subflow called from another bulk process?
- Which elements read or write related records, call Apex, or branch in loops?
- Does the object already have Apex triggers that will share the same transaction budget?
- What's the expected peak concurrency (e.g. integration writes 2000 records/min → 10 parallel batches)?

## Questions to Ask Before Configuring

Ask these before opening Flow Builder or writing a line of flow XML. Each one decides an
element or an attribute in the metadata, and each one traces to a failure that only
appears under volume. An agent that skips them produces a flow that deploys, passes its
flow test, and takes down the nightly integration.

| Ask | Why it matters | What a good answer adds |
|---|---|---|
| "How many records arrive in one transaction — a user save, a 200-record API chunk, or a Data Loader file?" | The budget is per transaction, and a Bulk API chunk of 200 is one transaction with limits reset between chunks | The cardinality for the scale math, and the load-test file size that actually proves anything (`references/gotchas.md` § batches of 200) |
| "For each triggering record, how many related records does this touch — and what is the worst case, not the average?" | Fan-out is the multiplier on every in-loop element; the average hides the account with 400 children | Whether one interview fits at all, and whether the Get needs a `<limit>` (`references/metadata-examples.md` § 2) |
| "Does anything inside the loop read or write the database, or call Apex?" | Elements reachable from a Loop's `nextValueConnector` run once per item, per interview; everything else runs once | The refactor target: which elements move above the loop and which move onto `noMoreValuesConnector` (`references/gotchas.md` § loop without noMoreValuesConnector) |
| "Where does the collection get committed — which element sits on the 'after last' path?" | A Loop with no `noMoreValuesConnector` stages everything and writes nothing, with no error | The single DML element and its `<inputReference>`, rather than a per-record `recordUpdates` with `<filters>` (`references/llm-anti-patterns.md` § 7) |
| "If one row in the collection fails validation, should the whole batch roll back or should the good rows land?" | `recordUpdates` has no all-or-none switch; `recordCreates` in upsert mode has one and it defaults to all-or-none | An explicit `doesUpsertAllOrNone` decision, or the decision to escalate to invocable Apex for per-row results (`references/gotchas.md` § all-or-none) |
| "Does this object already carry Apex triggers or other flows on the same save?" | The 100 SOQL / 150 DML caps are per transaction and shared; the last automation to fire takes the failure | The combined budget math, and a `triggerOrder` conversation with whoever owns the other automation (`apex/trigger-and-flow-coexistence`) |
| "If this is scheduled, what bounds the working set — and who chose that bound?" | A scheduled flow with `<object>` on its Start starts one interview per matching record and has no batch-size field at all | An explicit design: no `<object>`, a Get `<limit>`, and a Collection Sort `<limit>` sized against a measured run (`references/metadata-examples.md` § 4) |

What a proper configuration adds over just building the flow: the element graph is bulk-safe by construction rather than by luck, the commit point is a deliberate single DML with a fault path, the partial-success behaviour was chosen instead of inherited, and there is a load test and a debug-log reading that prove it at the cardinality the org actually sees.

---

## Core Concepts

### Record-Triggered Flows Still Consume Shared Limits

Flows are not exempt from Salesforce governor limits. A record-triggered flow runs in the same transaction budget as Apex triggers, validation rules, process builders, and other automation firing on the same save. Key shared limits per transaction:

| Limit | Synchronous | Asynchronous | Where bulkification spends it |
|---|---|---|---|
| SOQL queries | 100 | 200 | 1 per `Get Records`. One Get on a loop path = 1 x items x interviews |
| DML statements | 150 | 150 | 1 per `Create` / `Update` / `Delete Records` element execution, whatever the row count |
| DML rows | 10,000 | 10,000 | The size of the collection a single `Update Records` commits |
| CPU time | 10,000 ms | 60,000 ms | Decisions, formulas and loop iterations — no database access required to exhaust it |
| Heap size | 6 MB | 12 MB | Collection variables. `<queriedFields>` is the lever, not the row count alone |

Every figure: Apex Developer Guide, Per-Transaction Apex Limits (`apexdev.txt` L19541–19580).
The asynchronous column is not decoration — it is why the same flow behaves differently
on a scheduled path than on the save, and **UNVERIFIED (2026-09-05):** which column a
schedule-triggered flow's interview draws from is not stated in `api_meta.txt` or
`apexdev.txt`; assume synchronous until you have measured
`FLOW_INTERVIEW_FINISHED_LIMIT_USAGE` on a real run.

Do the arithmetic rather than carrying a rule of thumb. One `Get Records` on a loop path,
12 children per parent, 200 records per chunk, is 2,400 queries against a budget of 100 —
it fails inside the eighth record, not at some threshold worth memorising. Halve the
budget again if Apex triggers share the transaction.

If the design assumes each interview is isolated (one-record mindset), imports and integrations will expose the mistake as the FIRST production incident.

### Collection-First Design Beats Per-Record Thinking

The safe pattern: collect identifiers, query once, shape data in memory, write once. The unsafe pattern: a `Loop` that performs `Get Records`, `Update Records`, or invocable Apex actions for each iteration. Flow makes it visually easy to build the second pattern, which is why explicit review matters.

The mental model: treat each Flow element as if it runs N times where N is the bulk cardinality. Any element that does `O(N)` work inside the loop becomes `O(N²)` work when called in bulk — and Salesforce's limits are `O(N)`-budget, so `O(N²)` work exhausts them.

### Before-Save And After-Save Have Different Scale Costs

Before-save record-triggered flows are the most efficient place to update fields on the triggering record because they avoid extra DML — the field changes are made IN-MEMORY on the record being saved, before the write commits. After-save flows are necessary for related-record work, but they are more expensive:

| Operation | Before-save cost | After-save cost |
|---|---|---|
| Update field on triggering record | Free — the assignment is part of the save | 1 DML statement, plus a second pass through the save procedure |
| Update related record | See below | 1 DML statement per `recordUpdates` execution |
| Create related record | See below | 1 DML statement per `recordCreates` execution |
| Call invocable Apex | Shares the transaction; the action receives a bulkified list | Same, with the record already written |
| Publish Platform Event | See below | Publishes within the transaction |

Grounding: record-triggered flows configured to run before the record is saved execute at
step 3 of the order of execution, and the record is written at step 7 (`apexdev.txt`
L15440 and L15447); after-save flows execute at step 14 (L15470). `RecordBeforeSave` is defined
as "Creating and/or updating a record triggers an autolaunched flow to make more updates to
that record **before it's saved to the database**" (`api_meta.txt` L72539–72542). That is
the whole cost argument: an assignment before step 7 rides the write that was already
happening.

**UNVERIFIED (2026-09-05):** which *elements* a before-save flow may contain is not stated
in `api_meta.txt` or `apexdev.txt` — the `Flow` type exposes `recordCreates`,
`recordUpdates`, `actionCalls` and `subflows` unconditionally, with no documented
restriction keyed to `triggerType`. The rows above marked "see below" reflect the
Flow Builder restriction as practitioners encounter it, not a documented one. Treat
before-save as assignment-only in design, and prove any exception in a scratch org;
`flow/record-triggered-flow-patterns` `scripts/check_record_triggered_flow_patterns.py`
enforces the assignment-only shape as a convention.

**Rule:** If the work is "set a field on the triggering record based on its other fields", ALWAYS prefer before-save.

### Bulkification Sometimes Means Escalating Out Of Flow

If the use case requires deep joins, heavy fan-out, callouts per record, or nightly processing across very large datasets, the correct bulkification answer may be Batch Apex, Queueable dispatch, Platform Events, or a scheduled integration rather than more Flow complexity. The sign that you've crossed the line: the Flow's collection variables exceed ~1000 items, or the Flow's DML count cannot be reduced below the limit without heroic redesign.

## Common Patterns

### Pattern 1: Query Once, Reuse In The Loop

**When to use:** The flow must compare or update child or sibling records for many triggering records.

**Before (anti-pattern):**
```text
Loop over triggering records:
    └── [Get Records: Contact WHERE AccountId = currentRecord.AccountId]
        (executes N times — 200-record load = 200 SOQL queries)
```

**After:**
```text
[Assignment: collect accountIds from triggering records into Set<Id>]
[Get Records: Contact WHERE AccountId IN :accountIds]  // ONE query, all contacts
[Loop over triggering records]:
    └── Filter the pre-fetched Contact collection by AccountId in memory
```

**Why it works:** Converts an `O(N)` SOQL pattern to `O(1)` SOQL. Scales linearly instead of linearly-in-queries.

### Pattern 2: Build An Update Collection And Commit Once

**When to use:** The flow needs to update many related records.

**Before:**
```text
Loop over triggering records:
    └── [Get Related Contact]
    └── [Update Contact]  // N DML calls
```

**After:**
```text
[Assignment: accountIds collection]
[Get Records: Contact WHERE AccountId IN :accountIds]  // 1 query
[Loop over triggering records]:
    └── [Find matching Contact in collection]
    └── [Assignment: modify Contact fields, add to contactsToUpdate collection]
[Update Records: contactsToUpdate]  // 1 DML call (bulk-safe up to 10k rows)
```

**Why it works:** `O(N)` DML → `O(1)` DML — it moves the element off the 150-DML-statements-per-transaction limit, which is the actual failure this pattern prevents.

**What it does NOT buy you: partial success — on this element.** `FlowRecordUpdate` has exactly six fields — `connector`, `faultConnector`, `filters`, `inputAssignments`, `inputReference`, `object` (`api_meta.txt` L71279–71296). There is no all-or-none switch, so one row violating a validation rule fails the whole collection, and there is no itemized per-row result to inspect. Salesforce documents the same behaviour on the schedule-triggered path: "if a schedule-triggered flow has a Create Records, Delete Records, Get Records, or Update Records element that processes multiple records and some records fail, all records are rolled back."

**One declarative exception, and it is easy to miss.** `FlowRecordCreate` gained `doesUpsert` and `doesUpsertAllOrNone` in API 62.0: "If set to true and a record fails, then the transaction rolls back and no records are created or updated. If set to false, the transaction creates or updates only the records that are successful. The default value is `true`" (`api_meta.txt` L70953–70963). So a bulk write *can* be partial declaratively — as a Create-in-upsert-mode with `doesUpsertAllOrNone` explicitly `false` — but only there, and never by accident, because the default is all-or-none. Choose it; do not inherit it.

Bulkifying makes the Flow *fit inside limits*; it does not by itself make failures granular. If you need per-record error isolation with inspectable results, you need Invocable Apex using `Database.update(records, false)` and reading `Database.SaveResult[]` — see Pattern 3 and `apex/invocable-methods`.

### Pattern 3: Offload Heavy Work To Async Or Apex

**When to use:** The Flow's work exceeds what's reasonable for a synchronous save transaction.

**Signal:** DML count after Pattern 2 still > 150, OR the Flow's fan-out creates > 50 records per source record, OR the Flow needs an external callout per record.

**Approach:**

| Mechanism | When to use |
|---|---|
| Scheduled Path on the after-save Flow | Delay work by 1+ hours, giving it its own async transaction context. |
| Platform Event + Platform-Event-Triggered Flow | Fire-and-forget; decouples work from the save transaction. |
| Invocable Apex dispatching to Queueable/Batch | When the async work is complex enough to need Apex. |
| Change Data Capture + external system | Integration-heavy fan-out; CDC offloads to external middleware. |

See `standards/decision-trees/async-selection.md` for the full async-target decision.

### Pattern 4: Use Before-Save For Same-Record Field Changes

**When to use:** Any rule that sets a field on the triggering record based on its own other fields (or its parent, if the parent is already fetched by the save context).

**Example:** "Set `Priority = 'High'` when `Amount > 50000`".

**Implementation:**
```text
Before-save record-triggered flow on Opportunity:
    └── [Decision: Amount > 50000]
         └── Yes → [Assignment: $Record.Priority = 'High']
```

No DML. No new transaction. No governor cost beyond negligible CPU. This is the cheapest automation pattern Salesforce offers.

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Update only fields on the triggering record | Before-save record-triggered flow | Lowest transaction cost (zero DML) |
| Update related records for many triggering records | After-save flow with Pattern 1 + Pattern 2 | Related DML requires after-save but must stay collection-based |
| Large nightly or imported dataset with complex joins | Batch Apex or async pattern (Pattern 3) | Flow becomes harder to bulkify than code at this scale |
| Loop contains queries, DML, or invocable Apex | Refactor immediately (Pattern 1 or 2) | This is the highest-risk Flow bulkification smell; P0 in review |
| Flow has > 1000 items in a collection variable | Consider escalation (Pattern 3) | Approaching heap limits; one more fetch may tip over |
| Per-source-record fan-out > 10 related records | Escalation candidate | Linear DML growth hits the 150-statement limit quickly |
| User-triggered one-at-a-time | Any pattern works; optimize for readability | Single-record mode is forgiving |

## Scale Math Worksheet

Before approving a record-triggered Flow, do this math:

```
Per-interview SOQL count: ___
Per-interview DML count: ___
Max expected bulk cardinality: ___

SOQL × cardinality: ___   (must be < 100)
DML × cardinality: ___    (must be < 150)

If Apex triggers are ALSO on the object:
  Apex SOQL + Flow SOQL = ___  (combined, must still be < 100)
  Apex DML + Flow DML = ___    (combined, must still be < 150)
```

If either combined number exceeds the limit, redesign BEFORE deploying. If the team can't estimate "expected bulk cardinality", default to 200 (Salesforce's standard batch size for data-load pipelines).

## Review Checklist

- [ ] No `Get Records`, `Create`, `Update`, `Delete`, or Apex action is executed per loop iteration without a justified exception.
- [ ] Before-save is used when only the triggering record needs field changes.
- [ ] Related-record writes are collected and committed intentionally (Pattern 2).
- [ ] The design considers imports, integrations, and data-loader scenarios, not just one-click UI saves.
- [ ] Fault handling exists for the bulk path, not only the single-record happy path.
- [ ] Scale math has been computed: SOQL × cardinality < 100, DML × cardinality < 150.
- [ ] If the object has Apex triggers, the combined SOQL + DML math still fits.
- [ ] The team explicitly decided whether Flow is still the right implementation at the expected scale.
- [ ] Collection variables stay under ~1000 items (heap consideration).


## Recommended Workflow

1. **Get the cardinality before you look at the flow.** Answer the seven questions above,
   especially the first two: records per transaction, and worst-case fan-out per record.
   Everything downstream is that pair multiplied. If nobody can say, use 200 — a Bulk API
   chunk is 200 records and limits reset between chunks (`references/gotchas.md` § batches
   of 200), so 200 is the smallest number that can still fail.
2. **Read the connector graph, not the canvas.** In the `*.flow-meta.xml`, walk each
   `<loops>` element from `<nextValueConnector>` until you return to the loop. Every
   `recordLookups`, `recordCreates`, `recordUpdates`, `recordDeletes`, `actionCalls` and
   `subflows` on that path is a per-iteration cost. Then check that `<noMoreValuesConnector>`
   exists and lands on a DML element — a loop that stages a collection and never commits it
   is the one bulkification defect that raises no error at all.
3. **Compute the scale math and write it down.** SOQL x cardinality < 100 and DML x
   cardinality < 150, with the Apex triggers on the object included in the same sum
   (§ Scale Math Worksheet). The worked comparison is in `references/examples.md` § 3.
4. **Refactor to the collection shape, using the XML in
   `references/metadata-examples.md` § 2** — one `Get Records` above the loop with
   `<getFirstRecordOnly>false</getFirstRecordOnly>` and narrow `<queriedFields>`, a loop
   body containing only an `assignments` element that appends with `<operator>Add</operator>`,
   and one `recordUpdates` on `noMoreValuesConnector` carrying `<inputReference>`. Push
   per-item filtering out of the loop entirely with a Collection Filter (§ 3). Route every
   database element's `faultConnector` per `templates/flow/FaultPath_Template.md`. Start
   record-triggered flows from `templates/flow/RecordTriggered_Skeleton.flow-meta.xml`.
5. **Decide the failure semantics explicitly.** All-or-none is the default and the only
   option on `recordUpdates`; `doesUpsertAllOrNone` on a Create-as-upsert is the one
   declarative alternative (Pattern 2). If you need per-row results, that is the escalation
   signal to Pattern 3, not a Flow tuning problem.
6. **Run the checker, then the flow test, then a real 200-record load.**
   `python3 skills/flow/flow-bulkification/scripts/check_flow_bulkification.py
   --manifest-dir force-app/main/default` reports database elements on loop paths, loops
   with no commit, missing collection staging, DML-element counts and unbounded scheduled
   flows. Deploy the `FlowTest` (`references/metadata-examples.md` § 5) — it pins that the
   loop staged something and the bulk DML did not fault, which is all a single interview can
   prove. Then load 200 records; a flow that has never seen a full chunk has not been tested.
7. **Read the debug log before activating in production.** Set the `Workflow` category to
   `FINER` and check `FLOW_BULK_ELEMENT_LIMIT_USAGE` against the budget, and
   `FLOW_BULK_ELEMENT_NOT_SUPPORTED` for anything the platform declined to bulkify
   (`references/metadata-examples.md` § 8). Record the measured numbers in
   `templates/flow-bulkification-template.md` so the next reviewer inherits evidence rather
   than an estimate.

---

## Salesforce-Specific Gotchas

1. **One import can trigger many interviews in one governor budget** — a flow that looks fine during manual testing can fail when 200 records arrive together. This is the most common cause of "the Flow was working yesterday" incidents.
2. **After-save updates on the same record are more expensive than before-save field changes** — using after-save for simple enrichment wastes transaction budget and can trigger more automation (including re-triggering the same Flow on the `Update`).
3. **Subflows do not magically bulkify a bad design** — moving a query-in-loop pattern into a subflow only hides it.
4. **Invocable Apex called from Flow still shares the transaction** — wrapping heavy work in Apex helps only if the Apex code is genuinely bulk-safe (method signature accepts `List<T>`, not a single instance).
5. **Collection variables consume heap memory** — a collection with 10,000 items that each hold 20 fields ≈ ~2 MB of heap. Two such collections + variable assignments may exceed the 6 MB synchronous heap limit. Heap exhaustion is a silent failure mode.
6. **Before-save on certain standard objects has restrictions** — **UNVERIFIED (2026-09-05):** the specific OpportunityLineItem / `ActivatedDate` behaviour this bullet used to name is not stated in `apexdev.txt` or `object_reference.txt`; searching both for `ActivatedDate` returns only field definitions, and the guide's `OpportunityLineItem` material is a bulk-trigger example (`apexdev.txt` L15202–15240), not a restriction. What *is* documented and matters here: on a recursive save Salesforce skips steps 9 through 17 of the order of execution — which includes after-save record-triggered flows at step 14 (`apexdev.txt` L15414–15415, L15470). Verify per-object before-save behaviour in a scratch org rather than trusting a remembered rule.
7. **Platform Events in a Flow still count against the org-wide publish allocation** — Standard-Volume is 100,000 events/hour org-wide on Enterprise / Performance / Unlimited, but only 1,000/hour on Developer and Professional-with-API-Add-On. A before-save that publishes one event per save will exhaust the Developer-edition allocation during a 1k-record load and the Enterprise allocation during a 100k-record load, and the bucket is shared with every other Standard-Volume publisher in the org.
8. **Recursion controls on Flow are weaker than on Apex** — a flow that updates its own triggering object in after-save re-fires, and each re-entry spends more of the same transaction budget. The canonical guard is `<doesRequireRecordChangedToMeetCriteria>true</doesRequireRecordChangedToMeetCriteria>` on the Start element: "conditions evaluate to true only if the record didn't meet the required conditions before the triggering update but now meets the conditions after the update", API 50.0+ (`api_meta.txt` L72322–72325; the same field exists on `FlowRule`, L71320–71323). Field History is a tracking feature, not a recursion control — do not reach for it here. The hard ceiling is stack depth 16 for recursive trigger firing (`apexdev.txt` L19559–19560); you will exhaust SOQL or DML long before you reach it.

## Proactive Triggers

Surface these WITHOUT being asked:

- **`Get Records` inside a `Loop` element** → Flag as Critical. This is the #1 Flow bulkification anti-pattern; refactor via Pattern 1.
- **DML inside a `Loop` element** → Flag as Critical. Refactor via Pattern 2.
- **Invocable Apex with single-instance signature called from record-triggered Flow** → Flag as High. Make the invocable method `List<T>`-safe.
- **After-save Flow doing only same-record field updates** → Flag as High. Convert to before-save — free performance win.
- **Flow on high-volume object (> 1M records) with no scale math documented** → Flag as High. Request the math before approving.
- **Per-source-record fan-out > 10 related records created in after-save** → Flag as Medium. Consider moving to async.
- **Collection variable in a Flow holds > 1000 items** → Flag as Medium. Approaching heap limit; review.
- **Flow on object that ALSO has Apex triggers, with no combined-budget analysis** → Flag as Medium. The combined SOQL + DML math is the real constraint.

## Output Artifacts

| Artifact | Description |
|---|---|
| Bulkification review | Findings on loop design, query count risk, DML fan-out, async boundaries, combined-transaction math |
| Flow redesign plan | Collection-based pattern or before-save/after-save refactor recommendation with worked math |
| Escalation decision | Guidance on whether the workload should stay in Flow or move to Batch Apex / Queueable / Platform Events |
| Scale math worksheet | Worked computation of SOQL × cardinality and DML × cardinality for the specific Flow |

## Reference Files

| File | Read it when |
|---|---|
| `references/metadata-examples.md` | You are writing or reviewing actual `*.flow-meta.xml`: the anti-pattern fixture, the corrected collection flow, a Collection Filter + Sort variant, a bounded scheduled batch flow, a `FlowTest`, `package.xml`, deploy order, and the debug-log verification that is the only direct evidence of bulkification |
| `references/gotchas.md` | The flow deploys, passes its test, and still fails or silently does nothing at volume — bulk-element semantics, `getFirstRecordOnly` coupling, loops with no commit, scheduled flows with no batch dial, all-or-none behaviour |
| `references/examples.md` | You want the narrative before/after, or the reviewable scale-math table for a flow you have been handed |
| `references/llm-anti-patterns.md` | You are reviewing flow advice or generated flow XML from an AI assistant, or self-checking your own output — includes the two claims that get repeated without grounding |
| `references/well-architected.md` | You need the pillar framing, the tradeoffs, or the source and guide line behind any claim in this skill |
| `templates/flow-bulkification-template.md` | You are recording the review — loop audit, measured limit usage, refactor decision — for someone else to act on |
| `scripts/check_flow_bulkification.py` | Before every deploy, and against any fixture directory. `--manifest-dir <source tree>`, optional `--max-dml`; exits non-zero on any finding |

---

## Related Skills

- **flow/record-triggered-flow-patterns** — when the main question is before-save vs after-save behavior and entry criteria rather than scale mechanics.
- **flow/fault-handling** — companion skill; high-volume paths need both bulkification AND predictable failure.
- **flow/scheduled-flows** — when the right bulkification answer is moving work out of the save transaction.
- **apex/governor-limits** — when the safe answer is to move heavy processing into code.
- **apex/trigger-and-flow-coexistence** — when the object has BOTH Apex triggers and Flows; combined budget math lives there.
- **flow/flow-loop-element-patterns** — when the question is the Loop element itself: iteration-variable aliasing, the retired 2,000-element ceiling, empty-collection behaviour.
- **flow/flow-collection-processing** — when the work is the Collection Filter / Sort / Transform elements rather than the transaction budget around them.
- **flow/flow-batch-processing-alternatives** — when the bounded-scheduled-flow shape in `references/metadata-examples.md` § 4 still is not enough and the workload needs a different engine.
- **apex/invocable-methods** — the method-side contract for an Apex action called from a bulkified flow: list in, list out, same size, same order.
- **flow/flow-testing** — when you need more coverage than the single-interview `FlowTest` in `references/metadata-examples.md` § 5 can give.
- **standards/decision-trees/async-selection.md** — when the bulkification answer is "go async"; the tree routes `@future` vs Queueable vs Batch vs Platform Events.
