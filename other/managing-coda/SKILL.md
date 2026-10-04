---
name: managing-coda
description: |
  Use when working with Coda — coda document management covering docs, pages,
  tables, formulas, and workspace analytics. Use when auditing Coda workspace
  usage, managing documents and tables, querying structured data, or analyzing
  collaboration patterns across a Coda organization.
connection_type: coda
preload: false
---

# Managing Coda

Coda workspace management and analytics via the Coda REST API.

## Discovery Phase

```bash
#!/bin/bash
CODA_BASE="https://coda.io/apis/v1"

echo "=== Current User ==="
curl -s -H "Authorization: Bearer $CODA_TOKEN" \
  "$CODA_BASE/whoami" | jq '{name, loginId, type, scoped}'

echo ""
echo "=== Documents (top 25) ==="
curl -s -H "Authorization: Bearer $CODA_TOKEN" \
  "$CODA_BASE/docs?limit=25" \
  | jq -r '.items[] | "\(.id)\t\(.name[0:35])\t\(.folder.name // "root")\t\(.updatedAt[0:10])\t\(.owner)"' | column -t

echo ""
echo "=== Workspaces ==="
curl -s -H "Authorization: Bearer $CODA_TOKEN" \
  "$CODA_BASE/workspaces" \
  | jq -r '.items[]? | "\(.id)\t\(.name)\t\(.organizationId // "personal")"' | column -t

echo ""
echo "=== Doc Categories ==="
curl -s -H "Authorization: Bearer $CODA_TOKEN" \
  "$CODA_BASE/categories" \
  | jq -r '.items[]? | "\(.name)"' | head -15
```

## Analysis Phase

```bash
#!/bin/bash
CODA_BASE="https://coda.io/apis/v1"
DOC_ID="${1:?Doc ID required}"

echo "=== Document Details ==="
curl -s -H "Authorization: Bearer $CODA_TOKEN" \
  "$CODA_BASE/docs/$DOC_ID" \
  | jq '{name, owner, createdAt, updatedAt, folder: .folder.name, browserLink}'

echo ""
echo "=== Pages ==="
curl -s -H "Authorization: Bearer $CODA_TOKEN" \
  "$CODA_BASE/docs/$DOC_ID/pages?limit=25" \
  | jq -r '.items[] | "\(.id)\t\(.name[0:40])\t\(.parent.name // "root")"' | column -t

echo ""
echo "=== Tables ==="
curl -s -H "Authorization: Bearer $CODA_TOKEN" \
  "$CODA_BASE/docs/$DOC_ID/tables?limit=20" \
  | jq -r '.items[] | "\(.id)\t\(.name[0:30])\t\(.rowCount) rows\t\(.parent.name // "root")"' | column -t

echo ""
echo "=== Formulas ==="
curl -s -H "Authorization: Bearer $CODA_TOKEN" \
  "$CODA_BASE/docs/$DOC_ID/formulas?limit=15" \
  | jq -r '.items[]? | "\(.name[0:30])\t\(.value // "N/A")"' | column -t
```

## Output Format

```
CODA WORKSPACE OVERVIEW
User:          [name] ([email])
Total Docs:    [count]
Workspaces:    [count]

DOCUMENTS
Document               Folder     Updated     Owner
[name]                 [folder]   [date]      [owner]

DOCUMENT HEALTH: [doc_name]
Pages:         [count]
Tables:        [count]
Total Rows:    [count]
Formulas:      [count]
Last Updated:  [date]
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

