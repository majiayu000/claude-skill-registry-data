---
name: commerce-order-api
description: "Use this skill when building or debugging headless B2C Commerce storefront order submission using the Salesforce Commerce API (SCAPI) ShopAPI Orders endpoint or the legacy OCAPI /orders resource. Covers SCAPI order creation, SLAS authentication for shopper order access, OCAPI order placement and amendment, order status retrieval from the storefront layer, and notification/webhook configuration for order events. NOT for standard REST API (no generic CRUD against Order SObject). NOT for OMS Connect API (no OrderSummary, FulfillmentOrder, submit-cancel, or ensure-funds-async — those are covered by admin/commerce-order-management). NOT for CPQ order workflows."
category: apex
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Security
  - Reliability
  - Performance
triggers:
  - "How do I submit an order from a headless B2C Commerce storefront using the Salesforce Commerce API?"
  - "SCAPI ShopAPI order creation is returning a 401 or token error — how do I authenticate shoppers for order placement?"
  - "What is the difference between SCAPI and OCAPI for placing orders from a headless storefront?"
  - "How do I retrieve order status and order history for a logged-in shopper via the Commerce API?"
  - "OCAPI /orders endpoint is being deprecated — how do I migrate headless order submission to SCAPI?"
  - "How do I configure order confirmation webhooks or notification hooks in B2C Commerce headless?"
tags:
  - b2c-commerce
  - scapi
  - ocapi
  - headless-storefront
  - shopper-orders
  - slas
  - order-submission
  - commerce-api
inputs:
  - "B2C Commerce Cloud org with Salesforce B2C Commerce license and a configured storefront site"
  - "SLAS (Shopper Login and API Access Service) client configuration (client ID, redirect URI, scopes) for shopper authentication"
  - "Active shopper basket containing product line items, a shipping method, and a payment instrument before order creation"
  - "OCAPI Shop API settings (if using legacy path): allowed origins, resource access configurations, client permissions"
  - "Order notification target: webhook endpoint URL or Salesforce Platform Event / Flow to receive order events"
outputs:
  - "Order object returned by SCAPI POST /checkout/shopper-orders/v1/organizations/{organizationId}/orders with orderNo, status, and payment details"
  - "SLAS access token and refresh token flow suitable for authenticated (registered) or guest shopper order submission"
  - "Decision table: SCAPI ShopAPI Orders vs OCAPI /orders — which to use, key behavioral differences, migration path"
  - "Notification/webhook configuration for order confirmation and order status change events from B2C Commerce"
  - "Apex or external service callout patterns for reading B2C Commerce order data into Salesforce core from headless storefronts"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-12
---

# Commerce Order API (SCAPI / OCAPI — Headless Storefront)

This skill activates when a practitioner needs to submit, retrieve, or manage orders from a headless B2C Commerce storefront using the Salesforce Commerce API (SCAPI) or its predecessor OCAPI. It covers the shopper-facing API layer: authenticating shoppers via SLAS, placing orders against an active basket, retrieving order status and history, and wiring order notifications. It does NOT cover the OMS Connect API layer (OrderSummary, FulfillmentOrder, submit-cancel, ensure-funds-async) — that is handled by `admin/commerce-order-management`.

---

## Before Starting

Gather this context before working on anything in this domain:

- Confirm whether the project is on SCAPI (modern, recommended) or OCAPI (legacy). OCAPI's Shop API is in maintenance mode as of Spring '24 and Salesforce has signaled eventual deprecation. New integrations must use SCAPI.
- Confirm SLAS is configured: a SLAS client must exist in Account Manager with the correct scopes (`sfcc.shopper-baskets-orders`, `sfcc.shopper-myaccount.order`) and redirect URIs registered before any order API call will succeed. Missing scopes produce silent 403 errors, not descriptive messages.
- Verify the shopper has an active basket with a valid shipping address, shipping method, and at least one payment instrument before calling the orders endpoint — the API will reject the order creation if the basket is incomplete, but the error responses can be generic.
- The SCAPI Orders endpoint consumes and deletes the basket in a single call. Once `POST /orders` returns 200, the basket is gone. There is no rollback of a successfully submitted order through the shopper API; amendments require either the OMS layer or OCAPI order amendment resources.
- Know whether shoppers are guest (anonymous) or registered (authenticated): SLAS guest tokens can place orders, but order history retrieval (`GET /orders`) requires a registered shopper token. Guest order lookup uses order number + email, not a shopper session.

---

## Core Concepts

### SCAPI ShopAPI Orders — The Modern Path

The Salesforce Commerce API (SCAPI) ShopAPI Orders resource is the current standard for headless order submission:

- **Endpoint**: `POST /checkout/shopper-orders/v1/organizations/{organizationId}/orders`
- **Auth**: SLAS Bearer token in the `Authorization` header. Guest shoppers use a SLAS guest token; registered shoppers use a SLAS registered (JWT) token obtained via PKCE or client credentials flow.
- **Input state**: The request body contains only `{"basketId": "<uuid>"}`. The shopper must have previously built a basket via the Shopper Baskets API. All product, price, shipping, and payment data is read from the basket at submit time.
- **Output**: A full Order representation including `orderNo`, `status` (`created`), `payment_status`, `confirmation_status`, line items, shipments, and applied promotions. The basket is atomically deleted.
- **Idempotency**: SCAPI orders are NOT idempotent. Retrying a `POST /orders` after a network timeout can create a duplicate order if the first call succeeded. Implement client-side order submission deduplication using a client-generated basket ID check before retrying.

**SLAS Scopes for Orders**:

| Operation | Required Scope |
|---|---|
| Place order (guest or registered) | `sfcc.shopper-baskets-orders` |
| Get order details | `sfcc.shopper-baskets-orders` |
| Get shopper order history | `sfcc.shopper-myaccount.order` |
| Guest order lookup (by email + orderNo) | `sfcc.shopper-orders` (public client) |

### OCAPI Shop API Orders — The Legacy Path

OCAPI (`/s/{site-id}/dw/shop/v23_2/orders`) remains available for existing integrations but is in maintenance mode. Key behavioral differences from SCAPI:

- Auth uses OCAPI client ID + HMAC or OAuth 2.0, not SLAS. OCAPI client IDs are configured per-site in Business Manager under Administration > Site Development > OCAPI Settings.
- OCAPI orders support POST (create), GET (retrieve), and PATCH (amend). SCAPI's ShopAPI does not expose an amendment endpoint — post-submission changes go through OMS.
- OCAPI returns `customer_info`, `billing_address`, and `shipments` in the same response structure but with underscore-delimited keys vs SCAPI's camelCase.
- Order amendment via OCAPI PATCH is possible for status updates within certain lifecycle states, but this is being phased out in favor of OMS Connect API actions.
- **Do not start new integrations on OCAPI.** SCAPI is the strategic path.

### SLAS Authentication for Order Submission

SLAS (Shopper Login and API Access Service) is mandatory for SCAPI order submission. It is hosted separately from the core Salesforce platform and operates through Account Manager:

- **Guest flow**: `POST /shopper/auth/v1/organizations/{organizationId}/oauth2/guest/token` — Returns a short-lived access token usable for basket creation and order submission. Guest tokens cannot access order history.
- **Registered flow (PKCE)**: Authorization Code + PKCE with `redirect_uri` in the browser. After the shopper logs in, exchange the code for tokens. The access token carries the shopper's `customer_id` and enables order history.
- **Token refresh**: Both guest and registered tokens have configurable TTLs (default 30 min / 7 day refresh). Implement token refresh before expiry; SCAPI returns 401 with `invalid_token` when expired.
- **Trusted agent flow**: For server-side integrations (e.g., Apex callouts reading shopper orders into Salesforce core), use the SLAS Trusted Agent flow with a private client and a `sfcc.shopper-baskets-orders.rw` scope. This avoids requiring a browser-based PKCE flow in backend systems.

### Order Status and Notifications

B2C Commerce headless does not push order status changes via native Salesforce Platform Events. Order status notifications use one of two mechanisms:

1. **B2C Commerce Hooks** (`dw.system.HookMgr`): A custom cartridge can register a hook on `dw.order.afterOrderCreated` or `dw.order.afterOrderStatusChange`. The hook script runs server-side in the Commerce Cloud cartridge layer and can fire an HTTP callout to an external webhook or a Salesforce Experience Cloud endpoint.
2. **Order Management Platform Events** (after OMS integration): Once a B2C order is ingested into OMS as an OrderSummary, `OrderSummaryCreatedEvent`, `FOStatusChangedEvent`, and `OrderSumStatusChangedEvent` platform events carry status changes back to Salesforce core. This requires the OMS integration layer and is described in `admin/commerce-order-management`.

For pure headless storefronts without OMS, polling `GET /orders/{orderNo}` is the fallback for order status — it is not a webhook model.

---

## Common Patterns

### Pattern: Guest Shopper Order Submission via SCAPI

**When to use:** A headless storefront (React, Vue, mobile) needs to place an order for an anonymous/guest shopper.

**How it works:**

1. Obtain a SLAS guest token:
   ```
   POST https://{shortCode}.api.commercecloud.salesforce.com/shopper/auth/v1/organizations/{organizationId}/oauth2/guest/token
   Body: grant_type=client_credentials&client_id={publicClientId}
   ```
2. Create a basket via Shopper Baskets API (`POST /baskets`). Add product line items, set shipping address and method, add payment instrument.
3. Submit the order:
   ```
   POST /checkout/shopper-orders/v1/organizations/{organizationId}/orders
   Authorization: Bearer {slasGuestToken}
   Body: {"basketId": "{basketId}"}
   ```
4. Parse the response `orderNo` and `status`. Store `orderNo` in local state — it is the only future lookup key for guest shoppers.
5. Trigger confirmation email via cartridge hook or external service using `orderNo`.

**Why not the alternative:** Using OCAPI for new guest order placement requires configuring OCAPI client settings in Business Manager per-site and does not benefit from SLAS centralized token management or the newer Commerce API rate-limiting and observability tooling.

### Pattern: Registered Shopper Order History Retrieval

**When to use:** A logged-in shopper views their order history in a headless My Account page.

**How it works:**

1. Obtain a SLAS registered token for the shopper (PKCE flow or session-based via trusted agent).
2. Call:
   ```
   GET /checkout/shopper-orders/v1/organizations/{organizationId}/orders?offset=0&limit=10
   Authorization: Bearer {registeredToken}
   ```
3. The response is paginated. Use `total`, `offset`, and `limit` in the response envelope for pagination. Filter by `status` query param if needed (`created`, `new`, `open`, `completed`, `cancelled`).
4. For order detail, call `GET /orders/{orderNo}` with the same registered token.

**Why not the alternative:** Guest tokens cannot access `GET /orders` — the API returns 403. Attempting to look up a registered shopper's order history with a guest token is the most common auth mistake in headless implementations.

### Pattern: Apex Callout to Read B2C Order Data into Salesforce Core

**When to use:** A Salesforce core org needs to read order data from B2C Commerce (e.g., to display recent orders in Service Console) without OMS integration.

**How it works:**

1. Use the SLAS Trusted Agent flow in Apex to obtain a server-side access token (no browser required):
   ```apex
   HttpRequest req = new HttpRequest();
   req.setEndpoint('callout:SLAS_Endpoint/shopper/auth/v1/organizations/{orgId}/oauth2/token');
   req.setMethod('POST');
   req.setBody('grant_type=client_credentials&client_id={privateClientId}&client_secret={secret}');
   ```
2. Store the token in a custom setting or Platform Cache (not in a field on a record — avoid token persistence in audit-visible storage).
3. Use the token in a subsequent callout to `GET /orders/{orderNo}` or `GET /orders` and map the response to a Salesforce object or LWC display component.

**Why not the alternative:** Hardcoding an OCAPI client secret in Apex Named Credentials or Custom Metadata without rotating expiry logic creates a credential exposure risk and makes the integration fragile when OCAPI clients are regenerated in Business Manager.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| New headless storefront, order submission | SCAPI ShopAPI Orders + SLAS | Strategic API; modern token management; no per-site OCAPI configuration required |
| Existing OCAPI integration, maintenance mode | Keep OCAPI until migration window; plan SCAPI migration | OCAPI is not yet sunset, but no new features; plan migration per Salesforce roadmap |
| Guest shopper order placement | SLAS guest token + SCAPI POST /orders | Guest tokens work; registered token not required for submission |
| Registered shopper order history | SLAS registered token (PKCE) + SCAPI GET /orders | Guest tokens cannot access order history; registered token is mandatory |
| Order amendments after submission | OMS Connect API (admin/commerce-order-management) | SCAPI ShopAPI has no amendment endpoint; all post-submission changes go through OMS |
| Order confirmation email | B2C Commerce Hook (dw.order.afterOrderCreated) | Runs in cartridge layer at order creation time; native to Commerce Cloud |
| Reading B2C order data into Salesforce core | SLAS Trusted Agent + Apex callout | Avoids browser PKCE in server-side context; secure client credentials flow |
| Order status webhooks without OMS | B2C Hooks + external HTTP callout | Commerce Cloud has no native push webhook; hooks fire server-side callouts |

---

## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner working on this task:

1. **Confirm API path (SCAPI vs OCAPI)**: Determine whether this is a new integration (use SCAPI) or a maintained legacy integration (OCAPI). For SCAPI, confirm the org's `shortCode` and `organizationId` from the Commerce Cloud Business Manager (Administration > Salesforce Commerce API Settings). For OCAPI, locate the site-level OCAPI Shop API settings in Business Manager.
2. **Configure SLAS**: In Account Manager, verify a SLAS client exists with `sfcc.shopper-baskets-orders` scope and the storefront's redirect URI. For server-side Apex callouts, configure a private SLAS client and store credentials in Salesforce Named Credentials — never in Apex source or Custom Metadata readable by all profiles.
3. **Implement the basket-to-order flow**: Build the shopper basket using the Shopper Baskets API before calling the Orders endpoint. Validate the basket is complete (shipping address, shipping method, payment instrument) before submission. The Orders endpoint will reject an incomplete basket with a 400 error.
4. **Submit the order and handle the response**: Call `POST /checkout/shopper-orders/v1/.../orders` with the `basketId`. Parse `orderNo` and `status` from the response. Implement client-side deduplication: do not retry a POST /orders without first confirming via `GET /orders/{orderNo}` that the order does not already exist.
5. **Wire notifications**: Implement a B2C Commerce cartridge hook on `dw.order.afterOrderCreated` for immediate post-submission notifications. For status change notifications, implement a hook on `dw.order.afterOrderStatusChange` or integrate with OMS platform events if the org uses OMS.
6. **Test authentication edge cases**: Verify that expired SLAS tokens return 401 and the client refreshes correctly. Test guest shopper order lookup using `orderNo` + email (not session token). Test that registered shopper order history returns correct results and pagination works at the 10-record boundary.
7. **Review security posture**: Confirm SLAS client secrets are not exposed in browser-accessible JavaScript (use private SLAS clients only in server-side code). Confirm Named Credentials are used for Apex callouts. Confirm OCAPI allowed-origins whitelist is restricted to known storefront domains if OCAPI is in use.

---

## Review Checklist

Run through these before marking work in this area complete:

- [ ] SLAS client is configured in Account Manager with correct scopes and redirect URIs
- [ ] SCAPI organization ID and short code are confirmed from Business Manager
- [ ] Order submission uses basket-first flow — basket is complete before POST /orders is called
- [ ] Client-side deduplication is implemented for POST /orders retries
- [ ] SLAS client secrets are stored in Named Credentials or equivalent — not in Apex literals or Custom Metadata accessible to all profiles
- [ ] Guest vs registered token usage is correct: guest for submission, registered for order history
- [ ] Order notification mechanism is in place (B2C hook or OMS platform events)
- [ ] If OCAPI: OCAPI allowed-origins is restricted to known domains; no wildcard origins in production

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **POST /orders is not idempotent and basket is destroyed on success** — A network timeout during order submission leaves the client uncertain: did the order succeed? The basket is deleted on success. Retrying POST /orders creates a duplicate order. The safe recovery pattern is to call `GET /orders?basketId={basketId}` (OCAPI) or check order history by other means before retrying. Design the storefront to show a "checking order status" state before offering a retry button.
2. **SLAS scope mismatches produce 403 with no useful error body** — If the SLAS client lacks `sfcc.shopper-baskets-orders`, the orders endpoint returns a 403 with a generic payload. Business Manager does not surface scope errors in request logs by default. Always verify scopes in Account Manager before debugging storefront code.
3. **Guest tokens cannot retrieve order history — 403, not 401** — Developers often mistake a guest-authenticated `GET /orders` 403 for a token expiry or scope issue. The distinction matters: 401 means re-authenticate; 403 means the token is valid but lacks privilege. For guest order lookup, use the OCAPI `GET /orders/{orderNo}?guest_email={email}` pattern or implement a dedicated guest order lookup endpoint.
4. **OCAPI and SCAPI use different key casing conventions** — OCAPI response keys are `snake_case` (`customer_info`, `billing_address`); SCAPI response keys are `camelCase` (`customerInfo`, `billingAddress`). Code that handles both APIs without an adapter layer will produce silent null-reference bugs in JavaScript when the casing assumption is wrong.
5. **SCAPI has no order amendment endpoint — amendments require OMS** — After a SCAPI order is submitted, the ShopAPI has no `PATCH /orders/{orderNo}` equivalent. Any quantity change, address correction, or cancellation requires either the OMS Connect API actions (if OMS is integrated) or a custom cartridge solution with direct business object access. Teams that discover this limitation post-launch often attempt direct DML against OMS objects, which corrupts financial aggregates in MANAGED mode.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| SCAPI order submission response | JSON with orderNo, status, paymentStatus, confirmationStatus, lineItems, shipments |
| SLAS token configuration | Account Manager client configuration with scopes for guest and registered order flows |
| B2C Commerce hook registration | Cartridge hook script wired to dw.order.afterOrderCreated for order notifications |
| Order history API response | Paginated list of order summaries for registered shoppers via GET /orders |
| Named Credential configuration | Salesforce Named Credential for Apex callout to SCAPI with SLAS Trusted Agent auth |

---

## Related Skills

- `admin/commerce-order-management` — Use for OMS-layer order processing: OrderSummary, FulfillmentOrder, submit-cancel, ensure-funds-async, and OMS platform events. This is the post-submission layer after a SCAPI order is ingested into Salesforce OMS.
- `lwc/commerce-lwc-components` — Use for building LWC checkout and My Account components that call SCAPI via the wire service or imperative Apex.
- `apex/external-service-callout` — Use for Apex HTTP callout patterns to external APIs including SCAPI and SLAS token management.

---

## Official Sources Used

- Salesforce Commerce API (SCAPI) ShopAPI Orders — https://developer.salesforce.com/docs/commerce/salesforce-commerce/guide/ShopperOrders.html
- SLAS (Shopper Login and API Access Service) Developer Guide — https://developer.salesforce.com/docs/commerce/salesforce-commerce/guide/slas.html
- OCAPI Shop API Orders Resource — https://developer.salesforce.com/docs/commerce/b2c-commerce/references/ocapi-shop-api?meta=Orders
- Salesforce Well-Architected Overview — https://architect.salesforce.com/docs/architect/well-architected/guide/overview.html
- B2C Commerce Hooks Reference — https://developer.salesforce.com/docs/commerce/b2c-commerce/references/b2c-commerce-hooks-reference?meta=Summary
