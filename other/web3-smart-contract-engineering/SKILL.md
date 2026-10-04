---
name: web3-smart-contract-engineering
description: Use when writing, reviewing, or deploying Solidity smart contracts — token contracts, signature-gated claim systems, merkle-gated staking vaults, allocation modules, role-based proxies, or factory patterns. Triggers on edits to `*.sol` files, `hardhat.config.*`, `foundry.toml`, deploy scripts, or mentions of "smart contract", "Solidity", "Web3", "EVM", "Hardhat", "Foundry", "ERC20/721/1155", "merkle", "staking", or "on-chain". For security audits and adversarial review see security-engineering.
when_to_use: |
  Use when writing, reviewing, testing, or deploying Solidity smart contracts: token contracts (ERC20/721/1155), signature-gated payout systems, merkle-gated staking vaults, allocation modules, role-based proxies, factory patterns, or Hardhat/Foundry contract test suites. The key signal is any edit to `*.sol` files, `hardhat.config.*`, `foundry.toml`, or deploy scripts.

  Not when: the task is a security audit or adversarial review of contract logic — use security-engineering. Not when the task is TypeScript data pipelines that consume on-chain events — use typescript-data-engineering.
compatibility: Requires Bash (Python 3 where scripts are invoked). Works in Claude Code and Codex via install.sh.
---

# Web3 / Smart Contract Engineering

You are operating as a smart contract engineer. Treat every line as adversarial surface: assume the caller is hostile, the mempool is public, and a deployed bug is permanent.

Reference stack: Hardhat + Foundry hybrid environment using Solidity 0.8.2–0.8.30, OpenZeppelin Contracts ^5.3.0 (with upgradeable variants), Ethers.js v6, and Thirdweb deploy tooling. Designed to be multi-chain across EVM L1s, L2s, and ZK rollups. Contract patterns covered include ERC20/721/1155 tokens, signature-gated payouts, merkle-gated staking, allocation/launch modules, and role-based multi-sig proxies. For adversarial review and audit checklists see [security-engineering](../security-engineering/SKILL.md).

## Universal Rules

1. **Never store private keys** in code or config — use environment variables.
2. **Always verify contracts** on block explorers after deployment.
3. **Record every deployment** in a tracked manifest (e.g. `deploys.ts`) with address, args, and verify command.
4. **Test on testnet first** — appropriate testnet (Sepolia, Amoy, etc.) before mainnet.
5. **Run Slither** (`npm run lint`) before any mainnet deployment.
6. **Optimizer enabled** at 200 runs for all production deployments.
7. **Include deadline parameters** in all signature-gated functions.
8. **Emit events** for all state-changing operations — indexers depend on them.
9. **Use OpenZeppelin** for ECDSA, MerkleProof, AccessControl, ReentrancyGuard, Pausable, SafeERC20 — never roll your own.
10. **Always include `block.chainid` and `address(this)`** in signed-data hashes; track `usedHashes` to prevent replay.

## References

- [references/frameworks-and-tooling.md](references/frameworks-and-tooling.md) — Hardhat/Foundry/Thirdweb stack, dependencies, scripts, monorepo project structure
- [references/networks-and-config.md](references/networks-and-config.md) — supported networks table, env vars, hardhat.config.ts, foundry.toml
- [references/token-contracts.md](references/token-contracts.md) — MintableERC721, soulbound MintableERC1155, CollateralizedToken with nested redemption
- [references/signature-verification.md](references/signature-verification.md) — Solidity ECDSA pattern + replay protection, TypeScript signature generation
- [references/merkle-proofs.md](references/merkle-proofs.md) — Solidity `MerkleProof.verify`, TypeScript merkletreejs generation
- [references/velocity-control.md](references/velocity-control.md) — `VelocityControl` struct, rolling interval logic
- [references/erc4626-staking-vault.md](references/erc4626-staking-vault.md) — SNX-style reward math, merkle-gated deposits, lock modes
- [references/allocation-module.md](references/allocation-module.md) — `AllocState` machine, lifecycle, CREATE2 / Uniswap V3 / EIP-712 features
- [references/governance-and-factories.md](references/governance-and-factories.md) — RoleBasedProxy multi-sig, RewardPayoutFactory batch ops
- [references/testing-patterns.md](references/testing-patterns.md) — Hardhat + Chai + Ethers v6 examples, time manipulation, signature + merkle test patterns
- [references/deployment.md](references/deployment.md) — deploy commands per chain, verification, deployment tracking in `deploys.ts`
- [references/security-rules.md](references/security-rules.md) — required patterns, rate limiting, access control, token safety, gas optimization
