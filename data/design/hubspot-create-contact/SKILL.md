---
name: hubspot-create-contact
description: "Create a new contact in HubSpot CRM. Load when user says 'create contact', 'add contact', 'new contact'. Requires email, optional firstname, lastname, phone, company."
---

# Create HubSpot Contact

**Specialized skill** for creating contacts in HubSpot CRM.

## Pre-Flight Check

Before running, execute config check:
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/check_hubspot_config.py --json
```

If `ai_action` is not `proceed_with_operation`, follow hubspot-connect setup guide.

---

## Usage

### Required Parameters
- `--email` - Contact email address (required)

### Optional Parameters
- `--firstname` - First name
- `--lastname` - Last name
- `--phone` - Phone number
- `--company` - Company name

### Examples

**Minimal (email only):**
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/create_contact.py \
  --email "john@example.com" \
  --json
```

**Full contact:**
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/create_contact.py \
  --email "john@example.com" \
  --firstname "John" \
  --lastname "Doe" \
  --phone "+1234567890" \
  --company "Acme Corp" \
  --json
```

---

## Output Format

```json
{
  "id": "12345",
  "properties": {
    "email": "john@example.com",
    "firstname": "John",
    "lastname": "Doe",
    "createdate": "2025-12-13T10:00:00Z"
  }
}
```

---

## Display Format

```
✅ Contact created!
  ID: 12345
  Name: John Doe
  Email: john@example.com
  Phone: +1234567890
  Company: Acme Corp
```

---

## Error Handling

| Error | Solution |
|-------|----------|
| 401 | Invalid token - re-run setup |
| 403 | Missing `crm.objects.contacts.write` scope |
| 409 | Contact already exists with this email |
| 429 | Rate limited - wait and retry |

---

## Related Skills

- `hubspot-list-contacts` - List all contacts
- `hubspot-search-contacts` - Find existing contacts
- `hubspot-update-contact` - Update contact details
