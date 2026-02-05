---
name: rollup-config-generator
description: Generate Rollup configuration files for bundling JavaScript libraries. Triggers on "create rollup config", "generate rollup configuration", "rollup setup", "library bundler config".
---

# Rollup Config Generator

Generate Rollup configuration files for efficient library bundling.

## Output Requirements

**File Output:** `rollup.config.js` or `rollup.config.mjs`
**Format:** Valid Rollup configuration
**Standards:** Rollup 4.x

## When Invoked

Immediately generate a complete Rollup configuration with plugins for bundling libraries.

## Example Invocations

**Prompt:** "Create rollup config for TypeScript library"
**Output:** Complete `rollup.config.mjs` with ESM and CJS outputs.
