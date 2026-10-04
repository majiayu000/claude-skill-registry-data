---
name: codacy-analysis-cli
description: Uses the Codacy Analysis CLI to run local static analysis on repositories or specific files. Handles installation, initialization, dependency management, dry-runs, and analysis with JSON output. Use whenever the user wants to analyze code locally, run static analysis, scan for bugs or security issues, lint files, check code quality without pushing to Codacy, or run tools like ESLint, Ruff, Semgrep, RuboCop, or any other supported analyzer on their machine. Also trigger when the user asks to analyze staged changes, scan a PR locally, or set up local Codacy analysis.
license: MIT
metadata:
  author: Codacy
  version: 1.4.0
---

# Codacy Analysis CLI

> **Glossary:** See [glossary.md](../../references/glossary.md) for shared definitions of Codacy concepts (issues, findings, severity, coverage, tools, patterns, etc.).

The Codacy Analysis CLI (`codacy-analysis`) runs static analysis locally on a repository. It detects languages, selects tools, and reports issues — without pushing code to Codacy. This is a different tool from the Codacy Cloud CLI (`codacy`), which queries remote Codacy data.

Always use `--output-format json` for structured output in agentic workflows.

## Setup

```bash
# Install
npm i -g @codacy/analysis-cli

# Verify
codacy-analysis --help
```

### Authentication (optional)

Authentication is only required for `init --remote` (fetching config from a Codacy repository). Local analysis works without authentication.

```bash
# Option 1: Interactive login
codacy-analysis login

# Option 2: Token flag
codacy-analysis login --token <your-api-token>

# Option 3: Environment variable
export CODACY_API_TOKEN=<your-api-token>

# Obtain tokens: Codacy > My Account > Access Management
# Remove credentials
codacy-analysis logout
```

**Shared session:** The Analysis CLI and the Cloud CLI (`codacy`) share the same credentials at `~/.codacy/credentials`. Logging in or out with either CLI applies to both — there is no need to authenticate separately.

## Getting help

```bash
codacy-analysis --help
codacy-analysis <command> --help
# e.g. codacy-analysis analyze --help
```

## Filesystem conventions

The CLI uses two managed locations:

| Location | Scope | Contents |
|----------|-------|----------|
| `.codacy/` (in repo root) | Per-project | `codacy.config.json`, `generated/` (tool configs), `.gitignore` (auto-created) |
| `~/.codacy/` (home dir) | Machine-wide | Runtimes, tool binaries, caches, logs, credentials |

The analyzed repository is **never modified outside of `.codacy/`**. The `.codacy/.gitignore` is auto-created to exclude `generated/`, logs, and other transient files.

### Key files

- `.codacy/codacy.config.json` — Main configuration: tools, patterns, excludes, metadata. See [references/config-format.md](references/config-format.md) for the full schema
- `.codacy/generated/<ToolId>/` — Materialized tool-specific configs (gitignored)
- `~/.codacy/credentials` — Stored API token
- `~/.codacy/logs/` — Structured logs (JSON lines, rotated at 10 MB)

## Provider values

Used with `init --remote`. See the [Provider section in the glossary](../../references/glossary.md#provider) for the full table of CLI values (`gh`, `gl`, `bb`).

## Analysis workflow

```
Analysis Progress:
- [ ] Step 1: Initialize configuration
- [ ] Step 2: Inspect tool availability (dry-run)
- [ ] Step 3: Install missing dependencies
- [ ] Step 4: Run analysis
- [ ] Step 5: Interpret results
```

### Step 1: Initialize configuration

Choose the init mode based on the repository's situation:

**Repository is in Codacy and you want its exact config:**
```bash
# Requires authentication (login or CODACY_API_TOKEN)
codacy-analysis init --remote <provider> <org> <repo>
# e.g. codacy-analysis init --remote gh my-org my-repo
```

**Repository is in Codacy but you just want sensible defaults:**
```bash
# No token needed — uses the public Codacy API for default patterns
codacy-analysis init --default
```

**Broad auto-tuned initialization (maximum pattern coverage):**
```bash
# Initializes with all patterns matching the given severity/category filter
codacy-analysis init --auto "AllCritical,High,Warning,Minor,AllSecurity,ErrorProne,Performance,BestPractice,UnusedCode,Compatibility,Complexity,Comprehensibility,CodeStyle,Documentation"
```

The `--auto` flag selects patterns broadly based on a comma-separated filter of severities and categories. Use this when you want to start with maximum coverage and then trim noise using analysis data.

**Repository is not in Codacy (local-only analysis):**
```bash
# Detects languages and tools based on local files and config
codacy-analysis init
```

**A specific directory (not the current one):**
```bash
codacy-analysis init /path/to/repo
```

All modes create `.codacy/codacy.config.json` in the repo root (or the file passed to `--config-file`, see [Working with alternative configuration files](#working-with-alternative-configuration-files)). If a `.codacy.yaml` (or `.codacy.yml`) exists, its `exclude_paths` are automatically merged into the config.

#### Updating an existing configuration

When the config was initialized with `--remote` and you want to re-sync with the remote Codacy configuration:

```bash
codacy-analysis update-config
```

This re-fetches the configuration from the same Codacy repository used during init.

**Only use `update-config` with `--remote` configs.** For configs initialized with `--default` or bare `init`, `update-config` re-runs the original init mode, which would overwrite any manual changes you've made to the config file.

#### Working with alternative configuration files

By default every command reads and writes `.codacy/codacy.config.json`. Pass `--config-file <path>` to `init`, `analyze`, and `update-config` to use a different file. This lets you keep several configurations side by side and **test them in parallel** without overwriting the main config:

```bash
# Create an alternative, broadly-tuned config in a separate file
codacy-analysis init --auto AllCritical,AllSecurity --config-file .codacy/auto-config.json

# Analyze using that config instead of the default
codacy-analysis analyze --config-file .codacy/auto-config.json --output-format json

# Regenerate it later using its original init mode (the mode is stored in the file)
codacy-analysis update-config --config-file .codacy/auto-config.json
```

`--config-file` is honored by `init` (where to create the config), `analyze` (which config to run with), and `update-config` (which config to regenerate). It defaults to `.codacy/codacy.config.json` everywhere.

#### Combining configuration files (`config` command)

The `config` command performs set operations on two config files, combining their tools and patterns. Use it to reconcile experimental configs with a baseline:

```bash
# Merge — union of tools/patterns from source into dest
codacy-analysis config --merge --source .codacy/extra.json

# Intersect — keep only tools/patterns present in BOTH files
codacy-analysis config --intersect --source a.json --dest b.json

# Diff — keep tools/patterns in dest that are NOT in source (dest − source)
codacy-analysis config --diff --source baseline.json --dest .codacy/codacy.config.json
```

- Exactly **one** of `--merge`, `--intersect`, `--diff` is required.
- `--source <path>` is **read-only** (default `.codacy/codacy.config.json`); `--dest <path>` is **overwritten** with the result (default `.codacy/codacy.config.json`).
- At least one of `--source` / `--dest` must be provided — they cannot both fall back to the same default file.

**`--dest` is overwritten in place.** Point it at a throwaway file (or back up the original first) if you need to preserve the destination config.

#### Discovering the repository stack

Use `discover` to auto-detect the repository's languages, frameworks, and libraries before initialization:

```bash
codacy-analysis discover --output-format json --output /tmp/codacy-discover.json
```

The output lists detected languages, frameworks, and the tools that apply. Use this to inform which tools and patterns to enable.

#### Listing supported tools

Use `info` to see which tools are available in the local Analysis CLI:

```bash
codacy-analysis info
```

This lists all tools the CLI can run locally. Compare against tools enabled in Codacy Cloud to identify cloud-only tools that the local CLI cannot run.

### Step 2: Inspect tool availability (dry-run)

Before running analysis, check which tools are available and which are missing:

```bash
codacy-analysis analyze --inspect --output-format json
```

This produces a capability report without running any analysis. Parse the JSON output:

```bash
# See which tools are ready
codacy-analysis analyze --inspect --output-format json | jq '.capability.ready[] | {toolId, version, installation}'

# See which tools are missing and how to fix them
codacy-analysis analyze --inspect --output-format json | jq '.capability.unavailable[] | {toolId, reason, remediation}'
```

**Important:** `--inspect` and `--install-dependencies` are mutually exclusive. Use `--inspect` first to check readiness, then `--install-dependencies` to install and run in a single step.

**Decision point:**
- If all needed tools are in `capability.ready` → skip to Step 4
- If tools are in `capability.unavailable` → proceed to Step 3

### Step 3: Install missing dependencies

**Preferred: use `--install-dependencies`** — installs tools into the `.codacy/` / `~/.codacy/` scope without affecting the rest of the machine:

```bash
codacy-analysis analyze --install-dependencies --output-format json
```

This installs missing tools and then runs analysis in a single command. The installed binaries go to `~/.codacy/` (machine-scoped, reused across repositories).

**Last resort: manual installation** — if `--install-dependencies` fails for a specific tool, install it manually on the machine (e.g., `brew install shellcheck`, `pip install ruff`). See [references/supported-tools.md](references/supported-tools.md) for tool details.

### Step 4: Run analysis

Always use `--output-format json` for agentic workflows.

#### Analyze the entire repository

```bash
codacy-analysis analyze --output-format json
```

#### Analyze specific files or paths

```bash
# Single file (positional argument)
codacy-analysis analyze ./src/main.py --output-format json

# Multiple files by path or glob (--files flag)
codacy-analysis analyze --files src/a.py src/b.py --output-format json

# Glob pattern (always quote to prevent shell expansion)
codacy-analysis analyze --files "src/**/*.ts" --output-format json

# Subdirectory
codacy-analysis analyze ./src/api/ --output-format json
```

#### Restrict to specific tools

Tool IDs are **case-sensitive**. See [references/supported-tools.md](references/supported-tools.md) for the full list.

```bash
# Single tool
codacy-analysis analyze --tool Ruff --output-format json

# Multiple tools
codacy-analysis analyze --tool Ruff --tool Bandit --output-format json

# Combine with file targeting
codacy-analysis analyze --tool ESLint9 --files "src/**/*.ts" --output-format json
```

#### Run with an alternative configuration file

By default `analyze` reads `.codacy/codacy.config.json`. Pass `--config-file <path>` to run with a different config — useful for comparing configurations side by side (see [Working with alternative configuration files](#working-with-alternative-configuration-files)):

```bash
codacy-analysis analyze --config-file .codacy/auto-config.json --output-format json
```

#### Git-aware scoping

Analyze only the code that changed, instead of the full repository:

```bash
# Only files staged for commit
codacy-analysis analyze --staged --output-format json

# Changes relative to the current branch's merge base (uncommitted + committed)
codacy-analysis analyze --diff --output-format json

# Changes in a pull request (compares against the PR's target branch)
codacy-analysis analyze --pr --output-format json
```

These flags work with `--tool`, `--files`, and all other analyze options. When combined with `--files`, the intersection is used (files that match both the git scope and the file filter).

#### Performance tuning

```bash
# Run up to 4 tools in parallel
codacy-analysis analyze --parallel-tools 4 --output-format json

# Increase timeout for slow tools (default: 600000ms = 10 min)
codacy-analysis analyze --tool-timeout 600000 --output-format json
```

#### Strict mode

Fail immediately if any configured tool is unavailable (instead of skipping it):

```bash
codacy-analysis analyze --fail-if-missing --output-format json
```

#### Save output to file

```bash
codacy-analysis analyze --output-format json --output results.json
```

#### Debugging

```bash
# Verbose logging to stderr
codacy-analysis analyze --log-level debug --output-format json

# Disable log file writing (e.g., in CI)
codacy-analysis analyze --no-log --output-format json
```

### Step 5: Interpret results

The JSON output contains the full `AnalysisResult`. See [references/output-format.md](references/output-format.md) for the complete schema.

**Quick reference for parsing:**

```bash
# Count issues by severity
codacy-analysis analyze --output-format json | jq '.issues | group_by(.severity) | map({severity: .[0].severity, count: length})'

# Get critical/high issues only
codacy-analysis analyze --output-format json | jq '[.issues[] | select(.severity == "Error" or .severity == "High")]'

# Issues grouped by file
codacy-analysis analyze --output-format json | jq '.issues | group_by(.filePath) | map({file: .[0].filePath, count: length})'

# Check for tool errors
codacy-analysis analyze --output-format json | jq '.errors'

# Per-tool summary
codacy-analysis analyze --output-format json | jq '.toolResults | map({toolId, status, issueCount, durationMs})'
```

**Exit codes:**
- `0` — Success, no issues found
- `1` — Issues found
- `2` — Execution error (tool crash, missing dependency, etc.)

## Common workflows

### Quick scan of a repository not in Codacy

```bash
codacy-analysis init
codacy-analysis analyze --install-dependencies --output-format json
```

### Scan only changed files (e.g., before a commit)

```bash
# Staged files only (pre-commit check)
codacy-analysis analyze --staged --output-format json

# All changes on the current branch
codacy-analysis analyze --diff --output-format json

# Changes in a pull request
codacy-analysis analyze --pr --output-format json
```

### Reproduce Codacy remote analysis locally

```bash
codacy-analysis login --token <token>
codacy-analysis init --remote gh my-org my-repo
codacy-analysis analyze --install-dependencies --output-format json
```

### Check a single file for issues

```bash
codacy-analysis analyze ./src/main.py --output-format json
```

### Re-scan after configuration changes

```bash
codacy-analysis update-config
codacy-analysis analyze --output-format json
```

### Test two configurations side by side

```bash
# Baseline config (default location) plus an experimental, broader config
codacy-analysis init
codacy-analysis init --auto AllCritical,AllSecurity --config-file .codacy/experimental.json

# Run each independently and compare the results
codacy-analysis analyze --output-format json --output baseline-results.json
codacy-analysis analyze --config-file .codacy/experimental.json --output-format json --output experimental-results.json

# Promote the extra tools/patterns from the experiment into the baseline
codacy-analysis config --merge --source .codacy/experimental.json --dest .codacy/codacy.config.json
```

### Run only security-focused tools

```bash
codacy-analysis analyze --tool Bandit --tool Brakeman --tool Trivy --tool Semgrep --tool Checkov --output-format json
```

### Analyze a Ruby project

```bash
codacy-analysis analyze --tool RuboCop --tool Reek --tool Brakeman --output-format json
```

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| `Tool X not found` / tool in `unavailable` | Tool binary not installed | Run with `--install-dependencies`; if that fails, install the tool manually |
| Analysis produces no results | No tools enabled or no matching files | Re-run `codacy-analysis init` or check `.codacy/codacy.config.json` has tools configured |
| Wrong tools detected | Language detection missed files | Use `--tool <id>` to force specific tools |
| Tool timeout | Analysis takes too long on large codebase | Increase `--tool-timeout <ms>` (default 600000) |
| Config outdated after adding new languages | Init was run before new files existed | Run `codacy-analysis update-config` |
| `Config already exists` on init | `.codacy/codacy.config.json` already present | Use `update-config` instead, or delete `.codacy/codacy.config.json` first |
| Remote init fails with auth error | Missing or invalid API token | Run `codacy-analysis login` or set `CODACY_API_TOKEN` |
| Permission errors on `~/.codacy/` | Directory ownership mismatch | Check permissions: `ls -la ~/.codacy/` |
| Inspect shows tool as `bundled` but it fails | Bundled library tool has dependency issue | Check `--log-level debug` output; may need `npm rebuild` |
| Different results than Codacy Cloud | Different tool versions or pattern config | Use `init --remote` to sync config; check tool versions in inspect output |

### Reading logs

Logs are written to `~/.codacy/logs/` in JSON lines format:

```bash
# View latest log
cat ~/.codacy/logs/*.log | jq .

# Filter for errors
cat ~/.codacy/logs/*.log | jq 'select(.level == "error")'
```

Use `--log-level debug` for the most verbose output when troubleshooting tool issues.
