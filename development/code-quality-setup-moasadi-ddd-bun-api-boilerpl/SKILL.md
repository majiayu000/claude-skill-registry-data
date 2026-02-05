---
name: code-quality-setup
description: Setup ESLint with Airbnb TypeScript config and Prettier formatter for code quality enforcement. Use when setting up new project, adding linting/formatting, or configuring code quality tools (e.g., "Setup ESLint and Prettier", "Configure code quality", "Add Airbnb linter").
allowed-tools: Read, Write, Edit, Glob, Bash
---

# Code Quality Setup Skill

Configures ESLint with Airbnb TypeScript style guide and Prettier formatter for automated code quality enforcement.

## What This Skill Does

Sets up complete code quality tooling:

- **ESLint**: JavaScript/TypeScript linter with Airbnb style guide
- **Prettier**: Opinionated code formatter
- **Integration**: ESLint + Prettier working together without conflicts
- **Scripts**: npm/bun scripts for linting and formatting
- **Git Hooks**: Optional pre-commit hooks for automatic checks
- **VS Code**: Editor integration settings

## When to Use This Skill

Use when you need to:
- Set up linting and formatting for new project
- Add Airbnb style guide to existing project
- Configure ESLint + Prettier integration
- Update code quality configuration
- Add editor integration

Examples:
- "Setup ESLint and Prettier with Airbnb style guide"
- "Configure code quality tools"
- "Add linting to the project"

## Tech Stack Requirements

**Required:**
- Node.js or Bun.js runtime
- TypeScript project
- package.json file

**This Skill Installs:**
- eslint
- @typescript-eslint/parser
- @typescript-eslint/eslint-plugin
- eslint-config-airbnb-typescript
- eslint-config-airbnb-base
- eslint-plugin-import
- prettier
- eslint-config-prettier
- eslint-plugin-prettier

## Configuration Files Generated

### 1. .eslintrc.json
ESLint configuration with Airbnb TypeScript rules:
```json
{
  "parser": "@typescript-eslint/parser",
  "parserOptions": {
    "ecmaVersion": "latest",
    "sourceType": "module",
    "project": "./tsconfig.json"
  },
  "extends": [
    "airbnb-base",
    "airbnb-typescript/base",
    "plugin:@typescript-eslint/recommended",
    "plugin:prettier/recommended"
  ],
  "plugins": ["@typescript-eslint", "import"],
  "rules": {
    "import/prefer-default-export": "off",
    "class-methods-use-this": "off",
    "no-console": "warn",
    "@typescript-eslint/no-explicit-any": "error"
  }
}
```

### 2. .prettierrc
Prettier formatting rules:
```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2,
  "arrowParens": "always"
}
```

### 3. .prettierignore
Files to ignore:
```
node_modules
dist
build
coverage
*.min.js
```

### 4. .eslintignore
Files to ignore:
```
node_modules
dist
build
coverage
```

### 5. package.json scripts
Add these scripts:
```json
{
  "scripts": {
    "lint": "eslint . --ext .ts,.tsx",
    "lint:fix": "eslint . --ext .ts,.tsx --fix",
    "format": "prettier --write \"src/**/*.{ts,tsx,json,md}\"",
    "format:check": "prettier --check \"src/**/*.{ts,tsx,json,md}\""
  }
}
```

### 6. .vscode/settings.json (Optional)
VS Code integration:
```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "eslint.validate": [
    "javascript",
    "typescript"
  ]
}
```

## Airbnb Style Guide Key Rules

**This configuration enforces:**

**Variables:**
- Use `const` by default, `let` when reassignment needed
- No `var` usage
- Block-scoped declarations

**Functions:**
- Arrow functions for anonymous functions
- Function declarations for named functions
- Default parameters over conditional assignment

**Objects & Arrays:**
- Literal syntax (`{}`, `[]`)
- Object/array spread over `Object.assign()`
- Destructuring for multiple values
- Shorthand properties and methods

**Strings:**
- Template literals over concatenation
- Single quotes for strings (Prettier handles this)

**Naming:**
- camelCase for variables and functions
- PascalCase for classes and types
- UPPER_SNAKE_CASE for constants

**TypeScript Specific:**
- No `any` types (error level)
- Explicit return types for exported functions
- Interface over type when possible
- Proper generic naming

**Code Style:**
- Semicolons required
- 2-space indentation (configurable)
- Trailing commas in multiline
- Consistent spacing

## Installation Process

### Step 1: Install Dependencies

**Using npm:**
```bash
npm install -D eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin eslint-config-airbnb-typescript eslint-config-airbnb-base eslint-plugin-import prettier eslint-config-prettier eslint-plugin-prettier
```

**Using Bun:**
```bash
bun add -D eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin eslint-config-airbnb-typescript eslint-config-airbnb-base eslint-plugin-import prettier eslint-config-prettier eslint-plugin-prettier
```

### Step 2: Create Configuration Files

Generate all configuration files listed above.

### Step 3: Update package.json

Add lint and format scripts.

### Step 4: Run Initial Format

```bash
npm run format
npm run lint:fix
```

### Step 5: Verify Setup

```bash
npm run lint
```

## Custom Rule Adjustments

Common rules to adjust based on project needs:

```json
{
  "rules": {
    // Disable default export requirement
    "import/prefer-default-export": "off",

    // Allow class methods without 'this'
    "class-methods-use-this": "off",

    // Warn on console.log (don't error)
    "no-console": "warn",

    // Error on any types
    "@typescript-eslint/no-explicit-any": "error",

    // Allow unused vars with underscore prefix
    "@typescript-eslint/no-unused-vars": ["error", {
      "argsIgnorePattern": "^_"
    }],

    // Adjust max line length
    "max-len": ["warn", {
      "code": 100,
      "ignoreComments": true,
      "ignoreStrings": true
    }]
  }
}
```

## Git Hooks (Optional)

### Using Husky + lint-staged

**Install:**
```bash
npm install -D husky lint-staged
npx husky install
```

**Add .husky/pre-commit:**
```bash
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"
npx lint-staged
```

**Add to package.json:**
```json
{
  "lint-staged": {
    "*.{ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ]
  }
}
```

## Editor Integration

### VS Code Extensions

Install these extensions:
- ESLint (dbaeumer.vscode-eslint)
- Prettier - Code formatter (esbenp.prettier-vscode)

### VS Code Settings

Create `.vscode/settings.json` with the configuration above.

## Troubleshooting

### ESLint Parsing Errors

**Issue:** `Parsing error: Cannot read file 'tsconfig.json'`
**Fix:** Ensure `parserOptions.project` points to correct tsconfig.json

### Prettier Conflicts

**Issue:** ESLint and Prettier rules conflict
**Fix:** Ensure `eslint-config-prettier` is last in extends array

### Import Resolution

**Issue:** ESLint can't resolve imports with `@/` alias
**Fix:** Add to .eslintrc.json:
```json
{
  "settings": {
    "import/resolver": {
      "typescript": {
        "project": "./tsconfig.json"
      }
    }
  }
}
```

Install: `npm install -D eslint-import-resolver-typescript`

## Validation Checklist

After setup, verify:
- [ ] All dependencies installed
- [ ] Configuration files created
- [ ] Scripts added to package.json
- [ ] `npm run lint` runs without errors
- [ ] `npm run format` formats code
- [ ] VS Code shows linting errors
- [ ] Format on save works in editor
- [ ] No ESLint/Prettier conflicts

## Integration with Project

This skill integrates with project structure:

```
project-root/
├── .eslintrc.json          # ESLint config
├── .prettierrc             # Prettier config
├── .eslintignore           # ESLint ignore
├── .prettierignore         # Prettier ignore
├── .vscode/
│   └── settings.json       # Editor config
├── package.json            # With scripts
└── src/                    # Your code (will be linted)
```

## Post-Setup Actions

After setup:
1. Run `npm run format` to format all code
2. Run `npm run lint:fix` to auto-fix issues
3. Manually fix remaining linting errors
4. Commit configuration files
5. Share with team via git

## Related Skills

- **ddd-context-generator**: Generates code following these rules
- **ddd-validator**: Can check for code quality violations
- Use this skill BEFORE generating code for best results

## Best Practices

1. **Run before committing**: Always lint and format before commits
2. **Fix incrementally**: Don't disable rules, fix the issues
3. **Team agreement**: Discuss and agree on custom rules
4. **CI/CD integration**: Add linting to CI pipeline
5. **Regular updates**: Keep dependencies updated

---

**Note:** This skill sets up code quality tooling. For architectural validation, use `ddd-validator` skill.
