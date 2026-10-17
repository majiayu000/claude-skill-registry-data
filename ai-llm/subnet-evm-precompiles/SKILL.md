---
name: subnet-evm-precompiles
description: Use when the agent needs the overview of Subnet-EVM stateful precompiles and the shared AllowList interface (Admin/Manager/Enabled/None roles) — the foundation for permissioning an Avalanche L1. Includes the fixed precompile addresses and config keys.
category: Avalanche L1
difficulty: Intermediate
version: "0.1.0"
---

# Subnet-EVM Precompiles & the AllowList Interface

## Overview
**Subnet-EVM** (repo `subnet-evm`) is Avalanche's EVM fork. It ships **stateful precompiles** — native modules at fixed addresses, configured in genesis or via upgrade — that implement allowlisting, native minting, fee control, rewards, and interchain messaging. They are how you turn a generic EVM into a *permissioned* chain without writing core changes.

## The default precompiles
| Precompile | Address | Genesis configKey | Gates / Purpose |
|---|---|---|---|
| Contract Deployer AllowList | `0x0200000000000000000000000000000000000000` | `contractDeployerAllowListConfig` | who can deploy contracts ([[l1-deployer-allowlist]]) |
| Native Minter | `0x0200000000000000000000000000000000000001` | `contractNativeMinterConfig` | who can mint the native gas token ([[l1-native-minter-and-fees]]) |
| Transaction AllowList | `0x0200000000000000000000000000000000000002` | `txAllowListConfig` | who can submit transactions ([[l1-transaction-allowlist]]) |
| Fee Manager | `0x0200000000000000000000000000000000000003` | `feeManagerConfig` | who can change fee config ([[l1-native-minter-and-fees]]) |
| Reward Manager | `0x0200000000000000000000000000000000000004` | `rewardManagerConfig` | fee reward routing ([[l1-native-minter-and-fees]]) |
| Warp Messenger | `0x0200000000000000000000000000000000000005` | (interchain messaging) | cross-L1 messages |

## The shared AllowList interface
Most permissioning precompiles use the same **role-based access control** interface.
Roles (high → low): **Admin** (manage all roles) > **Manager** (manage Enabled only) > **Enabled** (use the precompile) > **None** (no access).
```solidity
interface IAllowList {
  function setAdmin(address addr) external;    // grant Admin
  function setManager(address addr) external;  // grant Manager
  function setEnabled(address addr) external;  // grant Enabled
  function setNone(address addr) external;     // revoke to None
  function readAllowList(address addr) external view returns (uint256); // role value
}
```
Call these directly on the precompile address (e.g. with ethers/viem) using an Admin/Manager account ([[precompile-genesis-and-upgrades]]).

## Genesis vs upgrade
Precompiles can be **active from genesis** or **activated/deactivated later** via a network `upgrade.json` (precompile upgrade). See [[precompile-genesis-and-upgrades]].

## Custom precompiles
Beyond the defaults, Subnet-EVM lets you author your own stateful precompiles (e.g. enforce KYC checks). Covered in builders-hub `docs/avalanche-l1s/custom-precompiles`.

## Common Pitfalls
- **Wrong role expectations.** Managers can only manage Enabled addresses, not other Admins/Managers.
- **No Admin set at genesis.** You then can't change roles without a network upgrade.
- **Assuming reads are gated.** Allowlists gate writes/deploys, not RPC reads — restrict RPC separately ([[restrict-rpc-access]]).

## AI Agent Prompt
> "Act as a Subnet-EVM expert. Explain the stateful precompiles, their fixed addresses and config keys, and how the AllowList Admin/Manager/Enabled/None roles work, then show how to grant roles on-chain."

## References
See `references/README.md` (subnet-evm repo, builders-hub `docs/avalanche-l1s/precompiles`, access-restriction course).
