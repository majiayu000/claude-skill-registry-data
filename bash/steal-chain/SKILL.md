---
name: steal-chain
description: >-
  Emperor Time index-finger chain — borrow other agents. CLI: local CLIs with
  interactive consent. CI: botified pool. Swarm-emulate when the host has no
  native swarm. Not the chain that captures public SKILL.md files (Chain Jail).
metadata:
  version: 0.3.6
  part-of: emperor-time
  kind: router
---

# Steal Chain — router

> *Pierce another's aura and their ability is yours to wield — for as long as
> the chain holds. It is still their Nen. Handle it accordingly.*

You are the master orchestrator. Enlisted agents are borrowed abilities.
Their output is CONJECTURE until Judgment quotes its own probes.

## Not this chain

Written skills from Superpowers or any public SKILL.md → Chain Jail
(`navigation.md` then `extract-aspect.md`). This chain only enlists *agents*.

## Selection — read exactly one

| Situation | Aspect |
|---|---|
| Headless / bot / pipeline | `ci-mode.md` |
| Host has no native swarm; tasks are disjoint | `swarm-emulate.md` |
| Roster exists — get client approval | `consent-protocol.md` |
| Approved agent needs auth | `sign-in-handoff.md` |
| Send work | `dispatch.md` |
| Agent returned output | `quarantine.md` |
| Which agent for which work | `routing.md` |

## Laws (every aspect)

1. No consent, no enlistment (CI consent is declared in env / repo file).
   Mechanical: `scripts/emperor consent --reject-no-consent` /
   `--check-consent` (HARD-GATE; G4 calls `consent.py`).
2. Credentials are radioactive. Sign-in / dispatch / swarm are mechanical:
   `scripts/emperor steal-flow --reject-no-signin` /
   `--reject-no-dispatch-layout` / `--reject-unbounded-swarm` /
   `--check-signin` / `--check-dispatch` / `--check-swarm` (HARD-GATE; G4
   calls `steal_flow.py`).
3. Everything returned is CONJECTURE.
4. Provenance or it didn't happen.
5. Never delegate Judgment.
