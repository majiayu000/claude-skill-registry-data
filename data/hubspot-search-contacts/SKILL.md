---
name: hubspot-search-contacts
description: "Search contacts in HubSpot CRM by email, name, or company. Load when user says 'search contacts', 'find contact', 'lookup contact', 'search for [name]'."
---

# Search HubSpot Contacts

**Specialized skill** for searching contacts in HubSpot CRM.

## Pre-Flight Check

Before running, execute config check:
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/check_hubspot_config.py --json
```

If `ai_action` is not `proceed_with_operation`, follow hubspot-connect setup guide.

---

## Usage

### Search by Email
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/search_contacts.py \
  --email "john@example.com" \
  --json
```

### Search by Name
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/search_contacts.py \
  --name "John" \
  --json
```

### Search by Company
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/search_contacts.py \
  --company "Acme" \
  --json
```

### Combined Search with Limit
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/search_contacts.py \
  --name "John" \
  --company "Acme" \
  --limit 20 \
  --json
```

---

## Output Format

```json
{
  "total": 5,
  "results": [
    {
      "id": "12345",
      "properties": {
        "email": "john@example.com",
        "firstname": "John",
        "lastname": "Doe",
        "company": "Acme Corp"
      },
      "url": "https://app.hubspot.com/..."
    }
  ]
}
```

---

## Display Format

```
Found 5 contacts matching "John":

1. John Doe
   Email: john@example.com
   Company: Acme Corp
   ID: 12345

2. Johnny Smith
   Email: johnny@corp.com
   Company: Tech Inc
   ID: 12346
   ...
```

---

## Search Behavior

- Name search uses `CONTAINS_TOKEN` operator (partial match)
- Email search uses `EQ` operator (exact match)
- Company search uses `CONTAINS_TOKEN` operator (partial match)
- Multiple filters are combined with AND logic

---

## Error Handling

| Error | Solution |
|-------|----------|
| 401 | Invalid token - re-run setup |
| 403 | Missing `crm.objects.contacts.read` scope |
| 429 | Rate limited - wait and retry |

---

## Related Skills

- `hubspot-list-contacts` - List all contacts
- `hubspot-update-contact` - Update found contact
- `hubspot-create-contact` - Create if not found
