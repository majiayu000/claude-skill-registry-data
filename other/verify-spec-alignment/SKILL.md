---
name: verify-spec-alignment
description: "Use when cross-checking spec consistency between user layer and core layer, or when upstream rules changed but downstream specs may not have updated."
---

# verify-spec-alignment - Skill Definition

## 1. Overview

Cross-checks consistency between user-layer and core-layer specifications, flagging semantic drift and naming mismatches before they cause implementation failures. Core principle: flag drift immediately — it is the single biggest failure mode in two-tier architectures.

## 2. When to Use

Use when:
- Upstream specs changed and you suspect downstream specs haven't been updated.
- Before implementation begins on a multi-tier architecture and you want to catch semantic drift.
- Naming mismatches or inconsistent terminology appear across spec layers.

Do not use when:
- Only one spec layer exists — this skill requires at least two layers to cross-check.
- Specs are still being drafted and aren't stable enough for comparison.

## 3. Triggers & Red Flags

* **Triggers**: `verify-spec-alignment`, `verify alignment`, `spec consistency`, `check cross-spec`, `drift check`, `spec alignment`, `cross-spec check`.
* **Red Flags**:
    * **Semantic Consistency**: Upstream rules and downstream implementation specs use identical terminology and logic.
    * **Structural Completeness**: Every required system component defined in the high-level roster appears in low-level ECS/Component definitions.
    * **Naming Uniformity**: Identical concepts use identical names across layers to prevent coding errors.

## 3. Core Pattern

1. **Change Detection** — Read all relevant spec files to identify which files are present and have content updates.
2. **Semantic Cross-Checking** — Execute a structured cross-check matrix:
    * **A: `003` <-> `101`**: Rule triggers vs. Event names/payloads.
    * **B: `004` <-> `104`**: P0 systems vs. ECS archetypes/systems.
    * **C: `101` <-> `102`**: Event names vs. State machine triggers.
    * **D: `101` <-> `103`**: Event names/subscribers vs. BT actions/conditions.
    * **E: `003` <-> `104`**: Entity types in rules vs. ECS archetypes.
3. **Severity Categorization** — Classify findings into **ERROR** (blocks implementation), **WARNING** (potential drift), or **INFO** (minor mismatch).
4. **Report Generation** — Output findings clearly, grouped by severity.
5. **Final Checklist** — Use `todowrite` to create a summary checklist reflecting the audit results for each spec file.

## 4. Intercepts & Guards

* **[Silent Drift Intercept]**: If the user assumes alignment but a mismatch is found: *"I notice a discrepancy between [Upstream Spec] and [Downstream Spec]. This drift could cause implementation failure. Should we regenerate the downstream spec or adjust the upstream rule?"*
* **[Ambiguous Match Intercept]**: If semantic matching is uncertain: *"I found a potential mismatch between [A] and [B], but the naming is too similar to be certain. Should I treat this as a match or a warning?"*

## 5. Strategic Imperative

**Flag drift immediately.** Semantic drift is the single biggest failure mode in two-tier architectures. Do not be apologetic about finding errors; your role is to protect system integrity through uncompromising vigilance.
