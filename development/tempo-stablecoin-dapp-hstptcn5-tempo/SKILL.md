---
name: tempo-stablecoin-dapp
description: Build stablecoin-first dapps on Tempo (TIP-20 payments, memos, fee tokens, sponsorship, batching, TIP-403 compliance, and stablecoin DEX).
---

# Tempo Stablecoin Dapp (Payments + Account Abstraction)

Production-ready patterns and code snippets for building on **Tempo**, an EVM chain optimized for **stablecoin payments** where transaction fees are paid in **USD-denominated TIP-20 tokens** (no native gas token).

## When to Use This Skill

- Gasless onboarding (fee sponsorship / paymaster-like flows)
- Stablecoin checkout & invoicing with onchain memos (32 bytes)
- Batch payouts (payroll, airdrops, disbursements)
- Issuing TIP-20 stablecoins with RBAC + pause/cap controls
- Compliance controls (whitelist/blacklist) via TIP-403 policies
- Stablecoin-to-stablecoin swaps via Tempo’s enshrined DEX
- Wallet/app integration on chains **without** a native gas token

## Network Quickstart (Tempo Testnet “Andantino”)

- **Chain ID:** 42429  
- **HTTP RPC:** https://rpc.testnet.tempo.xyz  
- **WS RPC:** wss://rpc.testnet.tempo.xyz  
- **Explorer:** https://explore.tempo.xyz  
- **Native currency symbol (wallet UI):** USD (even though there is no native token)

### Faucet (testnet)

```bash
cast rpc tempo_fundAddress <YOUR_ADDRESS> --rpc-url https://rpc.testnet.tempo.xyz
```

Faucet commonly funds (addresses may vary by network config):
- pathUSD: 0x20c0000000000000000000000000000000000000
- AlphaUSD: 0x20c0000000000000000000000000000000000001
- BetaUSD:  0x20c0000000000000000000000000000000000002
- ThetaUSD: 0x20c0000000000000000000000000000000000003

## Core Concepts

### 1) No native gas token (important!)

- EVM balance opcodes like `BALANCE` / `SELFBALANCE` return `0`
- `CALLVALUE` returns `0`
- Many wallets assume `eth_getBalance` is the native gas token balance and may display weird values.
- Recommendation: **do not gate UX on native-balance checks**; use TIP-20 `balanceOf()` instead.

### 2) Fees are paid in TIP-20 stablecoins

- Only TIP-20 tokens can be used for paying transaction fees.
- You can specify a `fee_token` (Tempo Transactions) or rely on fee token preferences.
- Tempo’s Fee AMM automatically converts the user’s fee token to the validator’s preferred fee token.

> Tip: If you’re using legacy EVM transactions to call a non–TIP-20 contract, the fee token may fall back to pathUSD. Prefer Tempo Transactions if you control submission.

### 3) Predeployed / system contracts (testnet-style addresses)

- TIP-20 Factory:      0x20fc000000000000000000000000000000000000
- Fee Manager:         0xfeec000000000000000000000000000000000000
- Stablecoin DEX:      0xdec0000000000000000000000000000000000000
- TIP-403 Registry:    0x403c000000000000000000000000000000000000
- pathUSD (TIP-20):    0x20c0000000000000000000000000000000000000

## Recipes

### Recipe 1 — Send a stablecoin payment with a 32-byte memo (TypeScript + viem)

```ts
import { parseUnits, pad, stringToHex } from "viem"
import { client } from "./viem.config"

const invoiceId = pad(stringToHex("INV-12345"), { size: 32 })

const { receipt } = await client.token.transferSync({
  amount: parseUnits("100", 6), // common USD stablecoin decimals
  to: "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEbb",
  token: "0x20c0000000000000000000000000000000000001", // AlphaUSD (example)
  memo: invoiceId,
})
console.log(receipt)
```

### Recipe 2 — Solidity: transferWithMemo for reconciliation / invoices

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface ITIP20 {
    function transfer(address to, uint256 amount) external returns (bool);
    function transferWithMemo(address to, uint256 amount, bytes32 memo) external;
}

contract PaymentSender {
    ITIP20 public immutable token;

    constructor(address tip20) {
        token = ITIP20(tip20);
    }

    function sendPayment(address recipient, uint256 amount) external {
        require(token.transfer(recipient, amount), "transfer failed");
    }

    function sendPaymentWithMemo(address recipient, uint256 amount, bytes32 invoiceId) external {
        token.transferWithMemo(recipient, amount, invoiceId);
    }
}
```

### Recipe 3 — Batch multiple TIP-20 transfers in one Tempo Transaction

```ts
import { encodeFunctionData, parseUnits } from "viem"
import { Abis } from "tempo.ts/viem"
import { client } from "./viem.config"

const tokenABI = Abis.tip20
const token = "0x20c0000000000000000000000000000000000001" // AlphaUSD example

const calls = [
  {
    to: token,
    data: encodeFunctionData({
      abi: tokenABI,
      functionName: "transfer",
      args: ["0x742d35Cc6634C0532925a3b844Bc9e7595f0bEbb", parseUnits("100", 6)],
    }),
  },
  {
    to: token,
    data: encodeFunctionData({
      abi: tokenABI,
      functionName: "transfer",
      args: ["0x70997970C51812dc3A010C7d01b50e0d17dc79C8", parseUnits("50", 6)],
    }),
  },
]

const hash = await client.sendTransaction({ calls })
console.log(hash)
```

### Recipe 4 — Sponsor fees (fee payer) using the Go SDK pattern

```go
// Pseudocode-style (see tempo-go SDK docs for full imports)
tx := transaction.NewDefault(42429)

// User signs transaction intent first
transaction.SignTransaction(tx, userSigner)

// A separate fee payer selects fee token and signs to sponsor
transaction.AddFeePayerSignature(tx, feePayerSigner)

client.SendTransaction(tx)
```

### Recipe 5 — Issue a new USD TIP-20 stablecoin using TIP-20 Factory

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface ITIP20 {}
interface ITIP20Factory {
    function createToken(
        string memory name,
        string memory symbol,
        string memory currency,
        ITIP20 quoteToken,
        address admin
    ) external returns (address token);
}

contract IssueStablecoin {
    address public constant TIP20_FACTORY = 0x20fc000000000000000000000000000000000000;
    address public constant PATH_USD     = 0x20c0000000000000000000000000000000000000;

    function createUSDToken(string memory name, string memory symbol) external returns (address) {
        return ITIP20Factory(TIP20_FACTORY).createToken(
            name,
            symbol,
            "USD",
            ITIP20(PATH_USD),
            msg.sender
        );
    }
}
```

### Recipe 6 — Compliance: TIP-403 policies (high-level)

- TIP-20 token transfers (including memo variants) enforce a configured TIP-403 transfer policy.
- A policy can implement allowlist/denylist behavior shared across tokens.
- Build your app UX assuming a transfer can revert if sender/recipient is not authorized.

## Best Practices & Gotchas

- Treat stablecoin **decimals as metadata** (pathUSD is commonly 6, but always read from `getMetadata` / `decimals()`).
- Keep memos within 32 bytes; pack IDs (invoice/order), hash longer payloads.
- Avoid sending TIP-20 tokens to TIP-20 token contract addresses (some implementations revert to prevent loss).
- Prefer **Tempo Transactions** (type 0x76) for: sponsorship, batching, scheduled txs, parallelizable nonces.
- Don’t block users on “native gas balance” checks; use TIP-20 balances instead.

## Resources

- docs.tempo.xyz — Quickstart, TIP-20 / TIP-403 specs, Tempo Transactions spec, Fee Manager + DEX specs
- Tempo TS SDK: `tempo.ts` (viem / wagmi actions)
- Tempo Go SDK: `github.com/tempoxyz/tempo-go`
