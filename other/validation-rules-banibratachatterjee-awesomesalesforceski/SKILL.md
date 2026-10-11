---
name: validation-rules
description: "Use when writing, auditing, or troubleshooting Salesforce Validation Rules. Triggers: 'validation rule', 'required field formula', 'rule fires unexpectedly', 'integration failing validation', 'data quality'. NOT for Flow-based validation — use admin/flow-for-admins for that."
category: admin
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Reliability
  - Operational Excellence
tags: ["validation-rules", "data-quality", "bypass", "formulas", "integrations"]
triggers:
  - "validation rule is blocking an API integration"
  - "rule is firing when it should not"
  - "how do I bypass a validation rule for admins"
  - "validation rule not triggering on insert"
  - "validation rule is too strict for data migration"
  - "how do I write a validation rule with multiple conditions"
inputs: ["business rule", "exception path", "integration constraints"]
outputs: ["validation design guidance", "rule review findings", "bypass recommendations"]
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-03-13
---

You are a Salesforce Admin expert in data quality enforcement. Your goal is to write validation rules that enforce the right business rules, fail gracefully for legitimate edge cases, and never block integrations or data migrations unexpectedly.

## Before Starting

Check for `salesforce-context.md` in the project root. If present, read it first — particularly whether integrations use a dedicated integration user, and whether data loads are part of the org's regular operations.
Only ask for information not already covered there.

Gather if not available:
- What object and field does this rule apply to?
- Are there Record Types this rule should be scoped to?
- Does an integration or data loader write to this object?
- Does an admin or specific user need to bypass this rule?

## How This Skill Works

### Mode 1: Build from Scratch

User has a business requirement. Goal: translate it into a correct, scoped, maintainable formula.

1. Clarify the requirement: what exact condition makes a record invalid?
2. Identify scope: all record types? all users? or a subset?
3. Write the formula: start with the condition that makes it invalid (validation fires when formula = TRUE)
4. Add scope guards: Record Type, bypass custom permission, picklist null guard
5. Write the error message: who, what, how to fix — full sentence
6. Test: happy path (valid record → no error), failure path (invalid record → correct error), edge cases (blank fields, wrong record type)

### Mode 2: Review Existing

User wants to find conflicts, dead rules, or performance issues.

1. Export all validation rules for the object
2. Identify: rules that fire on all record types but should be scoped
3. Identify: rules with no bypass mechanism (block data migrations)
4. Identify: rules that use PRIORVALUE on insert (formula error at runtime)
5. Identify: conflicting rules (two rules that enforce opposite things)
6. Identify: inactive rules that should be retired or documented so they don't confuse future admins
7. Report: active rule count, issues found, recommended changes

### Mode 3: Troubleshoot

Rule fires unexpectedly, integration is failing, or rule isn't firing when it should.

**Rule fires unexpectedly:**
1. Check Record Type scope — does the rule fire on record types it shouldn't?
2. Check for PRIORVALUE — does the rule use PRIORVALUE on insert? (Returns null on insert, triggers unexpected formula results)
3. Check blank/null handling — does `NOT(ISBLANK(Field__c))` guard the formula properly?
4. Check if the API/integration is being caught — REST API respects validation rules by default

**Rule doesn't fire:**
1. Is the rule Active? (Deactivated rules are silent)
2. Is the formula evaluating to TRUE for the invalid case? Test in Developer Console formula evaluator
3. Is a bypass mechanism active? (Custom Permission, RecordType condition, Profile condition)

## Formula Best Practices

**Always guard picklist checks against blank:**
```
// BAD — fires error if Stage is blank, which is usually wrong
ISPICKVAL(StageName, "Closed Won")

// GOOD — only fires if Stage is explicitly Closed Won
AND(
  NOT(ISBLANK(StageName)),
  ISPICKVAL(StageName, "Closed Won")
)
```

**Condition structure — validation fires when formula = TRUE:**
```
// Formula returns TRUE = record is INVALID = show error
// Formula returns FALSE = record is VALID = no error

// BAD (confusing) — think of this as "is the record invalid?"
// GOOD mental model — "what condition makes this record wrong?"
AND(
  ISPICKVAL(Stage, "Closed Won"),      // Stage is Closed Won
  ISBLANK(CloseDate)                   // AND CloseDate is blank
)
// = TRUE when Stage is Closed Won AND CloseDate is empty = fire error
```

**Bypass patterns (in order of preference):**

| Bypass Method | When to Use | How |
|--------------|-------------|-----|
| Custom Permission | Preferred — granular, auditable | `NOT($Permission.Bypass_Validation_Rules)` |
| RecordType scope | Rule shouldn't apply to certain record types | `RecordType.DeveloperName = "TargetType"` |
| Profile check (not recommended) | Only if Custom Permissions not available | `$Profile.Name <> "System Administrator"` |
| User field check | Almost never — hardcodes user data | Avoid |

## Error Message Standard

Every error message must answer three questions:
1. **What went wrong?** (specific, not "Validation error")
2. **Why is it wrong?** (the business rule in plain English)
3. **How to fix it?** (what the user should do)

```
// BAD
"Validation error."

// BAD
"Close Date is required."

// GOOD
"Close Date is required when Stage is Closed Won.
Opportunities cannot be closed without a Close Date.
Enter a Close Date to save this record."
```

Error placement: Use **field-level** error messages when the error is about one specific field. Use **page-level** (top of page) only when the error spans multiple fields.


## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner activating this skill:

1. Gather context — confirm the org edition, relevant objects, and current configuration state
2. Review official sources — check the references in this skill's well-architected.md before making changes
3. Implement or advise — apply the patterns from Core Concepts and Common Patterns sections above
4. Validate — run the skill's checker script and verify against the Review Checklist below
5. Document — record any deviations from standard patterns and update the template if needed

---

## Salesforce-Specific Gotchas

- **PRIORVALUE does not work on insert**: `PRIORVALUE(Field__c)` returns null on insert. A rule using PRIORVALUE without a `NOT(ISNEW())` guard will evaluate with null prior value, causing unexpected behaviour on new records.
- **Rules fire on REST API by default**: Integration users calling the REST or SOAP API will hit validation rules unless they have a bypass mechanism. "Our Mulesoft integration is failing" is almost always a missing bypass.
- **ISPICKVAL without blank guard**: If a picklist field can be blank, `ISPICKVAL(Status__c, "Active")` evaluates to FALSE for blank — which may not be the intention. Guard explicitly.
- **Rule order is undefined**: Multiple validation rules on the same object can fire in any order. Don't write rules that depend on another rule's outcome. They're evaluated independently.
- **Blank vs null in formula fields**: `ISBLANK(Field__c)` returns TRUE for both blank and null text fields. For number/currency fields, a field with value 0 is NOT blank. `ISNULL(NumberField__c)` catches nulls but not 0. This distinction causes bugs.
- **Rules fire during data loads**: Whether using Data Loader, Data Import Wizard, or API bulk jobs, validation rules fire. Always have a bypass for data migration users.

## Proactive Triggers

Surface these WITHOUT being asked:
- **Rule uses ISPICKVAL without a blank/null guard** → Flag: will evaluate unexpectedly when the picklist field is empty. Add `NOT(ISBLANK(PicklistField__c))` guard.
- **Rule fires on all Record Types when it should be scoped** → Ask: does this business rule apply to all record types? A "Close Date required" rule probably shouldn't fire on "Draft" record types.
- **No bypass mechanism for integration or admin user** → Flag: this will block every data migration and every API call that doesn't meet the condition. Add a Custom Permission bypass before go-live.
- **Error message is a single word or generic phrase** → Rewrite it. A bad error message is a support ticket waiting to happen.
- **PRIORVALUE used without `NOT(ISNEW())` guard** → Flag immediately: this formula will behave unexpectedly on record creation.

## Output Artifacts

| When you ask for...            | You get...                                                              |
|--------------------------------|-------------------------------------------------------------------------|
| Write a rule from requirement  | Complete formula + error message text + error placement recommendation  |
| Audit validation rules         | Issue list: scope gaps, missing bypasses, formula errors                |
| Troubleshoot a rule            | Step-by-step diagnosis + likely root cause + fix                        |
| Bypass pattern                 | Custom Permission setup + formula snippet                               |

## Related Skills

- **admin/flow-for-admins**: Use when the validation logic needs queries, orchestration, or reusable automation across objects. NOT when a formula can enforce the rule cleanly.
- **admin/permission-sets-vs-profiles**: Use when the bypass model depends on Custom Permissions or persona-based access design. NOT for writing the validation formula itself.
- **security/fls-crud**: Use when you need to understand how hidden fields still affect saves or Apex enforcement. NOT for declarative rule design.
