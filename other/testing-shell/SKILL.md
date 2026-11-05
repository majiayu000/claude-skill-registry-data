---
name: testing-shell
description: Test Bash scripts with BATS — @test blocks, setup/teardown, run + $status/$output assertions, stubbing commands, temp dirs. Use for hooks, CI helpers, setup scripts and GHA scripts.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Grep, Glob, Edit, Write, Bash
  argument-hint: "[script-or-test-path]"
  stability: experimental
---

# Testing Shell Scripts (BATS)

**Target**: $ARGUMENTS

Writes [BATS](https://github.com/bats-core/bats-core) tests for Bash scripts, test-first. For the
Red-Green-Refactor loop itself, see `tdd-core:testing-tdd`; for how the scripts under test should be
written, see `implementing-shell`.

## When to Use

- A script has logic worth pinning down: argument handling, branching, exit codes, file output
- Hook scripts, CI helper scripts, setup/install scripts, GitHub Action `scripts/*.sh`

## Do Not Use

- One-line wrappers with no branching — a ShellCheck pass is enough
- Testing what another tool already guarantees (e.g. that `jq` parses JSON)

## Layout

```text
scripts/do-thing.sh
tests/unit/do-thing.bats      # one .bats file per script
tests/unit/fixtures/          # static inputs (sample JSON, config files)
```

Run with `bats tests/unit/` (add `--tap` in CI if a TAP consumer reads it).

## Workflow

1. **RED** — write the `@test` blocks for the behaviour you want, including the failure paths
   (missing argument, bad input, missing dependency). Run them; they must fail.
2. **GREEN** — implement the script until they pass.
3. **REFACTOR** — tidy the script with the tests green; run ShellCheck on script and tests.

## Core patterns

```bash
#!/usr/bin/env bats

setup() {
  SCRIPT="$BATS_TEST_DIRNAME/../../scripts/do-thing.sh"
  TMP="$BATS_TEST_TMPDIR"          # per-test temp dir, removed by bats
}

@test "prints usage and exits 2 without arguments" {
  run bash "$SCRIPT"
  [ "$status" -eq 2 ]
  [[ "$output" == *"Usage:"* ]]
}

@test "writes the report to the given path" {
  run bash "$SCRIPT" --out "$TMP/report.txt"
  [ "$status" -eq 0 ]
  [ -s "$TMP/report.txt" ]
}

@test "DRY_RUN=1 changes nothing" {
  DRY_RUN=1 run bash "$SCRIPT" --out "$TMP/report.txt"
  [ "$status" -eq 0 ]
  [ ! -e "$TMP/report.txt" ]
}
```

- `run` captures `$status`, `$output` and `${lines[@]}`; assert on them **after** `run`, never
  inside the command.
- Feed stdin with `run bash -c '"$0" < "$1"' "$SCRIPT" "$fixture"` or a here-string inside
  `bash -c`; `run` itself does not take a redirect.
- `setup_file` / `teardown_file` for expensive one-time setup; `setup` / `teardown` per test.

## Stubbing external commands

Put fake binaries first on `PATH` so the script never calls the real `gh`, `curl` or `git push`:

```bash
setup() {
  mkdir -p "$BATS_TEST_TMPDIR/bin"
  printf '#!/usr/bin/env bash\necho "$*" >> "%s/gh.calls"\n' "$BATS_TEST_TMPDIR" \
    > "$BATS_TEST_TMPDIR/bin/gh"
  chmod +x "$BATS_TEST_TMPDIR/bin/gh"
  PATH="$BATS_TEST_TMPDIR/bin:$PATH"
}

@test "opens the PR against main" {
  run bash "$SCRIPT" feature-x
  [ "$status" -eq 0 ]
  grep -q -- "--base main" "$BATS_TEST_TMPDIR/gh.calls"
}
```

To test "dependency missing" paths, run with a `PATH` that only holds the stubs you want present.

## CI wiring

```yaml
- run: sudo apt-get install -y bats shellcheck
- run: shellcheck scripts/*.sh
- run: bats tests/unit/
```

Pin any third-party setup action by commit SHA, as the repo's other workflows do.

## Quality Check

- Every exit path the script documents has a test (success, usage error, dependency missing)
- No test touches the network, the real `$HOME`, or files outside `$BATS_TEST_TMPDIR`
- `bats tests/unit/` and `shellcheck` both pass before the PR
