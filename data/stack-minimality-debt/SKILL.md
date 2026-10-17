---
name: stack-minimality-debt
description: Collect deliberate stack-minimality shortcuts into a debt ledger with explicit ceilings and revisit triggers.
license: MIT
---
# Stack Minimality Debt

## Purpose
Track intentional simplifications that trade future flexibility or scale for present simplicity. The ledger prevents known ceilings from disappearing into tribal knowledge.

## Activate when
Use after minimality-driven implementation work or when asked to list deliberate shortcuts, deferred architecture, or known ceilings.

## Repository inspection
Search Ruby/Rails comments, TypeScript/React comments, SQL comments, ADRs, and documentation for stack-minimality markers. Exclude generated and vendored output.

## Decision rules
A valid marker states:
- what was simplified;
- the known ceiling;
- the event, measurement, or condition that should trigger reconsideration.

Examples:
- # stack-minimality: per-process cache; revisit when memory pressure or hit-rate evidence justifies shared caching
- // stack-minimality: feature-local state; revisit when another independent feature needs the same owner
- -- stack-minimality: sequential backfill; revisit when the deployment window no longer fits

## Implementation procedure
1. Scan all supported source/comment forms.
2. Record each marker with file and line.
3. Report its ceiling and trigger.
4. Flag markers with no concrete trigger as no-trigger.
5. Report counts.
6. Do not modify source files.

## Anti-patterns / failure modes
- Using markers to excuse missing security or data-integrity controls.
- Writing "revisit later" without a trigger.
- Keeping markers after the underlying shortcut has been removed.
- Marking every ordinary design decision as debt.

## Reference example

A marker states what was simplified, its ceiling, and the trigger to revisit it. `bin/stack-minimality debt` reports every marker (repository path shown as `/path/to/app`):

```ruby
# stack-minimality: summed in Ruby over loaded line items; revisit when orders exceed ~500 line items or the total is needed in SQL reports
def total_cents
  line_items.sum(&:amount_cents)
end
```

```json
{
  "schema_version": 1,
  "repository": "/path/to/app",
  "markers": [
    {
      "file": "app/models/order.rb",
      "line": 4,
      "text": "summed in Ruby over loaded line items; revisit when orders exceed ~500 line items or the total is needed in SQL reports",
      "no_trigger": false
    }
  ],
  "marker_count": 1,
  "no_trigger_count": 0
}
```

A marker whose text has no concrete trigger is reported with `"no_trigger": true` and counted in `no_trigger_count`.

## Agent review checklist
- [ ] Ruby, Rails, TypeScript, React, and SQL markers searched.
- [ ] Generated/vendor output excluded.
- [ ] Ceiling and trigger captured.
- [ ] No-trigger entries highlighted.
- [ ] No source modifications made.

## Verification
Compare the ledger with repository search results. A marker without a trigger is incomplete debt documentation.

## Source foundation
- https://ponytail.dev/
- https://github.com/DietrichGebert/ponytail
- Repository ADR and documentation conventions
