---
name: renovate-config-generator
description: Generate Renovate configuration for automated dependency updates. Triggers on "create renovate config", "generate renovate configuration", "renovate setup", "dependency updates config".
---

# Renovate Config Generator

Generate Renovate configuration for automated dependency update management.

## Output Requirements

**File Output:** `renovate.json` or `.renovaterc.json`
**Format:** Valid Renovate configuration
**Standards:** Renovate best practices

## When Invoked

Immediately generate a complete Renovate configuration with appropriate update rules.

## Example Invocations

**Prompt:** "Create renovate config with automerge for minor updates"
**Output:** Complete `renovate.json` with automerge and grouping rules.
