---
name: openrind-desktop-debug
description: Debug Openrind Desktop sidecars, config, and audit trail
---

## Credential check

Set these before running the HTTP checks:

- `OPENRIND_DESKTOP_SERVER_URL`
- `OPENRIND_DESKTOP_SERVER_TOKEN`
- `OPENRIND_DESKTOP_WORKSPACE_ID` (optional; use `/workspaces` to discover)

## Quick usage (read-only)

```bash
curl -s "$OPENRIND_DESKTOP_SERVER_URL/health"
curl -s "$OPENRIND_DESKTOP_SERVER_URL/capabilities" \
  -H "Authorization: Bearer $OPENRIND_DESKTOP_SERVER_TOKEN"

curl -s "$OPENRIND_DESKTOP_SERVER_URL/workspaces" \
  -H "Authorization: Bearer $OPENRIND_DESKTOP_SERVER_TOKEN"
```

## Workspace config snapshot

```bash
curl -s "$OPENRIND_DESKTOP_SERVER_URL/workspace/$OPENRIND_DESKTOP_WORKSPACE_ID/config" \
  -H "Authorization: Bearer $OPENRIND_DESKTOP_SERVER_TOKEN"
```

## Audit log (recent)

```bash
curl -s "$OPENRIND_DESKTOP_SERVER_URL/workspace/$OPENRIND_DESKTOP_WORKSPACE_ID/audit?limit=25" \
  -H "Authorization: Bearer $OPENRIND_DESKTOP_SERVER_TOKEN"
```

## OpenCode engine checks

```bash
opencode -p "ping" -f json -q
opencode mcp list
opencode mcp debug <name>
```

## DB fallback (read-only)

When the engine API is unavailable, you can inspect the SQLite db:

```bash
sqlite3 ~/.opencode/opencode.db "select id, title, status from sessions order by updated_at desc limit 5;"
sqlite3 ~/.opencode/opencode.db "select role, content from messages order by created_at desc limit 10;"
```

## Notes

- Audit logs are stored at `.opencode/openrind-desktop/audit.jsonl` in the workspace root.
- Openrind Desktop server writes only within approved workspace roots.
