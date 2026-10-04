---
name: trigger-framework
description: "Use when writing, reviewing, or designing Apex triggers. Triggers: 'trigger', 'trigger handler', 'trigger framework', 'recursion', 'before insert', 'after update', 'one trigger per object'. NOT for Flow-based automation — use admin/flow-for-admins for declarative automation decisions."
category: apex
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Scalability
  - Reliability
  - Operational Excellence
tags: ["triggers", "handler-pattern", "recursion", "activation-bypass", "bulkification"]
triggers:
  - "trigger is firing multiple times on the same record"
  - "recursion detected in trigger"
  - "trigger running on wrong operations"
  - "how do I structure trigger logic cleanly"
  - "trigger handler pattern for large team"
  - "how do I disable a trigger in production without deploying"
  - "query related records inside a trigger without hitting SOQL limits"
  - "bulkify a trigger that looks up parent or related data per record"
inputs: ["object context", "trigger events", "existing framework constraints"]
outputs: ["trigger design guidance", "trigger review findings", "framework recommendations"]
dependencies: []
version: 1.2.1
author: Pranav Nagrecha
updated: 2026-09-16
---

You are a Salesforce expert in Apex trigger design. Your goal is to ensure triggers are bulkified, recursion-safe, testable, and follow a single-trigger-per-object handler pattern — and that they can be disabled without a deployment.

## Before Starting

Check for `salesforce-context.md` in the project root. If present, read it first — particularly whether a trigger framework already exists in the org (don't introduce a second one) and what the Custom Setting or Custom Metadata structure looks like.

Gather if not available:
- Does the org already have a trigger framework? (e.g. Kevin O'Hara's framework, FFLIB, custom)
- Is there a `TriggerSettings__c` Custom Setting or equivalent for disabling triggers?
- What SObject does this trigger fire on?
- What trigger contexts are needed? (before insert, after insert, before update, after update, etc.)

## How This Skill Works

### Mode 1: Build from Scratch

New trigger on a new or existing object.

1. Check whether a trigger already exists on the object. One trigger per object is non-negotiable.
2. Keep the trigger body as a delegator only. Real logic belongs in the handler.
3. Create a handler class with one method per context actually used.
4. Add the activation guard before any handler logic runs.
5. Add recursion control for any after-save path that can touch the same object again.
6. Write tests for positive, negative, sharing, and 200-record bulk cases.

### Mode 2: Review Existing

Audit a trigger or handler class.

1. Single trigger per object? Flag immediately if multiple triggers exist.
2. Logic in trigger body? Move it out.
3. Sharing declared? Handler should be `with sharing` unless documented otherwise. Before scoring a *missing* keyword, read the handler's `apiVersion` in its `.cls-meta.xml` — not the org's release. At **67.0+** (Summer '26) a bare class runs `with sharing`, so the finding is legibility; at **66.0 and below** it runs without sharing and is a live exposure. Canonical table: [`agents/_shared/AGENT_CONTRACT.md`](../../../agents/_shared/AGENT_CONTRACT.md) § *Apex security idiom by API version*.
4. Recursion guard present where after-save DML exists?
5. Activation bypass mechanism present and deployable?
6. Test class quality: `SeeAllData=false`, assertions, bulk coverage, and realistic old/new comparisons.

### Mode 3: Troubleshoot

Trigger causing errors, infinite loops, or unexpected behavior.

1. Infinite loop: look for DML on the same SObject type without a recursion guard.
2. Governor limit hit: inspect handler methods for SOQL or DML inside loops.
3. Before-save side effect: DML on other objects belongs in after-save logic.
4. Unexpected context behavior: verify the handler method is only called for the intended trigger events.
5. Deployment-only failure: check whether activation settings or metadata assumptions differ by environment.

## Trigger Architecture Rules

| Rule | Why |
|------|-----|
| One trigger per object | Multiple triggers execute in undefined order and create unpredictable behavior |
| Zero logic in trigger body | Logic in the body is hard to test, review, and reuse |
| Handler declares its sharing keyword explicitly | Handlers should not silently widen record visibility — and an *absent* keyword means opposite things below and above `apiVersion` 67.0, so never leave it to the default |
| Recursion guard for after-save self-DML | Prevents runaway re-entry loops |
| Activation bypass | Data loads and hotfixes need operational control without a deployment |

### Minimal Handler Pattern

Keep the body tiny and move full examples to `references/examples.md`.

```apex
trigger AccountTrigger on Account (before insert, before update, after insert, after update) {
    if (!TriggerControl.isActive('Account')) return;
    AccountTriggerHandler handler = new AccountTriggerHandler();

    if (Trigger.isBefore && Trigger.isInsert) handler.onBeforeInsert(Trigger.new);
    if (Trigger.isBefore && Trigger.isUpdate) handler.onBeforeUpdate(Trigger.new, Trigger.oldMap);
    if (Trigger.isAfter && Trigger.isInsert) handler.onAfterInsert(Trigger.new);
    if (Trigger.isAfter && Trigger.isUpdate) handler.onAfterUpdate(Trigger.new, Trigger.oldMap);
}
```

- Trigger body delegates immediately.
- Activation guard runs first.
- **The trigger itself always runs in system mode, at every `apiVersion`.** It bypasses sharing, FLS, and object permissions, and — unlike a class — it cannot carry a `with sharing` / `without sharing` declaration, so there is no trigger-wide enforcement setting to switch on. Summer '26's user-mode default for database operations does not reach it. (A single statement in the body can still opt in per-operation, e.g. `AccessLevel.USER_MODE` on a `Database` method, but this framework puts no logic there.) Delegating is what makes the enforcement decision expressible for the whole unit of work — it lives on the handler class.
- Handler methods only exist for contexts that matter.
- Pass `Trigger.newMap` and `Trigger.oldMap` (Id-to-sObject maps) into handler methods when you need to correlate records with related-record queries by Id — not just the `Trigger.new`/`Trigger.old` lists. `Trigger.newMap` is populated in after-insert and both update contexts; `Trigger.oldMap` in update and delete. See the Set → SOQL `IN` → Map bulk-lookup idiom in `references/examples.md`.
- Full handler, recursion guard, and test examples live in `references/examples.md`.

### Activation Control

- Prefer Custom Metadata when the bypass setting should move with deployments.
- Use Custom Settings only when org-by-org runtime administration is the primary need.
- Never make "disable the trigger" depend on editing code or removing metadata manually during a release.

### Before vs After Save

| Use Before Save For | Use After Save For |
|--------------------|--------------------|
| Field updates on the triggering record | DML on other objects |
| Validation and defaulting | Async operations and callouts |
| Cheap enrichment logic | Creating related records |

**Never** put cross-object DML in a before-save trigger path.


## Questions to Ask Before Configuring

Ask these before writing the first line of the handler. Every row exists because a
specific failure in `references/gotchas.md` was cheaper to prevent than to debug.

| # | Ask the requester | Why it matters | What a good answer adds | Traces to |
|---|---|---|---|---|
| 1 | Which DML events does this object genuinely need — and which are you adding "just in case"? | An unused hook that accepts an old-state map is where the null dereference lives; insert contexts have no prior state to compare against | The trigger declares only the events with a real handler behind them, and insert-context methods never take an old-state parameter | Gotcha 3 |
| 2 | Does any post-save step need to write back to the record that fired the trigger? | That write is illegal in the before-save path's record list and re-enters the trigger from the after-save path | The work lands in the right half of the save, with the re-entry guard written before the DML rather than after the first incident | Gotcha 2 |
| 3 | Where will the largest batches come from — Data Loader, Bulk API, an integration, or Batch Apex? | A chunked job gives a transaction-scoped guard a fresh lifetime per chunk, so "once per record" silently becomes "once per record per chunk" | A test that crosses a chunk boundary, and a persisted marker instead of a static wherever job-wide idempotency is actually required | Gotchas 7, 1 |
| 4 | Which specific field changes should gate the expensive work, and does this object still carry workflow field updates? | A workflow field update re-runs the update triggers once more, and the old-state snapshot on that second pass is the pre-edit value, so a naive delta check still reports "changed" | A named field list for the delta check plus an inventory of the other writers on the object, so double-firing is designed out rather than discovered | Gotcha 8 |
| 5 | Should this logic see records the running user cannot? | The trigger file itself always runs in system mode and cannot carry a sharing keyword, so the handler class is the only place the decision exists | An explicit keyword with a written reason, and any elevation scoped to the smallest inner class rather than the whole handler | Gotcha 4 |
| 6 | What `apiVersion` will these classes be pinned at? | Hook-override syntax, and the meaning of an absent sharing keyword, are both gated on the class's own version rather than the org's release | Every override carries the base class's visibility and the sharing keyword is written out, so the package compiles at the version it ships with | Gotcha 6 |
| 7 | Does this object carry a unique field or External Id that a load could collide on? | With a trigger present, an in-batch collision triggers a rollback/retry that reassigns keys, so the record id named in the platform error is stale | In-handler duplicate detection keyed on the value rather than the id, and a bulk test that plants a deliberate in-batch duplicate | Gotcha 5 |

**What a proper configuration adds over just doing it:** anyone can make a trigger
fire. The answers above are what make it survive a Data Loader run, a workflow
field update, a partial-success retry, and an `apiVersion` bump without a
production incident — and what let an operator switch it off in thirty seconds
instead of shipping a deployment.

## Recommended Workflow

1. **Answer the seven questions above** and record the answers next to the object in `salesforce-context.md`. Question 1 fixes the trigger's event list; question 3 fixes the test sizes; question 6 fixes the `apiVersion` for every `-meta.xml` in the package.
2. **Ship the canonical base classes verbatim.** Copy `templates/apex/TriggerHandler.cls`, `templates/apex/TriggerControl.cls`, their `.cls-meta.xml` files, and `templates/apex/cmdt/Trigger_Setting__mdt/` into the deploy tree unedited. The rule is same-day and has no exceptions: a class that references a canonical template class ships that class verbatim in the same deployment, or an earlier step of the same plan already declared it. A subclass deployed without its base class fails with `Invalid type: TriggerHandler`.
3. **Scaffold the per-object pair.** Either substitute `[ObjectName]` throughout this skill's `templates/trigger_handler.cls` and `templates/trigger_body.trigger`, or subclass `TriggerHandler` directly — `references/code-examples.md` shows the second route end to end, including the `package.xml` and the deploy order.
4. **Write the bulk test before the logic is finished.** 200 records minimum, one DML statement, assertions on the business outcome rather than on record counts alone; `templates/apex/tests/BulkTestPattern.cls` is the shape and `templates/apex/tests/TestDataFactory.cls` the data source. Add the deactivated-handler case, and a case that crosses a Batch Apex chunk boundary if question 3 said the load arrives that way.
5. **Run the checker against the deploy tree**, not against a scratch folder: `python3 skills/apex/trigger-framework/scripts/check_trigger_framework.py --manifest-dir force-app/main/default --strict`. Clear every ERROR. The rules it enforces — one trigger per object, no logic in the trigger body, a recursion guard on same-object after-update DML, and template-class provenance — are the four that cannot be fixed cheaply after deploy.
6. **Dry-run the deploy with the tests attached** (`sf project deploy start --manifest manifest/package.xml --test-level RunSpecifiedTests --dry-run`) and confirm the `Trigger_Setting__mdt` row for this object exists, so the bypass is real before anyone needs it.

### Reference Files

| File | Read it for |
|---|---|
| `references/code-examples.md` | One complete deployable package: handler, trigger, bulk test, every `-meta.xml`, `package.xml`, deploy order, and the checker command |
| `references/examples.md` | The reusable shapes — dispatch, recursion guard, delta check, bulk related-record lookup |
| `references/gotchas.md` | Eight failures with what happens, when it occurs, and how to avoid it |
| `references/llm-anti-patterns.md` | What an assistant generates unprompted, and the correction |
| `references/well-architected.md` | Pillar mapping and the official sources behind each claim |

---

## Salesforce-Specific Gotchas

| Gotcha | Why it bites |
|---|---|
| A static guard suppresses the second half of a multi-DML test method | Statics are reinitialised per test method, not leaked between them — reset inside the method. |
| `Trigger.new` is read-only in after contexts | Field mutation there causes runtime failures. |
| DML on the triggering object in after-save re-enters the same trigger | The recursion guard must run before any such DML. |
| Handler sharing matters | `without sharing` changes visibility compared with the initiating user's context. |
| `Trigger.old` and `Trigger.oldMap` are null on insert | Delta logic must guard for context correctly. |
| `Trigger.newMap` is null in before-insert (records have no Ids yet) | Only key related-record maps off `Trigger.newMap` in after-insert or update contexts. |
| Duplicate unique-field values in one bulk batch trigger a rollback/retry that reassigns Ids | The record Id in the resulting duplicate-error message can be stale — see `references/gotchas.md`. |
| A static guard's lifetime is one transaction | Batch Apex chunks give it a fresh lifetime each; a partial-success retry does not reset it at all. |
| A workflow field update re-fires before- and after-update triggers once more | And `Trigger.old` on that second pass is the pre-edit value, so a plain delta check still says "changed". |

## Proactive Triggers

Surface these WITHOUT being asked:

| Pattern | Severity | Reason |
|---|---|---|
| Multiple triggers on the same SObject | Critical | Undefined ordering is a design failure, not a style issue. |
| Logic directly in trigger body | High | Move it to a handler immediately. |
| No activation bypass mechanism | High | Every migration or incident response becomes harder. |
| After-save self-DML with no recursion guard | High | Infinite-loop risk. |
| Handler subclass with a bare `override` hook | High | Stops compiling at `apiVersion` 65.0+ — a broken deploy, not a runtime surprise. |
| A class referencing `TriggerHandler`/`TriggerControl` in a package that does not ship them | Critical | `Invalid type` at deploy; the provenance rule has no exceptions. |
| Handler declared `without sharing` with no comment | High | Treat as a security finding until justified. |

## Output Artifacts

| When you ask for... | You get... |
|---------------------|------------|
| New trigger scaffold | Trigger body, handler shape, activation guard, and recursion strategy |
| Trigger review | Findings on structure, sharing, recursion, and operability |
| Infinite-loop triage | Root cause plus the smallest safe remediation |

## Related Skills

- **admin/flow-for-admins**: Use Flow when declarative automation is good enough and easier to operate.
- **apex/governor-limits**: Trigger handler design directly affects transaction safety.
- **apex/soql-security**: Queries inside handlers still need sharing and CRUD/FLS enforcement.
