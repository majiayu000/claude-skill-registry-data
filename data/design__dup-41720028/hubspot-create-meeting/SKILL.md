---
name: hubspot-create-meeting
description: "Create a meeting engagement in HubSpot CRM. Load when user says 'create meeting', 'add meeting', 'schedule meeting', 'new meeting'. Requires title, start and end times."
---

# Create HubSpot Meeting

**Specialized skill** for creating meeting engagements in HubSpot CRM.

## Pre-Flight Check

Before running, execute config check:
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/check_hubspot_config.py --json
```

If `ai_action` is not `proceed_with_operation`, follow hubspot-connect setup guide.

---

## Usage

### Required Parameters
- `--title` - Meeting title (required)

### Optional Parameters
- `--body` - Meeting description/notes
- `--start` - Start time in ISO format (defaults to now)
- `--end` - End time in ISO format (defaults to start + 1 hour)

### Examples

**Meeting with times:**
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/create_meeting.py \
  --title "Product Demo" \
  --body "Demo of new features for enterprise team" \
  --start "2025-12-15T14:00:00Z" \
  --end "2025-12-15T15:00:00Z" \
  --json
```

**Quick meeting (defaults to now + 1 hour):**
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/create_meeting.py \
  --title "Quick sync call" \
  --json
```

---

## Output Format

```json
{
  "id": "14771947458",
  "properties": {
    "hs_meeting_title": "Product Demo",
    "hs_meeting_body": "Demo of new features...",
    "hs_meeting_start_time": "2025-12-15T14:00:00Z",
    "hs_meeting_end_time": "2025-12-15T15:00:00Z",
    "hs_timestamp": "2025-12-15T14:00:00Z"
  }
}
```

---

## Display Format

```
✅ Meeting created!
  ID: 14771947458
  Title: Product Demo
  Start: 2025-12-15 14:00
  End: 2025-12-15 15:00
  Duration: 1 hour
  Notes: Demo of new features for enterprise team
```

---

## Time Format

Use ISO 8601 format for times:
- `2025-12-15T14:00:00Z` (UTC)
- `2025-12-15T14:00:00+01:00` (with timezone)

---

## Error Handling

| Error | Solution |
|-------|----------|
| 401 | Invalid token - re-run setup |
| 403 | Missing `crm.objects.meetings.write` scope |
| 400 | Invalid time format |
| 429 | Rate limited - wait and retry |

---

## Related Skills

- `hubspot-list-meetings` - List all meetings
- `hubspot-get-associations` - Link meeting to contacts
