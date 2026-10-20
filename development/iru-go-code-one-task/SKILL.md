---
name: iru-go-code-one-task
description: >-
  Implement a single task from a Go `implementation_plan.md`-style task list — just the implementation and its tests
  — in any Go module: an agent-friendly command-line tool (Cobra, optional Bubble Tea v2 terminal UI) scaffolded by
  `iru-setup-go-cli`, or any other Go library, service or CLI. Detects at runtime the module path and `go` version
  from `go.mod` (and a `go.work` workspace), the `cmd/<bin>/` vs root-`main.go` layout and the `internal/` packages,
  the CLI framework (Cobra, urfave/cli, kong, or none), Bubble Tea/Lip Gloss and their import paths, the test harness
  (standard `testing`, testscript `testdata/script/*.txtar` driven by `TestMain`, teatest, testify/go-cmp if already
  used, container tests behind the `integration` build tag), the golangci-lint config, and `//go:generate`
  directives, then loads only the matching guidance from this skill's own `reference/` directory (always: Go code
  style — Effective Go/Code Review Comments, package naming, `internal/`, small consumer-side interfaces,
  `context.Context` first — and errors — `%w` wrapping, `errors.Is`/`As`/`AsType`, sentinel vs typed errors, exit-code
  mapping in one place; as needed: testing — table tests, `t.Parallel` caveats, golden files with `-update`,
  testscript, Cobra in-process tests, teatest —, the shared CLI contract, Cobra, output/TTY/colour/signals/EPIPE,
  Bubble Tea v2, the catalog's UI contract on Bubble Tea when a task touches the terminal UI — composed sub-models,
  typed intent messages, Bubbles lists/tables rendering only what fits, state × direction × theme UI tests captured as
  `.txt` into `.ui-screenshots/`, asserted accessibility checks at the `.ui-quality.yml` level —, doc comments, security — argv-only `exec.CommandContext`, `--` before operands, `os.Root` —, and
  concurrency — errgroup, cancellation, no leaks). Re-checks the current code state, implements exactly what the task
  specifies, writes/updates the tests next to the code, formats the touched files (`gofmt`/`goimports`) and
  compile-checks with `go build ./...` plus `go vet` on the touched packages (test files included), then — if the
  task didn't stop on a blocker — immediately checks off this task's own checkbox (and its sub-tasks') in
  `implementation_plan.md` with a "group validation pending" note, before handing back a short summary. Does not
  capture a quality baseline, add license headers, audit doc comments beyond the code it writes, or run tests,
  coverage, golangci-lint or govulncheck — those happen once per task group in `iru-go-code-one-task-group`, which
  invokes this skill once per task (in parallel when the group allows it, through `iru-isolated-skill-executor`).
  Invoke as `/iru-go-code-one-task <task description>`, passing the task's own text — including its exact
  `implementation_plan.md` checkbox line(s) — as the argument. For plan tasks tagged `go`.
model: sonnet
allowed-tools: Read Edit Write Bash(go build *) Bash(go vet *) Bash(go version) Bash(go env *) Bash(go list *) Bash(go doc *) Bash(go mod tidy*) Bash(go get *) Bash(go generate *) Bash(gofmt *) Bash(goimports *) Bash(golangci-lint fmt *) Bash(command -v *) Bash(git status *) Bash(git diff *) Bash(git log *) Bash(find *) Bash(grep *) Bash(ls *) Bash(cat *)
---

# Implement one plan task (Go)

Carry out a single task's implementation, tests, and checkbox update in a Go module — nothing else. This is the
narrowest execution unit for a `go` task in the `iru-code` pipeline: `iru-go-code-one-task-group` calls it once per
task in a bucket (potentially many at once, in parallel agents), then handles license headers, doc-comment auditing,
tests, coverage, the race detector, golangci-lint and govulncheck itself, once for the whole bucket. It uses a medium
model on purpose — the plan carries the hard reasoning; this skill executes one task against code agreements that live
in `reference/`.

Two things shape how a Go task is done here:

1. **Logic lives in `internal/` packages, `main` stays thin.** `cmd/<bin>/main.go` only builds a context and calls
   `cli.Main(ctx, args, stdin, stdout, stderr)`; commands are small Cobra constructors over plain, unit-testable
   functions. That's what makes the group's 80%-per-file coverage gate reachable without a TTY, a network, or a
   container — so where code goes is decided first.
2. **A CLI's observable behaviour is its API.** Exit codes, stdout vs stderr, the JSON shapes and the error envelope
   follow `reference/cli-contract.md`; scripts and agents depend on them, so a CLI task changes them only as the task
   says, never renumbers an exit code, and pins every change with a test.

## Step 0 — Detect the project shape once

Settle these from the files, never from assumptions (this skill is copied into other repositories):

- **Module(s)**: the nearest `go.mod` above the task's paths — its `module` path and its `go` directive (the newest
  language/library features you may use) and `toolchain` line; `go version` for the installed toolchain (an older
  installed Go than the `go` line with `GOTOOLCHAIN=local` → "compile-check unavailable", Step 5). A `go.work` at the
  root → a workspace: note every `use` directory; `./...` doesn't cross module boundaries, so build each touched
  module from its own directory. No `go.mod` anywhere → **this isn't a Go module: report it as a blocker** (the task
  was mis-tagged).
- **Layout**: `cmd/<bin>/main.go` (one or more binaries) or a root `main.go` with `package main`; `internal/`
  packages (`internal/cli`, `internal/tui`, `internal/version`, …); a `tools/`/`internal/tools/gendocs` generator;
  `vendor/` (then builds use `-mod=vendor` automatically — never add a dependency without re-vendoring as the task
  says).
- **CLI framework**: `github.com/spf13/cobra` (+ `cobra/doc`), `github.com/urfave/cli/v3`, `github.com/alecthomas/kong`,
  or the standard `flag` package, from `go.mod`'s `require` block. The scaffold's contract files —
  `internal/cli/exitcode.go`, `errors.go`, `output.go`, `term.go`, `signals.go`, `config.go`, `root.go` (the `App`
  type, `(*App).exitCode`, `finishTree`/`wrapRunE`, `a.emit`, `safety(…)`) — tell you how the repository maps errors,
  formats output and decides colour; read the ones the task touches before writing a command. No CLI framework and no
  `package main` → a library/service: the CLI references don't apply.
- **TUI**: `charm.land/bubbletea/v2` / `charm.land/lipgloss/v2` (v2 vanity paths) or the v1
  `github.com/charmbracelet/...` paths — follow whichever the module uses; `reference/bubbletea.md` is v2.
- **Tests**: the assertion style of neighbouring `_test.go` files (standard library, testify, go-cmp); testscript
  (`grep -rn "testscript.Main\|testscript.Run" --include=*_test.go`) and its `Dir` (`testdata/script/`); teatest;
  golden files under `testdata/` and the `-update` flag that refreshes them; `//go:build integration` files
  (container-backed — testcontainers-go).
- **Quality config**: `.golangci.yml`/`.golangci.yaml`/`.golangci.toml` (`version: "2"` → golangci-lint v2; its
  enabled linters, `goimports.local-prefixes`, exclusions), so the code you write passes the group's gate.
- **Generated code**: `//go:generate` directives (`grep -rn "^//go:generate"`) and files carrying
  `// Code generated … DO NOT EDIT.`

## Step 1 — Decide the package(s), then read only the reference material this task needs

A path in the task wins. Otherwise: domain logic and its types → the `internal/<area>` package that owns them; a new
or changed command → `internal/cli/<command>.go` (constructor) calling a plain function (in `internal/cli` or a
domain package); TUI state → `internal/tui`; version metadata → `internal/version`; nothing new in `cmd/<bin>/` beyond
wiring. Genuinely ambiguous → the most specific existing `internal/` package, and say so in Step 8. Record the
**packages touched** — Step 5 derives `go vet` from them.

This skill ships a `reference/` directory next to this file. Read `reference/README.md` first — it is short and routes
you to the rest — then read only what it points at. The routing, restated:

| Read | When |
|---|---|
| `reference/code-style.md` | **Always.** |
| `reference/errors.md` | **Always** for code that returns, wraps, compares, or maps errors (nearly every task). |
| `reference/testing.md` | The task writes or updates tests — nearly every task. |
| `reference/cli-contract.md` | A CLI task adding/changing a command, flag, output, exit code, prompt, or error message. |
| `reference/cobra.md` | A Cobra command, flag, `Args` validator, flag group, completion, or the generated reference/man pages. |
| `reference/output-and-terminal.md` | stdout/stderr writes, `--format`/JSON payloads, Lip Gloss styling, prompts, TTY detection, signals, broken pipes, file writes. |
| `reference/bubbletea.md` | The Bubble Tea model or the command that starts it. |
| `reference/ui-contract.md` + `reference/ui-implementation.md` | The task adds or changes a TUI screen, component, list or other UI. |
| `reference/godoc.md` | A new/changed exported identifier or a new package. |
| `reference/security.md` | Child processes, paths from arguments/env/config, secrets/tokens, network I/O, or a `gosec` finding. |
| `reference/concurrency.md` | Goroutines, channels, `sync`, `errgroup`, timeouts/cancellation, signal handling. |

If `reference/` is missing (the skill directory was copied without it), proceed using the repository's own
`CLAUDE.md` conventions and the surrounding code's style, and say so in Step 8 — don't guess at what the reference
would have said.

## Step 2 — Re-check the current code state

Read the actual current content of every file the task touches before editing — other tasks in the same bucket may be
landing concurrently. For a command, also read `root.go` (global flags, `PersistentPreRunE`, where errors are mapped
to exit codes), the exit-code/envelope files, the command's existing tests and testscript files, and any golden files
it writes: a changed field name or exit code there is an interface change. Note what the surrounding code does about
the things `reference/` has opinions on; a package that consistently does something else wins, and the divergence goes
in Step 8.

## Step 3 — Implement exactly what the task specifies

Apply `reference/code-style.md`, `reference/errors.md`, and whichever optional files Step 1 selected, plus the
repository's own `CLAUDE.md` where more specific. Work in dependency order: domain types/functions → command or TUI
wiring → registration in the root → generator inputs.

Non-negotiable, because a gate or a caller enforces them:

- **No `os.Exit`, `os.Stdout`/`os.Stderr`, `fmt.Println`, or global logger below `cmd/<bin>/`** — write through the
  injected streams (`cmd.OutOrStdout()`/`cmd.ErrOrStderr()`) and return errors; `cli.Main` maps them to exit codes in
  one place (`reference/errors.md`). Results on stdout only; everything else on stderr.
- **Exit codes and JSON are API** — use the existing constants (never a bare number), keep JSON struct fields in
  alphabetical JSON-name order with `schemaVersion`, never rename/remove a field or renumber a code unless the task
  says so (then the golden files and `schemaVersion` change with it).
- **Doc comments** on every exported identifier and package you add (`reference/godoc.md`) — revive and godot fail the
  group's gate otherwise.
- **Context first, argv only** — `ctx context.Context` as the first parameter of anything that blocks;
  `exec.CommandContext` with an argument list and `--` before operands, never `sh -c` (`reference/security.md`).
- **No new module dependency, `go` directive bump, `replace`, or new binary under `cmd/`** unless the task explicitly
  calls for it — a blocker to report (Step 6) otherwise. If it does: `go get <module>@<version resolved live>`, then
  `go mod tidy`, and list the `go.mod`/`go.sum` change in Step 8.
- **Never hand-edit generated code.** If the task changes a `//go:generate` input, run that package's
  `go generate ./<pkg>` and keep the regenerated output.

- **Terminal UI work decomposes first** (`reference/ui-contract.md` §2): write the `Screen › Region › Component` tree
  (inputs, intent messages, visual states, what is reused) before coding, build leaves first, keep raw key messages
  inside the component that owns them, render collections through Bubbles or a windowed slice
  (`reference/ui-implementation.md`), and include the tree in the Step 8 report.

Don't add anything the task didn't ask for — no speculative interfaces, no unrelated cleanup, no restyling.

## Step 4 — Write or update the tests

Follow `reference/testing.md` and the neighbouring test style: table tests next to the code; parallel where safe
(never with `t.Setenv`/`t.Chdir`); `t.TempDir`/`t.Context`; in-process command tests through the repository's
`runCLI`-style helper asserting exit code, stdout, stderr, and the envelope; a new or updated golden file for any
changed JSON output (created/refreshed only through the test's `-update` flag, then read); a `.txtar` script under the
testscript `Dir` when the task adds a command or changes end-to-end behaviour (help, exit code, no-TTY output); pure
`Update` tests (plus a teatest program test when the task asks for one) for the TUI — and, for a screen/component
the task added or changed, the UI tests of `reference/ui-implementation.md` §4–§6: every visual state with
minimal/typical/many-items/long-content and right-to-left fixtures, each captured through
`internal/tui/ui_screenshots_test.go` as `.ui-screenshots/<kind>/<Id>/<state>--<direction>--<theme>.txt` for every
`.ui-quality.yml` direction × theme the TUI has (plus `no-color`), and the asserted accessibility checks at the file's
level. Produce every new exit code on
purpose in the exit-code table. Container-backed tests go in `//go:build integration` files only. Aim the new tests
at ≥ 80% statement coverage of every file you changed — the group gates on it per file.

Do not run the tests — `iru-go-code-one-task-group` runs them once per bucket. A new golden file is therefore written
by hand from the exact output the code produces (compact JSON, keys in struct order, trailing newline from
`json.Encoder`), and the group's test run confirms it; say so in Step 8 so a mismatch is traced back quickly.

## Step 5 — Format and compile-check

A broken build in one task blocks every other task in a parallel bucket from validating. From the module root of each
touched module:

1. **Format only the files you touched**: `gofmt -w <files>`; then `goimports -w <files>` when `command -v goimports`
   finds it (with `-local <module path>` when `.golangci.yml` sets `goimports.local-prefixes`), or
   `golangci-lint fmt <files>` when the repository uses golangci-lint v2 formatters and it's installed.
2. **`go build ./...`** — every package of the module compiles (this also catches a sibling's in-flight breakage).
3. **`go vet <touched packages>`**, e.g. `go vet ./internal/cli ./internal/tui` — vet compiles the `_test.go` files
   too, so it is this skill's test-compile check; add `-tags integration` when you touched an `integration`-tagged
   file.
4. **`go mod tidy`** only when this task added a dependency it was allowed to add (Step 3) — never to "clean up".

No golangci-lint, `go test`, coverage or `govulncheck` here — the group runs them once.

Outcomes:

- **Failure in code this task wrote or edited**: fix it — it's the task's own code, not a finding to defer. Vet
  findings (`printf` verbs, `copylocks`, unreachable code, struct tags) count.
- **Failure outside the task's scope** (a sibling task's in-flight edit, a pre-existing error): don't fix unrelated
  code; re-run once if it looks like a transient race with a concurrently-writing sibling, then note it in Step 8.
- **The toolchain can't run** (no `go`, an installed Go older than the `go` directive with `GOTOOLCHAIN=local`, no
  network for a first module download): report "compile-check unavailable" with the reason — the group's validation
  still catches real errors.

## Step 6 — When to interrupt the user

Keep interruptions rare. Stop and use `AskUserQuestion` (or plain text if no real choice is offered) only when:

- The task is ambiguous in a way that changes correctness or scope and can't be safely inferred.
- The task's approach is infeasible against the real code (it names a package/function that doesn't exist, or demands
  a pattern the framework in use can't express).
- The task needs a new module dependency, a `go` directive bump, a `replace`, a new binary, or a module major-version
  change (a `/vN` import-path change) it didn't ask for.
- The task would change an existing exit code number, rename/remove a JSON field, or make a read-only command mutate
  without saying so — an interface break to confirm, not to slip in.
- The task needs a secret embedded in code, config or `testdata/` (`reference/security.md`) — a design problem to
  report.

Don't stop merely because the task is nontrivial. Don't report the task done to work around a blocker; report it as
blocked (Step 8). A conflict between `reference/` and the surrounding code is not a reason to stop: follow the
surrounding code and report the divergence.

## Step 7 — Check off this task's checkbox now

If this task did not stop on a blocker, update `implementation_plan.md` at the repository root before reporting back.
Re-read it fresh (sibling tasks may be editing it), locate this task's own checkbox line by the exact text passed in,
flip `[ ]` to `[x]` for it and every sub-task the work covered, and add a short note naming the packages and files
touched, e.g.:

```
- [x] Task 3. **Add `list` command with `--limit`/`--cursor`** — internal/cli/list.go, internal/catalog/list.go,
  list_test.go + testdata/script/list.txtar + testdata/list.golden.json; group validation pending.
```

Keep the "group validation pending" wording — `iru-go-code-one-task-group` replaces it with the final outcome. Edit
only this task's own line(s). If this task stopped on a blocker, leave its checkbox untouched.

## Step 8 — Report the outcome

Hand back a short summary:

- **The shape detected** (module path, `go` directive, workspace or not, CLI framework, TUI library and import path,
  test harness: testscript/teatest/golden) and **the packages touched**, with the reference files actually read.
- **The files touched** and **the tests added/updated** per package (not run), including `.txtar` scripts and golden
  files (and whether a golden file was hand-written pending the group's run).
- **The compile-check result**: `go build ./...` and `go vet` per package — passed, failed on this task's code and
  fixed, failed outside this task's scope, or unavailable (and why); which files were formatted and with which tool.
- **For terminal UI work**: the `Screen › Region › Component` decomposition, and the UI tests and captures added
  (component/screen/flow, states × directions × themes, accessibility rule ids checked; not run).
- **Interface changes**: new/changed commands, flags, exit codes used, JSON fields/`schemaVersion`, and whether the
  generated CLI reference/man pages need regenerating.
- **Dependency changes** (`go.mod`/`go.sum`), only when the task allowed them, with the resolved versions.
- **Whether this task stopped on a blocker**, with enough detail for the caller to surface it.
- **Any deliberate deviation from `reference/`**, and pre-existing violations noticed and left alone (`os.Exit` in
  commands, shell-string `exec`, unsorted JSON fields, missing `--` in docs, global command variables).

This skill never captures a quality baseline, adds license headers, runs tests/coverage/golangci-lint/govulncheck,
or starts containers.

## Verification notes

Exercised on 2026-10-16 in `$TMPDIR/iru-verify/cli/go-coding/greeter` (outside this repository) on macOS 27 arm64 with
Go 1.27.2, golangci-lint 2.15.0 and govulncheck, against a CLI shaped like the `iru-setup-go-cli` contract
(`cmd/greeter/main.go` → `cli.Main`; `internal/cli/{root,greet,schema,browse,output,errors,exitcode,term,signal}.go`;
`internal/tui` Bubble Tea model; `internal/version`; `testdata/script/*.txtar`). Module versions resolved live from
proxy.golang.org that day: cobra v1.10.2 (pflag v1.0.9 via cobra; v1.0.10 is latest), `charm.land/bubbletea/v2`
v2.1.0, `charm.land/lipgloss/v2` v2.0.6, `github.com/rogpeppe/go-internal` v1.16.0, `golang.org/x/term` v0.47.0,
`golang.org/x/sync` v0.24.0, `github.com/charmbracelet/x/exp/teatest/v2` v2.0.0-20261012121918-43427fdbad12.
Fallback if a lookup fails: those versions.

- `go build ./...`, `go vet ./...`, `go test -race ./...` (in-process exit-code table, golden JSON, envelope, colour
  policy, prompt policy, EPIPE, signal-cause and panic-recovery tests; pure `Update` tests and a teatest v2 program
  test; a testscript suite) and `govulncheck ./...` were clean; `golangci-lint run` with the v2 config recommended in
  `reference/code-style.md` reported **0 issues** after fixing what it found (unformatted struct, an unused
  `nolint`, an unwrapped `p.Run()` error). Every reference snippet was compiled and exercised in a `snippets/`
  package of the same module.
- Behaviours verified, and recorded in `reference/`: Cobra v1.10.2 runs `ValidateRequiredFlags`/`ValidateFlagGroups`
  **after** `PersistentPreRunE`, so a mutually-exclusive-flags error first classified as INTERNAL (exit 1) until the root
  hook validated them early (now exit 2); `EnablePrefixMatching` defaults to false (`gre` → exit 2 with a suggestion);
  `--` makes `--help` a NAME; `cobra/doc.GenManTree` doesn't create its output directory; an unrecovered panic exits
  **2** (= USAGE), hence the single `recover` in `cli.Main`; real `kill -TERM`/`-INT` gave 143/130; `tool | head -n1`
  dies silently by SIGPIPE (141) by default and returns `EPIPE` (handled as exit 0) when SIGPIPE is ignored; Lip Gloss
  v2 has no per-stream renderer (`colorprofile.Writer` with `NoTTY` strips, `Detect` on a buffer → `NoTTY`);
  testscript v1.16's `Main(m, map[string]func())` re-execution counts toward `-coverprofile -coverpkg=./...`
  (`WithSignals` was covered only through it); teatest's `golden` package registers `-update`, so declaring another
  `-update` in the same test binary panics (`flag redefined: update`); gosec G204 fires on the safe argv
  `exec.CommandContext`; `os.Root` rejects `..`, absolute paths and an escaping symlink; revive `package-comments` and
  `exported` fire on `internal/` packages.
- The scaffold-style testscript wiring (`RequireExplicitExec`, `UpdateScripts: *update`, and a custom
  `status CODE exec …` command built on `ts.Exec` + `*exec.ExitError`) was added to the same module and pins exact
  exit codes (a deliberate wrong expectation failed as `codes.txtar:2: exit status 3, want 4`).
- The verification CLI used the generic `classify`/`started` error mapping; the `iru-setup-go-cli` templates' `App` /
  `wrapRunE` / `exitCode` structure that `reference/` also describes was read from that skill (written concurrently)
  but not built here — its own verification covers it.
- `reference/ui-contract.md` (verbatim catalog copy) and `reference/ui-implementation.md` were added later for the UI
  contract without a Go toolchain on the authoring machine: the APIs they use (`tea.View.Content`,
  `tea.RequestBackgroundColor`/`BackgroundColorMsg.IsDark`, `lipgloss.LightDark`, Bubbles v2 `list.New`/
  `ItemDelegate`, `ansi.Strip`) were checked against pkg.go.dev, the code sketches were not compiled.
- **Not verified**: Windows and Linux hosts (only macOS arm64), a TTY-attached run of `browse` (teatest drives the
  model without a real terminal), urfave/cli and kong projects (detection only), and the per-task skill's own
  end-to-end run inside the `iru-code` pipeline.
