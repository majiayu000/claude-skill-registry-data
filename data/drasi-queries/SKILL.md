---
name: drasi-queries
description: Guide for writing Drasi continuous queries using Cypher. Use this when asked to create, modify, or troubleshoot Drasi queries.
---

# Drasi Query Development Skill

Use this skill when developing Drasi ContinuousQuery definitions with Cypher. If the user is not working with Drasi, do not apply this skill.

**IMPORTANT**: Use the `context7` MCP server with library ID `/drasi-project/docs` to get the latest Drasi documentation and Cypher syntax. Do not assume—verify current supported features.

**Verify-first** any Drasi capability or function behavior that may be version-dependent:

```text
[VERIFY]
EvidenceType = Docs | ReleaseNotes | Issue | Repro
WhereToCheck = <URL, repo, command, or repro steps>
```

## Capability & Version Notes

- **Tested against Drasi X.Y** (record `drasi version` output and keep this line current; version not verified in this repo).
- Cypher support follows Drasi's documented subset; GQL support is additive and must be explicitly enabled via `queryLanguage: GQL`.
- Verified against Drasi Cypher docs: features not listed in the supported subset (e.g., `collect`, `DISTINCT`, `ORDER BY`, `LIMIT`) should be treated as unsupported unless release notes state otherwise.

## Drasi Function Guidance (Select the Right Tool)

| Task type                    | Function                            | Notes / When to use                                                                                                   |
| ---------------------------- | ----------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| Detect state transition      | `drasi.previousDistinctValue()`     | Ignores repeated identical values.                                                                                    |
| Compare last-known values    | `drasi.previousValue()`             | Detect any change between revisions.                                                                                  |
| Evaluate sustained truth     | `drasi.trueFor()`                   | Requires continuous "true" state for duration.                                                                       |
| Evaluate timed condition     | `drasi.trueLater()`                 | Pending result until specified timestamp.                                                                             |
| Retrieve version snapshot    | `drasi.getVersionByTimestamp()`     | Requires temporal index.                                                                                              |
| Compute trend                | `drasi.linearGradient()`            | Aggregate slope detection (telemetry, rate rise).                                                                      |
| Change timestamps            | `drasi.changeDateTime()`            | Windowing and recency checks against element's last change time. Evidence: Drasi custom functions docs (link below).  |
| Historical lookup (range)    | `drasi.getVersionsByTimeRange()`    | Requires temporal index. Evidence: Drasi custom functions docs (link below).                                          |

Evidence: Drasi custom functions docs (https://github.com/drasi-project/docs/blob/main/docs/content/reference/query-language/drasi-custom-functions.md).

## When to Use Drasi vs Brokers

- **Use Drasi** for continuous queries over changing graphs, temporal reasoning (e.g., `trueFor`, historical versions), and when you need query results that reflect graph state transitions.
- **Use Event Hubs/Kafka** for high-throughput event streaming with replay and retention when you want to reprocess raw events or build multiple downstream projections.
- **Use Service Bus/queues** for command-style workflows, strict ordering per key, or guaranteed processing with dead-letter workflows.
- If you need **change-graph outputs with declarative querying**, Drasi is the right fit; if you need **raw event replay and fanout** without query semantics, prefer a broker.

## Query Performance & Reliability Guardrails

- Avoid Cartesian joins (`MATCH (a), (b)`) unless absolutely required; they scale poorly.
- Filter early with `WHERE` before aggregations to reduce per-diff work.
- Prefer indexed properties in Source data where possible; query cost is driven by change volume + aggregation.
- Reactions are **at-least-once**: design consumers to be idempotent and safe on duplicates.
- Document a replay plan when queries drive external side effects (e.g., Service Bus/webhooks).

## Supported Cypher Features (Safe to Use)

| Feature                         | Example                                                          |
| ------------------------------- | ---------------------------------------------------------------- |
| `MATCH`, `WHERE`, `RETURN`      | `MATCH (n:Node) WHERE n.id > 5 RETURN n`                         |
| `WITH ... count()`              | `WITH n.category AS cat, count(*) AS cnt`                        |
| Aggregations                    | `max()`, `min()`, `sum()`, `avg()`, `count()`                    |
| `coalesce()`                    | `RETURN coalesce(n.value, 0)`                                    |
| `drasi.changeDateTime()`        | `WHERE drasi.changeDateTime() > datetime()`                      |
| `drasi.previousValue()`         | `WHERE i.amount > drasi.previousValue(i.amount)`                 |
| `drasi.previousDistinctValue()` | `WHERE drasi.previousDistinctValue(c.status) = 'pending'`        |
| Graph relationships             | `MATCH (a)-[:LIKES]->(b)`                                        |
| Identifier escaping             | Use backticks for special chars: `` MATCH (n:`Special-Label`) `` |

## Unsupported Features (Will Fail)

| Feature     | Status                         | Workaround                          |
| ----------- | ------------------------------ | ----------------------------------- |
| `collect()` | ⚠️ Not in supported subset     | Use `WITH ... count()` pattern      |
| `DISTINCT`  | ❌ Not in supported subset      | Use `WITH ... count()` for grouping |
| `ORDER BY`  | ❌ Not in supported subset      | Sort client-side                    |
| `LIMIT`     | ❌ Not in supported subset      | Filter client-side                  |

Source: Drasi Cypher support docs (https://github.com/drasi-project/docs/blob/main/docs/content/reference/query-language/cypher.md)

## Query Patterns

### Aggregation Pattern (Correct)

```cypher
MATCH (w:WishlistItem)
WITH w.text AS item, count(*) AS frequency
WHERE frequency > 0
RETURN item, frequency
```

### Duplicate Detection Pattern

```cypher
MATCH (w1:WishlistItem), (w2:WishlistItem)
WHERE w1.toyName = w2.toyName
  AND w1.childId <> w2.childId
RETURN w1.childId AS child1,
       w2.childId AS child2,
       w1.toyName AS duplicate
```

### Time-Windowed Pattern

```cypher
MATCH (w:WishlistItem)
WHERE drasi.changeDateTime() > datetime() - duration('PT24H')
WITH w.toyName AS toy, count(*) AS requests
WHERE requests >= 5
RETURN toy, requests
```

## Critical: Label Configuration

Queries must use the **middleware label**, NOT the event hub name:

```yaml
# In Source definition
middleware:
  - kind: map
    my-event-hub:
      insert:
        - label: WishlistItem # <-- Use THIS in queries
```

```yaml
# Map event types to labels (event type != hub/topic name)
middleware:
  - kind: map
    toy-events-hub:
      insert:
        - label: WishlistItem
          when:
            eventType: wishlist.item.created
        - label: ChildProfile
          when:
            eventType: child.profile.updated
```

```cypher
# ✅ CORRECT
MATCH (w:WishlistItem)

# ❌ WRONG
MATCH (w:`my-event-hub`)
```

## Deployment Commands

Always use Drasi CLI, NOT kubectl. Deploy in this order and verify each step:

1. Source
2. Namespace (if used)
3. ContinuousQuery
4. Reaction

````bash
drasi apply -f queries.yaml -n drasi-system
drasi describe query my-query -n drasi-system
````

## GQL Support

**New Feature**: Drasi now supports Graph Query Language (GQL) in addition to Cypher!

```yaml
kind: ContinuousQuery
spec:
  queryLanguage: GQL  # or "Cypher" (default)
  query: |
    MATCH (v:Vehicle)
    WHERE v.color = 'Red'
    RETURN v.color
````

**GQL-Specific Features:**

- `FILTER` - Post-query filtering (like SQL HAVING)
- `LET` - Create computed variables
- `YIELD` - Project and rename columns
- `NEXT` - Chain multiple query statements
- `GROUP BY` - Explicit aggregation grouping

**Example with FILTER (post-aggregation):**

```gql
MATCH (v:Vehicle)
RETURN v.color AS color, count(v) AS vehicle_count
GROUP BY color
NEXT FILTER vehicle_count > 5
RETURN color, vehicle_count
```

**Common Parser Errors:**

- "Identifier not found in scope" - Check variable names match your MATCH clause
- Unexpected token errors - Ensure proper escaping with backticks for special characters

## Security Best Practices

### Input Validation

- **Never** concatenate user input directly into Cypher queries
- Validate and sanitize all external inputs before use in queries
- Use typed parameters where possible to prevent injection attacks

### Principle of Least Privilege

- Grant Sources only the minimum permissions needed to read data
- Configure Reactions with minimal write access to target systems
- Use separate service accounts for different query contexts

### Query Safety

- Avoid runtime construction of query strings; keep queries static and validate inputs before they reach Drasi.
- Prefer managed identities or workload identities for downstream reactions instead of embedding secrets.

## Contract Evolution Guidance

- **Additive schema changes**: add new properties/labels without removing existing ones; update queries to tolerate missing fields.
- **Renames**: dual-write old and new property names/labels during a transition period, then remove after consumers migrate.
- **Deprecations**: annotate query comments with deprecation date and migration path.

## YAML Structure Best Practices

### Naming Conventions

- Use descriptive, lowercase names with hyphens: `wishlist-trending-items`
- Prefix with domain/feature: `inventory-low-stock-alert`
- Include purpose in the name: `order-fraud-detection`

### Complete ContinuousQuery Example

```yaml
apiVersion: v1
kind: ContinuousQuery
name: wishlist-trending-items # Descriptive, hyphenated name
spec:
  # Specify query language explicitly
  queryLanguage: Cypher

  # Document the query purpose
  # Purpose: Detect trending wishlist items requested by 5+ children in 24h
  # Trigger: New WishlistItem events from event hub
  # Output: List of trending toy names with request counts

  sources:
    input:
      - wishlist-source # Reference to Source definition

  query: |
    MATCH (w:WishlistItem)
    WHERE drasi.changeDateTime() > datetime() - duration('PT24H')
    WITH w.toyName AS toy, count(*) AS requests
    WHERE requests >= 5
    RETURN toy, requests
```

### Complete Source Example

```yaml
apiVersion: v1
kind: Source
name: wishlist-source
spec:
  kind: EventHub # or PostgreSQL, CosmosDB, etc.
  properties:
    connectionString: ${EVENTHUB_CONNECTION_STRING} # Use env vars for secrets
    consumerGroup: drasi-consumer
  middleware:
    - kind: map
      my-event-hub:
        insert:
          - label: WishlistItem # Label used in MATCH clauses
            properties:
              - name: toyName
              - name: childId
              - name: priority
```

### Complete Reaction Example

```yaml
apiVersion: v1
kind: Reaction
name: trending-alert-reaction
spec:
  kind: SignalR # or Webhook, StoredProc, etc.
  queries:
    - wishlist-trending-items # Reference to ContinuousQuery
  properties:
    connectionString: ${SIGNALR_CONNECTION_STRING}
    hubName: trending-alerts
```

## Testing Guidance

### Local Loop

1. `drasi apply` to a test namespace
2. Inspect output with a debug Reaction and `drasi logs`
3. Validate query lag and expected match counts
4. Adjust and redeploy using versioned YAML

### Local Testing

1. Use representative sample data that covers edge cases
2. Test with the Drasi debug reaction to inspect query output:
   ```bash
   drasi apply -f debug-reaction.yaml -n drasi-system
   drasi logs reaction debug-reaction -n drasi-system -f
   ```

### Validation Checklist

- [ ] Query returns expected results with sample data
- [ ] Aggregations produce correct counts/sums
- [ ] Time-windowed queries trigger at appropriate intervals
- [ ] Middleware labels match MATCH clause labels exactly
- [ ] No unsupported Cypher features used
- [ ] Duplicate detection queries include deterministic keys for idempotent reactions
- [ ] Time-window boundaries behave as expected at edge values

### Common Test Scenarios

- Empty result set handling
- Single item vs. multiple items
- Boundary conditions for thresholds
- Time window edge cases

### Replay & Idempotency

- Reactions are **at-least-once**: design outputs to be idempotent with deterministic keys (e.g., `${queryId}:${entityId}:${windowStart}`).
- For external side effects, document a replay plan and how duplicates are deduplicated.

**Replay checklist:**

- [ ] Rebuild source with known input range
- [ ] Clear or version downstream projections
- [ ] Validate idempotency keys and dedupe logic
- [ ] Re-run query and compare counts before/after

### Backpressure & Retry Bounds

- Tighten `WHERE` filters early to reduce per-change workload and avoid backlog growth.
- Bound retries in downstream reactions; send poison messages to DLQ after max attempts.
- Monitor backlog and tune reaction concurrency to match downstream capacity.

## Troubleshooting

If query shows **TerminalError**:

1. Check for unsupported Cypher features (see table above)
2. Verify middleware label matches MATCH clause exactly
3. Use `drasi describe query <name> -n drasi-system` for error details

**Debug Steps:**

```bash
# Check query status
drasi list query -n drasi-system

# Get detailed error information
drasi describe query my-query -n drasi-system

# View reaction logs for output inspection
drasi logs reaction my-reaction -n drasi-system -f
```

## Observability & Cost

- Propagate correlation IDs from sources through reactions (headers or message properties).
- Emit metrics: query lag, reaction throughput, DLQ counts, and duplicate rate.
- Maintain a runbook: query purpose, rollback steps, replay steps, and alert thresholds.
- Minimize payload size in reactions; project only required fields.
- Avoid high-cardinality aggregations unless explicitly needed.

## References

### MCP Server

- Use `context7` MCP server with library ID: `/drasi-project/docs`

### Official Documentation

- [Drasi Documentation](https://drasi.io/) - Official docs and tutorials
- [Drasi GitHub Repositories](https://github.com/orgs/drasi-project/repositories) - Source code and examples

### Known Issues

- [Issue #308](https://github.com/drasi-project/drasi-platform/issues/308) - `drasi apply` 500 errors on reapply
- [Issue #43](https://github.com/drasi-project/drasi-core/issues/43) - `collect()` function implementation (in progress)
