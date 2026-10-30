---
name: spark-agent-knowledge
description: Use when Spark engineering knowledge must be placed, deduplicated, migrated, or validated across AGENTS, Notes, Roles, Skills, and Workflows.
---

# Spark agent knowledge

Apply one home per fact and progressive disclosure.

## Classification

Use [agent knowledge instructions](../../AGENTS.md) for asset ownership and
loading rules, and `CONTRIBUTING.md` for public documentation ownership.

## Procedure

1. Locate the enforced or runtime owner of each fact and existing copies.
2. Classify each fact before editing; link to the authoritative home instead of restating details.
3. Keep Role bodies free of methods owned by Skills. Keep Workflows free of specialist implementation instructions.
4. Update all active inbound links atomically and leave archived public docs unchanged unless explicitly requested.
5. Run the repository agent-knowledge and documentation checks that apply.

Preserve the runtime-context and public-documentation boundaries. Reconcile stale prose with verified enforced contracts; escalate a conflict only when resolving it requires a product or authority decision. Return `classification`, `authoritativeHomes`, `moves`, `linksUpdated`, `validation`, and `blockers`.
