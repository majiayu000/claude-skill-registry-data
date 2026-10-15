---
name: zoho-api
description: Zoho API integration for all Zoho apps, one auth model.
version: 1.0.0
author: Hermes Agent
platforms: [windows, linux, macos]
---

# Zoho API Integration (all applications)

Covers API integration across the entire Zoho ecosystem with one common OAuth 2.0 model. Use when connecting any Zoho app to external data sources, syncing data between Zoho apps, or building integrations for Harsh's clients.

## Trigger Conditions
- Integrate data into or out of any Zoho application (CRM, Creator, Books, Inventory, Desk, People, Analytics, etc.)
- Multi-source data sync to Zoho (CSV, SQL, Google Sheets, external APIs → Zoho)
- Build webhooks, scheduled syncs, or Zoho Flow automations
- Any OAuth/token question for Zoho APIs

## 1. Authentication (works for ALL Zoho apps)

One OAuth 2.0 flow, per-app scopes. Self-client setup in https://api-console.zoho.com:

```
POST https://accounts.zoho.{dc}/oauth/v2/token
  grant_type=authorization_code&code=<grant_token>
  &client_id=<id>&client_secret=<secret>&redirect_uri=<uri>
# Refresh:
POST https://accounts.zoho.{dc}/oauth/v2/token
  grant_type=refresh_token&refresh_token=<rt>&client_id=<id>&client_secret=<secret>
```

**Data centers (dc) — CRITICAL, org-dependent:**
| Region | Auth domain | API domain |
|---|---|---|
| US | accounts.zoho.com | api.zoho.com |
| EU | accounts.zoho.eu | api.zoho.eu |
| IN | accounts.zoho.in | api.zoho.in |
| AU | accounts.zoho.com.au | api.zoho.com.au |
| JP | accounts.zoho.jp | api.zoho.jp |

Auth header for every request: `Authorization: Zoho-oauthtoken <access_token>`.
Scopes are per app (e.g. `ZohoCRM.modules.ALL`, `ZohoBooks.fullaccess.all`, `ZohoCreator.forms.ALL`).
Pitfalls: refresh tokens expire after 60 days of non-use on self-clients; use connections inside Creator/Flow where possible to skip token management; check the org's data center before coding (wrong DC = auth failures).

## 2. Master app table

| App | API base (US) | Scope prefix | REST docs |
|---|---|---|---|
| CRM | api.zoho.com/crm/v6 | ZohoCRM.modules.ALL | zoho.com/crm/developer/docs/api |
| Creator | creator.zoho.com/api/v2 | ZohoCreator.forms.ALL | zoho.com/creator/help/api |
| Books | books.zoho.com/api/v3 | ZohoBooks.fullaccess.all | zoho.com/books/api |
| Invoice | invoice.zoho.com/api/v3 | ZohoInvoice.fullaccess.all | zoho.com/invoice/api |
| Inventory | inventory.zoho.com/api/v1 | ZohoInventory.fullaccess.all | zoho.com/inventory/api |
| Desk | desk.zoho.com/api/v1 | ZohoDesk.tickets.ALL | zoho.com/desk/developer |
| People | people.zoho.com/people/api | ZohoPeople.people.ALL | zoho.com/people/api |
| Recruit | recruit.zoho.com/recruit/v2 | ZohoRecruit.modules.ALL | zoho.com/recruit/developer |
| Projects | projectsapi.zoho.com/restapi | ZohoProjects.projects.ALL | zoho.com/projects/api |
| Analytics | analytics.zoho.com/api | ZohoAnalytics.analytics.ALL | zoho.com/analytics/api |
| Mail | mail.zoho.com/api | ZohoMail.messages.ALL | zoho.com/mail/api |
| Calendar | calendar.zoho.com/api/v1 | ZohoCalendar.calendar.ALL | zoho.com/calendar/api |
| Expense | expense.zoho.com/api/v1 | ZohoExpense.expense.ALL | zoho.com/expense/api |
| Subscriptions | subscriptions.zoho.com/api/v1 | ZohoSubscriptions.fullaccess.all | zoho.com/subscriptions/api |
| Billing | billing.zoho.com/api/v1 | ZohoBilling.fullaccess.all | zoho.com/billing/api |
| SalesIQ | salesiq.zoho.com/api | ZohoSalesIQ.* | zoho.com/salesiq/developer |
| Survey | survey.zoho.com/api/v1 | ZohoSurvey.surveys.ALL | zoho.com/survey/api |
| Forms | forms.zoho.com/api | ZohoForms.forms.ALL | zoho.com/forms/api |
| Sign | sign.zoho.com/api/v1 | ZohoSign.document.ALL | zoho.com/sign/api |
| Flow | flow.zoho.com/api/v1 | ZohoFlow.flow.ALL | zoho.com/flow/api |
| Catalyst | catalyst.zoho.com/api/v1 | ZohoCatalyst.* | catalyst.zoho.com/developer |
| Tables | tables.zoho.com/api | ZohoTables.table.ALL | zoho.com/tables/api |
| Cliq | cliq.zoho.com/api/v2 | ZohoCliq.* | zoho.com/cliq/developer |
| WorkDrive | workdrive.zoho.com/api/v1 | ZohoWorkDrive.files.ALL | zoho.com/workdrive/api |
| Bigin | bigin.zoho.com/api/v1 | ZohoBigin.modules.ALL | zoho.com/bigin/api |
| Bookings | bookings.zoho.com/api/v1 | ZohoBookings.* | zoho.com/bookings/api |
| ZeptoMail | zeptomail.zoho.com/api/v1 | ZohoMail.ZeptoMail.ALL | zoho.com/zeptomail/api |
| Qntrl | qntrl.zoho.com/api | ZohoQntrl.ALL | qntrl.zoho.com/developer |
| Payroll | payroll.zoho.com/api | ZohoPayroll.* | zoho.com/payroll/api |
| Social | social.zoho.com/api/v1 | ZohoSocial.* | zoho.com/social/developer |

## 3. Multi-source → Zoho integration patterns

**Pattern A: External API/CSV/SQL → Zoho (bulk sync)**
1. Extract: pull from source (SQL query, Google Sheets, REST API, CSV)
2. Transform: map fields to Zoho API names, handle types (dates ISO yyyy-MM-dd)
3. Load: chunked POSTs (50-100/batch), dedupe by external ID in a custom field
4. Handle 429: backoff with Retry-After header; watch daily quota (varies by app, ~10k/day default)

**Pattern B: Zoho → external system (webhook/push)**
- Use Zoho Flow (flow.zoho.com) for no-code triggers/actions across apps
- Or build webhooks: subscribe to CRM/Desk events (channel API) and forward via invokeurl/Deluge or Python

**Pattern C: Two-way sync (e.g. CRM ↔ Books)**
- CRM contact ↔ Books customer, Deal ↔ Invoice. Use external-ID mapping fields on both sides
- Deluge `connection.execute()` or zoho.crm/zoho.books built-ins inside Creator/Flow

## 4. Best practices

- ✅ Always confirm the org's data center (DC) first — check accounts URL used by the org admin
- ✅ Use per-app scopes, minimal privilege; store tokens encrypted, never in code
- ✅ Use Zoho Flow or Creator connections for app-to-app (no custom OAuth code)
- ✅ Set external-ID fields for idempotent syncs; upsert where API supports (CRM upsert endpoint)
- ✅ Webhooks: verify signature, respond 200 fast, retry with exponential backoff
- ❌ Do not hardcode client_secret or refresh tokens in Deluge/Python files
- ❌ Do not use US API domain for an IN/EU org — token calls fail with invalid_grant

## References
- **Complete docs directory (all apps, verified links): references/docs-directory.md**
- Per-app detail files: references/crm.md, references/books.md, references/inventory.md, references/desk.md, references/people.md, references/projects.md, references/analytics.md, references/mail.md, references/flow.md, references/tables.md
- Zoho Creator + Deluge deep-dive: use the `zoho-creator` skill
- All docs root: https://www.zoho.com/developer/
