---
name: precompile-genesis-and-upgrades
description: Use when the agent needs to activate, deactivate, or reconfigure Avalanche L1 precompiles — at genesis vs later via a network upgrade.json — and the operational steps to roll an upgrade across validators.
category: Avalanche L1
difficulty: Advanced
version: "0.1.0"
---

# Precompile Activation: Genesis vs Network Upgrade

## Overview
Subnet-EVM precompiles ([[subnet-evm-precompiles]]) can be turned on at **genesis** or **activated/deactivated/reconfigured later** via a coordinated **network upgrade**. Choosing correctly matters because genesis config is baked in, while upgrades require all validators to apply the same change at the same activation timestamp.

## Option A — Activate at genesis
Put the precompile's `*Config` block in `genesis.json` with `blockTimestamp: 0` and the initial roles. Simplest for new chains; chosen via `avalanche blockchain create` ([[create-avalanche-l1]]).
```json
"txAllowListConfig": { "blockTimestamp": 0, "adminAddresses": ["0xAdmin"] }
```

## Option B — Activate/deactivate via network upgrade
Use an **`upgrade.json`** that schedules a precompile change at a future `blockTimestamp`. Every node must run the same `upgrade.json` before that timestamp.

```json
{
  "precompileUpgrades": [
    {
      "txAllowListConfig": {
        "blockTimestamp": 1735689600,
        "adminAddresses": ["0xAdmin"]
      }
    },
    {
      "txAllowListConfig": { "blockTimestamp": 1735693200 }   // empty body after = disable
    }
  ]
}
```
Rules:
- **Ordering:** upgrades are applied in increasing `blockTimestamp` order.
- **To enable:** provide the config with roles. **To disable:** schedule a later entry with an empty/disabling config.
- **Consistency:** all validators must have the same upgrade file; mismatches cause them to disagree and stall.

## Operational rollout (network upgrade)
1. Author/modify `upgrade.json` with a `blockTimestamp` safely in the future.
2. Distribute it to **every** validator's chain-config directory.
3. Restart nodes so they load the upgrade.
4. Verify each validator reads the same config; confirm activation after the timestamp passes; test the new precompile behavior.

## When to use which
- **New chain / known requirements** → genesis.
- **Live chain / new requirement, recovering from a lost admin, or rotating policy** → network upgrade.

## Common Pitfalls
- **Past or too-soon timestamp.** Set `blockTimestamp` comfortably in the future so all validators upgrade in time.
- **Partial rollout.** If some validators lack the upgrade, the network forks/stalls.
- **Disabling syntax.** Deactivation is a *later* scheduled entry, not deletion of the original.

## AI Agent Prompt
> "Act as an L1 operator. Write an `upgrade.json` to activate the Transaction AllowList at a future timestamp on a live L1, then describe the validator rollout and verification steps."

## References
See `references/README.md` (builders-hub `docs/avalanche-l1s/upgrade/precompile-upgrades`, academy access-restriction network-upgrade modules).
