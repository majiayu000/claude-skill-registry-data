---
name: zoho-creator
description: Zoho Creator API v2 + Deluge for app builds and automation.
version: 1.0.0
author: Hermes Agent
platforms: [windows, linux, macos]
---

# Zoho Creator (API v2 + Deluge)

Zoho Creator is a low-code app platform (forms, reports, workflows, custom functions). This skill covers REST API v2 integration and Deluge scripting for Harsh's Zoho stack (Creator + CRM + Books). Use for client app builds, data migration, automation, and AI-assisted Creator work.

## Trigger Conditions
- Build or modify a Zoho Creator app, form, report, workflow, or custom function
- Automate Creator data: create, read, update, delete records via API
- Write Deluge script (custom function, workflow, or function rule)
- Integrate Creator with Zoho CRM or Zoho Books via connections
- Migrate data into or out of Creator

## 1. Authentication (OAuth 2.0)

Server-side flow (recommended for agent automation):

```
# 1. Create self-client in Zoho Developer Console (https://api-console.zoho.com)
#    grant_type: client_credentials, scope: ZohoCreator.forms.ALL
# 2. Exchange client_id + client_secret + grant_token for tokens:
POST https://accounts.zoho.com/oauth/v2/token
  grant_type=authorization_code&code=<grant_token>&client_id=<id>&client_secret=<secret>
# 3. Refresh:
POST https://accounts.zoho.com/oauth/v2/token
  grant_type=refresh_token&refresh_token=<rt>&client_id=<id>&client_secret=<secret>
```

Pitfall: refresh tokens expire after **60 days** of non-use for self-clients (and on grant token regeneration). Store tokens outside code; never commit client_secret.

## 2. REST API v2 Base

```
Base:  https://creator.zoho.com/api/v2/{accountOwnerName}/{appLinkName}
Auth:  Authorization: Zoho-oauthtoken <access_token>
Limits: 10,000 API calls per day per account; 100 calls per 15 seconds (429 = slow down)
```

Key endpoints:

| Operation | Method + Path | Notes |
|---|---|---|
| List records | GET `/report/{reportLinkName}?limit=200&from=0` | criteria param: `criteria=Field=='value'` |
| Get record | GET `/report/{reportLinkName}/{recordId}` | |
| Create record | POST `/form/{formLinkName}` | JSON body `{"data": {"Field": "value"}}` |
| Update record | PUT `/report/{reportLinkName}/{recordId}` | |
| Delete record | DELETE `/report/{reportLinkName}/{recordId}` | |
| Upload file | POST `/form/{formLinkName}/upload_file?data={recordId}` | multipart |
| List forms/reports | GET `/forms`, GET `/reports` | |
| Call custom function | POST `/functions/{functionLinkName}/execute` | body `{"arguments": "{\"k\":\"v\"}"}` |

Response shape: `{"data": [...]}` for reports, `{"data": {...}}` for single records. Errors come as `{"data": [], "message": "..."}` with non-2xx codes.

## 3. Deluge Scripting (custom functions, workflows, function rules)

Deluge runs server-side in Creator. Patterns Harsh uses daily:

```javascript
// Query records with criteria
records = zoho.creator.getRecords("applink", "reportlink", "criteria", 200, 0);

// Create record (maps to a form)
record = zoho.creator.createRecord("applink", "formlink", {"Field": value, "Owner.Id": 123});

// Update record
zoho.creator.updateRecord("applink", "reportlink", recordId, {"Field": newValue});

// Delete record
zoho.creator.deleteRecord("applink", "reportlink", recordId);

// HTTP to external APIs (LLM, webhook, anything)
resp = invokeurl
[
    url: "https://api.openai.com/v1/chat/completions"
    type: POST
    headers: {"Authorization": "Bearer <key>"}
    body: "{\"model\":\"gpt-4o-mini\",\"messages\":[{\"role\":\"user\",\"content\":\"x\"}]}"
];
// Parse: info = resp.get("choices").get(0).get("message").get("content")

// Response builder for API invocation
response = {"success": true, "data": records};
```

Errors: use `try-catch` blocks; Deluge throws exceptions that surface as HTTP 500 in executed functions.

## 4. Connections (Creator to CRM / Books)

Use Creator's built-in **Connections** (Authorization > Connections) instead of raw OAuth:

```
// Zoho CRM connection
leads = zoho.crm.getRecords("Leads", "criteria", 200, 0);
zoho.crm.create("Deals", {"Deal_Name": "x", "Amount": 1000});

// Zoho Books connection
invoice = zoho.books.create("SalesInvoices", orgId, {"customer_id": "x", "line_items": [...]});
zoho.books.get("Invoices", orgId, "criteria");
```

Connection names are set in the app's connection settings. This is the maintainable path: reuses one authorized connection per app, no token handling in scripts.

## 5. Deploy (sandbox vs production)

- `https://creator.zoho.com/api/v2/...` routes to the **live/production** app data
- Sandbox/test apps use the sandbox link name and `sandbox=true` deployments
- Custom functions must be **deployed** to production (Publish > Deploy) before they respond via API; API-invoked functions can also be exposed via **API invocation settings** with generated auth tokens per function

## 6. Pitfalls

- ❌ 429 throttling: batch inserts in chunks of 50-100 with pauses
- ❌ Never hardcode OAuth tokens in Deluge (use connections or secure variables)
- ❌ `zoho.creator.getRecords` returns max 200 per call - paginate with from offset
- ❌ Field API names are the internal names, not display labels (check app > form > fields > API Name)
- ❌ Date fields: pass ISO `yyyy-MM-dd` strings; datetime needs timezone care
- ✅ Verify in sandbox app first, then deploy; test every custom function via "Run" button before wiring workflows
- ✅ Use `invokeurl` for LLM APIs - this is Harsh's Zoho + AI differentiator pattern
- ✅ Always confirm app link names, form/report link names, and field API names from the actual app before writing scripts

## References
- API v2 docs: https://www.zoho.com/creator/help/api/v2/ (and https://www.zoho.com/creator/help/api/v2/get-records.html)
- Deluge reference: https://www.zoho.com/deluge/help/
- Complete Zoho docs directory (all apps, verified links): load `zoho-api` skill, file references/docs-directory.md
- Harsh's context: Zoho Creator + CRM + Books + AI is the primary market differentiator (AGENTS.md)
