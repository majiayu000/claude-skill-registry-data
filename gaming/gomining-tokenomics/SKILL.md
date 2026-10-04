---
name: gomining-tokenomics
description: "GoMining Tokenomics skill covering the GMT token ecosystem: token locking (Lock), vote-escrowed tokens (veGOMINING), voting systems for reward distribution and re-minting coefficient, the Burn & Mint deflationary mechanism including epochs, post-mint distribution, token utility, and supply reduction from 500M to 100M tokens."
license: Apache-2.0
compatibility: "Compatible with Claude Code, Codex, and all Agent Skills spec tools."
metadata:
  author: gomining
  version: "1.0"
  tags:
    - gomining
    - tokenomics
    - gmt
    - locking
    - voting
    - burn-and-mint
    - veGOMINING
    - defi
  triggers:
    - "GMT token"
    - "token locking"
    - "veGOMINING"
    - "VE tokens"
    - "burn and mint"
    - "re-minting coefficient"
    - "voting reward distribution"
    - "token supply"
    - "tokenomics"
    - "locked tokens"
    - "mint distribution"
    - "token utility"
    - "epoch burn"
---

# GoMining Tokenomics

The Tokenomics module governs the GMT token ecosystem including token locking (Lock), voting (Voting), and the deflationary Burn & Mint mechanism.

## Overview

GoMining Tokenomics is built around three interconnected systems that work together to manage the GMT token supply, incentivize long-term holding, and enable community governance:

| System | Purpose | Key Mechanism |
|--------|---------|---------------|
| **Lock** | Incentivize long-term holding | Lock GMT to receive vote-escrowed (VE) tokens |
| **Voting** | Community governance | VE holders vote on reward distribution and burn rate |
| **Burn & Mint** | Deflationary supply management | Daily burns from user spending, controlled re-minting |

## Smart Contracts

- **GMT Contract**: Initial supply of 500M tokens, manages token issuance across the ecosystem.
- **VEGoMining (VE) Contracts**: Issue vote-escrowed tokens when users lock GMT. Voting power is proportional to VE token quantity.

## Long-term Goals

1. **Reduce total supply** from 500M to 100M tokens over time.
2. **Two vectors** to achieve this:
   - Gradual token reduction through systematic burns.
   - Increase token utility to drive demand and usage.

## Token Types

GoMining supports both on-chain token locking (via smart contracts) and a streamlined in-app locking flow for a faster user experience. Both methods maintain parity with the on-chain state.

## Token Utility

1. **Electricity discount** for mining operations.
2. **Game boosts** for enhanced gameplay rewards.
3. **Reinvestment** into hashrate for increased mining power.
4. **Voting and locked-token bonuses** for governance participants.

## Reference Files

| File | Contents |
|------|----------|
| [LOCK-AND-VOTE.md](references/LOCK-AND-VOTE.md) | Locking mechanism, veGOMINING tokens, voting systems |
| [BURN-AND-MINT.md](references/BURN-AND-MINT.md) | Burn/mint mechanics, epochs, post-mint distribution |

## References

- [FAQ: Tokenomics Overview](references/FAQ-OVERVIEW.md) — Overview of GoMining tokenomics mechanics
- [FAQ: Burn & Mint Cycles](references/FAQ-BURN-MINT.md) — How weekly burn and mint cycles work
- [FAQ: Epochs](references/FAQ-EPOCHS.md) — What epochs are and how they affect the mint coefficient
- [FAQ: veGOMINING and Locks](references/FAQ-VEGOMINING.md) — How to lock GOMINING tokens to receive veGOMINING votes
- [FAQ: Voting](references/FAQ-VOTING.md) — How veGOMINING holders participate in governance voting
