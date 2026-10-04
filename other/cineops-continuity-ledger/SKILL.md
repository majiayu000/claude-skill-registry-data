---
name: cineops-continuity-ledger
description: Create and maintain canonical character, location, prop, and scene-state records; detect downstream impact when approved facts change. Use across episodes, revisions, shot handoffs, or generated clips where identity, geography, wardrobe, possession, damage, knowledge, or emotional state must remain consistent.
---

# CineOps Continuity Ledger

## Purpose

Maintain one explicit source of production truth without erasing uncertainty or history. Track state transitions at scene boundaries and identify work invalidated by revisions.

Read `references/ledger-contract.md`. Start from `assets/continuity-ledger.template.json`. Use the root `cineops` CLI for deterministic validation and impact reports.

## Build Or Update The Ledger

1. Identify the current authoritative sources and their approval status.
2. Assign stable IDs to characters, locations, and props. Never recycle an ID after deletion.
3. Record only facts supported by an approved source. Put alternatives under `proposals`; put unavailable facts under `unknowns`.
4. For every scene, record entry and exit state, involved entity IDs, and the source revision.
5. When facts conflict, preserve both citations, mark the conflict, and request a decision. Do not silently pick the newest file.
6. After a canon change, compare ledgers and review every affected scene and downstream shot.

## Validate

Run:

```bash
cineops validate path/to/project
cineops impact old-continuity-ledger.json new-continuity-ledger.json
```

Validation checks ID formats, duplicates, missing references, scene coverage, shot references, and readiness coverage. Impact analysis is conservative: a listed scene needs human review; omission does not prove safety when the source data is incomplete.

## State Categories

Track only categories relevant to continuity, such as position, facing, wardrobe, carried items, visible damage, knowledge, allegiance, emotional pressure, environment, time, and unresolved action. Prefer specific observable values over interpretation.

Bad: `Mara feels different.`

Good: `Mara avoids eye contact, keeps the access card hidden in her left sleeve, and now knows the lift is listening.`

## Exit Criteria

The ledger is usable when every referenced ID resolves, every planned scene has a state record or explicit exemption, conflicts have owners, and changed canon has an impact report. Return changed facts, affected artifacts, unresolved conflicts, and required re-approvals.
