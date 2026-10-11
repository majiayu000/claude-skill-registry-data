---
name: repo-scan
description: Cross-stack codebase audit that classifies every file as project code, third-party, or build artifact, detects embedded libraries and duplication, and assigns Core-Asset, Extract-Merge, Rebuild, or Deprecate verdicts. Use before major refactors or when asked what is dead weight.
metadata:
  origin: community-ecc-adapted
---

# Repo Scan

> How much code is actually yours, what's third-party, and what's dead weight.

## When to Use

- Taking over a large codebase and need a structural overview
- Before major refactoring — identify what's core, what's duplicate, what's dead
- Auditing third-party dependencies embedded directly in source (not declared in package managers)
- Preparing architecture decision records for monorepo reorganization

## How It Works

1. **Classify the surface**: enumerate files, tag each as project code, embedded third-party code, or build artifact.
2. **Detect embedded libraries**: inspect directory names, headers, license files, and version markers to identify bundled dependencies and likely versions.
3. **Score each module**: group files by module or subsystem, assign one of the four verdicts based on ownership, duplication, and maintenance cost.
4. **Highlight structural risks**: dead-weight artifacts, duplicated wrappers, outdated vendored code, modules to extract, rebuild, or deprecate.
5. **Produce the report**: concise summary plus per-module drill-down.

## Four-Level Verdicts

| Verdict | Meaning |
|---|---|
| Core Asset | Proprietary, maintained, keep |
| Extract & Merge | Duplicated across modules — consolidate |
| Rebuild | Outdated or broken — rewrite against current spec |
| Deprecate | Dead or superseded — delete |

## Analysis Depth Levels

| Level | Files Read | Use Case |
|---|---|---|
| `fast` | 1-2 per module | Quick inventory of huge directories |
| `standard` | 2-5 per module | Default audit with full dependency + architecture checks |
| `deep` | 5-10 per module | Adds thread safety, memory management, API consistency |
| `full` | All files | Pre-merge comprehensive review |

## Best Practices

- Start with `standard` depth for first-time audits.
- Use `fast` for monorepos with 100+ modules to get a quick inventory.
- Run `deep` incrementally on modules flagged for refactoring.
- Review the cross-module analysis for duplicate detection across sub-projects.
- Never trust lint or test output as proof of cleanliness — read the lines.
