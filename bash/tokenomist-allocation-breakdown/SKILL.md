---
name: tokenomist-allocation-breakdown
description: Get the full allocation distribution for a token — who owns what and how much is locked vs unlocked. Use when analyzing supply distribution across team, investors, community, etc.
metadata:
  openclaw:
    requires:
      env:
        - TOKENOMIST_API_KEY
      bins:
        - tok
    primaryEnv: TOKENOMIST_API_KEY
    install:
      - kind: node
        package: "@tokenomist-ai/tokenomist-cli"
        bins: [tok]
allowed-tools: Bash(tok:*)
---

# Skill: Allocation Breakdown

Get the full allocation distribution for a token — who owns what and how much is locked vs unlocked.

## When to use

When you need to understand a token's supply distribution across allocations (team, investors, community, ecosystem, etc.).

## Command

```bash
tok allocation detail <tokenId> --output json
```

## Example

```bash
tok allocation detail solana --output json
```

## Key output fields

**Top-level:**
- `name`, `symbol` — token identification
- `maxSupply` — maximum token supply (null if unlimited)
- `totalUnlockedAmount` — total tokens currently unlocked
- `totalLockedAmount` — total tokens still locked
- `totalUntrackedAmount` — tokens not tracked by Tokenomist
- `totalTBDLockedAmount` — tokens locked with no defined unlock schedule

**Per allocation (`allocations[]`):**
- `allocationName` — project-specific allocation name
- `standardAllocationName` — Tokenomist's standardized category (comparable across projects)
- `allocationType` — allocation classification
- `allocationAmount` — total tokens in this allocation
- `allocationUnlockedAmount` — tokens unlocked from this allocation
- `allocationLockedAmount` — tokens still locked in this allocation
- `trackedAllocationPercentage` — % of total tracked supply

## Analysis workflow

1. Get allocation: `tok allocation detail <id> --output json`
2. Check `totalLockedAmount` vs `totalUnlockedAmount` for overall supply status
3. Look at individual allocations — high locked amounts in "Investor" or "Team" allocations signal future sell pressure
4. Compare `standardAllocationName` across different tokens for apples-to-apples comparison
5. Cross-reference with `tok unlock upcoming` to see when locked tokens will release

## Domain Context

- Allocations are **point-in-time analyses**. They reflect the current understanding of token distribution and may be updated as new information becomes available.
- `standardAllocationName` enables cross-project comparison — different projects may use different names for similar allocations (e.g., "Core Contributors" vs "Team"), but the standard name normalizes this.
- `totalTBDLockedAmount` represents tokens that are known to be locked but have no defined unlock schedule. Their classification may change as the project releases more information.

## Workflow

- Use allocation data as context for unlock analysis — understanding allocations helps interpret **who** is receiving unlocked tokens and why it matters.
- Chain with `tok fundraising detail <id>` to see investor-specific allocation details and funding round information.
- Compare `allocationLockedAmount` vs `allocationUnlockedAmount` per allocation to identify which groups still have significant locked positions.
