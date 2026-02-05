---
name: hubspot-get-associations
description: "Get associated records in HubSpot CRM. Load when user says 'get associations', 'linked records', 'contacts on deal', 'company contacts', 'related records', 'who is on this deal'."
---

# Get HubSpot Associations

**Specialized skill** for retrieving associated records between HubSpot CRM objects.

## Pre-Flight Check

Before running, execute config check:
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/check_hubspot_config.py --json
```

If `ai_action` is not `proceed_with_operation`, follow hubspot-connect setup guide.

---

## Usage

### Required Parameters
- `--object-type` - Source object type (contacts, companies, deals)
- `--object-id` - Source object ID
- `--to-type` - Target object type to find associations

### Examples

**Get contacts on a deal:**
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/get_associations.py \
  --object-type deals \
  --object-id 5840795376 \
  --to-type contacts \
  --json
```

**Get contacts at a company:**
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/get_associations.py \
  --object-type companies \
  --object-id 6493611979 \
  --to-type contacts \
  --json
```

**Get deals for a contact:**
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/get_associations.py \
  --object-type contacts \
  --object-id 12345 \
  --to-type deals \
  --json
```

**Get company for a contact:**
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/get_associations.py \
  --object-type contacts \
  --object-id 12345 \
  --to-type companies \
  --json
```

---

## Valid Object Types

| Type | Description |
|------|-------------|
| contacts | Contact records |
| companies | Company records |
| deals | Deal/opportunity records |

---

## Output Format

```json
{
  "results": [
    {
      "toObjectId": 12345,
      "associationTypes": [
        {
          "category": "HUBSPOT_DEFINED",
          "typeId": 3,
          "label": "Deal to Contact"
        }
      ]
    }
  ]
}
```

---

## Display Format

```
Found 3 contacts associated with deal 5840795376:

1. Contact ID: 12345 (Deal to Contact)
2. Contact ID: 12346 (Deal to Contact)
3. Contact ID: 12347 (Deal to Contact)

Use 'search contacts --id 12345' for full details.
```

---

## Common Use Cases

| User Says | Command |
|-----------|---------|
| "Who is on this deal?" | deals → contacts |
| "What company is John at?" | contacts → companies |
| "Show contacts at Acme" | companies → contacts |
| "What deals does John have?" | contacts → deals |

---

## Error Handling

| Error | Solution |
|-------|----------|
| 401 | Invalid token - re-run setup |
| 403 | Missing read scope for object type |
| 404 | Object not found - check ID |
| 429 | Rate limited - wait and retry |

---

## Related Skills

- `hubspot-list-contacts` - Get contact details
- `hubspot-list-companies` - Get company details
- `hubspot-list-deals` - Get deal details
