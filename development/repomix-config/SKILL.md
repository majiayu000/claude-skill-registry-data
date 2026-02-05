---
name: repomix-config
description: Repomix AI-friendly codebase compression configuration (.repomix.config.json) template and validation logic. Achieves 70% token reduction through XML compression and repository-type-specific include patterns. Includes 5 critical standards (XML output format, include patterns by repo type, gitignore integration, exclude patterns, security checks). Use when creating or auditing .repomix.config.json files for optimal LLM context compression.
---

# Repomix Configuration Skill

This skill provides .repomix.config.json template and validation logic for AI-friendly codebase compression.

## Purpose

Manage .repomix.config.json to:

- Achieve 70% token reduction through XML compression
- Configure repository-type-specific include patterns
- Integrate with .gitignore for automatic exclusions
- Exclude build artifacts and prevent recursion
- Enable automatic security checks for sensitive data

## Usage

This skill is invoked by the `repomix-config-agent` when:

- Creating new .repomix.config.json files
- Auditing existing Repomix configurations
- Validating .repomix.config.json against standards

## Templates

Repository-type-specific templates are located in:

```
templates/.repomix.config.json.template
```

## The 5 Repomix Standards

### Rule 1: XML Output Format (CRITICAL)

**Must configure XML output with compression:**

```json
{
  "output": {
    "filePath": ".repomix-output.txt",
    "style": "xml",
    "showLineNumbers": true,
    "compress": true
  }
}
```

**Requirements:**

- `style: "xml"` - Enables Tree-sitter compression (70% token reduction vs plain text)
- `compress: true` - Activates compression
- `showLineNumbers: true` - Maintains code traceability
- `filePath: ".repomix-output.txt"` - Standard output location

**Validation:**

```bash
# Check XML output configuration
grep -q '"style": "xml"' .repomix.config.json || echo "VIOLATION: Missing XML format"
grep -q '"compress": true' .repomix.config.json || echo "VIOLATION: Compression disabled"
grep -q '"showLineNumbers": true' .repomix.config.json || echo "VIOLATION: Line numbers disabled"
```

### Rule 2: Include Patterns by Repository Type (CRITICAL)

**Must configure include patterns matching repository type:**

| Repository Type    | Include Patterns                                                                 |
| ------------------ | -------------------------------------------------------------------------------- |
| Turborepo          | `apps/**`, `packages/**`, `services/**`, `prisma/**`, `.github/**`, `scripts/**` |
| Library            | `packages/**`, `components/**`, `config/**`, `.github/**`, `scripts/**`          |
| Plugin Marketplace | `plugins/**`, `.claude-plugin/**`                                                |
| Python             | `tools/**`, `providers/**`, `*.py`, `.github/**`, `Dockerfile`                   |
| Shell              | `*.sh`, `scripts/**`, `.github/**`                                               |

**Validation:**

```bash
# For Turborepo (example)
grep -q '"apps/\*\*"' .repomix.config.json || echo "VIOLATION: Missing apps/** pattern"
grep -q '"packages/\*\*"' .repomix.config.json || echo "VIOLATION: Missing packages/** pattern"
```

### Rule 3: Gitignore Integration

**Must enable gitignore and default patterns:**

```json
{
  "ignore": {
    "useGitignore": true,
    "useDefaultPatterns": true
  }
}
```

**Settings explained:**

- `useGitignore: true` - Automatically respects .gitignore patterns
- `useDefaultPatterns: true` - Includes Repomix default exclusions

**Validation:**

```bash
# Check gitignore integration
grep -q '"useGitignore": true' .repomix.config.json || echo "VIOLATION: Gitignore disabled"
grep -q '"useDefaultPatterns": true' .repomix.config.json || echo "VIOLATION: Default patterns disabled"
```

### Rule 4: Exclude Patterns (CRITICAL)

**Must exclude build artifacts and prevent recursion:**

```json
{
  "ignore": {
    "customPatterns": [
      "node_modules/**",
      ".git/**",
      "dist/**",
      "build/**",
      ".turbo/**",
      ".next/**",
      "coverage/**",
      ".repomix-output.*",
      "*.log"
    ]
  }
}
```

**Critical exclusions:**

- `.repomix-output.*` - Prevents including previous outputs (recursion)
- Build artifacts - Reduces noise and context size
- Log files - Excludes runtime logs

**Validation:**

```bash
# Check critical exclusions
grep -q '".repomix-output.\*"' .repomix.config.json || echo "VIOLATION: Missing .repomix-output.* exclusion"
grep -q '"node_modules/\*\*"' .repomix.config.json || echo "VIOLATION: Missing node_modules exclusion"
```

### Rule 5: Security Check

**Must enable automatic security scanning:**

```json
{
  "security": {
    "enableSecurityCheck": true
  }
}
```

**Validation:**

```bash
# Check security enabled
grep -q '"enableSecurityCheck": true' .repomix.config.json || echo "VIOLATION: Security check disabled"
```

## Repository Type Detection

Use `/skill scope-check` to determine repository type if not provided.

## Validation

To validate .repomix.config.json:

1. Check that file exists at repository root
2. Detect repository type
3. Read .repomix.config.json content
4. Validate against 5 standards
5. Verify include patterns match repository type
6. Check .gitignore excludes `.repomix-output.*`
7. Report violations

### Validation Approach

```bash
# Check file exists
[ -f ".repomix.config.json" ] || echo "VIOLATION: Missing .repomix.config.json at root"

# Rule 1: XML output
grep -q '"style": "xml"' .repomix.config.json || echo "VIOLATION: Missing XML format"
grep -q '"compress": true' .repomix.config.json || echo "VIOLATION: Compression disabled"

# Rule 2: Include patterns (repo-specific)
# Example for Turborepo
grep -q '"apps/\*\*"' .repomix.config.json || echo "VIOLATION: Missing apps/** pattern"

# Rule 3: Gitignore integration
grep -q '"useGitignore": true' .repomix.config.json || echo "VIOLATION: Gitignore disabled"

# Rule 4: Exclude patterns
grep -q '".repomix-output.\*"' .repomix.config.json || echo "VIOLATION: Missing output exclusion"

# Rule 5: Security
grep -q '"enableSecurityCheck": true' .repomix.config.json || echo "VIOLATION: Security disabled"

# Check .gitignore
grep -q ".repomix-output.\*" .gitignore || echo "VIOLATION: .gitignore missing .repomix-output.* exclusion"
```

## Repository Type Considerations

- **Turborepo**: Includes apps, packages, services
- **Library**: Focuses on packages and components
- **Plugin Marketplace**: Includes plugins and .claude-plugin
- **Python**: Includes tools, providers, .py files
- **Shell**: Includes scripts and .sh files

## Best Practices

1. Root only - .repomix.config.json at repository root
2. Match repo type - Use appropriate include patterns
3. Always exclude .repomix-output.\* - Prevents recursion
4. Enable compression - Critical for 70% token reduction
5. Update .gitignore - Add `.repomix-output.*` exclusion
6. Re-audit after changes - Verify compliance
7. Use security check - Auto-detect sensitive data

## .gitignore Integration

**CRITICAL:** Always add to .gitignore:

```gitignore
# Repomix output
.repomix-output.*
```

This prevents committing compressed output to version control.

## Integration

This skill integrates with:

- Repository type provided via `scope` parameter. If not provided, use `/skill scope-check`
- `/skill audit-workflow` - Bi-directional comparison workflow
- `/skill remediation-options` - Conform/Update/Ignore choices
