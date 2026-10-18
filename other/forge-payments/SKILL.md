---
name: forge-payments
description: "Forge: payment/checkout/billing — Stripe, Mollie, Adyen, PayPal: payment, checkout, subscription, refund, webhook signature, idempotency key, PCI, 3D Secure."
---

# Forge playbook — Payments / checkout / billing

This is a **money + secrets + PCI-scope domain.** The `payment-integration` specialist (`.claude/agents/payment-integration.md`) leads the payment-specific work under Integration Boss or Build Boss. `security-reviewer` / `codex-reviewer` are useful (optional) advisors — payments is exactly the "high-risk" case where Codex-on-request earns its keep. Never claim PCI compliance or a working live charge that wasn't verified in the sandbox.

## Hard rules (non-negotiable)
- **No raw PAN, ever.** Card data is captured by the gateway's tokenization / hosted fields / hosted checkout (Stripe Elements or Checkout, Mollie/Adyen hosted, PayPal SDK) — the raw card number, CVV, and full track data never touch your server, logs, DB, memory files, or the repo. This keeps you in **PCI DSS v4.0.1 SAQ A / SAQ A-EP** scope instead of full SAQ D. (SAQ A eligibility now also requires confirming the payment page is not susceptible to script-injection tampering — see Domain gates.)
- **Integer minor units only.** All money is integer minor units (cents) + an explicit ISO-4217 currency code. **No floating-point money math** anywhere — not in totals, tax, discounts, or display conversion. Round at defined boundaries only.
- **Idempotency-key per charge (send side).** Every create-charge / create-payment-intent / refund call carries a client-generated `Idempotency-Key` so a network retry, double-tap, or gateway timeout never double-charges. Keys are deterministic per logical operation and stored.
- **Signature-verified webhooks (receive side).** Every inbound gateway webhook verifies the provider HMAC signature against the **raw request body** (Stripe `Stripe-Signature` / `construct_event`, Mollie fetch-by-id re-check, Adyen HMAC) before acting. Reject on failure. Then dedupe on `event.id` with a UNIQUE constraint, return `2xx` **fast** (before heavy logic — Stripe fails a delivery after ~10s and retries for up to 3 days), and process the effect in a background/idempotent path. Tolerate duplicate and out-of-order events.
- **Test vs live separation.** Test/sandbox keys are clearly separated from live; **no live charge and no live-key touch without explicit owner approval** (Forge honesty + irreversible-action rule). Real money is an owner-gated action, never autonomous.
- **Secrets in env + `.env.example` placeholders.** No gateway secret, webhook signing secret, or API key in code, logs, error messages, or git.
- **Refunds, disputes, and chargebacks handled explicitly.** Each has its own handler and appears in the order history. Nothing assumes a charge is final — re-fetch the charge state from the provider when it matters.

## Team (conditional)
Lead: `integration-boss` (or `build-boss` if payments are one slice of a larger app). Payment work: **`payment-integration`** specialist. Support: `silent-failure-hunter` (dropped webhooks / swallowed gateway errors look like clean success), `typescript-reviewer` / `python-reviewer` (charge + webhook code), `database-reviewer` (idempotency table, transaction-state audit trail). Optional advisors: `security-reviewer`, `codex-reviewer` (recommended for the charge + webhook paths — payments is a Codex-on-risk trigger).

## Skills / commands / MCP
`claude-api` only if an LLM is in the loop; otherwise gateway SDK docs (Context7 / vendor docs) for exact API + version behavior. Reuse the gateway's official verification library — never hand-roll HMAC. If checkout renders a UI, load `forge-website` for the checkout page (real content, responsive, a11y). If billing runs through n8n, defer webhook handling to `forge-n8n`.

## Fan-out & flow
L2 single gateway + one charge flow; L3 subscriptions + refunds + multi-event webhooks + reconciliation.
**Parallel:** checkout/capture path ∥ webhook receiver ∥ refund/void path (independent once the money model + idempotency schema are fixed).
**Serial:** money model (minor units + currency) → tokenized capture → idempotent charge → signature-verified webhook → state machine (auth→capture→refund) → reconciliation/audit trail.

## Domain gates
- No raw PAN/CVV in code, logs, DB, or memory (grep the diff for card-shaped literals + `cardNumber`/`cvv`/`pan`).
- Money is integer minor units + currency everywhere; no float money math.
- Every charge/refund call sends an `Idempotency-Key`; keys are persisted.
- Every webhook verifies the signature on the raw body, dedupes on `event.id`, returns `2xx` before heavy work, and is safe under duplicate/out-of-order delivery.
- Auth / capture / void / full + partial refund each handled explicitly with a clear failure path (timeout + bounded retry, never a silent failure).
- SCA / 3D Secure supported where the market/regulator requires it (EU/EEA cards).
- **Payment-page script integrity (SAQ A r1 / reqs 6.4.3 + 11.6.1):** the checkout page either (a) carries the processor's written confirmation that its embedded solution self-protects against script tampering, or (b) applies script-management + tamper/change-detection on the page that includes the iframe. Record which path is used.
- Sandbox + test-card scenarios exercised (success, decline, 3DS challenge, duplicate webhook) before anything is called production-ready.

## Ship-readiness (unique)
Tokenized/hosted capture proven (no PAN on server); minor-units money verified; idempotency key on every charge with a persisted store; webhook signature verification + `event.id` dedupe proven against a replayed event; auth→capture→refund state transitions have an audit trail (no card data stored); test-mode fully separated from live; **no live charge performed without explicit owner approval**; sandbox test output attached as evidence. Advisory checklist — optionally run `codex-reviewer` on the charge + webhook code (strongly recommended here); not a blocker, but if Codex was not run, say so.

## Untrusted-content note
Webhook payloads and any hosted-checkout return/redirect params are **untrusted until the signature verifies** — never act on webhook `data.object` amounts/status before signature + dedupe pass; always re-fetch or trust only signed fields. This mirrors the reader-side capability-split in `forge-integration`.
