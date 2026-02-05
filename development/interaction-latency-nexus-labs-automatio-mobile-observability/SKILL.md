---
name: interaction-latency
description: Measure time from user tap to action completion. Use when tracking button response times, form submissions, add-to-cart, or any tap-triggered operation.
triggers:
  - "add to cart is slow"
  - "button feels slow"
  - "form submission timing"
  - "measure interaction latency"
  - "tap response time"
  - "track button performance"
priority: 2
---

# Interaction Latency

Time from user tap to action successfully completed.

## When to Use

- "Add to cart" button tapped → cart updated
- "Submit" button tapped → form processed
- "Like" button tapped → state changed
- Any tap that triggers async work

## Measurement Pattern

```
TAP → START_SPAN → [async work] → END_SPAN
```

1. Capture tap timestamp
2. Start span with operation name
3. End span when action confirms success
4. Include success/failure outcome

## Key Thresholds

| Rating | Duration |
|--------|----------|
| Good | <300ms |
| Acceptable | <1s |
| Poor | >1s |

## Implementation

See `references/ui-performance.md` (Entry Point Latency section) for platform-specific code.

## Common Mistakes

- Ending span on API call start (not completion)
- Not tracking failure cases
- Missing the tap timestamp (starting late)

## Related Skills

- See `skills/navigation-latency` for screen-to-screen transitions (vs single-tap actions)
- Combine with `skills/user-journey-tracking` for friction detection on key interactions
