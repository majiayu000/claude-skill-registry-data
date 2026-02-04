---
name: drasi-queries
description: Guide for writing Drasi continuous queries using Cypher. Use this when asked to create, modify, or troubleshoot Drasi queries.
---

# Drasi Query Development Skill

Use this skill when developing Drasi ContinuousQuery definitions with Cypher.

**IMPORTANT**: Use the `context7` MCP server with library ID `/drasi-project/docs` to get the latest Drasi documentation and Cypher syntax. Do not assume—verify current supported features.

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

| Feature     | Status                     | Workaround                          |
| ----------- | -------------------------- | ----------------------------------- |
| `collect()` | ⚠️ In development (PR #86) | Use `WITH ... count()` pattern      |
| `DISTINCT`  | ❌ Not supported           | Use `WITH ... count()` for grouping |
| `ORDER BY`  | ❌ Not supported           | Sort client-side                    |
| `LIMIT`     | ❌ Not supported           | Filter client-side                  |

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

```cypher
# ✅ CORRECT
MATCH (w:WishlistItem)

# ❌ WRONG
MATCH (w:`my-event-hub`)
```

## Deployment Commands

Always use Drasi CLI, NOT kubectl:

````bash
drasi apply -f queries.yaml -n drasi-system
drasi describe query my-query -n drasi-system
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

### Common Test Scenarios

- Empty result set handling
- Single item vs. multiple items
- Boundary conditions for thresholds
- Time window edge cases

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

## References

### MCP Server

- Use `context7` MCP server with library ID: `/drasi-project/docs`

### Official Documentation

- [Drasi Documentation](https://drasi.io/) - Official docs and tutorials
- [Drasi GitHub Repositories](https://github.com/orgs/drasi-project/repositories) - Source code and examples

### Known Issues

- [Issue #308](https://github.com/drasi-project/drasi-platform/issues/308) - `drasi apply` 500 errors on reapply
- [Issue #43](https://github.com/drasi-project/drasi-core/issues/43) - `collect()` function implementation (in progress)
