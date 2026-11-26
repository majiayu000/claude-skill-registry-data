---
name: cf-onchain
category: research
description: When the user asks to analyze blockchain transactions, trace wallet activity, decode contract interactions, or explain token movements — activate this skill for onchain transaction analysis
---

# Onchain Transaction Analyzer

Analyzes blockchain transactions by tracing wallets, contracts, and token movements and providing simple, understandable explanations.

## Activation

- User says "trace this transaction", "what happened in this tx", "analyze this wallet"
- User provides transaction hash, wallet address, or contract interaction
- User needs plain-language explanation of onchain activity

## Process

### 1. Trace Flows
- Identify sender, receiver, intermediary contracts
- Map token movements (amounts, types, directions)

### 2. Identify Actors
- Label known contracts (DEX, bridge, lending protocol)
- Note wallet patterns (whale, bot, new wallet)

### 3. Explain
- Step-by-step narrative of what happened
- Highlight notable actions (large transfers, swaps, approvals)

## Output

- Step-by-step transaction explanation in plain language
- Key actors and their roles
- Token flow summary (what moved, where, how much)
- Risk flags if applicable (suspicious patterns)
