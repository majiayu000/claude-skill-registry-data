---
name: flow-bulkification
description: "Use when designing, reviewing, or troubleshooting Salesforce Flows that must survive data loads, integrations, or high-volume record changes without hitting transaction limits. Triggers: 'Get Records in loop', 'Flow bulkification', 'data loader causing flow errors', 'DML in loop', 'record-triggered flow scale'. NOT for general screen-flow UX or Flow type selection when scale is not the main risk."
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
inputs:
  - "flow type and trigger context"
  - "expected record volume per transaction or schedule"
  - "whether the flow queries or updates related records"
outputs:
  - "bulkification review findings"
  - "collection-based flow redesign guidance"
  - "decision on whether Flow should stay Flow or move to Apex"
dependencies: []
version: 2.0.0
author: Pranav Nagrecha
updated: 2026-04-17
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

## Core Concepts

### Record-Triggered Flows Still Consume Shared Limits

Flows are not exempt from Salesforce governor limits. A record-triggered flow runs in the same transaction budget as Apex triggers, validation rules, process builders, and other automation firing on the same save. Key shared limits per transaction:

| Limit | Per-transaction budget | Typical bulkification impact |
|---|---|---|
| SOQL queries | 100 | Exceeded by `Get Records` inside a loop at ~50 records |
| DML statements | 150 | Exceeded by per-iteration `Update Records` at ~75 records |
| DML rows | 10,000 | Usually not the first limit to hit |
| CPU time | 10,000 ms (sync) / 60,000 ms (async) | Exceeded by complex Decision branches + large collections |
| Heap size | 6 MB (sync) / 12 MB (async) | Exceeded by large collection variables holding many fields |

If the design assumes each interview is isolated (one-record mindset), imports and integrations will expose the mistake as the FIRST production incident.

### Collection-First Design Beats Per-Record Thinking

The safe pattern: collect identifiers, query once, shape data in memory, write once. The unsafe pattern: a `Loop` that performs `Get Records`, `Update Records`, or invocable Apex actions for each iteration. Flow makes it visually easy to build the second pattern, which is why explicit review matters.

The mental model: treat each Flow element as if it runs N times where N is the bulk cardinality. Any element that does `O(N)` work inside the loop becomes `O(N²)` work when called in bulk — and Salesforce's limits are `O(N)`-budget, so `O(N²)` work exhausts them.

### Before-Save And After-Save Have Different Scale Costs

Before-save record-triggered flows are the most efficient place to update fields on the triggering record because they avoid extra DML — the field changes are made IN-MEMORY on the record being saved, before the write commits. After-save flows are necessary for related-record work, but they are more expensive:

| Operation | Before-save cost | After-save cost |
|---|---|---|
| Update field on triggering record | Free (in-memory) | 1 DML statement + 1 recursion if re-triggered |
| Update related record | Not available (can't do cross-object DML before-save) | 1 DML statement per call |
| Create related record | Not available | 1 DML statement per call |
| Call invocable Apex | Available but risky | Available, standard semantics |
| Publish Platform Event | Available | Available; event publishes in same transaction |

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

**Why it works:** `O(N)` DML → `O(1)` DML. Also fails more predictably — if one record in the collection violates a validation rule, you get an `AllOrNone=false` partial success with itemized errors rather than a rollback.

### Pattern 3: Offload Heavy Work To Async Or Apex

**When to use:** The Flow's work exceeds what's reasonable for a synchronous save transaction.

**Signal:** DML count after Pattern 2 still > 150, OR the Flow's fan-out creates > 50 records per source record, OR the Flow needs an external callout per record.

**Approach:**
- **Scheduled Path on the after-save Flow** — delay work by 1+ hours, giving it its own async transaction context.
- **Platform Event + Platform-Event-Triggered Flow** — fire-and-forget; decouples the work from the save transaction.
- **Invocable Apex dispatching to Queueable/Batch** — when the async work is complex enough to need Apex.
- **Change Data Capture + external system** — for genuine integration-heavy fan-out, CDC offloads to external middleware.

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

Step-by-step instructions for an AI agent or practitioner activating this skill:

1. Gather context — confirm the org edition, relevant objects, and current configuration state
2. Review official sources — check the references in this skill's well-architected.md before making changes
3. Implement or advise — apply the patterns from Common Patterns above; compute the scale math
4. Validate — run the skill's checker script and verify against the Review Checklist above
5. Document — record any deviations from standard patterns and update the template if needed

---

## Salesforce-Specific Gotchas

1. **One import can trigger many interviews in one governor budget** — a flow that looks fine during manual testing can fail when 200 records arrive together. This is the most common cause of "the Flow was working yesterday" incidents.
2. **After-save updates on the same record are more expensive than before-save field changes** — using after-save for simple enrichment wastes transaction budget and can trigger more automation (including re-triggering the same Flow on the `Update`).
3. **Subflows do not magically bulkify a bad design** — moving a query-in-loop pattern into a subflow only hides it.
4. **Invocable Apex called from Flow still shares the transaction** — wrapping heavy work in Apex helps only if the Apex code is genuinely bulk-safe (method signature accepts `List<T>`, not a single instance).
5. **Collection variables consume heap memory** — a collection with 10,000 items that each hold 20 fields ≈ ~2 MB of heap. Two such collections + variable assignments may exceed the 6 MB synchronous heap limit. Heap exhaustion is a silent failure mode.
6. **Before-save on certain standard objects has restrictions** — e.g. OpportunityLineItem triggers behave specially around ActivatedDate; check the release notes for your target object before relying on before-save.
7. **Platform Events in a Flow still count against the publish limit** — 6,000 events per hour org-wide. A before-save that publishes one event per save will exhaust this during a 10k-record data load.
8. **Recursion controls on Flow are weaker than on Apex** — a flow that updates its own triggering object in after-save re-fires; use Field History + Decision to check "did this field change" guards as canonical recursion mitigation.

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

## Related Skills

- **flow/record-triggered-flow-patterns** — when the main question is before-save vs after-save behavior and entry criteria rather than scale mechanics.
- **flow/fault-handling** — companion skill; high-volume paths need both bulkification AND predictable failure.
- **flow/scheduled-flows** — when the right bulkification answer is moving work out of the save transaction.
- **apex/governor-limits** — when the safe answer is to move heavy processing into code.
- **apex/trigger-and-flow-coexistence** — when the object has BOTH Apex triggers and Flows; combined budget math lives there.
- **standards/decision-trees/async-selection.md** — when the bulkification answer is "go async"; the tree routes `@future` vs Queueable vs Batch vs Platform Events.
