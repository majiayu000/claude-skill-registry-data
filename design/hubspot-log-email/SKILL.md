---
name: hubspot-log-email
description: "Log an email engagement in HubSpot CRM. Load when user says 'log email', 'record email', 'add email', 'email sent'. Requires subject and body."
---

# Log HubSpot Email

**Specialized skill** for logging email engagements in HubSpot CRM.

## Pre-Flight Check

Before running, execute config check:
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/check_hubspot_config.py --json
```

If `ai_action` is not `proceed_with_operation`, follow hubspot-connect setup guide.

---

## Usage

### Required Parameters
- `--subject` - Email subject line (required)
- `--body` - Email body content (required)

### Optional Parameters
- `--direction` - EMAIL (sent) or INCOMING_EMAIL (received)
- `--timestamp` - ISO timestamp (defaults to now)

### Examples

**Log sent email:**
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/log_email.py \
  --subject "Follow up on proposal" \
  --body "Hi John, following up on our conversation about the enterprise package..." \
  --json
```

**Log received email:**
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/log_email.py \
  --subject "Re: Proposal" \
  --body "Thanks for sending over the details..." \
  --direction "INCOMING_EMAIL" \
  --json
```

---

## Output Format

```json
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
```

---

## Display Format

```
✅ Email logged!
  ID: 14389550562
  Subject: Follow up on proposal
  Direction: Sent
  Status: SENT
  Timestamp: 2025-12-13 10:00
```

---

## Error Handling

| Error | Solution |
|-------|----------|
| 401 | Invalid token - re-run setup |
| 403 | Missing `crm.objects.emails.write` scope |
| 429 | Rate limited - wait and retry |

---

## Related Skills

- `hubspot-list-emails` - List all emails
- `hubspot-get-associations` - Link email to contact
