---
name: formula-fields
description: "Use when designing, reviewing, or troubleshooting Salesforce formula fields. Triggers: 'formula field', 'cross-object formula', 'null handling', 'compile size', 'HYPERLINK', 'IMAGE', 'why is formula slow'. NOT for save-time validation or persisted values - use validation rules, Flow, or real fields for that."
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
inputs: ["formula requirement", "source fields", "reporting use case"]
outputs: ["formula design guidance", "formula risk findings", "alternative pattern recommendations"]
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-03-13
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

- **Blank handling is data-type specific**: text, number, percent, date, and checkbox do not behave the same.
- **Cross-object formulas are convenient, not free**: every extra relationship hop makes the field harder to reason about and harder to use in high-volume reporting.
- **Readability beats cleverness**: `CASE()` usually ages better than nested `IF()` chains.
- **Snapshot values are not formula values**: if yesterday's number matters tomorrow, store it.


## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner activating this skill:

1. Gather context — confirm the org edition, relevant objects, and current configuration state
2. Review official sources — check the references in this skill's well-architected.md before making changes
3. Implement or advise — apply the patterns from Core Concepts and Common Patterns sections above
4. Validate — run the skill's checker script and verify against the Review Checklist below
5. Document — record any deviations from standard patterns and update the template if needed

---

## Salesforce-Specific Gotchas

- **Compile size is not the same as visible character count**: a formula that looks fine in the editor can still become unmaintainable or fail as it grows.
- **Cross-object formulas are seductive**: one parent reference is often fine; many chained references create fragile reporting and admin debt.
- **Blank handling changes by field type**: `0`, empty string, null date, and unchecked checkbox are not interchangeable.
- **Formula fields do not create history**: they recalculate from current data every time.
- **`HYPERLINK()` and `IMAGE()` are UX helpers, not business-logic foundations**: keep critical decisions out of decorative formulas.

## Proactive Triggers

Surface these WITHOUT being asked:
- **Nested `IF()` chain keeps growing** -> Suggest `CASE()`, helper formulas, or Flow before it becomes unreadable.
- **Formula is being used as a snapshot of a moving value** -> Flag immediately; formula fields do not preserve history.
- **Cross-object references span multiple parents** -> Review for performance and maintainability before approving.
- **Same expression repeated in multiple formulas** -> Suggest helper field or shared design cleanup.
- **Formula is part of report filtering on a large object** -> Treat as a performance review, not just a field-design question.

## Output Artifacts

| When you ask for... | You get... |
|---------------------|------------|
| New formula design | Recommended formula structure, return type, and null-handling plan |
| Formula review | Readability, performance, and correctness findings |
| Debug wrong formula result | Edge-case walkthrough and likely root cause |
| Formula vs Flow decision | Clear recommendation on whether the value should be calculated or stored |

## Related Skills

- **admin/validation-rules**: Use when the formula is meant to block saves or enforce data entry. NOT for derived display values.
- **admin/reports-and-dashboards**: Use when the main concern is how formulas affect reporting or dashboard design. NOT for writing the formula itself.
- **admin/flow-for-admins**: Use when the business needs a stored outcome, lifecycle snapshot, or complex branching. NOT for lightweight real-time calculations.
