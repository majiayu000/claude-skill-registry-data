---
name: hubspot
description: "Manage HubSpot CRM objects and properties, configure workflows and private apps, and handle API rate limits."
category: enterprise
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["hubspot", "crm", "workflows", "marketing", "api", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# HubSpot CRM & Marketing AI Skill Guide

## Overview & Engine Architecture

HubSpot unifies CRM (contacts, companies, deals, tickets), marketing automation, and a REST API. Properties define fields; workflows and pipelines move records through stages. Private apps replace legacy API keys with scoped tokens. Agents design clear property taxonomies, idempotent syncs, and workflow rules that do not thrash records.

```
Portals
   -> CRM objects (contacts, companies, deals, tickets, custom)
       -> Properties + associations
       -> Pipelines / workflows / lists
Integrations -> Private app tokens -> HubSpot APIs (CRM, CMS, Events)
```

## When to use this skill

- Modeling deal pipelines and contact lifecycle stages
- Building HubSpot workflows without loops
- Syncing product/user data via the CRM API
- Debugging association and property mismatches

## Operational directives

1. Use private apps with least-privilege scopes; rotate tokens on staff changes.
2. Prefer association APIs over stuffing foreign keys into free-text properties.
3. Workflows: enrollment criteria must exclude already-processed records; watch re-enrollment.
4. Respect rate limits; batch reads/writes and backoff on `429`.
5. Do not use marketing emails as a substitute for transactional product mail without compliance review.

## CRM API sketch

```bash
curl -s -X POST "https://api.hubapi.com/crm/v3/objects/contacts/batch/upsert" \
  -H "Authorization: Bearer $HUBSPOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": [{
      "idProperty": "email",
      "id": "user@example.com",
      "properties": { "firstname": "Ada", "lifecyclestage": "lead" }
    }]
  }'
```

## Workflow hygiene

| Smell | Better approach |
| --- | --- |
| Workflow updates property that re-enrolls same workflow | Exclude that property from re-enrollment triggers |
| Dozens of near-duplicate properties | One canonical property + clear naming convention |
| Sync writes every field every time | Patch only changed properties; store last sync hash |
| Shared super-admin private app | Split apps by system (billing vs support vs marketing) |

## Best practices

- Document internal vs HubSpot-owned properties; prevent two systems fighting over the same field.
- Use custom objects only when standard objects cannot model the relationship.
- Log HubSpot object IDs on your side for supportability.
- Test workflow changes in a sandbox portal when available.

## Limitations

- Hub and seat tiers gate API limits, custom objects, and workflow capacity.
- Legacy API keys should be migrated; behavior differs from private apps.
- Attribution and marketing analytics need clean UTM and form capture - out of pure API scope.

## Related skills

- `@salesforce` - enterprise CRM with Apex/SOQL depth
- `@zapier` - connect HubSpot to tools without custom code
- `@asana` - task follow-ups spawned from deal stages
