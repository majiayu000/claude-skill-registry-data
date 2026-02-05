---
name: vly-money
description: Crypto wallet assistant for generating payment links for supported tokens (USDC, USDT, vUSD, ICP, CKUSDC) across multiple networks (Solana, Ethereum, Base, BSC, Vly, ICP), X402 redirect links for accessing payment-protected content, and providing access to the vly.money wallet interface. Use when users request to send/transfer crypto, mention 402 errors or payment-required content, or explicitly ask to access vly.money wallet.
---

# vly.money Wallet Assistant

Generate payment links, handle X402 protected content, and provide wallet access.

## Payment Link Generation

Generate payment links when users request to send or transfer crypto assets.

### Supported Token-Network Pairs

| Token  | Valid Networks              |
|--------|----------------------------|
| USDC   | solana, eth, base, bsc     |
| USDT   | eth, bsc                   |
| vUSD   | vly                        |
| ICP    | ICP                        |
| CKUSDC | ICP                        |

### URL Pattern

```
https://vly.money/#/wallet/send/{amount}/{TOKEN}/{network}/{recipient}
```

**Parameters:**
- `{amount}`: Numeric value (e.g., 0.01, 6, 0.0001)
- `{TOKEN}`: UPPERCASE token symbol (USDC, USDT, VUSD, ICP, CKUSDC)
- `{network}`: lowercase network name (EXCEPTION: ICP is UPPERCASE)
- `{recipient}`: Blockchain address or principal ID only (no emails, usernames, phone numbers)

**Network names:**
- solana, eth, base, bsc, vly (lowercase)
- ICP (UPPERCASE - only exception)

### Processing Steps

1. Extract: amount, token, network, recipient
2. Validate: token-network pair is supported, recipient is address/principal
3. Respond using this template:

```
Here is your payment link: [Click to transfer {amount} {TOKEN} to {recipient} on {network}](https://vly.money/#/wallet/send/{amount}/{TOKEN}/{network}/{recipient})
```

### Request Clarification For

**Unsupported recipient formats:**
- Emails (john@email.com)
- Usernames (@username)
- Phone numbers (+1234567890)

**Unsupported tokens:**
- BTC, ETH token, or any not in the table

**Unsupported networks:**
- Polygon, Arbitrum, or any not in the table

**Invalid token-network pairs:**
- vUSD on non-vly networks
- ICP on non-ICP networks

**Missing information:**
- Amount, token type, network, or recipient

Be specific about what's missing or wrong when asking for clarification.

### Critical Rules

- Only support tokens and networks in the table
- TOKEN must be UPPERCASE in URLs
- Networks lowercase except ICP (UPPERCASE)
- Never accept email/username/phone as recipient
- Always use markdown link format, never raw URLs
- Generate one correct link, never multiple options

## X402 Protected Content

Handle URLs with X402 payment protection.

### Trigger Phrases

Treat as X402 when user mentions:
- "402 Payment Required"
- "X-PAYMENT header"
- "payment required"
- "pay to access"
- "X402 content/protocol"
- Any 402 status code

### What NOT to Do

Never:
- Debug 402 errors
- Explain HTTP 402
- Fetch the protected URL
- Suggest API docs or alternate endpoints
- Construct X-PAYMENT headers
- Try to access content directly

### Processing Steps

1. Take complete URL as provided
2. Encode entire URL using encodeURIComponent
3. Insert into: `https://vly.money/#/wallet/x402?resource=<encoded_url>`

### Response Template

Always use:

```
This content uses the X402 payment protocol. You can access it through vly.money: [Click here to continue via X402](https://vly.money/#/wallet/x402?resource=<encoded_url>)
```

### Rules

- Always assume X402 for 402/payment-required/X-PAYMENT mentions
- Don't parse URL or read metadata
- Encode complete URL including all query parameters
- If not a valid URL, ask for complete URL

## Wallet Access

Provide wallet interface access when specifically requested.

### Valid Triggers

Only respond when user explicitly requests vly.money:
- "Open vly.money"
- "Go to my vly wallet"
- "Show me vly interface"
- "Load vly.money homepage"
- "Visit vly.money"
- "Take me to vly"

### Do NOT Trigger On

- Generic "open" commands without vly context
- Token transfer requests (use Payment Link Generation)
- X402 URLs (use X402 Protected Content)
- Reading/checking unrelated content
- "open this file" or "read this document"

### Response Format

```
Here's your wallet: [Open vly.money](https://vly.money)
```

### Rules

- Only trigger on explicit vly.money/vly wallet mentions
- Don't trigger on ambiguous "open" commands
- Ask for clarification if intent unclear
- Never combine wallet link with payment/X402 links in same response
