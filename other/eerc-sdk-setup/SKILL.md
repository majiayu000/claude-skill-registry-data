---
name: eerc-sdk-setup
description: Use when the agent needs to install and initialize the eERC TypeScript SDK (@avalabs/ac-eerc-sdk) in a frontend — the useEERC hook, wagmi/viem clients, and the circuit (wasm/zkey) URLs required for client-side proof generation.
category: eERC SDK
difficulty: Intermediate
version: "0.1.0"
---

# eERC SDK — Setup & Initialization

## Overview
The eERC SDK (`@avalabs/ac-eerc-sdk`, repo `ac-eerc-sdk`) handles **key generation, client-side proof generation, and balance encryption/decryption**. The primary entry point is the React hook **`useEERC`**, which returns state + actions and a nested `useEncryptedBalance` hook.

## Install
```bash
npm install @avalabs/ac-eerc-sdk
# peer deps used by the hooks:
npm install wagmi viem
```

## Initialize `useEERC`
```ts
import { useEERC } from "@avalabs/ac-eerc-sdk";
import { usePublicClient, useWalletClient } from "wagmi";

const publicClient = usePublicClient();
const { data: walletClient } = useWalletClient();

const circuitURLs = {
  register: { wasm: "/circuits/registration.wasm", zkey: "/circuits/registration.zkey" },
  transfer: { wasm: "/circuits/transfer.wasm",     zkey: "/circuits/transfer.zkey" },
  mint:     { wasm: "/circuits/mint.wasm",         zkey: "/circuits/mint.zkey" },
  withdraw: { wasm: "/circuits/withdraw.wasm",     zkey: "/circuits/withdraw.zkey" },
  burn:     { wasm: "/circuits/burn.wasm",         zkey: "/circuits/burn.zkey" },
};

const {
  isInitialized, isRegistered, isConverter, publicKey,
  register, generateDecryptionKey, useEncryptedBalance, auditorDecrypt,
} = useEERC(
  publicClient,
  walletClient,
  EERC_CONTRACT_ADDRESS,                 // from your deploy
  { transferURL: "/transfer.wasm", multiWasmURL: "/multi.wasm" }, // prover assets
  circuitURLs,
  decryptionKey,                          // optional; omit to generate later
);
```

## Signature (what each argument is)
1. `client: PublicClient` — read client (wagmi/viem).
2. `wallet: WalletClient` — signer.
3. `contractAddress: string` — the deployed `EncryptedERC`.
4. `urls: { transferURL, multiWasmURL }` — prover WASM assets (relative paths are resolved against `location.origin`).
5. `circuitURLs: CircuitURLs` — per-operation `{ wasm, zkey }` (register/transfer/mint/withdraw/burn).
6. `decryptionKey?: string` — optional saved key; otherwise generate via `generateDecryptionKey()`.

## Hosting the circuit artifacts
The `.wasm` and `.zkey` files come from building the circuits ([[eerc-circuits-proofs]]). Serve them statically (e.g. `public/circuits/`). They can be large — host on CDN for production.

## What you get back
State: `isInitialized`, `isRegistered`, `isConverter`, `publicKey`, `auditorPublicKey`, `isAuditorKeySet`, `areYouAuditor`, `name`, `symbol`, `owner`.
Actions: `register`, `generateDecryptionKey`, `auditorDecrypt`, `isAddressRegistered`, `setContractAuditorPublicKey`, and `useEncryptedBalance(tokenAddress?)` ([[eerc-encrypted-balance]]).

## Common Pitfalls
- **Missing circuit URLs.** The hook will not initialize without valid `circuitURLs`; proofs cannot be generated.
- **Calling actions before `isInitialized`.** Gate UI on `isInitialized` (and `isRegistered` for ops).
- **Wrong wallet/key pairing.** The decryption key is bound to the wallet address; switching wallets resets it.

## AI Agent Prompt
> "Act as a frontend engineer. Set up `@avalabs/ac-eerc-sdk` in a wagmi/viem React app: initialize `useEERC` with circuit URLs, gate the UI on initialization, and expose register + balance hooks."

## References
See `references/README.md` (ac-eerc-sdk `src/hooks/useEERC.tsx`, `src/hooks/types.ts`).
