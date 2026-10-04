---
name: crane-morpho
description: This skill should be used when the user asks about "Crane Morpho", "MorphoBlueService", "TestBase_MorphoBlue", "Morpho port", "Morpho fork parity", "FOUNDRY_PROFILE=morpho_port", "MorphoBlueAwareRepo", integrating Morpho into a Diamond/strategy, or writing Foundry tests against Crane's Morpho port.
license: MIT
---

# Crane Morpho Integration

How to **build on** and **test** Morpho using Crane’s port (not how Morpho works in general — see architecture/ops skills).

## Layout

| Layer | Path |
|-------|------|
| Domain | `contracts/external/morpho/{blue,blue-irm,blue-oracles,metamorpho-v1.1,public-allocator,vault-v2,bundler3}/` |
| Wrappers | `contracts/protocols/lending/morpho/{blue,metamorpho,vault-v2,bundler}/` |
| Hermetic tests | `test/foundry/spec/protocols/lending/morpho/` |
| Fork tests | `test/foundry/fork/{ethereum_main,base_main}/morpho/` |
| Constants | `contracts/constants/networks/*` |

Each domain package has `VENDOR.md` (pin + license + adaptations).

## Quick start: strategy / Diamond

```solidity
import {MorphoBlueAwareRepo} from
    "@crane/contracts/protocols/lending/morpho/blue/aware/MorphoBlueAwareRepo.sol";
import {MorphoBlueService} from
    "@crane/contracts/protocols/lending/morpho/blue/services/MorphoBlueService.sol";
import {IMorpho, MarketParams} from
    "@crane/contracts/external/morpho/blue/interfaces/IMorpho.sol";

// init (once)
MorphoBlueAwareRepo._initialize(morpho, irm, oracleFactory);

// ops — tokens must sit on this contract
IMorpho m = MorphoBlueAwareRepo._morpho();
MorphoBlueService._supply(m, marketParams, amount, address(this));
MorphoBlueService._supplyCollateral(m, marketParams, coll, address(this));
MorphoBlueService._borrow(m, marketParams, debt, address(this), address(this));
```

**Service = library context of caller.** Do not `vm.prank(user)` + Service unless the user is the contract holding inventory.

## Testing ladder

| Layer | Command / base |
|-------|----------------|
| Domain compile | `FOUNDRY_PROFILE=morpho_port forge build` |
| Blue upstream | `forge test --match-path '…/morpho/blue/upstream/**'` |
| Crane hermetic | `TestBase_MorphoBlue`, `TestBase_MetaMorpho` |
| Fork parity | `MorphoBluePortedMarketParity_Fork` ETH + Base |
| Profile | Always set `FOUNDRY_PROFILE=morpho_port` for Morpho work |

Default monorepo profile **skips** `contracts/external/**` — Morpho still compiles when tests import it, but path-scoped Morpho CI should use `morpho_port`.

## Production-first rules

- Never `vm.mockCall` Morpho/MetaMorpho SUT.
- Hermetic: `new Morpho` / factory / IRM from vendored sources.
- Fork: bind `ETHEREUM_MAIN.MORPHO` / `BASE_MAIN.MORPHO`; parity uses **second local Morpho**.
- Exact deltas / share equality — not “balance increased”.

## Navigation

| Topic | File |
|-------|------|
| Service + Aware API | `references/service-and-aware.md` |
| TestBase inheritance | `references/testbases.md` |
| Fork parity recipe | `references/fork-parity.md` |
| Commands checklist | `references/commands.md` |
| Protocol meaning | `skill:morpho-architecture` |
| User ops | `skill:morpho-blue-operations`, `skill:morpho-vaults` |

## Key files

- `MorphoBlueService.sol`, `MorphoBlueAwareRepo.sol`, `Behavior_IMorpho.sol`
- `TestBase_MorphoBlue.sol`, `TestBase_MetaMorpho.sol`
- `MorphoBluePortedMarketParity_Fork.t.sol` (ETH + Base)
- Plan: `docs/superpowers/plans/2026-07-27-morpho-port.md`

## See also

- `skill:crane-testing`, `skill:crane-porting`, `skill:crane-porting-verification`
- `skill:crane-architecture` (AwareRepo / Service patterns)
