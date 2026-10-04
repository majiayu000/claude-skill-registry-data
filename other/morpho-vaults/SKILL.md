---
name: morpho-vaults
description: This skill should be used when the user asks about "MetaMorpho", "Morpho vault deposit", "Morpho ERC4626", "reallocate Morpho", "Public Allocator", "Vault V2 Morpho", "Morpho curator", "supplyQueue", "Bundler3", "atomic Morpho multicall", or needs to use Morpho vaults as an end user or integrate curated vault products.
license: MIT
---

# Morpho Vaults & Bundler

End-user and integrator guide for **MetaMorpho V1.1**, **Public Allocator**, **Vault V2**, and **Bundler3**.

## Choose a path

| Goal | Product | Entry |
|------|---------|--------|
| Deposit loan asset, earn curated yield | MetaMorpho V1.1 | ERC-4626 `deposit` / `mint` |
| Curate markets / caps / queues | MetaMorpho roles | owner / curator / allocator / guardian |
| Permissionless rebalance within caps | Public Allocator | `reallocateTo` |
| Next-gen vault + adapters | Vault V2 | `VaultV2Factory.createVaultV2` |
| One-tx multi-step Blue/vault UX | Bundler3 | `multicall(Call[])` |

## Quick start: MetaMorpho deposit (end user)

```solidity
import {IMetaMorphoV1_1} from
    "@crane/contracts/external/morpho/metamorpho-v1.1/interfaces/IMetaMorphoV1_1.sol";

IMetaMorphoV1_1 vault = IMetaMorphoV1_1(vaultAddress);
IERC20 asset = IERC20(vault.asset());

asset.approve(address(vault), assets);
uint256 shares = vault.deposit(assets, receiver);
// later:
vault.redeem(shares, receiver, owner);
```

Factory (hermetic / new vault):

```solidity
MetaMorphoV1_1Factory factory = new MetaMorphoV1_1Factory(address(morpho));
IMetaMorphoV1_1 vault = factory.createMetaMorpho(
    initialOwner, initialTimelock, asset, name, symbol, salt
);
```

## MetaMorpho roles (integrator/curator)

| Role | Typical powers |
|------|----------------|
| **Owner** | Timelock, fee, guardian accept paths, ownership |
| **Curator** | Submit caps, market enablement paths |
| **Allocator** | `setSupplyQueue`, `reallocate` |
| **Guardian** | Emergency revokes (with timelock rules) |

Cap flow (simplified):

1. Curator `submitCap(marketParams, cap)`  
2. Wait timelock  
3. Anyone `acceptCap(marketParams)`  
4. Allocator sets `supplyQueue` including market `Id`  
5. Deposits allocate along the queue subject to caps  

## Public Allocator

Permissionless reallocation **within flow caps** set by vault admin:

```solidity
// Conceptual — see PublicAllocator.sol
publicAllocator.reallocateTo(vault, withdrawals, supplyMarketParams);
```

Requires vault to authorize the allocator and flow caps configured.

## Vault V2 (smoke-level)

```solidity
VaultV2Factory f = new VaultV2Factory();
address vault = f.createVaultV2(owner, asset, salt);
// Configure adapters (MarketV1 / VaultV1) and caps via owner/curator APIs
```

Domain: `contracts/external/morpho/vault-v2/`. Adapter realAssets reporting is critical for share price.

## Bundler3 (atomic UX)

```solidity
import {Bundler3} from "@crane/contracts/external/morpho/bundler3/Bundler3.sol";
import {Call} from "@crane/contracts/external/morpho/bundler3/interfaces/IBundler3.sol";

// Empty bundle reverts EmptyBundle()
Call[] memory bundle = new Call[](n);
// Fill adapter calls (GeneralAdapter1 supplyCollateral, borrow, …)
bundler.multicall{value: msg.value}(bundle);
```

Live addresses: `ETHEREUM_MAIN.MORPHO_BUNDLER3`, `MORPHO_GENERAL_ADAPTER_1`, etc.

## Navigation

| Topic | File |
|-------|------|
| MetaMorpho setup & hermetic TestBase | `references/metamorpho.md` |
| Bundler3 Call encoding notes | `references/bundler3.md` |
| Vault V2 adapters | `references/vault-v2.md` |
| Raw Blue markets | `skill:morpho-blue-operations` |
| Crane tests / ports | `skill:crane-morpho` |

## Key files

- `contracts/external/morpho/metamorpho-v1.1/MetaMorphoV1_1.sol`
- `contracts/external/morpho/public-allocator/PublicAllocator.sol`
- `contracts/external/morpho/vault-v2/VaultV2.sol`
- `contracts/external/morpho/bundler3/Bundler3.sol`
- Crane: `TestBase_MetaMorpho`, `MetaMorphoLifecycle.t.sol`, vault/bundler smokes

## Constraints

- MetaMorpho needs asset **`decimals()`** (use OZ ERC20 or Crane-extended mocks).
- First deposit inflation risk if decimals offset is 0 — seed vault or check share price.
- Crane has **no MetaMorpho DFPkg** in first merge — deploy factory + vault via `new` / CREATE2 salt.
- Upstream skips: see `test/.../metamorpho/upstream/SKIPPED.md` (IERC777 reentrancy, URD).

## See also

- `skill:morpho-architecture`, `skill:morpho-blue-operations`, `skill:crane-morpho`
- `skill:crane-tokens` (ERC-4626 patterns)
