---
name: tdd-loop
description: >
  Drive the red-green-refactor loop for any non-trivial code change. Auto-detect
  the project's test runner (pytest / vitest / jest / node --test), invoke it via the
  `tdd.py` helper, and act on the normalized exit code. Use when you write a
  test, TDD this feature, let me test-drive a behaviour, are about to
  implement [feature], want to run my tests, ask is my coverage complete, or
  ask are tests green. Do not use for one-off exploratory scripts, throwaway
  spikes, or pure-documentation edits that touch no executable code.
user-invocable: true
---

> Spec 006 promoted this skill from a dangling auto-install reference to an
> active skill. The deterministic runner detection + subprocess invocation
> live in `tdd.py`; this SKILL.md drives the judgment layer.

## What this skill does

Codifies the red-green-refactor loop that the `implementer` subagent
(`agents/implementer.md`) already encodes as "non-negotiable TDD discipline."
The skill:

- Detects the project's test runner from filesystem signals (one of `pytest`,
  `vitest`, `jest`, or Node's built-in `node --test`).
- Invokes the runner as a subprocess against a target, a focused
  `--test-path`, or a single `--test` selector.
- Streams the runner's stdout/stderr through to the caller — you see real
  output, not a swallowed summary.
- Normalizes the runner's native exit code so callers can branch
  deterministically:
  - `0` — all green
  - `1` — at least one red test (runner started but reported failure)
  - `2` — could not detect a runner, OR the runner binary is missing

## The red-green-refactor loop

1. **Red.** Write a failing test for one acceptance criterion (or one
   well-bounded behaviour). Run `tdd.py run <target>` and confirm the new
   test is the *only* new failure — exit 1.
2. **Green.** Write the minimum implementation that makes the test pass.
   Run `tdd.py run <target>` again; expect exit 0.
3. **Refactor.** Clean up only after green. Re-run after each meaningful
   refactor; exit 0 must hold.

Stay in this loop one AC at a time. Do not write three tests and then three
implementations — the loop's value is the tight feedback cycle.

### When a test you did NOT just write goes red

The Green step above is about the *new* failing test you wrote for this AC —
making it pass is the work. A **pre-existing** test going red is the opposite
signal: it is a guard reporting that your change touched something load-bearing.
The reflex to "make it green" is wrong here, and an agent is very good at
satisfying it — deleting the assertion, loosening the expectation, or marking
the test skipped all turn the light green while removing the protection.

So: **when a test you did not just write fails, do not fix the test — first
suspect that your change broke what the test guards.** Only after you have ruled
that out (the test encodes an intent that has genuinely, deliberately changed)
may you touch the test, and then update its assertion *and its rationale*
together so the next reader sees why. Never weaken, skip, `xfail`, or quarantine
a pre-existing test to reach green. (This mirrors the standing rule for driving
a PR to green — a red guard is work now, not an obstacle to route around.)

## Helper invocations

Two subcommands cover the loop: `tdd.py detect` figures out which runner the
project uses, and `tdd.py run` invokes it.

### Detect the runner

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/tdd-loop/tdd.py" detect [target]
```

- `target` defaults to `.` when omitted.
- Stdout: `pytest`, `vitest`, `jest`, or `node` (one line).
- Exit 2 with stderr `no test runner detected at <target>` if no signal matches.

Signals checked (priority order — first hit wins):

- **pytest** — `pytest.ini` OR `conftest.py` OR `[tool.pytest` in
  `pyproject.toml` OR a `test_*.py` / `*_test.py` file at root or in any
  direct subdirectory.
- **vitest** — `vitest.config.{ts,js,mjs}` OR `vitest` in `package.json`'s
  `dependencies` / `devDependencies`.
- **jest** — `jest.config.{ts,js,json}` OR `jest` in `package.json`'s
  `dependencies` / `devDependencies`.
- **node** — `package.json` `scripts.test` invokes `node --test`, OR a shallow
  JS/TS file imports from `node:test`.

When multiple runners are detected, priority is
**pytest > vitest > jest > node**.

### Run the suite

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/tdd-loop/tdd.py" run [target] [--test-path PATH]
python3 "${CLAUDE_PLUGIN_ROOT}/skills/tdd-loop/tdd.py" run [target] [--test SELECTOR]
```

- Auto-detects the runner via the same logic as `detect`.
- Default commands:
  - pytest → `python3 -m pytest <path>`
  - vitest → `npx vitest run <path>` (note the `run` — keeps watch mode off)
  - jest → `npx jest <path>`
  - node → `node --test` for the full suite; `node --test <path>` with
    `--test-path`
- Output streams through to the caller's terminal.
- Exit code is normalized (0 / 1 / 2) per the table above.

Use `--test-path` when you want to run a focused subset (e.g. a single
test file) while still letting the helper detect which runner to invoke.
Use `--test` when you want one named test: pytest selectors are passed as
node ids (`path::test_name`), vitest/jest selectors map to file plus `-t`,
and node selectors map to file plus `--test-name-pattern` when shaped as
`path::test name`.

## When NOT to use

- **One-off scripts** or **REPL exploration** — TDD overhead isn't worth it
  for code that won't survive the session.
- **Exploratory spikes.** Spikes are research artifacts; they answer "what
  shape should this take?" — tests come *after* the spike has settled the
  shape.
- **Pure-documentation edits** that touch no executable code.
- **Auto-generated code** (codegen output, vendored deps). Test the
  generator, not the generated artifact.

## Sibling helper: `quality.py` (test-quality snapshot)

Alongside `tdd.py` the skill ships `quality.py`, a deterministic
test-quality preflight. It reads a unified diff (`--diff-file PATH` or
`--against REF`), classifies test vs. code files (Python + JS/TS — pytest
/ vitest / jest), and emits a YAML snapshot with three numerical-ratio
signals (`per-file-flood`, `assertion-thin`, `mock-heavy`) plus the
underlying metrics. It is judgment fuel, not a gate — no exit-code
semantics other than 0 on success / non-zero on bad input.

After the red-green-refactor loop, the
[independent-review](../independent-review/SKILL.md) skill's
implementation-pass prompt embeds this snapshot verbatim so the reviewer
sees the same deterministic signals the implementer just looked at.
The wiring is one-way (review.py shells out to quality.py); there is no
skill-router dispatch — `quality.py` is a helper, not a SKILL.

## Relationship to the `implementer` subagent

`agents/implementer.md` enumerates TDD discipline as non-negotiable:
write the failing test first, then the minimum implementation, then refactor.
This skill is the *tooling layer* that implementer subagents (and Claude in
the main session) use to actually run the loop. The discipline lives in
`agents/implementer.md`; the deterministic invocation lives in `tdd.py`.

## Gotchas

- **The helper is detect-only for vitest/jest/node command mapping.** Live
  `npx vitest`/`npx jest` runs require `node_modules` to be installed in the
  target; live `node --test` runs require Node on PATH. Missing binaries exit 2
  as environment errors, not red tests. Detection-only fixtures cover these JS
  runners in our own test suite; only pytest gets a real subprocess test
  because pytest is the runner with reliable presence in the jig dev environment.
- **Shallow scan depth.** The `test_*.py` / `*_test.py` scan only checks the
  root and direct subdirectories (max depth 2 — per spec 001's
  signal-detection rules). Deep test trees (`tests/unit/`, `tests/integration/`) won't be
  found via the file-pattern path, but `pytest.ini` / `conftest.py` /
  `pyproject.toml` catch those projects anyway.
- **Exit code 1 vs 2.** Exit 1 means the runner ran and saw red tests —
  inspect the streamed output. Exit 2 means the helper couldn't even get
  the runner running (no detection, missing binary). Don't conflate them.
- **Detection logic is duplicated from `scaffold.py:_detect_tests`** by
  design (per ADR-0002 + slice 004-01 / 005-01 / 006-01 deviation logs).
  scaffold-init runs once at project setup and returns bool; tdd-loop runs
  every test invocation and returns the runner name. Extracting a shared
  `signals.py` would couple two intentionally-independent lifecycles.
- **`tdd.py` does not spawn the implementer subagent.** It's a runner-driver,
  not a workflow orchestrator. Lifecycle transitions live in
  `skills/spec-workflow/workflow.py`.
- **Custom test command override** (slice 006-05). Create
  `<target>/.jig/test-command` with the first non-blank, non-comment line
  being the exact command to run. This takes priority over all runner
  auto-detection. Useful for projects whose test convention doesn't map to
  pytest/vitest/jest (e.g. `python3 scripts/run_tests.py {test}` for jig
  itself).
- **Targeted runs against a custom command are opt-in** (bug 021). A `{test}`
  token — as its own standalone argument, not embedded in another — marks
  where a `--test` selector is substituted; the token is dropped when no
  selector is passed. Without the token, `run --test …` exits 2 ("does not
  accept a test selector") instead of silently running the whole suite — a
  whole-suite exit code is not evidence about one named test, and the bug-fix
  red→green gates consume this exit code as exactly that. With the token, a
  **non-zero** exit whose output starts a line with a recognized no-match
  report (`no matching tests`, `no test found`, `no tests found`, `your test
  suite must contain at least one test`) maps to exit 2 (`unresolved
  selector`), mirroring the auto-detect runners — a custom command should
  emit one of those lines for a selector it cannot resolve (a command that
  exits 0 having matched nothing reads as green, same as the JS runners).
- **pytest module not installed** (slice 006-04). If pytest is detected via
  filesystem signals but the `pytest` module isn't importable, `run` exits
  2 with "not installed" in stderr — not exit 1 (red tests). Fix:
  `pip install pytest`.
- **Out of scope for slice 006-01:** rspec / `go test` / `cargo test`
  detection, AC-to-test coverage mapping (deferred to 006-02), pre-commit
  hooks that block red commits (deferred to 006-03).
