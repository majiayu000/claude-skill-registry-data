---
description: Launch new tokens on Pump.fun directly via the Pump SDK
---

# PumpFun Token Launcher

Launch new tokens on the Pump.fun protocol using the native Pump SDK integrated into SolanaOS.

## Prerequisites

- Solana wallet configured (`solanaos birth`)
- `HELIUS_RPC_URL` or `SOLANA_RPC_URL` set in vault
- Sufficient SOL balance for transaction fees (~0.05 SOL)

## How It Works

The Pump SDK provides offline instruction builders for token creation. This skill uses the `PumpSdk.createV2Instruction()` method to build a token creation transaction.

### Token Creation Flow

1. Generate a new mint keypair
2. Upload metadata JSON to Arweave/IPFS (name, symbol, image, description)
3. Build the `createV2` instruction via `PUMP_SDK.createV2Instruction()`
4. Optionally build a combined `createV2AndBuy` to purchase initial supply
5. Sign and send the transaction

### Example Usage

```typescript
import { Keypair, Connection } from "@solana/web3.js";
import { PUMP_SDK, OnlinePumpSdk, getBuyTokenAmountFromSolAmount } from "solanaos";

const connection = new Connection(process.env.HELIUS_RPC_URL!);
const mintKeypair = Keypair.generate();
const creator = wallet.publicKey;

// Create token
const createIx = await PUMP_SDK.createV2Instruction({
  mint: mintKeypair.publicKey,
  name: "My Token",
  symbol: "MYTKN",
  uri: "https://arweave.net/metadata.json",
  creator,
  user: creator,
  mayhemMode: false,
});

// Or create + buy in one transaction
const sdk = new OnlinePumpSdk(connection);
const global = await sdk.fetchGlobal();
const ixs = await PUMP_SDK.createV2AndBuyInstructions({
  global,
  mint: mintKeypair.publicKey,
  name: "My Token",
  symbol: "MYTKN",
  uri: "https://arweave.net/metadata.json",
  creator,
  user: creator,
  amount: new BN(1_000_000_000), // tokens to buy
  solAmount: new BN(100_000_000),  // 0.1 SOL
  mayhemMode: false,
});
```

### Mayhem Mode

Set `mayhemMode: true` for tokens with randomized bonding curve parameters. This creates unpredictable pricing dynamics.

### Safety Notes

- **Always test on devnet first** — never launch tokens with real funds without testing
- **Use mock keypairs for development** — never commit real wallet keys
- **Token creation is irreversible** — once created, the bonding curve is live

## On-Chain Programs

| Program | Address |
|---------|---------|
| Pump | `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P` |
| PumpAMM | `pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA` |
| PumpFees | `pfeeUxB6jkeY1Hxd7CsFCAjcbHA9rWtchMGdZ6VojVZ` |
