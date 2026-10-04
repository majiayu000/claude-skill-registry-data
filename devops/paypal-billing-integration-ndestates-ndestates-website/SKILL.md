---
name: paypal-billing-integration
description: >
  Full skill for PayPal integration in ndestates-io for payments and generating billing documents (invoices, receipts) directly at PayPal. Non-Microsoft (pure PayPal + Laravel). Use for checkout flows (e.g. admin subscriptions or document requests), webhook handling (payments, disputes), generating/sending PayPal invoices tied to e-sign usage, and refunds. Integrated with DO hosting, drift avoidance (project-drift-guardian), security (webhook verification, PCI via PayPal), Filament admin (billing dashboard), and cache-first. Enforces no-drift via cache + guardian. Always load cache first.
argument-hint: 'Task (e.g. "integrate PayPal checkout for document requests", "setup PayPal webhooks for billing", "generate PayPal invoice for admin user", "handle PayPal payment success in Laravel")'
user-invocable: true
disable-model-invocation: false
---

# PayPal Billing & Payments Integration for ndestates-io (Non-Microsoft)

**Goal for ndestates-io:** Monetize via PayPal (payments for plans, per-document requests, or usage). Generate billing documents (invoices/receipts) natively at PayPal (not custom PDFs or Microsoft tools). Ties to e-sign workflows: pay to create requests, receive invoices via PayPal. Non-Microsoft: PayPal APIs + Laravel (no Azure Billing, no Microsoft Invoicing). Integrated with existing DO (droplet/App), CI, drift prevention, and security.

**Core mandate:** Integration is infrastructure (Stage 6): cache-backed (PayPal config from cache, expected flows), drift-gated (project-drift-guardian before/after code/webhook changes), security-first (webhook sig verification, no card data in app, least-privilege API creds), observable (webhooks + evals), repeatable via one-liners + Laravel updates. Never ad-hoc. Use DDEV for local (PayPal sandbox), host for prod webhooks.

This skill is self-contained, references ndestates-io skills (load-project-cache-first, cache-efficient, project-drift-guardian, digitalocean-app-platform-docr-deploy, git-workflow-guardrails, security-audit-agent, eval/maintenance-task, laravel-expert-agent for code), and provides composer/PayPal setup, webhook examples (payments, billing docs), invoice generation via PayPal Invoicing API, Filament integration, and verification.

## Mandatory Start (cache + context — per all ndestates-io skills)
1. `.github/prompts/load-project-cache-first.prompt.md` (or .github/skills/cache-efficient/SKILL.md) — load INDEX, docs/codebase/ (ARCHITECTURE for billing in flows, INTEGRATIONS/STACK for PayPal, CONCERNS for payment risks), TODO-2026-06-14.md, prior evals.
2. `.github/skills/project-drift-guardian/SKILL.md` (or drift-check) — run scope/branch alignment on payment code/webhooks. Non-negotiable to avoid drift (e.g. webhook mismatches, config drift post-deploy, scope creep in billing).
3. Cross-load: branch-context-agent, github-expert (for CI webhooks), git-workflow-guardrails (before changes), security-audit-agent (PCI/secrets/webhooks), digitalocean-... (update DO env + webhooks URLs), laravel-expert-agent (for integration code), ai-engineering-maturity (track to Stage 6/8 for billing as agent slot).
4. Confirm current state: git status --short, current DO target (webhook URLs must match), last known billing state (from cache/TODO), PayPal account (sandbox vs live).

Never proceed without these. Update shared assets (TODO, docs/codebase/INTEGRATIONS.md, drift DB) after.

**Non-Microsoft policy:** Pure PayPal (Checkout + Invoicing APIs). No Microsoft Payment/ Billing. Use PayPal for all billing docs (invoices generated/sent via PayPal, not custom or Microsoft tools).

## PayPal Overview for ndestates-io
- **Payments:** Checkout for requesters (pay to create/send signature requests, usage-based, or subscriptions). Laravel handles approval, PayPal handles PCI.
- **Billing Documents:** Use PayPal Invoicing API to generate/send invoices/receipts tied to ndestates-io usage (e.g. "ndestates-io Pro - 100 signatures"). Invoices live in PayPal (user pays/views there). Webhooks notify app on paid/voided.
- **Webhooks:** Critical for async (payment success → create request, invoice paid → unlock features). Verify signatures.
- **Sandbox vs Live:** Start sandbox. Move to live with real creds.
- **Costs:** PayPal fees (standard); no extra for invoicing.
- **Security:** Never store card data (PayPal does). Webhook verification mandatory. Least-privilege API creds (Client ID/Secret).
- **Drift avoidance:** Webhook routes/config as code, pre/post checks via guardian + tests. Post-deploy: test payment + invoice + eval.

**References (load first):** docs/codebase/ARCHITECTURE.md (billing in e-sign flows), INTEGRATIONS.md (PayPal), CONCERNS.md (payment risks), .github/prompts/paypal-integration.md (detailed prompt), digitalocean skill (env/secrets/webhook URLs in DO), project-drift-guardian (no-drift on integration).

## Setup Procedures (one-liners + Laravel + webhooks)
Always: composer for SDK, .env for creds (DDEV local with sandbox, prod via DO secrets). Use PayPal REST API (v2 Checkout + Invoicing). No old SDKs.

### 1. PayPal Account & App (sandbox first)
- Create PayPal developer account (developer.paypal.com).
- Create App: get Client ID + Secret (for .env).
- For live: request app approval, get live creds.
- Sandbox accounts for testing (buyer/seller).

### 2. Laravel Integration (composer + config)
```bash
# Via DDEV (local prep)
ddev composer require paypal/rest-api-sdk-php  # or srmklive/paypal for v2 if preferred; adapt for Invoicing too
ddev exec php artisan vendor:publish --provider="Srmklive\PayPal\Providers\PayPalServiceProvider"  # if using wrapper
```

.env (DDEV override for sandbox; prod DO secrets):
```
PAYPAL_CLIENT_ID=your_sandbox_or_live_id
PAYPAL_CLIENT_SECRET=...
PAYPAL_MODE=sandbox  # or live
PAYPAL_CURRENCY=USD
# Webhook ID (from PayPal dashboard after creating webhook)
PAYPAL_WEBHOOK_ID=...
```

config/paypal.php (or services.php):
```php
'paypal' => [
    'client_id' => env('PAYPAL_CLIENT_ID'),
    'secret' => env('PAYPAL_CLIENT_SECRET'),
    'mode' => env('PAYPAL_MODE', 'sandbox'),
    'currency' => env('PAYPAL_CURRENCY', 'USD'),
    'webhook_id' => env('PAYPAL_WEBHOOK_ID'),
],
```

### 3. Checkout Flow (Payments for ndestates-io)
In Laravel (e.g. Filament action or controller for "Pay for Request"):
- Create order via PayPal API (amount from plan/usage).
- Redirect to PayPal approval.
- On return: capture payment, create SignatureRequest in DB, send signer magic links.
- Example (simplified; full in .github/prompts/paypal-integration.md):
```php
// In a service or controller
$provider = new \PayPal\Rest\ApiContext(...);
$payment = new \PayPal\Api\Payment();
$payment->setIntent('sale')
    ->setPayer(...) // credit_card or paypal
    ->setTransactions([new \PayPal\Api\Transaction(['amount' => ..., 'description' => 'ndestates-io request'])]);
$payment->create($provider);
$approvalUrl = $payment->getApprovalLink();
// Redirect user
```

On success webhook or return: verify, update request status, notify signers.

### 4. Webhooks (Critical for Billing + Payments)
- In PayPal dashboard: create webhook (e.g. https://yourdomain.com/webhooks/paypal).
- Events: PAYMENT.CAPTURE.COMPLETED, INVOICING.INVOICE.PAID, etc.
- In Laravel: route for webhook, verify signature (using webhook ID + secret).
```php
// routes/web.php (no CSRF for webhook)
Route::post('/webhooks/paypal', [PayPalWebhookController::class, 'handle']);

// Controller: verify + handle
$headers = request()->headers;
$body = request()->getContent();
if (! $this->verifyPayPalWebhook($headers, $body)) { abort(403); }
$event = json_decode($body);
if ($event->event_type === 'PAYMENT.CAPTURE.COMPLETED') {
    // Create request, generate PayPal invoice, etc.
}
```

For billing docs: on paid event, use PayPal Invoicing API to create/send invoice (template with ndestates-io branding, line items for usage). Store invoice ID in DB for reference.

Example invoice via API (PayPal Invoicing):
```php
$invoice = new \PayPal\Api\Invoice();
$invoice->setMerchantInfo(...) // your PayPal business
    ->setBillingInfo(...)
    ->setItems([new \PayPal\Api\InvoiceItem(['name' => 'ndestates-io Pro', 'quantity' => 1, 'unit_price' => 29.99])]);
$invoice->create($provider);
$invoice->send($provider);  // Emails via PayPal
```

### 5. Filament Admin Integration (Billing Dashboard)
- Add resource or page in Filament for "Billing" (list PayPal invoices, trigger manual invoice, view payments).
- Use laravel-expert-agent patterns for Eloquent (Payment model linking to SignatureRequest).
- Actions: "Generate PayPal Invoice" (calls API).

### 6. Testing & Drift
- Sandbox: full flows (pay, invoice, webhook).
- After setup: .github/skills/eval/maintenance-task/SKILL.md (define "clean" = successful test payment + invoice received + no errors).
- Pre/post any webhook/deploy: .github/skills/project-drift-guardian/SKILL.md --scope "paypal integration + billing docs".
- Update docs/codebase/INTEGRATIONS.md with webhook URLs, flows.
- In CI (digitalocean skill): test with PayPal sandbox in staging.

**One-liner full setup (cache-verified):**
```bash
# Local via DDEV
ddev composer require paypal/rest-api-sdk-php
# Set .env PAYPAL_* (sandbox)
ddev exec php artisan tinker
# Test: create payment, get approval link
# Prod: set live creds in DO, create webhook in PayPal dashboard, update env
# Verify: send test payment + check PayPal invoice
```

**Security & Governance (Stage 4 — mandatory):**
- Webhook verification mandatory (signature + webhook_id). No trust on body alone.
- Creds: DO secrets or AWS Secrets (inject at runtime). Full checklist on changes (MCP threats for new webhooks/scripts).
- PCI: PayPal handles cards (JS SDK or hosted fields). App never sees PAN.
- Billing docs: generated at PayPal (user pays/views there) — no custom storage of sensitive billing data.
- Refunds/disputes: handle via webhooks, update request status.

**Cross-references (max cache):**
- .github/prompts/load-project-cache-first.prompt.md + .github/skills/project-drift-guardian/SKILL.md + .github/skills/digitalocean-app-platform-docr-deploy/SKILL.md (hosting + webhook URLs in DO) + /security-audit-agent (webhooks/PCI).
- /eval/maintenance-task (post-setup).
- docs/codebase/ (billing in e-sign).
- .github/prompts/paypal-integration.md (for detailed AI-assisted code).
- copilot-instructions (DDEV local, no destructive, auth for billing data).

**Advancement (AI Engineering Maturity):** Turns billing into Stage 6 infra (agent slot for setup/verification/webhook handling, shared context in cache, evals as gates). Future: scheduled billing reports or auto-invoice on usage.

Invoke for any PayPal task: `.github/skills/paypal-billing-integration/SKILL.md "setup webhook for payment success + generate invoice"`. After: update TODO + cache. Re-run security checklist.

This makes PayPal native for ndestates-io payments + billing docs (generated at PayPal, non-Microsoft). Combined with .github/skills/amazon-ses-email/SKILL.md for comms. Cite https://upsun.com/blog/8-stages-ai-engineering-maturity/ when using.

(Adapted from patterns in digitalocean/prod-db-maintenance.github/skills/project-drift-guardian/SKILL.md skills across projects, made specific to ndestates-io + PayPal billing + Laravel.)