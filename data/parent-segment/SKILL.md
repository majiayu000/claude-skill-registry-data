---
name: parent-segment
description: Manages CDP parent segments using `tdx ps` commands with YAML configs. Covers master tables, attributes, behaviors, `tdx ps validate` for join validation, `tdx ps preview` for data preview, and schedule configuration (daily/hourly/cron). Use when creating customer master tables, validating join match rates, or troubleshooting parent segment workflows.
---

# tdx Parent-Segment - CDP Parent Segment Management

## Core Commands

```bash
tdx ps list                                  # List parent segments
tdx ps pull "Customer 360"                   # Pull to YAML (sets context)
tdx ps push                                  # Push changes
tdx ps validate                              # Validate all
tdx ps validate --attribute "User Profile"   # Validate specific attribute
tdx ps preview --enriched                    # Preview joined data
tdx ps run                                   # Push and run workflow
tdx ps fields                                # List segmentation fields
```

## YAML Configuration

```yaml
name: "Customer 360"

master:
  database: cdp_db
  table: customers
  filters:                          # Optional: max 2 filters
    - column: status
      values: ["active"]

schedule:
  type: daily                       # none | hourly | daily | weekly | cron
  time: "03:00:00"
  timezone: "America/Los_Angeles"

attributes:
  - name: "User Profile"
    source:
      database: cdp_db
      table: user_profiles
    join:
      parent_key: user_id
      child_key: customer_id
    columns:
      - column: age
        type: number

behaviors:
  - name: "Purchases"
    source:
      database: cdp_db
      table: purchase_events
    join:
      parent_key: user_id
      child_key: customer_id
    columns:
      - column: amount
        type: number
```

## Common Issues

| Issue | Solution |
|-------|----------|
| Low join match rate | `tdx ps preview --master` and `--attribute` to compare keys |
| Workflow fails | `tdx ps validate --master`, `--attribute`, `--behavior` |

## Related Skills

- **segment** - Child segments using parent segment data
- **tdx-basic** - Core CLI operations

## Resources

- https://tdx.treasuredata.com/commands/parent-segment.html
