---
name: using-terminal
description: MANDATORY skill for safe and efficient terminal/shell command execution.
---

## Required `<project-root>/docs` reads

Read these project-root spec files before running any terminal/shell command (use shell `cat`/`ls` — they may be in `.gitignore`, invisible to built-in search). Missing file → fall back to native tools, note the gap; never invent contents.

- `<project-root>/docs/container-clis.md`
- `<project-root>/docs/terminal-wrappers.md`
- `<project-root>/docs/terminal-tools.md`

# Terminal Token Compression

## Pre-flight checklist

Before every terminal/shell command, verify:

1. A terminal wrapper is configured in `<project-root>/docs/terminal-wrappers.md`. If the file is missing, empty, or no wrapper is configured, run the raw command without any wrapper.
2. The command uses the configured terminal wrapper (or a matching wrapper subcommand).
3. No `cd` in the command. The shell runs in the correct `cwd`. Use absolute paths for file arguments. Use `cd` only when the destination differs from `cwd` and no absolute-path form exists. If unsure, omit `cd`.
4. The skill that suggested the command (e.g. the container CLI skill) was also invoked.

Anti-`cd` examples:

- Bad: `cd /Users/jun/.agents && terminal-wrapper ls` · Good: `terminal-wrapper ls /Users/jun/.agents` (e.g. `rtk ls`)
- Bad: `cd src && terminal-wrapper grep foo` · Good: `terminal-wrapper grep foo /abs/path/src` (e.g. `rtk grep`)

## Rule

If a terminal wrapper is configured in `<project-root>/docs/terminal-wrappers.md`, prefix commands with it and use the matching wrapper subcommand instead of the raw binary. If no subcommand exists, fall back to the wrapper's raw run or raw proxy command.

If no wrapper is configured or `<project-root>/docs/terminal-wrappers.md` is missing/empty, run raw commands without any wrapper.

```bash
terminal-wrapper git status
terminal-wrapper cargo test
terminal-wrapper npm run test
```

## Subcommand map (common)

The wrapper maps raw commands to compressed subcommands (see `<project-root>/docs/terminal-wrappers.md` for the full map):

| Category | Examples |
| --- | --- |
| Filesystem | `terminal-wrapper ls`, `terminal-wrapper tree`, `terminal-wrapper read <file>`, `terminal-wrapper grep`, `terminal-wrapper find`, `terminal-wrapper wc`, `terminal-wrapper diff` |
| Git | `terminal-wrapper git …`, `terminal-wrapper gh …`, `terminal-wrapper glab …`, `terminal-wrapper gt …` |
| Containers/Cloud | `terminal-wrapper docker …`, `terminal-wrapper kubectl …`, `terminal-wrapper aws …`, `terminal-wrapper psql …` |
| JS/TS | `terminal-wrapper npm run …`, `terminal-wrapper pnpm …`, `terminal-wrapper npx …`, `terminal-wrapper next …`, `terminal-wrapper jest`, `terminal-wrapper vitest`, `terminal-wrapper playwright`, `terminal-wrapper prisma …` |
| Rust/Go | `terminal-wrapper cargo …`, `terminal-wrapper go …`, `terminal-wrapper golangci-lint run` |
| Python | `terminal-wrapper pip …`, `terminal-wrapper pytest`, `terminal-wrapper ruff`, `terminal-wrapper mypy` |
| Ruby | `terminal-wrapper rspec`, `terminal-wrapper rubocop`, `terminal-wrapper rake` |
| JVM | `terminal-wrapper mvn …`, `terminal-wrapper gradlew …` |
| Lint (special) | `eslint` → `terminal-wrapper lint`, `prettier --check` → `terminal-wrapper prettier` |
| Network | `terminal-wrapper curl`, `terminal-wrapper wget`, `terminal-wrapper env` |

For anything else, use the wrapper's raw run or raw proxy command.

## Meta commands

```bash
terminal-wrapper gain              # Show token savings
terminal-wrapper gain --history    # Command history with savings
terminal-wrapper discover          # Find missed terminal wrapper opportunities
terminal-wrapper session           # Terminal wrapper adoption across recent sessions
terminal-wrapper rewrite <cmd>     # Print the terminal wrapper equivalent of a raw command
```

## Exceptions — do NOT use the terminal wrapper

- No terminal wrapper is configured or `<project-root>/docs/terminal-wrappers.md` is missing/empty.
- Commands needing byte-exact stdout (piping binary, checksums, terminal wrapper verify).
- Interactive/TUI programs (`vim`, `top`, `tmux`, REPLs).
- Commands inside the wrapper's raw run/proxy are already raw — do not double-wrap.
- Container CLI (see `<project-root>/docs/container-clis.md`): the container CLI wraps Docker/docker-compose invocations and manages its own output formatting. Wrapping it breaks script resolution and output handling. Run container CLI commands directly.
- A project rule or the user explicitly disables the terminal wrapper for a command.

## Preferences

- Prefer wrapper subcommands over raw binaries.
- Pipe through `head`/`tail`/`grep`/`wc` for a slice of large output: `terminal-wrapper logs app | tail -50`.
- Invoke the container CLI skill before any container CLI command.

## Output Truncation Awareness

Large output overflows into a file you must re-read. Avoid it:

- Pass scope flags first: `--stat`, `--oneline`, `--name-only`, `--count`, `-q`.
- Pipe through `head`/`tail`/`grep`/`wc` for the decisive slice.
- `git log`/`diff`: always `--no-pager` + `--oneline` or `--stat`; never raw full diff.
- Test/lint suites: use compact mode (`--compact`, `--no-progress`, summary-only) over verbose per-test output.
- If output will likely exceed ~200 lines, narrow the command before running instead of re-reading the overflow.
