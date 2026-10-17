---
name: l1-transaction-allowlist
description: Use when the agent needs to control who can submit transactions on an Avalanche L1 (write access) via the Transaction AllowList precompile at 0x02..02 — genesis config and on-chain role management.
category: Avalanche L1
difficulty: Intermediate
version: "0.1.0"
---

# L1 Transaction AllowList (write gating)

## Overview
The **Transaction AllowList** precompile restricts **who can submit transactions** to your L1 — the core of a permissioned-write chain. Addresses not on the list cannot transact at all.

- **Address:** `0x0200000000000000000000000000000000000002`
- **Genesis configKey:** `txAllowListConfig`
- **Interface:** the shared AllowList ([[subnet-evm-precompiles]]) — Admin/Manager/Enabled/None.

## Enable at genesis
```json
{
  "config": {
    "txAllowListConfig": {
      "blockTimestamp": 0,
      "adminAddresses": ["0xYourAdmin"],
      "managerAddresses": ["0xYourManager"],
      "enabledAddresses": ["0xUser1", "0xUser2"]
    }
  }
}
```
- **Admin** can add/remove anyone (Admins, Managers, Enabled).
- **Manager** can add/remove **Enabled** addresses only.
- **Enabled** addresses can submit transactions.
- Everyone else: **None** → transactions rejected.

`avalanche blockchain create` can set this up interactively ([[create-avalanche-l1]]).

## Manage roles on-chain
```ts
// using viem/ethers against the precompile address, from an Admin/Manager
const TX_ALLOWLIST = "0x0200000000000000000000000000000000000002";
await wallet.writeContract({ address: TX_ALLOWLIST, abi: IAllowListAbi, functionName: "setEnabled", args: [newUser] });
const role = await client.readContract({ address: TX_ALLOWLIST, abi: IAllowListAbi, functionName: "readAllowList", args: [user] });
// role: 0 = None, then Enabled/Manager/Admin values
```

## Use cases
- Consortium / enterprise chain where only KYC'd members transact.
- Closed beta / testnet where only your team submits txs.
- Regulated environments requiring participant control.

## Common Pitfalls
- **Locking yourself out.** Always keep at least one Admin (ideally a multisig — [[poa-validator-manager]]).
- **Confusing tx vs deploy gating.** This gates *all* transactions; to gate only contract *deployment* use the Deployer AllowList ([[l1-deployer-allowlist]]).
- **Reads still open.** This does not restrict RPC reads — pair with [[restrict-rpc-access]].

## AI Agent Prompt
> "Act as an L1 operator. Enable the Transaction AllowList at genesis with an admin multisig and an initial enabled set, then show how to grant/revoke transactor access on-chain."

## References
See `references/README.md` (builders-hub `docs/avalanche-l1s/precompiles/transaction-allowlist`, access-restriction course).
