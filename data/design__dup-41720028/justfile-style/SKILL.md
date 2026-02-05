---
name: justfile-style
description: Style guidelines for justfile recipe documentation. Use when writing or editing justfiles to ensure consistent and concise documentation.
---

# Justfile Style Guidelines

This skill provides best practices for writing justfile recipe documentation comments.

## Doc Comment Simplification

For very short justfile recipes, change the doc comment string to be the entire command instead of a descriptive phrase.

### When to Simplify

- The cutoff for when to perform this refactoring should be approximately a single line of 120 characters
- If the recipe is a shebang recipe, don't shorten the doc comment
- If the recipe is multiple lines, or longer than 120 characters, don't shorten the doc comment

### Example Transformation

❌ Before:

```justfile
# Install dependencies
[group('setup')]
install:
    npm install
```

✅ After:

```justfile
# npm install
[group('setup')]
install:
    npm install
```

### Rationale

For simple, single-command recipes, the command itself is often more informative than a descriptive phrase. This approach:

1. **Reduces redundancy**: "Install dependencies" vs "npm install" convey the same information
2. **Shows the actual command**: Users can see exactly what will run
3. **Maintains consistency**: All simple recipes follow the same pattern
4. **Improves scannability**: The actual command is immediately visible

### When NOT to Simplify

Keep descriptive doc comments for:

1. **Multi-line recipes**:

```justfile
# Set up development environment
[group('setup')]
dev-setup:
    npm install
    cp .env.example .env
    just db-migrate
```

2. **Shebang recipes**:

```justfile
# Generate API documentation
[group('docs')]
gen-docs:
    #!/usr/bin/env bash
    set -euo pipefail
    # ... multiple lines of bash script
```

3. **Long single-line commands** (>120 characters):

```justfile
# Build production bundle with optimizations
[group('build')]
build-prod:
    webpack --mode production --config webpack.prod.js --optimization-minimize --output-path dist/
```

In these cases, a descriptive comment provides more value than repeating the complex command.
