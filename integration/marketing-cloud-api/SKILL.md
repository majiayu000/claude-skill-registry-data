---
name: marketing-cloud-api
description: "Use this skill when integrating Salesforce or external systems with Marketing Cloud Engagement REST or SOAP APIs — including OAuth 2.0 authentication, journey injection via /interaction/v1/events, triggered sends, and Data Extension row operations. Trigger keywords: MC API, Marketing Cloud REST, journey injection, triggered send, fire entry event, DE row upsert, dataeventsasync, Installed Package API integration. NOT for Salesforce core REST/SOAP APIs, MCAE/Pardot APIs, or Marketing Cloud Connect (CRM connector sync)."
category: apex
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Security
  - Performance
  - Reliability
triggers:
  - "how do I authenticate to the Marketing Cloud REST API using OAuth 2.0 from Salesforce Apex"
  - "my journey injection is not adding contacts even though the API returns 201"
  - "how do I fire a triggered send from Salesforce using the Marketing Cloud messaging API"
  - "what is the correct endpoint format for Marketing Cloud REST API calls"
  - "how do I bulk upsert rows into a Marketing Cloud Data Extension from Salesforce"
  - "Marketing Cloud API returns invalid_client or 401 when I try to authenticate"
  - "contacts are not entering the journey after I call the fire entry event API"
tags:
  - marketing-cloud
  - rest-api
  - soap-api
  - journey-builder
  - triggered-sends
  - data-extensions
  - oauth2
  - integration
inputs:
  - "Marketing Cloud Installed Package with API Integration component (Client ID, Client Secret, tenant-specific subdomain)"
  - "Target resource: journey EventDefinitionKey, TriggeredSend ExternalKey, or Data Extension ExternalKey"
  - "Payload schema: ContactKey field name, required journey or DE field names and types"
outputs:
  - "Working OAuth 2.0 token acquisition code (REST or Apex HTTP callout)"
  - "Journey injection request with correct eventDefinitionKey and data object structure"
  - "Triggered send sequence: create definition, start it, POST send request"
  - "Data Extension row upsert or bulk async insert with requestId polling"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-10
---

# Marketing Cloud API

Use this skill when a task involves calling Marketing Cloud Engagement REST or SOAP APIs from Salesforce Apex, external systems, or integration middleware. It covers OAuth 2.0 authentication via Installed Package credentials, injecting contacts into journeys, firing triggered sends, and upserting rows into Data Extensions. Activate it when you see references to MC API endpoints, journey fire events, or dataeventsasync in the context.

---

## Before Starting

Gather this context before working on anything in this domain:

- Confirm the Marketing Cloud org has an **Installed Package** with an **API Integration** component. This is the only supported credential source for OAuth 2.0 client credentials flow. Legacy Fuel (AppCenter) credentials are deprecated.
- Identify the **tenant-specific subdomain** (also called MID subdomain). All REST and auth endpoints use `https://{{subdomain}}.auth.marketingcloudapis.com` and `https://{{subdomain}}.rest.marketingcloudapis.com`. A generic or shared endpoint URL is wrong.
- Know which resource you are targeting: a Journey (needs EventDefinitionKey and the exact entry source field names), a Triggered Send (needs TriggeredSendDefinition ExternalKey and the send must be in Started status), or a Data Extension (needs DE ExternalKey and field names matching DE schema exactly).
- Marketing Cloud REST API has **account-level throttling**. For bulk operations over ~100 rows, prefer the async endpoint (`dataeventsasync`) to avoid rate limit errors.

---

## Core Concepts

### OAuth 2.0 Client Credentials Flow

Both the REST and SOAP Marketing Cloud APIs require an OAuth 2.0 bearer token. The token is obtained by POSTing to the tenant-specific auth endpoint:

```
POST https://{{subdomain}}.auth.marketingcloudapis.com/v2/token
Content-Type: application/json

{
  "grant_type": "client_credentials",
  "client_id": "{{clientId}}",
  "client_secret": "{{clientSecret}}"
}
```

The response contains `access_token` (a short-lived JWT, typically 20 minutes), `token_type: Bearer`, and `expires_in`. Cache the token and re-acquire only when it expires — do not request a new token for every API call. The token is then passed as `Authorization: Bearer {{access_token}}` on every subsequent request.

The Client ID and Client Secret come from the **API Integration** component inside an Installed Package in Marketing Cloud Setup. They are not Salesforce Connected App credentials.

### Journey Injection via Fire Entry Event

To inject a contact into a Journey, POST to:

```
POST https://{{subdomain}}.rest.marketingcloudapis.com/interaction/v1/events
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "ContactKey": "subscriber@example.com",
  "EventDefinitionKey": "APIEvent-abc123",
  "Data": {
    "FirstName": "Jane",
    "AccountTier": "Gold"
  }
}
```

**Critical:** The field names inside `Data` must exactly match the field names configured on the journey's entry source schema — including case. If a field name is wrong or missing, the API returns HTTP 201 (Created) but the contact is silently dropped from the journey with no error. There is no retry or error callback.

`EventDefinitionKey` is found in Journey Builder under the journey's entry source settings, not the Journey's own key. These are different values.

### Triggered Sends

Triggered sends require a three-step lifecycle:

1. **Create** a `TriggeredSendDefinition` via SOAP API or Marketing Cloud Setup UI, specifying the email, subscriber list, and ExternalKey.
2. **Start** the definition (status must be `Active` / `Running`). Sending against a definition in `Draft` status returns an error.
3. **Fire** the send via REST:
   ```
   POST https://{{subdomain}}.rest.marketingcloudapis.com/messaging/v1/messageDefinitionSends/key:{ExternalKey}/send
   ```
   with a payload containing the subscriber's `To.Address` and `To.SubscriberKey`, plus any profile attribute substitutions.

### Data Extension Row Operations

Two patterns exist for writing rows to a Data Extension:

- **Synchronous upsert** (up to ~100 rows per call, recommended for real-time use cases):
  ```
  POST /hub/v1/dataevents/key:{ExternalKey}/rowset
  ```
  Blocks until rows are committed. Returns 200 on success.

- **Asynchronous bulk insert** (preferred for > 100 rows or high-volume batch jobs):
  ```
  POST /hub/v1/dataeventsasync/key:{ExternalKey}/rowset
  ```
  Returns immediately with a `requestId`. Poll `GET /hub/v1/dataeventsasync/{requestId}` to confirm completion. Use this pattern when throughput matters more than immediate confirmation.

---

## Common Patterns

### Pattern: Apex Callout for Journey Injection

**When to use:** Salesforce Apex code needs to fire a contact into a Marketing Cloud journey after a record change (e.g., Opportunity stage change triggers onboarding journey).

**How it works:**
1. Store Client ID, Client Secret, and subdomain in a Custom Metadata Type or Named Credential (never hardcode).
2. Make an Apex `HttpRequest` to the token endpoint; parse the `access_token` from the JSON response.
3. Build the journey injection payload with the correct `EventDefinitionKey` and `Data` object using the exact field names from the entry source schema.
4. POST to `/interaction/v1/events` with the bearer token.
5. Check the HTTP response code. A 201 means the request was accepted — not that the contact entered the journey. Log the response body for debugging.

**Why not a simple callout without token caching:** Each token request counts against API call limits. In a trigger or batch context, acquiring a new token per record will exhaust limits quickly.

### Pattern: Async DE Row Upsert for Bulk Sync

**When to use:** A nightly batch or platform event processor needs to sync hundreds or thousands of Salesforce records into a Marketing Cloud Data Extension.

**How it works:**
1. Batch records into chunks of up to 2,000 rows per request (check current limit in official docs).
2. POST each chunk to `dataeventsasync` endpoint and store the returned `requestId`.
3. After all chunks are submitted, poll each `requestId` until status is `Complete` or `Error`.
4. Log errors and implement retry logic only for `Error` status responses.

**Why not the synchronous endpoint:** The sync endpoint blocks the Apex thread and can time out on large datasets. The async endpoint decouples submission from confirmation and is the documented pattern for bulk operations.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| New REST vs SOAP for new integration | Use REST API | REST is the documented preferred approach; simpler, JSON-native, broader support |
| Sending to < 100 DE rows in real-time | Sync upsert `/hub/v1/dataevents/.../rowset` | Immediate confirmation; simpler error handling |
| Sending > 100 DE rows or batch job | Async `/hub/v1/dataeventsasync/.../rowset` | Avoids throttling; decouples submission from confirmation |
| Contact must enter a Journey | POST `/interaction/v1/events` with exact field names | Journey injection is the only supported entry mechanism for API-triggered journeys |
| Sending a transactional email | Use Triggered Send via `/messaging/v1/messageDefinitionSends/...` | Designed for 1:1 transactional sends; journeys add unnecessary overhead |
| Authentication | OAuth 2.0 client credentials from Installed Package | Legacy Fuel credentials are deprecated; client credentials is the only current standard |

---

## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner working on this task:

1. **Confirm credentials and endpoints:** Retrieve the Client ID, Client Secret, and tenant-specific subdomain from the Installed Package API Integration component. Verify the subdomain format is `{{MID}}.auth.marketingcloudapis.com` — not a generic URL.
2. **Acquire an OAuth 2.0 token:** POST to the `/v2/token` endpoint with `grant_type=client_credentials`. Parse and cache `access_token` and `expires_in`. Implement token refresh logic so the token is re-acquired before expiry, not on every call.
3. **Identify the target resource:** For journeys, locate the `EventDefinitionKey` from the entry source settings (not the journey key). For triggered sends, confirm the `TriggeredSendDefinition` exists and is in `Active` status. For DEs, confirm the DE ExternalKey and retrieve the field schema.
4. **Build the request payload:** Match field names exactly to the target resource schema. For journey injection, every field in `Data` must match entry source field names case-sensitively. For DE row operations, include all required fields or upsert will fail silently.
5. **Make the API call and handle the response:** A 201 for journey injection means accepted, not confirmed entry. A `requestId` from async DE insert requires polling. Log the full response body — Marketing Cloud error messages are in the body, not always in the status code.
6. **Validate end-to-end:** In Marketing Cloud, check Journey Builder contact history or DE row count to confirm records are processed, not just accepted.

---

## Review Checklist

Run through these before marking work in this area complete:

- [ ] Credentials come from an Installed Package API Integration component — not hardcoded, not Legacy Fuel
- [ ] Token is cached and refreshed before expiry, not requested per API call
- [ ] Journey injection payload uses the EventDefinitionKey from the entry source, not the journey key
- [ ] All field names in `Data` object exactly match the entry source schema (case-sensitive)
- [ ] TriggeredSendDefinition is in Active/Started status before firing sends
- [ ] Bulk DE operations use async endpoint and poll the requestId for completion status
- [ ] API responses are logged; errors from Marketing Cloud appear in response body, not only HTTP status codes

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **Journey injection silently drops contacts on field name mismatch** — If any field name in the `Data` object does not exactly match the entry source schema (including case), the API returns HTTP 201 but the contact never enters the journey. There is no error message and no retry. This is the most common cause of "contacts not entering the journey" bugs.
2. **TriggeredSendDefinition must be Started before firing** — Creating the definition is not enough. The definition must be explicitly started (status `Active`). Firing a send against a `Draft` definition returns an error, but the error message is not always obvious that status is the cause.
3. **Tenant-specific subdomain is mandatory — generic endpoints fail** — Marketing Cloud REST API endpoints are always tenant-specific: `https://{{subdomain}}.rest.marketingcloudapis.com`. Using a generic URL or the wrong tenant subdomain results in authentication failures or 404 errors that look like network issues.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| OAuth 2.0 token acquisition snippet | Apex HttpRequest or REST client code to obtain and cache a bearer token from the MC token endpoint |
| Journey injection payload | JSON request body with EventDefinitionKey and Data object matching entry source schema |
| Triggered send sequence | Three-step setup: create definition, start it, fire the send POST request |
| DE row upsert request | Sync or async POST payload for Data Extension row operations with requestId polling for async |

---

## Related Skills

- `admin/marketing-cloud-connect` — use when configuring the CRM connector between Salesforce core and Marketing Cloud (not API-based integration)
- `integration/soap-api-patterns` — use when the integration requires SOAP API patterns in Salesforce core (not Marketing Cloud SOAP)
- `integration/oauth-flows-and-connected-apps` — use when managing OAuth flows for Salesforce core Connected Apps (not MC Installed Package credentials)
