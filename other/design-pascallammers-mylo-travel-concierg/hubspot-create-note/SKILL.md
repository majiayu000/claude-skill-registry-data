---
name: hubspot-create-note
description: "Create a note engagement in HubSpot CRM. Load when user says 'create note', 'add note', 'new note', 'record note'. Requires body content."
---

# Create HubSpot Note

**Specialized skill** for creating note engagements in HubSpot CRM.

## Pre-Flight Check

Before running, execute config check:
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/check_hubspot_config.py --json
```

If `ai_action` is not `proceed_with_operation`, follow hubspot-connect setup guide.

---

## Usage

### Required Parameters
- `--body` - Note content (required)

### Optional Parameters
- `--timestamp` - ISO timestamp (defaults to now)

### Examples

**Simple note:**
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/create_note.py \
  --body "Spoke with John about pricing. He's interested in the enterprise tier." \
  --json
```

**Note with timestamp:**
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/create_note.py \
  --body "Meeting notes from yesterday's call" \
  --timestamp "2025-12-12T14:00:00Z" \
  --json
```

---

## Output Format

```json
{
  "id": "16977760701",
  "properties": {
    "hs_note_body": "Spoke with John about pricing...",
    "hs_timestamp": "2025-12-13T10:00:00Z"
  }
}
```

---

## Display Format

```
✅ Note created!
  ID: 16977760701
  Content: Spoke with John about pricing. He's interested in the enterprise tier.
  Timestamp: 2025-12-13 10:00
```

---

## Best Practices

- Keep notes concise but informative
- Include action items and next steps
- Reference specific topics discussed
- Use for internal context that won't go in emails

---

## Error Handling

| Error | Solution |
|-------|----------|
| 401 | Invalid token - re-run setup |
| 403 | Missing `crm.objects.notes.write` scope |
| 429 | Rate limited - wait and retry |

---

## Related Skills

- `hubspot-list-notes` - List all notes
- `hubspot-get-associations` - Link note to contact/deal
