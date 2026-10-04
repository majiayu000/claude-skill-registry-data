---
name: pons-architecture
description: >
  Explains the pons token launch protocol on Robinhood Chain (chain ID 4663):
  v1 (Uniswap V3 locked pool from day one) vs v2 (bonding curve then Uniswap V4
  graduation), network facts, contract roles, fees, graduation, and risk model.
  Use when the user asks about "pons", "ponsfamily", "pons v1", "pons v2",
  "Robinhood Chain launchpad", "how pons works", "pons graduation", "pons factory",
  or needs a system map before trading or integrating. DO NOT use for step-by-step
  trade/launch UX (skill:pons-operations) or indexer/ABI wiring (skill:pons-integration).
license: MIT
---

# pons architecture

**pons** (always lowercase) is a noncustodial token launch and trading protocol on **Robinhood Chain**. Users sign every launch and trade; pons never holds funds.

Official docs: [docs.ponsfamily.com](https://docs.ponsfamily.com/) · App: [ponsfamily.com/launchpad](https://ponsfamily.com/launchpad)

## Two protocol generations

| | **v1** (live) | **v2** (documented; mainnet addresses not published) |
|--|---------------|------------------------------------------------------|
| Docs | [docs.ponsfamily.com](https://docs.ponsfamily.com/) | [docs.ponsfamily.com/v2](https://docs.ponsfamily.com/v2) |
| Pre-trade venue | Uniswap **V3** pool from create | **Bonding curve** holds full supply |
| Graduation | Paired WETH reaches threshold (default **4.2 ETH**); **same pool** continues | Curve sells out → Uniswap **V4** pool + permanent lock |
| Quote asset | **WETH only** | ETH (zero address) or **approved** ERC-20 pairs |
| Liquidity lock | Active/legacy locker contracts | Launch locker (no withdraw path) |
| Status | Deployed, immutable factories | Audits in progress; treat as **unaudited / undeployed** until addresses published |

**Rule:** Tokens launched before v2 remain on v1 forever. New work must pin which generation the token uses (`getLaunchedToken` / factory address).

## Network (shared)

| Item | Value |
|------|--------|
| Chain | Robinhood Chain |
| Chain ID | `4663` |
| Native asset | ETH |
| Public RPC | `https://rpc.mainnet.chain.robinhood.com` |
| Explorer | [robinhoodchain.blockscout.com](https://robinhoodchain.blockscout.com) |

## Mental models

### v1 — pool-first

1. **Create** — token + WETH Uniswap V3 pool in one tx; liquidity locked; fixed supply **1e9**.
2. **Trade** — buys/sells vs WETH in that pool from launch; **1%** pool fee (`10000`).
3. **Graduate** — when paired WETH ≥ threshold (default **4.2 ETH**); trading stays in the **same** pool (no migration event).

Launch protection (first ~2 blocks): launch block only creator initial buy; then max **5%** supply hold / **5.5%** buy per wallet until `restrictionsEndBlock`. Sells and transfers unrestricted.

### v2 — curve-then-pool

1. **Create** — full supply minted to curve; launch fee paid; config + quote asset fixed.
2. **Trade curve** — buy/sell vs quote asset; always a counterparty.
3. **Graduate** — curve sold out; reserved tokens + collected quote seed Uniswap V4; liquidity locked forever.
4. **Pool** — ordinary V4 swaps; pons **meme hook** takes fees (pool fee field is zero).

Phases on factory record: `0` NotGraduated · `1` Swept · `2` PoolCreated · `3` Rescued. Route by **phase**, never by heuristics alone.

## Contract roles

### v1

| Role | Job |
|------|-----|
| Active / legacy factory | Deploy launches; `TokenLaunched`; `getLaunchedToken`; `graduationStatus` |
| Active / legacy locker | Locked position; fee share snapshot; creator payout redirect |
| Uniswap V3 factory / PM / router / quoter | Pool infra |
| Launch token | Self-describing ERC-20 + `liquidityPool`, `logo`, `socials`, etc. |

Addresses: [references/v1-contracts.md](references/v1-contracts.md)

### v2

| Role | Job |
|------|-----|
| Launch factory | `launchToken`, configs, graduation, takeovers |
| Bonding curve (per launch) | Pre-grad buy/sell pricing |
| Launch token (per launch) | Fixed-supply ERC-20 |
| Meme hook (singleton) | Post-grad fee accrual/split |
| Fee escrow | Claimable creator/protocol balances |
| Buyback vault | 5-year linear vest of bought-back supply |
| Launch locker | Permanent LP + excess supply |

Addresses: **not published** until audits close. Source: [references/v2-contracts.md](references/v2-contracts.md)

## Fees (high level)

| Generation | Trader pays | Split notes |
|------------|-------------|-------------|
| v1 | 1% pool fee | Creator/protocol snapshotted at launch: **70/30** current factory (≥ block 8991118); **90/10** legacy. Creator claims from interface; automation may claim for them. |
| v2 | Base trade fee + optional **creator tax** (capped, fixed at create) | Protocol share first; optional buyback from creator slice; remainder + full creator tax → creator. Same rates curve and post-grad. Fees claimed from **escrow** (pull, not push). |

Protocol (v1 docs): ~80% of protocol fees → PONS buyback TWAP (not yet immutable); ~20% ops. Burning does not guarantee higher price.

## Invariants agents must not invent

- **Names/symbols are not unique** — only the **token address** is canonical.
- **Graduation ≠ quality** — threshold/curve sold-out only.
- **v1:** no bonding curve, no migration after graduate.
- **v2:** no snipe-able day-one pool; creator cannot mint, raise tax, unlock LP, or change quote after create.
- Product name is **pons** (lowercase); do not imply official partnership without written agreement.

## Read by task

| Need | Open |
|------|------|
| v1 addresses, params, fee blocks | [references/v1-contracts.md](references/v1-contracts.md) |
| v2 components, phases, reserved supply math | [references/v2-contracts.md](references/v2-contracts.md) |
| Risks, CTO, disclosures | [references/risk-and-governance.md](references/risk-and-governance.md) |
| User flows | `skill:pons-operations` |
| Indexers, ABIs, swaps | `skill:pons-integration` |

## See also

- `skill:pons-operations`, `skill:pons-integration`
- Family meta: `pons-family/SOURCES.md`, `pons-family/COVERAGE.md`
- Related: Uniswap V3/V4 skills when routing post-grad V4 pools
