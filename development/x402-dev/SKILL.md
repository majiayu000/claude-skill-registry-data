---
name: x402-dev
description: |
  Comprehensive development support for x402 protocol — the open HTTP payment standard built on HTTP 402.
  Covers client (buyer) integration, server (seller) middleware, MCP server monetization, and AWS CloudFront/Lambda@Edge deployments.

  USE THIS SKILL whenever the user:
  - Asks about x402, HTTP 402 payments, or machine-to-machine micropayments
  - Wants to add pay-per-request pricing to an API, endpoint, or HTTP resource
  - Integrates x402 with Express, Next.js, Hono, FastAPI, Flask, or any HTTP framework
  - Builds an AI agent that pays for tools/APIs automatically (agentic commerce)
  - Implements an MCP server with payment-gated tools
  - Deploys x402 on AWS CloudFront, Lambda@Edge, or AgentCore
  - Needs wallet setup, facilitator config, EVM/Solana network configuration, or USDC payments
  - Asks about Bazaar service discovery, x402 whitepaper concepts, or x402 architecture
  - Migrates from testnet (Base Sepolia) to mainnet (Base Mainnet / Solana Mainnet)

  Even if the user just says "add payments to my API", "charge per API call", or "monetize my HTTP endpoint", invoke this skill.
---

# x402 Development Guide

x402 is an **open payment standard** that extends HTTP 402 to enable programmatic, account-free micropayments between clients and servers — natively supporting AI agent autonomous payments.

## Quick Orientation

| Role | Description |
|---|---|
| **Client / Buyer** | Holds a wallet, receives 402, signs and retries with payment |
| **Server / Seller** | Returns 402 with payment instructions, verifies payment, delivers resource |
| **Facilitator** | Off-chain service that handles `/verify` and `/settle` (e.g., `https://x402.org/facilitator`) |

**Payment Flow:**
1. Client requests resource → Server returns `402` with `X-PAYMENT-REQUIRED` header
2. Client creates signed payment payload → retries with `X-PAYMENT-SIGNATURE` header
3. Server verifies via facilitator → settles on-chain → returns `200`

---

## Package Reference

### TypeScript / Node.js

```bash
# Client (buyer)
npm install @x402/core @x402/evm @x402/fetch    # fetch-based
npm install @x402/core @x402/evm @x402/axios    # axios-based
npm install @x402/core @x402/svm @x402/fetch    # Solana client

# Server (seller)
npm install @x402/express    # Express.js
npm install @x402/next       # Next.js
npm install @x402/hono       # Hono

# MCP integration
npm install @x402/mcp
```

### Python

```bash
pip install x402                # base
pip install x402[httpx]         # async httpx client
pip install x402[requests]      # sync requests client
pip install x402[fastapi]       # FastAPI middleware
pip install x402[flask]         # Flask middleware
pip install x402[svm]           # Solana support
```

---

## Network & Facilitator Configuration

| Network | CAIP-2 ID | Facilitator |
|---|---|---|
| Base Sepolia (testnet) | `eip155:84532` | `https://x402.org/facilitator` |
| Base Mainnet | `eip155:8453` | `https://api.cdp.coinbase.com/platform/v2/x402` |
| Solana Devnet | `solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1` | `https://x402.org/facilitator` |
| Solana Mainnet | `solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp` | `https://api.cdp.coinbase.com/platform/v2/x402` |

**Always start on testnet.** For mainnet migration see [references/networks.md].

---

## Implementation Paths

Choose your path and read the reference file:

| Task | Reference File |
|---|---|
| Build a **client** that pays for APIs | [references/client.md] |
| Build a **server** that charges for APIs | [references/server.md] |
| Build an **MCP server** with payment-gated tools | [references/mcp-server.md] |
| Deploy on **AWS CloudFront + Lambda@Edge** | [references/aws-cloudfront.md] |
| Network config, facilitators, mainnet migration | [references/networks.md] |

---

## Minimal Working Examples

### Client (Buyer) — TypeScript

```typescript
import { wrapFetchWithPayment } from "@x402/fetch";
import { x402Client } from "@x402/core/client";
import { ExactEvmScheme } from "@x402/evm/exact/client";
import { privateKeyToAccount } from "viem/accounts";

const signer = privateKeyToAccount(process.env.EVM_PRIVATE_KEY as `0x${string}`);
const client = new x402Client();
client.register("eip155:*", new ExactEvmScheme(signer));

const fetchWithPayment = wrapFetchWithPayment(fetch, client);

// Automatically handles 402 → sign → retry
const response = await fetchWithPayment("https://api.example.com/paid-endpoint");
const data = await response.json();
```

### Server (Seller) — Express.js

```typescript
import express from "express";
import { paymentMiddleware, x402ResourceServer } from "@x402/express";
import { ExactEvmScheme } from "@x402/evm/exact/server";
import { HTTPFacilitatorClient } from "@x402/core/server";

const app = express();

const facilitator = new HTTPFacilitatorClient({ url: "https://x402.org/facilitator" });
const server = new x402ResourceServer(facilitator)
  .register("eip155:84532", new ExactEvmScheme());

app.use(paymentMiddleware({
  "GET /weather": {
    accepts: [{
      scheme: "exact",
      price: "$0.001",
      network: "eip155:84532",
      payTo: process.env.WALLET_ADDRESS!,
    }],
    description: "Real-time weather data",
    mimeType: "application/json",
  },
}, server));

app.get("/weather", (req, res) => {
  res.json({ weather: "sunny", temperature: 72 });
});

app.listen(4021);
```

### MCP Server — Payment-Gated Tool

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { x402MCPServer } from "@x402/mcp";
import { HTTPFacilitatorClient } from "@x402/core/server";
import { ExactEvmScheme } from "@x402/evm/exact/server";

const mcpServer = new McpServer({ name: "paid-tools", version: "1.0.0" });

const facilitator = new HTTPFacilitatorClient({ url: "https://x402.org/facilitator" });
const x402Server = new x402MCPServer(facilitator)
  .register("eip155:84532", new ExactEvmScheme());

// Wrap a tool with payment requirement
x402Server.wrapTool(mcpServer, "get_premium_data", {
  accepts: [{
    scheme: "exact",
    price: "$0.001",
    network: "eip155:84532",
    payTo: process.env.WALLET_ADDRESS!,
  }],
  handler: async (params) => ({ data: "premium content" }),
});
```

---

## Route Configuration Schema

```typescript
interface RouteConfig {
  accepts: Array<{
    scheme: string;    // "exact" (fixed) or "upto" (consumption-based)
    price: string;     // Dollar format: "$0.001"
    network: string;   // CAIP-2 identifier
    payTo: string;     // Wallet address to receive payment
    asset?: string;    // Token contract address (auto-resolved if omitted)
  }>;
  description?: string;
  mimeType?: string;
  extensions?: {
    bazaar?: {
      discoverable: boolean;
      category: string;
      tags: string[];
    };
  };
}
```

---

## Common Issues & Solutions

| Issue | Solution |
|---|---|
| `No scheme registered for network` | Register the correct scheme: `client.register("eip155:*", new ExactEvmScheme(signer))` |
| Payment fails on retry | Check wallet has sufficient USDC balance on the target network |
| `PAYMENT-REQUIRED` header missing | Ensure middleware is applied before route handlers |
| Lambda@Edge: env vars not available | Bundle config as `deploy-config.json` at build time (Lambda@Edge restriction) |
| Cache serving 402 response | Disable caching on payment routes (`defaultTtl: 0`) |
| Mainnet facilitator URL wrong | Use `https://api.cdp.coinbase.com/platform/v2/x402` for mainnet |

---

## Environment Variables

```bash
# Client (buyer)
EVM_PRIVATE_KEY=0x...          # EVM wallet private key
SVM_PRIVATE_KEY=...            # Solana wallet private key (base58)

# Server (seller)
WALLET_ADDRESS=0x...           # Address to receive payments
FACILITATOR_URL=https://x402.org/facilitator  # testnet

# AWS / AgentCore
CDP_API_KEY_ID=...
CDP_API_KEY_SECRET=...
CDP_WALLET_SECRET=...
SELLER_API_URL=https://dXXX.cloudfront.net
```

---

## Bazaar Service Discovery

Register your API for discoverability:

```typescript
"GET /weather": {
  accepts: [{ scheme: "exact", price: "$0.001", network: "eip155:8453", payTo: "0x..." }],
  extensions: {
    bazaar: {
      discoverable: true,
      category: "weather",
      tags: ["forecast", "real-time"],
    },
  },
}
```

Query the Bazaar:

```typescript
const response = await fetch("https://api.cdp.coinbase.com/platform/v2/x402/discovery/resources");
const { items } = await response.json();
const affordable = items.filter(item =>
  item.accepts.some(req => Number(req.amount) < 100000)
);
```

---

## Reference Files

- **[references/client.md]** — Full client patterns: fetch, axios, multi-network, error handling, AI agent integration
- **[references/server.md]** — Full server patterns: Express, Next.js, Hono, Python FastAPI/Flask, route config
- **[references/mcp-server.md]** — MCP server monetization: tool wrapping, payment lifecycle hooks, Claude integration
- **[references/aws-cloudfront.md]** — CloudFront + Lambda@Edge: CDK stack, payment verifier, AgentCore, 3-step flow
- **[references/networks.md]** — Network IDs, facilitators, testnet/mainnet migration, USDC addresses
