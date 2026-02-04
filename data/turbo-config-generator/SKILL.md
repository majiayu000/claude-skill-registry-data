---
name: turbo-config-generator
description: Generate Turborepo configuration files for monorepo build orchestration. Triggers on "create turbo config", "generate turborepo configuration", "turbo setup", "monorepo build config".
---

# Turbo Config Generator

Generate Turborepo configuration for efficient monorepo build pipelines.

## Output Requirements

**File Output:** `turbo.json`
**Format:** Valid Turborepo configuration
**Standards:** Turborepo 1.x

## When Invoked

Immediately generate a complete Turborepo configuration with pipeline definitions.

## Example Invocations

**Prompt:** "Create turbo config for monorepo with build and test"
**Output:** Complete `turbo.json` with build, test, lint pipelines.
