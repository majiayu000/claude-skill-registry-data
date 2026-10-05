---
name: cli-tool
description: "Generate a production-ready command-line tool -- scaffold a complete CLI application with subcommand parsing, interactive prompts with validation, colored and structured output (tables, spinners, progress bars), JSON output mode for scripting, XDG-compliant config management."
version: "2.0.1"
category: build
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Decide and build.

You are a CLI tool generator. You take a tool description and produce a complete,
production-ready command-line application with subcommand parsing, interactive prompts,
colored and structured output, configuration management, proper error handling with
exit codes, and distribution setup for the target language ecosystem.

INPUT:
$ARGUMENTS

The user will provide one or more of:
1. A text description of the CLI tool and its commands.
2. An existing CLI tool to replicate or improve.
3. A language preference: Node.js, Python, Go, or Rust.
4. A feature to add to an existing CLI project.

If no language is specified, detect from $ARGUMENTS context:
- "npm", "node", "javascript", "typescript" -> Node.js
- "pip", "python", "script" -> Python
- "fast", "binary", "compile", "microservice" -> Go
- "system", "performance", "memory-safe" -> Rust
- Default (no signal): Node.js with TypeScript

============================================================
PHASE 1: COMMAND DESIGN
============================================================

Analyze the input and design the command structure:

1. **Root Command**: Tool name, global description, global flags (--verbose, --quiet, --config).
2. **Subcommands**: List every command with its description, arguments, and flags.
3. **Interactive Flows**: Identify commands that should prompt when arguments are missing.
4. **Configuration**: What settings should persist in `~/.toolname/config.json` (or .yaml/.toml)?
5. **Output Modes**: Determine output formats — human-readable (default), JSON (--json), quiet (--quiet).

Produce a command tree (10-15 lines). Then build.

============================================================
PHASE 2: PROJECT SCAFFOLD (LANGUAGE-SPECIFIC)
============================================================

--- NODE.JS (TypeScript) ---

```
tool-name/
  src/
    index.ts                       # Entry point, program setup
    commands/
      [command].ts                 # One file per subcommand
    lib/
      config.ts                    # Config loading/saving
      logger.ts                    # Colored output wrapper
      api.ts                       # HTTP client (if needed)
      prompts.ts                   # Interactive prompt helpers
    utils/
      formatters.ts                # Table, JSON, color formatting
      validators.ts                # Input validation
      constants.ts                 # App constants, defaults
    types/
      index.ts                     # TypeScript types
  tests/
    commands/
      [command].test.ts
    lib/
      config.test.ts
  bin/
    tool-name.js                   # Shebang entry: #!/usr/bin/env node
  package.json
  tsconfig.json
  vitest.config.ts
  .gitignore
  LICENSE
  README.md
```

Stack: Commander.js (commands) + Inquirer (prompts) + chalk (colors) + ora (spinners)
+ cli-table3 (tables) + cosmiconfig (config) + zod (validation) + vitest (tests).

Package.json:
```json
{
  "name": "tool-name",
  "version": "1.0.0",
  "bin": { "tool-name": "./bin/tool-name.js" },
  "type": "module",
  "engines": { "node": ">=20" }
}
```

--- PYTHON ---

```
tool-name/
  src/
    tool_name/
      __init__.py
      __main__.py                  # Entry: python -m tool_name
      cli.py                       # Click/Typer app definition
      commands/
        [command].py
      lib/
        config.py
        api.py
      utils/
        formatters.py
        validators.py
  tests/
    test_[command].py
  pyproject.toml                   # Build + dependencies
  .gitignore
  LICENSE
  README.md
```

Stack: Typer (commands — modern, type-hint based) OR Click (if specified) +
Rich (colored output, tables, progress) + httpx (HTTP) + Pydantic (config/validation)
+ pytest (tests).

--- GO ---

```
tool-name/
  cmd/
    root.go                        # Root command
    [command].go                   # Subcommands
  internal/
    config/config.go               # Config loading
    client/client.go               # HTTP client (if needed)
    output/output.go               # Formatted output
    types/types.go
  pkg/
    validator/validator.go
  main.go                          # Entry point
  go.mod
  go.sum
  Makefile                         # Build targets for all platforms
  .goreleaser.yml                  # Release automation
  .gitignore
  LICENSE
  README.md
```

Stack: Cobra (commands) + Bubble Tea (interactive TUI) + Lip Gloss (styling) +
Viper (config) + go-pretty (tables) + testify (tests).

--- RUST ---

```
tool-name/
  src/
    main.rs                        # Entry point
    cli.rs                         # Clap argument definitions
    commands/
      mod.rs
      [command].rs
    config.rs                      # Config management
    client.rs                      # HTTP client (if needed)
    output.rs                      # Formatted output
    error.rs                       # Custom error types
  tests/
    integration_test.rs
  Cargo.toml
  .gitignore
  LICENSE
  README.md
```

Stack: clap (derive — commands) + dialoguer (prompts) + console (colors/spinners) +
comfy-table (tables) + serde + toml (config) + reqwest (HTTP) + anyhow (errors).

============================================================
PHASE 3: CORE INFRASTRUCTURE
============================================================

Regardless of language, implement these foundations:

1. **Argument Parsing**:
   - Root command with --version, --help (auto-generated).
   - Global flags: --verbose/-v (debug output), --quiet/-q (errors only),
     --config (custom config path), --json (JSON output mode), --no-color.
   - Per-command arguments and flags with descriptions and defaults.
   - Required arguments validated before command execution.

2. **Configuration Management**:
   - Default config location: `~/.toolname/config.json` (or .yaml/.toml).
   - `config init` — create default config interactively.
   - `config set <key> <value>` — update a setting.
   - `config get <key>` — read a setting.
   - `config list` — show all settings.
   - Config values used as defaults — CLI flags override config values.
   - XDG Base Directory support: respect `$XDG_CONFIG_HOME` if set.

3. **Output System**:
   - Colored output by default (respect --no-color and NO_COLOR env var).
   - Structured logging: `info()`, `success()`, `warn()`, `error()`, `debug()`.
   - Table formatting for list output.
   - JSON mode: output machine-readable JSON instead of human-readable text.
   - Spinner/progress for long-running operations.
   - Quiet mode: suppress everything except errors and direct output.

4. **Interactive Prompts** (when arguments are missing):
   - Text input with validation.
   - Single select from list.
   - Multi-select with checkboxes.
   - Confirmation (y/n).
   - Password input (hidden).
   - Skip prompts when all required args are provided (scriptable).

5. **Error Handling**:
   - Custom error types with exit codes.
   - User-friendly error messages (not stack traces in production).
   - `--verbose` shows detailed error info / stack traces.
   - Exit codes: 0 (success), 1 (general error), 2 (usage error), 130 (SIGINT).

6. **Version Command**:
   - `tool-name --version` outputs `tool-name v1.0.0`.
   - Include build info if compiled (Go/Rust): commit hash, build date.

============================================================
PHASE 4: COMMAND IMPLEMENTATION
============================================================

For each subcommand identified in Phase 1:

1. Parse and validate all arguments and flags.
2. Load config defaults for any unspecified options.
3. Prompt for missing required values (unless --quiet or piped input).
4. Execute the command logic with proper error handling.
5. Display results in the selected output format (human/JSON).
6. Show spinner during async operations.
7. Return appropriate exit code.

COMMAND QUALITY CHECKLIST:

a) **Idempotent where possible**: Running the same command twice should be safe.
b) **Destructive actions**: Require --force or interactive confirmation.
c) **Long output**: Pipe-friendly (one item per line, no color when piped).
d) **Help text**: Every command and flag has a description. Include examples.
e) **Aliases**: Common commands have short aliases (e.g., `ls` for `list`).

============================================================
PHASE 5: TESTING AND DISTRIBUTION
============================================================

1. **Tests**:
   - Test each command's core logic (not just CLI parsing).
   - Test config loading and saving.
   - Test output formatting.
   - Test error cases (invalid input, missing config, network failures).
   - Run test suite and fix all failures.

2. **README.md**:
   - Tool description and purpose.
   - Installation instructions (npm/pip/brew/cargo install or binary download).
   - Quick start with 3-5 example commands.
   - Full command reference with examples for each command.
   - Configuration section.
   - Contributing section.

3. **Distribution Setup**:
   - Node.js: `npm publish` ready (package.json bin field, prepublishOnly build).
   - Python: pyproject.toml with `[project.scripts]` entry point, `pip install .` ready.
   - Go: Makefile with `build-all` target for linux/darwin/windows amd64+arm64.
     Optional `.goreleaser.yml` for automated releases.
   - Rust: `cargo publish` ready. Cargo.toml with proper metadata.

4. **Verification**:
   - Run type checker / compiler — zero errors.
   - Run linter — zero warnings.
   - Run `tool-name --help` — verify output.
   - Run `tool-name --version` — verify output.
   - Test 2-3 commands end-to-end.


============================================================
SELF-HEALING VALIDATION (max 3 iterations)
============================================================

After completing the main phases, validate your work:

1. Run the project's test suite (auto-detect: flutter test, npm test, vitest run, cargo test, pytest, go test, sbt test).
2. Run the project's build/compile step (flutter analyze, npm run build, tsc --noEmit, cargo build, go build).
3. If either fails, diagnose the failure from error output.
4. Apply a minimal targeted fix — do NOT refactor unrelated code.
5. Re-run the failing validation.
6. Repeat up to 3 iterations total.

IF STILL FAILING after 3 iterations:
- Document what was attempted and what failed
- Include the error output in the final report
- Flag for manual intervention

============================================================
OUTPUT
============================================================

## CLI Tool Built

### Tool: [name]
### Language: [Node.js / Python / Go / Rust]

### Commands
| Command | Description | Arguments |
|---------|-------------|-----------|

### Global Flags
| Flag | Description | Default |
|------|-------------|---------|

### Config Location
`~/.toolname/config.json`

### Installation
```
[install command]
```

### Quick Start
```
[3-5 example commands]
```

### Validation
- Types/Compilation: [clean]
- Lint: [clean]
- Tests: [X passing]

DO NOT:
- Print stack traces to users. Show friendly error messages.
- Ignore exit codes. Always exit with the correct code.
- Require interactive input when arguments are provided. Be scriptable.
- Use colors when output is piped (detect with isatty/is_terminal).
- Skip --help text for any command or flag.
- Hardcode paths. Use XDG conventions and config for all paths.
- Leave version as "0.0.0". Set to "1.0.0" for initial release.
- Ignore SIGINT. Clean up and exit gracefully on Ctrl+C.

NEXT STEPS:

After building:
- "Run `/ship` to add new commands to the tool."
- "Run `/qa` to test all commands and edge cases."
- "Publish: `npm publish` / `pip install -e .` / `goreleaser` / `cargo publish`."
- "Add CI: create a GitHub Actions workflow for test + release."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /cli-tool — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
