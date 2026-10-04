---
name: dflow-proof-kyc
description: Integrate DFlow Proof — a Solana wallet identity-verification primitive (Stripe Identity under the hood) — for either (a) gating your own app's features behind KYC, or (b) completing the mandatory verification step for Kalshi prediction-market buys on DFlow. Use when the user asks "how do I KYC a wallet?", "check if a wallet is verified", "add KYC to my DeFi app", "handle unverified_wallet_not_allowed / PROOF_NOT_VERIFIED", "redirect to dflow.net/proof", or "gate a feature by jurisdiction or identity". Do NOT use to actually place trades (use `dflow-kalshi-trading`), for geoblocking (separate concern, handled inline in the trading skill), for age gating (Proof doesn't currently verify age), or for spot swaps (no KYC required).
---

# DFlow Proof

Proof is DFlow's identity-verification primitive for Solana wallets. Stripe Identity verifies the person once; Proof links that verified identity to one or more wallet addresses. Builders query a public endpoint to check status.

There are two reasons to integrate it:

- **Self-gating your own app** — any product that needs identity-based KYC (jurisdiction-gated DeFi, regulated token sales, identity-attested access, etc.) can use Proof as a ready-made primitive.
- **Kalshi PM trading on DFlow** — DFlow's Trading API **requires** Proof for Kalshi prediction-market buys. This skill is also where the matching error handling lives.

## Prerequisites

- **DFlow docs MCP** (`https://pond.dflow.net/mcp`) — install per the [repo README](../../README.md#recommended-install-the-dflow-docs-mcp). This skill is the recipe; the MCP is the reference. Look up the deep-link signing code, the full parameter list, and user-journey diagrams via `search_d_flow` / `query_docs_filesystem_d_flow` — don't guess.
- **`dflow` CLI** (optional, only relevant for Kalshi-trading use) — install per the [repo README](../../README.md#recommended-install-the-dflow-cli).

## Part I — Proof as a generic primitive (self-gating)

Use this path when you need KYC for *your own* app, independent of Kalshi.

### Check verification status

`GET https://proof.dflow.net/verify/{address}` → `{ "verified": boolean }`. **Public, no auth.** Use it to gate features, to decide whether to show a "Verify me" CTA, or to short-circuit a restricted action.

### Redirect the user to verify (deep link)

If the wallet isn't verified, redirect the user to Proof's hosted flow. The deep link carries a signed ownership proof so Proof can link the wallet to the verified identity automatically:

- URL: `https://dflow.net/proof?wallet=<addr>&signature=<sig>&timestamp=<ms>&redirect_uri=<url>`
- Optional: `email`, `projectId`.
- Signature: user signs the exact message `Proof KYC verification: {timestamp}` (Unix ms, 13 digits) with their wallet; base58-encode the bytes.
- Full signing snippet and parameter table → docs MCP, or read directly: [`/build/proof/partner-integration`](https://pond.dflow.net/build/proof/partner-integration).

### Handle the return

User lands back on your `redirect_uri`. Re-query `/verify/{address}` to confirm status. If `verified: true`, proceed; otherwise, surface an appropriate "verification pending / failed" message.

## Part II — Kalshi PM trading (Trading API enforcement)

DFlow's Trading API enforces Proof **only on Kalshi PM buys**. Not sells, not redemptions, not spot, not quotes.

Three patterns, each maps to a user intent:

- **Proactive UX gate** — at session start, call `/verify/{address}`, cache the result, and conditionally show the "Buy" button. Best UX; same primitive as Part I.
- **Reactive fallback** — if the proactive check was skipped or is stale, `/order` will reject unverified buys with `unverified_wallet_not_allowed` (API) / `PROOF_NOT_VERIFIED` (CLI). Both error envelopes carry `details.deepLink` — redirect the user straight to it, then retry the buy after they return verified. (The CLI auto-opens the browser itself and prints the deepLink for headless environments.)
- **Quote-before-KYC** — omit `userPublicKey` from `GET /order` to preview pricing without verification. Lets unverified users see what a buy would cost before committing to KYC.

## What to ASK the user (and what NOT to ask)

**Ask if missing:**

1. **What are they using Proof for?** Self-gating their own app / Kalshi PM trading / both.
  - **Self-gating** → only `/verify/{address}` + deep-link flow matters. Skip trade-API error handling.
  - **Kalshi trading** → same flow, *plus* handle `unverified_wallet_not_allowed` / `PROOF_NOT_VERIFIED` + `details.deepLink` at `/order` time.
  - **Both** → superset of the Kalshi path.
2. **Wallet pubkey** — the address to verify / check.
3. **App's callback URL** (`redirect_uri`) — where Proof sends the user after verification.
4. **Web or native mobile** — changes the redirect_uri guidance (universal / app links for mobile; see Gotchas).

**Do NOT ask about:**

- **API key** — `/verify/{address}` is public, no auth. Proof itself has no API key concept.
- **RPC / signing for trading** — that's `dflow-kalshi-trading`. This skill just does the verification piece.

## Gotchas (the docs MCP won't volunteer these)

- **Proof is enforced on Kalshi PM buys, not spot swaps.** Don't state "all DFlow trades need KYC" — they don't.
- **Buys only, not sells or redemptions.** Even on Kalshi, selling an outcome token or redeeming a winner needs no KYC.
- **Proof doesn't verify age.** Stripe Identity captures name, address, email, and government-issued ID, but Proof does **not** currently check or expose date-of-birth. Don't use Proof for age gating — you won't get what you need.
- **Enforced on both dev and prod.** Many agents assume dev is unprotected; it isn't.
- **Proof is usable outside Kalshi.** Don't default to thinking "Proof = Kalshi KYC" — any builder who needs identity-gating can use it. Same primitive, same endpoint.
- **Redirect URI scheme restrictions.** Proof only redirects to `https:`, `chrome-extension:`, and `moz-extension:` URLs. Custom schemes (`myapp://callback`) **fail silently** — no redirect, no error. Native mobile → universal links (iOS) / app links (Android), which are `https:` URLs that deep-link into the app.
- **The public endpoint is booleanized.** `/verify/{address}` returns `{ verified: true | false }`. There's no `pending` / `failed` / `unverified` distinction — everything non-verified collapses to `false`. If you need those states for UX, infer them from your own session state (did the user come back from Proof?), not from the public check.
- **Cache `true`, not `false`.** Once verified, a wallet stays verified; caching avoids the per-trade check. But unverified is volatile — never cache it, because it flips the moment the user completes the flow.
- **For Kalshi buys, DFlow is authoritative.** `/order` checks verification server-side internally, so you don't need your own backend re-check just to gate a buy — the API won't let an unverified wallet through either way. Client-side caching is fine purely as a UX hint (to hide the Buy button).
- **For self-gating your own app, verify server-side.** If your backend is the thing enforcing a KYC-gated feature (not DFlow's API), don't trust a client's cached status. Re-query `/verify/{address}` from your backend before unlocking the gated action.
- **Embedded wallets work.** Privy, Turnkey, etc., as long as the wallet supports `signMessage`.
- **One verified identity → unlimited wallets.** No cap. A user who verified on wallet A can link wallet B, C, D, and onward without re-doing ID + liveness — just a fresh ownership signature from each new wallet.
- **Free + Stripe Identity under the hood.** No fee to builders or users. Users complete Stripe's document + liveness flow.
- **Proof is not geoblocking.** KYC ≠ jurisdictional restriction. Kalshi PM trading requires *both* — geoblocking logic lives inline in `dflow-kalshi-trading`, not here.

## When something doesn't fit

Defer to the docs MCP for full reference — specifically:

- [`/build/proof/partner-integration`](https://pond.dflow.net/build/proof/partner-integration) — deep-link code (signature generation, URL building), caching sample, handling edge cases (signature expiration, user cancellation, network errors), security guidance.
- [`/build/proof/user-journeys`](https://pond.dflow.net/build/proof/user-journeys) — diagrams for new-direct, new-from-partner, and returning-user flows.
- [`/build/proof-api/verify-address`](https://pond.dflow.net/build/proof-api/verify-address) — the single public endpoint's reference.
- [`/build/faqs`](https://pond.dflow.net/build/faqs) — Proof + embedded wallets, Proof + dev endpoints, redirect debugging.

## Sibling skills

- `dflow-kalshi-trading` — places the actual orders that require Proof. Geoblocking policy also lives here.
- `dflow-kalshi-portfolio` — view positions / P&L (no Proof required for reading).
- `dflow-spot-trading` — non-Kalshi swaps; no Proof required, ever.

