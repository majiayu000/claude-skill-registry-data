---
name: verify
description: |
  Verify that a code change actually does what it's supposed to by running it and
  observing real behavior — not just by reading the diff. Run the project's tests and,
  where it makes sense, exercise the app/CLI/endpoint the change touches. Use when asked
  to "verify", "confirm the fix works", "test this change", "make sure it runs", or as
  the verify stage of a ship pipeline. Reports concrete evidence (commands + output).
license: MIT
metadata:
  author: Nicholas Sollazzo
  version: "3.0.0"
---

# Verify — prove the change works by running it

Confirm the change behaves as intended by **executing** it and observing the result. A
green read-through is not verification; a green *run* is. Produce evidence (the exact
commands and their output) so the result is checkable, not asserted.

> **Portability note.** Needs a shell to run the project's own commands. It does NOT
> assume any specific test framework, language, or harness tool — it discovers the
> project's recipe. Prefer a richer native `verify` skill if your harness ships one.

> **Sub-agents.** Verification is mostly **sequential** — test suites and a single app boot
> share ports, build artifacts, and DB state, so running them in parallel sub-agents tends to
> collide. Use a sub-agent only for genuinely independent work (e.g. an independent
> reproduction of the bug while the main suite runs), and don't parallelize the suite itself
> unless the project's own tooling is built for it.

## Workflow

1. **Find the project's recipe first.** The repo's own conventions beat any generic
   guess (this is a hard rule — see below). Look, in order, for:
   - A project skill / runbook for running or testing the app.
   - `CLAUDE.md` / `AGENTS.md` / `README` "test" or "run" instructions.
   - Scripts in `package.json`, `Makefile`, `justfile`, `pyproject.toml`, `cargo` config,
     `go.mod`, CI workflow files (`.github/workflows/*`) — CI shows the real commands.
2. **Run the tests** the project defines (e.g. `npm test`, `pytest`, `cargo test`,
   `go test ./...`, `make test`). Capture pass/fail and the summary line.
3. **Exercise the change at runtime** when it's user-facing and feasible: start the
   server and hit the touched endpoint, run the CLI subcommand, render the component,
   reproduce the original bug and confirm it's gone. For pure docs/config changes with no
   runtime surface, tests (or a lint/build) are sufficient — say so.
4. **Report evidence.** State exactly what you ran and what you observed. Quote the
   relevant output. Distinguish "tests pass" from "I also exercised the feature and saw X".

## Gate (when used in a pipeline)

- **Pass** → report the evidence and continue.
- **Fail** → **STOP and fail loud.** Report the failing command and its output verbatim.
  Never report "verified" when something errored, and never silently skip a step. A
  skipped step (e.g. "no runtime check because docs-only") must be named as skipped with
  the reason.

## Rules

- **Run, don't predict.** Ground every claim in actual command output.
- **Project recipe overrides the generic one.** If the repo runs tests in CI / a
  container / a remote host rather than locally, follow that — don't invent a local run.
- **Honesty over green.** Surfacing a real failure is the whole point; hiding one defeats it.
