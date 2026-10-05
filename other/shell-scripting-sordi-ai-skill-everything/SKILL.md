---
name: shell-scripting
description: Apply when writing or reviewing Bash or POSIX shell scripts — automation, CI steps, deploy scripts, or any shell-based tooling.
license: MIT
version: 1.0.0
tokens_target: 1500
triggers:
  - bash script
  - shell script
  - posix scripting
loads_after: []
supersedes: []
---

# Sub-Skill: Bash / POSIX Scripting
<!-- target: tokens_target above. Run `python tools/render_readme_table.py` to update README. -->

**Purpose:** Prevent silent failures, portability bugs, and security holes in shell scripts by enforcing safe defaults, clean structure, and ShellCheck compliance.

---

## Rules

### Safety & Error Handling

1. **Fail-fast header.** Always begin every shell script with `set -euo pipefail` so that unset variables, failed commands, and pipeline errors abort execution immediately. Reference: ERR-2026-021

2. **Trap cleanup.** Always register a `trap 'cleanup' EXIT` function to remove temp files and release locks even when the script exits early due to an error.

3. **Meaningful exit codes.** Always exit with a non-zero code that reflects the failure category (e.g., `exit 1` for usage errors, `exit 2` for dependency missing); never exit with `0` on failure.

4. **No eval.** Never use `eval` to construct or execute dynamic commands; prefer arrays or explicit argument lists to avoid injection vulnerabilities.

### Variables & Quoting

5. **Quote every variable.** Always double-quote variable expansions (`"$var"`, `"$@"`) to prevent word-splitting and glob expansion on values containing spaces or special characters.

6. **Declare locals.** Always declare variables inside functions with `local` to prevent accidental global namespace pollution.

7. **Readonly constants.** Use `readonly` for values that must not change after assignment (e.g., `readonly SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"`).

### Portability & Compatibility

8. **POSIX shebang.** Always start scripts with `#!/usr/bin/env bash` (or `#!/bin/sh` for strict POSIX); never rely on `/bin/bash` being present at a fixed path on all target systems.

9. **Portable syntax.** Prefer POSIX-compatible constructs (`[ ]` over `[[ ]]`, `$(...)` over backticks) when the script must run under `/bin/sh`; use Bash-specific features only when the shebang explicitly targets Bash.

10. **ShellCheck clean.** Ensure every script passes `shellcheck -S warning` with zero warnings before committing; treat ShellCheck output as mandatory, not advisory.

### Structure & Maintainability

11. **Use functions.** Always decompose scripts longer than ~30 lines into named functions with a `main` entry point called at the bottom; avoid top-level imperative code scattered throughout the file.

12. **Argument parsing with getopts.** Use `getopts` for option parsing in scripts that accept flags; never parse `$1`, `$2` manually for flag-style arguments.

13. **Temp file handling.** Always create temporary files with `mktemp` and store the path in a variable cleaned up by the `EXIT` trap; never hard-code paths like `/tmp/myfile`.

### Logging & Idempotency

14. **Structured logging.** Use a `log()` helper that prefixes output with a timestamp and level (`INFO`, `WARN`, `ERROR`) and routes errors to stderr (`>&2`); never mix diagnostic output into stdout used for data.

15. **Idempotent operations.** Ensure scripts can be run multiple times without side effects — use guards like `[ -d "$dir" ] || mkdir -p "$dir"` and `command -v tool >/dev/null 2>&1 || install_tool` before acting.

16. **Heredocs for multi-line strings.** Prefer heredocs (`<<'EOF' ... EOF`) over concatenated `echo` calls for multi-line output or embedded config; use the quoted form (`<<'EOF'`) to suppress variable expansion when the content is literal.

---

## See also

- `skills/code-quality/SKILL.md`
- `skills/error-log/SKILL.md`
