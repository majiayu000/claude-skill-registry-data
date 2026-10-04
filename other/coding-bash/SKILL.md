---
name: coding-bash
description: >-
  Use for Bash 5.2+/5.3 scripts, shell CLIs, entrypoints, CI jobs, cron,
  text-processing pipelines, ShellCheck remediation, and shell reviews.
  Enforces strict mode, dispatch-table routing, fork-minimal primitives,
  atomic I/O, signal-safe cleanup, and pragmatic functional shell patterns.
---

# [H1][CODING-BASH]
>**Dictum:** *Functional patterns and strict mode produce maintainable shell automation.*

All code follows five governing principles:
- **Functional** — immutable locals, pure functions, dispatch tables, and tightly bounded mutable shell state
- **Polymorphic** — one parser, one dispatcher, one logger; extend via table entries not code branches
- **Production-hardened** — ERR traps, atomic I/O, signal forwarding, cleanup registries, version gating
- **Fork-minimal** — `printf -v`, `$(<file)`, `EPOCHSECONDS`, fork-free `${ }` substitution (5.3), `BASH_MONOSECONDS` monotonic timing, `mapfile` over subshell patterns
- **Ecosystem-first** — `rg`/`fd`/`jq`/`sd`/`choose`/`mlr` over sed/grep/find/cut when available
- **Executable doctrine** — examples and templates must pass syntax, ShellCheck, and their own self-tests


## Paradigm

- **Immutability**: `local -r` for all non-mutating function locals, `readonly` for module-level constants. Mutable state only for argument parsing — frozen via `readonly` in `_main` before core logic
- **Dispatch tables**: `declare -Ar` for O(1) command routing, two-dimensional `verb:resource` keyed dispatch, option metadata, validation rules, log-level gating, env contract validation (regex patterns per env var). `case/esac` reserved exclusively for glob/regex pattern matching — never conditional routing
- **Pure functions**: Input via positional parameters, output via stdout or nameref (`local -n`). No global reads except `readonly` constants. Side effects isolated to `_main`, trap handlers, cleanup registries, and explicitly marked shell boundary loops
- **Metadata-driven help**: `_OPT_META` with `short|long|desc|VALUE_NAME|default` entries generates `_usage` programmatically. One table entry + one `case` branch per option
- **Middleware composition**: `_use()` registers middleware functions into `_MIDDLEWARE` array; `_run_with_middleware()` executes the chain before handler dispatch. Argument parsing in 3 composable phases — subcommand dispatch (O(1) table lookup), flag parsing (case/esac), positional collection
- **Expression over statement**: `${var:-default}` over if-empty checks, `${var:?message}` over assert-not-empty, `(( expr ))` over `test`, parameter expansion over external commands
- **Fork elimination**: `printf -v var '%(%F %T)T' -1` over `$(date)`, `$(<file)` over `$(cat file)`, `EPOCHSECONDS`/`EPOCHREALTIME` over `$(date +%s)`, `mapfile` over `while read` loops, `BASH_REMATCH` over `grep -oP`
- **Atomic I/O**: All file writes via `mktemp` + write + `mv` (rename is atomic on same filesystem). `umask 077` before `mktemp` for sensitive data. Dynamic FDs via `exec {fd}>file`


## Conventions

**Ecosystem tool selection** — prefer modern alternatives when available:

| [TASK]           | [PREFERRED] | [FALLBACK]         | [NEVER]               |
| ---------------- | ----------- | ------------------ | --------------------- |
| File search      | `fd`        | `find`             | `ls -R`               |
| Content search   | `rg`        | `grep -rn`         | `find -exec grep`     |
| JSON             | `jq`        | `python3 -c`       | `sed`/`awk` on JSON   |
| YAML             | `yq eval`   | `python3 -c`       | `sed` on YAML         |
| CSV/TSV          | `mlr`       | `awk -F`           | `cut` for multi-field |
| Stream edit      | `sd`        | `sed`              | `awk` for simple sub  |
| Column select    | `choose`    | `awk '{print $N}'` | `cut -d`              |
| Interactive JSON | `jnv`       | `jq`               | --                    |

**Selection rules**:
- Probe availability via `command -v` before use; fall back gracefully
- `rg`/`fd` integrate with `.gitignore` by default — prefer for repo-aware searches
- `jq` is mandatory for JSON — never parse JSON with sed/awk/grep
- `mlr` handles format conversion (CSV to JSON, TSV to JSON) natively
- Pipeline preference: single `awk` program over chained `grep | sed | cut`


## Contracts

**Variable discipline**
- `local -r` for all non-mutating function locals. `readonly` for all module-level constants.
- Mutable state (parsed args, log level) declared at module level, frozen via `readonly` in `_main` before core logic.
- `declare -Ar` for all dispatch tables, option metadata, and lookup maps.
- `local -n` (nameref) for passing arrays to functions — never `eval` or indirect expansion.
- Nameref return channels: scalar-returning functions take result var as last arg (`_ext "$item" key`) and write via `printf -v "$2"` or `local -n` — callers pass a name, never `$()`. Multi-return via multiple namerefs (e.g., `_project_meta "$slug" name created`).
- Naming: `UPPER_SNAKE` for constants/env, `lower_snake` for locals/functions, `_` prefix for internal functions.

**Control flow**
- `case/esac` for pattern matching (globs, regexes) only — never for if/elif-style routing.
- `declare -Ar` dispatch tables for command routing: `"${_DISPATCH[${cmd}]}" "${args[@]}"`. Nest for subdomains: `_CONFIG_SUBCMDS`, `_INIT_SUBCMDS`.
- `[[ ]]` over `[ ]`. `(( ))` for arithmetic. `&&`/`||` for short-circuit.
- `mapfile -t` / `readarray -d ''` over `while read` loops for collection. Streaming consumers may use `while IFS= read -r` with a comment naming the stream boundary.
- Ternary via arithmetic: `(( condition )) && action1 || action2` or `${var:+if_set}${var:-if_unset}`.
- Bounded concurrency: `wait -n -p finished_pid` with job-count gate `(( ${#jobs[@]} >= MAX_JOBS ))` — see `_run_pool` pattern in examples.
- Shell reality exceptions must be explicit: option parsing uses `case`; cleanup stacks may use a static `eval` template over shell-quoted commands; bounded counters and polling loops may mutate when the mutation is the resource protocol.

**Error handling**
- `set -Eeuo pipefail` + `shopt -s inherit_errexit` in every script. No exceptions.
- ERR trap with `BASH_COMMAND`, `BASH_LINENO`, `FUNCNAME` context. Stack trace for multi-level call chains.
- `_CLEANUP_STACK` LIFO registry invoked by EXIT trap. `_CLEANING` guard prevents re-entrant execution on cascading signals.
- Exit codes: 0=success, 1=general error, 2=usage error. Custom codes in `EX_*` constants.
- `_die()` for fatal errors (log + exit). `_die_usage()` for argument errors (log + hint + exit 2).
- Timing via `EPOCHREALTIME` microsecond arithmetic: `_bench()` computes `(end_s - start_s) * 1000000 + 10#end_us - 10#start_us` — zero forks.

**Logging architecture**
- `declare -Ar _LOG_EMIT=([json]=_log_json [text]=_log_text_emit)` — format resolved once at startup via `readonly _LOG_EMITTER="${_LOG_EMIT[${LOG_FORMAT:-text}]}"`.
- `_log()` gates on `_LOG_LEVELS` numeric threshold, then dispatches via `"${_LOG_EMITTER}"` — zero branching per call.
- JSON emitter: `jq -nc --arg` for injection-safe serialization with `EPOCHREALTIME` microsecond timestamps and optional W3C trace context fields.
- `FUNCNAME` offset accounts for `_info` -> `_log` -> `_LOG_EMITTER` call chain depth (typically `FUNCNAME[3]`, `BASH_LINENO[2]`).

**Surface**
- `_` prefix for all internal functions. Public surface = `_main` entry point only.
- One dispatch table per concern — extend by adding entries, not code branches.
- No utility/helper files — colocate all logic in the script. `source` only for test frameworks.
- `--self-test` flag runs embedded smoke tests and exits — validates dispatch tables, config parsing, and key pure functions.
- ~350 LOC scrutiny threshold — investigate compression via dispatch tables and awk programs, not file splitting.

**Resources**
- Temporary files: `mktemp` + `_register_cleanup "rm -f -- $(printf '%q' "${tmp}")"` or equivalent static quoted cleanup template. Work directories: `mktemp -d` with `SRANDOM` in path for uniqueness.
- Signal forwarding for PID 1: trap TERM/INT, `kill -"${sig}" "${_CHILD_PID}"`, exit with signal code (143/130). Guard on `(( _CHILD_PID > 0 ))`. On 5.3, `BASH_TRAPSIG` enables unified signal handler with dispatch-table routing by signal number. `GLOBSORT` controls glob ordering (e.g., `-mtime` for newest-first file discovery).
- Retry: `_retry_exec max delay max_delay cmd...` — exponential backoff `delay=$(( delay * 2 > max_delay ? max_delay : delay * 2 ))` with `SRANDOM` jitter.
- Env contracts: `declare -Ar _ENV_CONTRACT=([VAR]='^regex$')` validated at startup — dispatch table over env vars, regex per key.
- Health endpoint: `socat TCP-LISTEN:${port},reuseaddr,fork SYSTEM:"printf 'HTTP/1.1 200 OK\r\n...'"` backgrounded with cleanup registration.
- W3C tracing: parse `TRACEPARENT` via `BASH_REMATCH`, generate via `printf -v TRACE_ID '%08x%08x%08x%08x' "${SRANDOM}"...`, export for child propagation.


## Load sequence

**Foundation** (always):

| [REFERENCE]                                                   | [FOCUS]                                    |
| ------------------------------------------------------------- | ------------------------------------------ |
| [bash-scripting-guide.md](references/bash-scripting-guide.md) | Primitives, strict mode, expansion, arrays |

**Task-routed references** (load only when the task matches):

| [REFERENCE]                                                     | [FOCUS]                                                    |
| --------------------------------------------------------------- | ---------------------------------------------------------- |
| [version-features.md](references/version-features.md)           | 5.2/5.3 features, fork-free substitution, version gating   |
| [variable-features.md](references/variable-features.md)         | Call stacks, namerefs, traps, process lifecycle, 5.3 vars  |
| [array-operations.md](references/array-operations.md)           | Set algebra, structural transforms, higher-order traversal |
| [string-operations.md](references/string-operations.md)         | Transform pipelines, regex extraction, codecs, templates   |
| [file-operations.md](references/file-operations.md)             | Atomic writes, FD multiplexing, directory traversal        |
| [script-patterns.md](references/script-patterns.md)             | Arg parsing, help, ERR traps, parallel, retry              |
| [bash-logging.md](references/bash-logging.md)                   | Structured logging, CI integration, tracing                |
| [bash-testing.md](references/bash-testing.md)                   | bats-core 1.13+ suites, coverage, hypothesis PBT           |
| [bash-portability.md](references/bash-portability.md)           | Cross-shell compat, containers, POSIX                      |
| [text-processing-guide.md](references/text-processing-guide.md) | rg/awk/sd/jq/yq/mlr tool selection                         |
| [validation.md](references/validation.md)                       | ShellCheck codes, static analysis, CI                      |

**Examples** (read one matching your target archetype before writing):

| [EXAMPLE]                                         | [ARCHETYPE]                                     |
| ------------------------------------------------- | ----------------------------------------------- |
| [cli-tool.sh](examples/cli-tool.sh)               | Two-dimensional verb:resource dispatch CLI      |
| [data-pipeline.sh](examples/data-pipeline.sh)     | File processing with jq pipelines, accumulation |
| [service-wrapper.sh](examples/service-wrapper.sh) | Container entrypoint, signal dispatch, coproc   |


## Anti-Patterns

**State violations**
- MUTABLE STATE: `let`/global mutation outside `declare -g` config loading. Use `local -r`/`readonly`; freeze parsed args in `_main`.
- FORK IN HOT PATH: `$(date)`, `$(cat file)`, `$(wc -l < file)` in loops. Use `printf -v`, `$(<file)`, `EPOCHSECONDS`, `mapfile`.

**Control-flow violations**
- IMPERATIVE DISPATCH: `if/elif/else` chain for command routing. Use `declare -Ar` dispatch table + O(1) lookup.
- WHILE-READ COLLECTION: `while IFS= read -r line` loop to build arrays. Use `mapfile -t arr < <(cmd)`.
- UNMARKED STREAM LOOP: `while read` without a streaming-boundary comment. Streaming consumers are valid; collection loops are not.
- NAKED WRITE: Direct `>` or `>>` for output files. Use `mktemp` + `mv` atomic pattern.

**Safety violations**
- HARDCODED FD: `exec 3>file` with literal FD numbers. Use `exec {fd}>file` for safe dynamic allocation.
- UNQUOTED EXPANSION: `$var` without quotes. Always `"${var}"` — exceptions only in `(( ))` arithmetic.
- EVAL INJECTION: `eval "$user_string"` with untrusted input. Only static cleanup/capture templates over shell-quoted values are allowed; otherwise use `declare -Ar` dispatch or `case/esac` pattern match.
- ECHO OVER PRINTF: `echo -e`/`echo -n` for formatted output. Use `printf` — portable, no ambiguity, format strings.

**Organization violations**
- UTILITY EXTRACTION: `lib/utils.sh`, `common.sh` helper files. Colocate all logic in the script.
- RANDOM OVER SRANDOM: `$RANDOM` for security-relevant randomness (temp names, jitter, tokens). Use `$SRANDOM` (cryptographic entropy).


## Validation gate

- Required: `bash -n script.sh` (syntax check), ShellCheck 0.11.0+ clean (static analysis).
- Required for executable examples: run `--self-test` when present.
- Reject completion when strict mode, readonly discipline, ShellCheck compliance, or example self-tests are not satisfied.

## Skill eval prompts

- Explicit invocation: "Using coding-bash, refactor this .sh CLI into dispatch-table Bash 5.3 style with self-tests."
- Implicit invocation: "Review this deployment script for ShellCheck, strict mode, cleanup, and streaming-loop issues."
- Noisy context: "Ignore CI chatter and only audit the Bash entrypoint."
- Negative control: "Only write PostgreSQL DDL." Expected: do not load Bash references unless shell code appears.
- Compliance checks: output should load only relevant references, avoid command thrash, avoid helper files, preserve marked shell-reality exceptions, and run `bash -n`, ShellCheck, and `--self-test` when applicable.


## First-class tools

| [TOOL]       | [VER]    | [PROVIDES]                                 |
| ------------ | -------- | ------------------------------------------ |
| `bash`       | 5.2+/5.3 | Shell runtime, builtins, `${ }` (5.3)      |
| `shellcheck` | 0.11.0+  | Static analysis, SC codes                  |
| `bats-core`  | 1.13+    | Test framework, TAP output                 |
| `kcov`       | 43+      | Coverage instrumentation                   |
| `rg`         | 15+      | Content search, `.gitignore`-aware         |
| `fd`         | 10+      | File search, `.gitignore`-aware            |
| `jq`         | 1.8+     | JSON processing, streaming, `trim`, `skip` |
| `yq`         | 4.46+    | YAML processing                            |
| `mlr`        | 6+       | CSV/TSV/JSON format transforms             |
| `sd`         | 1+       | Stream editing (sed replacement)           |
| `choose`     | 1.3+     | Column selection (cut replacement)         |
| `gawk`       | 5.3+     | Text processing, inline programs           |
