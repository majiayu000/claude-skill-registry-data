---
name: prettier-config
description: Prettier configuration validation and templates for package.json "prettier" field in MetaSaver monorepos. Includes 4 required standards (prettier field in package.json with string reference only, no separate prettierrc files, prettier in devDependencies, required npm scripts format and format:check). Use when creating or auditing Prettier configs to ensure consistent code formatting via shared library.
---

# Prettier Configuration Skill

This skill provides package.json "prettier" field templates and validation logic for Prettier formatting setup.

## Purpose

Manage Prettier configuration to:

- Configure code formatting via package.json "prettier" field
- Use shared configuration from @metasaver/core-prettier-config
- Maintain simple string reference pattern (complexity in shared library)
- Ensure consistent formatting across monorepo
- Provide required npm scripts for formatting

## Usage

This skill is invoked by the `prettier-agent` when:

- Creating new Prettier configurations
- Auditing existing Prettier configurations
- Validating Prettier configs against standards

## Templates

Standard templates are located at:

```
templates/prettier-field.template.json
templates/prettierignore.template
```

## The 4 Prettier Standards

### Rule 1: Prettier Field in package.json

Must have "prettier" field with string reference only:

```json
{
  "prettier": "@metasaver/core-prettier-config/react"
}
```

OR for base projects:

```json
{
  "prettier": "@metasaver/core-prettier-config"
}
```

The prettier field maps to config type based on projectType:

| projectType    | Config Type | Description                 |
| -------------- | ----------- | --------------------------- |
| base           | base        | Minimal config (utilities)  |
| node           | base        | Node.js backend services    |
| web-standalone | react       | Vite React web applications |
| react-library  | react       | React component libraries   |

All Prettier rules and configuration complexity lives in the shared @metasaver/core-prettier-config library. Individual projects should always use string references for configuration.

### Rule 2: No Separate .prettierrc Files

Configuration must be in package.json only:

- NO `.prettierrc`, `.prettierrc.json`, `.prettierrc.js`, or similar files
- ONLY package.json "prettier" field is allowed
- Keeps configuration simple and centralized

Exception: Root `.prettierignore` file is REQUIRED (see Rule 4).

### Rule 3: Prettier Dependency

Must have in package.json devDependencies:

```json
{
  "devDependencies": {
    "prettier": "^3.0.0",
    "@metasaver/core-prettier-config": "workspace:*"
  }
}
```

For monorepos, use `workspace:*` protocol to reference the shared config package.

### Rule 4: Required npm Scripts and Root Ignore File

**npm Scripts:**

Must include format scripts in package.json:

For packages:

```json
{
  "scripts": {
    "format": "prettier --check .",
    "format:check": "prettier --check .",
    "format:fix": "prettier --write ."
  }
}
```

For monorepo root:

```json
{
  "scripts": {
    "format": "turbo run format",
    "format:check": "turbo run format:check",
    "format:fix": "turbo run format:fix"
  }
}
```

**Root .prettierignore:**

Must have `.prettierignore` at repository root with essential patterns:

```
# Dependencies
node_modules
pnpm-lock.yaml

# Build outputs
dist
build
.next
.turbo

# Coverage
coverage

# OS
.DS_Store
```

## Validation

To validate a Prettier configuration:

1. Read package.json to get `metasaver.projectType`
2. Map projectType to expected config type (react vs base)
3. Check that "prettier" field exists in package.json
4. Verify it's a string reference (not inline object)
5. Verify shared config dependency exists
6. Check npm scripts (format, format:check, format:fix)
7. Check root .prettierignore exists (monorepo only)
8. Verify .prettierrc files do not exist
9. Report violations

### Validation Approach

```javascript
// Rule 1: Map projectType to config type
const typeMap = {
  base: "base",
  node: "base",
  "web-standalone": "react",
  "react-library": "react",
};
const expectedType = typeMap[projectType];

// Check prettier field exists and is string
const prettierField = packageJson.prettier;
if (!prettierField) {
  errors.push("Rule 1: Missing 'prettier' field in package.json");
} else if (typeof prettierField !== "string") {
  errors.push(
    "Rule 1: prettier field must be string reference, not inline object",
  );
} else {
  // Verify correct config type
  const expectedRef =
    expectedType === "base"
      ? "@metasaver/core-prettier-config"
      : "@metasaver/core-prettier-config/react";
  if (prettierField !== expectedRef) {
    errors.push(
      `Rule 1: Expected "${expectedRef}" for projectType "${projectType}"`,
    );
  }
}

// Rule 2: Check for .prettierrc files
const prettierrcFiles = glob("**/.prettierrc*", {
  ignore: ["node_modules/**"],
});
if (prettierrcFiles.length > 0) {
  errors.push(
    `Rule 2: Remove .prettierrc files: ${prettierrcFiles.join(", ")}`,
  );
}

// Rule 3: Check dependencies
const deps = packageJson.devDependencies || {};
if (!deps["@metasaver/core-prettier-config"]) {
  errors.push(
    "Rule 3: Missing @metasaver/core-prettier-config in devDependencies",
  );
}
if (!deps.prettier) {
  errors.push("Rule 3: Missing prettier in devDependencies");
}

// Rule 4: Check npm scripts
const scripts = packageJson.scripts || {};
const isMonorepoRoot = !packageJson.name; // Root has no name
if (isMonorepoRoot) {
  if (!scripts.format?.includes("turbo")) {
    errors.push('Rule 4: Monorepo root must use "turbo run format"');
  }
} else {
  if (!scripts.format?.includes("prettier")) {
    errors.push('Rule 4: Missing "format" script with prettier');
  }
  if (!scripts["format:check"]?.includes("prettier")) {
    errors.push('Rule 4: Missing "format:check" script');
  }
  if (!scripts["format:fix"]?.includes("prettier")) {
    errors.push('Rule 4: Missing "format:fix" script with --write');
  }
}

// Rule 4: Check root .prettierignore (monorepo only)
if (isMonorepoRoot) {
  const rootIgnore = fs.existsSync(".prettierignore");
  if (!rootIgnore) {
    errors.push("Rule 4: Missing .prettierignore at repository root");
  }
}
```

## Repository Type Considerations

- **Consumer Repos**: Must strictly follow all 4 standards unless exception declared
- **Library Repos**: May have custom configs for specialized formatting needs

### Exception Declaration

Consumer repos may declare exceptions in package.json:

```json
{
  "metasaver": {
    "exceptions": {
      "prettier-config": {
        "type": "custom-rules",
        "reason": "Requires custom printWidth for legacy documentation files"
      }
    }
  }
}
```

## Best Practices

1. Use package.json "prettier" field (not .prettierrc files)
2. Choose template matching your projectType
3. Keep config as string reference - delegate complexity to shared library
4. Add shared config dependency with workspace protocol
5. Include all three format scripts (format, format:check, format:fix)
6. Place .prettierignore at repository root only
7. Re-audit after making changes

## Integration

This skill integrates with:

- Repository type provided via `scope` parameter. If not provided, use `/skill scope-check`
- `/skill audit-workflow` - Bi-directional comparison workflow
- `/skill remediation-options` - Conform/Update/Ignore choices
- `eslint-agent` - Coordination with ESLint style rules
- `editorconfig-agent` - Coordination with EditorConfig settings
