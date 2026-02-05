---
name: babel-config-builder
description: Generate Babel configuration files for JavaScript/TypeScript transpilation with presets and plugins. Triggers on "create babel config", "generate babel configuration", "babel setup", "transpilation config".
---

# Babel Config Builder

Generate Babel configuration files for JavaScript transpilation with appropriate presets and plugins.

## Output Requirements

**File Output:** `babel.config.js`, `babel.config.json`, or `.babelrc`
**Format:** Valid Babel 7 configuration
**Standards:** Babel 7.x

## When Invoked

Immediately generate a complete Babel configuration with presets for the target environment and necessary plugins.

## Configuration Template

```javascript
module.exports = {
  presets: [
    ['@babel/preset-env', { targets: { node: 'current' } }],
    '@babel/preset-typescript',
    ['@babel/preset-react', { runtime: 'automatic' }],
  ],
  plugins: [
    '@babel/plugin-transform-runtime',
  ],
};
```

## Example Invocations

**Prompt:** "Create babel config for React TypeScript"
**Output:** Complete `babel.config.js` with React, TypeScript presets.
