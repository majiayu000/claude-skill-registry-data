---
name: managing-glpi
description: |
  Use when working with Glpi — gLPI IT asset and service management covering
  ticket handling, hardware and software inventory, CMDB configuration items,
  and IT budget tracking. Use when managing helpdesk tickets with categorization
  and assignment, cataloging IT assets from network discovery, querying CMDB
  relationships between infrastructure components, or tracking IT procurement
  and contracts.
connection_type: glpi
preload: false
---

# GLPI IT Asset & Service Management Skill

Manage and analyze GLPI tickets, inventory, and CMDB.

## API Conventions

### Authentication
All API calls use session token obtained via `/initSession`. Token injected automatically.

### Base URL
`https://{{server}}/apirest.php`

### Core Helper Function

```bash
#!/bin/bash

glpi_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Session-Token: $GLPI_SESSION_TOKEN" \
            -H "Content-Type: application/json" \
            -H "App-Token: $GLPI_APP_TOKEN" \
            "${GLPI_URL}/apirest.php${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Session-Token: $GLPI_SESSION_TOKEN" \
            -H "Content-Type: application/json" \
            -H "App-Token: $GLPI_APP_TOKEN" \
            "${GLPI_URL}/apirest.php${endpoint}"
    fi
}
```

## Common Operations

### Ticket Management

```bash
#!/bin/bash
echo "=== Open Tickets ==="
glpi_api GET "/Ticket?searchText[status]=notold&range=0-24&order=ASC&sort=priority" \
    | jq -r '.[] | "\(.id)\tP\(.priority)\t\(.status)\t\(.name[0:60])"' \
    | column -t

echo ""
echo "=== Tickets by Category ==="
glpi_api GET "/Ticket?searchText[status]=notold&range=0-199" \
    | jq -r '[.[].itilcategories_id] | group_by(.) | map({cat: .[0], count: length}) | sort_by(.count) | reverse | .[:10] | .[] | "Category \(.cat): \(.count)"'

echo ""
echo "=== Overdue Tickets ==="
glpi_api GET "/Ticket?searchText[status]=notold&range=0-24&sort=time_to_resolve&order=ASC" \
    | jq -r '[.[] | select(.time_to_resolve != null and .time_to_resolve < now)] | .[:15] | .[] | "\(.id)\tP\(.priority)\t\(.time_to_resolve)\t\(.name[0:50])"' \
    | column -t
```

### Asset Inventory

```bash
#!/bin/bash
echo "=== Computer Inventory ==="
glpi_api GET "/Computer?range=0-24&order=DESC&sort=date_mod" \
    | jq -r '.[] | "\(.id)\t\(.name)\t\(.states_id)\t\(.date_mod[0:10])"' \
    | column -t

echo ""
echo "=== Network Equipment ==="
glpi_api GET "/NetworkEquipment?range=0-24" \
    | jq -r '.[] | "\(.id)\t\(.name)\t\(.networkequipmenttypes_id)\t\(.locations_id)"' \
    | column -t

echo ""
echo "=== Software Licenses ==="
glpi_api GET "/SoftwareLicense?range=0-24&order=DESC&sort=date_mod" \
    | jq -r '.[] | "\(.id)\t\(.name)\t\(.number // "unlimited")\t\(.expire[0:10] // "no expiry")"' \
    | column -t
```

### CMDB Operations

```bash
#!/bin/bash
echo "=== Item Types in CMDB ==="
for type in Computer Monitor NetworkEquipment Peripheral Phone Printer; do
    count=$(glpi_api GET "/${type}?range=0-0" | jq 'length')
    echo "${type}: ${count}"
done
```

## Output Format

Present results as a structured report:
```
Managing Glpi Report
════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

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

- **Session management**: Sessions expire — call `/initSession` to get a new token when receiving 401
- **App-Token required**: Both `Session-Token` and `App-Token` headers are required for API access
- **Range-based pagination**: Use `range=0-49` format (start-end) — not offset/limit
- **Status values**: `notold` = not solved/closed, `old` = solved/closed — or use numeric IDs (1-6)
- **Search criteria**: Complex queries use `criteria[]` array format with `field`, `searchtype`, `value`
- **Entity restrictions**: Results filtered by user's entity (organizational unit) permissions
- **Item types**: Endpoint names match GLPI class names exactly — case-sensitive (e.g., `Computer`, `NetworkEquipment`)
