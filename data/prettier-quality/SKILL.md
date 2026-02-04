---
name: prettier-quality
description: Interpretive guidance for Prettier code formatting across multiple file types (JS/TS, YAML, JSON, CSS, HTML). Use when configuring Prettier, troubleshooting formatting issues, or understanding tool selection for these file types.
---

# Prettier Quality Skill

Prettier is an opinionated code formatter that supports many languages. This skill provides interpretive guidance on when Prettier is the right tool and how our configuration balances strictness with flexibility.

## Required Reading

Fetch official Prettier documentation when needed:

- **<https://prettier.io/docs/options>** - All configuration options
- **<https://prettier.io/docs/cli>** - CLI usage
- **<https://prettier.io/docs/configuration>** - Config file formats and discovery

## Core Understanding

### Prettier Philosophy

**Key principle:** End style debates by enforcing consistent formatting automatically.

**What this means:**

- **Minimal configuration** - Prettier is intentionally opinionated; fewer options = less bikeshedding
- **Format on save** - Integrate with editors/hooks for seamless experience
- **No partial formatting** - Entire file reformatted each time (ensures consistency)

**Our overrides:**

- **printWidth: 9999** - Effectively disable line wrapping; let content breathe naturally
- **singleQuote: true** - JavaScript community standard
- **singleAttributePerLine: true** - Cleaner diffs for JSX/HTML

### When Prettier vs Other Tools

**Prettier handles:**

- JavaScript, TypeScript (`.js`, `.jsx`, `.ts`, `.tsx`, `.mjs`, `.cjs`)
- YAML (`.yaml`, `.yml`)
- JSON (`.json`, `.json5`, `.jsonc`)
- CSS, SCSS, Less
- HTML, Vue, Angular templates
- GraphQL

**Not Prettier:**

- **Markdown** - Use markdownlint (better table handling, CommonMark compliance)
- **Python** - Use ruff or black (Python-native understanding)
- **Shell** - Use shfmt (shell-specific formatting)
- **Ruby** - Use standardrb or rubocop (Ruby-native)

### Tool Selection in lint.py

The linting script uses this priority:

1. **Project config detected** - Use configured tools (e.g., biome if `biome.json` exists)
2. **No project config** - Fall back to defaults (Prettier for YAML/JSON, ruff for Python)

For JS/TS specifically:

- If `biome.json` exists: use biome (modern all-in-one)
- If `eslint.config.js` exists: use eslint + prettier
- Otherwise: fall back to biome

For YAML/JSON:

- Prettier is the default and only option

## Configuration Approach

### Layer 1: Project Config (Preferred)

**Best practice:** Add `.prettierrc` to project root for team consistency.

```json
{
  "singleQuote": true,
  "trailingComma": "all"
}
```

**Config file discovery:** Prettier searches up from file location for config files.

### Layer 2: Global Fallback

**When no project config exists:**

1. Check `~/.prettierrc.json5` (user global config)
2. Fall back to skill default config

**Our default config** in this skill directory provides sensible defaults for personal projects.

## YAML Formatting

### Why Prettier for YAML

- Consistent indentation (2 spaces)
- Normalized quoting (removes unnecessary quotes)
- Sorted/aligned keys (when possible)
- Trailing newline enforcement

### YAML-Specific Settings

Our config uses `printWidth: 300` for YAML via overrides - allows long lines for CI/CD pipelines and configuration values that shouldn't wrap.

### Common YAML Patterns

**Before Prettier:**

```yaml
name:   'my-app'
version: "1.0.0"
dependencies:
    - lodash
    -   express
```

**After Prettier:**

```yaml
name: my-app
version: 1.0.0
dependencies:
  - lodash
  - express
```

## JSON Formatting

Prettier normalizes:

- Consistent indentation (2 spaces)
- Trailing commas removed (JSON spec)
- Consistent quoting
- Sorted keys (configurable)

**Note:** For `package.json`, Prettier respects npm's key ordering conventions.

## Common Pitfalls

### Pitfall #1: Conflicting with ESLint

**Problem:** ESLint and Prettier disagree on formatting.

**Solution:** Use `eslint-config-prettier` to disable ESLint formatting rules:

```bash
npm install -D eslint-config-prettier
```

Then add to ESLint config:

```js
export default [
  // ... other configs
  require("eslint-config-prettier"),
];
```

### Pitfall #2: Prettier Reformats Everything

**Problem:** Prettier changes files you didn't want changed.

**Solution:** Use `.prettierignore`:

```text
# Don't format generated files
*.generated.ts
api/types.ts

# Vendor code
vendor/
```

### Pitfall #3: Config Not Found

**Problem:** Prettier uses defaults instead of your config.

**Debug:**

```bash
prettier --find-config-path path/to/file.ts
```

**Common causes:**

- Config file in wrong location
- Typo in config filename (`.prettierrc` not `.prettierc`)

## Automatic Hook Behavior

The mr-sparkle PostToolUse hook:

1. Triggers after Write/Edit operations
2. Detects supported file types
3. Runs `prettier --write` if project has Prettier config
4. Falls back to global/skill default config
5. Silently skips if prettier not installed

## Quality Checklist

**Before committing formatted files:**

- [ ] Prettier config committed to repo (for team consistency)
- [ ] `.prettierignore` excludes generated/vendor files
- [ ] No conflicts with ESLint (use eslint-config-prettier)
- [ ] Editor configured for format-on-save

## Reference Files

- `default-config.json5` - Fallback configuration with opinionated defaults
- `default-ignore` - Standard ignore patterns

## Official Documentation

- <https://prettier.io/docs/> - Main documentation
- <https://prettier.io/docs/options> - All options with descriptions
- <https://prettier.io/playground/> - Interactive playground

**Remember:** Prettier's value is ending style debates. Resist the urge to configure extensively.
