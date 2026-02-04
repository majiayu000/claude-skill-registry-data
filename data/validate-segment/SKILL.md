---
name: validate-segment
description: Validates CDP segment YAML configurations against the TD CDP API specification. Use when reviewing segment rules for correctness, checking operator types and values, or troubleshooting segment configuration errors before pushing to Treasure Data.
---

# Segment YAML Validation

```bash
tdx sg validate                           # Validate all YAML files locally
tdx sg validate path/to/segment.yml       # Validate specific file
tdx sg push --dry-run                     # Preview changes before push
```

## Required Structure

```yaml
name: string
kind: batch                    # batch | realtime | funnel_stage
rule:
  type: And                    # And | Or
  conditions:
    - type: Value
      attribute: field_name
      operator:
        type: OperatorType
        value: ...
```

## Operators Quick Reference

| Type | Value | Notes |
|------|-------|-------|
| `Equal`, `NotEqual` | single value | |
| `Greater`, `GreaterEqual`, `Less`, `LessEqual` | number | |
| `In`, `NotIn` | array | `["US", "CA"]` |
| `Contain`, `StartWith`, `EndWith` | array | `["@gmail.com"]` |
| `Regexp` | string | regex pattern |
| `IsNull` | (none) | |
| `TimeWithinPast`, `TimeWithinNext` | number + unit | `value: 30, unit: day` |
| `include`, `exclude` | segment name | reuse existing segment |

## Time Units (Singular Form Only)

```
year | quarter | month | week | day | hour | minute | second
```

**Common mistake**: `days` → `day`, `months` → `month`

## Behavior Aggregation Structure

```yaml
# Behavior condition with aggregation
- type: Value
  attribute: field_name          # Or "" for pure count
  operator:
    type: GreaterEqual
    value: 1
  aggregation:
    type: Count                  # Count | Sum | Avg | Min | Max
  source: behavior_name          # Behavior from parent segment
```

**Required fields**: `aggregation.type` and `source` must both be present

## Related Skills

- **segment** - Full segment management
