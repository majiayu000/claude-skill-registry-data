---
name: tac-domain-logistics
description: >-
  Load when working on shipments, manifests, AWBs, scanning, invoices, rate cards, customers, exceptions, or hubs in tac-express. Contains the real domain model, status lifecycles, branded types, financial model, RPC names, and event-derivation rules.
---

# Logistics Domain Knowledge

## Core Entities & Service Routing

| Entity | Types file | Service file |
|--------|-----------|-------------|
| Shipment | `packages/types/src/shipment.types.ts` | `packages/services/src/shipment.service.ts` |
| TrackingEvent | `packages/types/src/shipment.types.ts` | (via shipment service) |
| Manifest | `packages/types/src/manifest.types.ts` | `packages/services/src/manifest.service.ts` |
| Exception | `packages/types/src/exception.types.ts` | `packages/services/src/exception.service.ts` |
| Invoice | `packages/types/src/invoice.types.ts` | `packages/services/src/invoice.service.ts` |
| Hub | `packages/types/src/hub.types.ts` | `packages/services/src/hub.service.ts` |
| Customer | — | `packages/services/src/customer.service.ts` |
| Scan | `packages/types/src/domain.types.ts` (ScanPayload/ScanEvent) | `packages/services/src/scan-sync.service.ts` |
| Analytics | `packages/types/src/analytics.types.ts` | `packages/services/src/analytics.service.ts` |
| RateCard | `packages/types/src/rate-card.types.ts` | `packages/services/src/rate-card.service.ts` |

---

## ADR-004: Event-Derived Status (CRITICAL)

**Shipment status is NEVER stored directly. It is always derived from `tracking_events`.**

- Never set `shipment.status` directly in a mutation
- Status = last `TrackingEvent.status` ordered by `createdAt DESC`
- To update status: INSERT a new `TrackingEvent` — status updates automatically via DB trigger or query

---

## Branded Types (domain.types.ts)

```ts
import type { AWB, UUID, ManifestNumber, InvoiceNumber } from "@workspace/types"

// AWB format: TAC + 8-11 digits (e.g., TAC00012345)
const isAWB = (v: string): v is AWB => /^TAC\d{8,11}$/i.test(v)
const parseAWB = (input: string): AWB | null   // handles raw string or JSON QR payload
const formatAWB = (awb: AWB): string           // → "TAC-00012345" (with hyphen for display)
```

**Always use branded types — never plain `string` for AWB/UUID fields.**

---

## Hub Codes

```ts
enum HubCode {
  IMPHAL    = "IMPHAL",
  NEW_DELHI = "NEW_DELHI",
}
```

---

## Shipment Status Lifecycle

```
CREATED
  → PICKUP_SCHEDULED   (pickup booked)
  → PICKED_UP          (courier collected)
  → RECEIVED_AT_ORIGIN (arrived at origin hub)
  → IN_TRANSIT         (en route to destination hub)
  → RECEIVED_AT_DEST   (arrived at destination hub)
  → OUT_FOR_DELIVERY   (last-mile dispatch)
  → DELIVERED          (terminal — success)

  (any state) →
  → CANCELLED          (terminal — voided)
  → RTO                (return to origin)
  → EXCEPTION          (flagged — not terminal, can recover)
```

**Terminal states:** `DELIVERED`, `CANCELLED` — no further tracking events expected.

---

## Manifest Status Lifecycle

```
DRAFT → BUILDING → OPEN → CLOSED → DEPARTED → ARRIVED → RECONCILED
```

- `DRAFT`/`BUILDING`: scanning shipments in
- `OPEN`: ready to accept more AWBs
- `CLOSED`: locked for departure
- `DEPARTED`: in transit between hubs
- `ARRIVED`: received at destination hub
- `RECONCILED`: all AWBs accounted for (terminal)

---

## Invoice Status Lifecycle

```
DRAFT → ISSUED → PAID      (terminal — success)
               → OVERDUE
               → CANCELLED  (terminal)
```

---

## Exception Types & Severities

```ts
enum ExceptionType {
  DAMAGED, LOST, DELAYED, MISMATCH, PAYMENT_HOLD,
  MISROUTED, ADDRESS_ISSUE, MISSING_PACKAGE,
  WRONG_HUB, ROUTE_MISMATCH, INVOICE_DISPUTE,
}
enum ExceptionSeverity { LOW, MEDIUM, HIGH, CRITICAL }
enum ExceptionStatus   { OPEN, IN_PROGRESS, RESOLVED, CLOSED }
```

---

## Financial Model (Financials interface)

```ts
interface Financials {
  ratePerKg:      number   // base rate
  baseFreight:    number   // ratePerKg × chargeableWeight
  docketCharge:   number
  pickupCharge:   number
  packingCharge:  number
  fuelSurcharge:  number
  handlingFee:    number
  insurance:      number
  tax:            TaxBreakdown  // { cgst, sgst, igst, total }
  discount:       number
  totalAmount:    number   // sum of all charges + tax - discount
  advancePaid:    number
  balance:        number   // totalAmount - advancePaid
}
```

**Chargeable weight** = `max(dead, volumetric)`. Always use `Weight.chargeable` for billing.

---

## Scan System (QR / Barcode)

```ts
interface ScanPayload {
  v:           number
  type:        "shipment" | "manifest" | "package"
  awb?:        AWB
  manifestId?: UUID
  packageId?:  UUID
  metadata?:   Record<string, unknown>
}
```

QR codes encode a JSON `ScanPayload`. Use `parseAWB(input)` to extract AWB from raw string or QR JSON.

---

## User Roles & Permissions

```ts
enum UserRole { ADMIN, MANAGER, STAFF, CUSTOMER, DRIVER }

hasPermission(role, permission): boolean
canAccessModule(role, module): boolean
```

- ADMIN has `modules: ["*"]` — full access
- Always check roles at the service layer (`packages/services`) — never in components

---

## Zod Schemas (use, don't re-create)

```ts
import { createShipmentSchema, updateShipmentStatusSchema, contactSchema, weightSchema } from "@workspace/types/schemas/shipment.schema"
import { createManifestSchema } from "@workspace/types/schemas/manifest.schema"
import { createInvoiceSchema }  from "@workspace/types/schemas/invoice.schema"
```

---

## Key Business Rules

1. **AWB uniqueness** — `awbNumber` is globally unique. Format: `TAC` + 8–11 digits.
2. **Chargeable weight** — always `max(dead, volumetric)`. Never use `dead` alone for billing.
3. **Hub routing** — every shipment has `originHub` + `destHub`. Currently: IMPHAL ↔ NEW_DELHI.
4. **GST** — CGST+SGST for intra-state; IGST for inter-state. Computed server-side only.
5. **Scan events** — scanning triggers TrackingEvent inserts (ADR-004 — never direct status updates).
6. **Exception lifecycle** — exceptions don't block delivery but require resolution before invoice.
7. **Manifest reconciliation** — all AWBs in a DEPARTED manifest must be accounted for before RECONCILED.
