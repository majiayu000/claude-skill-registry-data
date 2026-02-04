---
name: prettier-config-generator
description: Generate Prettier configuration files for consistent code formatting across JavaScript, TypeScript, CSS, and other file types. Triggers on "create prettier config", "generate prettier configuration", "prettier setup", "code formatting config".
---

# Prettier Config Generator

Generate Prettier configuration files for consistent code formatting.

## Output Requirements

**File Output:** `.prettierrc`, `.prettierrc.js`, or `prettier.config.js`
**Format:** Valid Prettier configuration
**Standards:** Prettier 3.x

## When Invoked

Immediately generate a complete Prettier configuration with formatting rules for the project type.

## Configuration Template

```json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100,
  "bracketSpacing": true,
  "arrowParens": "avoid"
}
```

## Example Invocations

**Prompt:** "Create prettier config for TypeScript project"
**Output:** Complete `.prettierrc` with TypeScript-friendly settings.
