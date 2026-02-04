---
name: scripts-config
description: Utility scripts directory configuration (/scripts) for MetaSaver monorepos including setup automation, environment management, and cross-platform support. Includes 4 critical standards (setup scripts, cross-platform support, error handling, documentation). Use when creating or auditing /scripts directory with Node.js and shell utility scripts.
---

# Scripts Directory Configuration Skill

This skill provides templates and validation logic for /scripts directory configuration in MetaSaver monorepos.

## Purpose

Manage /scripts directory to:

- Automate environment setup (setup-env.js, setup-npmrc.js)
- Provide utility scripts for deployment and development
- Ensure cross-platform compatibility (Windows, macOS, Linux)
- Standardize error handling and documentation

## Usage

This skill is invoked by the `scripts-agent` when:

- Creating new /scripts directory
- Auditing existing scripts directory configurations
- Validating scripts against standards

## Templates

Standard script templates are located at:

```
templates/setup.sh.template
```

## The 4 /scripts Standards

### Rule 1: Setup Scripts (CRITICAL)

**Required scripts for all repositories:**

| Script             | Purpose                                                     | Repository Type |
| ------------------ | ----------------------------------------------------------- | --------------- |
| setup-env.js       | Generate .env from .env.example files                       | All repos       |
| setup-npmrc.js     | Generate .npmrc from .npmrc.template with token replacement | All repos       |
| clean-and-build.sh | Clean and rebuild monorepo                                  | All repos       |

**Additional scripts for consumer repositories:**

| Script                | Purpose                            |
| --------------------- | ---------------------------------- |
| back-to-prod.sh       | Switch to GitHub Packages registry |
| use-local-packages.sh | Switch to local Verdaccio registry |
| killport.sh           | Cross-platform port management     |

**Validation:**

```bash
# Check required scripts exist
[ -f "scripts/setup-env.js" ] || echo "VIOLATION: Missing setup-env.js"
[ -f "scripts/setup-npmrc.js" ] || echo "VIOLATION: Missing setup-npmrc.js"
[ -f "scripts/clean-and-build.sh" ] || echo "VIOLATION: Missing clean-and-build.sh"

# Consumer repos only
if [ "$REPO_TYPE" = "consumer" ]; then
  [ -f "scripts/back-to-prod.sh" ] || echo "VIOLATION: Missing back-to-prod.sh"
  [ -f "scripts/use-local-packages.sh" ] || echo "VIOLATION: Missing use-local-packages.sh"
  [ -f "scripts/killport.sh" ] || echo "VIOLATION: Missing killport.sh"
fi
```

### Rule 2: Cross-Platform Support (CRITICAL)

**Requirements for Node.js scripts:**

- ALWAYS USE `path` module for all file paths (do not hardcode slashes)
- USE `process.platform` for OS-specific logic
- INCLUDE Shebang: `#!/usr/bin/env node`

**Example:**

```javascript
const path = require("path");
const envPath = path.join(__dirname, "..", ".env"); // CORRECT - uses path module
// const envPath = '../.env';  // INCORRECT - avoid hardcoded paths
```

**Validation:**

```bash
# Verify path module usage
grep -q "require.*path" scripts/*.js || echo "VIOLATION: path module must be used"

# Check for hardcoded paths (should not exist)
grep -E "\.\.\/|\.\.\\\\|\.\/" scripts/*.js && echo "WARNING: Hardcoded paths detected - use path module instead"
```

### Rule 3: Error Handling

**Required error handling patterns:**

- `try-catch` blocks for async operations
- `console.log` feedback for success/failure
- `process.exit(1)` on errors
- Descriptive error messages

**Example:**

```javascript
try {
  // Operation
  console.log("Success: Operation completed");
} catch (error) {
  console.error("Error: Operation failed -", error.message);
  process.exit(1);
}
```

**Validation:**

```bash
# Check for error handling
grep -q "try.*catch" scripts/*.js || echo "WARNING: No try-catch blocks found"
grep -q "process.exit" scripts/*.js || echo "WARNING: No process.exit calls found"
```

### Rule 4: Documentation

**Required documentation elements:**

- Shebang line (`#!/usr/bin/env node` or `#!/usr/bin/env bash`)
- JSDoc comments for Node.js scripts
- Usage examples in comments
- scripts/README.md documenting all scripts

**README.md structure:**

```markdown
# Scripts Directory

Utility scripts for [repository name].

## Available Scripts

### setup-env.js

Description of what it does and when to use it.

### setup-npmrc.js

Description of what it does and when to use it.

...
```

**Validation:**

```bash
# Check for shebang
head -n1 scripts/*.js | grep -q "#!/usr/bin/env node" || echo "VIOLATION: Missing shebang"

# Check for README
[ -f "scripts/README.md" ] || echo "VIOLATION: Missing scripts/README.md"
```

## Validation

To validate /scripts directory:

1. Detect repository type (library vs consumer)
2. Check that /scripts exists at repository root
3. Verify required scripts present (Rule 1)
4. Check cross-platform patterns (Rule 2)
5. Verify error handling (Rule 3)
6. Check documentation (Rule 4)
7. Report violations

### Validation Approach

```bash
# Check directory exists at root
[ -d "scripts" ] || echo "VIOLATION: /scripts directory not found at root"

# Validate against 4 standards (see rules above)
# Report only violations
```

## Repository Type Considerations

- **Library Repos** (`@metasaver/multi-mono`): Core setup scripts only
- **Consumer Repos**: All setup scripts + registry switching + port management
- **All Repos**: Scripts must be at root `/scripts` directory only

## Best Practices

1. ALWAYS PLACE scripts at repository root `/scripts` (use subdirectories for monorepo workspaces only)
2. USE Node.js for cross-platform file operations (setup-env.js, setup-npmrc.js)
3. USE bash for build/deploy scripts with proper error handling
4. INCLUDE `chmod +x` instructions for shell scripts
5. DOCUMENT each script in scripts/README.md
6. TEST scripts on multiple platforms when possible
7. ALWAYS USE `path` module consistently (avoid hardcoded paths)
8. RE-AUDIT after making changes

## Integration

This skill integrates with:

- Repository type provided via `scope` parameter. If not provided, use `/skill scope-check`
- `/skill audit-workflow` - Bi-directional comparison workflow
- `/skill remediation-options` - Conform/Update/Ignore choices
- `package-scripts-agent` - For npm scripts that invoke /scripts utilities
