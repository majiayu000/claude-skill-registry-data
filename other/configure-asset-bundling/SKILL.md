---
name: configure-asset-bundling
description: "Use when defining asset streaming strategies (AOT vs DLC/Addressables) to optimize package size and load priority tiers."
---

# configure-asset-bundling

## 1. Overview

Defines asset streaming strategies (AOT vs DLC/Remote Loading) that minimize initial package size while ensuring seamless content availability during gameplay. Produces `bundle_strategy.md` with bundle group definitions, dependency DAGs, load priority tiers, and platform compliance validation.

## 2. When to Use

- **Scenarios**: Defining asset bundle groups, optimizing initial download size, planning DLC or on-demand content delivery.
- **Triggers**: `asset bundles`, `DLC`, `asset streaming`, `package size`, `content delivery`, `dynamic loading`, `addressables`.

## 3. Core Pattern

1. **Load Priority Categorization**: Classify assets into priority tiers: **AOT** (Embedded), **Initial Download**, **Stream On Demand**, or **Background Download**.
2. **Bundle Group Definition**: Group related assets into logical bundles, specifying size targets and dependency requirements using `{TARGET_FOLDER}/docs/asset_budget.md` as a baseline.
3. **Dependency Graph Construction**: Build a Directed Acyclic Graph (DAG) of bundle dependencies to ensure correct loading order.
4. **DAG Validation**: Perform critical checks for Cycle Detection (via topological sort), Orphan Check (every asset assigned once), Size Constraints, and Platform Compliance.
5. **Specification Export**: Write the finalized bundle strategy to `{TARGET_FOLDER}/docs/bundle_strategy.md`.

## 4. Interaction Protocol

### Error Handling & Intercepts

- **[Circular Dependency Intercept]**: If a cycle is detected in the dependency graph: *"I've detected a circular dependency between [Bundle A], [Bundle B], and [Bundle C]. This will break the loading sequence. Should we reassign one of these to a higher-level bundle or remove the dependency?"*
- **[Orphan Asset Intercept]**: If assets are unassigned: *"I've found {N} assets that are not assigned to any bundle. Every asset must belong to exactly one group to be included in the build. How should these be categorized?"*

## 5. Red Flags

- **Acyclic Dependencies**: Maintain cycle-free bundle dependency DAG for correct loading sequences.
- **Complete Asset Assignment**: Assign every asset to exactly one logical bundle group.
- **Size-Constrained Bundles**: Keep bundles within specified target sizes and general constraints (1 MB - 500 MB range).
- **Platform-Compliant Sizes**: Stay within platform limits for total package/download sizes (Mobile ≤ 2 GB, PC ≤ 5 GB).
- **Unique Asset Placement**: Place each asset in only one bundle to avoid build conflicts.
