---
name: coding-bash
description: >-
    Authors, hardens, reviews, and debugs Bash and shell scripts. Use whenever
    creating, editing, or reading any .sh/.bash file, and ShellCheck remediation.
---

# [CODING_BASH]

All code follows these governing principles:
- [FUNCTIONAL] — immutable locals, pure functions, dispatch tables, and tightly bounded mutable shell state
- [POLYMORPHIC] — one parser, one dispatcher, one logger; extend via table entries not code branches
- [PRODUCTION_HARDENED] — ERR traps, atomic I/O, signal forwarding, cleanup registries, version gating
- [FORK_MINIMAL] — `printf -v`, `$(<file)`, `EPOCHSECONDS`, fork-free `${ }`, `BASH_MONOSECONDS` timing, `mapfile` over subshell patterns
- [ECOSYSTEM_FIRST] — `rg`/`fd`/`jq`/`sd`/`choose`/`mlr` over sed/grep/find/cut when available
- [EXECUTABLE_DOCTRINE] — examples and templates must pass syntax, ShellCheck, and their own self-tests

## [01]-[ROUTING]

[FOUNDATION]: every task loads [bash-scripting-guide.md](references/bash-scripting-guide.md) — primitives, strict mode, expansion, arrays.

[TASK_ROUTED]: load only when the task matches.
- [01]-[VERSION_FEATURES](references/version-features.md): runtime features, fork-free substitution, version gating
- [02]-[VARIABLE_FEATURES](references/variable-features.md): call stacks, namerefs, traps, process lifecycle, runtime variables
- [03]-[ARRAY_OPERATIONS](references/array-operations.md): set algebra, structural transforms, higher-order traversal
- [04]-[STRING_OPERATIONS](references/string-operations.md): transform pipelines, regex extraction, codecs, templates
- [05]-[FILE_OPERATIONS](references/file-operations.md): atomic writes, FD multiplexing, directory traversal
- [06]-[SCRIPT_PATTERNS](references/script-patterns.md): arg parsing, help, ERR traps, parallel, retry
- [07]-[BASH_LOGGING](references/bash-logging.md): structured logging, CI integration, tracing
- [08]-[BASH_TESTING](references/bash-testing.md): bats-core suites, coverage, hypothesis PBT
- [09]-[BASH_PORTABILITY](references/bash-portability.md): cross-shell compat, containers, POSIX
- [10]-[TEXT_PROCESSING_GUIDE](references/text-processing-guide.md): rg/awk/sd/jq/yq/mlr tool selection
- [11]-[VALIDATION](references/validation.md): ShellCheck codes, static analysis, CI

[EXAMPLES]: read the one matching the target archetype before writing.
- [01]-[CLI_TOOL](examples/cli-tool.sh): two-dimensional verb:resource dispatch CLI
- [02]-[DATA_PIPELINE](examples/data-pipeline.sh): file processing with jq pipelines, accumulation
- [03]-[SERVICE_WRAPPER](examples/service-wrapper.sh): container entrypoint, signal dispatch, coproc

[TEMPLATE]: scaffold a new script from [standard.template.md](templates/standard.template.md) — strict-mode header, logging, cleanup stack, traps, flag parsing, self-test.

## [02]-[PARADIGM]

- [IMMUTABILITY]: `local -r` for every non-mutating function local, `readonly` for module-level constants
- [FROZEN_ARGS]: Mutable state only for argument parsing — frozen via `readonly` in `_main` before core logic
- [DISPATCH_TABLES]: `declare -Ar` for O(1) command routing and two-dimensional `verb:resource` dispatch
- [DATA_TABLES]: `declare -Ar` also tables option metadata, validation rules, log-level gating, and env contracts (regex per var)
- [CASE_RESERVED]: `case/esac` reserved exclusively for glob/regex pattern matching — never conditional routing
- [PURE_FUNCTIONS]: Input via positional parameters, output via stdout or nameref (`local -n`); no global reads except `readonly` constants
- [SIDE_EFFECTS]: Side effects isolated to `_main`, trap handlers, cleanup registries, and explicitly marked shell boundary loops
- [METADATA_DRIVEN_HELP]: `_OPT_META` with `short|long|desc|VALUE_NAME|default` entries generates `_usage`. One entry + one `case` branch per option
- [MIDDLEWARE_COMPOSITION]: `_use()` registers middleware into `_MIDDLEWARE`; `_run_with_middleware()` executes the chain before handler dispatch
- [PARSE_PHASES]: Argument parsing composes subcommand dispatch (O(1) table lookup), flag parsing (`case/esac`), positional collection
- [EXPRESSION_OVER_STATEMENT]: `${var:-default}` over if-empty, `${var:?message}` over assert-nonempty, `(( expr ))` over `test`, expansion over forks
- [FORK_ELIMINATION]: `printf -v var '%(%F %T)T' -1` over `$(date)`, `$(<file)` over `$(cat file)`, `EPOCHSECONDS`/`EPOCHREALTIME` over `$(date +%s)`, `mapfile` over `while read`, `BASH_REMATCH` over `grep -oP`
- [ATOMIC_IO]: Every file write goes `mktemp` + write + `mv` — rename is atomic on the same filesystem; `umask 077` before `mktemp` for sensitive data
- [DYNAMIC_FD]: Dynamic FDs via `exec {fd}>file`

## [03]-[CONVENTIONS]

[ECOSYSTEM_TOOL_SELECTION]: richer ecosystem tools own each available operation:

| [INDEX] | [TASK]           | [PREFERRED] | [FALLBACK]         | [NEVER]               |
| :-----: | :--------------- | :---------- | :----------------- | :-------------------- |
|  [01]   | File search      | `fd`        | `find`             | `ls -R`               |
|  [02]   | Content search   | `rg`        | `grep -rn`         | `find -exec grep`     |
|  [03]   | JSON             | `jq`        | `python3 -c`       | `sed`/`awk` on JSON   |
|  [04]   | YAML             | `yq eval`   | `python3 -c`       | `sed` on YAML         |
|  [05]   | CSV/TSV          | `mlr`       | `awk -F`           | `cut` for multi-field |
|  [06]   | Stream edit      | `sd`        | `sed`              | `awk` for simple sub  |
|  [07]   | Column select    | `choose`    | `awk '{print $N}'` | `cut -d`              |
|  [08]   | Interactive JSON | `jnv`       | `jq`               | --                    |

[SELECTION_RULES]:
- Probe availability via `command -v` before use; fall back gracefully
- `rg` and `fd` own repo-aware searches through default `.gitignore` integration
- `jq` is mandatory for JSON — never parse JSON with sed/awk/grep
- `mlr` handles format conversion (CSV to JSON, TSV to JSON) natively
- Pipeline preference: single `awk` program over chained `grep | sed | cut`

## [04]-[CONTRACTS]

[VARIABLE_DISCIPLINE]:
- `local -r` for all non-mutating function locals. `readonly` for all module-level constants.
- Mutable state (parsed args, log level) declared at module level, frozen via `readonly` in `_main` before core logic.
- `declare -Ar` for all dispatch tables, option metadata, and lookup maps.
- `local -n` (nameref) for passing arrays to functions — never `eval` or indirect expansion.
- Nameref return channels: a scalar-returning function takes the result var last (`_ext "$item" key`), writing via `printf -v "$2"` or `local -n`.
- Callers pass a name, never `$()`. Multi-return via multiple namerefs (`_project_meta "$slug" name created`).
- Naming: `UPPER_SNAKE` for constants/env, `lower_snake` for locals/functions, `_` prefix for internal functions.

[CONTROL_FLOW]:
- `case/esac` for pattern matching (globs, regexes) only — never for if/elif-style routing.
- `declare -Ar` dispatch tables for command routing: `"${_DISPATCH[${cmd}]}" "${args[@]}"`. Nest for subdomains: `_CONFIG_SUBCMDS`, `_INIT_SUBCMDS`.
- `[[ ]]` over `[ ]`. `(( ))` for arithmetic. `&&`/`||` for short-circuit.
- `mapfile -t` / `readarray -d ''` over `while read` loops for collection.
- Streaming consumers may use `while IFS= read -r` with a comment naming the stream boundary.
- Ternary via arithmetic: `(( condition )) && action1 || action2` or `${var:+if_set}${var:-if_unset}`.
- Bounded concurrency: `wait -n -p finished_pid` with job-count gate `(( ${#jobs[@]} >= MAX_JOBS ))` — see `_run_pool` pattern in examples.
- Shell reality exceptions are explicit: option parsing uses `case`; cleanup stacks may use a static `eval` template over shell-quoted commands.
- Bounded counters and polling loops may mutate when the mutation is the resource protocol.

[ERROR_HANDLING]:
- `set -Eeuo pipefail` + `shopt -s inherit_errexit` in every script. No exceptions.
- ERR trap with `BASH_COMMAND`, `BASH_LINENO`, `FUNCNAME` context. Stack trace for multi-level call chains.
- `_CLEANUP_STACK` LIFO registry invoked by EXIT trap. `_CLEANING` guard prevents re-entrant execution on cascading signals.
- Exit codes: 0=success, 1=general error, 2=usage error. Custom codes in `EX_*` constants.
- `_die()` for fatal errors (log + exit). `_die_usage()` for argument errors (log + hint + exit 2).
- Timing: `BASH_MONOSECONDS` for elapsed-time durations — monotonic, immune to NTP drift, zero forks.
- `EPOCHREALTIME` only for absolute timestamps and microsecond benchmarks (`_bench()` shape: `(end_s - start_s) * 1000000 + 10#end_us - 10#start_us`).
- Version-safe `BASH_MONOSECONDS` / `EPOCHREALTIME` fallback dispatch: `references/version-features.md`.

[LOGGING_ARCHITECTURE]:
- `declare -Ar _LOG_EMIT=([json]=_log_json [text]=_log_text_emit)` tables the emitters.
- Format resolves once at startup: `readonly _LOG_EMITTER="${_LOG_EMIT[${LOG_FORMAT:-text}]}"`.
- `_log()` gates on `_LOG_LEVELS` numeric threshold, then dispatches via `"${_LOG_EMITTER}"` — zero branching per call.
- JSON emitter: `jq -nc --arg` for injection-safe serialization with `EPOCHREALTIME` microsecond timestamps and optional W3C trace context fields.
- `FUNCNAME` offset accounts for `_info` -> `_log` -> `_LOG_EMITTER` call chain depth (typically `FUNCNAME[3]`, `BASH_LINENO[2]`).

[SURFACE]:
- `_` prefix for all internal functions. Public surface = `_main` entry point only.
- One dispatch table per concern — extend by adding entries, not code branches.
- No utility/helper files — colocate all logic in the script. `source` only for test frameworks.
- `--self-test` flag runs embedded smoke tests and exits — validates dispatch tables, config parsing, and key pure functions.
- ~350 LOC scrutiny threshold — investigate compression via dispatch tables and awk programs, not file splitting.

[RESOURCES]:
- Temporary files: `mktemp` + `_register_cleanup "rm -f -- $(printf '%q' "${tmp}")"` or an equivalent static quoted cleanup template.
- Work directories: `mktemp -d` with `SRANDOM` in path for uniqueness.
- Signal forwarding for PID 1: trap TERM/INT, `kill -"${sig}" "${_CHILD_PID}"`, exit with signal code (143/130). Guard on `(( _CHILD_PID > 0 ))`.
- `BASH_TRAPSIG` carries the signal number, so one unified handler routes every signal through a dispatch table.
- `GLOBSORT` controls glob ordering (e.g., `-mtime` for newest-first file discovery).
- Retry: `_retry_exec max delay max_delay cmd...` — backoff `delay=$(( delay * 2 > max_delay ? max_delay : delay * 2 ))` with `SRANDOM` jitter.
- Env contracts: `declare -Ar _ENV_CONTRACT=([VAR]='^regex$')` validated at startup — dispatch table over env vars, regex per key.
- Health endpoint: `socat TCP-LISTEN:${port},reuseaddr,fork SYSTEM:"printf 'HTTP/1.1 200 OK\r\n...'"` backgrounded with cleanup registration.
- W3C tracing: parse `TRACEPARENT` via `BASH_REMATCH`, generate via `printf -v TRACE_ID '%08x%08x%08x%08x' "${SRANDOM}"...`, export for children.

## [05]-[ANTI_PATTERNS]

[STATE_VIOLATIONS]:
- MUTABLE STATE: `let`/global mutation outside `declare -g` config loading. Use `local -r`/`readonly`; freeze parsed args in `_main`.
- FORK IN HOT PATH: `$(date)`, `$(cat file)`, `$(wc -l < file)` in loops. Use `printf -v`, `$(<file)`, `EPOCHSECONDS`, `mapfile`.

[CONTROL_FLOW_VIOLATIONS]:
- IMPERATIVE DISPATCH: `if/elif/else` chain for command routing. Use `declare -Ar` dispatch table + O(1) lookup.
- WHILE-READ COLLECTION: `while IFS= read -r line` loop to build arrays. Use `mapfile -t arr < <(cmd)`.
- UNMARKED STREAM LOOP: `while read` without a streaming-boundary comment. Streaming consumers are valid; collection loops are not.
- NAKED WRITE: Direct `>` or `>>` for output files. Use `mktemp` + `mv` atomic pattern.

[SAFETY_VIOLATIONS]:
- HARDCODED FD: `exec 3>file` with literal FD numbers. Use `exec {fd}>file` for safe dynamic allocation.
- UNQUOTED EXPANSION: `$var` without quotes. Always `"${var}"` — exceptions only in `(( ))` arithmetic.
- EVAL INJECTION: `eval "$user_string"` with untrusted input. Use `declare -Ar` dispatch or `case/esac` pattern match.
- ECHO OVER PRINTF: `echo -e`/`echo -n` for formatted output. Use `printf` — portable, no ambiguity, format strings.

[ORGANIZATION_VIOLATIONS]:
- UTILITY EXTRACTION: `lib/utils.sh`, `common.sh` helper files. Colocate all logic in the script.
- RANDOM OVER SRANDOM: `$RANDOM` for security-relevant randomness (temp names, jitter, tokens). Use `$SRANDOM` (cryptographic entropy).

## [06]-[VALIDATION_GATE]

- Required: `bash -n script.sh` (syntax check), ShellCheck clean (static analysis).
- Required for executable examples: run `--self-test` when present.
- Reject completion when strict mode, readonly discipline, ShellCheck compliance, or example self-tests are not satisfied.

## [07]-[FIRST_CLASS_TOOLS]

| [INDEX] | [TOOL]       | [PROVIDES]                                 |
| :-----: | :----------- | :----------------------------------------- |
|  [01]   | `bash`       | Shell runtime, builtins, `${ }`            |
|  [02]   | `shellcheck` | Static analysis, SC codes                  |
|  [03]   | `bats-core`  | Test framework, TAP output                 |
|  [04]   | `kcov`       | Coverage instrumentation                   |
|  [05]   | `rg`         | Content search, `.gitignore`-aware         |
|  [06]   | `fd`         | File search, `.gitignore`-aware            |
|  [07]   | `jq`         | JSON processing, streaming, `trim`, `skip` |
|  [08]   | `yq`         | YAML processing                            |
|  [09]   | `mlr`        | CSV/TSV/JSON format transforms             |
|  [10]   | `sd`         | Stream editing (sed replacement)           |
|  [11]   | `choose`     | Column selection (cut replacement)         |
