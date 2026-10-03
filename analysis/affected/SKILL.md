---
name: affected
description: Analyze which monorepo packages and apps are affected by current changes
type: analysis
version: v0.1
---

# Affected

Invoke as `$affected`.

Use this skill when the user wants to understand the blast radius of their current changes in a monorepo.

## Process

1. Determine the change set from git diff or a specified commit range.
2. Read the monorepo config to understand the package graph.
3. Map changed files to their packages.
4. Compute transitive dependents.
5. Check for cross-cutting changes (root configs, shared packages).
6. Recommend test commands for affected packages.

## Output

- **Directly Changed**: packages with file changes
- **Transitively Affected**: downstream dependents
- **Cross-Cutting**: root config changes affecting all packages
- **Recommended Test Commands**: specific commands to run

## Constraints

- Do not run tests — only analyze and recommend.
- Prefer Turbo-native filtering for Turborepo projects.


## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
