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
inputs: ["object context", "trigger events", "existing framework constraints"]
outputs: ["trigger design guidance", "trigger review findings", "framework recommendations"]
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-03-13
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
3. Sharing declared? Handler should be `with sharing` unless documented otherwise.
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
| Handler declared `with sharing` by default | Handlers should not silently widen record visibility |
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
- Handler methods only exist for contexts that matter.
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


## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner activating this skill:

1. Gather context — confirm the org edition, relevant objects, and current configuration state
2. Review official sources — check the references in this skill's well-architected.md before making changes
3. Implement or advise — apply the patterns from Core Concepts and Common Patterns sections above
4. Validate — run the skill's checker script and verify against the Review Checklist below
5. Document — record any deviations from standard patterns and update the template if needed

---

## Salesforce-Specific Gotchas

- **Static recursion guards affect tests too**: Clear static state between tests or expose a reset helper.
- **`Trigger.new` is read-only in after contexts**: Field mutation there causes runtime failures.
- **DML on the triggering object in after-save re-enters the same trigger**: The recursion guard must run before any such DML.
- **Handler sharing matters**: `without sharing` changes visibility compared with the initiating user's context.
- **`Trigger.old` and `Trigger.oldMap` are null on insert**: Delta logic must guard for context correctly.

## Proactive Triggers

Surface these WITHOUT being asked:
- **Multiple triggers on the same SObject** -> Flag as Critical. Undefined ordering is a design failure, not a style issue.
- **Logic directly in trigger body** -> Flag as High. Move it to a handler immediately.
- **No activation bypass mechanism** -> Flag as High. Every migration or incident response becomes harder.
- **After-save self-DML with no recursion guard** -> Flag as High. This is an infinite-loop risk.
- **Handler declared `without sharing` with no comment** -> Flag as High. Treat it as a security finding until justified.

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
