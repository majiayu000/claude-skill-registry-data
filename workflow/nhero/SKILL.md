---
name: nhero
description: Aftermarket cybernetic network device framework. nhero is the umbrella for all pill-dispenser-as-network-device modifications — from Hero Health hardware RE to PyHole DNS-style medication routing to killdispenser supply chain primitives. One lowercase word. Append-only reference architecture.
version: 0.1.0
trit: -1
color: "#E59798"
tags: [nhero, aftermarket, cybernetic, dispenser, pyhole, killdispenser, aptos, hamming]
---

# nhero

Aftermarket cybernetic network device. One lowercase word.

nhero treats every pill dispenser as a network device. The same way Pi-hole intercepts DNS queries and decides what passes through, nhero intercepts medication scheduling commands and routes them through a scrambled, GF(3)-conserved, confidential-asset-backed supply chain.

## Hierarchy

```
nhero/                          ← umbrella (this skill)
├── killdispenser/              ← fundamental primitive: the piehole in every device
├── hero-dispenser-mod/         ← Hero Health Model 100 specific implementation
├── nhero-pyhole/               ← DNS-style medication routing layer
├── nhero-scramble/             ← derangement-based name scrambling
├── nhero-confidential/         ← Twisted ElGamal supply tracking on Aptos
└── nhero-nurse/                ← nurse approval email automation
```

## Concepts

### killdispenser
The fundamental piehole in every device. Like `kill(1)` sends signals to processes, killdispenser sends signals to dispensing slots. Like Pi-hole blocks DNS, killdispenser blocks unauthorized dispense events. Every nhero device has a killdispenser — it's the control plane.

### PyHole Model
Pi-hole blocks ads at DNS level. nhero blocks/routes medications at schedule level:
- **Blocklist** = controlled substances requiring nurse approval
- **Allowlist** = OTC supplements (Magnesium, Zinc, Ginkgo, Caffeine)
- **Upstream** = Hero cloud API (intercepted via mitmproxy)
- **Local DNS** = scramble index (letter → medication lookup)

### Scramble Index (Derangement)
No medication maps to its own initial letter. Full derangement:

| Slot | Medication | GF(3) |
|------|-----------|-------|
| q | Vyvanse | -1 |
| x | Magnesium | 0 |
| y | Zinc | +1 |
| k | Ginkgo | -1 |
| u | Caffeine | 0 |

Conservation: Q(-1) + X(0) + Y(+1) + K(-1) + U(0) = **-1** = H world trit

### Confidential Assets (Huber-Duncan)
`0x7::confidential_asset` on Aptos testnet:
- Twisted ElGamal encrypts supply counts
- ZK range proofs verify `remaining > threshold` without revealing count
- Nurse holds auditor key, never sees medication names or exact counts
- Each dispense = confidential withdraw of 1

## Topos-MCP Server
9 tools as morphisms in the category of dispenser states.
Registered as `hero-topos` MCP server (stdio JSON-RPC).

## Hardware Target
- **Hero Model 100** (FCC ID: 2AN4DM115, OEM: Xiamen Zayata Technology)
- PCB revisions: ZA-D102LCD_V2.1 (UI), 1027306-V46 (logic), ZA-1200DCM/2.0 (USB)
- OMRON G5V-1 relay, WiFi 2.4GHz, PCB trace antenna at ANT1
- Test points TP1-TP4 on USB daughter board (likely UART)

## World
- Letter: H (index 7, GF(3) -1, Chain 1 Witness-Bridge)
- Email: `mantissa+hero-h@plurigrid.com`
- Nurse: `mantissa@gmail.com` / `ies@plurigrid.com`
