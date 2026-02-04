---
name: js-quality
description: Interpretive guidance for JavaScript/TypeScript code quality using biome (modern) or eslint+prettier (traditional). Use when linting JS/TS files, configuring JS/TS tools, troubleshooting lint errors, or understanding tool selection.
---

# JavaScript/TypeScript Quality Skill

This skill teaches how to apply JavaScript and TypeScript linting and formatting tools effectively using mr-sparkle's tool selection system. It provides guidance on what the tools do, when each tool group is used, and how our configuration balances modern unified tooling with traditional setups.

## Official Documentation

Claude knows how to use biome, eslint, and prettier. Fetch these docs only when you need:

- Specific rule codes or error messages you don't recognize
- Advanced configuration options
- Recent feature changes

**Reference URLs:**

- **<https://biomejs.dev/linter/>** - Biome linting rules and configuration
- **<https://eslint.org/docs/latest/>** - ESLint configuration and rules
- **<https://prettier.io/docs/en/>** - Prettier formatting options

## Core Understanding

### Tool Selection Philosophy

**Key principle:** Prefer modern unified tooling (biome) when project has it configured; fall back to traditional tools (eslint+prettier) when they're configured; default to biome if no configuration exists.

**What this means:**

- **Biome preferred** - Single tool for linting + formatting, extremely fast (Rust-based)
- **Project config wins** - Respects existing project tooling choices
- **Smart fallback** - Uses traditional tools if project has them configured
- **Zero-config default** - Falls back to biome with sensible defaults

**Decision test:** Does the project have explicit tool configuration? Use configured tools. Otherwise use biome.

### How Tool Selection Works

The linting system uses **group-based priority selection** for JS/TS files:

```text
Priority 1: biome (if project has biome config)
    ↓
Priority 2: eslint + prettier (if project has their configs)
    ↓
Fallback: biome (with default config)
```

**Detection logic:**

1. Find project root (`package.json`, `pyproject.toml`, or `.git`)
2. Check for biome configuration (first group)
3. Check for eslint/prettier configuration (second group)
4. If no config found, use biome with `default-biome.json`

**All tools in winning group run sequentially** (e.g., if eslint config exists, runs eslint → prettier).

## Biome: Modern Unified Tool (Official Specification)

**From official docs:**

- **Purpose:** Fast unified toolchain for JavaScript/TypeScript written in Rust
- **Capabilities:** Linting + formatting in a single tool
- **Replaces:** ESLint + Prettier + parts of TypeScript compiler
- **Performance:** 10-100x faster than ESLint
- **Commands:** `biome check --fix` (linting + formatting in one pass)

**Configuration locations:**

- `biome.json` or `biome.jsonc` (dedicated config)

## Biome: Modern Unified Tool (Best Practices)

**When biome shines:**

- ✅ New projects (no legacy tooling)
- ✅ Large codebases (speed matters)
- ✅ Want single tool instead of chain
- ✅ TypeScript projects (built-in TS support)

**Basic configuration pattern:**

```json
{
  "$schema": "https://biomejs.dev/schemas/2.0.0/schema.json",
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true
    }
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "single",
      "semicolons": "asNeeded"
    }
  }
}
```

**Key configuration areas:**

- `linter.rules` - Enable/disable rule groups (recommended, suspicious, complexity, etc.)
- `formatter` - Global formatting options (indents, line width)
- `javascript.formatter` - JS-specific formatting (quotes, semicolons)
- `typescript` - TypeScript-specific options

See `biome-reference.md` for common rule categories and `default-biome.json` for our opinionated defaults.

## Traditional Tools: eslint + prettier (Official Specification)

**From official docs:**

**ESLint:**

- Pluggable JavaScript linter
- Finds and fixes problems in JavaScript/TypeScript code
- Highly configurable with extensive plugin ecosystem
- Command: `eslint --fix <file>`

**Prettier:**

- Opinionated code formatter
- Enforces consistent style across codebase
- Supports multiple languages beyond JS/TS
- Command: `prettier --write <file>`

**Configuration locations:**

**ESLint (modern flat config - recommended):**

- `eslint.config.js` (or `.mjs`, `.cjs`)
- Uses JavaScript export instead of JSON

**ESLint (legacy):**

- `.eslintrc` (or `.eslintrc.js`, `.eslintrc.json`, `.eslintrc.yaml`)

**Prettier:**

- `.prettierrc` (or `.prettierrc.js`, `.prettierrc.json`, `.prettierrc.yaml`)
- `prettier.config.js` (or `.cjs`, `.mjs`)

## Traditional Tools (Best Practices)

**When traditional tools make sense:**

- ✅ Existing projects with established configs
- ✅ Need specific ESLint plugins (React, Vue, etc.)
- ✅ Team familiarity with ESLint ecosystem
- ✅ Projects that haven't migrated to biome yet

**Running order matters:**

1. **eslint** - Linting with auto-fix (modifies code)
2. **prettier** - Formatting (modifies code)

**Why this order:** ESLint fixes code issues first, then Prettier formats the result.

**Critical:** ESLint and Prettier must be configured to work together:

- Use `eslint-config-prettier` to disable conflicting ESLint formatting rules
- Let Prettier handle formatting, ESLint handle code quality

## Tool Selection in Practice (Best Practices)

### Scenario 1: New project, no config

```bash
$ lint.py file.js
# Runs: biome check --fix
# Uses: default-biome.json from skill directory
```

### Scenario 2: Project with biome config

```bash
# Project has biome.json
$ lint.py file.ts
# Runs: biome check --fix
# Uses: project's biome.json config
```

### Scenario 3: Project with traditional tools

```bash
# Project has .eslintrc.json or .prettierrc
$ lint.py file.jsx
# Runs: eslint --fix, prettier --write
# Uses: project's existing configs
```

### Scenario 4: Mixed config (biome wins)

```bash
# Project has both biome.json and .eslintrc
$ lint.py file.ts
# Runs: biome only (first group with config wins)
```

## Common Configuration Patterns

### Biome Configuration

**Minimal (uses defaults):**

```json
{
  "$schema": "https://biomejs.dev/schemas/2.0.0/schema.json",
  "linter": {
    "enabled": true
  },
  "formatter": {
    "enabled": true
  }
}
```

**Typical project:**

```json
{
  "$schema": "https://biomejs.dev/schemas/2.0.0/schema.json",
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "suspicious": {
        "noExplicitAny": "warn"
      }
    }
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "single",
      "semicolons": "asNeeded"
    }
  }
}
```

**See `default-biome.json`** for our opinionated baseline configuration.

### ESLint Configuration (Modern Flat Config)

**Minimal:**

```javascript
// eslint.config.js
export default [
  {
    rules: {
      "no-unused-vars": "warn",
      "no-console": "off"
    }
  }
];
```

**With TypeScript:**

```javascript
// eslint.config.js
import js from "@eslint/js";
import tseslint from "typescript-eslint";

export default [
  js.configs.recommended,
  ...tseslint.configs.recommended,
  {
    rules: {
      "@typescript-eslint/no-explicit-any": "warn"
    }
  }
];
```

**See `default-eslint.config.js`** for a complete example with Prettier integration.

### Prettier Configuration

**Minimal:**

```json
{
  "semi": true,
  "singleQuote": true,
  "printWidth": 100
}
```

**Comprehensive:**

```json
{
  "semi": true,
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2,
  "trailingComma": "es5",
  "arrowParens": "avoid"
}
```

**See `default-prettier.json`** for our opinionated defaults.

## Common Pitfalls

### Pitfall #1: ESLint and Prettier Conflicts

**Problem:** ESLint formatting rules conflict with Prettier.

```javascript
// ❌ ESLint config with formatting rules
{
  "rules": {
    "max-len": ["error", { "code": 80 }],
    "quotes": ["error", "single"],
    "indent": ["error", 2]
  }
}
```

**Why it fails:** ESLint and Prettier fight over formatting, causing inconsistent results.

**Better:**

```javascript
// ✅ Use eslint-config-prettier to disable conflicts
import js from "@eslint/js";
import prettier from "eslint-config-prettier";

export default [
  js.configs.recommended,
  prettier, // Disables conflicting ESLint rules
  {
    rules: {
      // Only code quality rules, no formatting
      "no-unused-vars": "warn"
    }
  }
];
```

### Pitfall #2: Mixing Legacy and Flat ESLint Config

**Problem:** Project has both `.eslintrc.json` and `eslint.config.js`.

**Why it fails:** ESLint 9+ uses flat config by default, ignores legacy `.eslintrc.*` files unless explicitly configured.

**Better:** Choose one format:

- **New projects:** Use `eslint.config.js` (flat config)
- **Existing projects:** Migrate to flat config or stick with `.eslintrc.*`
- **Don't mix both**

### Pitfall #3: Not Installing Required Packages

**Problem:** Config references plugins not in `package.json`.

```javascript
// ❌ Using plugin that's not installed
import react from "eslint-plugin-react"; // Error if not installed
```

**Why it fails:** Linting fails with module not found errors.

**Better:**

```bash
# Install required plugins
npm install --save-dev eslint-plugin-react
```

```javascript
// ✅ Now it works
import react from "eslint-plugin-react";
```

### Pitfall #4: Over-Configuring Biome

**Problem:** Trying to replicate entire ESLint plugin ecosystem in Biome.

**Why it fails:** Biome doesn't support all ESLint plugins. Start simple, add rules incrementally.

**Better:**

```json
{
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true
    }
  }
}
```

Then add specific rules as needed, or stick with ESLint if you need specific plugins.

### Pitfall #5: Ignoring Auto-Fixable Issues

**Problem:** Manually fixing issues that tools can fix automatically.

**Why it fails:** Wastes time, may introduce inconsistencies.

**Better:** Let `biome check --fix` or `eslint --fix` + `prettier --write` handle formatting. Focus on logic errors and design issues.

## Automatic Hook Behavior

The mr-sparkle plugin's linting hook:

1. Triggers after Write and Edit operations
2. Detects JS/TS files (`.js`, `.jsx`, `.ts`, `.tsx`, `.mjs`, `.cjs`)
3. Runs selected tools automatically (biome OR eslint+prettier)
4. Applies auto-fixes where possible
5. Reports unfixable issues (non-blocking)
6. Silently skips if tools not installed

**What this means:** Most formatting issues auto-fix on save. Pay attention to reported unfixable issues.

## Quality Checklist

**Before finalizing JavaScript/TypeScript code:**

**Auto-fixable (tools handle):**

- ✓ Import sorting and organization
- ✓ Quote style consistency
- ✓ Semicolon usage
- ✓ Indentation and line length
- ✓ Trailing whitespace
- ✓ Basic syntax issues

**Manual attention required:**

- ✓ Undefined variables
- ✓ Logic errors
- ✓ Type safety (TypeScript)
- ✓ Complexity warnings
- ✓ Security issues (e.g., eval usage)
- ✓ Performance anti-patterns

## CLI Tool Usage

The universal linting script handles JS/TS files automatically:

```bash
# Lint JavaScript file (applies fixes)
./plugins/mr-sparkle/skills/linting/scripts/lint.py file.js

# Lint TypeScript file
./plugins/mr-sparkle/skills/linting/scripts/lint.py file.ts

# JSON output for programmatic use
./plugins/mr-sparkle/skills/linting/scripts/lint.py file.jsx --format json
```

**Exit codes:**

- `0` - Clean or successfully fixed
- `1` - Lint errors found (non-blocking)
- `2` - Tool execution error

See `linting` skill for complete CLI documentation.

## Reference Documentation

**Detailed guides** (loaded on-demand for progressive disclosure):

- `biome-reference.md` - Biome rule categories and common configurations
- `eslint-reference.md` - ESLint configuration patterns and flat config migration
- `prettier-reference.md` - Prettier philosophy and configuration options
- `default-biome.json` - Our opinionated biome defaults
- `default-eslint.config.js` - Modern flat config example with Prettier integration
- `default-prettier.json` - Our opinionated prettier defaults

**Official documentation to fetch:**

- <https://biomejs.dev/> - Biome documentation and rule reference
- <https://eslint.org/docs/latest/> - ESLint documentation
- <https://typescript-eslint.io/> - TypeScript ESLint plugin
- <https://prettier.io/docs/en/> - Prettier formatter documentation

**Remember:** This skill documents mr-sparkle's tool selection logic for JS/TS. Fetch official docs when you need specific rule definitions or configuration syntax you're unsure about.
