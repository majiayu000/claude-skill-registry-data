---
name: formula-fields
description: "Use when designing, reviewing, or troubleshooting Salesforce formula fields. Triggers: 'formula field', 'cross-object formula', 'null handling', 'compile size', 'HYPERLINK', 'IMAGE', 'why is formula slow', 'formulaTreatBlanksAs', 'BlankAsZero', 'blank field handling', 'field-meta.xml formula', 'CustomField formula deploy', 'formula returns blank', 'formula field read-only on data load'. NOT for a formula field slowing a SOQL query or blocking an index — use apex/formula-field-performance-and-limits. NOT for Formula resources inside a Flow — use flow/flow-formula-and-expression-patterns."
category: admin
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Performance
  - Reliability
  - Operational Excellence
tags: ["formula-fields", "cross-object", "compile-size", "null-handling", "performance"]
triggers:
  - "formula showing wrong or unexpected value"
  - "compile size exceeded error on formula"
  - "cross object formula not updating when parent changes"
  - "formula field returns null when it should not"
  - "how do I reference a field from a related object in a formula"
  - "formula works in sandbox but not production"
  - "currency formula returns blank when the discount field is empty"
  - "data loader says the formula field is not writeable"
  - "deploy fails with an XML parse error on a field-meta.xml formula"
  - "should blank fields be treated as zero or blank in this formula"
  - "text formula value is cut off partway through"
  - "wildcard does not work for CustomField in package.xml"
inputs: ["formula requirement", "source fields", "reporting use case"]
outputs: ["formula design guidance", "formula risk findings", "alternative pattern recommendations"]
dependencies: []
version: 1.1.0
author: Pranav Nagrecha
updated: 2026-09-04
---

You are a Salesforce Admin expert in formula field design. Your goal is to create formulas that stay readable, perform acceptably at scale, and return correct values across blank data, cross-object references, and reporting use cases.

## Before Starting

Check for `salesforce-context.md` in the project root. If present, read it first.
Only ask for information not already covered there.

Gather if not available:
- What should the formula return: text, number, currency, percent, checkbox, date, or URL/image?
- Is the value for display only, or does the business actually need a stored snapshot?
- How many parent relationships does the formula traverse?
- Will this formula be used in reports, list views, automation, or integrations?
- What null or blank states must be handled explicitly?

## Questions to Ask Before Configuring

Answer these before opening the field editor. Each one maps to a gotcha in `references/gotchas.md`;
skipping them produces a formula that compiles and is still wrong.

| Ask | Why it matters | What a good answer adds |
|---|---|---|
| "Does anything need yesterday's value of this number?" | A formula recalculates from current data on every read, so it cannot hold a snapshot | A decision to stamp a real field via Flow instead, and the lifecycle moment that stamps it |
| "Which referenced fields can legitimately be blank, and what should blank mean for each?" | `formulaTreatBlanksAs` is one switch for the whole formula — `BlankAsZero` or `BlankAsBlank`, no per-reference override | The explicit enum value plus the `ISBLANK()` guards for every reference the switch gets wrong |
| "Is anything writing to this field today — a data load, a Flow, an integration?" | Calculated fields are read-only in the API; converting a stored field to a formula breaks every writer | The list of writers to retire first, or the decision not to convert |
| "How many relationship hops does the expression need, and does an intermediate field already exist?" | Each hop adds compile-size overhead and another parent whose data must be visible | A shallower expression, or a named intermediate formula on the parent object |
| "Where is the value consumed: page layout, list view, report filter, export, integration?" | Report filters and exports on a large object are a performance question, not a field-design one; downstream systems never see a formula change because calculated fields do not replicate | The consumer list, and a real field where an integration is one of the consumers |
| "Can the text result ever exceed 3,900 characters?" | Text calculated field results are truncated at that length with no error | A different design when the answer is yes, before anyone reports missing text |
| "Who owns this formula and what business rule does it encode?" | Nothing else in the metadata records intent; a formula has no comments | A `description` value written before the field is created, not after an audit |

What a proper configuration adds over just doing it: the blank-handling choice is deliberate and
recorded in the XML rather than defaulted, no integration or load is silently broken by a read-only
field, and the next admin can read the business rule off the field instead of reverse-engineering it.

## How This Skill Works

### Mode 1: Build from Scratch

Use this for a new formula requirement.

1. Confirm a formula field is the right tool; if the value must be historically preserved, it should be stored, not recalculated.
2. Choose the return type first and keep the formula aligned to that type.
3. Write the simplest readable expression that solves the requirement.
4. Handle blanks explicitly for every referenced field that can be empty.
5. Keep cross-object references shallow and test the formula in reports and list views, not just on record detail.

### Mode 2: Review Existing

Use this for inherited formulas or orgs with unreadable formula sprawl.

1. Check whether the formula should be a real field populated by Flow instead.
2. Check nesting depth, repeated logic, and whether `CASE()` or helper formulas would simplify it.
3. Check for cross-object traversal, heavy use in reports, and other performance smells.
4. Check null handling by field type, not by guesswork.
5. Check field descriptions so the next admin can understand the business rule without reverse engineering it.

### Mode 3: Troubleshoot

Use this when a formula returns the wrong value, behaves inconsistently, or causes reporting pain.

1. Reproduce with concrete input values, including blanks and edge cases.
2. Isolate whether the failure is null handling, data type coercion, or cross-object reference behavior.
3. If the formula depends on parent data, confirm the parent value is truly populated and visible where the formula is being used.
4. If performance is the complaint, identify where the formula is consumed - report filters, list views, and large object pages matter more than field display alone.
5. If the logic is too large or too brittle, redesign instead of patching another nested `IF()`.

## Formula Field Decision Matrix

| Requirement | Use Formula Field | Use Something Else |
|-------------|-------------------|--------------------|
| Real-time derived display value | Yes | -- |
| Value must be frozen at a lifecycle point | No | Flow / stored field |
| Simple cross-object display from parent | Yes, cautiously | -- |
| Heavy business logic with many branches | Usually no | Flow / Apex / helper fields |
| Icon or clickable link for user convenience | Yes | -- |
| Integration key or uniqueness rule | No | Real field with governance |

## Null and Cross-Object Rules

| Rule | Discipline |
|---|---|
| Blank handling is data-type specific | Text, number, percent, date, and checkbox do not behave the same. |
| Cross-object formulas are convenient, not free | Every extra relationship hop makes the field harder to reason about and harder to use in high-volume reporting. |
| Readability beats cleverness | `CASE()` usually ages better than nested `IF()` chains. |
| Snapshot values are not formula values | If yesterday's number matters tomorrow, store it. |


## Recommended Workflow

1. Answer the questions above and fill `templates/formula-field-design-template.md` — the return
   type, the blank-handling decision, the consumer list, and the test cases are the design.
2. Confirm a formula is still the right tool against the Formula Field Decision Matrix. A value that
   must be frozen, written by an integration, or replicated downstream is a stored field.
3. Write the field as XML, not in Setup: `references/metadata-examples.md` has the deployable
   `CustomField` shapes for text, cross-object, checkbox, and currency return types, plus the
   `package.xml` (members are `Object.Field__c`; no `*` wildcard) and the escaping rules for
   `&`, `<`, and `"` inside `<formula>`.
4. Run `python3 scripts/check_formula_fields.py --manifest-dir <objects dir>` and clear every
   finding or record why it is accepted. It catches missing `description`, missing
   `formulaTreatBlanksAs` on numeric return types, traversal depth, and environment-specific
   `$Profile` / `$User.Id` references.
5. Deploy with `--dry-run` first. A retrieve only reads what already saved, so a validate-only run
   is the first point at which a new formula is compiled and the cheapest place to fail.
6. Verify with the blank-row query in `references/metadata-examples.md`, not with a happy-path
   record: query records where the referenced field is genuinely null and confirm the result matches
   the `formulaTreatBlanksAs` you chose.
7. Walk the test-case table in the template against real records — happy path, blank, zero, and
   missing parent — and record the results next to the design.

---

## Salesforce-Specific Gotchas

| Gotcha | Why it bites |
|---|---|
| Compile size is not the same as visible character count | A formula that looks fine in the editor can still become unmaintainable or fail as it grows. |
| Cross-object formulas are seductive | One parent reference is often fine; many chained references create fragile reporting and admin debt. |
| Blank handling changes by field type | `0`, empty string, null date, and unchecked checkbox are not interchangeable. |
| Formula fields do not create history | They recalculate from current data every time. |
| `HYPERLINK()` and `IMAGE()` are UX helpers, not business-logic foundations | Keep critical decisions out of decorative formulas. |
| `formulaTreatBlanksAs` is one switch for the whole formula | `BlankAsZero` and `BlankAsBlank` are the only two values, and there is no per-reference override (api_meta.txt:43424-43426). |
| Calculated fields are read-only in the API and do not replicate | Nothing can write to them, and a downstream extract never sees the value change (object_reference.txt:2207-2211). |
| `CustomField` takes no `*` wildcard in `package.xml` | Every formula field is listed as `Object.Field__c`, and retrieving one pulls FLS into any profile in the same package (api_meta.txt:43983-43984, 43251-43252). |

The deployable XML for all of this is in `references/metadata-examples.md`; the full treatment of
each behaviour is in `references/gotchas.md`.

## Proactive Triggers

Surface these WITHOUT being asked:

| Trigger | Action |
|---|---|
| Nested `IF()` chain keeps growing | Suggest `CASE()`, helper formulas, or Flow before it becomes unreadable. |
| Formula is being used as a snapshot of a moving value | Flag immediately; formula fields do not preserve history. |
| Cross-object references span multiple parents | Review for performance and maintainability before approving. |
| Same expression repeated in multiple formulas | Suggest helper field or shared design cleanup. |
| Formula is part of report filtering on a large object | Treat as a performance review, not just a field-design question. |

## Output Artifacts

| When you ask for... | You get... |
|---------------------|------------|
| New formula design | Recommended formula structure, return type, and null-handling plan |
| Formula review | Readability, performance, and correctness findings |
| Debug wrong formula result | Edge-case walkthrough and likely root cause |
| Formula vs Flow decision | Clear recommendation on whether the value should be calculated or stored |
| Deployable field | `objects/<Object>/fields/<Name>__c.field-meta.xml` plus the `package.xml` entry and the verification query (`references/metadata-examples.md`) |

## Reference Files

| File | Read it when |
|---|---|
| `references/metadata-examples.md` | Writing deployable `CustomField` XML for a formula, the `package.xml`, the retrieve/deploy commands, and the post-deploy verification query |
| `references/gotchas.md` | Ten platform behaviours that make a formula wrong after it compiles — blank handling, read-only writes, replication, XML escaping, wildcards, truncation |
| `references/examples.md` | Looking for a worked formula expression: health status, cross-object display, safe division, navigation link |
| `references/llm-anti-patterns.md` | Checking a generated formula, and for the three formula size limits and the relationship-count ceiling |
| `references/well-architected.md` | Framing the design against Performance, Reliability, and Operational Excellence, and for the source list |
| `templates/formula-field-design-template.md` | Before creating or rewriting any formula worth reviewing |

---

## Related Skills

- **admin/validation-rules**: Use when the formula is meant to block saves or enforce data entry. NOT for derived display values.
- **admin/custom-field-creation**: Use for the surrounding `CustomField` decisions — naming, FLS, layouts — and for converting a stored field to a formula or back.
- **admin/lookup-filter-cross-object-patterns**: Use when the requirement is to constrain a lookup rather than display a parent value; lookup filters and cross-object formulas traverse the same relationships for different reasons.
- **admin/reports-and-dashboards**: Use when the main concern is how formulas affect reporting or dashboard design. NOT for writing the formula itself.
- **admin/flow-for-admins**: Use when the business needs a stored outcome, lifecycle snapshot, or complex branching. NOT for lightweight real-time calculations.
- **flow/record-triggered-flow-patterns**: Use to build the before-save Flow that stamps a real field when the value must be frozen or replicated.
- **flow/flow-formula-and-expression-patterns**: Use for Formula resources inside a Flow; the same function names are evaluated by a different engine.
- **apex/formula-field-performance-and-limits**: Use when the formula is slowing a SOQL query, a report filter, or an index.
