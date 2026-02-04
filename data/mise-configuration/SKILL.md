---
name: mise-configuration
description: Configure environment via mise [env] SSoT. TRIGGERS - mise env, mise.toml, environment variables, centralize config, Python venv, mise templates.
allowed-tools: Read, Bash, Glob, Grep, Edit, Write
---

# mise Configuration as Single Source of Truth

Use mise `[env]` as centralized configuration with backward-compatible defaults.

## Core Principle

Define all configurable values in `.mise.toml` `[env]` section. Scripts read via environment variables with fallback defaults. Same code path works WITH or WITHOUT mise installed.

**Key insight**: mise auto-loads `[env]` values when shell has `mise activate` configured. Scripts using `os.environ.get("VAR", "default")` pattern work identically whether mise is present or not.

## Quick Reference

### Language Patterns

| Language   | Pattern                            | Notes                       |
| ---------- | ---------------------------------- | --------------------------- |
| Python     | `os.environ.get("VAR", "default")` | Returns string, cast if int |
| Bash       | `${VAR:-default}`                  | Standard POSIX expansion    |
| JavaScript | `process.env.VAR \|\| "default"`   | Falsy check, watch for "0"  |
| Go         | `os.Getenv("VAR")` with default    | Empty string if unset       |
| Rust       | `std::env::var("VAR").unwrap_or()` | Returns Result<String>      |

### Special Directives

| Directive       | Purpose                 | Example                                             |
| --------------- | ----------------------- | --------------------------------------------------- |
| `_.file`        | Load from .env files    | `_.file = ".env"`                                   |
| `_.path`        | Extend PATH             | `_.path = ["bin", "node_modules/.bin"]`             |
| `_.source`      | Execute bash scripts    | `_.source = "./scripts/env.sh"`                     |
| `_.python.venv` | Auto-create Python venv | `_.python.venv = { path = ".venv", create = true }` |

## Python Venv Auto-Creation (Critical)

Auto-create and activate Python virtual environments:

```toml
[env]
_.python.venv = { path = ".venv", create = true }
```

This pattern is used in ALL projects. When entering the directory with mise activated:

1. Creates `.venv` if it doesn't exist
2. Activates the venv automatically
3. Works with `uv` for fast venv creation

**Alternative via [settings]**:

```toml
[settings]
python.uv_venv_auto = true
```

## Special Directives

### Load from .env Files (`_.file`)

```toml
[env]
# Single file
_.file = ".env"

# Multiple files with options
_.file = [
    ".env",
    { path = ".env.secrets", redact = true }
]
```

### Extend PATH (`_.path`)

```toml
[env]
_.path = [
    "{{config_root}}/bin",
    "{{config_root}}/node_modules/.bin",
    "scripts"
]
```

### Source Bash Scripts (`_.source`)

```toml
[env]
_.source = "./scripts/env.sh"
_.source = { path = ".secrets.sh", redact = true }
```

### Lazy Evaluation (`tools = true`)

By default, env vars resolve BEFORE tools install. Use `tools = true` to access tool-generated paths:

```toml
[env]
# Access PATH after tools are set up
GEM_BIN = { value = "{{env.GEM_HOME}}/bin", tools = true }

# Load .env files after tool setup
_.file = { path = ".env", tools = true }
```

## Template Syntax (Tera)

mise uses Tera templating. Delimiters: `{{ }}` expressions, `{% %}` statements, `{# #}` comments.

### Built-in Variables

| Variable              | Description                     |
| --------------------- | ------------------------------- |
| `{{config_root}}`     | Directory containing .mise.toml |
| `{{cwd}}`             | Current working directory       |
| `{{env.VAR}}`         | Environment variable            |
| `{{mise_bin}}`        | Path to mise binary             |
| `{{mise_pid}}`        | mise process ID                 |
| `{{xdg_cache_home}}`  | XDG cache directory             |
| `{{xdg_config_home}}` | XDG config directory            |
| `{{xdg_data_home}}`   | XDG data directory              |

### Functions

```toml
[env]
# Get env var with fallback
NODE_VER = "{{ get_env(name='NODE_VERSION', default='20') }}"

# Execute shell command
TIMESTAMP = "{{ exec(command='date +%Y-%m-%d') }}"

# System info
ARCH = "{{ arch() }}"      # x64, arm64
OS = "{{ os() }}"          # linux, macos, windows
CPUS = "{{ num_cpus() }}"

# File operations
VERSION = "{{ read_file(path='VERSION') | trim }}"
HASH = "{{ hash_file(path='config.json', len=8) }}"
```

### Filters

```toml
[env]
# Case conversion
SNAKE = "{{ name | snakecase }}"
KEBAB = "{{ name | kebabcase }}"
CAMEL = "{{ name | lowercamelcase }}"

# String manipulation
TRIMMED = "{{ text | trim }}"
UPPER = "{{ text | upper }}"
REPLACED = "{{ text | replace(from='old', to='new') }}"

# Path operations
ABSOLUTE = "{{ path | absolute }}"
BASENAME = "{{ path | basename }}"
DIRNAME = "{{ path | dirname }}"
```

### Conditionals

```toml
[env]
{% if env.DEBUG %}
LOG_LEVEL = "debug"
{% else %}
LOG_LEVEL = "info"
{% endif %}
```

## Required & Redacted Variables

### Required Variables

Enforce variable definition with helpful messages:

```toml
[env]
DATABASE_URL = { required = true }
API_KEY = { required = "Get from https://example.com/api-keys" }
```

### Redacted Variables

Hide sensitive values from output:

```toml
[env]
SECRET = { value = "my_secret", redact = true }
_.file = { path = ".env.secrets", redact = true }

# Pattern-based redactions
redactions = ["*_TOKEN", "*_KEY", "PASSWORD"]
```

## [settings] Section

```toml
[settings]
experimental = true              # Enable experimental features
python.uv_venv_auto = true       # Auto-create venv with uv
```

## [tools] Version Pinning

Pin tool versions for reproducibility:

```toml
[tools]
python = "3.11"  # minimum baseline; use 3.12, 3.13 as needed
node = "latest"
uv = "latest"

# With options
rust = { version = "1.75", profile = "minimal" }
```

**min_version**: Enforce mise version compatibility:

```toml
min_version = "2024.9.5"
```

## Implementation Steps

1. **Identify hardcoded values** - timeouts, paths, thresholds, feature flags
2. **Create `.mise.toml`** - add `[env]` section with documented variables
3. **Add venv auto-creation** - `_.python.venv = { path = ".venv", create = true }`
4. **Update scripts** - use env vars with original values as defaults
5. **Add ADR reference** - comment: `# ADR: 2025-12-08-mise-env-centralized-config`
6. **Test without mise** - verify script works using defaults
7. **Test with mise** - verify activated shell uses `.mise.toml` values

## GitHub Token Multi-Account Patterns (MANDATORY for Multi-Account Setups) {#github-token-multi-account-patterns}

For multi-account GitHub setups, mise `[env]` provides per-directory token configuration that overrides gh CLI's global authentication.

### Token Storage

Store tokens in a centralized, secure location:

```bash
mkdir -p ~/.claude/.secrets
chmod 700 ~/.claude/.secrets

# Create token files (one per account)
gh auth login  # authenticate as account
gh auth token > ~/.claude/.secrets/gh-token-accountname
chmod 600 ~/.claude/.secrets/gh-token-*
```

### Per-Directory Configuration

```toml
# ~/.claude/.mise.toml (terrylica account)
[env]
GH_TOKEN = "{{ read_file(path=config_root ~ '/.secrets/gh-token-terrylica') | trim }}"
GITHUB_TOKEN = "{{ read_file(path=config_root ~ '/.secrets/gh-token-terrylica') | trim }}"
GH_ACCOUNT = "terrylica"  # For human reference only
```

```toml
# ~/eon/.mise.toml (terrylica account - different directory)
[env]
GH_TOKEN = "{{ read_file(path=env.HOME ~ '/.claude/.secrets/gh-token-terrylica') | trim }}"
GITHUB_TOKEN = "{{ read_file(path=env.HOME ~ '/.claude/.secrets/gh-token-terrylica') | trim }}"
GH_ACCOUNT = "terrylica"
```

### Variable Naming Convention

| Variable       | Usage Context                                 | Example                     |
| -------------- | --------------------------------------------- | --------------------------- |
| `GH_TOKEN`     | mise [env], Doppler, verification tasks       | `.mise.toml`, shell scripts |
| `GITHUB_TOKEN` | npm scripts, GitHub Actions, semantic-release | `package.json`, workflows   |

**Rule**: Always set BOTH variables in mise [env] pointing to the same token file. Different tools check different variable names.

### Alternative: 1Password Integration

For enhanced security with automatic token rotation:

```toml
[env]
GH_TOKEN = "{{ op_read('op://Engineering/GitHub Token/credential') }}"
```

With caching for performance:

```toml
[env]
GH_TOKEN = "{{ cache(key='gh_token', duration='1h', run='op read op://Engineering/GitHub Token/credential') }}"
```

### Verification

```bash
/usr/bin/env bash << 'MISE_EOF'
for dir in ~/.claude ~/eon ~/own ~/scripts ~/459ecs; do
  cd "$dir" && eval "$(mise hook-env -s bash)" && echo "$dir → $GH_ACCOUNT"
done
MISE_EOF
```

**ADR Reference**: [GitHub Multi-Account Authentication](https://github.com/terrylica/claude-config/blob/main/docs/adr/2025-12-17-github-multi-account-authentication.md)

> **SSH ControlMaster Warning**: If using multi-account SSH, ensure `ControlMaster no` is set for GitHub hosts in `~/.ssh/config`. Cached connections can authenticate with the wrong account. See [semantic-release authentication](../semantic-release/references/authentication.md#controlmaster-cache-issues) for troubleshooting.

## Anti-Patterns

| Anti-Pattern                | Why                    | Instead                                    |
| --------------------------- | ---------------------- | ------------------------------------------ |
| `mise exec -- script.py`    | Forces mise dependency | Use env vars with defaults                 |
| Secrets in `.mise.toml`     | Visible in repo        | Use Doppler or `redact = true`             |
| No defaults in scripts      | Breaks without mise    | Always provide fallback                    |
| Mixing env/tools resolution | Order matters          | Use `tools = true` for tool-dependent vars |

## Task Orchestration Integration

When you detect **workflow opportunities** during mise configuration, prescriptively invoke the `mise-tasks` skill.

### Detection Triggers

- Multi-step workflows (test + build + deploy)
- Repeatable project commands (lint, format, release)
- Dependency chains (db-migrate depends on db-init)
- File-tracked builds (sources/outputs caching)

### Prescriptive AI Reminder

> **PRESCRIPTIVE**: When detecting multi-step project workflows, **invoke [`mise-tasks` skill](../mise-tasks/SKILL.md)** to generate appropriate `[tasks]` definitions with dependency management.

### Example: From Environment to Tasks

**Step 1**: Configure environment (this skill):

```toml
[env]
DATABASE_URL = "postgresql://localhost/mydb"
_.python.venv = { path = ".venv", create = true }
```

**Step 2**: Define tasks (`mise-tasks` skill):

```toml
[tasks.test]
depends = ["lint"]
run = "pytest tests/"

[tasks.deploy]
depends = ["test", "build"]
run = "deploy.sh"
```

Tasks automatically inherit `[env]` values.

---

## Additional Resources

For complete code patterns and examples, see: **[`references/patterns.md`](./references/patterns.md)**

**For task orchestration**, see: **[`mise-tasks` skill](../mise-tasks/SKILL.md)** - Dependencies, arguments, file tracking, watch mode

**ADR Reference**: When implementing mise configuration, create an ADR at `docs/adr/YYYY-MM-DD-mise-env-centralized-config.md` in your project.
