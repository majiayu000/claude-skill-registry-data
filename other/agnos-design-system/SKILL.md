---
name: agnos-design-system
description: "AGNOS process design-system skill. Provides the reusable design-system template (assets/design-system-template.md) and the procedure to instantiate it in a UI project, as required by MANDATORY DESIGN SYSTEM, before the first UI requirement is implemented. USE FOR: starting the design system of a project with a user interface; looking up the token-chain rules a UI change must follow."
argument-hint: "(no arguments)"
---

<!-- RQ-DSY-001 / ADR-DSY-001 (DEC-DSY-001) -->
# AGNOS Design System

## Template

`assets/design-system-template.md` (in this skill folder): framework-agnostic, written to be followed
literally by an agent. Its §0 "Agent Operating Rules" is the token-chain contract every UI change
SHALL follow. Never edit the template to fit one project: edit the project's instantiated copy.

## Procedure

1. Check `agnos-process/process.idx.md` and `agnos-process/1.requirements/` for an existing design-system
   feature. If one exists, use it and STOP: a project has a single design system.
2. Choose the design-system trigram `<TRI>` and the next free FTR/RQ/ADR IDs from the `#next` line
   of the index. If the trigram cannot be inferred, ask the user (process rule 4.a).
3. Copy the template to `agnos-process/1.requirements/FTR-<TRI>-<NNN>-design-system.md`, give it an
   `FTR-<TRI>-<NNN>` title and its requirement(s) `RQ-<TRI>-<NNN>`, then fill every `[...]`.
4. Write the design-system ADR in `agnos-process/2.architecture/` (token structure, tiers,
   generation/verification mechanism), referencing those RQ IDs.
5. Invoke the `agnos-index` skill so the new artifacts are indexed.
6. From then on, every UI requirement, ADR, task and code change SHALL reference these
   design-system IDs (MANDATORY DESIGN SYSTEM).
