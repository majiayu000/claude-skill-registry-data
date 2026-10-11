---
name: mcae-pardot-api
description: "Use this skill when integrating with the Account Engagement (Pardot) REST API v5 to create, read, update, or query Prospects, Visitors, Visitor Activities, or Form Handlers programmatically. Trigger keywords: Pardot API, Account Engagement API, prospect sync, visitor tracking API, form handler integration, MCAE REST API. NOT for Marketing Cloud API (Email Studio, Journey Builder REST), NOT for standard Salesforce CRM REST API, NOT for MCAE setup or business unit provisioning."
category: apex
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Security
  - Performance
  - Reliability
triggers:
  - "How do I call the Pardot API from Apex or an external system to create or update a prospect record?"
  - "I need to query visitor activity records from Account Engagement using the REST API and paginate through large result sets"
  - "My API call to Account Engagement returns a 401 error even though my OAuth token is valid — what header am I missing?"
  - "How do I use a Form Handler to submit data from an external web form into Pardot without replacing our existing form"
  - "I need to look up an MCAE prospect by Salesforce Lead or Contact ID using the v5 API"
tags:
  - mcae
  - pardot
  - account-engagement
  - api-v5
  - prospects
  - visitors
  - visitor-activity
  - form-handlers
  - oauth
  - integration
inputs:
  - Salesforce Connected App client_id and client_secret for OAuth
  - Pardot Business Unit ID (found in Account Engagement Settings > Account Settings)
  - "Object to operate on: Prospect, Visitor, VisitorActivity, or FormHandler"
  - "Query filters: email address, Salesforce CRM ID, Pardot ID, or date range"
outputs:
  - Authenticated API request pattern with correct headers and base URL
  - CRUD operation examples for Prospect, Visitor, and VisitorActivity objects
  - Pagination logic using nextPageMark cursor
  - Form Handler POST target and field mapping guidance
  - Review checklist for API integration correctness
dependencies:
  - admin/mcae-pardot-setup
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-10
---

# MCAE (Pardot) API v5

This skill activates when a practitioner or AI agent needs to integrate with the Account Engagement (Pardot) REST API v5 — covering authentication setup, Prospect CRUD, Visitor and Visitor Activity queries, Form Handler configuration, and cursor-based pagination. It does not cover Marketing Cloud Email Studio or Journey Builder APIs, nor does it cover Salesforce CRM object REST APIs.

---

## Before Starting

Gather this context before working on anything in this domain:

- Confirm which API version is in use. API v3 and v4 are deprecated; all new integrations must use v5. The base URL is `https://pi.pardot.com/api/v5/objects/{object}`.
- Obtain the Pardot Business Unit ID from Account Engagement Settings > Account Settings. Every request must include the `Pardot-Business-Unit-Id` header with this value — omitting it causes 401 errors even with a valid OAuth token.
- Confirm a Salesforce Connected App is configured for OAuth. API v5 authenticates exclusively via Salesforce OAuth (SSO), not standalone Pardot credentials. The access token issued by Salesforce is passed as a `Bearer` token.
- Know which object you need: Prospects (marketing database contacts), Visitors (anonymous session records), VisitorActivities (engagement events), or FormHandlers (external form integration points).
- Understand that Prospects and Salesforce Leads/Contacts are distinct objects. CRUD on Prospects goes through the MCAE API; CRUD on Leads/Contacts goes through the Salesforce CRM REST API. The sync between them is managed by the Marketing Data Sharing rules, not the API caller.

---

## Core Concepts

### API v5 Authentication

API v5 uses the Salesforce OAuth 2.0 flow exclusively. You request a token from `https://login.salesforce.com/services/oauth2/token` (or the sandbox equivalent) using the Connected App's `client_id` and `client_secret`. The resulting `access_token` is sent as `Authorization: Bearer {token}`. Additionally, every request to `pi.pardot.com` must include the `Pardot-Business-Unit-Id` header. Missing either causes a 401. Tokens expire on the same schedule as Salesforce access tokens; implement token refresh using the `refresh_token` grant.

### Prospects

Prospects are the core marketing entity in Account Engagement. Email address must be unique per business unit — duplicate email POST requests will upsert the existing record rather than create a new one (behavior is configurable). You can query Prospects by email (`?fields=id,email&email=user@example.com`), by Salesforce CRM ID (`?crmLeadFQN=Lead/{sfId}` or `?crmContactFQN=Contact/{sfId}`), or by Pardot internal ID. CRUD is available: GET, POST (create), PATCH (update), DELETE. Field names in v5 use camelCase JSON, not underscores.

### Visitors and Visitor Activities

Visitors represent anonymous tracking sessions identified by a tracking cookie set by the Pardot tracking pixel. A Visitor record is created automatically when an anonymous user loads a page with the pixel. Once the visitor submits a form or clicks a tracked email link, the Visitor is associated with a Prospect. Visitor Activity records capture every engagement event — email opens, email clicks, form submissions, page views, file downloads, custom redirects — and are queryable per visitor or prospect. Activity types are represented as integer codes in the `type` field (e.g., 1 = email click, 4 = form submission, 6 = page view).

### Cursor-Based Pagination

API v5 does not support offset-based pagination. Instead, responses include a `nextPageMark` token in the response envelope when more pages exist. To retrieve the next page, include `?nextPageMark={value}` in the subsequent request. The response also includes `totalResults` (total matching records) and `nextPageUrl` (convenience URL). Callers must follow `nextPageMark` iteratively; jumping to arbitrary offsets is not supported.

---

## Common Patterns

### Upsert Prospect by Email

**When to use:** You have a form submission or external system event and need to ensure the prospect exists and is up to date in MCAE.

**How it works:**
1. POST to `https://pi.pardot.com/api/v5/objects/prospects` with JSON body containing `email` and any field values.
2. If a prospect with that email already exists in the BU, MCAE updates the existing record (upsert behavior).
3. Check the response `id` field to confirm which Prospect was created or updated.
4. If you need to associate with a Salesforce Lead, include `crmLeadFQN: "Lead/{sfLeadId}"` in the body.

**Why not the alternative:** Querying first to check existence, then conditionally POSTing or PATCHing, is two round trips and introduces a race condition. The POST upsert pattern is atomic and recommended by Salesforce docs.

### Paginated Visitor Activity Query

**When to use:** You need to export all engagement events for a prospect or date range, and the result set may exceed one page (default page size is 200, max is 200).

**How it works:**
1. GET `https://pi.pardot.com/api/v5/objects/visitor-activities?fields=id,type,createdAt,prospectId&prospectId={id}&orderBy=createdAt`
2. Check response body for `nextPageMark`.
3. If present, issue next GET with `?nextPageMark={value}` appended (keep all other filter params).
4. Repeat until `nextPageMark` is absent from the response.
5. Accumulate results across pages.

### Form Handler POST

**When to use:** The company has an existing web form (on their own site, in a CMS, etc.) and wants submissions to create or update MCAE Prospects without migrating to a Pardot-hosted form.

**How it works:**
1. In Account Engagement, create a Form Handler object and note its endpoint URL.
2. The external form POSTs field values to the Form Handler URL using standard HTML form encoding (`application/x-www-form-urlencoded`).
3. The Form Handler matches or creates a Prospect by email.
4. Completion actions (e.g., add to list, assign to user, send autoresponder) execute as configured on the Form Handler.
5. The Form Handler can be configured to redirect the browser to a success URL or return JSON for AJAX submissions.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Need to create or update a Prospect from backend code | POST to Prospects API v5 with JSON body | Supports all fields, returns full Prospect record, uses official API |
| External web form needs to submit into MCAE | Configure a Form Handler and POST form data to its endpoint | Designed for this use case; handles completion actions; no API credentials required in browser |
| Need all engagement history for a given Prospect | GET Visitor Activities filtered by `prospectId` with nextPageMark pagination | VisitorActivity is the canonical engagement event store |
| Need to match a Pardot Prospect to a Salesforce Lead | Query Prospect by `crmLeadFQN=Lead/{sfId}` | Avoids email-based ambiguity when multiple records exist |
| Authenticating from an external server-side system | Use Connected App OAuth Client Credentials flow | Avoids embedding user credentials; tokens can be refreshed automatically |
| Need to identify which BU a request targets | Include `Pardot-Business-Unit-Id` header on every request | Required header; missing it returns 401 regardless of token validity |

---

## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner working on this task:

1. **Gather prerequisites** — Collect the Connected App client_id/secret, the Pardot Business Unit ID, and the target object (Prospect, Visitor, VisitorActivity, or FormHandler). Confirm API v5 is being used, not a deprecated version.
2. **Obtain an OAuth access token** — POST to `https://login.salesforce.com/services/oauth2/token` with grant_type, client_id, client_secret. Extract the `access_token` from the response. Store the `refresh_token` for automated renewal.
3. **Construct the request** — Set base URL to `https://pi.pardot.com/api/v5/objects/{object}`. Add headers: `Authorization: Bearer {token}`, `Pardot-Business-Unit-Id: {buId}`, `Content-Type: application/json`. Add query params (`fields`, filters) or JSON body for mutations.
4. **Handle pagination** — For list/query operations, inspect the response for `nextPageMark`. Loop until no `nextPageMark` is present. Do not use offset parameters.
5. **Validate the response** — Check HTTP status code. 200/201 indicates success. 401 indicates missing or expired token or missing BU header. 400 indicates malformed request or field validation failure. Parse error `details` array for field-level messages.
6. **Test with a known record** — Before wiring into production flows, use a known Prospect email to verify the round trip: GET by email, PATCH a safe field, GET again to confirm the change.
7. **Review checklist** — Run through the Review Checklist below before marking the integration complete.

---

## Review Checklist

Run through these before marking work in this area complete:

- [ ] API v5 base URL used (`https://pi.pardot.com/api/v5/objects/...`), not v3 or v4
- [ ] `Pardot-Business-Unit-Id` header present on every request
- [ ] OAuth access token obtained from Salesforce (not standalone Pardot auth)
- [ ] Pagination uses `nextPageMark` cursor, not offset parameters
- [ ] Prospect email uniqueness constraint understood — POST to existing email will upsert, not create duplicate
- [ ] Visitor Activity type field interpreted as integer code, not string label
- [ ] Error responses inspected for `details` array, not just top-level message
- [ ] Token refresh logic implemented for long-running integrations

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **Missing `Pardot-Business-Unit-Id` returns 401, not 400** — The error message does not say the header is missing; it looks identical to an invalid token error. Always verify this header is present before investigating token issues.
2. **Prospect POST upserts by email silently** — Posting a new Prospect with an email that already exists in the BU does not return an error — it updates the existing Prospect. If you expected a new record, you will not detect the upsert from the status code alone; check whether the returned `id` matches an existing record.
3. **Visitor records are not directly queryable by email** — Visitors are anonymous until conversion. You cannot query `GET /visitors?email=...`. To find visits for a known Prospect, query VisitorActivities by `prospectId` instead.
4. **Deprecated v3/v4 endpoints return XML by default** — Callers migrating from older integrations may forget that v5 uses JSON (`application/json`) exclusively. v3/v4 used XML. Sending an `Accept: application/xml` header to v5 endpoints returns an error.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Authenticated API request pattern | Headers, base URL, and token acquisition flow |
| Prospect CRUD examples | Create, read, update, delete operations with sample payloads |
| Visitor Activity query | Paginated fetch of all engagement events for a Prospect |
| Form Handler configuration guide | Steps to create a Form Handler and wire an external form to it |
| Review checklist | Pre-completion verification checklist for API integrations |

---

## Related Skills

- admin/mcae-pardot-setup — Required precondition: the MCAE business unit must be provisioned and the Connected App configured before the API can be used
