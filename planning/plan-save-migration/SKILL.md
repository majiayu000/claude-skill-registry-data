---
name: plan-save-migration
description: "Use when planning save file schema migration between game versions. Triggers: 'save migration', 'save file version', 'schema change', 'save compatibility', 'save format'."
---

# plan-save-migration - Skill Definition

## 1. Overview
Generates robust, backward-compatible migration paths for save file schema changes. This skill compares old and new schemas, defines atomic transformation rules, and maps the full migration chain from all supported versions to the current version. The output is a safety-planned `save_migration.md` with backup strategies and fallback defaults.

## 2. When to Use

Use when:
- You're releasing a new version with schema changes (added/removed/renamed fields, type conversions).
- Existing players have save files that must remain loadable after the update.
- You need migration rules, a compatibility matrix, and backup/fallback strategies documented.

Do not use when:
- This is the first version of the save system — there's nothing to migrate from.
- The schema hasn't changed between versions.

## 3. Triggers & Red Flags
* **Triggers**: `save migration`, `save file version`, `schema change`, `save compatibility`, `save system update`, `save format`.
* **Red Flags**:
    * **Breaking Change Detected**: Deleting a critical field without providing a default value or mapping it to a new structure (potential permanent data loss).
    * **Ambiguous Type Conversion**: Changing types where implicit conversion is risky (e.g., Float to Int) without defining rounding/truncation rules.
    * **Orphaned Data Structures**: Removing complex nested objects that are still referenced by other systems in the game loop.

## 3. Interaction Protocol
* **Communication Style**: Precise, cautious, and safety-oriented; focus heavily on risk assessment of schema changes and impact on existing player data.
* **Phase 1: Discovery & Diffing** — Compare old (N) and new (N+1) schemas to identify all changes: Added, Removed, Renamed, Type Changed, or Restructured.
* **Phase 2: Rule Generation** — For every change, define an atomic rule with clear transformation logic (e.g., `M_001: Rename hp -> health`).
* **Phase 3: Compatibility Matrix** — Map the full migration path chain required to move from all supported versions up to the current version. Every path step must be independently testable.
* **Phase 4: Safety Planning** — Define backup strategies (`.bak` files), checksum verification, and fallback/default values for missing data.
* **Phase 5: Specification Export** — Write the finalized plan into `{TARGET_FOLDER}/docs/save_migration.md`.

## 4. Intercepts & Guards
* **[Breaking Change Intercept]**: If a change is inherently non-backward compatible (e.g., deleting a field without a default): *"I notice a breaking change in the schema (removal of [Field]). This will cause data loss for existing players. Should we implement a migration rule to preserve this data or proceed with removal?"*
* **[Schema Ambiguity Intercept]**: If version differences are unclear: *"The change from v[N] to v[N+1] is ambiguous. Is [Field] being renamed, or is it a type conversion? Please clarify."*

## 5. Strategic Imperative
**Prioritize backward compatibility above all else.** Every schema change MUST have a defined, tested migration path from previous versions to prevent catastrophic player progress loss.
