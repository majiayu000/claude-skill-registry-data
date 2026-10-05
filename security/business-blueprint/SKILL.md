---
name: business-blueprint
description: "Comprehensive business-logic blueprint for SaaS, ERP, e-commerce, and marketplace applications. Walks through every domain (auth, billing, multi-tenancy, inventory, audit, compliance, etc.), surfaces the edge cases that actually break in production, and proposes a concrete plan tailored to the user's context."
argument-hint: "[saas | erp | ecommerce | marketplace | fintech | full-stack]"
---

# /business-blueprint

A structured walkthrough of business logic for the project type the user is building. Output is a personalized blueprint — the relevant domains for their app, the edge cases that matter, and a prioritized build plan.

## When to use

- Starting a new SaaS / ERP / e-commerce / marketplace / fintech project — *before* committing to an architecture.
- Auditing an existing project against the full set of real-world concerns.
- Onboarding to a domain you haven't built before and want a checklist of what to think about.
- Preparing for a Series A / SOC 2 / enterprise customer review.

## Operating method

### 1. Lock down the project type and context

Ask, in one round:

- **Project type**: SaaS / ERP / e-commerce / marketplace / fintech / internal tool / something else.
- **Customer**: B2C / SMB B2B / mid-market B2B / enterprise B2B / government / regulated industry.
- **Sales motion**: self-serve / freemium / sales-led / hybrid.
- **Monetization**: subscription / usage / transaction fee / one-time / hybrid.
- **Jurisdictions** (where customers and the business are): US / EU / UK / India / etc.
- **Stage**: pre-launch / early users / scaling / mature.
- **Constraints**: must-self-host, no-third-party-data, single-region, etc.

Don't blueprint without these. Domain ambiguity makes for irrelevant blueprints.

### 2. Walk the domain checklist for the project type

Different project types have different "must-have at v1" lists. Pick the matching section below.

### SaaS blueprint

**Identity & access**
- Auth methods: password + magic link minimum; OAuth (Google/GitHub) for self-serve; SAML SSO for enterprise tier.
- MFA: TOTP + WebAuthn. Avoid SMS for high-value accounts.
- Roles: Owner > Admin > Member > Viewer (B2B default). Customize per domain.
- Permission model: role-based at v1. ABAC if resources need fine-grained ownership.
- Session: refresh tokens with rotation; idle timeout per security tier.
- Account merging: design how to handle "user signs up Google and SAML with same email."
- Account recovery: backup admin, recovery codes, support escalation path.

**Multi-tenancy**
- Isolation: shared DB + tenant_id (default for < 10K tenants). DB-per-tenant for enterprise/regulated.
- Tenant context: every query filters tenant_id; wrap DB layer.
- Cross-tenant tests: integration test that runs as A and tries B's IDs — should always 404.
- Tenant switching UI for multi-workspace users.
- Tenant export (GDPR, portability).
- Tenant deletion (cascade, retention).

**Subscription billing**
- Stripe Billing / Recurly / Paddle / Chargebee — pick one, don't roll your own.
- Plan structure: tiered + usage hybrid is most common (Stripe pricing model).
- Trial: 14-day free trial without credit card is the SMB default; 30-day with-card for enterprise.
- Upgrade: immediate, prorate. Downgrade: end-of-period (default) or immediate with refund.
- Failed payment: Stripe Smart Retries default (4 retries / 15 days). Email cadence d1/d3/d7. Grace period before suspend.
- Dunning: in-app banner + email + customer portal for self-rescue.
- Cancel: cancel-at-period-end vs immediate. Retention offer at cancel time (downgrade, pause, discount).
- Refunds: partial vs full, time window, who can authorize, audit trail.
- Coupons: stacking rules, expiration, code-vs-link, fraud prevention.
- Tax: Stripe Tax / Avalara — never hand-roll VAT/GST/sales-tax.
- Invoices: sequential, immutable, PDF retention, e-invoicing for EU.

**Onboarding**
- Trial: minimize time-to-value (TTV). One-step signup if possible.
- Activation event: define what "activated" means (first invite sent? first project created? first payment?).
- Onboarding checklist UI for SaaS.
- Empty states that guide first action.
- Sample data option for demos.

**Notifications**
- Channels: in-app, email, SMS, push, webhook, Slack.
- Per-user per-category preferences.
- Digest mode for low-priority items.
- One-click unsubscribe + suppression list.
- Localization (timezone, language).
- Quiet hours / do-not-disturb.

**Webhooks (outgoing for integrators)**
- HMAC signing.
- Retry with exponential backoff + dead-letter.
- Stable event IDs for dedupe.
- No ordering guarantees.
- Schema versioning + sunset policy.

**API**
- Versioning (URL or header).
- Idempotency-Key header on every state change.
- Cursor-based pagination.
- Rate limits per-key + per-tenant.
- Stable error codes alongside human messages.

**Audit & compliance**
- Audit log on every state change to regulated entities.
- Append-only, retention by data class.
- SOC 2 readiness: access controls, monitoring, change management, vendor management.
- GDPR: DSAR endpoint, right-to-erasure (cascade including backups), DPA with sub-processors.

**Account lifecycle**
- Trial → paid conversion.
- Active → past_due → suspended → cancelled.
- Cancelled → reactivation window (typically 30 days).
- Permanent deletion after retention.

### ERP blueprint

**Financial**
- Chart of accounts (5- or 6-digit hierarchy: assets, liabilities, equity, revenue, expense).
- Double-entry posting: every transaction has matching debits and credits.
- Period close: monthly + annual; lock once closed; adjustments via journal entries.
- Multi-currency: functional currency vs presentation currency. FX rate table. Realized vs unrealized FX gains/losses.
- AR (accounts receivable): invoice → payment → reconciliation; aging buckets (30/60/90+).
- AP (accounts payable): PO → GRN (goods received note) → invoice → payment → 3-way match.
- GL (general ledger): every transaction posts here; trial balance must balance.
- Depreciation: straight-line / declining-balance / units-of-production. Recurring monthly entry.
- Tax: VAT/GST per line item, configurable per jurisdiction.
- Bank reconciliation: import statement → match transactions.

**Inventory**
- Stock levels: on-hand, reserved, allocated, available = on_hand − reserved − allocated.
- Valuation: FIFO / LIFO / average cost / specific identification. Pick per business; tax implications.
- Multi-warehouse: stock per location; transfers; in-transit.
- Lot / serial tracking for regulated industries (food, pharma, electronics).
- Cycle counting: scheduled partial inventory checks; variance tracking.
- Reorder points: min stock + reorder qty per SKU. Auto-PR when triggered.

**Procurement**
- Workflow: PR (purchase requisition) → PO (purchase order) → GRN (goods received note) → invoice → payment.
- 3-way match: PO + GRN + invoice quantities and prices must agree.
- Vendor management: master data, terms, ratings.
- Approval workflows: thresholds by amount + role.
- Blanket POs / contracts.

**Sales**
- Workflow: quote → order → fulfillment → invoice → payment.
- Credit limits per customer; block orders that exceed.
- Returns / RMAs: link to original order, restock or scrap, refund or credit memo.
- Drop-ship vs warehouse fulfillment.

**Manufacturing (if applicable)**
- BOM (bill of materials): components per finished good; multi-level.
- MRP (material requirements planning): demand → required components → POs.
- Work orders: production schedule, routings, capacity.
- Scrap / rework tracking.

**HR / payroll (if applicable)**
- Employee master data, org structure, manager hierarchy.
- Time tracking: timesheets, approvals.
- Payroll: gross → deductions → net. Per-jurisdiction tax + benefits.
- Leave management: accrual, balance, requests.
- Performance reviews + onboarding/offboarding workflows.

**Compliance**
- SOX (US public companies): segregation of duties (no one approves their own POs), audit trail, change management.
- Approval matrices: by amount, by role, by department.
- Audit log: append-only, queryable, retained 7+ years.

### E-commerce blueprint

**Catalog**
- Products + variants (size, color, material).
- SKUs unique per merchant.
- Bundle products, subscription products, digital goods, services.
- Inventory sync to fulfillment systems.

**Cart & checkout**
- Cart abandonment recovery (email at 1h / 24h / 72h).
- Guest checkout vs account-required.
- Shipping calculator (rate per zone + weight or flat).
- Tax: Stripe Tax / Avalara / TaxJar.
- Address validation.
- Multi-payment-method: card, wallet (Apple/Google Pay), BNPL (Klarna/Afterpay), bank transfer (B2B).
- Idempotent checkout: re-submitting must not double-charge.
- 3DS / SCA for EU/UK.

**Order management**
- Order states: pending → paid → fulfilled → completed. Or cancelled / refunded / disputed.
- Inventory hold at order placement; release on cancel.
- Partial fulfillment (some items ship now, others later).
- Backorders.
- Order edits (price adjust, item swap) — track who, when, what.

**Returns / RMA**
- Return window (typically 14–30 days; longer is friendlier).
- Refund vs store credit vs exchange.
- Restock vs scrap.
- Return shipping label generation.
- Dispute / chargeback workflow.

**Fraud**
- Risk scoring (Stripe Radar, Sift, Signifyd).
- Velocity rules (multiple orders to new shipping address, mismatched billing/shipping).
- Manual review queue.
- Blocklist (email, IP, card).

**Marketplace-specific (if applicable)**
- Seller onboarding + KYC.
- Connected accounts (Stripe Connect Express/Custom).
- Split payments + platform fee.
- Payouts schedule + holds for first-time sellers.
- Seller-side dashboard.
- Dispute escalation between buyer/seller/platform.

### Marketplace blueprint

Add to e-commerce blueprint:

- KYC/AML for sellers (Stripe Identity, Persona, Sumsub).
- Transaction monitoring for money-laundering signals.
- Dual-side reviews (buyer rates seller; seller rates buyer).
- Escrow / hold periods (release funds N days after delivery).
- Dispute resolution between buyers and sellers.
- Tax form generation (1099-K in US for sellers above threshold).

### Fintech blueprint

Add stricter versions of:

- KYC/AML at onboarding + transaction monitoring.
- Sanctions screening (OFAC, EU, UN lists).
- Reg-specific compliance (PSD2 SCA, GDPR, PCI-DSS Level 1).
- Audit log retention 7+ years; immutable + append-only ledger.
- Reconciliation jobs that run nightly and alert on mismatches.
- Reserves and capital requirements per regulator.
- Disaster recovery RTO/RPO measured in minutes.

### Full-stack web app (no specific business domain)

Use SaaS blueprint as default; trim sections that don't apply.

### 3. Identify what's missing

Compare the user's current project against the relevant blueprint. Mark each item as:

- **Done** — already implemented well.
- **Partial** — exists but has gaps.
- **Missing** — not started; risk level depending on stage.
- **N/A** — doesn't apply to this project.

### 4. Prioritize by stage

- **Pre-launch** — auth, basic billing, 1 plan, audit log, terms/privacy. Don't over-engineer; 80% of mature-SaaS features are post-PMF.
- **Early users (< 100 paying)** — solid billing (failed-payment retries, dunning), one good notification channel, GDPR basics.
- **Scaling (100–10K paying)** — multi-tier plans, SAML SSO for enterprise tier, robust webhooks, audit log, SOC 2 prep.
- **Mature** — multi-currency, multi-region, advanced RBAC, public API w/ versioning, full SOC 2 + GDPR + region-specific compliance.

Don't recommend mature-stage features to a pre-launch project. Stage matters more than feature completeness.

### 5. Save the blueprint

Write the result to `.claude/memory/project/business-blueprint.md` so future sessions reference it. Add to `MEMORY.md`.

## Output format

```
## Project context
- Type: <saas/erp/...>
- Customer: <segment>
- Stage: <pre-launch/early/scaling/mature>
- Jurisdictions: <list>

## Audit
| Domain | Status | Notes |
|---|---|---|
| Auth + MFA | Done | TOTP only; consider WebAuthn |
| Multi-tenancy | Partial | tenant_id filter present; cross-tenant test missing |
| Billing — failed payment | Missing | High risk for SaaS — implement before scaling |
| Audit log | Missing | Required pre-SOC-2 |
| …

## Top 5 priorities for your stage
1. <highest impact>
2. …

## Build plan
- Now (this sprint): <items>
- Soon (next 2 sprints): <items>
- Later (post-PMF / SOC 2 prep): <items>
- Maybe never: <items that don't fit your context>

## Open questions for you
1. …
```

## Boundaries

- Don't recommend mature-stage complexity to a pre-launch project.
- Don't invent in well-trodden domains (billing, auth, search) — point at Stripe/Auth0/Algolia patterns.
- Don't overlook jurisdiction-specific compliance.
- Don't write the actual code from this skill; this is the *plan*. Implementation happens in subsequent sessions, agent by agent.
- Always cite where a recommendation comes from (Stripe Billing docs, Linear engineering blog, etc.) when borrowing patterns.
