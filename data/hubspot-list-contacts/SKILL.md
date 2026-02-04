---
name: hubspot-list-contacts
description: "List contacts from HubSpot CRM. Load when user says 'list contacts', 'show contacts', 'get contacts', 'hubspot contacts'. Returns paginated contact list with email, name, phone, company."
---

# List HubSpot Contacts

**Specialized skill** for listing contacts from HubSpot CRM.

## Pre-Flight Check

Before running, execute config check:
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/check_hubspot_config.py --json
```

If `ai_action` is not `proceed_with_operation`, follow hubspot-connect setup guide.

---

## Usage

### Basic List (default 10 contacts)
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/list_contacts.py --json
```

### With Limit
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/list_contacts.py --limit 25 --json
```

### With Pagination (after cursor)
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/list_contacts.py --after "cursor_value" --json
```

---

## Output Format

```json
{
  "results": [
    {
      "id": "12345",
      "properties": {
        "email": "john@example.com",
        "firstname": "John",
        "lastname": "Doe",
        "phone": "+1234567890",
        "company": "Acme Corp"
      },
      "url": "https://app.hubspot.com/contacts/.../record/0-1/12345"
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

Present results to user as:
```
Found {count} contacts:

1. John Doe
   Email: john@example.com
   Phone: +1234567890
   Company: Acme Corp
   ID: 12345

2. Jane Smith
   Email: jane@example.com
   ...
```

---

## Error Handling

| Error | Solution |
|-------|----------|
| 401 | Invalid token - re-run setup |
| 403 | Missing `crm.objects.contacts.read` scope |
| 429 | Rate limited - wait and retry |

---

## Related Skills

- `hubspot-create-contact` - Create new contact
- `hubspot-search-contacts` - Search by email/name
- `hubspot-update-contact` - Update existing contact
