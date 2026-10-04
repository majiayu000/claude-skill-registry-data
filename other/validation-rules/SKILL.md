---
name: validation-rules
description: "Use when writing, auditing, or troubleshooting Salesforce Validation Rules. Triggers: 'validation rule', 'required field formula', 'rule fires unexpectedly', 'integration failing validation', 'data quality', 'errorConditionFormula', 'errorDisplayField', 'errorMessage 255 characters', 'ValidationRule metadata', 'validationRule-meta.xml', 'deploy validation rule inactive', 'bypass custom permission', 'FIELD_CUSTOM_VALIDATION_EXCEPTION', 'validation rule on custom metadata type', 'compound field validation rule', 'require at least one child record before a stage', 'HasOpportunityLineItem'. NOT for Flow-based validation — use admin/flow-for-admins for that."
category: admin
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Reliability
  - Operational Excellence
tags: ["validation-rules", "data-quality", "bypass", "formulas", "integrations"]
triggers:
  - "validation rule is blocking an API integration"
  - "validation rule blocks data loader import"
  - "rule is firing when it should not"
  - "how do I bypass a validation rule for admins"
  - "validation rule not triggering on insert"
  - "validation rule is too strict for data migration"
  - "user checkbox bypass instead of custom permission"
  - "hardcoded user id in validation rule"
  - "how do I write a validation rule with multiple conditions"
  - "write the validation rule XML so I can deploy it"
  - "deploy a validation rule but leave it inactive"
  - "validation rule error message shows at top of page instead of next to the field"
  - "records exist that violate an active validation rule"
  - "validation rule wont fire when the opportunity line item changes the amount"
  - "wildcard in package.xml is not retrieving my validation rules"
  - "error message is too long to save the validation rule"
  - "write an apex test that proves the validation rule fires"
  - "cant write a validation rule on the billing address"
  - "check whether a validation rule formula references a field that does not exist"
  - "require at least one opportunity product before the stage can advance"
  - "validation rule to check the opportunity has products"
inputs: ["business rule", "exception path", "integration constraints", "object and field API names", "record types in scope", "which users or integrations must bypass"]
outputs: ["validation design guidance", "rule review findings", "bypass recommendations", "deployable ValidationRule XML plus package.xml", "Apex tests that assert the rule fires and that the bypass suppresses it"]
dependencies: []
version: 1.2.1
author: Pranav Nagrecha
updated: 2026-09-19
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

## Questions to Ask Before Configuring

Ask these before writing a formula. Each one traces to a behaviour in `references/gotchas.md` that no amount of formula care recovers from once the rule ships.

| Ask | Why it matters | What a good answer adds |
|---|---|---|
| "Which field does the user actually edit to cause this — the one on the record, or a child record?" | Validation rules don't fire on an Opportunity when an opportunity product changes it, so a rule guarding `Amount` never runs in a line-item-driven process | The right object for the rule, or a decision to use a record-triggered flow on the child instead |
| "Is any workflow field update or automation writing this field after save?" | Custom validation rules are not re-run after a workflow field update re-saves the record, so the rule is not a database invariant | Either a migration of that field update to a before-save flow, or an explicit acceptance that violating records will exist |
| "Which users and integrations must be able to save a record the rule would reject?" | Every rule with no bypass blocks every data load and every API write that doesn't meet the condition | The Custom Permission name and the Permission Set that carries it, per `templates/admin/validation-rule-patterns.md` |
| "Is the field the error should attach to on every layout for every record type in scope?" | `errorDisplayField` silently changes to Top of Page when the field isn't visible on the layout | Either a confirmed layout, or an error message written to read correctly at the top of the page |
| "Does the message fit in 255 characters and name both the problem and the fix?" | `errorMessage` is capped at 255 characters; a rule that can't say what to do generates a support ticket per occurrence | The final message text, not a placeholder to be filled in at deploy time |
| "Does the data already violate this rule today?" | Validation rules fire on update as well as insert, so an active rule on dirty data blocks every edit of every violating record except the one that happens to satisfy the rule | A decision to deploy with `active=false` and a named cleanup owner, or a count proving the data is clean |
| "Does the formula touch an address, a person name, or a dependent picklist?" | Validation rules can't use compound fields as of API version 20.0 | A rewrite against the component fields (`BillingStreet`, `BillingCity`, `FirstName`, `LastName`) before anyone starts typing |
| "When the rule says 'this deal has products', which stages are gated, and may a deal be *created* already at one of them?" | `HasOpportunityLineItem` is false on every Opportunity insert — a line item is inserted *for* an Opportunity that already exists — so an `ISNEW()` fire condition forbids creation at that stage instead of gating it, and `NOT(ISNEW())` lets a record inserted straight at Propose through until its next stage change | The stage list, whether `Closed Lost` is in it, and an explicit yes/no on direct creation at a gated stage — see Gotcha 15 in `references/gotchas.md` |
| "Does the formula call `ISBLANK(` or `ISNULL(` directly on a picklist field?" | The org rejects it at deploy time — `ISBLANK`/`ISNULL` don't accept a picklist argument directly; only `TEXT(<picklist>)` does. Proven live via `sf project deploy start --dry-run` (API 67.0, 2026-09-12): "Field StageName is a picklist field. Picklist fields are only supported in certain functions." | `NOT(ISBLANK(TEXT(Field__c)))` instead of `NOT(ISBLANK(Field__c))` — see Gotcha 14 in `references/gotchas.md` |

What a proper configuration adds over just writing the formula: the rule is scoped to the object where the edit actually happens, carries a bypass that data loads and integrations can use without anyone deactivating anything in production, attaches its error to a field that exists on the layout, and ships inactive when the existing data can't yet satisfy it.

---

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
1. Is the rule Active? (Deactivated rules are silent, and a rule shipped with `active=false` looks identical in source control to one shipped active)
2. Turn on a debug log with the **Validation** category and reproduce the save. That category records the rule name and whether the rule evaluated true or false — it answers "did my rule run and what did it decide" directly, which no amount of reading the formula does
3. Is a bypass mechanism active? (Custom Permission, RecordType condition, Profile condition)
4. Did the edit land on this object at all? An Opportunity rule does not fire when an opportunity product changes the Opportunity — see `references/gotchas.md`
5. Did a workflow field update write the offending value *after* validation ran? Validation rules are not re-run when a workflow field update re-saves the record

## Formula Best Practices

**Always guard picklist checks against blank:**
```
// BAD — fires error if Stage is blank, which is usually wrong
ISPICKVAL(StageName, "Closed Won")

// BAD — does not compile. StageName is a picklist; ISBLANK() applied
// directly to a picklist field is rejected at deploy time with
// "Field StageName is a picklist field. Picklist fields are only
// supported in certain functions." See Gotcha 14 in references/gotchas.md.
AND(
  NOT(ISBLANK(StageName)),
  ISPICKVAL(StageName, "Closed Won")
)

// GOOD — TEXT() converts the picklist to a string first, which ISBLANK()
// accepts; only fires if Stage is explicitly Closed Won
AND(
  NOT(ISBLANK(TEXT(StageName))),
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


## The Deployable Surface

A validation rule is a `ValidationRule` component, available in **API version 12.0 and later**. In metadata format it is a `<validationRules>` element inside the object's `.object` file; in DX source format it is its own `.validationRule-meta.xml` file. Same six elements either way:

| Element | Required | The part that surprises people |
|---|---|---|
| `fullName` | yes | Must start with a letter, can't end with `_`, can't contain two consecutive underscores |
| `active` | yes | `false` deploys a real but dormant rule — the correct way to land a rule ahead of a data cleanup |
| `description` | no | The only place the business justification survives a sandbox refresh |
| `errorConditionFormula` | yes | Fires when it returns **true**. `<` and `&` must be XML-escaped |
| `errorDisplayField` | no | Changes automatically to Top of Page if omitted **or if the field isn't visible on the page layout** |
| `errorMessage` | yes | Hard cap of **255 characters** |

Two version gates that change what you can write: as of **API 20.0** rules can't use compound fields (addresses, first and last names, dependent picklists, dependent lookups); as of **API 40.0** rules are supported on custom metadata types.

`ValidationRule` **doesn't support the `*` wildcard in package.xml** — name each rule `Object.RuleName`, or retrieve the enclosing `CustomObject`. Full XML, manifests, `sf` commands, the Tooling API verification query and both Apex tests are in `references/metadata-examples.md`.


## Recommended Workflow

1. **Locate the edit.** Confirm which object the user's change actually lands on, and whether a workflow field update or a before-save flow writes the same field afterwards. `references/gotchas.md` covers both cases where the rule you are about to write will not run.
2. **Retrieve what exists.** `sf project retrieve start --metadata "CustomObject:<Object>"` — never a `*` wildcard on `ValidationRule`, which the type does not support. Read the existing `<validationRules>` elements for a rule that already covers this, and for a rule that contradicts it.
3. **Compose the formula in the canonical order** — bypass, then relevance gate, then business condition — from `templates/admin/validation-rule-patterns.md`. The formula describes the **invalid** state; it fires when it evaluates to TRUE.
4. **Write the XML** from `references/metadata-examples.md`: `active`, `description` (business justification and bypass name), `errorConditionFormula`, `errorDisplayField`, `errorMessage` under 255 characters. Set `active=false` if existing data would violate the rule.
5. **Lint it.** `python3 scripts/check_validation_rules.py --manifest-dir force-app/main/default/objects` — it exits 1 on CRITICAL/HIGH findings (empty or over-long error messages, a `description` over 255 characters — `VR-DESC-01`; `description` and `errorMessage` are capped at 255 **independently**, and the org rejects the deploy with "Validation rule description cannot be longer than 255 characters long." (org-verified 2026-09-19) — `$Profile.Name` gating, duplicate `fullName`, unguarded `PRIORVALUE`, `ISBLANK`/`ISNULL` applied directly to a picklist field — VR-PICK-01) and reports MEDIUM/LOW/REVIEW advisories (picklist blank guards, missing `$Permission` bypass) and INFO advisories (`VR-OPP-01` — an Opportunity rule counting line items by hand where `HasOpportunityLineItem` would do) without failing; add `--strict` to fail on any finding. A `--manifest-dir` that does not exist is an ERROR (exit 1, not promotable); one that exists but carries no validation-rule metadata is a REVIEW advisory (exit 0; `--strict` promotes it to exit 1) rather than a hard failure — an object with no rules yet is not a defect. When the same scan also carries `objects/<Object>/fields/*.field-meta.xml` and `customPermissions/*.customPermission-meta.xml`, it additionally resolves `__c` field tokens, `errorDisplayField`, and `$Permission` names against that inventory (VR-REF-01/VR-REF-02, both HIGH). Run it over the whole build/package tree — not one step's directory — or every reference comes back as an advisory INFO instead of a real answer; standard fields are never flagged either way.
6. **Write both tests** from `references/metadata-examples.md`: one that asserts the rule fires and attaches to the right field via `Database.Error.getFields()`, and one under `System.runAs` that asserts the bypass permission suppresses it. Without the second, nothing catches the removal of the bypass clause.
7. **Validate-only, then deploy, then verify.** `sf project deploy validate` proves the formula compiles; the Tooling API query in `references/metadata-examples.md` proves the rules landed with the intended `Active` state. Record the rule in `templates/validation-rule-template.md` so the next admin knows why it exists.

---

## Salesforce-Specific Gotchas

| Gotcha | Detail |
|---|---|
| PRIORVALUE does not work on insert | `PRIORVALUE(Field__c)` returns null on insert. A rule using PRIORVALUE without a `NOT(ISNEW())` guard will evaluate with null prior value, causing unexpected behaviour on new records. |
| Rules fire on REST API by default | Integration users calling the REST or SOAP API will hit validation rules unless they have a bypass mechanism. "Our Mulesoft integration is failing" is almost always a missing bypass. |
| ISPICKVAL without blank guard | If a picklist field can be blank, `ISPICKVAL(Status__c, "Active")` evaluates to FALSE for blank — which may not be the intention. Guard explicitly. |
| ISBLANK/ISNULL applied directly to a picklist does not compile | `NOT(ISBLANK(StageName))` is rejected at deploy time — wrap the picklist in `TEXT()` first: `NOT(ISBLANK(TEXT(StageName)))`. See Gotcha 14 in `references/gotchas.md`. |
| Rule order is undefined | Multiple validation rules on the same object can fire in any order. Don't write rules that depend on another rule's outcome. They're evaluated independently. |
| Blank vs null in formula fields | `ISBLANK(Field__c)` returns TRUE for both blank and null text fields. For number/currency fields, a field with value 0 is NOT blank. `ISNULL(NumberField__c)` catches nulls but not 0. This distinction causes bugs. |
| Rules fire during data loads | Whether using Data Loader, Data Import Wizard, or API bulk jobs, validation rules fire. Always have a bypass for data migration users. |
| A child-record count you are about to build may already be a standard field | Opportunity carries `HasOpportunityLineItem`, a platform-set read-only boolean — "has products" needs no roll-up, formula field or trigger. It is false on every insert, which changes how the rule must be guarded. See Gotcha 15 in `references/gotchas.md` and the worked example in `references/examples.md`. |
| Step-scope lint cannot resolve field tokens — declare the checker at build scope | `check_validation_rules.py`'s VR-REF-01/VR-REF-02 checks need `objects/<Object>/fields/*.field-meta.xml` and `customPermissions/*.customPermission-meta.xml` in the same scan to resolve `__c` field tokens, `errorDisplayField`, and `$Permission` names. Point it at one build step's directory (where the rule lives but the field/permission it depends on doesn't) and every reference comes back as an advisory INFO, not a pass — declare the checker's acceptance test at build/package scope, not step scope. |

## Proactive Triggers

Surface these WITHOUT being asked:

| Trigger | Action |
|---|---|
| Rule uses ISPICKVAL without a blank/null guard | Flag: will evaluate unexpectedly when the picklist field is empty. Add `NOT(ISBLANK(TEXT(PicklistField__c)))` guard — `ISBLANK()` on a picklist without `TEXT()` does not compile. |
| Rule applies `ISBLANK(`/`ISNULL(` directly to a field also passed to `ISPICKVAL(` in the same formula | Flag immediately: this is a picklist and the deploy will be rejected. Wrap it in `TEXT()`. |
| Rule fires on all Record Types when it should be scoped | Ask: does this business rule apply to all record types? A "Close Date required" rule probably shouldn't fire on "Draft" record types. |
| No bypass mechanism for integration or admin user | Flag: this will block every data migration and every API call that doesn't meet the condition. Add a Custom Permission bypass before go-live. |
| Error message is a single word or generic phrase | Rewrite it. A bad error message is a support ticket waiting to happen. |
| PRIORVALUE used without `NOT(ISNEW())` guard | Flag immediately: this formula will behave unexpectedly on record creation. |
| Requirement is "record must have at least one child before stage X" | Check the parent's standard fields before proposing a roll-up, formula field or trigger. On Opportunity the answer is `NOT(HasOpportunityLineItem)`; flag the guards it needs (`NOT(ISNEW())` + `ISCHANGED`) in the same breath. |

## Output Artifacts

| When you ask for...            | You get...                                                              |
|--------------------------------|-------------------------------------------------------------------------|
| Write a rule from requirement  | Complete formula + error message text + error placement recommendation  |
| Audit validation rules         | Issue list: scope gaps, missing bypasses, formula errors                |
| Troubleshoot a rule            | Step-by-step diagnosis + likely root cause + fix                        |
| Bypass pattern                 | Custom Permission setup + formula snippet                               |

## Reference Files

| File | Read it when |
|---|---|
| `references/metadata-examples.md` | Writing deployable `ValidationRule` XML (both metadata and DX source shapes), the package.xml, the `sf retrieve`/`deploy`/`validate` commands, the Tooling API verification query, and the two Apex tests |
| `references/gotchas.md` | Fifteen platform behaviours that make a correct-looking rule not run, not block, not compile, or not display where you put it |
| `references/examples.md` | Formula patterns by requirement shape: conditional-required, date-in-future, record-type-scoped, cross-object, bypass, and "at least one child record" via a standard platform boolean |
| `references/llm-anti-patterns.md` | Self-checking generated output — inverted formulas, missing bypass, and the rest |
| `references/well-architected.md` | Pillar mapping, governance and review cadence, and the source list behind every claim in this package |
| `templates/validation-rule-template.md` | Documenting a shipped rule: justification, scope, bypass, test scenarios, change history |
| `scripts/check_validation_rules.py` | Linting retrieved or authored rule metadata before a deploy. Run at build/package scope (not one step's directory) to get real VR-REF-01/VR-REF-02 field- and `$Permission`-reference resolution instead of an advisory INFO |

---

## Related Skills

- **admin/formula-fields**: Use for formula syntax itself — operators, functions, field-type behaviour, and which fields are addressable. NOT for rule scoping or bypass design.
- **admin/record-types-and-page-layouts**: Use when scoping a rule by record type, or when `errorDisplayField` has relocated because the field left a layout. NOT for writing the condition.
- **admin/flow-for-admins**: Use when the validation logic needs queries, orchestration, or reusable automation across objects. NOT when a formula can enforce the rule cleanly.
- **flow/record-triggered-flow-patterns**: Use when the check belongs on a child object, or when a before-save flow should repair the data at step 3 instead of a rule rejecting it at step 5. NOT for declarative field-level checks on the same record.
- **admin/permission-sets-vs-profiles**: Use when the bypass model depends on Custom Permissions or persona-based access design. NOT for writing the validation formula itself.
- **data/data-loader-and-tools**: Use when planning the load that a rule will block, and when deciding whether the bypass permission is assigned for the window or permanently. NOT for rule authoring.
- **admin/products-and-pricebooks**: Use when the rule gates on whether an Opportunity has product lines, and you need the catalog side — price books, `PricebookEntry`, why a line item can exist at all. NOT for the formula itself.
- **apex/apex-stripinaccessible-and-fls-enforcement**: Use when you need to understand how hidden or inaccessible fields still affect saves and Apex enforcement. NOT for declarative rule design.
