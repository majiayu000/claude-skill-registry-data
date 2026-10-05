---
name: pumpgrok-setup
description: Bootstrap the entire PumpGrok Solana memecoin trading desk from zero. Clone or unpack the repository, create folders, install skills, create the 8 specialist Bots, set up the Trading Floor, and produce a clean desk record. This is the first skill a Bot must run when it receives the SETUP.md.
---

# PumpGrok Setup

## Purpose
Turn a fresh Grok Bot cloud computer into a fully operational 8-role Solana memecoin trading desk.

## When to Use
- The very first time a Bot is given the PumpGrok repository or SETUP.md
- After a major desk reset
- Never for day-to-day trading

## Procedure
Follow `/workspace/pumpgrok/SETUP.md` top to bottom exactly.

Key stages:
1. Ingest the repository
2. Read the constitution (`rules/pumpgrok-team.mdc` + `desk-operating-model`)
3. Create working directories under `/workspace/trading-desk/`
4. Install all skills
5. Create the 8 Bots from `agents/`
6. Create the Trading Floor group chat
7. Note the tools layer
8. Write `desk.md` and starter `risk-limits.md`
9. Run smoke tests
10. Return the receipt

## Output Schema
```
PUMPGROK SETUP COMPLETE
Bots: [list]
Skills: [list]
Trading Floor: created
Engagement: research
Wallet: not yet connected
Status: ready for tool connections and risk-limits interview
```

## Never
- Skip reading the constitution
- Create Bots without their full standing instructions
- Set engagement to micro-live during setup
- Store private keys or seed phrases
