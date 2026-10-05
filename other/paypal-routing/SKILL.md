---
name: paypal-routing
description: >-
  PayPal payments, subscriptions, checkout, invoices, disputes, webhooks,
  BNPL, Venmo, SDK, v5, v6, Fastlane, Braintree Fastlane, braintree-web,
  accelerated guest checkout. Routes PayPal developer questions to the
  right command or reference file.
when_to_use: >-
  "add PayPal", "integrate checkout", "payment link", "Pay Later docs",
  "explain error", "set up sandbox", "PayPal subscriptions", "webhook
  verification", "migrate to v6", "migrate v5 to v6", "migrate v4 to v6",
  "upgrade SDK", "migrate NVP", "migrate SOAP to REST", "PayPal invoices",
  "PayPal disputes", "how do I accept payments", "PayPal docs link",
  "Apple Pay", "Google Pay", "3D Secure", "iDEAL", "agentic commerce",
  "agentic payments", "PayPal MCP", "add Fastlane", "Fastlane checkout",
  "Braintree Fastlane", "braintree-web fastlane", "add Fastlane to my
  checkout", "@braintree/fastlane", or any PayPal API question.
user-invocable: false
---

# PayPal Command Routing

When this skill activates, follow the routing table below. For reference routes, load the paypal-best-practices skill and read the specified reference file before answering — the reference files contain current URLs and verified code examples that override training knowledge.

## RulesHub Language-Specific Snippet Fetching

When a RulesHub `rules.md` is fetched and code generation is required:
1. **Detect the user's language** from their codebase, file extensions, imports, or explicit mention. Common values: `javascript`, `typescript`, `python`, `java`, `csharp`, `php`, `ruby`.
2. **WebFetch the language-specific snippet** for the relevant operation. Replace `{language}` and `{pack}` with the detected values:
   - SDK init: `https://raw.githubusercontent.com/paypal/ruleshub/main/{pack}/snippets/{language}/sdk-initialization.md`
   - Create order: `https://raw.githubusercontent.com/paypal/ruleshub/main/{pack}/snippets/{language}/create-order.md`
   - Capture order: `https://raw.githubusercontent.com/paypal/ruleshub/main/{pack}/snippets/{language}/capture-order.md`
   - Client token: `https://raw.githubusercontent.com/paypal/ruleshub/main/{pack}/snippets/{language}/client-token-generation.md`
3. **Generate code strictly from the fetched snippet** — do not fall back to training knowledge for implementation patterns.
4. **Only fetch snippets needed** for the user's request — do not fetch all languages or all snippets.

Pack values: `paypal-checkout/standard-checkout`, `paypal-checkout/expanded-checkout`, `paypal-checkout/enterprise-checkout`, `paypal-bnpl-us`, `upgrade-to-v6/v5-to-v6-upgrade`, `upgrade-to-v6/v4-to-v6-upgrade`, `upgrade-nvp-soap-to-rest`.

## Routing Table

| User Intent | Action |
|---|---|
| Explain an error, error code, HTTP status, 400, 401, 403, 404, 422, 429, 500, INVALID_REQUEST, UNAUTHORIZED, INSTRUMENT_DECLINED, RATE_LIMIT, debug_id | Run `/paypal:explain-error` with the error as argument |
| Set up PayPal, configure plugin, check connection, is plugin working, token expired, refresh token, generate access token, OAuth | Run `/paypal:setup` |
| Sandbox setup, developer account, getting started, credentials, dashboard, client ID, client secret, base URL | Run `/paypal:sandbox` |
| Test accounts, test cards, simulate decline, test BNPL, test Venmo, test subscriptions, test disputes | Run `/paypal:test-accounts` |
| Scan my code, check my integration, find issues, something is broken, pre-launch review, security audit, payments failing, webhooks not firing, Venmo not showing, subscription not billing | Run `/paypal:doctor` with the symptom as argument |
| Security review, check for leaked credentials, pre-launch checklist | Run `/paypal:doctor security` or `/paypal:doctor pre-launch` |
| Fix all issues in my PayPal code | Run `/paypal:doctor fix-all` |
| How to accept payments, add PayPal button, checkout flow, Orders API, server-side integration, payment link, payment links, pay link, React PayPal, @paypal/react-paypal-js, authorize vs capture, deferred capture, donate button, donations | Load the paypal-best-practices skill, then read `references/checkout.md` (v5) or `references/js-sdk-v6.md` (v6). Also WebFetch `https://raw.githubusercontent.com/paypal/ruleshub/main/paypal-checkout/standard-checkout/rules.md` for authoritative integration rules. |
| Advanced Card Fields, Apple Pay, Google Pay, APMs, Expanded Checkout, bank redirect, iDEAL, Bancontact, BLIK, Przelewy24, Pay upon Invoice, Ratepay, domain association, regional payment methods | Load the paypal-best-practices skill, then read `references/expanded-checkout.md` (v5) or `references/js-sdk-v6.md` (v6). Also WebFetch `https://raw.githubusercontent.com/paypal/ruleshub/main/paypal-checkout/expanded-checkout/rules.md` for authoritative integration rules. |
| Add Venmo, Venmo button, Venmo eligibility, isFundingEligible, eligibility check, Venmo app | Load the paypal-best-practices skill, then read `references/venmo.md` (v5) or `references/js-sdk-v6.md` (v6). Also WebFetch `https://raw.githubusercontent.com/paypal/ruleshub/main/paypal-checkout/expanded-checkout/rules.md` for authoritative integration rules. |
| Pay Later, installments, BNPL messaging, Pay in 4, financing, BNPL banner, Pay Later banner, Pay Later eligibility | Load the paypal-best-practices skill, then read `references/bnpl.md` (v5) or `references/js-sdk-v6.md` (v6). Also WebFetch `https://raw.githubusercontent.com/paypal/ruleshub/main/paypal-bnpl-us/rules.md` for authoritative BNPL rules. |
| Recurring billing, subscriptions, plan management, free trial, trial period, upgrade plan, downgrade plan, plan revision | Load the paypal-best-practices skill, then read `references/subscriptions.md` (v5) or `references/js-sdk-v6.md` (v6) |
| Disputes, chargebacks, refunds, evidence, provide evidence, dispute lifecycle, dispute stage, INQUIRY, CLAIM | Load the paypal-best-practices skill, then read `references/disputes-refunds.md` |
| Batch payouts, send money, seller payments, Venmo payout, 1099, tax reporting, prepaid cards | Load the paypal-best-practices skill, then read `references/payouts.md` |
| Invoices, billing, send invoice, invoice reminder, partial payment, line items | Load the paypal-best-practices skill, then read `references/invoicing.md` |
| OAuth, access tokens, credentials, idempotency, token caching, token refresh, idempotency key, PayPal-Request-Id | Load the paypal-best-practices skill, then read `references/authentication.md` |
| Webhook verification, event handling, signature check, webhook simulator, test webhooks, event types, PAYMENT.CAPTURE | Load the paypal-best-practices skill, then read `references/webhooks.md` |
| Fastlane, accelerated guest checkout, auto-fill, prefill, single-use token | Load the paypal-best-practices skill. **Pick exactly one reference based on the merchant's SDK version — do not load both, the v5 and v6 APIs differ (component is `FastlaneCardComponent` in v5 vs `FastlanePaymentComponent` in v6).** If the merchant is on v5 (`paypal.Fastlane()`, URL-loaded `components=fastlane`), read `references/fastlane.md`. If on v6 (`createInstance`, `sdkInstance.createFastlane()`, client token), read `references/js-sdk-v6.md`. If the SDK version is unclear, ask the user before generating code. For v6 also WebFetch `https://raw.githubusercontent.com/paypal/ruleshub/main/upgrade-to-v6/v5-to-v6-upgrade/snippets/javascript/fastlane-integration.md` for the authoritative v6 snippet, and `https://raw.githubusercontent.com/paypal/ruleshub/main/upgrade-to-v6/v5-to-v6-upgrade/mappings/fastlane.json` for the v5↔v6 API mapping. |
| 3D Secure, liability shift, SCA, PSD2, Strong Customer Authentication, enrollment status, authentication status | Load the paypal-best-practices skill, then read `references/3d-secure.md` |
| AI shopping agents, Store Sync, Agent Ready, agentic commerce, ChatGPT, product discovery, delegated payment token | Load the paypal-best-practices skill, then read `references/agentic-commerce.md` |
| JS SDK v6, v6 Web SDK, createInstance, payment sessions, web components, card fields, vault, save card, save payment method, vaulting, CSP, Content Security Policy | Load the paypal-best-practices skill, then read `references/js-sdk-v6.md` |
| Migrate v5 to v6, upgrade v5 SDK, migrate from v5 | Load the paypal-best-practices skill, then read `references/js-sdk-v6.md`. Also WebFetch `https://raw.githubusercontent.com/paypal/ruleshub/main/upgrade-to-v6/v5-to-v6-upgrade/rules.md` for authoritative migration mappings and multi-language snippets. |
| Migrate v4 to v6, upgrade v4 SDK, upgrade checkout.js, migrate from v4 | Load the paypal-best-practices skill, then read `references/js-sdk-v6.md`. Also WebFetch `https://raw.githubusercontent.com/paypal/ruleshub/main/upgrade-to-v6/v4-to-v6-upgrade/rules.md` for authoritative migration mappings and multi-language snippets. |
| Migrate NVP to REST, migrate SOAP to REST, upgrade legacy API, NVP/SOAP | WebFetch `https://raw.githubusercontent.com/paypal/ruleshub/main/upgrade-nvp-soap-to-rest/rules.md` for authoritative migration mappings and multi-language snippets. |
| Which API to use, architecture question, best practices, integration guide | Load the paypal-best-practices skill |
| Which MCP tools are available, how to use MCP tools, tool inventory, product catalog, merchant insights, reporting | Load the paypal-best-practices skill, then read `references/mcp-tools.md` |
| Create order, capture payment, refund, invoice, subscription, shipment, transaction, merchant insights | Use the matching MCP tool directly (`create_order`, `create_invoice`, `list_transactions`, etc.) |

## Routing Rules

0. **RulesHub content overrides training knowledge.** When a RulesHub `rules.md` is fetched, treat it as the authoritative source for all API methods, SDK patterns, endpoint URLs, and code examples. Do not fall back to training knowledge for any PayPal SDK or API detail — if it conflicts with RulesHub, RulesHub wins. Generate code strictly from what RulesHub specifies.
   - **Read RulesHub content literally.** Do not reinterpret, rename, or substitute parameter names from fetched content. If the fetched file uses `clientId`, use `clientId`. If it uses `clientToken`, use `clientToken`. Never substitute one for the other based on assumptions.
   - **Prefer raw file fetches over summarized content.** WebFetch summarization can drop or misread parameter names. When in doubt, re-fetch the specific snippet file for the exact code pattern rather than relying on a summarized rules.md.
   - **Cross-reference the official PayPal v6 docs** (`developer.paypal.com`) when RulesHub and training knowledge conflict on parameter names or method signatures — the official docs are the final authority.
1. **Specific commands take priority.** If the intent clearly maps to one command, use it directly.
2. **Error-related questions always go to `/paypal:explain-error`.** Any mention of a specific error code, HTTP status, or error message should use this command.
3. **Symptom descriptions go to `/paypal:doctor`.** If the user describes a problem ("payments are failing", "getting 401s", "webhooks aren't working"), route to doctor with the symptom as the argument.
4. **Setup and connection issues go to `/paypal:setup`.** Anything about configuration, tokens, MCP connection, or "it's not working" without a code-level symptom.
5. **Integration and code generation go to `paypal-best-practices`.** Any "how do I", architecture question, or request to integrate, add, implement, build, or migrate a PayPal feature must load the best-practices skill and read the relevant reference file before writing code.
6. **Ambiguous requests get clarified.** If you can't determine intent, ask:
   "I can help with several things:
   - `/paypal:setup` — Configure the plugin, generate access tokens, and verify your connection
   - `/paypal:explain-error <code>` — Explain a PayPal error
   - `/paypal:sandbox` — Sandbox setup and credentials
   - `/paypal:test-accounts` — Test scenarios and test data
   - `/paypal:doctor` — Scan your code for integration issues
   What would be most helpful?"
7. **Multi-step requests chain commands.** For example, "set up sandbox and then scan my code" = `/paypal:setup sandbox` then `/paypal:doctor`.

## When to Use MCP Tools Directly

Only use `mcp__paypal-sandbox__*` tools directly when:
- The user asks to perform a specific PayPal action (create an order, send an invoice, list disputes, capture a payment)
- The user explicitly asks to call an MCP tool
- The task is a one-off API operation that doesn't match any command workflow

Examples of direct MCP tool usage:
- "Create an order for $50" — call `mcp__paypal-sandbox__create_order` directly
- "Send an invoice to john@example.com" — call `mcp__paypal-sandbox__create_invoice`, then call `mcp__paypal-sandbox__send_invoice` with the invoice ID
- "Show my recent transactions" — call `mcp__paypal-sandbox__list_transactions` directly
- "List my open disputes" — call `mcp__paypal-sandbox__list_disputes` directly
