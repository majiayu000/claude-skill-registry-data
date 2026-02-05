---
name: postcss-config-builder
description: Generate PostCSS configuration files with plugins for CSS processing, autoprefixing, and optimizations. Triggers on "create postcss config", "generate postcss configuration", "postcss setup", "css processing config".
---

# PostCSS Config Builder

Generate PostCSS configuration files with appropriate plugins for CSS processing.

## Output Requirements

**File Output:** `postcss.config.js` or `postcss.config.cjs`
**Format:** Valid PostCSS configuration
**Standards:** PostCSS 8.x

## When Invoked

Immediately generate a complete PostCSS configuration with plugins for the project needs.

## Configuration Template

```javascript
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
```

## Example Invocations

**Prompt:** "Create postcss config for Tailwind with autoprefixer"
**Output:** Complete `postcss.config.js` with Tailwind and autoprefixer.
