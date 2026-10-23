---
name: cli-output-conventions
description: "Conventions for designing AND testing CLI output so it stays parseable and assertable - exit-code policy (0 success, non-zero failure with stable codes per failure mode), `stdout` for primary data / `stderr` for messages, `--json` / `--plain` for machine-readable output, deterministic ordering and timestamps, `NO_COLOR` / TTY-aware color, `-q` / `--verbose` discipline, and stable `--help` / `--version`. Built on the [Command Line Interface Guidelines][clig]. Use when designing or testing a CLI's output - a new flag, command, or error message, writing CLI assertions, or fixing flaky tests caused by non-deterministic output; it is the assertion contract for `bats-testing` and tells `tui-snapshot-tester` what does NOT need a snapshot."
---

# cli-output-conventions

## Overview

Per [clig][clig]:

[clig]: https://clig.dev/

> "Send output to `stdout`. The primary output for your command
> should go to `stdout`. Anything that is machine readable should
> also go to `stdout`."
>
> "Send messaging to `stderr`. Log messages, errors, and so on
> should all be sent to `stderr`."

Tests can only assert on output that is **stable, separated, and
documented**. This skill defines those conventions; sister skills
(`bats-testing`,
`tui-snapshot-tester`) test
against them.

## When to use

- Authoring or reviewing a CLI's output (any new flag, command,
  or error message).
- Writing tests for a CLI: this skill tells you WHAT to assert
  on; bats / pytest etc. tell you HOW.
- A CLI's tests are flaky / brittle - usually the underlying
  output isn't deterministic. Fix the output, not the assertion.

## Convention 1 - Exit codes

Per [clig][clig]:

> "Return zero exit code on success, non-zero on failure."

> "Map non-zero codes to important failure modes for script
> integration."

```
Exit code | Meaning
----------+----------------------------
0         | Success
1         | General error (catch-all)
2         | Misuse (bad flag, bad usage)
3         | Resource not found
4         | Permission denied
5         | Network / external failure
... documented per CLI
```

**Test pattern:**

```bash
@test "exit 0 on success" {
  run mycli list
  [ "$status" -eq 0 ]
}

@test "exit 2 on bad flag" {
  run mycli --nonexistent
  [ "$status" -eq 2 ]
}
```

Don't test `[ "$status" -ne 0 ]` - assert the **specific** code.
Otherwise refactors silently change the contract.

## Convention 2 - stdout vs stderr

Per [clig][clig]: "This separation ensures piped commands receive
only data, not messages."

```bash
# Good: data on stdout, message on stderr
$ mycli list 2>/dev/null
alice
bob

$ mycli list >/dev/null
fetched 2 users in 0.3s
```

**Test pattern (bats):**

```bash
@test "list emits names on stdout, status on stderr" {
  run --separate-stderr mycli list
  [ "$status" -eq 0 ]
  [ "$output" = $'alice\nbob' ]
  [[ "$stderr" == *"fetched 2 users"* ]]
}
```

`run --separate-stderr` (Bats 1.5+) splits the streams; without
it, `$output` mixes both.

## Convention 3 - Machine-readable mode

Per [clig][clig]:

> "Display output as formatted JSON if `--json` is passed."

> "If human-readable output breaks machine-readable output, use
> `--plain` to display output in plain, tabular text format for
> integration with tools like `grep` or `awk`."

> "Encourage your users to use `--plain` or `--json` in scripts
> to keep output stable."

```bash
$ mycli list --json | jq '.[] | .name'
"alice"
"bob"

$ mycli list --plain
alice  active   2026-04-15
bob    active   2026-04-20
```

**Test pattern:** assert against `--json`, never against the
human-formatted default. Human output is allowed to evolve;
JSON is the contract.

```bash
@test "list --json contract" {
  run mycli list --json
  assert_success
  echo "$output" | jq -e '.[0] | has("name") and has("status")'
}
```

## Convention 4 - Determinism

Stable output for tests requires:

- **No timestamps** in default output (only with `--verbose` or
  human-mode banner).
- **Stable ordering** - sort lists by a canonical key, not insertion
  order.
- **No random IDs** in output unless documented.
- **Locale-independent number formatting** in `--json` /
  `--plain` (no thousand separators; ISO 8601 dates).

```bash
# Bad: randomized order, locale-dependent date
$ mycli list
bob   2026/04/20
alice 2026/04/15

# Good: sorted, ISO 8601
$ mycli list --plain
alice 2026-04-15
bob   2026-04-20
```

**Test pattern:** golden-file comparison with sorted output.

## Conventions 5-8 - color/TTY, verbosity, `--help`/`--version`, documenting the contract

The remaining four conventions and their bats test patterns are in [references/conventions-5-8.md](references/conventions-5-8.md).

## Anti-patterns

| Anti-pattern                                                          | Why it fails                                                              | Fix |
|-----------------------------------------------------------------------|---------------------------------------------------------------------------|-----|
| Tests assert `status -ne 0`                                            | Refactors silently change error code; scripts break.                    | Assert specific code (Convention 1). |
| Errors on stdout                                                       | Pipes carry error text into downstream parsers.                        | stderr (Convention 2). |
| Tests assert against default human output                              | Human output evolves; tests churn.                                      | Test against `--json` (Convention 3). |
| Timestamps in default output                                           | Tests fail on every run.                                                | Verbose-mode only (Convention 4). |
| ANSI codes leak when piped                                             | `wc -l`, `grep`, etc. break.                                           | TTY check + `NO_COLOR` (Convention 5). |
| Progress bars in CI                                                    | CI logs flooded; tests can't assert frame counts.                      | TTY check (Convention 5). |
| Help output requires network / config                                 | `--help` should always work.                                            | Help is local + static. |
| `--version` mixed with marketing                                       | Tooling can't parse.                                                    | Pure version string (Convention 7). |

## Limitations

- **Legacy CLIs.** Adopting this skill against an existing CLI
  requires a deprecation cycle for output changes.
- **Verbose / debug modes are inherently non-deterministic.**
  Don't snapshot them; assert presence of key markers.
- **Cross-shell quoting.** Bats runs in Bash; PowerShell tests
  via Pester need their own assertions.
- **Color contract is OS-dependent.** Windows terminal emulators
  have different ANSI support; test on the target platforms.

## References

- [clig][clig] - Command Line Interface Guidelines: exit codes,
  stdout / stderr, `--json` / `--plain`, `NO_COLOR`, `-q` /
  `--verbose`, `--help` / `--version`.
- `https://no-color.org/` - `NO_COLOR` informal standard.
- ISO 8601 - date / time format for `--json` output.
- `bats-testing` - Bash-based
  assertion runner that consumes this contract.
- `tui-snapshot-tester` - 
  layout-level snapshots; this skill covers text-level contract.
