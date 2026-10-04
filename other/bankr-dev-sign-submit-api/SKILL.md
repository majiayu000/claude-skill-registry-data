---
name: Bankr Dev - Sign & Submit API
description: This skill should be used when building apps that need to sign messages, sign typed data (EIP-712), sign transactions, or submit raw transactions via the Bankr API. Covers the synchronous /agent/sign and /agent/submit endpoints with TypeScript patterns.
version: 1.0.0
---

# Sign & Submit API

Synchronous endpoints for signing and submitting transactions directly — no job polling required.

## Endpoints

| Endpoint | Purpose | Returns |
|----------|---------|---------|
| `POST /agent/sign` | Sign messages, typed data, or transactions | Signature |
| `POST /agent/submit` | Submit raw transactions to chain | Transaction hash |

## POST /agent/sign

### Signature Types

| Type | Use Case |
|------|----------|
| `personal_sign` | Plain text messages (auth, verification) |
| `eth_signTypedData_v4` | EIP-712 typed data (permits, orders) |
| `eth_signTransaction` | Sign transactions for later broadcast |

### Usage

```typescript
// personal_sign
const signMessage = await fetch(`${API_URL}/agent/sign`, {
  method: "POST",
  headers: { "x-api-key": API_KEY, "Content-Type": "application/json" },
  body: JSON.stringify({
    signatureType: "personal_sign",
    message: "Sign in to MyApp\nNonce: abc123",
  }),
});
// → { success: true, signature: "0x...", signer: "0x...", signatureType: "personal_sign" }

// eth_signTypedData_v4 (EIP-2612 permit)
const signPermit = await fetch(`${API_URL}/agent/sign`, {
  method: "POST",
  headers: { "x-api-key": API_KEY, "Content-Type": "application/json" },
  body: JSON.stringify({
    signatureType: "eth_signTypedData_v4",
    typedData: {
      domain: { name: "USD Coin", version: "2", chainId: 8453, verifyingContract: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913" },
      types: {
        Permit: [
          { name: "owner", type: "address" },
          { name: "spender", type: "address" },
          { name: "value", type: "uint256" },
          { name: "nonce", type: "uint256" },
          { name: "deadline", type: "uint256" },
        ],
      },
      primaryType: "Permit",
      message: { owner: "0x...", spender: "0x...", value: "1000000", nonce: "0", deadline: "1735689600" },
    },
  }),
});

// eth_signTransaction
const signTx = await fetch(`${API_URL}/agent/sign`, {
  method: "POST",
  headers: { "x-api-key": API_KEY, "Content-Type": "application/json" },
  body: JSON.stringify({
    signatureType: "eth_signTransaction",
    transaction: { to: "0x...", chainId: 8453, value: "0", data: "0xa9059cbb..." },
  }),
});
```

### Error Responses

| Status | Error | Cause |
|--------|-------|-------|
| 400 | Missing required field | Missing message, typedData, or transaction |
| 401 | Authentication required | Missing or invalid API key |
| 403 | Read-only API key | Key lacks write permissions |

## POST /agent/submit

### Transaction Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `to` | string | Yes | Destination address |
| `chainId` | number | Yes | Chain ID (8453=Base, 1=Ethereum, 137=Polygon) |
| `value` | string | No | Value in wei |
| `data` | string | No | Calldata (hex) |
| `gas` | string | No | Gas limit |
| `maxFeePerGas` | string | No | EIP-1559 max fee |
| `maxPriorityFeePerGas` | string | No | EIP-1559 priority fee |

### Options

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `description` | string | — | Human-readable description for logging |
| `waitForConfirmation` | boolean | true | Wait for on-chain confirmation |

### Usage

```typescript
// Submit a transaction and wait for confirmation
const result = await fetch(`${API_URL}/agent/submit`, {
  method: "POST",
  headers: { "x-api-key": API_KEY, "Content-Type": "application/json" },
  body: JSON.stringify({
    transaction: { to: "0x...", chainId: 8453, value: "1000000000000000000" },
    description: "Send 1 ETH",
    waitForConfirmation: true,
  }),
});
// → { success: true, transactionHash: "0x...", status: "success", blockNumber: "123", gasUsed: "21000" }

// Fire-and-forget (don't wait for confirmation)
const pending = await fetch(`${API_URL}/agent/submit`, {
  method: "POST",
  headers: { "x-api-key": API_KEY, "Content-Type": "application/json" },
  body: JSON.stringify({
    transaction: { to: "0x...", chainId: 8453, value: "100000000000000000" },
    waitForConfirmation: false,
  }),
});
// → { success: true, transactionHash: "0x...", status: "pending" }
```

### Multi-Step Workflow

```typescript
// Approve + Swap sequence
async function approveAndSwap(approveTx: object, swapTx: object) {
  // 1. Approve token spending
  const approval = await submitTransaction(approveTx);
  if (approval.status !== "success") throw new Error("Approval failed");

  // 2. Execute swap
  const swap = await submitTransaction(swapTx);
  if (swap.status !== "success") throw new Error("Swap failed");

  return swap;
}
```

### Transaction Status Values

| Status | Description |
|--------|-------------|
| `success` | Confirmed and succeeded |
| `reverted` | Confirmed but reverted |
| `pending` | Submitted, not yet confirmed |

## Comparison with /agent/prompt

| Feature | /agent/prompt | /agent/sign | /agent/submit |
|---------|---------------|-------------|---------------|
| Input | Natural language | Structured data | Transaction object |
| Response | Async (job ID) | Sync (signature) | Sync (tx hash) |
| Executes on-chain | Via AI agent | No | Yes |
| Best for | General queries | Auth, permits | Raw transactions |

## Security Notes

- `/agent/submit` executes immediately — **no confirmation prompt**
- Read-only API keys get 403 on both endpoints
- Always validate transaction parameters before submission
- Use `waitForConfirmation: true` for critical transactions

## Related Skills

- `bankr-api-basics` - API fundamentals
- `bankr-client-patterns` - Client setup
- `bankr-safety` - Security best practices
- `bankr-arbitrary-transaction` - Constructing raw transaction JSON
