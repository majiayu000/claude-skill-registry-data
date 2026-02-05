---
name: GDScript Format
description: Format and lint GDScript files using gdscript-formatter. Use after editing GDScript files to ensure code style consistency.
---

# GDScript Format

Format and lint GDScript files using the gdscript-formatter tool from GDQuest.

## When to Use

- After creating or editing GDScript files
- Before committing code to ensure style consistency
- When running code quality checks

## Setup

Install the formatter binary using the install script included in this skill (`scripts/install.sh`).

```bash
scripts/install.sh
```

This downloads the appropriate binary for your platform (Linux/Windows x86_64) to the skill's `bin/` directory.

## Format

Format GDScript files using the format script included in this skill (`scripts/format.sh`).

### Single File

```bash
scripts/format.sh path/to/file.gd
```

### Multiple Files

```bash
scripts/format.sh path/to/file1.gd path/to/file2.gd
```

### Safe Mode

```bash
scripts/format.sh --safe path/to/file.gd
```

Verifies that formatting doesn't change code semantics.

### Check Mode (CI)

```bash
scripts/format.sh --check path/to/file.gd
```

Returns exit code 1 if changes are needed (useful for CI/CD).

### Reorder Code

```bash
scripts/format.sh --reorder-code path/to/file.gd
```

Reorders code according to GDScript style guide.

## Lint

Check code style using the lint script included in this skill (`scripts/lint.sh`).

### Single File

```bash
scripts/lint.sh path/to/file.gd
```

### With Options

```bash
scripts/lint.sh --max-line-length 120 path/to/file.gd
scripts/lint.sh --disable unused-argument,private-access path/to/file.gd
```

## Lint Rules

Available rules include:
- **Naming**: `function-name`, `class-name`, `variable-name`, `signal-name`
- **Quality**: `unused-argument`, `max-line-length`, `no-else-return`, `private-access`

## Exit Codes

- **0**: Success (no issues or formatting applied)
- **1**: Issues found or changes needed
- **2**: Error (binary not found, invalid file, etc.)
