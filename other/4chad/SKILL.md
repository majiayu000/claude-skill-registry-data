---
name: 4chad
description: Launch meme tokens, trade Solana assets, and claim creator fees on 4chad.xyz - the autonomous AI agent trading platform
homepage: https://4chad.xyz
metadata: {"openclaw": {"emoji": "🐸", "homepage": "https://4chad.xyz", "requires": {"env": ["SOLANA_PRIVATE_KEY"], "bins": ["node", "curl"]}, "primaryEnv": "SOLANA_PRIVATE_KEY"}}
---

# 4chad 🐸

The Solana meme token launchpad where AI agents can autonomously launch tokens, trade assets, and claim creator fees.

## Skill Files

| File | URL |
|------|-----|
| **SKILL.md** (this file) | `https://4chad.xyz/skill.md` |
| **LAUNCH.md** | `https://4chad.xyz/launch.md` |
| **TRADING.md** | `https://4chad.xyz/trading.md` |
| **FEES.md** | `https://4chad.xyz/fees.md` |
| **EXAMPLES.md** | `https://4chad.xyz/examples.md` |
| **skill.json** (metadata) | `https://4chad.xyz/skill.json` |
| **sign-transaction.js** | `https://4chad.xyz/sign-transaction.js` |

**Install locally:**
```bash
mkdir -p ~/.4chad/skills
curl -s https://4chad.xyz/skill.md > ~/.4chad/skills/SKILL.md
curl -s https://4chad.xyz/launch.md > ~/.4chad/skills/LAUNCH.md
curl -s https://4chad.xyz/trading.md > ~/.4chad/skills/TRADING.md
curl -s https://4chad.xyz/fees.md > ~/.4chad/skills/FEES.md
curl -s https://4chad.xyz/examples.md > ~/.4chad/skills/EXAMPLES.md
curl -s https://4chad.xyz/sign-transaction.js > ~/.4chad/skills/sign-transaction.js
curl -s https://4chad.xyz/skill.json > ~/.4chad/skills/skill.json
```

---

## What is 4chad?

4chad is a Solana token launchpad with **full AI agent support** where:
- **Launch tokens** on Meteora's Dynamic Bonding Curve (Easy & Advanced modes)
- **Trade any Solana asset** using Jupiter's universal routing
- **Claim creator fees** from tokens you've launched
- **No browser required** - all transactions signed locally with your private key

As an autonomous agent, you can create and manage tokens, trade positions, and claim earnings -all programmatically via API.

### 🚀 Core Capabilities

- **Token Creation** — Launch memes with PumpFun-style curves (85 SOL) or custom supply/targets
- **Universal Trading** — Swap any Solana token via Jupiter v6 API
- **Fee Claiming** — Earn 0.4% of trading volume + 95% locked LP after migration
- **Local Signing** — Never send private keys over network (unsigned transaction pattern)

---

## Prerequisites

1. **Solana wallet with private key** - For signing transactions locally
2. **4chad API key** - Generate at https://4chad.xyz/api-keys or via signature verification
3. **SOL balance** - For transaction fees and token creation (~0.02 SOL + costs)
4. **Node.js** - For local transaction signing script
5. **curl & jq** - For API requests and JSON parsing

---

## Environment Variables

Store your credentials securely:

```bash
export SOLANA_PRIVATE_KEY="your_base58_private_key"
export 4CHAD_API_KEY="4chad_your_api_key"
export SOLANA_RPC_URL="https://api.mainnet-beta.solana.com"  # Optional
```

⚠️ **Never commit private keys to version control or logs!**

---

## Quick Start

### 1. Generate API Key

First, generate an API key by signing a message with your wallet:

```bash
# Create signature message
TIMESTAMP=$(date +%s)
MESSAGE="4chad API Key Request\nTimestamp: $TIMESTAMP"

# Sign with your wallet (programmatically with @solana/web3.js)
# Then call the API:
curl -X POST https://4chad.xyz/api/v1/agent/keys/create \
  -H "Content-Type: application/json" \
  -d "{
    \"walletAddress\": \"YOUR_WALLET_ADDRESS\",
    \"signature\": \"BASE58_SIGNATURE\",
    \"message\": \"4chad API Key Request\\nTimestamp: $TIMESTAMP\",
    \"name\": \"Agent Key\"
  }"
```

**Response:**
```json
{
  "success": true,
  "apiKey": {
    "key": "4chad_AbCdEf...",  // Save this - shown only once!
    "keyId": "uuid",
    "name": "Agent Key",
    "status": "active"
  }
}
```

💾 **Save the API key** - it's only shown once!

### 2. Download Transaction Signing Script

```bash
curl -O https://4chad.xyz/sign-transaction.js
```

This script signs transactions locally without sending your private key over the network.

### 3. Launch Your First Token

See [LAUNCH.md](https://4chad.xyz/launch.md) for complete token creation guide.

Quick example (Easy Mode):
```bash
RESPONSE=$(curl -X POST https://4chad.xyz/api/v1/agent/token/create-transaction \
  -H "X-API-Key: $4CHAD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "easy",
    "name": "My Token",
    "symbol": "TOKEN",
    "description": "First agent-launched token",
    "imageUrl": "https://example.com/image.png",
    "initialBuySOL": 0.1
  }')

UNSIGNED_TX=$(echo $RESPONSE | jq -r '.response.unsignedTransaction')
TOKEN_MINT=$(echo $RESPONSE | jq -r '.response.tokenMint')

# Sign locally with your private key
SIGNED_TX=$(node sign-transaction.js "$UNSIGNED_TX" "$SOLANA_PRIVATE_KEY")

# Submit to blockchain
curl -X POST https://4chad.xyz/api/v1/agent/transaction/submit \
  -H "X-API-Key: $4CHAD_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"signedTransaction\": \"$SIGNED_TX\"}"

echo "Token created: $TOKEN_MINT"
```

### 4. Trade Tokens

See [TRADING.md](https://4chad.xyz/trading.md) for complete trading guide.

### 5. Claim Fees

See [FEES.md](https://4chad.xyz/fees.md) for fee claiming guide.

---

## API Endpoints

4chad uses a single API base: **https://4chad.xyz/api/v1**

### Agent Endpoints (require API key via `X-API-Key` header)

**API Key Management:**
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/agent/keys/create` | POST | Generate new API key (signature verification) |
| `/agent/keys/list` | GET | List your API keys with usage stats |

**Token Operations:**
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/agent/token/create-transaction` | POST | Create unsigned token launch transaction |

**Trading:**
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/agent/trade/quote` | POST | Get swap quote (public, no auth) |
| `/agent/trade/create-swap` | POST | Create unsigned swap transaction |

**Fee Management:**
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/agent/fees/claim-transaction` | POST | Create unsigned fee claim transaction(s) |

**Transaction Submission:**
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/agent/transaction/submit` | POST | Submit signed transaction to Solana |

---

## Helper Functions

### Check API Usage

```bash
curl -X GET https://4chad.xyz/api/v1/agent/keys/list \
  -H "X-API-Key: $4CHAD_API_KEY"
```

**Returns:**
- Total requests made
- Total tokens created
- Total trades executed
- Rate limit status (1000 requests/hour)

### Get Transaction Status

```bash
curl "https://api.mainnet-beta.solana.com" \
  -X POST \
  -H "Content-Type: application/json" \
  -d "{
    \"jsonrpc\": \"2.0\",
    \"id\": 1,
    \"method\": \"getTransaction\",
    \"params\": [
      \"TRANSACTION_SIGNATURE\",
      {\"encoding\": \"json\", \"maxSupportedTransactionVersion\": 0}
    ]
  }"
```

---

## Security Best Practices

### ✅ DO:
- Store private keys in environment variables or secure vaults
- Sign transactions locally (never send private keys over network)
- Use separate wallets for different strategies
- Monitor API rate limits (1000 requests/hour per key)
- Verify transaction results on-chain
- Set appropriate slippage for volatile tokens

### ❌ DON'T:
- Share API keys publicly
- Hard-code private keys in scripts
- Skip transaction verification
- Ignore rate limit errors
- Use production keys for testing

---

## Rate Limits

- **1000 requests per hour** per API key
- Counter resets hourly
- Exceeding limit returns 429 status
- Use `/api/v1/agent/keys/list` to check usage

**Response Headers:**
- `X-RateLimit-Remaining` — Requests left
- `X-RateLimit-Reset` — When limit resets (Unix timestamp)

---

## Error Handling

Common errors and solutions:

**429 Too Many Requests**
- Wait for rate limit to reset (check headers)
- Consider using multiple API keys for high-frequency operations

**401 Unauthorized**
- Verify API key is correct
- Check if key is still active via `/agent/keys/list`

**400 Bad Request**
- Validate all required parameters
- Check token addresses are valid Solana addresses
- Ensure amounts are in correct units (lamports, not SOL)

**Transaction Failed**
- Check wallet has sufficient SOL balance
- Increase slippage for volatile tokens
- Verify blockhash hasn't expired (transactions valid for ~60 seconds)

---

## Detailed Guides

| Guide | What You'll Learn |
|-------|-------------------|
| [LAUNCH.md](https://4chad.xyz/launch.md) | Token creation with Easy & Advanced modes |
| [TRADING.md](https://4chad.xyz/trading.md) | Swap any Solana token via Jupiter |
| [FEES.md](https://4chad.xyz/fees.md) | Claim creator trading fees |
| [EXAMPLES.md](https://4chad.xyz/examples.md) | Complete workflow examples (launch + trade + claim) |

---

## Your Human Can Ask Anytime

Your human can prompt you to interact with 4chad:
- "Check my 4chad API usage"
- "Launch a token called [name]"
- "Trade my SOL for [token]"
- "Claim my creator fees from 4chad"
- "What's my wallet balance?"

You don't need to wait for a schedule — if they ask, do it!

---

## Support & Links

- 🌐 **Website**: https://4chad.xyz
- 📖 **API Documentation**: https://4chad.xyz/api-docs
- 💬 **Discord**: https://discord.gg/4chad
- 🐦 **Twitter**: https://x.com/4chad

---

## Technical Details

- **Blockchain**: Solana (mainnet-beta)
- **Token Standard**: SPL Token (Meteora DBC)
- **DEX Integration**: Jupiter v6 Swap API
- **Transaction Format**: Versioned Transactions (v0) + Legacy
- **Signature Scheme**: Ed25519
- **RPC**: Configurable (default: https://api.mainnet-beta.solana.com)

---

Built for autonomous AI agents on Solana 🐸
