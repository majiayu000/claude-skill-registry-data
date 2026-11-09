---
name: plan-web3-game-assets
description: Define an opt-in Ethereum, Base or Immutable game-asset lifecycle, including token identity, supply, rights, custody, game eligibility and chain-specific dependencies.
engines: [AGNOSTIC]
---

## When to use

Use when a game needs blockchain-owned assets, NFT collections, transferable inventory or a Web3 asset economy. A visual asset request alone does not select blockchain integration.

## Workflow

Read the host `WEB3.md`, `web3-game.json` and the shared `.web3/CONTRACT.md` when configured. Use `commands/web3-game.sh registry` and local `inspect`, `validate` or `doctor`; these do not contact a chain. Preserve ENGINE, ARCHITECTURE, STYLE and independent media selection.

Define the actual lifecycle using [the asset brief](references/asset-brief.md). Separate card/item definitions, unique instances or interchangeable quantities, wallet control, on-chain ownership, gameplay entitlement and content licenses. Keep authoritative game rules separate from arbitrary NFT metadata.

Honor explicit Ethereum mainnet, Base or current Immutable selection. Refresh the dated chain/compiler/operator facts from primary sources before production. Do not replace L1 with a cheaper chain or treat retired Immutable X as the EVM target. Disclose managed chain ingress/operator dependencies and optional hosted products separately.

Choose the transfer-during-match rule before implementing admission. A snapshot license can permit an admitted match to finish after sale; a server reservation cannot stop external transfers. Strict exclusivity needs a reviewed contract-enforced lock/escrow with custody and recovery decisions. Never select custody silently.

Prepare the complete proposed policy, asset/content ancestry, numerical limits and open production decisions for user review. Explicit `init --spec reviewed-spec.json` creates fresh host files; it neither proves approval nor selects services. Route contract, wallet, ownership, trading and lifecycle verification to their focused skills and resolve the selected engine's concrete integration owners.

## Output

Return a reviewed lifecycle specification, exact chain/collection/content identities, authority and dependency map, failure/recovery rules, evidence requirements and any unresolved decisions. Keep configuration and installation separate from signing, transactions, live deployment, asset promotion and release.
