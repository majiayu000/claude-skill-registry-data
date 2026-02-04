---
name: nodemon-config
description: Nodemon JSON configuration templates and validation logic for development server hot-reload. Includes 5 required standards (watch patterns, exec command, ignore patterns, development settings, required dependencies). Use when creating or auditing nodemon.json files to enable automatic server restart on file changes.
---

# Nodemon Configuration Skill

This skill provides nodemon.json templates and validation logic for development server hot-reload configuration.

## Purpose

Manage nodemon.json configuration to:

- Enable automatic server restart on file changes
- Configure appropriate watch patterns for TypeScript/JavaScript projects
- Set up proper ignore patterns to prevent restart loops
- Define development environment settings
- Support both ts-node and node execution

## Usage

This skill is invoked by the `nodemon-agent` when:

- Creating new nodemon.json files
- Auditing existing Nodemon configurations
- Validating Nodemon settings against standards

## Templates

Standard templates are located at:

```
templates/nodemon-typescript.template.json    # TypeScript projects (ts-node)
templates/nodemon-javascript.template.json    # JavaScript projects (node)
```

## The 5 Nodemon Standards

### Rule 1: Required Watch Patterns

**Watch the source directory and specify file extensions:**

```json
{
  "watch": ["src"],
  "ext": "ts,js,json"
}
```

**For TypeScript projects:**

- Extensions: `ts,js,json`

**For JavaScript projects:**

- Extensions: `js,json`

**Validation:**

```bash
# Check watch patterns
jq '.watch | contains(["src"])' nodemon.json
jq '.ext' nodemon.json | grep -q "ts\|js"
```

### Rule 2: Required Exec Command

**Execute with appropriate runtime:**

**TypeScript projects:**

```json
{
  "exec": "ts-node src/index.ts"
}
```

**JavaScript projects:**

```json
{
  "exec": "node src/index.js"
}
```

**Compiled projects:**

```json
{
  "exec": "node dist/index.js"
}
```

**Validation:**

```bash
# Check exec command exists
jq '.exec' nodemon.json

# Verify matches project type
if grep -q "typescript" package.json; then
  jq '.exec' nodemon.json | grep -q "ts-node" || echo "VIOLATION: TypeScript project should use ts-node"
fi
```

### Rule 3: Required Ignore Patterns

**Prevent restart loops by ignoring:**

```json
{
  "ignore": [
    "node_modules/**",
    "dist/**",
    "**/*.test.ts",
    "**/*.spec.ts",
    ".git/**"
  ]
}
```

**For JavaScript projects:**

```json
{
  "ignore": [
    "node_modules/**",
    "dist/**",
    "**/*.test.js",
    "**/*.spec.js",
    ".git/**"
  ]
}
```

**Required patterns:**

- `node_modules/**` (always)
- `dist/**` (always)
- Test files (`.test.ts`, `.spec.ts`, or `.test.js`, `.spec.js`)
- `.git/**` (always)

**Validation:**

```bash
# Check all required ignore patterns
jq '.ignore | contains(["node_modules/**"])' nodemon.json
jq '.ignore | contains(["dist/**"])' nodemon.json
jq '.ignore | contains([".git/**"])' nodemon.json
jq '.ignore | map(select(test("test|spec"))) | length > 0' nodemon.json
```

### Rule 4: Development Settings

**Configure performance and environment:**

```json
{
  "verbose": false,
  "delay": 1000,
  "env": {
    "NODE_ENV": "development"
  }
}
```

**Settings explained:**

- `verbose: false` - Reduces console noise
- `delay: 1000` - Prevents multiple rapid restarts (1 second delay)
- `NODE_ENV: "development"` - Sets development mode

**Validation:**

```bash
# Check delay setting
jq '.delay' nodemon.json | grep -q "1000" || echo "VIOLATION: Missing or incorrect delay"

# Check NODE_ENV
jq '.env.NODE_ENV' nodemon.json | grep -q "development" || echo "VIOLATION: Missing NODE_ENV"
```

### Rule 5: Required Dependencies

**Package.json must include:**

**TypeScript projects:**

```json
{
  "devDependencies": {
    "nodemon": "^3.0.0",
    "ts-node": "^10.9.0"
  }
}
```

**JavaScript projects:**

```json
{
  "devDependencies": {
    "nodemon": "^3.0.0"
  }
}
```

**Required npm script:**

```json
{
  "scripts": {
    "dev": "nodemon"
  }
}
```

**Validation:**

```bash
# Check dependencies
jq '.devDependencies | has("nodemon")' package.json

# If TypeScript project
if [ -f "tsconfig.json" ]; then
  jq '.devDependencies | has("ts-node")' package.json || echo "VIOLATION: Missing ts-node"
fi

# Check dev script
jq '.scripts.dev' package.json | grep -q "nodemon" || echo "VIOLATION: Missing dev script"
```

## Validation

To validate nodemon.json configuration:

1. Check if nodemon.json exists (optional - only validate if present)
2. Determine project type (TypeScript vs JavaScript)
3. Read nodemon.json and package.json
4. Validate against 5 standards
5. Check dependencies match project type
6. Verify dev script exists
7. Report violations

### Validation Approach

```bash
# Check if nodemon.json exists (skip if not present - it's optional)
if [ ! -f "nodemon.json" ]; then
  echo "ℹ️  nodemon.json not present (optional)"
  exit 0
fi

# Rule 1: Watch patterns
jq '.watch | contains(["src"])' nodemon.json || echo "VIOLATION: watch must include 'src'"
jq '.ext' nodemon.json | grep -q "js" || echo "VIOLATION: ext must include 'js'"

# Rule 2: Exec command
jq '.exec' nodemon.json > /dev/null || echo "VIOLATION: Missing exec command"

# Rule 3: Ignore patterns
for pattern in "node_modules/**" "dist/**" ".git/**"; do
  jq ".ignore | contains([\"$pattern\"])" nodemon.json | grep -q "true" || echo "VIOLATION: Missing ignore pattern: $pattern"
done

# Rule 4: Development settings
jq '.delay' nodemon.json > /dev/null || echo "VIOLATION: Missing delay setting"
jq '.env.NODE_ENV' nodemon.json | grep -q "development" || echo "VIOLATION: Missing NODE_ENV"

# Rule 5: Dependencies
jq '.devDependencies | has("nodemon")' package.json | grep -q "true" || echo "VIOLATION: Missing nodemon in devDependencies"
jq '.scripts.dev' package.json | grep -q "nodemon" || echo "VIOLATION: Missing dev script"
```

## Repository Type Considerations

- **Consumer Repos**: Standard nodemon configuration enforced
- **Library Repos**: May have custom watch patterns for multi-package development
- **All Repos**: Nodemon is optional - only validate if nodemon.json exists

## Best Practices

1. Only validate if nodemon.json exists (it's optional)
2. Detect project type first (TypeScript vs JavaScript)
3. Use appropriate template based on project type
4. Verify dependencies match exec command (ts-node requires ts-node package)
5. Keep delay at 1000ms to prevent rapid restarts
6. Always ignore node_modules, dist, .git, and test files
7. Set NODE_ENV to development
8. Add "dev": "nodemon" script to package.json
9. Re-audit after making changes

## Integration

This skill integrates with:

- Repository type provided via `scope` parameter. If not provided, use `/skill scope-check`
- `/skill audit-workflow` - Bi-directional comparison workflow
- `/skill remediation-options` - Conform/Update/Ignore choices
- `typescript-agent` - For TypeScript project detection
- `package-scripts-agent` - For dev script validation
