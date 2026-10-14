---
name: hubspot
description: Query and manage HubSpot CRM data — contacts, companies, deals, tickets, pipelines. Use when the user asks about CRM, clients, leads, sales pipeline, or customer data.
---

# HubSpot CRM (GenosOS)

Manage HubSpot CRM directly via `web_fetch` to the HubSpot API. No Python, no exec, no CLI needed.

## Setup

Store your HubSpot token in config:
```
config set env.HUBSPOT_TOKEN pat-eu1-xxxxx
```

## API Base

All requests use: `https://api.hubapi.com/crm/v3/objects/{objectType}`

Headers: `{ "Authorization": "Bearer {token}", "Content-Type": "application/json" }`

**Important:** Read the token from config first: `config get env.HUBSPOT_TOKEN`

## Search

```
web_fetch({
  url: "https://api.hubapi.com/crm/v3/objects/contacts/search",
  method: "POST",
  headers: { "Authorization": "Bearer {token}", "Content-Type": "application/json" },
  body: '{"filterGroups":[{"filters":[{"propertyName":"email","operator":"CONTAINS_TOKEN","value":"john"}]}],"properties":["firstname","lastname","email","phone"]}'
})
```

Search by: `email`, `firstname`, `lastname`, `company`, `phone`
Operators: `EQ`, `CONTAINS_TOKEN`, `GT`, `LT`, `BETWEEN`

## List Objects

```
web_fetch({
  url: "https://api.hubapi.com/crm/v3/objects/contacts?limit=20&properties=firstname,lastname,email,phone",
  headers: { "Authorization": "Bearer {token}" }
})
```

Object types: `contacts`, `companies`, `deals`, `tickets`

## Get Specific Object

```
web_fetch({
  url: "https://api.hubapi.com/crm/v3/objects/contacts/{id}?properties=firstname,lastname,email,phone,company",
  headers: { "Authorization": "Bearer {token}" }
})
```

## Create Object

### Contact
```
web_fetch({
  url: "https://api.hubapi.com/crm/v3/objects/contacts",
  method: "POST",
  headers: { "Authorization": "Bearer {token}", "Content-Type": "application/json" },
  body: '{"properties":{"email":"new@example.com","firstname":"Jane","lastname":"Doe","phone":"+34600000000"}}'
})
```

### Company
```
body: '{"properties":{"name":"Acme Corp","domain":"acme.com"}}'
```

### Deal
```
body: '{"properties":{"dealname":"Enterprise Plan","amount":"50000","pipeline":"default","dealstage":"appointmentscheduled"}}'
```

## Update Object

```
web_fetch({
  url: "https://api.hubapi.com/crm/v3/objects/contacts/{id}",
  method: "PATCH",
  headers: { "Authorization": "Bearer {token}", "Content-Type": "application/json" },
  body: '{"properties":{"phone":"+34600000001"}}'
})
```

## Associate Objects

```
web_fetch({
  url: "https://api.hubapi.com/crm/v4/objects/contacts/{contactId}/associations/companies/{companyId}",
  method: "PUT",
  headers: { "Authorization": "Bearer {token}", "Content-Type": "application/json" },
  body: '[{"associationCategory":"HUBSPOT_DEFINED","associationTypeId":1}]'
})
```

## Pipelines

```
web_fetch({
  url: "https://api.hubapi.com/crm/v3/pipelines/deals",
  headers: { "Authorization": "Bearer {token}" }
})
```

## Owners

```
web_fetch({
  url: "https://api.hubapi.com/crm/v3/owners",
  headers: { "Authorization": "Bearer {token}" }
})
```

## Common Properties

### Contacts
`firstname`, `lastname`, `email`, `phone`, `company`, `jobtitle`, `lifecyclestage`

### Companies
`name`, `domain`, `industry`, `phone`, `city`, `country`

### Deals
`dealname`, `amount`, `dealstage`, `pipeline`, `closedate`, `hubspot_owner_id`

## Workflow

1. Read token: `config get env.HUBSPOT_TOKEN`
2. Build API URL with object type and properties
3. Use `web_fetch` with Bearer auth
4. Save frequently-used IDs in [MEMORY] for faster access

## Notes

- API returns paginated results (default 10, max 100 per page)
- Use `after` cursor for pagination
- Token format: `pat-eu1-...` (EU) or `pat-na1-...` (US)
- All data transmitted via HTTPS — no local storage of CRM data
