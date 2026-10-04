---
name: feature-delivery
description: Deliver one scoped feature end-to-end tests, implementation, verification, and completion report. Portable, language-agnostic. Use when a task must be implemented and shipped.
triggers:
  - feature delivery
  - implement feature
  - deliver this task
  - finish implementation
tools:
  - read_file
  - list_dir
  - grep
  - glob
  - find_references
  - write_file
  - search_replace
  - run_command
---

<!-- Provenance: generic, portable. It names no fixed language or project toolchain. -->

# Feature Delivery

## Purpose

Deliver one scoped feature end-to-end: tests, implementation, verification, and an honest completion report. This skill is the **portable, language-agnostic** delivery skill. A repository may also provide a project-bound delivery or contract skill with mechanical gates. When one exists and the feature is within its scope, prefer it for mechanical gates; use this skill when no project-specific contract applies, or for the reasoning, scope discipline, and report it provides.

## Read First

- The task or feature slice named by the user, and any acceptance criteria attached to it.
- Workspace conventions for contributing, testing, and tooling (for example a contributing guide, root build scripts, or manifest files) when they exist.
- Any project-specific contract, quality config, or delivery skill present in the workspace, when one applies to the change.

## Method

1. Lock scope to one feature slice (production paths + tests). Do not broaden.
2. Write or update tests for success and at least one error or negative path first or alongside code.
3. Implement the smallest change that satisfies the scope.
4. Discover the project's focused test command and linter or type-checker from the workspace, then run them for the touched scope. Examples by ecosystem, selected by what the workspace actually declares: `pytest` (Python), `npm test` (Node), `cargo test` (Rust), `go test` (Go), `mvn test` (JVM), alongside the matching lint and/or type-check. If the workspace declares a Makefile, task runner, or root test script, prefer the project's own entry point over a hand-picked command.
5. Run any project-specific contract or quality gates whose scope overlaps the change, when they exist in the workspace.
6. Apply security checks before claiming done: scan for hardcoded secrets, confirm path safety for any filesystem writes, and verify fail-closed defaults on new guards. When a dedicated security-review skill is available in the workspace, run it; otherwise apply these checks inline.
7. When the change parses or decodes untrusted structured input (for example config, frontmatter, CLI schema, or tool parameters), add malformed, empty, oversized, and duplicate-input cases. Run the project's native fuzzer when a deterministic fuzz target is practical (for example `go test -fuzz`, `cargo fuzz`, a pytest fuzzing harness, or a jest fuzz target), bounded to a short duration; otherwise state why it was not run.
8. Emit a completion report only for actual progress; no invented metrics.

## Rules

- Do not bypass pre-commit or Git hooks. Do not suppress static-analysis findings. Do not leave unresolved TODO/FIXME/HACK/XXX drift markers in committed code or agent config.
- Do not default to one OS process per concurrent agent task; prefer in-process concurrency.
- Severity never gates approval; open gaps block `PASS`.

## Report shape

When a resource catalogue and its scoped reader are available, load
`report-template` before producing the delivery report. Without that capability,
use the inline report shape below.

### Result

`PASS`, `BLOCK`, `PARTIAL`, or `NOT_RUN`.

### Scope

- the single feature slice delivered and the files touched;
- tests added or updated (success and negative paths).

### Verification

- the discovered test command, linter, and/or type-checker actually run (with exit status and summarized result, not full successful output);
- any project-specific contract or quality gate run, or listed as not run only when it was required and could not execute.

### Fuzz

- the malformed/oversized/duplicate cases added, and the fuzz target run (or why it was not practical).

### Remaining gaps

- unresolved implementation, test, verifier, or security gap; or `None identified within the executed scope`.

Result semantics:

- `PASS` - scoped feature implemented, verified, gaps closed, and ready for the requested handoff.
- `BLOCK` - implementation, test, verifier, or security gap remains.
- `PARTIAL` - a useful slice landed but a named dependency or user decision remains; or a required project-specific gate could not execute and the implementation cannot be fully verified without it.
- `NOT_RUN` - plan only or delivery could not start.

Keep the report concise. Do not paste complete successful logs.
