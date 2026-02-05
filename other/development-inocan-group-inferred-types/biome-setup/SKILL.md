---
name: biome-setup
description: Biome linter/formatter setup. Use when configuring Biome as an alternative to ESLint + Prettier.
---

# Biome Setup Skill

This skill covers Biome configuration for TypeScript projects as an alternative to ESLint + Prettier.

## When to Use

Use this skill when:
- Setting up a new project with modern tooling
- Replacing ESLint + Prettier with a single tool
- Need faster linting and formatting
- Want simpler configuration

## Core Principle

**ONE TOOL, ZERO DEPENDENCIES** - Biome replaces both ESLint and Prettier with 10-100x better performance.

## Installation

```bash
npm install -D @biomejs/biome
```

## Basic Configuration

### biome.json

```json
{
  "$schema": "https://biomejs.dev/schemas/1.9.0/schema.json",
  "organizeImports": {
    "enabled": true
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "suspicious": {
        "noExplicitAny": "error",
        "noImplicitAnyLet": "error"
      },
      "correctness": {
        "noUnusedVariables": "error",
        "noUnusedImports": "error"
      },
      "style": {
        "noNonNullAssertion": "warn",
        "useConst": "error",
        "useTemplate": "error"
      },
      "complexity": {
        "noBannedTypes": "error",
        "noUselessTypeConstraint": "error"
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
      "semicolons": "always",
      "quoteStyle": "single",
      "trailingCommas": "all",
      "arrowParentheses": "always"
    }
  },
  "files": {
    "ignore": ["node_modules", "dist", "coverage"]
  }
}
```

## Package.json Scripts

```json
{
  "scripts": {
    "lint": "biome check .",
    "lint:fix": "biome check --write .",
    "format": "biome format --write .",
    "format:check": "biome format ."
  }
}
```

## Key Rules

### Type Safety Rules

```json
{
  "linter": {
    "rules": {
      "suspicious": {
        "noExplicitAny": "error",
        "noImplicitAnyLet": "error",
        "noConfusingVoidType": "error",
        "noAsyncPromiseExecutor": "error"
      }
    }
  }
}
```

**noExplicitAny:**
```typescript
// ❌ Error
function process(data: any) { }

// ✅ OK
function process(data: unknown) { }
```

**noImplicitAnyLet:**
```typescript
// ❌ Error
let value;  // implicit any

// ✅ OK
let value: string;
let value: unknown;
```

### Code Quality Rules

```json
{
  "linter": {
    "rules": {
      "correctness": {
        "noUnusedVariables": "error",
        "noUnusedImports": "error",
        "noConstantCondition": "error",
        "noUndeclaredVariables": "error"
      }
    }
  }
}
```

### Style Rules

```json
{
  "linter": {
    "rules": {
      "style": {
        "useConst": "error",
        "useTemplate": "error",
        "noVar": "error",
        "useShorthandFunctionType": "error",
        "useExportType": "error",
        "useImportType": "error"
      }
    }
  }
}
```

**useExportType / useImportType:**
```typescript
// ❌ Error - using value import for type
import { User } from './types';
export { User };

// ✅ OK - type-only imports/exports
import type { User } from './types';
export type { User };
```

## Formatter Configuration

### JavaScript/TypeScript Formatting

```json
{
  "javascript": {
    "formatter": {
      "semicolons": "always",
      "quoteStyle": "single",
      "jsxQuoteStyle": "double",
      "trailingCommas": "all",
      "arrowParentheses": "always",
      "bracketSpacing": true,
      "bracketSameLine": false
    }
  }
}
```

### JSON Formatting

```json
{
  "json": {
    "formatter": {
      "trailingCommas": "none"
    }
  }
}
```

## File-Specific Overrides

```json
{
  "overrides": [
    {
      "include": ["**/*.test.ts", "**/*.test.tsx"],
      "linter": {
        "rules": {
          "suspicious": {
            "noExplicitAny": "off"
          }
        }
      }
    },
    {
      "include": ["*.config.js", "*.config.ts"],
      "linter": {
        "rules": {
          "style": {
            "noDefaultExport": "off"
          }
        }
      }
    }
  ]
}
```

## VS Code Integration

### Install Extension

Install "Biome" extension from VS Code marketplace.

### settings.json

```json
{
  "editor.defaultFormatter": "biomejs.biome",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "quickfix.biome": "explicit",
    "source.organizeImports.biome": "explicit"
  },
  "[javascript]": {
    "editor.defaultFormatter": "biomejs.biome"
  },
  "[typescript]": {
    "editor.defaultFormatter": "biomejs.biome"
  },
  "[json]": {
    "editor.defaultFormatter": "biomejs.biome"
  }
}
```

## CLI Commands

### Linting

```bash
# Check all files
biome check .

# Check and fix
biome check --write .

# Check specific files
biome check src/

# Check with specific rules
biome check --diagnostic-level=error .
```

### Formatting

```bash
# Check formatting
biome format .

# Apply formatting
biome format --write .

# Format specific files
biome format --write src/**/*.ts
```

### CI Integration

```bash
# Check only (exit non-zero on issues)
biome ci .
```

## Migration from ESLint + Prettier

### Step 1: Install Biome

```bash
npm uninstall eslint prettier eslint-config-prettier @typescript-eslint/eslint-plugin @typescript-eslint/parser
npm install -D @biomejs/biome
```

### Step 2: Create biome.json

```bash
npx biome init
```

### Step 3: Update Scripts

```json
{
  "scripts": {
    "lint": "biome check .",
    "format": "biome format --write ."
  }
}
```

### Step 4: Remove Old Config Files

```bash
rm .eslintrc.json .eslintrc.js .prettierrc .prettierignore
```

### Rule Mapping

| ESLint Rule | Biome Rule |
|-------------|------------|
| `@typescript-eslint/no-explicit-any` | `suspicious/noExplicitAny` |
| `@typescript-eslint/no-unused-vars` | `correctness/noUnusedVariables` |
| `no-var` | `style/noVar` |
| `prefer-const` | `style/useConst` |
| `prefer-template` | `style/useTemplate` |

## Limitations

Biome does not support:
- Custom rules (plugin ecosystem)
- Some ESLint-specific rules
- JSON configuration with comments

Use ESLint if you need:
- eslint-plugin-react-hooks
- eslint-plugin-jsx-a11y
- Custom rule development

## Pre-commit Hook

```json
{
  "lint-staged": {
    "*.{ts,tsx,js,jsx,json,md}": [
      "biome check --write --no-errors-on-unmatched"
    ]
  }
}
```

## GitHub Actions

```yaml
name: Lint

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
      - run: npm ci
      - run: npx biome ci .
```

## Best Practices Summary

1. **Use `biome ci` in CI pipelines**
2. **Enable organizeImports**
3. **Set noExplicitAny to error**
4. **Use overrides for test files**
5. **Configure VS Code for format on save**
6. **Use lint-staged for pre-commit**

## Code Review Checklist

- [ ] biome.json present in project root
- [ ] noExplicitAny set to error
- [ ] noUnusedVariables enabled
- [ ] Formatter configured consistently
- [ ] VS Code extension installed
- [ ] Pre-commit hook configured
- [ ] CI uses `biome ci`
