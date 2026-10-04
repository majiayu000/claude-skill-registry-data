---
name: review-pre-commit
description: Use as a pre-commit quality gate — review the working diff for stub patterns (TODO/FIXME/`unimplemented!()`/`todo!()`), debug leftovers (`dbg!`, stray `console.log`/`println!`, commented-out code), then run the project's lint, format, and test suites and verify the active task has a handoff annotation. Prints a PASS/FAIL checklist. Trigger when the user says "review my changes", "/review", "ready to commit?", or asks for a final pass before committing.
---

# Review — pre-commit quality gate

You are about to commit. Run through this structured review to catch issues before they land.

## 1. Review full diff

```bash
git diff HEAD
```

Read through every change. Look for:

- Correctness: does the logic do what it should?
- Edge cases: are boundary conditions handled?
- Security: any injection, hardcoded secrets, or unsafe patterns?

## 2. Scan for stub patterns

Search the diff for patterns that indicate incomplete work:

- `TODO`, `FIXME`, `HACK`, `XXX`
- `pass` (Python), `unimplemented!()` / `todo!()` (Rust)
- `throw new Error("not implemented")`
- Empty function bodies or placeholder returns
- `...` as implementation

If found: fix them now. Do not commit stubs.

## 3. Check for debug leftovers

Search for debug code that shouldn't be committed:

- `dbg!()` (Rust)
- `console.log` used for debugging (not logging)
- `print(` / `println!` used for debugging
- Commented-out code blocks (more than 2 consecutive commented lines)

If found: remove them.

## 4. Run lint and format checks

Detect the project's toolchain and run the appropriate checks:

**Rust** (if `Cargo.toml` exists):

```bash
cargo clippy -- -D warnings
cargo fmt --check
```

**Node/TypeScript** (if `package.json` exists):

```bash
npx eslint . 2>/dev/null || npm run lint 2>/dev/null
```

**Python** (if `pyproject.toml` or `requirements.txt` exists):

```bash
ruff check . 2>/dev/null || uv run ruff check . 2>/dev/null
```

**Go** (if `go.mod` exists):

```bash
go vet ./...
gofmt -l .
```

**Elixir** (if `mix.exs` exists):

```bash
mix format --check-formatted
mix credo --strict
```

Fix any issues found before proceeding.

## 5. Run test suite

Run the project's test suite:

- Rust: `cargo test`
- Node: `npm test`
- Python: `uv run pytest` or `pytest`
- Go: `go test ./...`
- Elixir: `mix test --seed 0`

All tests must pass before committing.

## 6. Verify handoff annotated

Check that the active task has a handoff annotation, per the taskwork convention:

```bash
task project:<repo> +ACTIVE list
```

If working on a task, verify it has annotations covering the work:

```bash
task <id> information
```

## 7. Print checklist

Print a pass/fail summary:

```
Review checklist:
  [PASS] No stub patterns
  [PASS] No debug leftovers
  [PASS] Lint clean
  [PASS] Format clean
  [PASS] Tests pass
  [PASS] Handoff annotated

Ready to commit.
```

If any items fail, fix them first, then re-run the failed checks.

Once all checks pass, run `git commit` and annotate the task: `task <id> annotate "handoff: ..."`.
