---
name: shell
description: Use when writing Bash scripts or command-line automation. Covers strict mode, safe quoting, argument parsing, trap-based cleanup, portability, and ShellCheck-clean scripts.
metadata:
  category: languages
  version: 1.0.0
  tags: [bash, shell, scripting, shellcheck, automation]
---

# Shell

## Purpose

Write shell scripts that fail loudly instead of silently, handle paths with spaces, and clean up after themselves. Most shell bugs are one missing quote or one unchecked exit code.

## When to Use

- Writing or reviewing Bash scripts.
- Building CI steps, deployment scripts, or developer tooling.
- Hardening a script that "works on my machine".
- Deciding whether a task has outgrown shell entirely.

## Capabilities

- Strict mode and error handling that actually stops the script.
- Safe quoting, arrays, and `IFS` handling.
- Argument parsing and usage output.
- Cleanup via `trap`, temp file discipline, and idempotence.
- Portability between Bash, POSIX `sh`, and macOS's older toolchain.

## Inputs

- The script, its invocation context (CI, cron, interactive), and target shells.
- Whether it must run on macOS (BSD utilities) as well as Linux (GNU).

## Outputs

- A script passing `shellcheck -x` with no warnings.
- Deterministic exit codes and a usage message.
- Cleanup guaranteed on every exit path.

## Workflow

1. **Start strict** — `set -Eeuo pipefail` and an `IFS` you control.
2. **Parse arguments explicitly** — Validate required inputs and print usage on error.
3. **Quote everything** — Every variable expansion is `"$var"` unless you have a specific reason otherwise.
4. **Register cleanup** — `trap` before you create the first temporary resource.
5. **Gate** — Run ShellCheck; run the script under `bash -n` and, where practical, with `set -x` in a dry run.

## Best Practices

- `set -e` alone does not catch failures inside pipelines. `pipefail` is what makes `a | b` fail when `a` does.
- Unquoted `$var` splits on whitespace and glob-expands. This is the root cause of most "it broke on a filename with a space" bugs.
- Use `mktemp -d` and remove it in a trap — never hardcode `/tmp/mything`.
- Prefer `[[ ]]` over `[ ]` in Bash; it does not word-split and supports pattern matching.
- Check that required commands exist up front rather than failing halfway through.
- When a script exceeds roughly 100 lines or needs data structures, rewrite it in Python. Shell is glue, not a language for logic.

## Examples

**Script skeleton:**

```bash
#!/usr/bin/env bash
set -Eeuo pipefail
IFS=$'\n\t'

readonly SCRIPT_NAME="${0##*/}"

usage() {
  cat <<USAGE
Usage: ${SCRIPT_NAME} --source DIR --dest DIR [--dry-run]

  --source DIR   Directory to sync from (required)
  --dest DIR     Directory to sync to (required)
  --dry-run      Print actions without performing them
USAGE
}

die() { printf '%s: %s\n' "$SCRIPT_NAME" "$1" >&2; exit 1; }

main() {
  local source="" dest="" dry_run=0

  while (($# > 0)); do
    case "$1" in
      --source) source="${2:-}"; shift 2 ;;
      --dest)   dest="${2:-}";   shift 2 ;;
      --dry-run) dry_run=1; shift ;;
      -h|--help) usage; exit 0 ;;
      *) usage >&2; die "unknown argument: $1" ;;
    esac
  done

  [[ -n "$source" && -n "$dest" ]] || { usage >&2; die "missing required argument"; }
  [[ -d "$source" ]] || die "source not a directory: $source"
  command -v rsync >/dev/null || die "rsync is required but not installed"

  local workdir
  workdir="$(mktemp -d)"
  trap 'rm -rf "$workdir"' EXIT

  local -a flags=(--archive --delete)
  ((dry_run)) && flags+=(--dry-run)

  rsync "${flags[@]}" "$source/" "$dest/"
}

main "$@"
```

## Notes

- `set -E` propagates the `ERR` trap into functions and subshells; without it, error traps silently do not fire where you expect.
- macOS ships BSD `sed`, `date`, and `readlink`, which differ from GNU. If the script must run on both, either avoid them or depend on `coreutils`.
- `shellcheck -x` follows sourced files; the plain invocation does not.
