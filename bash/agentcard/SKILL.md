---
name: agentcard
description: Lets an AI agent pay merchants securely with the user's own card — through Mastercard Agent Pay (the default for Mastercard holders, passkey-approved per purchase) or, for any other card, a one-time card number capped to the purchase — completes KYC verification when required, handles checkout 3DS challenges, manages the user's AgentCard agent email inbox, and uses the AgentCard USDC wallet for Base/x402 payments. Use when an agent needs to pay a merchant, complete required KYC, complete a checkout, fetch paid x402 content, send or read agent email, inspect spend limits, or troubleshoot AgentCard CLI payments.
version: 2.2.0
author: "Alchemy (https://alchemy.com)"
license: MIT
homepage: https://agentcard.ai
prerequisites:
  commands:
    - npm
metadata:
  hermes:
    tags:
      - payments
      - commerce
      - identity
      - mastercard-agent-pay
      - virtual-cards
      - agent-commerce
      - email
      - wallet
      - x402
      - 3ds
    category: payments
    homepage: https://agentcard.ai
    requires_toolsets:
      - terminal
---

# AgentCard

AgentCard lets agents pay securely with the user's own card, under user-controlled limits. The core model: **request a payment credential for one purchase; the user's card decides the path**:

- **Mastercard Agent Pay (default for Mastercard holders).** The user connects their Mastercard once. Each purchase gets a one-time network-token credential scoped to the merchant and amount, which the user approves with a browser passkey. The merchant charges the user's own Mastercard directly; AgentCard holds no funds. Mastercard Agent Pay is enabled for all Mastercards.
- **One-time card number (Visa, Amex, Discover, any other card).** Source `agentcard`: AgentCard provides a one-time card number capped to the purchase amount, live for 7 days, funded by a hold on the user's saved card. Instant, no approval step. This is also the fallback whenever a connected-card path doesn't work.
- **Visa Intelligent Commerce (opt-in for Visa holders).** It supports only some Visa cards, so one-time card numbers stay the default for Visa. If the user wants to try it, run `agentcard sources connect --network visa`. If the card enrolls, it becomes the default (unless a Mastercard is on Agent Pay) and works like Agent Pay: passkey approval, merchant-scoped credential. If it doesn't enroll, keep using one-time card numbers.
- KYC verification for new or non-exempt direct accounts before spend.
- A dedicated `@agentcard.email` inbox for signups, verification codes, and user-approved communication.
- An SMS-capable agent phone number for signups and verification texts, unlocked after a spend threshold (`agentcard phone info` shows progress).
- A self-custodial USDC wallet on Base for x402 HTTP payments and USDC transfers.

Prefer exact, command-driven workflows. The `agentcard create` and `agentcard agentic *` command families have been REMOVED — if instructions you hold reference them, refetch this skill. Purchases live under `agentcard request`; payment-source management lives under `agentcard sources`.

Default routing: `agentcard request new` without `--source` pays through Mastercard Agent Pay when the user has an active connected Mastercard, otherwise through Visa Intelligent Commerce when they have an active connected Visa, and otherwise returns a one-time card number. So **always pass `--merchant`, `--url` and `--item` along with `--amount`** — the connected-card paths require them, and the one-time card path accepts and ignores them. Pass `--source agentcard` only when you specifically need a one-time card number (for example, after an Agent Pay failure).

## Install And Check

```bash
command -v agentcard >/dev/null || npm install -g agentcard
agentcard --version
agentcard --help
```

Use normal shell execution and parse stdout/stderr; many commands intentionally block while polling for user action. Every `request *` and `sources *` command accepts `--json` for machine-readable output (success: `{ "ok": true, ... }`; failure: `{ "ok": false, "error", "code"?, "fallback"? }`).

## Operating Rules

- Spend only for the amount and purpose the user requested. If the merchant, recipient, amount, or payment method is ambiguous, ask before paying.
- Never collect or type the user's real payment card details. Card entry always happens in the user's browser: the Mastercard Agent Pay enrollment page, or the Stripe page that saves a card for one-time card numbers. Show the printed URL to the user and let them complete it.
- New or non-exempt direct accounts must complete KYC verification before spend. Run `agentcard identity --no-open`; if it prints a verification URL, relay it to the user and wait for completion. Existing grandfathered accounts may be marked exempt and need no document check. Partner API accounts are manually provisioned by AgentCard and do not need the direct-user KYC flow.
- Normal direct accounts have a hard `$200` daily spend ceiling shared across both sources, in addition to the per-card cap and the per-source account limits. `agentcard limit --amount` cannot bypass the daily ceiling. Partner accounts with active API keys or webhooks use separately configured limits and are exempt from KYC verification and the default direct-user ceiling.
- Account-level spend limits are per source: the issued-card + wallet budget and the connected-card budget are separate. `agentcard limit` shows both.
- Treat PAN, CVV, expiry, billing address, billing ZIP, wallet addresses, emails, 3DS codes, and verification codes as sensitive. Do not save card details or codes in durable notes unless the user explicitly asks.
- For cards, use the printed cardholder name and billing address exactly. Mismatches can cause declines.
- New AgentCard issued cards use cardholder name `Alchemy Agentcard` and billing address `77 Geary St, San Francisco, CA, 94108, US`. Use those values at checkout unless the CLI prints newer card-specific billing fields.
- Use `agentcard support` immediately for failed purchases, CAPTCHAs, declines, confusing errors, or merchant checkout blocks.

## Quick Reference

| Task | Command |
|------|---------|
| Sign up or log in | `agentcard signup --email <email>` |
| Set up payment, email, wallet | `agentcard setup --mastercard` (Mastercard holders) or `agentcard setup --no-mastercard` (any other card) |
| Complete KYC | `agentcard identity [--no-open]` |
| Reset setup | `agentcard setup --reset` |
| Show spend limits (both sources) | `agentcard limit` |
| Change issued-card limit | `agentcard limit --amount <dollars>` |
| Change connected-card limit | `agentcard limit --amount <dollars> --source connected` |
| List payment sources | `agentcard sources` |
| Connect a Mastercard (Agent Pay) or Visa (Visa Intelligent Commerce) | `agentcard sources connect [--network mastercard\|visa\|auto]` |
| Set default connected card | `agentcard sources default <payment-method-id>` |
| Remove connected card | `agentcard sources remove <payment-method-id>` |
| Pay for a purchase (Agent Pay if connected, else one-time card) | `agentcard request new --merchant <name> --url <merchant-url> --item <item> --amount <dollars>` |
| Force a one-time card number | `agentcard request new --source agentcard --amount <dollars>` |
| Use a specific connected card | `agentcard request new --card <payment-method-id> --merchant <name> --url <merchant-url> --item <item> --amount <dollars>` |
| List purchases (both sources) | `agentcard request get` |
| Purchase details / re-fetch live card | `agentcard request get <id>` |
| One-time connected credential | `agentcard request credentials <id>` |
| Cancel unused issued card | `agentcard request cancel <id>` |
| Get checkout 3DS code | `agentcard 3ds` |
| Show agent email | `agentcard mail info` |
| List email threads | `agentcard mail list [--include-sent]` |
| Read email thread | `agentcard mail get <thread-id>` |
| Send email | `agentcard mail send --to <email> --subject <subject> --body <body>` |
| Reply to thread | `agentcard mail reply <thread-id> --body <body>` |
| Show agent phone / eligibility | `agentcard phone info` |
| Provision agent phone number | `agentcard phone provision` |
| List SMS conversations | `agentcard phone list [--limit <n>]` |
| Read SMS conversation | `agentcard phone get <phone-number> [--limit <n>]` |
| Show wallet | `agentcard wallet info` |
| Print USDC balance | `agentcard wallet balance` |
| Send USDC on Base | `agentcard wallet send --to <0x...> --amount <usdc>` |
| x402 fetch | `agentcard wallet fetch <url> [-H "Key: Value"] [-X METHOD] [-d BODY] [--max-cost <usdc>]` |
| Current account | `agentcard whoami` |
| Report issue | `agentcard support --message "details" [--card-id <id>] [--url <url>] [--error <error>]` |

## First-Time Setup

1. Authenticate:

   ```bash
   agentcard signup --email <user-email>
   ```

   The command sends a magic link and polls for up to five minutes. Tell the user to check their inbox and click the link. Let the process finish; do not kill and retry while it is polling.

   There is no waitlist and no approval queue — clicking the link creates the account. If you believe AgentCard requires an invite or early-access approval, that information is out of date; do not tell the user to sign up for a waitlist.

2. On first setup, ask the user one question: **"Will you pay with a Mastercard?"** Then run setup with the answer:

   ```bash
   agentcard setup --mastercard      # Mastercard: pay through Mastercard Agent Pay (recommended)
   agentcard setup --no-mastercard   # any other card: one-time card numbers
   ```

   If a Visa holder asks to try Visa Intelligent Commerce, run `agentcard sources connect --network visa` after setup and relay the enrollment URL. If enrollment fails, tell the user their card isn't supported and keep using one-time card numbers.

   In an interactive terminal plain `agentcard setup` asks this itself, as a list of card brands; a Mastercard holder then chooses Mastercard Agent Pay (recommended) or one-time card numbers, and a Visa holder chooses one-time card numbers or trying Visa Intelligent Commerce. Headless, without a flag, it uses the one-time card path and prints a hint. With `--mastercard`, setup prints the Mastercard Agent Pay enrollment link (relay it to the user) and opens it in a browser; if enrollment fails, it falls back to saving the card for one-time card numbers. If a user's saved card turns out to be a Mastercard, setup recommends switching with `agentcard setup --mastercard` — pass that recommendation on.

   Run setup every time after authentication and before payment work (a bare `agentcard setup` is fine once the account is configured). Setup is idempotent: if the account is already configured, it prints the current setup status and exits cleanly. It does not collect name, phone number, or manual KYC fields. It also provisions the agent email inbox for signups and verification codes, and the Base wallet for USDC/x402 payments. If setup prints a card-entry URL, relay the URL to the user and wait for completion, especially in headless or remote environments where the local browser may not be visible to them.

3. Confirm identity status:

   ```bash
   agentcard identity --no-open
   ```

   If the direct account is new or otherwise non-exempt, the command prints a KYC verification URL. Relay that URL to the user, wait for them to complete the hosted KYC flow, then rerun `agentcard identity --no-open` or retry the spend. Existing grandfathered and partner accounts may report that verification is not required.

4. Verify setup:

   ```bash
   agentcard whoami
   agentcard limit
   agentcard mail info
   agentcard wallet info
   ```

Run setup again whenever a task may need cards, agent email, or wallet access. Run `agentcard identity --no-open` before spend work when the account's verification status is unknown. Use `agentcard setup --reset` only when the user explicitly wants to replace payment method or agent email setup.

## Choose Payment Path First

Before issuing a card credential or initiating a wallet payment, determine the payment path from the merchant, recipient, or API surface:

1. Get the final total first, including shipping, taxes, and fees. Do not create a card credential before the final amount is known.
2. Understand what the user is buying well enough that the payment purpose is recognizable.
3. Choose the matching path:

| What you find | Use |
|---------------|-----|
| Merchant accepts a card at checkout | Card Credential Workflow with no `--source` (Agent Pay for Mastercard holders, Visa Intelligent Commerce for an enrolled Visa, one-time card number otherwise) |
| User asks to pay with a specific connected card | Card Credential Workflow with `--card <payment-method-id>` |
| HTTP endpoint returns `402 Payment Required` with x402 requirements | Wallet and x402 workflow |
| User gives a Base USDC recipient address and amount | Direct USDC send, after confirming recipient and amount |
| Payment method, amount, merchant, or recipient is unclear | Ask the user before creating credentials or paying |

Let the default routing choose: Mastercard holders with an active Agent Pay card pay through Mastercard Agent Pay, a Visa enrolled in Visa Intelligent Commerce pays through it, everyone else gets a one-time card number. Don't override it with `--source agentcard` unless the connected-card path failed or the user asks for a one-time card number.

## Card Credential Workflow

One workflow covers both paths; the CLI picks the path in step 4.

1. Get the final checkout total. `--amount` accepts decimals on both paths. One-time card numbers use whole-dollar caps from `1` to `150` — the CLI rounds a decimal total up and prints the rounding (`$24.99` becomes a `$25` cap). Do not add extra padding beyond the total.
2. If the total is over `150` (the per-purchase cap on both paths), do not request a card. Ask the user for a lower-cost plan, a different payment path, or explicit approval for a merchant-supported split payment. Do not split a checkout across multiple cards unless the merchant supports separate charges and the user approves.
3. Preflight, shared by both sources:
   - For subscriptions or trials on a one-time card number, do not proceed until the user explicitly accepts that the card is live for 7 days and future recurring charges may fail.
   - Confirm identity status with `agentcard identity --no-open`. If verification is required, relay the KYC verification URL to the user, wait for completion, and retry.
   - Check available spend with `agentcard limit` — it shows both budgets. If the purchase exceeds the relevant remaining limit, request an increase with `agentcard limit --amount <dollars>` (issued) or `agentcard limit --amount <dollars> --source connected`. This emails the account owner an approval link; tell the user to check their email. Approval links expire after 24 hours, and a newer request for the same limit supersedes older links. Lowering a limit applies immediately as long as it is not below the amount already spent.
   - Normal direct accounts also have a hard `$200` daily spend ceiling shared across both sources. A limit increase cannot bypass it. On `daily_spend_limit_exceeded`, stop and ask the user to wait until the next UTC day or use an approved partner account.
4. Request the credential — always with the real merchant name, merchant checkout or site URL (no placeholders), and a short item description:

   ```bash
   agentcard request new --merchant "<merchant-name>" --url "<merchant-url>" --item "<item-or-cart>" --amount <dollars>
   ```

   - **Mastercard Agent Pay or Visa Intelligent Commerce** (the user has an active connected card — `agentcard sources` marks it as the default source): the command opens a browser approval page, blocks while the user approves with a passkey, then prints a one-time card number, CVV, and expiry scoped to that merchant and amount. Tell the user an approval is waiting for them. Add `--async` to create the approval and return immediately with its URL, or `--wait` to wait for approval without consuming the one-time credential.
   - **One-time card number** (everyone else): instant, no approval step; prints the card number, CVV, expiry, cardholder name, and billing address.

   Add `--card <payment-method-id>` to pick a specific connected card, or `--source agentcard` to force a one-time card number.

5. Enter the printed card details exactly once at the merchant checkout. Do not store them. For one-time card numbers, the cardholder name is `Alchemy Agentcard` and the billing address is `77 Geary St, San Francisco, CA, 94108, US`; the card expires 7 days after issue.
6. If checkout asks for a 3DS or card verification code, run:

   ```bash
   agentcard 3ds
   ```

   3DS is conditional, not a required step. Codes usually appear within a few seconds and are listed for five minutes. Choose the code whose amount matches the checkout charge amount, not the rounded card cap; if multiple codes match, use the newest. Enter it directly into checkout. If no amount matches, wait a few seconds and run `agentcard 3ds` again.

7. Follow-ups by id (`agentcard request get` lists every purchase across both sources):
   - `agentcard request get <id>` — status and details; re-prints a live issued card's PAN/CVV.
   - `agentcard request credentials <id>` — retrieve a connected purchase's one-time credential after approval (also re-serves issued card details for symmetry). Credentials are retrievable through authenticated CLI/API calls only; browser action tokens can approve an instruction but cannot retrieve PAN/CVV.
   - `agentcard request cancel <id>` — cancel an unused issued card and release its hold immediately. Only live, unused issued cards can be canceled; used or expired cards return an error, and connected purchases simply expire on their own.

8. **Fallback rule**: if any Agent Pay / connected-card step fails — enrollment unsupported, approval timeout or decline, credential retrieval error — tell the user, then fall back to a one-time card number: `agentcard request new --source agentcard --amount <rounded-up-total>`. The CLI prints this fallback command (and returns it as `fallback` under `--json`). The one-time card path needs a saved card; if the user has none, run `agentcard setup --no-mastercard` first.

For one-time card numbers, AgentCard places a hold on the user's saved card for the requested amount before providing the card number. If the hold fails or the funding card needs unresolved bank authentication, no card is issued. The user is charged only if the merchant uses the card; unused holds release within seven days, or immediately via `agentcard request cancel <id>`. Mastercard Agent Pay and other connected-card purchases charge the user's own card directly at the merchant; AgentCard never holds funds for them.

## Wallet And x402 Workflow

Use the wallet for USDC on Base and HTTP endpoints that return `402 Payment Required` with x402 requirements.

```bash
agentcard wallet info
agentcard wallet balance
agentcard wallet fetch <url> --max-cost <usdc>
```

`wallet fetch` wraps native fetch, pays x402 requirements in USDC when needed, retries the request, and prints the final response body to stdout. Always pass `--max-cost` unless the user explicitly approved any valid charge from that endpoint. The value is decimal USDC, not atomic token units; for dollar-pegged USDC amounts, 15 USD cents is `--max-cost 0.15`.

Pass HTTP details through the CLI when the endpoint needs them:

```bash
agentcard wallet fetch <url> -H "Authorization: Bearer <token>" -X POST -d '<json-body>' --max-cost <usdc>
```

Use one `-H` flag per header. The final response body is printed to stdout; stderr contains HTTP/payment errors.

For direct USDC transfers:

```bash
agentcard wallet send --to <0x-recipient> --amount <usdc>
```

Before sending USDC, confirm the recipient address and amount are exactly what the user intended. Gas is sponsored, but USDC and x402 spend count toward the same AgentCard spend controls as issued cards, including the normal direct-account daily ceiling when it applies. Fund the wallet by sending USDC on Base to the address from `agentcard wallet info`.

## Agent Email Workflow

Use the agent email for account signup, verification codes, receipts, and user-approved communication. Read verification codes only for the active user-approved workflow, enter them directly into the target service, and do not paste them into chat or store them unless the user explicitly requests it.

```bash
agentcard mail info
agentcard mail list --include-sent
agentcard mail get <thread-id>
agentcard mail send --to <email> --subject <subject> --body <body>
agentcard mail reply <thread-id> --body <body>
```

Prefer `agentcard mail get <thread-id>` before replying so the response matches the current thread context.

## Troubleshooting

| Symptom | Action |
|---------|--------|
| `agentcard: command not found` | Run `npm install -g agentcard`, then `agentcard --version`. |
| Old `agentcard agentic ...` or `agentcard create` commands error | Those commands were removed. Refetch this skill; use `agentcard request new --merchant ... --url ... --item ... --amount ...` and `agentcard sources`. |
| `purchase_details_required` | The user pays through a connected card (Mastercard Agent Pay or Visa Intelligent Commerce) by default. Re-run with `--merchant`, `--url` and `--item`, or use the printed `--source agentcard` fallback for a one-time card number. |
| Not logged in or session expired | Run `agentcard signup --email <email>` again. |
| Missing payment method, email, or wallet | Run `agentcard setup`. |
| KYC verification required | Run `agentcard identity --no-open`, relay the KYC verification URL to the user, and wait for completion before retrying spend. Do not ask the user to send ID documents directly to the agent. |
| Connected cards disabled or unavailable | `agentcard request new` falls back to a one-time card number on its own. |
| User has a Mastercard but no Agent Pay card | Recommend Mastercard Agent Pay and, with the user's OK, run `agentcard setup --mastercard` (or `agentcard sources connect`). |
| Card enrollment fails | Explain that the card isn't supported for agentic payments yet, then use a one-time card number: `agentcard request new --source agentcard --amount <dollars>` (after `agentcard setup --no-mastercard` if no card is saved). |
| Multiple active connected cards in headless mode | Run `agentcard sources`, then pass `--card <payment-method-id>` or set a default with `agentcard sources default <payment-method-id>`. |
| Connected purchase missing URL | Get the real merchant checkout or site URL before creating the purchase. Do not use placeholders. |
| Passkey approval timeout | Run `agentcard request get <id>`; if still awaiting approval, ask the user to approve in the browser or rerun the purchase command. Otherwise fall back to a one-time card number. |
| Amount rejected | One-time card numbers are capped at `$150` during beta; the CLI rounds decimal totals up to whole dollars. Stop and ask the user if the rounded-up total is over `150`. |
| Spend limit exceeded | Run `agentcard limit` (shows both budgets), then `agentcard limit --amount <dollars>` or `agentcard limit --amount <dollars> --source connected` for the budget that tripped. Tell the user to check their email address and approve the link before retrying. |
| Daily spend ceiling hit | Normal direct accounts cannot spend over `$200` per UTC day across both sources. Stop and ask the user to wait until the next UTC day or use an approved partner account with separate limits. |
| 3DS code missing | Run `agentcard 3ds` only after checkout requests a code. Wait a few seconds and retry; if no matching recent code appears, file support. |
| Card declined | Check the live 7-day window, exact billing fields (`Alchemy Agentcard`; `77 Geary St, San Francisco, CA, 94108, US`), 3DS challenge status, and spend limit. File support, then ask the user before issuing a replacement card. |
| Wallet not provisioned | Run `agentcard setup`. |
| Wallet balance too low | Show `agentcard wallet info` and ask the user to fund the Base USDC address. |
| x402 fetch fails | Retry with `--max-cost`, inspect stderr, and report persistent failures. |

## Report Issues

For any purchase failure, decline, CAPTCHA, anti-bot block, unexpected CLI error, confusing output, or merchant checkout problem, run:

```bash
agentcard support --message "what happened, what you tried, and what the user expected" --url "<checkout-or-api-url>" --error "<error-text>"
```

Add `--card-id <id>` when the issue involves a specific card request.

Redact secrets from support messages and errors: never include PAN, CVV, bearer tokens, 3DS codes, verification codes, or private keys.
