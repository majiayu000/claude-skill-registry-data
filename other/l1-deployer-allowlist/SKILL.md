---
name: l1-deployer-allowlist
description: Use when the agent needs to control who can deploy contracts on an Avalanche L1 (KYC-style gating) via the Contract Deployer AllowList precompile at 0x02..00 — genesis config and role management.
category: Avalanche L1
difficulty: Intermediate
version: "0.1.0"
---

# L1 Contract Deployer AllowList (deploy gating)

## Overview
The **Contract Deployer AllowList** precompile restricts **who can deploy smart contracts** on your L1. Transactions can still flow (unless you also use the tx allowlist), but only allowed addresses can create contracts — ideal for KYC-gated or curated app environments.

- **Address:** `0x0200000000000000000000000000000000000000`
- **Genesis configKey:** `contractDeployerAllowListConfig`
- **Interface:** shared AllowList ([[subnet-evm-precompiles]]) — Admin/Manager/Enabled/None.

## Enable at genesis
```json
{
  "config": {
    "contractDeployerAllowListConfig": {
      "blockTimestamp": 0,
      "adminAddresses": ["0xYourAdmin"],
      "managerAddresses": [],
      "enabledAddresses": ["0xDeployer1"]
    }
  }
}
```
- **Enabled** addresses may deploy contracts; **None** cannot. Admin/Manager manage the list (Manager → Enabled only).

## Manage roles on-chain
```ts
const DEPLOYER_ALLOWLIST = "0x0200000000000000000000000000000000000000";
await wallet.writeContract({ address: DEPLOYER_ALLOWLIST, abi: IAllowListAbi, functionName: "setEnabled", args: [dev] });
await wallet.writeContract({ address: DEPLOYER_ALLOWLIST, abi: IAllowListAbi, functionName: "setNone",    args: [dev] }); // revoke
```

## Pattern: KYC-gated deployment
Combine with a custom precompile or off-chain KYC: an admin/manager only calls `setEnabled` after a deployer passes KYC. This enforces a "permissioned-public" model — public reads, curated deployers.

## Use cases
- App chains where only audited/approved teams deploy.
- Regulated DeFi where deployers must be KYC'd.
- Preventing arbitrary/malicious contracts on a shared enterprise L1.

## Common Pitfalls
- **Deploys blocked but txs open (or vice versa).** This gates *deployment* only; gate transactions separately ([[l1-transaction-allowlist]]).
- **No admin at genesis** → cannot grant deploy rights later without a network upgrade ([[precompile-genesis-and-upgrades]]).
- **Reads still public.** Restrict RPC for access privacy ([[restrict-rpc-access]]).

## AI Agent Prompt
> "Act as an L1 operator. Enable the Contract Deployer AllowList at genesis, then implement a KYC-gated flow where an admin grants `setEnabled` only to approved deployers."

## References
See `references/README.md` (builders-hub `docs/avalanche-l1s/precompiles/deployer-allowlist`, access-restriction course).
