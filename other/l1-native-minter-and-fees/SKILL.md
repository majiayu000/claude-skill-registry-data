---
name: l1-native-minter-and-fees
description: Use when the agent needs custom tokenomics on an Avalanche L1 — the Native Minter (mint the native gas token), Fee Manager (adjust fee config), and Reward Manager (route gas fees) precompiles, with their addresses and config keys.
category: Avalanche L1
difficulty: Intermediate
version: "0.1.0"
---

# L1 Native Minter, Fee Manager & Reward Manager

## Overview
Three precompiles let you control the economics of your L1's native (gas) token. All use the AllowList role model where relevant ([[subnet-evm-precompiles]]).

| Precompile | Address | configKey | Purpose |
|---|---|---|---|
| Native Minter | `0x0200000000000000000000000000000000000001` | `contractNativeMinterConfig` | mint new native gas token to addresses |
| Fee Manager | `0x0200000000000000000000000000000000000003` | `feeManagerConfig` | change the chain's fee/gas config at runtime |
| Reward Manager | `0x0200000000000000000000000000000000000004` | `rewardManagerConfig` | control where transaction fees go |

## Native Minter
Mint your L1's native token to any address (only **Enabled**/Admin callers).
```solidity
interface INativeMinter { function mintNativeCoin(address addr, uint256 amount) external; }
// constant: 0x0200000000000000000000000000000000000001
```
Use for: controlled token issuance, faucets, rewards programs, bridging-in native supply.

## Fee Manager
Adjust fee parameters (base fee, gas limits, target block rate, etc.) without a hard fork — useful as load changes. Enabled addresses call `setFeeConfig(...)`. Genesis sets the initial fee config.

## Reward Manager
Decide the destination of collected transaction fees:
- **Burn** them (deflationary), or
- Route them to a **specific fee-recipient address** (e.g. treasury), or
- Allow per-block coinbase recipients.

## Genesis example
```json
{
  "config": {
    "contractNativeMinterConfig": { "blockTimestamp": 0, "adminAddresses": ["0xAdmin"] },
    "feeManagerConfig":          { "blockTimestamp": 0, "adminAddresses": ["0xAdmin"] },
    "rewardManagerConfig":       { "blockTimestamp": 0, "adminAddresses": ["0xAdmin"] }
  }
}
```

## Common Pitfalls
- **Unbounded minting.** Native Minter is powerful; restrict the Enabled set and prefer a multisig Admin.
- **Fee config foot-guns.** Misconfigured gas limits/base fee can stall the chain; test on local/Fuji first.
- **Reward routing surprises.** If you stop burning and route to a treasury, model the incentive/economic impact.

## AI Agent Prompt
> "Act as an L1 tokenomics engineer. Configure the Native Minter, Fee Manager, and Reward Manager at genesis for a chain with a custom gas token, controlled issuance, and treasury fee routing — and explain the risks."

## References
See `references/README.md` (builders-hub `docs/avalanche-l1s/precompiles/{native-minter,fee-manager,reward-manager}`, academy l1-native-tokenomics).
