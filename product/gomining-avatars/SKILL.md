---
name: gomining-avatars
description: "GoMining avatar collections — cosmetic avatars assignable to Digital Miners. Covers the four avatar races (Humans, Sentinels, Cryptiles, Luminars), Luminar VIP level boost rules, secondary marketplace for miners and avatars, and branded merchandise."
license: Apache-2.0
compatibility: "Compatible with Claude Code, Codex, and all Agent Skills spec tools."
metadata:
  author: gomining
  version: "1.0"
  tags:
    - avatars
    - nft
    - marketplace
    - luminars
    - miner-wars
  triggers:
    - "avatar collection"
    - "luminars"
    - "luminar vip boost"
    - "nft marketplace"
    - "gomining merch"
    - "avatar races"
---

# GoMining Avatar Collections

## Overview

Avatars are cosmetic items that can be assigned to Digital Miners. There are four avatar races, each with unique visual styles. For information on Digital Miners themselves (blockchains, pricing, earning modes), see the [gomining-miners skill](../gomining-miners/SKILL.md).

---

## The Four Races

| # | Race | Collection URL | Special Feature |
|---|------|---------------|----------------|
| 1 | **Humans** | app.gomining.com/gominers-collection/humans | Standard collection |
| 2 | **Sentinels** | app.gomining.com/gominers-collection/sentinels | Standard collection |
| 3 | **Cryptiles** | app.gomining.com/gominers-collection/cryptiles | Standard collection |
| 4 | **Luminars** | app.gomining.com/gominers-collection/luminars | +1 VIP level when assigned (500+ TH users) |

---

## Luminar Avatar Rules

Luminars are the newest avatar race and provide a unique VIP tier boost.

| Rule | Description |
|------|-------------|
| **VIP Boost** | Assigning a Luminar avatar grants +1 VIP level immediately |
| **Eligibility** | User must have 500+ TH to benefit from the VIP boost |
| **Removal** | Removing the Luminar avatar immediately reverts the VIP level |
| **GoBox Reward** | A GoBox is issued once when the new VIP level is reached |
| **Re-assignment** | GoBox is **not** re-issued if the Luminar is removed and reassigned |
| **Bronze Protection** | Bronze GoBox is **not** issued to prevent farming exploits |

### Luminar VIP Boost Flow

1. User assigns a Luminar avatar to their miner.
2. If the user has 500+ TH, their VIP level increases by +1 immediately.
3. A GoBox corresponding to the new VIP level is issued (one-time).
4. If the user removes the Luminar avatar, VIP level reverts to the original.
5. Reassigning the same or different Luminar does **not** re-issue the GoBox for that level.
6. If the user is at Bronze tier, no GoBox is issued (anti-farming measure).

---

## Secondary Marketplace

The GoMining marketplace enables peer-to-peer trading of Digital Miners and avatars.

| Feature | Description |
|---------|-------------|
| **Miner Trading** | Buy and sell Digital Miners |
| **Avatar Trading** | Buy and sell avatars |
| **Listing** | Users set their own prices |
| **Settlement** | Transactions settled on-chain |
| **Supported Assets** | Digital Miners, Avatars (all four races) |

---

## Merchandise

GoMining offers physical branded merchandise available through the marketplace ecosystem.

| Category | Description |
|----------|-------------|
| **Branded Products** | Official GoMining-branded physical items |
| **Availability** | Through the GoMining marketplace |
| **Shipping** | Details available at time of purchase |

---

## FAQ

### How do Luminar avatars affect my VIP level?
Assigning a Luminar avatar gives an immediate +1 VIP level boost if you have 500+ TH. The boost is removed if you unassign the avatar.

### Will I get another GoBox if I reassign a Luminar?
No. The GoBox is issued once per VIP level achieved through Luminar assignment. Removing and reassigning does not re-issue the GoBox.

### Can I trade my avatar on the marketplace?
Yes, all four avatar races (Humans, Sentinels, Cryptiles, Luminars) can be traded on the secondary marketplace.

### What is GoMining merch?
GoMining offers physical branded products that can be purchased through the marketplace ecosystem.

---

## References

- [Avatar Collections](references/AVATAR-COLLECTIONS.md) — Race details and collection URLs
- [Marketplace](references/MARKETPLACE.md) — Trading mechanics for miners and avatars
- [FAQ: Collections Overview](references/FAQ-COLLECTIONS.md) — Overview of GoMiner collections
- [FAQ: GoMiners Avatars](references/FAQ-AVATARS.md) — Avatars, races, and how to use them
- [FAQ: Main Collections](references/FAQ-MAIN-COLLECTIONS.md) — Details on the main GoMiners collections
