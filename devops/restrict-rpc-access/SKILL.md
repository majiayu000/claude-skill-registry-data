---
name: restrict-rpc-access
description: Use when the agent needs to restrict reads on a private Avalanche L1 — limiting RPC endpoints, validator-only access, and building a true walled garden so only authorized participants can query the chain.
category: Avalanche L1
difficulty: Advanced
version: "0.1.0"
---

# Restrict RPC Access (the read-side of access privacy)

## Overview
Allowlist precompiles gate **writes** (txs, deploys). To make an L1 truly **private** you must also gate **reads** — i.e. restrict the **RPC endpoints** so only authorized participants can query state. This is the "walled garden" half of access privacy ([[private-permissioned-l1s]]).

## Layers of read restriction
1. **Don't expose public RPC.** Run validators/nodes on a private network (VPC/VPN); do not publish a public RPC URL or list it on chain explorers.
2. **Validator-only / private nodes.** Keep RPC bound to internal interfaces; provide RPC only to authorized API nodes behind authentication.
3. **Network/auth layer.** Put RPC behind a reverse proxy/gateway requiring API keys, mTLS, or VPN. The chain protocol doesn't authenticate RPC callers — your infra does.
4. **Node config.** Configure the avalanchego/Subnet-EVM node's HTTP/API settings (enabled APIs, host binding, allowed origins) to minimize the surface. Per-L1 chain configs live under the node's chain-config directory.

## Combine for full privacy
| Goal | Mechanism |
|---|---|
| Who can read | **Restricted RPC** (this skill) + private networking |
| Who can transact | Transaction AllowList ([[l1-transaction-allowlist]]) |
| Who can deploy | Deployer AllowList ([[l1-deployer-allowlist]]) |
| Who can validate | ValidatorManager / PoA ([[poa-validator-manager]]) |
| Data confidentiality | eERC on top ([[combining-eerc-with-private-l1]]) |

## Operational notes
- Treat RPC like any sensitive API: authenticate, rate-limit, log, and monitor.
- For consortiums, give each member their own credentialed RPC gateway rather than a shared public endpoint.
- Even with restricted RPC, on-chain data is plaintext to anyone who *does* have access — add eERC if members shouldn't see each other's amounts.

## Common Pitfalls
- **Allowlists without RPC restriction.** A common mistake — writes are gated but anyone can still read all state. Not private.
- **Public explorer indexing.** If you ever expose RPC publicly, indexers may cache your data permanently.
- **Assuming the protocol authenticates RPC.** It doesn't; access control is an infrastructure responsibility.

## AI Agent Prompt
> "Act as an infrastructure engineer. Design a private Avalanche L1 where only consortium members can reach the RPC: private networking, authenticated RPC gateways, hardened node API config, plus tx/deployer allowlists and a PoA validator set."

## References
See `references/README.md` (academy permissioned-l1s 'Private L1s', builders-hub node chain-configs, access-restriction course).
