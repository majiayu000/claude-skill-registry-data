---
name: journey
description: Creates CDP journey definitions in YAML using `tdx journey` commands. Covers journey stages, steps (wait, activation, decision_point, ab_test, merge, jump, end), entry/exit criteria, goals, embedded segments, and versioning. Use when building customer journey orchestration workflows or managing journey YAML files.
---

# tdx Journey - CDP Journey Orchestration

## Core Commands

```bash
tdx sg pull "Customer 360"                   # Pull all segments & journeys (sets context)
tdx journey pull                             # Pull all journeys to YAML
tdx journey pull path/to/journey.yml         # Pull specific journey
tdx journey push --dry-run                   # Preview changes
tdx journey push --yes                       # Push all journeys (skip confirmation)
tdx journey push path/to/journey.yml --yes   # Push specific journey
tdx journey pause "Journey Name"             # Pause
tdx journey resume "Journey Name"            # Resume
tdx journey view "Journey Name" --include-stats
```

## File Structure

Journey files stored in parent segment folder: `./segments/(parent-segment-name)/journey-name.yml`

## Basic Structure

```yaml
type: journey                # Required
name: Onboarding Journey

reentry: no_reentry          # no_reentry | reentry_unless_goal_achieved | reentry_always

goal:
  name: Completed
  segment: completed-users

journeys:
  - state: draft             # draft | launched
    stages:
      - name: Welcome
        entry_criteria:      # Who enters this stage
          name: New Users
          segment: new-users
        steps: [...]
```

**Limits**: Max 8 stages, 120 events/journey, 70 events/stage, 30 versions

## Step Types

| Type | `with` Parameters |
|------|-------------------|
| `wait` | `duration`, `unit` (day/week) or `condition` |
| `activation` | `activation` (key from activations section) |
| `decision_point` | `branches[]` with segment, next |
| `ab_test` | `variants[]` with percentage, next (must sum to 100) |
| `merge` | (none) |
| `jump` | `target` with `journey`, `stage` |
| `end` | (none, no next) |

**Important**: `next:` is a direct field on step, not inside `with:`

```yaml
steps:
  - type: wait
    name: Wait 7 Days
    next: send-email     # Direct field, not in with:
    with:
      duration: 7
      unit: day          # day | week only

  - type: wait
    name: Wait for Purchase
    with:
      condition:
        segment: made-purchase   # Wait until segment match
        next: follow-up          # Optional: defaults to next sequential step
        timeout:                 # Max wait duration
          duration: 14
          unit: day
          next: timeout-path     # Step when max wait exceeded

  - type: activation
    name: Send Email
    with:
      activation: welcome-email  # Key from activations section

  - type: decision_point
    name: Check Tier
    with:
      branches:
        - name: Premium
          segment: premium-tier
          next: premium-path
        - name: Others
          excluded: true         # Default branch
          next: default-path

  - type: jump
    name: Go to Retention
    with:
      target:
        journey: Retention Journey   # Target journey name
        stage: Welcome Stage         # Target stage name

  - type: end
    name: Complete
```

## Activations

```yaml
activations:
  welcome-email:                    # Key referenced in steps
    name: Welcome Email Campaign
    connection: My SFMC Connection  # Connection name from `tdx connection list`
    all_columns: true
    schedule:
      type: none                    # none | daily | hourly
      timezone: UTC
    connector_config:               # Use `tdx connection schema <type>` for fields
      de_name: WelcomeEmails
      data_operation: upsert
```

See **connector-config** skill for `connector_config` details.

## Segment References

- **Embedded**: `segment: my-segment` (defined in `segments:` section)
- **External**: `segment: ref:Existing Segment` (use `ref:` prefix)

## Embedded Segment with Behavior

Use behavior data from parent segment in journey segments:

```yaml
segments:
  active_website_visitors:
    description: Users who visited website
    rule:
      type: And
      conditions:
        # Attribute condition
        - type: Value
          attribute: pv
          operator:
            type: GreaterEqual
            value: 5
        # Behavior aggregation condition
        - type: And
          conditions:
            - type: Value
              attribute: ""                    # Empty for behavior count
              operator:
                type: GreaterEqual
                value: 1
              aggregation:
                type: Count
              source: behavior_behv_website    # behavior_<table_name>
          description: has visited website
```

**Note**: Journey embedded segments use `source: behavior_<table_name>` (with `behavior_` prefix), unlike standalone segments which use `source: <behavior_name>`.

## Simulation (Recommended)

Push as `draft` first, then use TD Console → "Simulation Mode" to validate before launching.

## Common Issues

| Issue | Solution |
|-------|----------|
| Journey not processing | `tdx journey resume "Name"` |
| Segment not found | Use `ref:` prefix for external segments |
| Activation not triggering | `tdx connection list` to verify |

## Related Skills

- **connector-config**, **validate-journey**, **segment**, **validate-segment**, **parent-segment**

## Resources

- https://docs.treasuredata.com/products/customer-data-platform/journey-orchestration
