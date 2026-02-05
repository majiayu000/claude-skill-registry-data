---
name: editorconfig-config
description: EditorConfig file validation and template for enforcing consistent coding styles across editors and IDEs in monorepos. Includes 4 required standards (root declaration, universal settings with UTF-8/LF/2-space defaults, language-specific sections for JS/TS/JSON/YAML/Markdown/Python/Shell/SQL/Docker/Prisma, root-only placement in monorepos). Use when creating or auditing .editorconfig files to ensure consistent code formatting.
---

# EditorConfig Configuration Skill

This skill provides .editorconfig template and validation logic for maintaining consistent coding styles across editors and IDEs.

## Purpose

Manage .editorconfig configuration to:

- Enforce consistent character encoding and line endings
- Define language-specific indentation rules
- Preserve trailing whitespace where needed (Markdown)
- Ensure monorepo consistency with single root configuration
- Cover all common file types in MetaSaver projects

## Usage

This skill is invoked by the `editorconfig-agent` when:

- Creating new .editorconfig files
- Auditing existing EditorConfig configurations
- Validating EditorConfig files against standards

## Template

The standard EditorConfig template is located at:

```
templates/.editorconfig.template
```

## The 4 EditorConfig Standards

### Rule 1: Root Declaration

File must start with root declaration:

```ini
root = true
```

This stops EditorConfig from searching parent directories, ensuring the monorepo has a single source of truth.

### Rule 2: Universal Settings with Default Indentation

Must include `[*]` section with these six settings:

```ini
[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = space
indent_size = 2
```

These settings apply to all files unless overridden by language-specific rules. The default 2-space indentation is inherited by most file types.

### Rule 3: Language-Specific Sections

Must include sections for all common file types:

**Core language sections (required):**

```ini
# TypeScript, JavaScript, JSX, TSX
[*.{ts,tsx,js,jsx,mjs,cjs}]
indent_size = 2
max_line_length = 100

# JSON files
[*.json]
indent_size = 2

# YAML files
[*.{yml,yaml}]
indent_size = 2

# Markdown files
[*.md]
trim_trailing_whitespace = false
max_line_length = off

# Python (if used in tooling)
[*.py]
indent_style = space
indent_size = 4
```

**Extended sections (recommended):**

```ini
# Shell scripts
[*.sh]
indent_size = 2

# Makefiles
[Makefile]
indent_style = tab

# Package.json (specific formatting)
[package.json]
indent_size = 2

# Lock files (should not be edited)
[{package-lock.json,pnpm-lock.yaml,yarn.lock}]
indent_size = 2
insert_final_newline = false

# SQL files
[*.sql]
indent_size = 2

# Docker files
[{Dockerfile,*.dockerfile}]
indent_size = 2

# Prisma schema files
[*.prisma]
indent_size = 2
```

### Rule 4: Root Location Only

In monorepos, .editorconfig must exist ONLY at repository root:

- Place at monorepo root (alongside pnpm-workspace.yaml)
- Individual packages must only reference the root .editorconfig file
- Single configuration ensures consistency across all packages

## Validation

Validation steps:

1. Check file exists at repository root
2. Verify root declaration is present
3. Check universal settings section `[*]` with all 6 settings (including indent defaults)
4. Verify core language-specific sections exist (JS/TS, JSON, YAML, Markdown, Python)
5. Scan for package-level .editorconfig files (monorepo only)
6. Report violations

### Validation Logic

```javascript
// Rule 1: Root declaration
if (!content.includes("root = true")) {
  errors.push("Rule 1: Missing 'root = true' declaration");
}

// Rule 2: Universal settings (check all 6)
[
  "[*]",
  "charset = utf-8",
  "end_of_line = lf",
  "insert_final_newline = true",
  "trim_trailing_whitespace = true",
  "indent_style = space",
  "indent_size = 2",
].forEach((setting) => {
  if (!content.includes(setting)) errors.push(`Rule 2: Missing ${setting}`);
});

// Rule 3: Core language sections
if (!/\[\*\.\{[^}]*ts[^}]*\}\]/.test(content)) {
  errors.push("Rule 3: Missing JS/TS indentation rules");
}
if (!/\[\*\.json\]/.test(content)) {
  errors.push("Rule 3: Missing JSON section");
}
if (!/\[\*\.\{[^}]*yml[^}]*\}\]/.test(content)) {
  errors.push("Rule 3: Missing YAML section");
}
if (!/\[\*\.md\]/.test(content)) {
  errors.push("Rule 3: Missing Markdown section");
}
if (!/\[\*\.py\]/.test(content)) {
  errors.push("Rule 3: Missing Python section");
}

// Rule 4: Package-level configs (monorepo only)
const packageConfigs = glob("packages/**/.editorconfig");
if (packageConfigs.length > 0) {
  errors.push(
    `Rule 4: Remove package-level configs: ${packageConfigs.join(", ")}`,
  );
}
```

## Exception Declaration

Repos may declare exceptions in package.json:

```json
{
  "metasaver": {
    "exceptions": {
      "editorconfig-config": {
        "type": "custom-language-rules",
        "reason": "Requires 4-space indentation for legacy YAML files"
      }
    }
  }
}
```

## Best Practices

1. Place .editorconfig at repository root (monorepo or standalone)
2. Use template as starting point
3. Preserve Markdown trailing whitespace (for double-space line breaks)
4. Keep extended sections for comprehensive coverage
5. Re-audit after making changes

## Integration

This skill integrates with:

- Repository type provided via `scope` parameter. If not provided, use `/skill scope-check`
- `/skill audit-workflow` - Bi-directional comparison workflow
- `/skill remediation-options` - Conform/Update/Ignore choices
- `prettier-agent` - Coordination with Prettier formatting rules
- `eslint-agent` - Coordination with ESLint style rules
