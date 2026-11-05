---
name: cli-tool-architect
version: 1.0.0
description: Cross-language CLI standards — subcommand structure, flag/env/config/default precedence, TOML in XDG, stdout-data/stderr-logs split, --output json|yaml, exit codes, NO_COLOR, completions. Go (cobra+pflag+viper) and Python (typer) recipes. Use when designing or reviewing a CLI.
---

# CLI Tool Architecture

Language-agnostic conventions for command-line tools. Go-specific recipes use `spf13/cobra` + `spf13/pflag` + `spf13/viper`; Python-specific recipes use `typer`. Per-language stacks are canonical in [go-architect](../../languages/go-architect/SKILL.md) and [python-architect](../../languages/python-architect/SKILL.md). See [STACK.md](STACK.md) for additional CLI-specific libraries (output styling, alternative loggers).

## 1. Command structure

- **Root + subcommands.** `tool <subcommand> [args] [flags]`. Mirrors `git`, `kubectl`, `docker`, `rsk`. Top-level flags are global; subcommand flags are scoped to that subcommand.
- **One verb per subcommand.** `tool create user` is fine. `tool create-user-now` is not.
- **Hierarchy when it reads naturally:** `tool resource action` (e.g. `kubectl get pods`, `aws s3 ls`). Skip if your tool has fewer than ~5 commands — flatten.
- **`tool` alone (no subcommand) prints help.** Never run "the default action" — implicit behavior is the source of surprise commits and accidental deploys.
- **Names: short, lowercase, single-word where possible.** `get`, `list`, `apply`, `delete`. Two words if they're a phrase: `get-config`.

## 2. Arguments vs flags

- **Positional arguments** for the *required noun* of the verb: `tool delete <user-id>`. Use sparingly — every extra positional reduces clarity.
- **Flags** for everything else. Required flags exist; mark them with `Required: true` (cobra) / `Option(...)` (typer) and document explicitly.
- **No more than 2 positional args** in most cases. Beyond that, switch to flags.
- **Short flags only for the top 5 most-used.** `-v`, `-h`, `-f`, `-o`. Don't shortify every flag — `tool deploy -e prod -r us-east-1 -p high -d` becomes unreadable; long form is self-documenting.
- **Boolean flags are pure switches:** `--dry-run`, not `--dry-run=true`. Negate with `--no-foo` if both states need an explicit form.
- **Plural for repeatable flags:** `--tag debug --tag perf` becomes `--tags debug,perf` or `--tag` repeatable. Pick one and document.

## 3. Flag / env / config-file / defaults precedence

Configuration values can come from four places. The order is fixed and inviolable:

```
flag > env var > config file > built-in default
```

- A `--log-level=debug` flag wins over `TOOL_LOG_LEVEL=info` env wins over `log_level = "warn"` in the config wins over the compiled-in default (`info`).
- **Env-var prefix** is the tool name in upper-snake: `TOOL_LOG_LEVEL`, `TOOL_API_URL`. Document the prefix in `--help`.
- **Show effective config**: every CLI should have a `tool config show` (or `tool config --show`) that prints the resolved values *and* where each came from (flag / env / file / default). This is the difference between "user can diagnose" and "user files a bug ticket".

## 4. Configuration file — TOML in XDG location

- **Default format: TOML** — readable, supports comments, modern default (Rust/Cargo, Python `pyproject.toml`, `uv.lock`).
- **Default location: XDG Base Directory spec.**
  - Config: `$XDG_CONFIG_HOME/<tool>/config.toml`, falling back to `~/.config/<tool>/config.toml`
  - Cache: `$XDG_CACHE_HOME/<tool>/`, falling back to `~/.cache/<tool>/`
  - Data: `$XDG_DATA_HOME/<tool>/`, falling back to `~/.local/share/<tool>/`
  - Windows: `%APPDATA%\<tool>\config.toml` (per [XDG-on-Windows convention](https://specifications.freedesktop.org/basedir-spec/latest/) translated to platform).
- **Discovery order for the config file:**
  1. `--config <path>` flag (explicit override)
  2. `TOOL_CONFIG` env var
  3. `./<tool>.toml` (project-local; useful for tools that have per-repo config)
  4. `$XDG_CONFIG_HOME/<tool>/config.toml` (user-global)
- **One canonical filename per tool.** Don't accept `.tool.toml`, `tool.config.toml`, `config.toml`, `.toolrc` all at once. Pick one and stick to it.
- **`tool init`** writes a sane default config to the canonical location; refuse to overwrite without `--force`.

> Note: `rsk` itself uses `~/.config/rsk/config.json` (JSON) for legacy / parsing reasons; TOML is the recommended default for new CLIs.

## 5. Help text discipline

Every command, subcommand, and flag has documented help. Help is the API surface.

- **`tool --help`** lists subcommands with a one-line description each.
- **`tool <subcommand> --help`** has: short description, usage line, flags grouped (Required, Common, Global), and **at least one example** at the bottom.
- **Examples drive understanding** — newcomers read examples before they read flag tables. Include 2–3 realistic invocations per subcommand.
- **Line length 80 chars** in help text — terminals are still ~80 cols by default.
- **No marketing copy.** Short, factual, actionable.

## 6. Output discipline — stdout for data, stderr for logs

**Strict separation.** Always.

- **Data → stdout.** The thing the user wants — JSON, the filename created, the resource ID, the table.
- **Logs, progress, errors → stderr.** Anything the user doesn't want piped into the next command.
- **Errors that prevent producing data must exit non-zero** (see §8). Don't print an error to stdout and exit 0.

Non-negotiable. Tools that mix the streams break every shell pipeline. Concrete pipe examples in [RECIPES § Output discipline](RECIPES.md#output-discipline--stdoutstderr-separation).

## 7. Output formats — `--output json|yaml` mandatory on list/get

Human-readable text is the default. Every command returning structured data must also support `--output json` and `--output yaml`.

- **`-o` short form is standard** (`kubectl`, `gh`, `oc`).
- **JSON output is stable and documented** — clients depend on it. Schema changes are breaking.
- **JSONL for list operations** — one line per record, so `tool list -o json | grep` works.
- **YAML for human eyeballing** of nested data; rarely useful for pipes.

Invocation examples in [RECIPES § Output format flag examples](RECIPES.md#output-format-flag-examples).

## 8. Exit codes

Standard semantics across the ecosystem — full table in [RECIPES § Exit-code reference](RECIPES.md#exit-code-reference). Key rules:

- **`0` success, `1` generic failure, `2` misuse, `130` SIGINT.** Anything custom is domain-specific and documented.
- **Document every non-standard exit code** in `--help` or `tool help exit-codes`.
- **Don't reuse codes** across categories within one tool.
- **Misuse vs failure:** parsing errors are 2; tool worked but operation failed is 1 or a custom non-zero.

## 9. Color & TTY behavior

- **Auto-detect TTY:** color on when stdout is a terminal, off when piped (`tool list | less` should not contain ANSI escapes).
- **Respect `NO_COLOR`** environment variable ([no-color.org](https://no-color.org)). Set → no color, regardless of TTY detection.
- **Respect `--no-color` flag** as an explicit override.
- **Respect `FORCE_COLOR`** when set (CI logs in tools like GitHub Actions render ANSI).
- **`--color=auto|always|never`** for full control (matches `git`, `grep`, `ls`).
- **Don't go wild with color.** A status column (`green: OK`, `red: FAILED`, `yellow: WARN`) is great. Rainbow output is not.

## 10. Logging — structured to stderr

CLI logging is for the user's terminal, not log aggregation. Different style from server logging.

- **Default log level: `info`.** `-v` → `debug`, `-vv` → `trace`. `--quiet` / `-q` → `warn`.
- **Log to stderr always.** No exceptions.
- **Structured output** even for human reading — key=value pairs are scannable. Use `log/slog` (Go) or `structlog` (Python). `charmbracelet/log` (Go) and `rich` (Python) add pretty-printing while preserving structure.
- **Errors include the operation** that failed, the inputs that mattered, and any correlation id if cross-service. Format example in [RECIPES § Error message format](RECIPES.md#error-message-format).
- **No stack traces in user-facing errors** (see §15).

## 11. Progress feedback

For long-running operations only — anything that takes more than ~2 seconds.

- **Spinner** for indeterminate work ("connecting to API...").
- **Progress bar** when total is known ("uploading 1.2 GB / 4 GB").
- **Suppress when not a TTY** — same auto-detection as color. Piping shouldn't fill the output with `\r` overwrites.
- **Don't conflict with log output.** Pause/reposition the spinner when printing a log line, or write progress to a single line that's overwritten in place.
- **Cancellation:** Ctrl-C should immediately stop work, clean up, and exit 130.

## 12. Shell completions

- **Ship completions for bash, zsh, fish, pwsh.** Cobra and typer both generate them — there's no excuse not to.
- **Install command:** `tool completion <shell>` writes the script to stdout; user can pipe to the right location or use the tool's `tool completion install --shell <shell>` if you provide that convenience.
- **Document the one-time install in `--help`** or a `tool help completion` page.

## 13. Versioning

- **`tool --version` and `tool version`** both work; both print the same thing.
- **Output format** is `tool <semver> (rev <sha>, built <date>, <runtime>)` — version + git short SHA + build date + runtime version. The SHA is critical for dev builds. Example in [RECIPES § Version output](RECIPES.md#version-output).
- **Semver always.** Pre-1.0 if the API isn't stable; commit to backward compatibility once you ship 1.0.
- **`tool version --output json`** for scripting.

## 14. Distribution & install

- **Static single binary** as the default delivery (`go build` static; Python via `pyinstaller` or distributed as a `uv tool install` package).
- **Multi-arch:** linux/amd64 + linux/arm64 + darwin/amd64 + darwin/arm64 + windows/amd64 + windows/arm64. Mirrors [docker-architect §5](../../infra/docker-architect/SKILL.md#5-multi-arch-builds).
- **Release artifacts:** signed binaries + checksums + (optional) SBOM. Use `goreleaser` (Go) or equivalent for the release matrix.
- **Package managers, in order of effort/reach:**
  1. Direct binary download from GitHub Releases (always; the universal fallback).
  2. **Homebrew** tap (macOS + Linux).
  3. **Scoop / Winget** (Windows).
  4. Linux package repos (apt, yum) — only when the user base genuinely justifies it.
- **`tool upgrade`** is a nice-to-have — fetches the latest release and replaces the binary. Make it opt-in; never auto-upgrade.

## 15. Error messages

Tell the user what failed, why, and what to try next. Three-line format + structured example in [RECIPES § Error message format](RECIPES.md#error-message-format). Key rules:

- **No stack traces** in user-facing errors. Log them at `debug` level (visible with `-vv`) or write to a file with a correlation id.
- **Suggest the fix** when the cause is unambiguous. `Did you mean: tool depoly → deploy?` (Levenshtein distance from known subcommands).
- **Distinguish user errors from tool bugs.** "Invalid flag value" → user error, exit 2. "Internal: nil pointer in handler" → bug, exit 1 with a "please file an issue" hint.

## 16. Language-specific recipes

Implementation skeletons for **Go (cobra + pflag + viper)** and **Python (typer + rich)** live in [RECIPES.md](RECIPES.md). Canonical per [go-architect §11](../../languages/go-architect/SKILL.md#11-dependencies--logging) and [python-architect §10](../../languages/python-architect/SKILL.md#10-tooling).
