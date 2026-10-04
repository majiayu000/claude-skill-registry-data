---
name: pons-operations
description: >
  Guides end-user and creator workflows on pons (Robinhood Chain launchpad):
  browse launches, verify token address, buy/sell, create a launch, track
  graduation, claim creator fees, community takeovers (CTO), and risk checks.
  Covers v1 (live WETH/Uniswap V3 pools) and v2 (bonding curve → Uniswap V4).
  Use when the user asks to "trade on pons", "launch a token on pons", "claim
  pons creator fees", "pons CTO", "graduate on pons", "buy pons launch",
  "pons launchpad", or "how do I use pons". DO NOT use for indexer/ABI
  integration (skill:pons-integration) or deep contract architecture
  (skill:pons-architecture).
license: MIT
---

# pons operations (users & creators)

Noncustodial launch + trade UX on Robinhood Chain. Every action is a wallet-signed transaction.

| Surface | URL |
|---------|-----|
| Launchpad | https://ponsfamily.com/launchpad |
| Docs (v1) | https://docs.ponsfamily.com/ |
| Docs (v2) | https://docs.ponsfamily.com/v2 |

## Golden rules before signing

1. **Address is identity** — names/symbols/images can be faked.
2. Confirm **chain ID 4663** (Robinhood Chain) in the wallet.
3. Read **slippage**, **price impact**, and (v2) **creator tax**.
4. **Graduation ≠ quality** — only means threshold/curve sold-out.
5. pons never asks for seed phrases or “processing” deposits.

## Identify generation

| Signal | Likely |
|--------|--------|
| Token from active/legacy factory; trades WETH pool from day one | **v1** |
| Trades on curve first; later V4 pool | **v2** |
| Docs-only; no published factory address yet | **v2 not live** — do not hardcode |

When unsure, open token page on launchpad or read factory `getLaunchedToken` (see `skill:pons-integration`).

## User workflows

### Browse and research

1. Open launchpad; pick a token.
2. Copy **token contract** address; verify on Blockscout.
3. Check: creator, liquidity, holders, quote asset (v2), fee/tax, graduation progress.
4. Prefer onchain pool price over screenshots/socials.

Detail: [references/user-trade-flows.md](references/user-trade-flows.md)

### Buy / sell (v1)

- Venue: locked **Uniswap V3** pool vs **WETH** from launch.
- Quote may differ slightly from execution; set slippage consciously.
- Near launch: buy limits may apply (see architecture); sells unrestricted.

### Buy / sell (v2)

- **Pre-grad:** trade on the **bonding curve** (buy with quote asset; sell tokens for quote).
- **Native quote:** send ETH equal to `quoteIn`.
- **Custom pair:** hold and **approve** the pair ERC-20 first.
- **Post-grad:** trade the Uniswap V4 pool (any V4-aware router); same pons fee policy via hook.
- Finishing buy may be **partially filled** + refund — accept returned amounts.

### Track graduation

| Gen | Meaning of progress | After graduate |
|-----|---------------------|----------------|
| v1 | Paired WETH toward threshold (default 4.2 ETH) | Same V3 pool continues |
| v2 | Quote raised / tokens sold vs allocation | Automatic pool create; if stuck, anyone can push |

## Creator workflows

### Create a launch (v1)

1. Set name, symbol, image, description, links, fee wallet.
2. Pay **0.0005 ETH** launch fee.
3. One tx: mint fixed **1e9** supply + live WETH pool + lock liquidity.
4. Optional initial buy on launch block (only creator can buy that block).

### Create a launch (v2)

1. Choose **enabled** launch config + **approved** quote asset (or native ETH).
2. Set metadata, `creatorFeeRecipient`, optional `creatorTaxBps` (≤ max), buyback on/off.
3. Pin economics (`expectedEconomics`) so owner config changes cannot swap terms mid-tx.
4. Pay `launchFee()`; full supply goes to curve — no pre-allocated creator bag.

### Claim fees

| Gen | How |
|-----|-----|
| v1 | Claim creator share from pons UI (accrues on locked position); automation may claim to payout wallet |
| v2 | Pull from **fee escrow** — separate balances per quote asset (and launch token for vested buybacks); claim each asset |

Redirect future fees to a new wallet without changing the token (v2: also moves buyback beneficiary). Claim accrued balances **before** redirect if needed.

Detail: [references/creator-and-fees.md](references/creator-and-fees.md)

### Community takeover (CTO)

Use when creator abandoned the project and community needs fee recipient control. Form: https://forms.gle/JjrWvybFeNfE5v8F6  

Does **not** change supply, pool, or locked liquidity. Not a safety endorsement.

## Risk checklist (copy before “done”)

- [ ] Token address verified
- [ ] Correct generation (v1 pool vs v2 curve/pool)
- [ ] Fees/tax understood
- [ ] Slippage set; size vs liquidity considered
- [ ] Custom pair (v2): pair asset risk accepted
- [ ] No seed phrase / random “support” transfer

## Navigation

| Topic | File |
|-------|------|
| Trade + graduation UX | [references/user-trade-flows.md](references/user-trade-flows.md) |
| Launch + claim + CTO | [references/creator-and-fees.md](references/creator-and-fees.md) |
| System map / addresses | `skill:pons-architecture` |
| Contracts / events / viem | `skill:pons-integration` |

## See also

- `skill:pons-architecture`, `skill:pons-integration`
