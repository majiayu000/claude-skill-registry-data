---
name: hubspot-update-contact
description: "Update an existing contact in HubSpot CRM. Load when user says 'update contact', 'edit contact', 'modify contact', 'change contact'. Requires contact ID."
---

# Update HubSpot Contact

**Specialized skill** for updating contacts in HubSpot CRM.

## Pre-Flight Check

Before running, execute config check:
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/check_hubspot_config.py --json
```

If `ai_action` is not `proceed_with_operation`, follow hubspot-connect setup guide.

---

## Usage

### Required Parameters
- `--id` - Contact ID (required)

### Optional Parameters (at least one required)
- `--email` - New email address
- `--firstname` - New first name
- `--lastname` - New last name
- `--phone` - New phone number
- `--company` - New company name

### Examples

**Update phone:**
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/update_contact.py \
  --id 12345 \
  --phone "+1987654321" \
  --json
```

**Update multiple fields:**
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/update_contact.py \
  --id 12345 \
  --firstname "Jonathan" \
  --company "New Corp Inc" \
  --json
```

---

## Finding Contact ID

If user says "update John Doe", first search for the contact:
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/search_contacts.py --name "John Doe" --json
```

Then use the returned ID for the update.

---

## Output Format

```json
{
  "id": "12345",
  "properties": {
    "email": "john@example.com",
    "firstname": "Jonathan",
    "lastname": "Doe",
    "lastmodifieddate": "2025-12-13T10:30:00Z"
  }
}
```

---

## Display Format

```
✅ Contact updated!
  ID: 12345
  Updated fields:
    - firstname: Jonathan
    - company: New Corp Inc
```

---

## Error Handling

| Error | Solution |
|-------|----------|
| 401 | Invalid token - re-run setup |
| 403 | Missing `crm.objects.contacts.write` scope |
| 404 | Contact not found - check ID |
| 429 | Rate limited - wait and retry |

---

## Related Skills

- `hubspot-search-contacts` - Find contact ID
- `hubspot-list-contacts` - List all contacts
- `hubspot-create-contact` - Create new contact
