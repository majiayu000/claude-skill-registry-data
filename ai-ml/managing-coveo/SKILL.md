---
name: managing-coveo
description: |
  Use when working with Coveo — coveo enterprise search platform management
  including sources, indexes, query pipelines, machine learning models, usage
  analytics, and security providers. Covers indexing health, query performance,
  ML model status, content freshness, and license utilization.
connection_type: coveo
preload: false
---

# Coveo Management Skill

Monitor and manage Coveo enterprise search and relevance platform.

## MANDATORY: Discovery-First Pattern

**Always discover organization and sources before querying analytics or ML status.**

### Phase 1: Discovery

```bash
#!/bin/bash
COVEO_API="https://platform.cloud.coveo.com/rest"
AUTH="Authorization: Bearer ${COVEO_API_KEY}"
ORG="${COVEO_ORG_ID}"

echo "=== Organization Info ==="
curl -s -H "$AUTH" "$COVEO_API/organizations/$ORG" | \
  jq -r '"Name: \(.displayName)\nType: \(.type)\nLicense: \(.license.type)\nRegion: \(.region)"'

echo ""
echo "=== Sources ==="
curl -s -H "$AUTH" "$COVEO_API/organizations/$ORG/sources" | \
  jq -r '.[] | "\(.name) | Type: \(.sourceType) | Status: \(.information.sourceStatus.type) | Items: \(.information.numberOfDocuments)"' | head -15

echo ""
echo "=== Query Pipelines ==="
curl -s -H "$AUTH" "$COVEO_API/search/v2/admin/pipelines?organizationId=$ORG" | \
  jq -r '.[] | "\(.name) | ID: \(.id) | Condition: \(.condition // "default")"'

echo ""
echo "=== ML Models ==="
curl -s -H "$AUTH" "$COVEO_API/organizations/$ORG/machinelearning/models" | \
  jq -r '.[] | "\(.modelDisplayName) | Type: \(.engineId) | Status: \(.modelStatus)"'

echo ""
echo "=== Security Providers ==="
curl -s -H "$AUTH" "$COVEO_API/organizations/$ORG/securityproviders" | \
  jq -r '.[] | "\(.name) | Type: \(.type) | Status: \(.statistics.status // "N/A")"'
```

**Phase 1 outputs:** Organization, sources, pipelines, ML models, security providers

### Phase 2: Analysis

```bash
#!/bin/bash
echo "=== Source Health ==="
curl -s -H "$AUTH" "$COVEO_API/organizations/$ORG/sources" | \
  jq -r '.[] | select(.information.sourceStatus.type != "IDLE") | "\(.name): \(.information.sourceStatus.type) - \(.information.sourceStatus.message // "")"'

echo ""
echo "=== Index Size ==="
curl -s -H "$AUTH" "$COVEO_API/organizations/$ORG/indexes" | \
  jq -r '.[] | "Index: \(.name) | Documents: \(.numberOfDocuments) | Size: \(.diskSpaceUsed // "N/A")"'

echo ""
echo "=== Search Usage (last 7 days) ==="
curl -s -H "$AUTH" "$COVEO_API/ua/v15/stats/search?org=$ORG&from=$(date -v-7d +%Y-%m-%dT%H:%M:%S 2>/dev/null || date -d '7 days ago' +%Y-%m-%dT%H:%M:%S)Z&to=$(date +%Y-%m-%dT%H:%M:%S)Z" | \
  jq -r '"Total Searches: \(.totalCount // "N/A")\nAvg Click Rank: \(.averageClickRank // "N/A")"' 2>/dev/null || echo "Check analytics via Coveo Admin Console"

echo ""
echo "=== Top Queries (no results) ==="
curl -s -H "$AUTH" "$COVEO_API/ua/v15/stats/topQueries?org=$ORG&from=$(date -v-7d +%Y-%m-%dT%H:%M:%S 2>/dev/null || date -d '7 days ago' +%Y-%m-%dT%H:%M:%S)Z&to=$(date +%Y-%m-%dT%H:%M:%S)Z&withNoResults=true" | \
  jq -r '.[:5] | .[] | "\(.query) | Count: \(.count)"' 2>/dev/null || echo "Check via admin console"

echo ""
echo "=== License Usage ==="
curl -s -H "$AUTH" "$COVEO_API/organizations/$ORG/license" | \
  jq -r '"Indexed Items: \(.indexedItems.current)/\(.indexedItems.limit)\nQueries/Month: \(.queryCount.current // "N/A")/\(.queryCount.limit // "N/A")"' 2>/dev/null
```

## Output Format

```
COVEO STATUS
============
Org: {name} ({license})
Sources: {count} ({healthy}/{total} healthy)
Indexed Documents: {count}/{limit}
Query Pipelines: {count}
ML Models: {active}/{total} active
7-Day Searches: {count}
No-Result Queries: {count}
Issues: {list_of_warnings}
```

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

## Common Pitfalls

- **API key scopes**: Different operations need different privilege levels — use least privilege
- **Source rebuilds**: Full rebuilds can take hours — schedule during off-peak
- **ML model training**: Models need sufficient query data — minimum ~1000 queries for ART
- **Security identity**: Index permissions require properly configured security providers
