---
name: vault-audit-repair
description: Use when a governed Obsidian vault may have drift, duplicates, missing registry state, missing metadata, orphan files, stale canonical notes, or unclear topic ownership. Applies to read-heavy inspection, repair planning, and controlled remediation.
---

# Vault Audit And Repair

## Overview

This skill checks whether the vault still matches its own governance model. It is for diagnosis first and repair second.

If your agent supports MCP, 优先 use the governance MCP server for structured findings, proposal, and review flows.
Use this skill as the compatibility layer when MCP is unavailable.

## Audit Targets

- missing or stale topic mapping
- orphan files
- duplicate topics
- notes without required metadata
- canonical notes updated outside the expected process
- registry and filesystem mismatch

## Audit Order

1. Read `RULES.md`
2. Read all registry files
3. Compare topic paths to real files
4. Inspect canonical drift
5. Inspect promotion queue backlog
6. Decide whether the fix is:
   - metadata-only
   - registry-only
   - proposal-based
   - coordinator-required

Read `references/audit-checklist.md` for the full checklist.

## Repair Rule

Prefer the smallest safe repair:

- fix registry before moving content
- fix topic identity before renaming folders
- use proposals when canonical content is involved

## Common Mistakes

- deleting files just because registry forgot them
- treating every mismatch as a content problem
- repairing canonical drift without recording it
