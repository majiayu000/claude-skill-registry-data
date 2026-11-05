---
name: implementing-shell
description: Write and review Bash scripts — strict mode, argument parsing, usage messages, exit codes, DRY_RUN, dependency checks, ShellCheck clean. Use for hooks, CI helpers and setup scripts.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Grep, Glob, Edit, Write, Bash
  argument-hint: "[script-path]"
  stability: experimental
---

# Implementing Shell Scripts

**Target**: $ARGUMENTS

Writes or reviews Bash scripts so they fail loudly, explain their usage, and pass ShellCheck. Test
them with `testing-shell` (BATS).

## When to Use

- New or changed `*.sh`: hooks, CI helpers, install/setup scripts, GitHub Action scripts
- Reviewing a script that silently continues after errors or has no usage message

## Do Not Use

- Logic that has outgrown shell (data structures, JSON transforms beyond `jq`, >~200 lines) — move
  it to Python or another real language instead of hardening the script

## Conventions

| Topic | Rule |
| --- | --- |
| Shebang | `#!/usr/bin/env bash` (or `sh` only when POSIX-portable and tested with `dash`) |
| Strict mode | `set -euo pipefail` for scripts that must stop on errors. Hooks that must never break the host tool use `set -u` and handle failures explicitly instead |
| Quoting | Quote every expansion: `"$var"`, `"$@"`, `"$(cmd)"` |
| Usage | `usage()` prints to stderr; `-h`/`--help` exits 0, a usage error exits 2 |
| Exit codes | 0 success · 1 runtime failure · 2 usage error; document any others in `usage()` |
| Dependencies | Check with `command -v tool >/dev/null` up front and say which tool is missing |
| Side effects | Honour `DRY_RUN=1`: print what would change, change nothing |
| Temp files | `tmp=$(mktemp -d)` plus `trap 'rm -rf "$tmp"' EXIT` |
| Output | Data to stdout, diagnostics to stderr, so callers can pipe the result |
| Untrusted input | Never `eval`; pass values as arguments, not interpolated into command strings |

## Skeleton

```bash
#!/usr/bin/env bash
# do-thing.sh — one line on what it does.
set -euo pipefail

usage() {
  cat >&2 <<'EOF'
Usage: do-thing.sh [--out FILE] TARGET
  --out FILE  write the report to FILE (default: stdout)
Env: DRY_RUN=1 prints actions without performing them.
EOF
}

die() { echo "error: $*" >&2; exit 1; }

out=""
while [ $# -gt 0 ]; do
  case "$1" in
    -h|--help) usage; exit 0 ;;
    --out) [ $# -ge 2 ] || { usage; exit 2; }; out="$2"; shift 2 ;;
    --) shift; break ;;
    -*) usage; exit 2 ;;
    *) break ;;
  esac
done
[ $# -eq 1 ] || { usage; exit 2; }
target="$1"

command -v jq >/dev/null 2>&1 || die "jq is required"

run() { if [ "${DRY_RUN:-0}" = "1" ]; then echo "DRY_RUN: $*" >&2; else "$@"; fi; }

write_report() { printf 'processed %s\n' "$target" > "$1"; }

if [ -n "$out" ]; then run write_report "$out"; else echo "processed $target"; fi
```

## ShellCheck

- Run `shellcheck path/to/script.sh` locally and in CI; fix findings rather than disabling them.
- When a disable is genuinely right, scope it to one line with a reason:
  `# shellcheck disable=SC2086 # word-splitting intended: FLAGS is a flag list`
- Source files ShellCheck can't follow: `# shellcheck source=lib/common.sh`.

## Review checklist

- Fails on the first error (or handles each failure explicitly), never continues on bad state
- Usage message matches the parser; usage errors exit 2
- All expansions quoted; no `eval`; no parsing of `ls` output
- Missing dependencies produce a clear message
- `DRY_RUN=1` path exists for anything that writes, deletes or calls an API
- ShellCheck clean; BATS tests cover each exit path (`testing-shell`)
