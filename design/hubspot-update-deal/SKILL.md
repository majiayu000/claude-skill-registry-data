---
name: hubspot-update-deal
description: "Update an existing deal in HubSpot CRM. Load when user says 'update deal', 'edit deal', 'change deal stage', 'move deal', 'close deal'. Requires deal ID."
---

# Update HubSpot Deal

**Specialized skill** for updating deals in HubSpot CRM.

## Pre-Flight Check

Before running, execute config check:
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/check_hubspot_config.py --json
```

If `ai_action` is not `proceed_with_operation`, follow hubspot-connect setup guide.

---

## Usage

### Required Parameters
- `--id` - Deal ID (required)

### Optional Parameters (at least one required)
- `--name` - New deal name
- `--amount` - New deal value
- `--stage` - New deal stage
- `--closedate` - New close date (YYYY-MM-DD)

### Examples

**Update stage (move deal):**
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/update_deal.py \
  --id 5840795376 \
  --stage "closedwon" \
  --json
```

**Update amount:**
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/update_deal.py \
  --id 5840795376 \
  --amount 75000 \
  --json
```

**Close deal as won:**
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/update_deal.py \
  --id 5840795376 \
  --stage "closedwon" \
  --closedate "2025-12-13" \
  --json
```

---

## Common Deal Stages

| Stage ID | Name |
|----------|------|
| appointmentscheduled | Appointment Scheduled |
| qualifiedtobuy | Qualified to Buy |
| presentationscheduled | Presentation Scheduled |
| decisionmakerboughtin | Decision Maker Bought In |
| contractsent | Contract Sent |
| closedwon | Closed Won |
| closedlost | Closed Lost |

---

## Finding Deal ID

If user says "close the Acme deal", first search:
```bash
python 00-system/skills/hubspot/hubspot-master/scripts/search_deals.py --name "Acme" --json
```

Then use the returned ID for the update.

---

## Output Format

```json
{
  "id": "5840795376",
  "properties": {
    "dealname": "Acme Corp - Enterprise",
    "amount": "75000",
    "dealstage": "closedwon",
    "hs_lastmodifieddate": "2025-12-13T10:30:00Z"
  }
}
```

---

## Display Format

```
✅ Deal updated!
  ID: 5840795376
  Name: Acme Corp - Enterprise
  Updated fields:
    - stage: Closed Won
    - amount: $75,000
```

---

## Error Handling

| Error | Solution |
|-------|----------|
| 401 | Invalid token - re-run setup |
| 403 | Missing `crm.objects.deals.write` scope |
| 404 | Deal not found - check ID |
| 400 | Invalid stage ID |
| 429 | Rate limited - wait and retry |

---

## Related Skills

- `hubspot-search-deals` - Find deal ID
- `hubspot-list-deals` - List all deals
- `hubspot-create-deal` - Create new deal
