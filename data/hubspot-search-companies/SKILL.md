---
name: hubspot-search-companies
description: "Search companies in HubSpot CRM by name or domain. Load when user says 'search companies', 'find company', 'lookup company', 'search for [company]'."
---

# Search HubSpot Companies

**Specialized skill** for searching companies in HubSpot CRM.

## Pre-Flight Check

Before running, execute config check:
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/check_hubspot_config.py --json
```

If `ai_action` is not `proceed_with_operation`, follow hubspot-connect setup guide.

---

## Usage

### Search by Name
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/search_companies.py \
  --name "Acme" \
  --json
```

### Search by Domain
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/search_companies.py \
  --domain "acme.com" \
  --json
```

### With Limit
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/search_companies.py \
  --name "Tech" \
  --limit 20 \
  --json
```

---

## Output Format

```json
{
  "total": 3,
  "results": [
    {
      "id": "6493611979",
      "properties": {
        "name": "Acme Corp",
        "domain": "acme.com",
        "industry": "Technology",
        "city": "San Francisco"
      },
      "url": "https://app.hubspot.com/..."
    }
  ]
}
```

---

## Display Format

```
Found 3 companies matching "Acme":

1. Acme Corp
   Domain: acme.com
   Industry: Technology
   City: San Francisco
   ID: 6493611979

2. Acme Industries
   Domain: acmeindustries.com
   ...
```

---

## Search Behavior

- Name search uses `CONTAINS_TOKEN` operator (partial match)
- Domain search uses `CONTAINS_TOKEN` operator (partial match)
- Results sorted by relevance

---

## Error Handling

| Error | Solution |
|-------|----------|
| 401 | Invalid token - re-run setup |
| 403 | Missing `crm.objects.companies.read` scope |
| 429 | Rate limited - wait and retry |

---

## Related Skills

- `hubspot-list-companies` - List all companies
- `hubspot-create-company` - Create if not found
- `hubspot-get-associations` - Get company contacts
