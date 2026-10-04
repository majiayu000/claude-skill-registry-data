---
name: pons-integration
description: >
  Integrates with the pons protocol onchain: Robinhood Chain RPC, v1 factory/locker
  addresses, TokenLaunched and Swap indexing, token self-describing reads, V3 pricing
  and graduationStatus, v2 curve buy/sell, launchToken, fee escrow, events, and Uniswap
  V4 pool keys. Use when the user asks to "index pons", "integrate pons", "pons
  TokenLaunched", "pons factory ABI", "trade pons via viem", "pons graduationStatus",
  "build a pons bot", "pons quoter", or "Robinhood Chain 4663 launchpad SDK". DO NOT use
  for pure product UX walkthroughs (skill:pons-operations) or high-level system narrative
  alone (skill:pons-architecture).
license: MIT
---

# pons integration (builders)

**Trust model:** everything authoritative is **onchain**. Optional HTTP helpers exist for UX only. Index factory + venue events (v1 pools / v2 curves) for a trust-minimized source of truth.

Docs: [v1](https://docs.ponsfamily.com/) · [v2](https://docs.ponsfamily.com/v2) · [llms.txt](https://docs.ponsfamily.com/llms.txt)

## Quick facts

| Item | Value |
|------|--------|
| Chain ID | `4663` |
| RPC | `https://rpc.mainnet.chain.robinhood.com` |
| Explorer | https://robinhoodchain.blockscout.com |
| Active factory (v1) | `0xA5aAb3F0c6EeadF30Ef1D3Eb997108E976351feB` |
| Active locker (v1) | `0x736D76699C26D0d966744cAe304C000d471f7F35` |
| WETH (v1 quote) | `0x0Bd7D308f8E1639FAb988df18A8011f41EAcAD73` |
| v2 addresses | **Not published** until audits complete |

## Integration checklist

1. Pin **generation** (v1 factory vs future v2 factory).
2. Backfill logs in **bounded block chunks** — wide `eth_getLogs` on public RPC times out.
3. Start v1 active factory from block **8991118** (legacy **8600612**).
4. Register each launched pool/curve; index trades from that address.
5. Never trust name/symbol uniqueness.
6. Prefer return values / events over assumed fill amounts (v2 partial fills).
7. Optional UX APIs (not trust root):  
   - `https://ponsfamily.com/api/pons-launches`  
   - `https://ponsfamily.com/api/pons-token/{token}`  
   - `https://ponsfamily.com/api/pons-market/{token}`

## v1 — minimum integration path

```text
1. getLogs TokenLaunched on factory
2. For each pool: getLogs Swap; derive buy/sell from amount signs + token order
3. Metadata: token ERC-20 + logo/description/socials/liquidityPool
4. Launch record: factory.getLaunchedToken(token)  // includes isToken0, restrictionsEndBlock
5. Price: pool.slot0 sqrtPriceX96 → priceInWeth (both 18 decimals)
6. Graduation: factory.graduationStatus(token) → (pairedPrincipal, threshold, graduated)
7. Swaps: Uniswap V3 router 0xCaf…cb2 + quoter 0x33e…9E7
```

| Need | Open |
|------|------|
| Addresses, topic0, buy/sell side math | [references/v1-indexing-and-reads.md](references/v1-indexing-and-reads.md) |
| Pricing, graduation, fee split reads | same file |

## v2 — minimum integration path

```text
1. Index factory TokenLaunched (token, curve, pairToken, config, threshold)
2. Index curve CurveBuy / CurveSell / refunds / completion
3. Route by getLaunchedToken.phase (0 curve, 1 push pool, 2 V4, 3 rescued)
4. Pre-grad: curve.buy / sell with minOut + correct native value rules
5. Post-grad: Uniswap V4 pool key (fee 0, meme hook); any V4 router
6. Fees: fee escrow claim/claimToken; index Credited* / Claimed*
7. Optional: buyback vault vest; pending CTO recipient
```

| Need | Open |
|------|------|
| Launch, trade, events, errors, V4 key | [references/v2-onchain-api.md](references/v2-onchain-api.md) |

## Common gotchas

- **Public RPC log ranges** — chunk backfills; do not `fromBlock: earliest` to latest in one call.
- **v1 trade side:**  
  `tokenIsToken0 = token < pairToken`; pair leg signed amount `> 0` → buy of token.
- **v1 graduation:** poll `graduationStatus`; there is **no** migration event.
- **v2 native buy:** `msg.value` must equal `quoteIn`; custom pair: approve curve, **no** value.
- **v2 economics pin:** re-read `previewLaunchEconomics` on `LaunchEconomicsMismatch`.
- **v2 fee total for UX:** `feeBps + creatorTaxBps` on quote leg.
- **Attribution:** product name **pons** lowercase; no implied partnership.

## Support

contact@ponsfamily.com — indexing, pricing, trade wiring, partnerships, quote-asset proposals, v2 early access.

## See also

- `skill:pons-architecture` — v1/v2 map, addresses tables  
- `skill:pons-operations` — user/creator product flows  
- Uniswap V3/V4 skills for router-level swap construction  
