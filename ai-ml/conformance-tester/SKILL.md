---
name: conformance-tester
description: Use this skill to test whether value-investing reports follow required workflow, schema, output, data, and execution-gate rules. Trigger after skill changes, model changes, report inconsistency, token optimization, or new valuation-module additions.
---

# Conformance Tester Skill

## Purpose

Test whether different AI models or runs follow the same Skill workflow and output requirements.

## When to Use

Use when:

- A new AI model is used
- A new Skill version is released
- A report seems inconsistent
- Token optimization changes are made
- A new valuation module is added

## Tests

1. Schema compliance
2. Required sections present
3. Required gates present
4. Selected model executed or blocked
5. Data provenance table present
6. Data freshness table present
7. No orphan numbers
8. Token budget respected
9. Final rating blocked if critical gate failed
10. Investor action blocked if valuation range missing

## Output

```markdown
## Conformance Test Result

| Test | Status | Severity | Note |
|---|---|---|---|
| Schema | Pass/Fail |  |  |
| Data Provenance | Pass/Fail |  |  |
| Reverse DCF Gate | Pass/Fail |  |  |
```
