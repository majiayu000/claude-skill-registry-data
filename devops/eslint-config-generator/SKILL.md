---
name: eslint-config-generator
description: Generate ESLint configuration files (.eslintrc.js, eslint.config.js) for JavaScript/TypeScript projects with framework-specific rules. Triggers on "create ESLint config", "generate eslint configuration", "eslint setup for", "linting rules for".
---

# ESLint Config Generator

Generate production-ready ESLint configuration files with appropriate rules, plugins, and extends for various JavaScript/TypeScript projects.

## Output Requirements

**File Output:** `.eslintrc.js`, `.eslintrc.json`, or `eslint.config.js`
**Format:** Valid ESLint configuration
**Standards:** ESLint 8.x / 9.x (flat config)

## When Invoked

Immediately generate a complete ESLint configuration file with appropriate plugins, extends, and rules for the specified project type.

## Configuration Templates

### Modern Flat Config (ESLint 9.x)
```javascript
// eslint.config.js
import js from '@eslint/js';
import typescript from '@typescript-eslint/eslint-plugin';
import typescriptParser from '@typescript-eslint/parser';

export default [
  js.configs.recommended,
  {
    files: ['**/*.{ts,tsx}'],
    languageOptions: {
      parser: typescriptParser,
      parserOptions: {
        ecmaVersion: 'latest',
        sourceType: 'module',
        project: './tsconfig.json',
      },
    },
    plugins: {
      '@typescript-eslint': typescript,
    },
    rules: {
      '@typescript-eslint/no-unused-vars': 'error',
      '@typescript-eslint/no-explicit-any': 'warn',
    },
  },
];
```

### Legacy Config
```javascript
// .eslintrc.js
module.exports = {
  root: true,
  env: { node: true, es2022: true },
  parser: '@typescript-eslint/parser',
  plugins: ['@typescript-eslint'],
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
  ],
};
```

## Example Invocations

**Prompt:** "Create ESLint config for React TypeScript"
**Output:** Complete `.eslintrc.js` with React, TypeScript, and hooks rules.
