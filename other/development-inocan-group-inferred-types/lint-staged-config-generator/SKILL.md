---
name: lint-staged-config-generator
description: Generate lint-staged configuration for running linters on staged Git files. Triggers on "create lint-staged config", "generate lint staged", "lint-staged setup", "staged file linting".
---

# Lint-Staged Config Generator

Generate lint-staged configuration for running linters only on staged Git files.

## Output Requirements

**File Output:** `.lintstagedrc.js`, `lint-staged.config.js`, or in `package.json`
**Format:** Valid lint-staged configuration
**Standards:** lint-staged 15.x

## When Invoked

Immediately generate a complete lint-staged configuration for the project's file types.

## Example Invocations

**Prompt:** "Create lint-staged config for TypeScript and CSS"
**Output:** Complete `.lintstagedrc.js` with ESLint, Prettier, and Stylelint.
