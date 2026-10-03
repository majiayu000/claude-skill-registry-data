---
name: implement-save-system
description: "Use when you need a save/load system with schema versioning, dual-format serialization, and migration logic for game state persistence."
---

## 1. Overview
Generates save/load architecture: schema definition, dual-format serialization, sequential migration, high-integrity load with corruption detection.

**Scenarios**: Persistent game state with schema versioning, ECS/State Machine entity state → long-term storage.

## 2. Core Pattern

1. **Environment & Spec Analysis**: Analyze config + `state_machine_spec.md` + `ecs_spec.md` for serialization requirements.
2. **Schema Design**: Top-level `SaveData` with explicit `CURRENT_SCHEMA_VERSION`.
3. **Serialization**: Dual-format (JSON for debug, Binary/MessagePack for production) with optional field handling.
4. **Migration Framework**: Version-dispatching with discrete sequential migration functions (e.g., `migrateV1toV2`).
5. **Resilient API**: `Save`/`Load` functions with multi-stage validation + specific error types (`CorruptedSaveError`).

## 3. Interaction Protocol
- **[Breaking Change]**: Field deleted without default → "Breaking change: removing [Field]. Data loss for existing players. Implement migration rule or proceed?"
- **[Schema Ambiguity]**: Version change unclear → "v[N]→v[N+1] ambiguous: [Field] renamed or type-converted? Clarify for correct migration."

**Guiding Principle**: Schema evolution is first-class. Every change MUST have a defined, tested migration path.

## 4. Quality Gates - STOP
- **Backward Compatibility**: Every field deletion includes default value or migration rule to prevent data loss
- **Clear Evolution**: Define version transformations explicitly (rename vs type change)
- **Complete Validation**: Apply multi-stage validation with checksums and integrity checks on load path

## 5. Final Integrity Audit
- [ ] `CURRENT_SCHEMA_VERSION` matches all migration paths
- [ ] Every schema mod has default value or migration rule
- [ ] Both JSON and Binary/MessagePack formats functional with optional data
- [ ] `CorruptedSaveError` triggered correctly on failed loads
