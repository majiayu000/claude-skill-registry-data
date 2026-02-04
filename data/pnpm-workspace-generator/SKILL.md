---
name: pnpm-workspace-generator
description: Generate pnpm workspace configuration files for monorepo package management. Triggers on "create pnpm workspace", "generate pnpm-workspace.yaml", "pnpm monorepo setup", "workspace config".
---

# PNPM Workspace Generator

Generate pnpm workspace configuration for monorepo package management.

## Output Requirements

**File Output:** `pnpm-workspace.yaml`
**Format:** Valid YAML
**Standards:** pnpm 8.x

## When Invoked

Immediately generate a complete pnpm workspace configuration file.

## Example Invocations

**Prompt:** "Create pnpm workspace for apps and packages"
**Output:** Complete `pnpm-workspace.yaml` with configured paths.
