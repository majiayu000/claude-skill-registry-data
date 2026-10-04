---
name: pons-launch
description: >
  Launch a fixed-supply V3 token on Robinhood Chain (4663) via PonsLaunchFactory
  (pons.family), reverse-discover the factory from live PonsLauncherToken tokens,
  prepare launchToken txs, and verify TokenLaunched receipts. Use when the user
  says "launch on Pons", "pons.family launch", "PonsLaunchFactory", "launchToken",
  "PonsLauncherToken", "V3 launch on Robinhood", or wants agents to create a Pons
  token. Does NOT use RH bonding-curve createToken (rh-bonded-launch), does NOT
  mint Solana $CLAWD, and does NOT use NOXA Fun factories.
---

# Pons Launch — `launchToken` on Robinhood Chain

## Product truth (do not dilute)

- **Pons** launches **fixed-supply ERC-20s** (`PonsLauncherToken`) with a Uniswap V3 pool, not a bonding curve.
- Factory entry point is **`launchToken`** (selector **`0x686399cb`**), **not** a guessed `createLaunch`.
- Supply / max-wallet / max-tx / restriction blocks come from **on-chain LaunchConfig** (`launchConfigId`), not free-form agent inventing.
- Launch costs **`launchFee` ETH** (live-read; historically **0.0005 ETH**) plus gas; `msg.value` above the fee funds optional atomic initial buy.
- Cheshire does **not** own Pons bytecode; we are a **partner surface** (like NOXA): registry + prepare + wallet sign + verify.

## Canonical addresses (Robinhood mainnet 4663)

Grounded in shipped `client/src/lib/pons-launch/registry.ts` and live probes.

| Item | Value |
|------|--------|
| **PonsLaunchFactory (current)** | `0xA5aAb3F0c6EeadF30Ef1D3Eb997108E976351feB` |
| **Legacy factory ($PONS only)** | `0x0c37a24F5D23A486FA692d1500881d698B1F77a4` |
| **Pair token (WETH)** | `0x0Bd7D308f8E1639FAb988df18A8011f41EAcAD73` |
| **DEX V3 factory** | `0x1f7d7550B1b028f7571E69A784071F0205FD2EfA` |
| **NonfungiblePositionManager** | `0x73991a25C818Bf1f1128dEAaB1492D45638DE0D3` (`PONS_DEFAULT_POSITION_MANAGER`) |
| **Swap router (dex config 0)** | `0xCaf681a66D020601342297493863E78C959E5cb2` (`PONS_DEFAULT_SWAP_ROUTER` — from factory `getDexConfig(0)`) |
| **Default pool fee** | `10000` (1%) (`PONS_DEFAULT_POOL_FEE`) |
| **Default launchConfigId / dexId** | `0` / `0` (read live before relying) |
| **Chain ID** | `4663` |
| **Public RPC** | `https://rpc.mainnet.chain.robinhood.com` (rate-limited) |
| **App RPC** | Set `RH_RPC_URL` (Alchemy/QuickNode preferred) |
| **Explorer** | `https://robinhoodchain.blockscout.com` |
| **Human UI (Cheshire)** | `/pons-launch` (launch) · `/pons-launch/{token}` (trade) |
| **Demo trade token** | `0x41e6318d44E0290CDd8c77219B57D17E44Bb59aB` (CTESTV2IW) |
| **Status API** | `GET /api/pons/launch/status` |
| **Prepare API** | `POST /api/pons/launch/prepare` |
| **Shipped helpers** | `client/src/lib/pons-launch/*` (launch + V3 trade) |

**Factory may migrate.** Re-discover (below) if launches fail or status drifts.

## When to use which path

| Goal | Action |
|------|--------|
| User wants click-launch in browser | Send to **`/pons`** → Wallet launch (EVM wallet on 4663) |
| Agent has funded RH EVM key + RPC | `preparePonsLaunch` → simulate → `launchToken` → verify receipt |
| User wants bonding-curve / pump-style RH | Use **`rh-bonded-launch`** (`createToken` on `0x3f60…`) |
| User wants Solana $CLAWD | Stop — wrong chain/product |
| User only wants Pons market data | Firecrawl monitor: `GET /api/pons/snapshot` (not a launch) |

## Factory reverse-discovery (no key from Pons required)

Every `PonsLauncherToken` stores:

```solidity
address public immutable launchFactory; // set to msg.sender in constructor
```

### Recipe

1. Collect graduated/live token addresses from `https://pons.family/launchpad` or `GET /api/pons/launchpad`.
2. For each token, `eth_call` **`launchFactory()`**.
3. Vote: most common non-zero address = current factory.
4. Confirm with factory **`getLaunchedToken(token)`** → `exists == true`.
5. Optionally read token **`dexFactory()`**, **`positionManager()`**, **`pairToken()`**, **`poolFee()`** to refresh periphery defaults.

```ts
// Pseudocode — use viem readContract
const factory = await read(token, "launchFactory()");
const row = await read(factory, "getLaunchedToken(token)");
// row.exists === true for tokens of that factory
```

Do **not** invent a factory address. Prefer shipped registry defaults, then re-probe if needed.

## Pre-flight (always)

```ts
import { createPublicClient, http, formatEther } from "viem";

const FACTORY = "0xA5aAb3F0c6EeadF30Ef1D3Eb997108E976351feB" as const;

// launchEnabled() → true
// launchFee() → wei (e.g. 5e14 = 0.0005 ETH)
// getLaunchConfig(0) → enabled, pairToken, supply, maxWalletBps, maxTxBps, restrictionBlocks
// getDexConfig(0) → enabled, factory, positionManager, poolFee
// wallet balance ≥ launchFee + gas buffer (~0.0003–0.002 ETH depending on gas)
// chainId === 4663
```

Live snapshot (verify; do not hardcode forever):

| Field | Observed |
|-------|----------|
| launchEnabled | true |
| launchFee | 0.0005 ETH |
| LaunchConfig 0 supply | 1e9 * 1e18 |
| maxWalletBps / maxTxBps | 500 / 550 |
| restrictionBlocks | 366 |
| Dex 0 poolFee | 10000 |

## Agent workflow (browser / human-in-the-loop)

1. Confirm product: **Pons V3 launch**, not bonding curve, not $CLAWD.
2. Open **`/pons`** (Cheshire) → **Wallet launch (Pons V3)**.
3. Connect EVM wallet → Robinhood Chain (4663) with ETH.
4. Name + symbol (+ optional description / extra buy above fee).
5. User confirms tx (pays launchFee + optional buy).
6. Report token, pool, explorer tx, and `https://pons.family/launchpad/{token}`.

## Agent workflow (programmatic — prefer shipped helpers)

**Source of truth (import these; do not reimplement ABI from memory):**

- `preparePonsLaunch` — `client/src/lib/pons-launch/prepare.ts`
- `verifyPonsLaunchReceipt` — `client/src/lib/pons-launch/receipt.ts`
- `getPonsLaunchRegistry` — `client/src/lib/pons-launch/registry.ts`
- API: `POST /api/pons/launch/prepare` with `{ name, symbol, feeWallet, launchConfigId, dexId, valueWei }`

### Encode + send (viem)

```ts
import {
  createPublicClient,
  createWalletClient,
  http,
  defineChain,
  type Hex,
} from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { preparePonsLaunch } from "./client/src/lib/pons-launch/prepare.ts";
import { verifyPonsLaunchReceipt } from "./client/src/lib/pons-launch/receipt.ts";

const RH = defineChain({
  id: 4663,
  name: "Robinhood Chain",
  nativeCurrency: { name: "Ether", symbol: "ETH", decimals: 18 },
  rpcUrls: {
    default: { http: [process.env.RH_RPC_URL || "https://rpc.mainnet.chain.robinhood.com"] },
  },
  blockExplorers: {
    default: { name: "Blockscout", url: "https://robinhoodchain.blockscout.com" },
  },
});

/**
 * Launch a Pons token. Never log or commit private keys.
 * Prefer user-signed wallet over agent-held keys.
 * Require explicit user confirmation before broadcast.
 */
export async function launchPonsToken(opts: {
  privateKey?: `0x${string}`; // only with explicit user approval
  name: string;
  symbol: string;
  description?: string;
  logo?: string;
  /** Defaults to the signing address */
  feeWallet?: `0x${string}`;
  launchConfigId?: number;
  dexId?: number;
  /** Total msg.value = launchFee + optional initial buy */
  valueWei?: bigint;
}) {
  if (!opts.privateKey) throw new Error("Need user wallet or authorized RH_EVM_PRIVATE_KEY");

  const account = privateKeyToAccount(opts.privateKey);
  const publicClient = createPublicClient({ chain: RH, transport: http() });
  const walletClient = createWalletClient({
    account,
    chain: RH,
    transport: http(),
  });

  const FACTORY = "0xA5aAb3F0c6EeadF30Ef1D3Eb997108E976351feB" as const;
  const fee = await publicClient.readContract({
    address: FACTORY,
    abi: [{ type: "function", name: "launchFee", stateMutability: "view", inputs: [], outputs: [{ type: "uint256" }] }] as const,
    functionName: "launchFee",
  });

  const prepared = preparePonsLaunch({
    name: opts.name,
    symbol: opts.symbol,
    description: opts.description,
    logo: opts.logo,
    feeWallet: opts.feeWallet ?? account.address,
    launchConfigId: opts.launchConfigId ?? 0,
    dexId: opts.dexId ?? 0,
    valueWei: opts.valueWei ?? fee,
  });

  // selector must be launchToken
  if (!prepared.data.startsWith("0x686399cb")) {
    throw new Error(`Unexpected selector ${prepared.data.slice(0, 10)} — expected launchToken 0x686399cb`);
  }

  await publicClient.call({
    account: account.address,
    to: prepared.to,
    data: prepared.data,
    value: prepared.value,
  });

  const hash = await walletClient.sendTransaction({
    account,
    chain: RH,
    to: prepared.to,
    data: prepared.data as Hex,
    value: prepared.value,
  });

  const receipt = await publicClient.waitForTransactionReceipt({ hash });
  const verified = verifyPonsLaunchReceipt({
    launchFactory: prepared.to,
    deployer: account.address,
    receipt: {
      status: receipt.status,
      logs: receipt.logs.map((l) => ({
        address: l.address,
        data: l.data,
        topics: l.topics,
      })),
    },
  });
  if (!verified.ok) throw new Error(verified.reason);

  return {
    txHash: hash,
    token: verified.token,
    pool: verified.pool,
    explorerTx: `https://robinhoodchain.blockscout.com/tx/${hash}`,
    explorerToken: `https://robinhoodchain.blockscout.com/token/${verified.token}`,
    ponsUrl: `https://pons.family/launchpad/${verified.token}`,
  };
}
```

### HTTP prepare (Cheshire server)

```bash
curl -sS -X POST "$ORIGIN/api/pons/launch/prepare" \
  -H 'content-type: application/json' \
  -d '{
    "name":"Cheshire Test",
    "symbol":"CTEST",
    "feeWallet":"0xYourEvmAddress",
    "launchConfigId":0,
    "dexId":0,
    "valueWei":"500000000000000"
  }'
# → { to, data, value, salt, … } then wallet_sendTransaction
```

### Proven test launch (regression reference)

- Tx: `0xe5a35a584e8ef9c09e9cd4d1953ad7d39a341c8854c024ccb36a7208a751b86c`
- Token: `0x41e6318d44E0290CDd8c77219B57D17E44Bb59aB`
- Pool: `0xc686755CECea371A99fd9CB110EDFad8af0056B1`

## On-site trading (host the market — not RH bonding)

Pons tokens are **already graduated into a locked Uniswap V3 pool** at launch. There is **no bonding-curve `buy`/`sell`**. “Host bonding” on Cheshire = **host the V3 market** via SwapRouter `exactInputSingle`.

### Trade surfaces

| Route | Page |
|-------|------|
| `/pons-launch/{token}` | `PonsTokenPage` + `PonsTradePanel` |
| `/pons/token/{token}` | same |
| `/launch/pons/{token}` | same |
| Demo | `/pons-launch/0x41e6318d44E0290CDd8c77219B57D17E44Bb59aB` |

### Trade path (source of truth)

1. `getLaunchedToken(token)` on factory → `exists`, `pairedToken`, `poolFee`, `isToken0`, `restrictionsEndBlock`, `supply`
2. V3 `dexFactory.getPool(token, pairedToken, poolFee)` → pool
3. `pool.slot0()` → `sqrtPriceX96` for spot estimate
4. Encode **SwapRouter02 `exactInputSingle`** (`0x04e45aaf`, **not** classic `0x414bf389`) to swap router `0xCaf681…`
   - **Buy**: `tokenIn=WETH`, `tokenOut=token`, `msg.value=amountIn`
   - **Sell**: approve token → router, then `tokenIn=token`, `tokenOut=WETH`, `value=0`
   - Classic deadline-in-struct selector **reverts** on this router (verified via estimateGas)
5. Precheck restriction window via `preparePonsTrade` / `assertRestrictedPoolBuyAllowed`

Helpers:

- `preparePonsExactInputSingle` — `client/src/lib/pons-launch/swap.ts`
- `preparePonsTrade` / `PONS_DEMO_TOKEN` — `client/src/lib/pons-launch/trade.ts`
- UI — `client/src/components/PonsTradePanel.tsx`

### Proven demo market (Cheshire Test V2IW)

| Field | Value |
|-------|--------|
| Token | `0x41e6318d44E0290CDd8c77219B57D17E44Bb59aB` |
| Symbol | CTV2IW |
| Pool | `0xc686755CECea371A99fd9CB110EDFad8af0056B1` |
| Fee | 10000 (1%) |
| isToken0 | false (WETH is token0) |
| Pair | WETH `0x0Bd7…AD73` |
| Router | `0xCaf681a66D020601342297493863E78C959E5cb2` |

## Restriction education (`PonsLauncherToken`)

Optional pre-trade education (pure helpers: `client/src/lib/pons-launch/policy.ts`):

- Launch-block pool buys blocked except factory atomic initial-buy exemption.
- During restriction window: max wallet BPS of supply; cumulative max-tx BPS of supply.
- After `restrictionEndBlock`: unrestricted ERC-20 transfers.

Agents do **not** set these at launch time when using `launchToken` — they are fixed by **LaunchConfig**.

## Safety rules for agents

1. **Never** print, log, or commit private keys / seed phrases.
2. Prefer **user-signed** wallet txs; agent keys only with **explicit** user approval and a funded throwaway EVM key (`RH_EVM_PRIVATE_KEY`).
3. **Confirm** name/symbol/value/chain with the user before broadcast.
4. Ensure **chain id 4663** before send.
5. Value must cover **`launchFee` + gas**; do not underpay.
6. Never claim the token is Solana `$CLAWD` or 1:1 backed.
7. Never use Solana keypairs for this path.
8. Do not use **RH bonding** factory (`0x3f60…`) for Pons launches.
9. If `launchEnabled` is false or `getLaunchConfig(0).enabled` is false — stop and report.

## Env

| Variable | Role |
|----------|------|
| `RH_RPC_URL` | Preferred RH JSON-RPC |
| `RH_EVM_PRIVATE_KEY` | Optional agent custody hex key (never commit) |
| `PONS_LAUNCH_FACTORY` | Override factory (else registry default) |
| `VITE_PONS_LAUNCH_FACTORY` | Browser mirror of factory override |

## Install this skill elsewhere

```bash
cp -R .agents/skills/pons-launch \
  ~/.agents/skills/pons-launch

# Portable repo mirror
cp -R .agents/skills/pons-launch \
  skills/pons-launch
```

Portable duplicate: `skills/pons-launch/SKILL.md` in this repository.

## Related

- Bonding-curve RH launches: skill `rh-bonded-launch`
- Cheshire Pons page: `client/src/pages/PonsPage.tsx`
- Server routes: `server/routes/pons.ts`
- Firecrawl monitor only: `server/lib/pons-firecrawl.ts` (not required for launch)
