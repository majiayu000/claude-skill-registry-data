---
name: ampeco-public-api
description: |
  Explore AMPECO Public API endpoints, schemas, and develop integrations
  with the EV charging platform. Use for API exploration, building
  integrations, or understanding available endpoints.
  Trigger keywords: "ampeco api", "public api", "ev charging api", "ampeco integration"
allowed-tools: Read, Glob, Grep, Bash, WebFetch
---

# AMPECO Public API Integration Guide

Explore and integrate with the AMPECO EV Charging Platform Public API.

---

## IMPORTANT: Update Reference Docs First

Before using the reference documentation, ensure you have the latest API spec:

```bash
bash scripts/fetch-and-generate.sh
```

This fetches the latest OpenAPI spec from https://developers.ampeco.com/openapi/ and regenerates all reference files.

**Prerequisites**: `curl` and `jq` must be installed:
- macOS: `brew install jq`
- Ubuntu/Debian: `apt-get install jq`

---

## Getting Started

### 1. Get API Access

Contact your AMPECO Customer Success Manager or generate a token in:
**Back Office → API Access Tokens**

### 2. Base URL

```
https://{tenantUrl}/public-api/
```

Replace `{tenantUrl}` with your organization's tenant URL.

### 3. Authentication

```bash
curl -H "Authorization: Bearer {your-api-token}" \
     https://{tenantUrl}/public-api/resources/charge-points/v2.0/
```

---

## Quick Reference

**Response Format**: JSON with `data` wrapper
```json
{
  "data": [...],
  "links": { "first": "...", "last": "...", "prev": null, "next": "..." },
  "meta": { "current_page": 1, "per_page": 100, "total": 250 }
}
```

**Path Patterns**:
- Resources: `/public-api/resources/{resource-name}/v{X.Y}/`
- Actions: `/public-api/actions/{target}/v{X.Y}/{id}/{action}`
- Notifications: `/public-api/notifications/v{X.Y}/`

---

<!-- BEGIN:QUICK_INDEX -->
## Endpoint Quick Index

| Resource | Version | Operations |
|----------|---------|------------|
| **Authorizations** | v1.0, 2.0 | Read |
| **Booking Requests** | v1.0 | Create, Read |
| **Bookings** | v1.0 | Read |
| **Cdrs** | v2.0 | Read |
| **Charge Point Downtime Periods** | v1.0 | Create, Delete, Read, Update |
| **Charge Point Models** | v1.0 | Create, Delete, Read, Update |
| **Charge Point Vendors** | v1.0 | Create, Delete, Read, Update |
| **Charge Points** | v1.0, 2.0 | Create, Delete, Read, Update |
| **Circuits** | v1.0, 2.0 | Create, Delete, Read, Update |
| **Configuration Templates** | v1.0 | Create, Delete, Read, Update |
| **Consents** | v1.0 | Create, Read |
| **Contact Details** | v2.0 | Delete, Read, Update |
| **Cp Models** | v1.0 | Create, Delete, Read, Update |
| **Cp Vendors** | v1.0 | Create, Delete, Read, Update |
| **Currencies** | v2.0 | Create, Delete, Read, Update |
| **Currency Rates** | v1.0 | Create, Delete, Read, Update |
| **Custom Fees** | v2.0 | Read |
| **Downtime Period Notices** | v1.0 | Create, Delete, Read, Update |
| **Electricity Meters** | v1.0 | Create, Delete, Read, Update |
| **Electricity Rates** | v1.0, 2.0 | Create, Delete, Read, Update |
| **Evse Downtime Periods** | v1.0 | Create, Delete, Read, Update |
| **Evses** | v2.0, 2.1 | Create, Delete, Read, Update |
| **Faqs** | v2.0 | Create, Delete, Read, Update |
| **Firmware Versions** | v1.0 | Read |
| **Flexibility Activation Requests** | v1.0 | Read |
| **Flexibility Assets** | v1.0 | Create, Delete, Read, Update |
| **Id Tags** | v2.0 | Create, Delete, Read, Update |
| **Installer Jobs** | v1.0 | Create, Delete, Read, Update |
| **Invoices** | v1.0 | Read |
| **Locations** | v1.0, 2.0 | Create, Delete, Read, Update |
| **Parking Spaces** | v1.0 | Create, Delete, Read, Update |
| **Partner Contracts** | v1.0 | Create, Delete, Read, Update |
| **Partner Expenses** | v1.0, 1.1 | Read |
| **Partner Invites** | v1.0 | Create, Delete, Read, Update |
| **Partner Revenues** | v1.0, 1.1 | Read |
| **Partner Settlement Reports** | v1.0 | Create, Delete, Read, Update |
| **Partners** | v1.0, 2.0 | Create, Delete, Read, Update |
| **Payment Terminals** | v1.0 | Create, Delete, Read, Update |
| **Provisioning Certificates** | v2.0 | Create, Delete, Read, Update |
| **Receipts** | v2.0 | Read |
| **Reservations** | v1.0 | Read |
| **Rfid Tags** | v1.0 | Create, Delete, Read, Update |
| **Roaming Connections** | v2.0 | Read |
| **Roaming Operators** | v2.0 | Create, Delete, Read, Update |
| **Roaming Platforms** | v1.0 | Read |
| **Roaming Providers** | v2.0 | Create, Delete, Read, Update |
| **Roaming Tariffs** | v2.0 | Read, Update |
| **Security Events** | v2.0 | Read |
| **Security Events Log** | v2.0 | Read |
| **Sessions** | v1.0 | Read |
| **Settings** | v1.0 | Read |
| **Sub Operators** | v1.0 | Read |
| **Subscription Plans** | v1.0, 2.0 | Create, Delete, Read, Update |
| **Subscriptions** | v1.0 | Read |
| **Tariff Groups** | v1.0 | Create, Delete, Read, Update |
| **Tariff Snapshots** | v1.0 | Read |
| **Tariffs** | v1.0 | Create, Delete, Read, Update |
| **Tax Identification Numbers** | v2.0 | Create, Delete, Read, Update |
| **Taxes** | v2.0 | Create, Delete, Read, Update |
| **Templates** | v1.0 | Read |
| **Terms And Policies** | v2.0 | Read |
| **Top Up Packages** | v2.0 | Create, Delete, Read, Update |
| **Transactions** | v1.0 | Create, Read, Update |
| **User Groups** | v1.0 | Create, Delete, Read, Update |
| **Users** | v1.0 | Create, Delete, Read, Update |
| **Utilities** | v1.0 | Create, Delete, Read, Update |
| **Vendor Error Codes** | v2.0 | Create, Delete, Read, Update |
| **Vouchers** | v2.0, 2.1 | Create, Delete, Read, Update |

*Run `bash scripts/fetch-and-generate.sh` to update this index*

**Actions**: See `reference/endpoints-index.md` for charge point, user, reservation, and notification actions.
<!-- END:QUICK_INDEX -->

---

## Data Model Overview

Understanding how AMPECO entities relate helps you choose the right endpoints.

```
Operator (tenant scope)
├── Location → ChargePoint → EVSE → Session
├── User → Session, PartnerInvite
├── Partner → ChargePoint (owned), PartnerInvite (users)
└── Tariff, SubscriptionPlan
```

**Common Use Cases:**

| Task | Key Endpoints |
|------|---------------|
| Charge point stats | `sessions?filter[chargePointId]=`, `sessions/{id}/consumption-stats` |
| User billing | `sessions?filter[userId]=`, `transactions?filter[userId]=`, `receipts` |
| Fleet management | `charge-points?filter[partnerId]=`, `partner-invites`, `partner-revenues` |
| Start/stop charging | `actions/charge-point/{id}/start/{evse}`, `actions/charge-point/{id}/stop/{session}` |

See `reference/data-model.md` for detailed relationships and recipes.

---

## Common Patterns

### Pagination

**Cursor pagination** (default, recommended):
```
GET /public-api/resources/users/v1.0?per_page=25
GET /public-api/resources/users/v1.0?cursor={next_cursor}&per_page=25
```

**Page pagination** (legacy support):
```
GET /public-api/resources/users/v1.0?page=1&per_page=25
```

### Filtering

Use `filter[fieldName]=value` format:
```
GET /public-api/resources/sessions/v1.0?filter[userId]=123
GET /public-api/resources/sessions/v1.0?filter[status]=active
GET /public-api/resources/sessions/v1.0?filter[startedAfter]=2024-01-01T00:00:00Z
```

### Includes

Embed related resources with `include[]=relationName`:
```
GET /public-api/resources/charge-points/v1.0?include[]=evses&include[]=location
```

### Error Responses

```json
{
  "message": "Unauthenticated."
}
```

Status codes: 401 (Unauthorized), 403 (Forbidden), 404 (Not Found), 422 (Validation Error)

---

## How to Use This Skill

1. **First**: Run `bash scripts/fetch-and-generate.sh` to get latest docs
2. **Find endpoints**: Load `reference/endpoints-index.md`
3. **Check schemas**: Load `reference/schemas-index.md`
4. **Check patterns**: Load `reference/common-patterns.md` for pagination, filtering, errors
5. **See deprecated**: Load `reference/deprecation-map.md`

## Reference Files

- `reference/data-model.md` - Entity relationships and use case recipes
- `reference/endpoints-index.md` - Complete list of all endpoints
- `reference/schemas-index.md` - Schema summaries
- `reference/deprecation-map.md` - Deprecated endpoints
- `reference/common-patterns.md` - Pagination, filtering, errors

## Live Documentation

https://developers.ampeco.com
