---
name: linting
description: Universal polyglot linting capabilities for Python, JavaScript/TypeScript, Markdown, Shell, Ruby, YAML, and JSON files. Use when you need to lint files programmatically, understand tool selection logic, or invoke linting from commands/agents.
---

# Linting Skill

This skill provides universal polyglot linting through a CLI script that detects file types, finds project configuration, and runs appropriate linters.

## Supported Languages and Tools

| Language              | Tool Groups (priority order)       | Config Detection                                  |
| --------------------- | ---------------------------------- | ------------------------------------------------- |
| Python                | `ruff` OR `pylint`+`isort`+`black` | pyproject.toml, ruff.toml, setup.cfg              |
| JavaScript/TypeScript | `biome` OR `eslint`+`prettier`     | biome.json, eslint.config.\*, package.json        |
| Markdown              | `markdownlint-cli2`                | .markdownlint-cli2.\*, ~/.markdownlint-cli2.jsonc |
| Shell                 | `shfmt`+`shellcheck`               | .editorconfig, .shellcheckrc                      |
| Ruby                  | `standard` OR `rubocop`            | .standard.yml, .rubocop.yml, Gemfile              |
| YAML                  | `prettier`                         | .prettierrc\*, ~/.prettierrc.json5                |
| JSON/JSON5/JSONC      | `prettier`                         | .prettierrc\*, ~/.prettierrc.json5                |

## Tool Selection Logic

The script uses **group-based priority selection**:

1. Tools are organized into groups (e.g., `[ruff]` vs `[pylint, isort, black]`)
2. First group with any project-level configuration wins
3. All tools in the winning group run (in order)
4. If no config found, falls back to first group's tools

**Example for Python:**

- If `pyproject.toml` has `[tool.ruff]` → runs `ruff check --fix` then `ruff format`
- If `setup.cfg` has `[isort]` section → runs `pylint`, `isort`, `black`
- If no config → runs `ruff` (first group default)

## CLI Script Usage

The universal linting script is at `scripts/lint.py`.

### Basic Usage

```bash
# Lint a file (auto-detects type, applies fixes)
./scripts/lint.py /path/to/file.py

# JSON output for programmatic use
./scripts/lint.py /path/to/file.py --format json

# Text output (default, human-readable)
./scripts/lint.py /path/to/file.py --format text
```

### Output Formats

**`--format text`** (default):

```text
✓ ruff file.py: OK
```

or

```text
⚠ ruff file.py: Lint errors!
<detailed output>
```

**`--format json`**:

```json
{
  "file": "/path/to/file.py",
  "toolset": "python",
  "tools_run": ["ruff"],
  "status": "ok",
  "results": [
    {"tool": "ruff", "status": "ok", "output": ""}
  ]
}
```

### Exit Codes

- `0`: Success (file clean or fixed)
- `1`: Lint errors found (non-blocking)
- `2`: Tool execution error

## Project Root Detection

The script finds project root by walking up from the file looking for:

1. `package.json`
2. `pyproject.toml`
3. `Gemfile`
4. `.git` directory

Config detection happens relative to project root.

## Config Detection Details

### Python Tools

| Tool   | Config Files              | pyproject.toml  | INI Files            |
| ------ | ------------------------- | --------------- | -------------------- |
| ruff   | `ruff.toml`, `.ruff.toml` | `[tool.ruff]`   | -                    |
| black  | -                         | `[tool.black]`  | -                    |
| isort  | `.isort.cfg`              | `[tool.isort]`  | `setup.cfg [isort]`  |
| pylint | `.pylintrc`, `pylintrc`   | `[tool.pylint]` | `setup.cfg [pylint]` |

### JavaScript/TypeScript Tools

| Tool     | Config Files                        | package.json             |
| -------- | ----------------------------------- | ------------------------ |
| biome    | `biome.json`, `biome.jsonc`         | `@biomejs/biome` in deps |
| eslint   | `eslint.config.*`, `.eslintrc.*`    | `eslint` in deps         |
| prettier | `.prettierrc*`, `prettier.config.*` | `prettier` in deps       |

### Markdown Tools

| Tool              | Config Files           | Global Fallback              |
| ----------------- | ---------------------- | ---------------------------- |
| markdownlint-cli2 | `.markdownlint-cli2.*` | `~/.markdownlint-cli2.jsonc` |

If no config found, uses skill's `../markdown-quality/default-config.jsonc`.

### Shell Tools

| Tool       | Config Files    |
| ---------- | --------------- |
| shfmt      | `.editorconfig` |
| shellcheck | `.shellcheckrc` |

### Ruby Tools

| Tool     | Config Files                        | Gemfile                                |
| -------- | ----------------------------------- | -------------------------------------- |
| standard | `.standard.yml`                     | `gem "standard"` or `gem "standardrb"` |
| rubocop  | `.rubocop.yml`, `.rubocop_todo.yml` | `gem "rubocop"`                        |

**Tool selection:**

- Standard (zero-config, opinionated) runs `standardrb --fix`
- RuboCop (configurable) runs `rubocop -a` (safe auto-correct only)

### YAML/JSON Tools

| Tool     | Config Files                        | Global Fallback       |
| -------- | ----------------------------------- | --------------------- |
| prettier | `.prettierrc*`, `prettier.config.*` | `~/.prettierrc.json5` |

If no config found, uses skill's `../prettier-quality/default-config.json5`.

**Supported extensions:**

- YAML: `.yaml`, `.yml`
- JSON: `.json`, `.json5`, `.jsonc`

## Integration Patterns

### From Commands

```markdown
Run the linting script:
`${MR_SPARKLE_ROOT}/skills/linting/scripts/lint.py <file_path>`
```

### From Agents

```markdown
For linting results, run:
`<plugin_root>/skills/linting/scripts/lint.py <file> --format json`

Parse the JSON output to understand lint status.
```

### From Hooks (Future)

The script supports `--stdin-hook` mode for hook integration:

```bash
# Reads hook JSON from stdin, outputs hook-compatible JSON
echo '{"tool_input":{"file_path":"/path/to/file.py"}}' | ./lint.py --stdin-hook
```

## Silent Skip Conditions

The script silently exits (code 0, no output) when:

- File doesn't exist
- File extension not recognized
- No tools installed for the detected toolset
- Tool requires config but none found (e.g., markdownlint without config)

## Related Skills

- `markdown-quality` - Interpretive guidance for markdownlint rules
- `prettier-quality` - Interpretive guidance for Prettier (YAML, JSON, JS/TS)
- `python-quality` - Default ruff configuration
- `js-quality` - Default biome configuration
