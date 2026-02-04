---
name: hubspot-create-company
description: "Create a new company in HubSpot CRM. Load when user says 'create company', 'add company', 'new company'. Requires name, optional domain, industry, city."
---

# Create HubSpot Company

**Specialized skill** for creating companies in HubSpot CRM.

## Pre-Flight Check

Before running, execute config check:
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/check_hubspot_config.py --json
```

If `ai_action` is not `proceed_with_operation`, follow hubspot-connect setup guide.

---

## Usage

### Required Parameters
- `--name` - Company name (required)

### Optional Parameters
- `--domain` - Company website domain
- `--industry` - Industry type
- `--city` - City location
- `--phone` - Company phone

### Examples

**Minimal (name only):**
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/create_company.py \
  --name "Acme Corp" \
  --json
```

**Full company:**
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/create_company.py \
  --name "Acme Corp" \
  --domain "acme.com" \
  --industry "Technology" \
  --city "San Francisco" \
  --json
```

---

## Output Format

```json
{
  "id": "6493611979",
  "properties": {
    "name": "Acme Corp",
    "domain": "acme.com",
    "industry": "Technology",
    "createdate": "2025-12-13T10:00:00Z"
  }
}
```

---

## Display Format

```
✅ Company created!
  ID: 6493611979
  Name: Acme Corp
  Domain: acme.com
  Industry: Technology
  City: San Francisco
```

---

## Error Handling

| Error | Solution |
|-------|----------|
| 401 | Invalid token - re-run setup |
| 403 | Missing `crm.objects.companies.write` scope |
| 409 | Company may already exist - search first |
| 429 | Rate limited - wait and retry |

---

## Related Skills

- `hubspot-list-companies` - List all companies
- `hubspot-search-companies` - Find existing companies
- `hubspot-get-associations` - Link contacts to company
