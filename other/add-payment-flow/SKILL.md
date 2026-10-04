---
name: add-payment-flow
description: Scaffold a payment gateway integration (HyperPay/Moyasar) with checkout, webhook, and transaction tracking. Use when adding payment capabilities.
---

# add-payment-flow

Integrates a Saudi-compatible payment gateway for processing earnest money, commissions, or subscription fees. Supports mada, Visa, Mastercard, and Apple Pay.

## Inputs to gather

- **Gateway** — HyperPay (recommended for Saudi) or Moyasar
- **Payment type** — one-time (commission, deposit) or recurring (subscription)
- **Entity** — what is being paid for (dealId, subscriptionId, invoiceId)
- **Amount source** — fixed or computed from entity (e.g., deal commission amount)

## Steps

1. **Create the transactions model** via `/add-prisma-model`:
   ```prisma
   model transactions {
     id            String   @id @default(uuid())
     amount        Decimal
     currency      String   @default("SAR")
     status        String   @default("PENDING") // PENDING, COMPLETED, FAILED, REFUNDED
     gatewayRef    String?
     gatewayData   Json?
     entityType    String   // "deal", "subscription", "invoice"
     entityId      String
     userId        String
     organizationId String?
     createdAt     DateTime @default(now())
     updatedAt     DateTime @updatedAt
   }
   ```

2. **Create payment service** at `apps/api/libs/payment-gateway.ts`:
   - `initiateCheckout(amount, currency, entityType, entityId)` → returns checkout URL
   - `verifyPayment(gatewayRef)` → returns status
   - `processRefund(transactionId)` → initiates refund

3. **Create API routes** at `apps/api/routes/payments.ts`:
   - `POST /api/payments/initiate` — create checkout session, return redirect URL
   - `POST /api/payments/webhook` — gateway callback (no auth, verify signature)
   - `GET /api/payments/transactions` — list user/org transactions
   - `POST /api/payments/:id/refund` — admin-only refund

4. **Create checkout page** at `apps/web/src/pages/platform/checkout.tsx`:
   - Shows amount, entity details, payment method selection
   - Embeds gateway form (HyperPay widget or redirect)
   - Success/failure callback pages

5. **Add environment variables:**
   ```
   HYPERPAY_ENTITY_ID=...
   HYPERPAY_ACCESS_TOKEN=...
   HYPERPAY_BASE_URL=https://test.oppwa.com  # sandbox
   ```

## Verification checklist

- [ ] Sandbox checkout completes successfully
- [ ] Webhook updates transaction status to COMPLETED
- [ ] Transaction appears in history page
- [ ] Refund flow works (admin only)
- [ ] Amount matches entity (no manipulation possible)
- [ ] Webhook signature verification prevents spoofing
- [ ] `/typecheck` passes

## Anti-patterns

- Don't trust client-side amount — always compute server-side from entity
- Don't store full card numbers — gateway handles PCI compliance
- Don't skip webhook signature verification
- Don't process payments without creating a transaction record first
- Don't expose sandbox credentials in production
