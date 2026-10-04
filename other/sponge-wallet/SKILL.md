---
name: sponge-wallet
version: 0.2.2
description: Crypto wallet, token swaps, cross-chain bridges, and access to paid external services (search, image gen, web scraping, AI, and more) via x402 payments.
homepage: https://wallet.paysponge.com
metadata:
  openclaw:
    emoji: "\U0001F9FD"
    category: finance
    primaryEnv: SPONGE_API_KEY
    requires:
      env:
        - SPONGE_API_KEY
---

# Sponge Wallet API — Agent Skills Guide (OpenClawd Edition)

This skill gives Clawd access to the Sponge Wallet REST API — a full crypto wallet
with swaps, bridges, trading, payments, banking, and paid external services.

## Quick Start

```bash
# Base URL
SPONGE_API_URL="https://api.wallet.paysponge.com"
SPONGE_API_KEY="sponge_live_..."  # set in .env or export

# Required header on every request
# Sponge-Version: 0.2.2
# Authorization: Bearer $SPONGE_API_KEY
# Content-Type: application/json
```

## What You Can Do

1. **Manage crypto** — check balances, transfer tokens (EVM/Solana/Tempo), swap on Solana/Base/Ethereum/Polygon/Arbitrum/Tempo, bridge cross-chain
2. **Create payment links** — generate reusable x402 payment URLs
3. **Access paid external services** — search, image gen, web scraping, AI, data enrichment
4. **Banking** — KYC onboarding, virtual bank accounts (receive USD as USDC), off-ramp to bank
5. **Trade** — Polymarket prediction markets, Hyperliquid perpetuals
6. **Checkout** — shop from online stores via URL checkout
7. **Store cards** — encrypted card data for checkout, virtual cards, Sponge Card
8. **Fiat onramp** — buy crypto with card/bank via Stripe or Coinbase

## Top-Level API Reference

```
Base:   https://api.wallet.paysponge.com
Auth:   Authorization: Bearer <SPONGE_API_KEY>
Ver:    Sponge-Version: 0.2.2  (REQUIRED on every request)

Paid services (search, image gen, scraping, AI, data, etc.):
  GET  /api/discover                     -> find services by query/category
  GET  /api/discover/:serviceId          -> get endpoints, params, pricing
  POST /api/paid/fetch                   -> call service (auto-selects x402 or MPP)
  POST /api/x402/fetch                   -> call service (x402 USDC only)
  POST /api/mpp/fetch                    -> call service (MPP on Tempo)

Wallet & tokens:
  GET  /api/balances                     -> get all balances
  POST /api/transfers/evm                -> EVM transfer (ETH/USDC)
  POST /api/transfers/solana             -> Solana transfer (SOL/USDC)
  POST /api/transfers/tempo              -> Tempo transfer (pathUSD etc.)
  POST /api/transactions/swap            -> Solana/EVM swap
  POST /api/transactions/base-swap       -> Base swap
  POST /api/transactions/tempo-swap      -> Tempo swap
  POST /api/transactions/bridge          -> cross-chain bridge
  GET  /api/solana/tokens                -> list SPL tokens
  GET  /api/solana/tokens/search         -> search Jupiter token list
  GET  /api/transactions/status/:txHash  -> transaction status
  GET  /api/transactions/history         -> transaction history

Trading:
  POST /api/polymarket                   -> Polymarket prediction markets
  POST /api/hyperliquid                  -> Hyperliquid perps/spot

Banking:
  POST /api/bank/onboard                 -> start KYC
  GET  /api/bank/status                  -> KYC status
  POST /api/bank/virtual-account         -> create virtual bank account
  GET  /api/bank/external-accounts       -> list linked bank accounts
  POST /api/bank/external-accounts       -> link bank account
  POST /api/bank/send                    -> off-ramp USD to bank

Cards & checkout:
  POST /api/cards                        -> fetch user's card
  POST /api/virtual-cards                -> issue per-transaction virtual card
  POST /api/checkout                     -> URL checkout from online stores
  GET  /api/checkout/:sessionId          -> checkout status
  POST /api/credit-cards                 -> store encrypted card data
  POST /api/onramp/crypto                -> fiat-to-crypto onramp link

Planning:
  POST /api/plans/submit                 -> submit multi-step plan
  POST /api/plans/approve                -> approve and execute plan
  POST /api/trades/propose               -> propose single swap
```

## Authentication

### For AI Agents — Use `register`, NOT `login`

Register with agent-first mode to get an API key immediately:

```bash
curl -sS -X POST "https://api.wallet.paysponge.com/api/agents/register" \
  -H "Sponge-Version: 0.2.2" \
  -H "Content-Type: application/json" \
  -d '{"name":"Clawd","agentFirst":true}'
```

Returns `apiKey` immediately in agent-first mode. Store it in `~/.spongewallet/credentials.json`.

### Human Login (only for existing accounts)

```bash
# Step 1: Request device code
curl -sS -X POST "https://api.wallet.paysponge.com/api/oauth/device/authorization" \
  -H "Sponge-Version: 0.2.2" \
  -H "Content-Type: application/json" \
  -d '{"clientId":"spongewallet-skill"}'

# Step 2: Poll for token
curl -sS -X POST "https://api.wallet.paysponge.com/api/oauth/device/token" \
  -H "Sponge-Version: 0.2.2" \
  -H "Content-Type: application/json" \
  -d '{
    "grantType":"urn:ietf:params:oauth:grant-type:device_code",
    "deviceCode":"<deviceCode>",
    "clientId":"spongewallet-skill"
  }'
```

### Standard Credential Storage

Store credentials in `~/.spongewallet/credentials.json`:
```json
{
  "apiKey": "sponge_live_...",
  "claimCode": "ABCD-1234",
  "claimUrl": "https://wallet.paysponge.com/device?code=ABCD-1234"
}
```

## Common Operations

### Check Balances
```bash
curl -sS "https://api.wallet.paysponge.com/api/balances?chain=base" \
  -H "Authorization: Bearer $SPONGE_API_KEY" \
  -H "Sponge-Version: 0.2.2"
```

### Transfer USDC on Base
```bash
curl -sS -X POST "https://api.wallet.paysponge.com/api/transfers/evm" \
  -H "Authorization: Bearer $SPONGE_API_KEY" \
  -H "Sponge-Version: 0.2.2" \
  -H "Content-Type: application/json" \
  -d '{"chain":"base","to":"0x...","amount":"10","currency":"USDC"}'
```

### Swap on Solana
```bash
curl -sS -X POST "https://api.wallet.paysponge.com/api/transactions/swap" \
  -H "Authorization: Bearer $SPONGE_API_KEY" \
  -H "Sponge-Version: 0.2.2" \
  -H "Content-Type: application/json" \
  -d '{"chain":"solana","inputToken":"SOL","outputToken":"USDC","amount":"0.1","slippageBps":50}'
```

### Paid Services (3-Step Flow)

**Step 1** — Find a service:
```bash
curl -sS "https://api.wallet.paysponge.com/api/discover?query=web+scraping" \
  -H "Authorization: Bearer $SPONGE_API_KEY" \
  -H "Sponge-Version: 0.2.2"
```

**Step 2** — Get service details (DO NOT SKIP):
```bash
curl -sS "https://api.wallet.paysponge.com/api/discover/{serviceId}" \
  -H "Authorization: Bearer $SPONGE_API_KEY" \
  -H "Sponge-Version: 0.2.2"
```

**Step 3** — Call the endpoint:
```bash
curl -sS -X POST "https://api.wallet.paysponge.com/api/paid/fetch" \
  -H "Authorization: Bearer $SPONGE_API_KEY" \
  -H "Sponge-Version: 0.2.2" \
  -H "Content-Type: application/json" \
  -d '{"url":"<url_from_step2>","method":"POST","body":{...},"chain":"base"}'
```

### Bridge USDC to Hyperliquid for Trading
```bash
curl -sS -X POST "https://api.wallet.paysponge.com/api/transactions/bridge" \
  -H "Authorization: Bearer $SPONGE_API_KEY" \
  -H "Sponge-Version: 0.2.2" \
  -H "Content-Type: application/json" \
  -d '{"sourceChain":"base","destinationChain":"hyperliquid","token":"USDC","amount":"50"}'
```

### Trade on Hyperliquid
```bash
curl -sS -X POST "https://api.wallet.paysponge.com/api/hyperliquid" \
  -H "Authorization: Bearer $SPONGE_API_KEY" \
  -H "Sponge-Version: 0.2.2" \
  -H "Content-Type: application/json" \
  -d '{"action":"order","symbol":"ETH","side":"buy","type":"limit","amount":"0.1","price":"3000"}'
```

## Chain Reference

Supported chains: `ethereum`, `base`, `polygon`, `arbitrum-one`, `tempo`, `solana`

## Error Handling

| Status | Meaning | Common Cause |
|--------|---------|--------------|
| 400 | Bad Request | Missing/invalid fields |
| 401 | Unauthorized | Missing or invalid API key |
| 403 | Forbidden | Permission denied |
| 404 | Not Found | Resource does not exist |
| 429 | Rate Limited | Too many requests |
| 500 | Server Error | Transient; retry later |

## Security

- Never share your API key in logs, posts, or screenshots
- Store API key in environment variable `SPONGE_API_KEY`
- Rotate the key if exposure is suspected
- Use `sponge_test_*` keys for development, `sponge_live_*` for production

## Integration with Clawd

The Sponge Wallet can be used by Clawd in two ways:

1. **Direct REST calls** — use `fetch_url` tool or `curl` via shell to hit the Sponge API
2. **MCP Server** — connect to `https://api.wallet.paysponge.com/mcp` with `Authorization: Bearer $SPONGE_API_KEY` header for structured tool access
