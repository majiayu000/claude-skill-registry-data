---
name: hubspot-list-emails
description: "List email engagements from HubSpot CRM. Load when user says 'list emails', 'show emails', 'email history', 'hubspot emails'. Returns logged email records."
---

# List HubSpot Emails

**Specialized skill** for listing email engagements from HubSpot CRM.

## Pre-Flight Check

Before running, execute config check:
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/check_hubspot_config.py --json
```

If `ai_action` is not `proceed_with_operation`, follow hubspot-connect setup guide.

---

## Usage

### Basic List (default 10 emails)
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/list_emails.py --json
```

### With Limit
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/list_emails.py --limit 25 --json
```

### With Pagination
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/list_emails.py --after "cursor_value" --json
```

---

## Output Format

```json
{
  "results": [
    {
      "id": "14389550562",
      "properties": {
        "hs_email_subject": "Follow up on proposal",
        "hs_email_text": "Hi John, following up on...",
        "hs_email_direction": "EMAIL",
        "hs_email_status": "SENT",
        "hs_timestamp": "2025-12-13T10:00:00Z"
      }
    }
  ],
  "paging": {
    "next": {
      "after": "cursor_for_next_page"
    }
  }
}
```

---

## Display Format

```
Found {count} emails:

1. Follow up on proposal
   Direction: Sent
   Status: SENT
   Date: 2025-12-13 10:00
   Preview: Hi John, following up on...
   ID: 14389550562

2. Re: Demo request
   Direction: Received
   ...
```

---

## Email Direction Values

| Value | Meaning |
|-------|---------|
| EMAIL | Outbound (sent) |
| INCOMING_EMAIL | Inbound (received) |
| FORWARDED_EMAIL | Forwarded |

---

## Error Handling

| Error | Solution |
|-------|----------|
| 401 | Invalid token - re-run setup |
| 403 | Missing `crm.objects.emails.read` scope |
| 429 | Rate limited - wait and retry |

---

## Related Skills

- `hubspot-log-email` - Log new email
- `hubspot-get-associations` - Get email's linked contacts
