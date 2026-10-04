---
name: managing-xata
description: |
  Use when working with Xata — xata serverless database management via the xata
  CLI and Xata API. Covers databases, branches, tables, schema management,
  migrations, and search. Use when managing Xata databases or reviewing schema
  workflows.
connection_type: xata
preload: false
---

# Managing Xata

Manage Xata serverless databases using the `xata` CLI and Xata REST API.

## MANDATORY: Discovery-First Pattern

**Always discover available resources before performing analysis.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Workspaces ==="
curl -s "https://api.xata.io/workspaces" \
    -H "Authorization: Bearer $XATA_API_KEY" | jq -r '.workspaces[] | "\(.id)\t\(.name)\t\(.plan)\t\(.memberCount)"' | head -10

echo ""
echo "=== Databases ==="
WORKSPACE="${XATA_WORKSPACE:-$(curl -s 'https://api.xata.io/workspaces' -H "Authorization: Bearer $XATA_API_KEY" | jq -r '.workspaces[0].id')}"
curl -s "https://api.xata.io/workspaces/$WORKSPACE/dbs" \
    -H "Authorization: Bearer $XATA_API_KEY" | jq -r '.databases[] | "\(.name)\t\(.region)\t\(.createdAt)"' | head -20

echo ""
echo "=== Database Branches ==="
for db in $(curl -s "https://api.xata.io/workspaces/$WORKSPACE/dbs" -H "Authorization: Bearer $XATA_API_KEY" | jq -r '.databases[].name'); do
    echo "--- $db ---"
    curl -s "https://$WORKSPACE.xata.sh/dbs/$db" \
        -H "Authorization: Bearer $XATA_API_KEY" | jq -r '.branches[] | "\(.name)\t\(.createdAt)"' 2>/dev/null | head -5
done
```

### Phase 2: Analysis

```bash
#!/bin/bash

WORKSPACE="${XATA_WORKSPACE:?Set XATA_WORKSPACE}"
DB_NAME="${1:?Database name required}"
BRANCH="${2:-main}"

echo "=== Database Schema ==="
curl -s "https://$WORKSPACE.xata.sh/db/$DB_NAME:$BRANCH" \
    -H "Authorization: Bearer $XATA_API_KEY" | jq '{
    tables: [.schema.tables[] | {
        name: .name,
        columns: [.columns[] | {name: .name, type: .type}]
    }]
}' | head -30

echo ""
echo "=== Table List ==="
curl -s "https://$WORKSPACE.xata.sh/db/$DB_NAME:$BRANCH/tables" \
    -H "Authorization: Bearer $XATA_API_KEY" | jq -r '.tables[] | "\(.name)"' | head -20

echo ""
echo "=== Migration History ==="
curl -s "https://$WORKSPACE.xata.sh/db/$DB_NAME:$BRANCH/migrations/history" \
    -H "Authorization: Bearer $XATA_API_KEY" | jq -r '.migrations[] | "\(.id)\t\(.status)\t\(.createdAt)"' | head -10

echo ""
echo "=== Branch Comparison ==="
curl -s "https://$WORKSPACE.xata.sh/db/$DB_NAME:$BRANCH/compare/main" \
    -H "Authorization: Bearer $XATA_API_KEY" | jq '{
    edits: [.edits[] | {table: .table, operation: .operation}]
}' 2>/dev/null | head -15

echo ""
echo "=== Record Counts ==="
for table in $(curl -s "https://$WORKSPACE.xata.sh/db/$DB_NAME:$BRANCH/tables" -H "Authorization: Bearer $XATA_API_KEY" | jq -r '.tables[].name' 2>/dev/null); do
    count=$(curl -s "https://$WORKSPACE.xata.sh/db/$DB_NAME:$BRANCH/tables/$table/summarize" \
        -H "Authorization: Bearer $XATA_API_KEY" \
        -H "Content-Type: application/json" \
        -d '{"summaries":{"count":"*"}}' 2>/dev/null | jq '.summaries[0].count // 0')
    echo "$table: $count records"
done | head -20
```

## Output Format

```
DATABASE    BRANCH   REGION     TABLES   CREATED
my-app      main     us-east-1  8        2024-01-15
my-app      staging  us-east-1  8        2024-02-01
```

## Safety Rules
- Use read-only GET API calls and SELECT queries only
- Never run DELETE, PATCH schema changes without explicit user confirmation
- Use jq for structured output parsing
- Limit output with `| head -N` to stay under 50 lines

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

