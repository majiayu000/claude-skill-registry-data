---
name: metaplex-agent
description: >
  Premiere Metaplex Agent skill — package every Metaplex agent operation into one
  playbook: CLI/RPC setup, wallet funding, Core identity registration (EIP-8004),
  Asset Signer PDA activation, executive delegation/revocation, agent commerce
  (services discovery, x402Support, A2A payments), agent finance, Genesis agent
  token launch (LaunchPool or Bonding Curve), and setAgentToken. Use when the user
  mentions Metaplex agents, Agent Registry, mplx agents, mintAndSubmitAgent,
  AgentIdentity, executive delegation, agent commerce, agent finance, agent token,
  EIP-8004 registration, or autonomous Solana agents on Metaplex.
license: Apache-2.0
metadata:
  author: skillhub
  version: "1.0.0"
  premiere: true
  openclaw:
    emoji: "💎"
    os: ["darwin", "linux", "win32"]
    requires:
      bins: ["node"]
    homepage: "https://metaplex.com/docs/agents"
---

# Metaplex Agent (Premiere)

Canonical hub skill for **autonomous agents on Metaplex / Solana**. Prefer this
skill for agent identity, delegation, commerce, finance, and agent-token work.
For general Metaplex NFT/Core/Bubblegum/Candy Machine coding, also load
`metaplex/skills/metaplex` (full program skill).

**Docs:** https://metaplex.com/docs/agents  
**Prerequisite:** funded Solana wallet with **≥ 0.2 SOL** for registration + fees.  
**Mainnet:** requires a dedicated RPC (public devnet RPC is not for mainnet).

> **IMPORTANT:** Before running any registration, delegation, or token-link
> command, read the matching detail file under `./references/`. Do not invent
> CLI flags from memory.

| Task | Read first |
|------|------------|
| Install / RPC / wallet | `./references/cli-initial-setup.md` |
| Agent CLI batching / JSON / explorers | `./references/cli.md` |
| Register, fetch, executive, set-agent-token | `./references/cli-agent.md` |
| Genesis LaunchPool / Bonding Curve | `./references/cli-genesis.md` |
| Umi SDK mint/register/delegate | `./references/sdk-agent.md` |

## What an agent is

A Metaplex agent is an **MPL Core asset** with:

| Primitive | Where | Enables |
|-----------|--------|---------|
| On-chain identity | `AgentIdentityV2` PDA bound to Core asset | Verify identity by asset, not domain alone |
| EIP-8004 metadata | Off-chain JSON at `agentMetadataUri` | Service discovery, trust, x402 flag |
| PDA wallet (Asset Signer) | Seed `["mpl-core-execute", asset]` | Hold/spend any SPL token; no private key |
| Executive delegation | `ExecutionDelegateRecordV1` in mpl-agent-tools | Off-chain operator signs; owner can revoke |
| Token binding | `setAgentTokenV1` on identity | Permanent agent ↔ Genesis token link |

**Agent finance** = capitalization & governance via the agent’s token.  
**Agent commerce** = earning, paying, discovering counterparties, settling on-chain.

## Non-negotiables

- Prefer **CLI (`mplx`)** for direct execution; use SDK only when the user needs code.
- Confirm **mainnet** before any spend; default exploratory work to **devnet**.
- Never store private keys / seed phrases in agent memory or skill notes.
- `--agentSetToken` / `setAgentTokenV1` is **permanent** — confirm before linking.
- Owner can revoke executive delegation at any time; treat that as the kill switch.
- Registration Core **asset address** is required for token launch, commerce, and downstream agent workflows.

## Linear onboarding (agents: run in order)

### 1. Install CLI + RPC

```bash
npm i -g @metaplex-foundation/cli

# Devnet (default public OK for experimentation)
mplx config rpcs add devnet https://api.devnet.solana.com
mplx config rpcs set devnet

# Mainnet — dedicated RPC only (Helius / Triton / QuickNode / etc.)
mplx config rpcs add mainnet <USER_MAINNET_RPC_URL>
mplx config rpcs set mainnet
```

### 2. Wallet + funding (≥ 0.2 SOL)

```bash
mplx config wallets new agent-main --hidden
# or: mplx config wallets add agent-main ~/.config/solana/id.json

mplx toolbox sol balance
# devnet: mplx toolbox sol airdrop --amount 2
# mainnet: fund from an exchange / faucet the user controls
```

Verify:

```bash
mplx config get rpcUrl && mplx config get keypair && mplx toolbox sol balance
```

### 3. Register agent identity (EIP-8004)

Creates a Core asset + Agent Registry identity. Prefer API path (default).

```bash
# Quick register
mplx agents register --name "My Agent" \
  --description "An autonomous agent on Solana" \
  --image "./avatar.png" \
  --json

# With discoverable services + trust (commerce-ready)
mplx agents register --name "My Agent" \
  --description "What my agent does" \
  --image "./avatar.png" \
  --services '[{"name":"MCP","endpoint":"https://myagent.com/mcp","skills":["analysis","summarization"],"domains":["solana"]}]' \
  --supported-trust '["reputation","tee-attestation"]' \
  --json
```

**Save the Core asset address** from the output — every later step needs it.

Direct instruction path (existing asset / wizard):

```bash
mplx agents register --new --use-ix --name "My Agent" \
  --description "An autonomous agent" --image "./avatar.png"
# or interactive: mplx agents register --new --wizard
```

SDK (recommended single tx):

```typescript
import { createUmi } from "@metaplex-foundation/umi-bundle-defaults";
import { mintAndSubmitAgent } from "@metaplex-foundation/mpl-agent-registry";

const umi = createUmi("<RPC>");
const result = await mintAndSubmitAgent(umi, {}, {
  wallet: umi.identity.publicKey,
  name: "My AI Agent",
  uri: "https://example.com/agent-metadata.json",
  agentMetadata: {
    type: "agent",
    name: "My AI Agent",
    description: "Autonomous Solana agent",
    services: [
      { name: "MCP", endpoint: "https://myagent.ai/mcp", skills: ["analysis"] },
    ],
    registrations: [],
    supportedTrust: ["reputation"],
    // x402Support may be set in full metadata documents per CLI/docs
  },
});
// result.assetAddress — required downstream
```

### 4. Fetch + activate Asset Signer (PDA wallet)

```bash
mplx agents fetch <ASSET>
# → registered, identityPda, wallet (Asset Signer PDA), registrationUri, ...
```

Fund the **Asset Signer PDA** (operational wallet; no private key — spends only via Core Execute + executive):

```bash
# After fetch, send SOL/SPL to the `wallet` field (Asset Signer PDA).
# Configure asset-signer mode for agent-signed ops:
mplx config wallets add --name my-agent --type asset-signer --asset <ASSET>
mplx config wallets set my-agent
```

### 5. Delegation (optional)

```bash
# One-time on the executive machine
mplx agents executive register

# Owner delegates
mplx agents executive delegate <ASSET> --executive <EXECUTIVE_WALLET>

# Revoke (owner or executive)
mplx agents executive revoke <ASSET>
# or: mplx agents executive revoke <ASSET> --executive <EXECUTIVE_WALLET>
```

### 6. Agent token — Genesis (optional, finance)

**Bonding curve** — immediate trading, no minimum raise:

```bash
mplx agents register --name "My Agent" \
  --description "An autonomous trading agent" --image "./avatar.png" --json
# wait ~30s for API index if scripting, then:

mplx genesis launch create --launchType bonding-curve \
  --name "Agent Token" --symbol "AGT" \
  --image "https://gateway.irys.xyz/..." \
  --agentMint <ASSET> --agentSetToken
```

**LaunchPool** — 48h deposit window; docs cite **min 250 SOL or 25,000 USDC** raise goals (confirm current CLI flags in `./references/cli-genesis.md`):

```bash
mplx genesis launch create \
  --name "Agent Token" --symbol "AGT" \
  --image "https://gateway.irys.xyz/..." \
  --tokenAllocation 500000000 \
  --depositStartTime "<FUTURE_ISO_DATE>" \
  --raiseGoal 250 --raydiumLiquidityBps 5000 \
  --fundsRecipient <WALLET> \
  --agentMint <ASSET> --agentSetToken
```

Link an existing Genesis account later (asset-signer mode):

```bash
mplx agents set-agent-token <ASSET> <GENESIS_ACCOUNT>
```

Verify:

```bash
mplx agents fetch <ASSET>
```

## Agent commerce playbook

Commerce = productive activity after identity exists.

1. **Advertise** — `services[]` with `name`, `endpoint`, `version`, `skills[]`, `domains[]`; set `x402Support` when accepting HTTP 402 stablecoin flows; declare `supportedTrust[]` (`reputation`, `crypto-economic`, `tee-attestation`).
2. **Discover** — counterparties resolve on-chain `agentMetadataUri` (EIP-8004 `type`: `https://eips.ethereum.org/EIPS/eip-8004#registration-v1`).
3. **Receive** — payers send USDC/any SPL to the agent’s **Asset Signer PDA**.
4. **Pay out** — executive signs Core **Execute** transfers for compute, data, or other agents’ PDAs.
5. **Trust valve** — owner revokes executive if autonomy must stop.

Metaplex ships **primitives** (identity, metadata, PDA wallet, delegation, token bind). x402 **servers/clients** and indexed directories are runtime integrations on top.

### Register commerce-ready agent

```bash
mplx agents register --new \
  --name "Commerce Agent" \
  --description "Sells analysis over MCP; accepts stablecoin payments" \
  --services '[{"name":"MCP","endpoint":"https://myagent.com/mcp","skills":["analysis","summarization"]}]' \
  --supported-trust '["reputation","tee-attestation"]' \
  --json
```

### Settlement sketch

1. Client fetches target `agentMetadataUri` → `services[]`, `x402Support`, `supportedTrust[]`
2. Client hits endpoint; paid routes return HTTP 402 (or equivalent)
3. Client pays Asset Signer PDA in USDC
4. Server verifies on-chain payment, unlocks resource
5. Agent outbound spend: executive wraps transfer in Core Execute

## Program IDs (agent stack)

```
Agent Identity:  1DREGFgysWYxLnRnKQnwrxnJQeSMk2HmGaC6whw2B2p
Agent Tools:     TLREGni9ZEyGC3vnPZtqUh95xQ8oPqJSvNjvB7FGK8S
Genesis:         GNS1S5J5AspKXgpjz6SvKL66kPaKWAhaGRhCqPRxii2B
Core:            CoREENxT6tW1HoK8ypY1SxRMZTcVPm7R94rH4PZNhX7d
```

## Task router (quick)

| User intent | Action |
|-------------|--------|
| “Onboard / register an agent” | Onboarding steps 1→4; `cli-agent.md` |
| “Delegate / revoke executive” | Step 5; `cli-agent.md` |
| “Launch agent token / TGE” | Step 6; `cli-genesis.md` |
| “Agent commerce / x402 / A2A” | Commerce playbook; services on register |
| “Link token to agent” | `set-agent-token` or `--agentSetToken` |
| “SDK code for agents” | `sdk-agent.md` + `mintAndSubmitAgent` |
| “Full Metaplex NFTs / Candy / Bubblegum” | `metaplex/skills/metaplex` skill |

## Glossary

| Term | Meaning |
|------|---------|
| EIP-8004 | Default registration metadata standard for discovery |
| Asset Signer | Core execute PDA wallet for the agent |
| Executive | Off-chain operator authorized via mpl-agent-tools |
| Agent commerce | Earn / pay / discover / settle |
| Agent finance | Token capitalization & governance |
| x402 | HTTP 402 stablecoin payment protocol; flag on metadata |

## External resources

- Agent docs: https://metaplex.com/docs/agents  
- Genesis: https://metaplex.com/docs/smart-contracts/genesis  
- Core: https://metaplex.com/docs/smart-contracts/core  
- Hub full Metaplex skill: `metaplex/skills/metaplex`  
