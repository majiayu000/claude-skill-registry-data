---
name: working-with-resources
description: Work with Resource datasets (mutable state tracking) using OPAL temporal joins. Use when you need to enrich Events/Intervals with contextual state information, track resource state changes over time, or navigate between datasets using temporal relationships. Covers temporal join mechanics (lookup, join, follow), automatic field matching, and when to use Resources vs Reference Tables.
---

# Working with Resources

Work with Resource datasets (mutable state tracking) using OPAL temporal joins. Resources track state changes over time with Valid From/To timestamps. **Resources are rarely useful by themselves** - their power comes from enriching Events/Intervals with contextual state information through temporal joins.

Use when you need to:
- Enrich spans/logs with service metadata (type, environment, namespace)
- Track database dependencies between services
- Add resource state context to point-in-time events
- Navigate from events to related resources across datasets

Covers temporal join mechanics, three working join verbs (lookup, join, follow), and automatic field matching.

## Key Concepts

### What Are Resources?

Resources represent **mutable state** that changes over time:
- **Valid From** / **Valid To** timestamps (nanoseconds)
- Track how resource properties evolve (e.g., service environment changes)
- Created from Events/Intervals using `make_resource` verb
- Different from Intervals (which are immutable completed activities)

**Example**: OpenTelemetry/Service Resource tracks service metadata:
```
service_name: "checkoutservice"
service_type: "Service"
environment: "eu01"
Valid From: 2025-01-10T00:00:00Z
Valid To: 2025-01-11T00:00:00Z
```

### Temporal Joins

**Critical**: Resources use automatic temporal joins based on timestamp overlap:

```
Span:     |-----------|  (start_time to end_time)
Resource:    |-------------|  (Valid From to Valid To)
Match: YES (overlap exists)
```

OPAL automatically:
1. Matches timestamps (span time must overlap Resource validity period)
2. Matches field names (e.g., service_name = service_name)
3. No explicit ON clause needed

**Performance note**: `join` is faster than `lookup` for Resource joins (avoids extra left outer join pass).

## Join Verbs for Resources

Three join verbs work reliably with Resources:

| Verb | Returns | Performance | Use Case |
|------|---------|-------------|----------|
| `lookup` | All left rows + Resource fields | Slower (two-pass) | Enrichment - keep all data |
| `join` | Only matching rows + Resource fields | Faster (single-pass) | Filter + enrichment |
| `follow` | Right dataset rows that match | Unknown | Cross-dataset navigation |

### Pattern 1: lookup - Enrich All Rows

**Use when**: You want to keep ALL primary dataset rows, with optional Resource enrichment.

```opal
# Enrich ALL checkoutservice spans with service metadata
filter service_name = "checkoutservice"
| lookup @service_resource
| make_col svc:service_name,
          svc_type:service_type,
          svc_env:environment,
          dur_ms:duration / 1ms
| topk 10
```

**Behavior**:
- Returns all spans (even if no Resource match found)
- Resource fields populated when match exists
- Slower due to two-pass join (band-join + left outer join)

**Common MCP parameters**:
```json
{
  "primary_dataset_id": "42160967",
  "secondary_dataset_ids": ["42160979"],
  "dataset_aliases": {"service_resource": "42160979"}
}
```

### Pattern 2: join - Filter to Matches Only

**Use when**: You only want rows WITH Resource matches (faster performance).

```opal
# Show only spans where service metadata exists
filter service_name = "checkoutservice"
| join @service_resource
| make_col svc:service_name,
          svc_type:service_type,
          dur_ms:duration / 1ms
| limit 10
```

**Behavior**:
- Returns only spans with matching Resources
- Faster than `lookup` (single-pass band-join)
- Filters out spans with no Resource match

**When to use**:
- Performance matters
- You don't need rows without Resource context
- Filtering to matches is acceptable

### Pattern 3: follow - Navigate to Related Dataset

**Use when**: You want to find related dataset rows (cross-dataset navigation).

**Critical difference**: `follow` returns rows from the FOLLOWED dataset, not the primary dataset!

```opal
# Given error logs, show ALL related spans by namespace
filter body ~ /error/i
| follow @spans.service_namespace = namespace
| make_col svc:service_name,
          span:span_name,
          dur_ms:duration / 1000000
| limit 20
```

**Syntax**:
```
follow @dataset.field = primary_field
```

**Behavior**:
- Returns rows from @spans (not from logs)
- Matches based on field equality + temporal overlap
- Use case: "Given these logs, show me all related spans"

**Important**: This is NOT enrichment - you're switching to a different dataset entirely.

**Common MCP parameters for follow**:
```json
{
  "primary_dataset_id": "42161740",
  "secondary_dataset_ids": ["42160967"],
  "dataset_aliases": {"spans": "42160967"}
}
```

## Common Patterns

### Pattern: Service Inventory from Resource

```opal
# Count services by type in eu01 environment
filter environment = "eu01"
| make_col svc:service_name,
          svc_type:service_type,
          svc_ns:service_namespace
| statsby count:count(), group_by(svc_type)
| sort desc(count)
```

**Result**: 14 Services + 1 Database in eu01

**Note**: This queries the Resource dataset directly (no join needed).

### Pattern: Database Dependencies

```opal
# Find which services call which databases
make_col caller:parent_service_name,
         database:service_name,
         env:environment
| statsby count:count(), group_by(caller, database, env)
| sort desc(count)
| topk 10
```

**Dataset**: ServiceExplorer/Database Call (Resource)

**Result**: Shows cartservice → redis, observe-community-mcp → postgresql

### Pattern: Enrich Spans with Service Context

```opal
# Add service type and environment to high-latency spans
filter duration > 100ms
| join @service_resource
| make_col svc:service_name,
          type:service_type,
          env:environment,
          latency_ms:duration / 1ms
| statsby avg_latency:avg(latency_ms),
          count:count(),
          group_by(svc, type, env)
| sort desc(avg_latency)
```

**Why `join` here**: Filtering to spans with service metadata is acceptable, and it's faster than `lookup`.

### Pattern: Navigate from Logs to Spans

```opal
# Find all spans from namespaces that logged errors
filter body ~ /error/i
| follow @spans.service_namespace = namespace
| make_col svc:service_name,
          span:span_name,
          dur_ms:duration / 1000000
| statsby error_span_count:count(),
          avg_latency:avg(dur_ms),
          group_by(svc, span)
| sort desc(error_span_count)
```

**Why `follow`**: We want to see ALL spans from namespaces with errors, not just enrich the error logs.

**Dataset**: Kubernetes Logs (42161740) following to OpenTelemetry/Span (42160967)

## Troubleshooting

### Issue: "Field not found" after join

**Cause**: Resource field name doesn't match primary dataset field.

**Solution**: Check exact field names in Resource dataset:
```
discover_context(dataset_id="42160979")
```

Copy field names exactly (case-sensitive!).

### Issue: No Resource matches found

**Diagnosis**:
1. Check temporal overlap - Resource must be valid during span/event time
2. Verify field name matching (e.g., both have `service_name`)
3. Confirm Resource data exists for that time range

**Solution**: Query Resource dataset directly to see available data:
```opal
filter service_name = "checkoutservice"
| make_col valid_from:int64("Valid From"),
          valid_to:int64("Valid To")
| limit 5
```

### Issue: "implicit lookup does not support additional arguments"

**Error**: Tried using ON clause with lookup:
```opal
| lookup @resource on service_name = @resource.service_name  ❌
```

**Fix**: Remove ON clause - temporal joins are automatic:
```opal
| lookup @resource  ✅
```

### Issue: follow returns unexpected dataset

**Cause**: `follow` returns rows from the FOLLOWED dataset, not primary.

**This is correct behavior**:
- `lookup/join`: Keep primary dataset structure + add Resource fields
- `follow`: Switch to followed dataset, return matching rows

**Solution**: Use `lookup` or `join` if you want to enrich primary dataset.

## Available Resource Datasets

Common Resources in Observe (from discovery):

**OpenTelemetry/Service** (ID: 42160979):
- service_name (str)
- service_type (str) - "Database", "Service"
- environment (str)
- service_namespace (str)

**ServiceExplorer/Database Call** (ID: 42160978):
- service_name (str) - Database name
- parent_service_name (str) - Calling service
- environment (str)

**Discovery**: Use MCP to find Resources:
```
discover_context("resource", result_type="dataset", interface_filter="resource")
```

## Performance Considerations

**Faster**: `join` over `lookup`
- Documentation recommends `join` for Resource/Interval joins
- Avoids extra left outer join pass
- Only use `lookup` when you MUST keep all rows

**Temporal join cost**:
- OPAL performs interval overlapping band-join
- Matches timestamps + field names automatically
- More expensive than simple equality joins

**Best practice**: Filter primary dataset first to reduce join volume:
```opal
filter service_name = "checkoutservice"  # Filter FIRST
| join @service_resource                 # Then join
```

## Key Takeaways

1. **Resources track mutable state over time** (Valid From/To timestamps)
2. **Power comes from temporal joins**, not standalone queries
3. **Three working join verbs**:
   - `lookup` - enrich all rows (slower)
   - `join` - filter to matches (faster)
   - `follow` - navigate to related dataset
4. **Automatic temporal matching** - no ON clause needed
5. **Performance**: Prefer `join` over `lookup` when filtering acceptable

## References

- Temporal joins use interval overlapping band-join
- `set_valid_from` and `set_valid_to` define Resource validity
- `join` is faster than `lookup` (single-pass vs two-pass)
- `follow` requires field-based join condition: `follow @dataset.field = primary_field`
