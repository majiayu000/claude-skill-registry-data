---
name: crane-netnet
description: >-
  Guides Crane integration with the NetNet Capital ($NET) port under protocols/pol/net.
  Use when the user asks about "Crane NetNet", "TestBase_NetNet", "protocols/pol/net",
  "NetNetSpotService", "NET FoT", NetNetStakingService, NetNetBondService,
  NetNetTurboService, or TestBase_NetNetFork. DO NOT use for Olympus, RwaDesk, arcade
  desks, or a netnet-architecture / netnet-operations family.
license: MIT
---

# Crane NetNet Integration

How to **build on** and **test** the NetNet Capital port (P0). Domain lives only under `contracts/protocols/pol/net/`. No DFPkg. No `[profile.netnet_port]`.

## Layout

| Layer | Path |
|-------|------|
| Domain | `contracts/protocols/pol/net/src/` |
| Aware | `contracts/protocols/pol/net/aware/NetNetAwareRepo.sol` (slot `protocols.pol.net.aware`) |
| Services | `contracts/protocols/pol/net/services/NetNet{Spot,Staking,Bond,Turbo}Service.sol` |
| TestBases | `TestBase_NetNet`, `TestBase_NetNetFork` |
| Hermetic / comparative | `test/foundry/spec/protocols/pol/net/{hermetic,comparative}/` |
| Fork | `test/foundry/spec/protocols/pol/net/fork/` |
| Pin | `VENDOR.md` dump `2026-08-28`; fork `ROBINHOOD_MAIN.DEFAULT_FORK_BLOCK` |

## Quick start

```solidity
import {NetNetAwareRepo} from
    "@crane/contracts/protocols/pol/net/aware/NetNetAwareRepo.sol";
import {NetNetSpotService} from
    "@crane/contracts/protocols/pol/net/services/NetNetSpotService.sol";

NetNetAwareRepo._initialize(init);
NetNetSpotService._buyNetWithUsdg(buyParams); // tokens sit on this contract
```

**Service = library context of caller.** Do not `vm.prank(user)` + Service unless the user is the contract holding inventory.

## Four services

| Library | Flows |
|---------|-------|
| `NetNetSpotService` | FoT buy/sell (`path [usdg,net]` / `[net,usdg]`), `TaxCollector.convert` |
| `NetNetStakingService` | `stake` / `unstake` / `rebase` |
| `NetNetBondService` | BondDepository deposit/redeem (P0 `marketId == 0`), InverseBond, PremiumSeller, pTEAM |
| `NetNetTurboService` | Morpho `setAuthorization`, TurboRouter turbo/unwind |

A fifth Service file is forbidden.

## TestBases

- `TestBase_NetNet` inherits `TestBase_UniswapV2`, deploys Morpho Blue + Vault V2 itself (does **not** inherit `TestBase_MorphoBlue`). Real `wire()` + `GenesisBond.finalize()`.
- `TestBase_NetNetFork` binds `ROBINHOOD_MAIN` at `DEFAULT_FORK_BLOCK`.

Constants: tax 500 bps, team start 400 bps, vest 2 days, epoch 8 hours, `TARGET_LTV_WAD` 0.53125e18 (`Constants.*` / `LendingConstants.*`).

## Commands

```bash
forge test --match-path 'test/foundry/spec/protocols/pol/net/**'
FOUNDRY_PROFILE=fork forge test --match-path 'test/foundry/spec/protocols/pol/net/fork/**'
```

Default `forge test` skips `**/fork/**` (no RPC). Do not add `[profile.netnet_port]` or `NETNET_FORK_BLOCK`. `viaIR` stays false.

## Production-first

- Never `vm.mockCall` NET, Staking, Treasury, BondDepository, TaxCollector, PTeam, TurboRouter, LoopbackOracle, Zap, wsNET, Uni pair/router, Morpho Blue, or Vault V2.
- No `assertEq(portOut, forkOut)` for market amounts.
- USDG hermetic double is mintable 6-decimal `NetNetUsdg`, not an SUT mock.

## Navigation

| Topic | File |
|-------|------|
| Service + Aware API | `references/services.md` |
| TestBase boot | `references/testbases.md` |
| Forge commands | `references/commands.md` |

## See also

- `skill:crane-porting`, `skill:crane-testing`, `skill:crane-morpho`, `skill:crane-uniswap`
