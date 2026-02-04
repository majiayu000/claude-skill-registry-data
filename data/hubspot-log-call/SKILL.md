---
name: hubspot-log-call
description: "Log a call engagement in HubSpot CRM. Load when user says 'log call', 'record call', 'add call', 'call made'. Requires title, optional body and duration."
---

# Log HubSpot Call

**Specialized skill** for logging call engagements in HubSpot CRM.

## Pre-Flight Check

Before running, execute config check:
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/check_hubspot_config.py --json
```

If `ai_action` is not `proceed_with_operation`, follow hubspot-connect setup guide.

---

## Usage

### Required Parameters
- `--title` - Call title (required)

### Optional Parameters
- `--body` - Call notes/summary
- `--duration` - Duration in minutes (default: 0)
- `--direction` - OUTBOUND or INBOUND (default: OUTBOUND)
- `--status` - COMPLETED, BUSY, NO_ANSWER, etc. (default: COMPLETED)

### Examples

**Log completed call:**
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/log_call.py \
  --title "Discovery Call with Acme" \
  --body "Discussed requirements, timeline, and budget. Next step: send proposal." \
  --duration 30 \
  --json
```

**Log missed call:**
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/log_call.py \
  --title "Follow-up attempt" \
  --status "NO_ANSWER" \
  --direction "OUTBOUND" \
  --json
```

---

## Call Status Values

| Status | Meaning |
|--------|---------|
| COMPLETED | Call connected |
| BUSY | Line busy |
| NO_ANSWER | No answer |
| FAILED | Call failed |
| CANCELED | Call canceled |

---

## Output Format

```json
{
  "id": "14772074448",
  "properties": {
    "hs_call_title": "Discovery Call with Acme",
    "hs_call_body": "Discussed requirements...",
    "hs_call_direction": "OUTBOUND",
    "hs_call_duration": "1800000",
    "hs_call_status": "COMPLETED",
    "hs_timestamp": "2025-12-13T10:00:00Z"
  }
}
```

---

## Display Format

```
✅ Call logged!
  ID: 14772074448
  Title: Discovery Call with Acme
  Direction: Outbound
  Duration: 30 minutes
  Status: Completed
  Notes: Discussed requirements, timeline...
```

---

## Error Handling

| Error | Solution |
|-------|----------|
| 401 | Invalid token - re-run setup |
| 403 | Missing `crm.objects.calls.write` scope |
| 429 | Rate limited - wait and retry |

---

## Related Skills

- `hubspot-list-calls` - List all calls
- `hubspot-get-associations` - Link call to contact
