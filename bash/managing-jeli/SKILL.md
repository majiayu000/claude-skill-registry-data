---
name: managing-jeli
description: |
  Use when working with Jeli — jeli incident analysis, narrative-based
  post-incident reviews, opportunity identification, and learning extraction.
  Covers incident ingestion from Slack, timeline reconstruction, contributing
  factor analysis, and organizational learning patterns. Use when reviewing
  post-incident narratives, identifying systemic patterns, tracking
  opportunities, or analyzing incident learning in Jeli.
connection_type: jeli
preload: false
---

# Jeli Management Skill

Manage and analyze incidents, post-incident narratives, and organizational learning in Jeli.

## API Conventions

### Authentication
All API calls use the `Authorization: Bearer $JELI_API_KEY` header. Never hardcode tokens.

### Base URL
`https://api.jeli.io/v1`

### Core Helper Function

```bash
#!/bin/bash

jeli_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer $JELI_API_KEY" \
            -H "Content-Type: application/json" \
            "https://api.jeli.io/v1${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer $JELI_API_KEY" \
            -H "Content-Type: application/json" \
            "https://api.jeli.io/v1${endpoint}"
    fi
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Extract only needed fields with `jq`
- Target <=50 lines per script output
- Never dump full API responses

## Discovery Phase

### List Incidents

```bash
#!/bin/bash
echo "=== Recent Incidents ==="
jeli_api GET "/incidents?limit=25&sort=-created_at" \
    | jq -r '.incidents[] | "\(.created_at[0:16])\t\(.severity // "none")\t\(.status)\t\(.title[0:60])"' \
    | column -t

echo ""
echo "=== Incident Count by Status ==="
jeli_api GET "/incidents?limit=100" \
    | jq -r '.incidents[] | .status' | sort | uniq -c | sort -rn
```

### List Opportunities

```bash
#!/bin/bash
echo "=== Open Opportunities ==="
jeli_api GET "/opportunities?status=open&limit=20" \
    | jq -r '.opportunities[] | "\(.priority // "none")\t\(.title[0:60])\t\(.assignee // "unassigned")"' \
    | column -t

echo ""
echo "=== Opportunity Tags ==="
jeli_api GET "/opportunities?limit=50" \
    | jq -r '.opportunities[].tags[]' | sort | uniq -c | sort -rn | head -10
```

## Analysis Phase

### Incident Narrative Review

```bash
#!/bin/bash
INCIDENT_ID="${1:?Incident ID required}"

echo "=== Incident Details ==="
jeli_api GET "/incidents/${INCIDENT_ID}" \
    | jq '.incident | {id, title, status, severity, created_at, resolved_at, summary: .summary[0:200]}'

echo ""
echo "=== Narrative ==="
jeli_api GET "/incidents/${INCIDENT_ID}/narrative" \
    | jq -r '.narrative.content[0:500]'

echo ""
echo "=== Contributing Factors ==="
jeli_api GET "/incidents/${INCIDENT_ID}/factors" \
    | jq -r '.factors[] | "\(.category)\t\(.description[0:60])"' | column -t
```

### Learning Patterns

```bash
#!/bin/bash
echo "=== Recurring Themes ==="
jeli_api GET "/incidents?limit=50" \
    | jq -r '.incidents[].tags[]' | sort | uniq -c | sort -rn | head -15

echo ""
echo "=== Incidents by Team ==="
jeli_api GET "/incidents?limit=50" \
    | jq -r '.incidents[] | .teams[].name' | sort | uniq -c | sort -rn | head -10
```

## Output Format
- Use tab-separated columns with `column -t`
- Limit lists to 15-25 items
- Show summaries before details

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
- **Narrative-focused**: Jeli emphasizes narrative understanding over metrics -- summaries and context are key fields
- **Opportunities**: Jeli calls improvement items "opportunities" not "action items"
- **Slack integration**: Most incident data is ingested from Slack conversations
- **Rate limits**: Respect API rate limiting headers
- **Pagination**: Use `limit` and `offset` parameters
