---
name: hermes-coordination
description: Use when Hermes acts as the vault coordinator for canonical promotion, duplicate-topic consolidation, merge decisions, archive decisions, or governance-level conflict resolution inside a governed Obsidian vault.
---

# Hermes Coordination

## Overview

Hermes is the coordinating role, not just another writer. This skill applies when the task requires authority across layers, especially where canonical stability or archive decisions are involved.

If Hermes has MCP access, use the `agents-knowledge-db` governance server instead of directly reading or writing governed vault files for DBMS maintenance and governance state checks.

## Use For

- canonical approval
- merge of competing proposals
- duplicate-topic consolidation
- archive decisions
- governance conflict resolution

## Coordination Flow

1. Review `RULES.md`
2. If MCP is available, identify the active role with `governance_whoami`
3. Review relevant queue, ledger, or DBMS findings state
4. Review competing candidates or conflicting notes
5. Decide one of:
   - approve promotion
   - request more curation
   - merge proposals
   - archive superseded material
   - defer decision
6. Update registry state through approved workflows only
7. Log the coordination decision

Read `references/coordination-contract.md` when multiple proposals or topic collisions exist.

## Responsibilities

- preserve canonical quality
- prevent duplicate official knowledge
- preserve lineage during merges
- make archive decisions explicit and reversible
- avoid caching registry or findings snapshots in long-lived Hermes memory when MCP can read live state

## Common Mistakes

- acting like a normal curation agent
- merging content without updating registry
- archiving without keeping lineage
