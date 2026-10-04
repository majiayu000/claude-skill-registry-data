---
name: managing-neon
description: |
  Use when working with Neon — neon serverless Postgres management via the
  neonctl CLI and Neon API. Covers projects, branches, databases, roles,
  endpoints, and compute scaling. Use when managing Neon databases or reviewing
  branch workflows.
connection_type: neon
preload: false
---

# Managing Neon

Manage Neon serverless Postgres using the `neonctl` CLI or Neon API.

## MANDATORY: Discovery-First Pattern

**Always discover available resources before performing analysis.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Projects ==="
neonctl projects list --output json 2>/dev/null | jq -r '.[] | "\(.id)\t\(.name)\t\(.region_id)\t\(.pg_version)\t\(.created_at)"' | head -20

echo ""
echo "=== Branches ==="
for proj in $(neonctl projects list --output json 2>/dev/null | jq -r '.[].id'); do
    echo "--- Project: $proj ---"
    neonctl branches list --project-id "$proj" --output json 2>/dev/null | jq -r '.[] | "\(.id)\t\(.name)\t\(.primary)\t\(.current_state)\t\(.created_at)"' | head -10
done

echo ""
echo "=== Endpoints ==="
for proj in $(neonctl projects list --output json 2>/dev/null | jq -r '.[].id'); do
    echo "--- Project: $proj ---"
    neonctl endpoints list --project-id "$proj" --output json 2>/dev/null | jq -r '.[] | "\(.id)\t\(.branch_id)\t\(.type)\t\(.current_state)\t\(.host)"' | head -10
done

echo ""
echo "=== Databases ==="
for proj in $(neonctl projects list --output json 2>/dev/null | jq -r '.[].id'); do
    BRANCH=$(neonctl branches list --project-id "$proj" --output json 2>/dev/null | jq -r '.[0].id')
    echo "--- Project: $proj ---"
    neonctl databases list --project-id "$proj" --branch-id "$BRANCH" --output json 2>/dev/null | jq -r '.[] | "\(.name)\t\(.owner_name)"' | head -10
done
```

### Phase 2: Analysis

```bash
#!/bin/bash

PROJECT_ID="${1:?Project ID required}"

echo "=== Project Details ==="
neonctl projects get "$PROJECT_ID" --output json 2>/dev/null | jq '{
    id, name, region_id, pg_version,
    store_passwords, history_retention_seconds,
    compute_last_active_at, created_at, updated_at
}'

echo ""
echo "=== Branch Details ==="
neonctl branches list --project-id "$PROJECT_ID" --output json 2>/dev/null | jq '.[] | {
    id, name, primary, current_state,
    logical_size, data_transfer_bytes,
    created_at, updated_at
}' | head -30

echo ""
echo "=== Endpoint Compute ==="
neonctl endpoints list --project-id "$PROJECT_ID" --output json 2>/dev/null | jq '.[] | {
    id, type, current_state, host,
    autoscaling_limit_min_cu, autoscaling_limit_max_cu,
    suspend_timeout_seconds
}' | head -20

echo ""
echo "=== Roles ==="
BRANCH=$(neonctl branches list --project-id "$PROJECT_ID" --output json 2>/dev/null | jq -r '.[0].id')
neonctl roles list --project-id "$PROJECT_ID" --branch-id "$BRANCH" --output json 2>/dev/null | jq -r '.[] | "\(.name)\t\(.protected)\t\(.created_at)"' | head -10

echo ""
echo "=== Operations (Recent) ==="
neonctl operations list --project-id "$PROJECT_ID" --output json 2>/dev/null | jq -r '.[] | "\(.id)\t\(.action)\t\(.status)\t\(.created_at)\t\(.updated_at)"' | head -10
```

## Output Format

```
PROJECT_ID       NAME        REGION     PG_VERSION  CREATED
abc123def456     my-app-db   us-east-2  16          2024-01-15T10:00:00Z
```

## Safety Rules
- Use read-only commands: `list`, `get`
- Never run `delete`, `suspend`, `reset` without explicit user confirmation
- Use `--output json` with jq for structured output parsing
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

