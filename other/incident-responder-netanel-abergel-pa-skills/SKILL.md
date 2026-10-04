---
name: incident-responder
description: |-
  Runbook skill for failures: cron error, PA failure, cascade, gateway disconnect, semantic DB stale.
  Walks: detect → classify → diagnose → notify → log. Replaces ad-hoc failure handling.
  Triggers: "cron failed", "X is broken", "cascade", "incident", "gateway down", "PA failure".
---

# Incident Responder

Standardizes failure handling. No more ad-hoc.

## Classes
| Class | Trigger | First action |
|---|---|---|
| `cron-failure` | `cron_health.py` reports >26h gap | Run cron manually, capture output |
| `cron-cascade` | `detect_cascade()` returns true | Suspect shared config; check Vertex proxy first |
| `gateway-499` | WA gateway 499 disconnect >10min | `docker restart ocana-litellm-proxy` |
| `semantic-stale` | `check_sqlite_freshness()` False | Re-run `memory_search` ingest pipeline |
| `pa-failure` | PA agent error reported | DM owner; do NOT message PA's owner directly |

## Procedure (every class)

1. **Classify** using table above
2. **Diagnose** — collect logs (`tools/error_tracker.py log <component> <msg>`)
3. **Notify** — DM the owner ONLY (not the affected PA's owner)
4. **Mitigate** — execute the first action from the table
5. **Log** — append daily-note: `[HH:MM IL] INCIDENT <class>: <one-line summary>; resolved=<yes/no>`
6. **Postmortem** (if user-visible impact >5min) — create `memory/incidents/YYYY-MM-DD-<class>.md`

## Anti-patterns
- Do NOT loop trying the same fix twice
- Do NOT tell the PA's owner there's a problem before the owner knows
- Do NOT skip the daily-note log entry
