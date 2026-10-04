---
name: ai-bounty-claim
version: 3.0.0
description: Use when claiming the AI bounty on the tDVV mainnet sidechain. This public claim skill now supports Portkey AA/CA only, requires CA sync and holder preflight before any write, and routes to AA/CA onboarding, AA/CA claim, or diagnostics-only stop handling.
---

# AI Bounty Claim

Use this skill for AI bounty claiming on `tDVV` through `RewardClaimContract`.

For AA/CA, the standard wallet path in this skill is `manager signer -> CA.ManagerForwardCall -> reward.ClaimByPortkeyToCa(Hash ca_hash)`.

This skill is intentionally split into one routing file plus focused branch references so weaker agents can follow one path at a time.

## Skill Version

- Current skill version: `3.0.0`
- If behavior seems inconsistent or an external AI reports unexpected output, ask them to report the `version` field from this `SKILL.md` first.

## Compatibility

- AA/CA dependency: `@portkey/ca-agent-skills >= 2.3.0`
- AA/CA required dependency interfaces:
  - CLI: `manager-sync-status`
  - MCP: `portkey_manager_sync_status`

## Scope

Supported claim path:

- `AA/CA`: `ManagerForwardCall(...) -> ClaimByPortkeyToCa(Hash ca_hash)`

This skill does not implement:

- wallet custody or wallet creation on behalf of the user
- private key generation, storage, or import on behalf of the user
- Portkey recovery flows on behalf of the user
- blind retry loops after claim failures
- legacy public EOA claim routing

## Required Dependency Skills

Use these dependency skills explicitly instead of assuming the host will infer them:

- Portkey CA skill: `https://github.com/Portkey-Wallet/ca-agent-skills` (minimum required version `2.3.0` for the AA/CA route)

Routing rule:

- use the Portkey CA skill for local AA/CA account setup, `caHash` resolution, `manager-sync-status`, holder lookup on `tDVV`, and recovery/login only when needed to recover local context, resolve the target AA/CA on `tDVV`, or recover a usable manager signer

## Current Environment Defaults

Use these defaults only when the user is clearly operating in the current AI bounty environment:

- Chain: `tDVV`
- Environment meaning: current AI bounty mainnet sidechain environment
- Reward contract: `ELF_2fc5uPpboX9K9e9NTiDHxhCcgP8T9nV28BLyK8rDu8JmDpn472_tDVV`
- Reward contract raw address: `2fc5uPpboX9K9e9NTiDHxhCcgP8T9nV28BLyK8rDu8JmDpn472`
- Public RPC: `https://tdvv-public-node.aelf.io`
- RPC validation endpoint: `https://tdvv-public-node.aelf.io/api/blockChain/chainStatus`
- Portkey CA contract: `ELF_2UthYi7AHRdfrqc1YCfeQnjdChDLaas65bW4WxESMGMojFiXj9_tDVV`
- Portkey CA contract raw address: `2UthYi7AHRdfrqc1YCfeQnjdChDLaas65bW4WxESMGMojFiXj9`
- Current campaign default reward: Portkey AA/CA `2 AIBOUNTY`

Treat reward amounts and addresses as campaign defaults, not permanent protocol constants.

## Canonical AA/CA Claim Path

- Always use `manager signer -> Portkey CA contract ManagerForwardCall -> reward contract ClaimByPortkeyToCa(Hash ca_hash)` as the standard AA/CA wallet operation.
- Always apply this fixed read-only gate before any AA/CA write, and do not skip or reorder it:
  1. resolve the local AA/CA context and `caHash`
  2. call `manager-sync-status` or `portkey_manager_sync_status`
  3. call `GetHolderInfo(caHash)` on `tDVV`
  4. only continue when `isManagerSynced=true` and the holder can be resolved on `tDVV`
- `ClaimByPortkeyToCa(Hash ca_hash)` is permissionless at the reward method layer, but this skill still models AA/CA claiming through the standard CA wallet forwarding path.
- The forwarded reward still goes to the resolved `holderInfo.CaAddress`, not to the manager signer.
- The forwarded reward method input is `.aelf.Hash`; pass `caHash` bytes as `Hash.value`.
- For SDK or helper calls, use raw CA and reward addresses rather than the wrapped `ELF_..._tDVV` strings.
- Prefer the high-level helper `managerForwardCallWithKey(...)` in the dependency implementation. Keep lower-level protobuf and descriptor details in the AA/CA branch reference.
- If the selected CA dependency does not expose `manager-sync-status` or `portkey_manager_sync_status`, stop and tell the user to upgrade to `@portkey/ca-agent-skills >= 2.3.0` before attempting AA/CA claim.

## Gas Rules

Use these gas rules as current environment defaults:

- `AA/CA`: when the selected signer appears to have little or no `ELF`, explain that the current environment may still provide a daily gas subsidy worth `1 ELF`
- `AA/CA`: if the standard wallet path is ready after the fixed read-only gate passes, do not stop before the first send only because visible `ELF` is low or zero; show the gas note, require explicit confirmation, and allow one attempt
- `AA/CA`: never infer a fee problem from `Holder is not found`, `CA holder not found`, or any failed holder lookup; only the final chain error `Transaction fee not enough` may trigger fee guidance

Treat these gas rules as current environment defaults, not permanent protocol constants.

RPC validation note:

- the RPC root URL may return `404`
- do not treat root-path `404` as proof that the node is down
- validate node availability through `/api/blockChain/chainStatus`

## Contract Introspection Guardrail

- Do not use `/api/contract/contractViewMethodList` to conclude that the reward contract lacks write methods.
- Treat `/api/contract/contractViewMethodList` as view-only discovery. If it only shows `GetConfig`, `HasAddressClaimed`, `HasCaClaimed`, or other read methods, that only proves those view methods are visible.
- If full method verification is needed, use `/api/blockChain/contractFileDescriptorSet` only as an optional verification path, not as the default claim flow.
- When using node introspection APIs, normalize the reward contract address into the format accepted by the endpoint. Do not send the wrapped `ELF_..._tDVV` address string directly.
- If introspection is ambiguous, incomplete, or returns `Not found` because of query format issues, keep using the canonical reward contract address and the supported public AA/CA method already defined in this skill.

## Required First Step

For generic claim requests, do not jump directly to an on-chain method.

Examples:

- `help me claim`
- `claim for me`
- `帮我 Claim`
- `帮我领取`

The agent must first explain:

- `AA/CA`: account-style experience, typically based on email / guardian / recovery flows, current campaign reward is `2 AIBOUNTY`
- `AA`: this is the preferred user-facing term in this skill
- `CA`: this is still accepted as an alias because some users still say `CA`
- `AA/CA`: this route requires `@portkey/ca-agent-skills >= 2.3.0` because claim preflight depends on `manager-sync-status` and holder lookup on `tDVV`
- `AA/CA`: current environment gas experience is smoother because daily subsidy rules may apply automatically, and the first confirmed AA/CA attempt can usually be tried before fee is treated as the blocker
- `AA/CA`: before any claim write, we must first confirm manager sync and holder readiness on `tDVV`
- `EOA`: this public bounty skill no longer exposes the legacy EOA route, even if older contract source snapshots still show legacy methods

Then ask the user whether the local Portkey AA/CA context is already ready, or whether they want to recover/login first with `email`.

## Routing Rules

Choose one branch before asking for extra claim inputs.

### Branch 1: Account Choice And Onboarding

Read [references/flows/account-choice.md](./references/flows/account-choice.md) when:

- the user makes a generic claim request
- examples: `help me claim`, `claim for me`, `帮我 Claim`, `帮我领取`
- the local AA/CA account context is not ready yet
- the user only has an `email` and needs onboarding, recovery, or login first

### Branch 2: Diagnostics And Stop

Read [references/flows/diagnostics-stop.md](./references/flows/diagnostics-stop.md) first when any of the following is true:

- the user tries to fill an exchange address, custodial address, or any address without a user-controlled private key
- the user wants the agent to create or hold a wallet for them
- the user says Portkey AA/CA already exists on mainnet but cannot be resolved on `tDVV`
- the selected Portkey CA dependency is below `2.3.0` or does not expose `manager-sync-status` / `portkey_manager_sync_status`
- `manager-sync-status` returns `isManagerSynced=false`
- `GetHolderInfo(caHash)` cannot resolve the holder on `tDVV`
- the user says the guardian already exists and recovery is required
- the user insists on using an EOA-only route
- a prior contract call failed and the prerequisite is still unresolved

### Branch 3: Portkey AA/CA Claim

Read [references/flows/portkey-ca.md](./references/flows/portkey-ca.md) when:

- the user explicitly chose `AA`, `CA`, or `AA/CA`
- a local Portkey AA/CA account is already available, or the target `caHash` is already known
- use the Portkey CA skill dependency at version `>= 2.3.0` for AA/CA handling

## AA/CA Error Mapping Rules

- `Holder is not found` or `CA holder not found` means the holder, `caHash`, or target-chain context on `tDVV` is not ready yet. Tell the user to wait for sync or re-check `caHash` and chain. Do not suggest adding `ELF`.
- `Sender is not a manager of the CA holder.` means the manager context on `tDVV` is not ready yet, or the current local manager is not a valid manager for the target holder. Tell the user to recover, re-login, or wait for sync.
- `Transaction fee not enough.` is a send-stage fee problem only. Explain that it is a transaction fee issue, not a holder lookup issue.
- `NOTEXISTED` means pending transaction lookup only. Keep polling and do not treat it as success, failure, or a fee blocker.

## Fixed User Messaging

- For a newly registered `tDVV` AA/CA account, emphasize that the on-chain context is still syncing and the user should retry later.
- For an older account whose origin is `AELF` while the claim write target is `tDVV`, emphasize that cross-chain sync to the sidechain can be slower and the user should wait for manager and holder sync to complete first.
- For `Transaction fee not enough`, emphasize that the problem happened at transaction send time and is not a holder lookup problem.

## Global Hard Rules

- Always tell the user not to fill exchange or custodial addresses.
- Never offer to create, custody, or store a wallet for the user.
- Do not ask the user to paste an address when a local AA/CA context should be used.
- For generic claim requests, explain that the current public bounty path is AA/CA only, then enter onboarding or claim branching.
- Treat `AA` as the preferred user-facing term, but accept `CA` as the same route alias.
- Treat the current public bounty flow as AA/CA only, even if older contract source snapshots still contain legacy EOA entries.
- For `AA/CA`, do not attempt any write until the fixed read-only gate has passed: resolve local context and `caHash`, confirm `manager-sync-status` or `portkey_manager_sync_status` returns `isManagerSynced=true`, and confirm `GetHolderInfo(caHash)` resolves on `tDVV`.
- For `AA/CA`, if the standard wallet path is ready after that gate passes, do not stop before the first confirmed attempt only because visible `ELF` is low or zero; show the gas note and allow one confirmed attempt.
- For AA/CA, require `@portkey/ca-agent-skills >= 2.3.0` because the claim flow depends on `manager-sync-status` and `portkey_manager_sync_status`.
- When checking whether the `tDVV` RPC is reachable, query `https://tdvv-public-node.aelf.io/api/blockChain/chainStatus` instead of the site root.
- If the RPC root URL returns `404` but `/api/blockChain/chainStatus` returns chain status JSON, treat the node as reachable.
- Never use `/api/contract/contractViewMethodList` to decide that `ClaimByPortkeyToCa(Hash ca_hash)` does not exist.
- If full method verification is needed, use `/api/blockChain/contractFileDescriptorSet` only as an optional verification path.
- When using node introspection APIs, normalize the contract address first instead of querying with the wrapped `ELF_..._tDVV` string directly.
- If introspection remains ambiguous, keep the reward contract address and supported write methods defined in this skill as canonical defaults.
- For AA/CA SDK or helper calls that require raw addresses, use raw CA and reward addresses rather than the wrapped `ELF_..._tDVV` strings.
- If the local AA/CA context is not ready, guide the user to create, recover, or log in to a local `AA/CA` first, then continue with the matching claim branch.
- `Holder is not found` and `CA holder not found` mean holder or chain context is not ready; do not reinterpret them as a fee problem and do not suggest adding `ELF`.
- `Sender is not a manager of the CA holder.` means manager context is not ready or the resolved manager is not valid for the holder on `tDVV`; prefer recovery, re-login, or waiting for sync.
- `NOTEXISTED` only means the transaction is not confirmed yet; it is not a final success or failure state.
- If the final chain error is `Transaction fee not enough`, treat it as an insufficient transaction fee problem from the send stage, not as a claim logic failure and not as a holder lookup problem.
- For AA/CA, accept either `email` or `caHash` as the starting input. If only `email` is available, use the Portkey CA skill to resolve the target `caHash`, and recover a usable manager signer when needed for the standard wallet path.
- Prefer the locally resolved AA/CA context for `ManagerForwardCall(...) -> ClaimByPortkeyToCa(Hash ca_hash)`.
- Do not route the recommended AA/CA claim through deprecated `ClaimByPortkey(Hash)`.
- Before any AA/CA write, show the resolved manager signer, `manager-sync-status` result, holder lookup result, CA contract, forwarded reward contract, method chain, key inputs, expected receiver semantics, and current campaign reward amount, then require explicit user confirmation.
- If explicit confirmation is missing, stop before sending.
- If any prerequisite is unresolved, stop and explain the blocker instead of guessing.
- If a submitted transaction returns `txId`, include `txId` and `https://aelfscan.io/tDVV/tx/<txid>` in the response, even if the final result is still pending lookup.
- If a transaction fails, return the exact chain error and stop. Do not invent recovery success.

## Receiver Semantics

- `ManagerForwardCall(...) -> ClaimByPortkeyToCa(Hash ca_hash)` sends the reward to the resolved AA/CA address, not to the manager signer.

## Required Reading Pattern

After choosing the branch:

1. Read the matching flow document under `references/flows/`.
2. Read the matching example document under `references/examples/`.
3. Follow that branch only.
4. Do not mix onboarding, diagnostics, and claim instructions in one answer when only one branch is needed.

## Branch Map

- Account choice and onboarding:
  [references/flows/account-choice.md](./references/flows/account-choice.md)
  Example: [references/examples/account-choice.md](./references/examples/account-choice.md)
- Portkey AA/CA:
  [references/flows/portkey-ca.md](./references/flows/portkey-ca.md)
  Example: [references/examples/portkey-ca.md](./references/examples/portkey-ca.md)
- Diagnostics and stop:
  [references/flows/diagnostics-stop.md](./references/flows/diagnostics-stop.md)
  Example: [references/examples/diagnostics-stop.md](./references/examples/diagnostics-stop.md)
