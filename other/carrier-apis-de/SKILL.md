---
name: carrier-apis-de
description: "Integrate German carrier APIs (DHL, DPD, GLS, Hermes, UPS) for Ottili flows: create idempotent labels, track via official APIs only and reconcile label costs. Use when an agent must create a shipping label, track a shipment, or reconcile carrier API responses. Not for general shipping logic or unofficial tracking scrapers."
license: MIT-compat
compatibility: "framework-agnostic; German carrier REST/XML/SOAP APIs; offline validation"
metadata: {}
allowed-tools: []
---

# carrier-apis-de

## When to use this skill

Use this skill when an agent must talk to a German carrier API
(DHL, DPD, GLS, Hermes, UPS) for Ottili flows: create a shipping
label, track a shipment, or reconcile label cost and status against
the Ottili shipping record. Do **not** use it for general shipping logic
(packing, routing, address validation) or for unofficial tracking
scrapers — every carrier here has an official API and a contract.

## Procedure (numbered, in order)

1. **Identify the carrier and its contract model.** Each carrier has a
   different auth and API shape; never assume one fits another. Read the
   per-carrier row from the contract table in `references/procedures.md`.
2. **Authenticate with the carrier's documented flow** (OAuth2 client
   credentials or token exchange). Cache the token, refresh at least 60 s
   before expiry, never hardcode credentials and never log the token.
3. **Create an idempotent label.** Every label request carries a
   client-generated idempotency key (your stable order/shipment reference).
   On a duplicate key the carrier hands back the label that already exists —
   never mint a second one. The key field name differs per carrier; read it
   from `config/versions.json`, never hardcode.
4. **Track via the official API only.** Poll the carrier's tracking
   endpoint, cache results for 5 minutes (pinned), never scrape the public
   page.
5. **Reconcile.** Compare label cost, status and tracking number against
   the Ottili shipping record. On a mismatch or unknown result re-query by
   tracking number, log the delta, flag for review. Exit 0 = match,
   1 = mismatch/unknown, 2 = malformed input.
6. **Handle errors via the fix table.** Map carrier status codes to a
   concrete fix. Auth errors (401/403) are never retried with the same
   token; 409 means re-query, never re-create; 429/5xx use bounded
   exponential backoff (base 500 ms, factor 2, max 3 attempts, cap 30 s).

## Decision tables

### Carrier contract model (condensed)

| Carrier | Transport | Credentials | Key placement | Test env. |
|---|---|---|---|---|
| DHL Parcel DE | REST v3 | OAuth2 client credentials | header `X-Request-ID` | sandbox |
| DPD Germany | XML/JSON | API key + DPD-Auth token | body field | sandbox |
| GLS Germany | SOAP/REST | API key + secret | body `labelId` | none public |
| Hermes Germany | REST | OAuth2 / API key | body `correlationId` | account needed |
| UPS Germany | REST | OAuth2 client credentials | header `X-Inbound-Idempotency-Key` | sandbox (CIM) |

### Label error → fix

| Carrier status | Meaning | Fix |
|---|---|---|
| 401 / 403 | Auth failure | Re-issue token; never retry with the same token |
| 409 | Conflict / duplicate key | Re-query by reference; never re-create |
| 422 | Validation error | Fix the field named in the response body |
| 429 | Rate limited | Exponential backoff, up to 3 attempts |
| 5xx | Carrier outage | Retry with backoff; mark the label unknown |

## Worked examples

### Good output — idempotent DHL label, first request
Input: `POST /v3/shipping/labels` with header `X-Request-ID: <uuid>`,
body `{shipmentId: "SPR001", product: "Paket"}`. First call returns
201 + label PDF + tracking number `JJD123456789DE`.
Expected behaviour: label stored with the client-generated `X-Request-ID`,
cost reconciled against the Ottili shipping record. `scripts/label_create.py`
exits 0.

### Bad output — duplicate label request with the same key
Input: the same request is sent again (network retry, same `X-Request-ID`).
Expected behaviour: DHL returns 200 with the **existing** label, not a new one.
`scripts/reconcile.py` exits 0 with `duplicate_key: returned existing label`.
If the agent had re-created the label, the Ottili record would carry two
label costs for one shipment.

### Bad output — 409 treated as "create again"
Input: a DPD label request returns 409 with a `labelId` in the body.
`scripts/label_create.py` exits 1 with:
`FAIL: 409 conflict — re-query by reference, never re-create`
Fix: call the query endpoint with the reference; the existing label comes
back. Re-creating produces a second label and a double charge.

### Good output — tracking via official API, cached
Input: `GET /v3/tracking?id=JJD123456789DE` returns `status: delivered`.
Expected behaviour: result cached for 5 minutes (pinned TTL); subsequent
requests within the window hit the cache and do not call the carrier.
`scripts/track.py` exits 0.

### Bad output — tracking scraped from the web page
Input: the agent fetches `https://www.dhl.com/track` and regexes the HTML.
`scripts/track.py` exits 2 with:
`FAIL: tracking must use the official endpoint, never a web page scrape`
Fix: use the tracking API. Scraping breaks on layout changes and violates
the carrier's terms; the data is also unverified for GoBD purposes.

## Pitfalls from research

- **Idempotency key names differ per carrier.** DHL and UPS put the key in
  a request header (`X-Request-ID`, `X-Inbound-Idempotency-Key`); DPD, GLS
  and Hermes embed it in the request body. Abstract the key behind a
  per-carrier adapter; never assume one header name.
- **A duplicate key does not always mean "return existing".** Some carriers
  return 409 and you must re-query by the reference number to find the
  existing label. Treat 409 as "re-query, never re-create".
- **Never scrape the tracking page.** Every carrier has an official tracking
  API; scraping breaks on layout changes and violates the carrier's terms.
- **Sandbox availability is uneven.** DHL, DPD and UPS provide sandboxes;
  GLS and Hermes do not, and Hermes needs a business account. When no
  sandbox exists, dry-run the request envelope instead — that path is fully
  offline and exercises the same adapter code.
- **Label cost reconciliation is not optional.** A label that was created but
  never reconciled silently diverges from the Ottili shipping record.
- **DPD and GLS portals are SPAs.** Deeper paths (`/track`, `/api`,
  `developer-portal`) 404 while the root 200s; the real contracts live behind
  login. Mark those endpoint paths as unverified.

## Verification checklist

- [ ] Carrier and contract model identified
- [ ] Auth token cached and refreshed before expiry
- [ ] Idempotency key present and client-generated
- [ ] Duplicate key returns the existing label (or 409 → re-query)
- [ ] Tracking uses the official endpoint, never a web page
- [ ] Results cached; no hammering
- [ ] Label cost/status reconciled with Ottili shipping record
- [ ] Error codes mapped to the fix table; auth errors never retried

## Near-miss triggers (stop and re-read)

- "I'll just retry the label request" → check the idempotency key first.
- "The tracking page shows..." → that is not a data source; use the API.
- "It worked once, so the key doesn't matter" → it matters on every retry.
- "GLS/Hermes have no sandbox, skip testing" → dry-run the envelope instead.
- "The tracking number looks odd" → reject non-numeric before any request.


## Related skills

[bank-reconciliation-camt](../bank-reconciliation-camt/) — label and transit costs are reconciled against the camt.053 statement
[webhooks-safe](../webhooks-safe/) — carrier webhook events need signature verification, dedupe and dead-letter
[gobd-archive](../gobd-archive/) — label and tracking records are vouchers (8y)

## References

- [Procedures, worked examples and carrier API summaries](references/procedures.md)
- [Standards and sources](references/SOURCES.md)
- [EVALS](references/EVALS.md)
- [Scripts](scripts/)
