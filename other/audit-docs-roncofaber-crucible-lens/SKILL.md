---
name: audit-docs
description: Audit AGENTS.md, README.md, project skills, and dev documentation against the repository, then repair factual drift and unnecessary duplication. Use only when explicitly asked to audit, refresh, migrate, or verify project documentation.
---

# Audit project documentation

## Scope

Review `AGENTS.md`, `README.md`, `agent-skills/`, and `dev/*.md`. Include tool-specific adapter files only when their integration changed.

## Method

1. Identify claims that name symbols, files, routes, parameters, versions, counts, or mechanisms.
2. Verify each claim against source or build configuration with `rg` and direct file inspection.
3. Recompute stated counts rather than copying them from another document.
4. Confirm described workflows and state machines still have an implementation.
5. Repair the document that owns the fact instead of duplicating details into multiple files.

Enumerative content drifts fastest. Prefer durable rules and links to the owning deep reference over repeated inventories. Keep useful rationale, but remove history and procedural narration that does not change the action an agent should take.

Do not accept another document, prior agent report, or memory as evidence. Reopen the implementation before writing a correction, then reread the corrected passage against the source.

## Finish

- Check for stale references with `rg`.
- Run the skill validator on every changed skill.
- Run `git diff --check`.
- Run `./scripts/verify-change.sh` as a build-safety check.
- Do not add a changelog entry for documentation-only changes.
- Report verified drift and any remaining uncertainty without repeating the entire document map.
