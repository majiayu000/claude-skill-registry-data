---
name: validate-journey
description: Validates CDP journey YAML configurations against tdx schema requirements. Use when reviewing journey structure, checking step types and parameters, verifying segment references, or troubleshooting journey configuration errors before pushing to Treasure Data.
---

# Journey YAML Validation

```bash
tdx journey validate                      # Validate all journey YAML files locally
tdx journey validate path/to/journey.yml  # Validate specific file
tdx journey push --dry-run                # Preview changes before push
```

## Required Structure

```yaml
type: journey              # Required
name: Journey Name

reentry: no_reentry        # no_reentry | reentry_unless_goal_achieved | reentry_always

journeys:
  - state: draft           # draft | launched
    latest: true           # Exactly one must be true
    stages:
      - name: Stage Name
        steps: [...]
```

**Limits**: Max 8 stages, 120 events/journey, 70 events/stage, 30 versions

## Step Types Quick Reference

| Type | Required `with` | Notes |
|------|-----------------|-------|
| `wait` | `duration` + `unit` OR `condition` | condition has `segment`, optional `next`, `timeout` |
| `activation` | `activation` | key from activations section |
| `decision_point` | `branches[]` | each needs segment, next |
| `ab_test` | `variants[]` | percentages must sum to 100 |
| `merge` | (none) | |
| `jump` | `target` with `journey`, `stage` | target is an object |
| `end` | (none) | no `next` or `with` |

**Important**: `next:` is a direct field on step, not inside `with:`

## Wait Condition Format

```yaml
# Wait for segment match with different paths for matched vs timeout
- type: wait
  name: Wait for Purchase
  with:
    condition:
      segment: made-purchase    # Wait until segment match
      next: follow-up           # Optional: defaults to next sequential step
      timeout:                  # Max wait duration
        duration: 14
        unit: day
        next: timeout-path      # Required when using different paths
```

## Segment References

- Embedded: `segment: my-segment` (defined in `segments:` section)
- External: `segment: ref:Existing Segment` (use `ref:` prefix)

## Related Skills

- **journey** - Full journey creation and management
