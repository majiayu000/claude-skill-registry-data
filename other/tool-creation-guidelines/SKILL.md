---
name: tool-creation-guidelines
description: Best practices for creating developer tools and scripts in this project. Use when planning or reviewing tools that parse, analyze, or transform code.
user-invocable: false
---

# Tool Creation Guidelines

Best practices for creating developer tools and scripts in this project. These apply to tools in `tools/` and `scripts/` directories.

## Tool-first philosophy

**Tools are the default, not the exception.** If you perform a task manually more than once, build a tool. Even for tasks that require thought and judgment, build "groundwork" tools that gather data, structure inputs, and present summaries — so the orchestrator can spend its effort on reasoning rather than mechanical data collection.

Examples of groundwork tools:
- A tool that scans Eva's recent comments and presents structured output (saves API query construction)
- A tool that diffs Google docs properties against codebase implementations (saves manual comparison)
- A tool that summarizes PR changes with relevant context (saves reading raw diffs)
- A tool that checks all startup checklist steps and reports only anomalies (saves running each step manually)

**Do not gate tool creation on frequency alone.** A tool that saves 2 minutes per cycle pays for itself within a few cycles. The cost of building a small Rust tool is low; the cost of not building it compounds across every future cycle.

## Use AST parsers, not regex

**When parsing source code (PHP, TypeScript, or any language), always use established AST parsing libraries** instead of regex-based string matching. This is a firm project convention (Eva directive #378).

### Why

- Regex is fragile against formatting changes (whitespace, comments, multiline constructs)
- Regex cannot handle nested structures reliably (brackets, generics, unions)
- Regex reinvents parsing that battle-tested libraries already solve
- AST parsers handle edge cases (e.g., `extends` clauses, complex type annotations) that regex misses

### Available parsers in this project

| Language | Parser | Package | Notes |
|----------|--------|---------|-------|
| TypeScript | TypeScript Compiler API | `typescript` (already installed) | Use `ts.createSourceFile()` to parse TS/JS files |
| PHP | php-parser (glayzzle) | `php-parser` (dev dependency) | Pure JS PHP 8.x parser |

### What NOT to do

- Do NOT use regex to extract class declarations, constructor parameters, interface properties, enum cases, or type annotations from source files
- Do NOT write custom bracket-depth-tracking string splitters (e.g., `splitTopLevel()`) — the AST handles nesting correctly
- Do NOT parse `PROPERTY_MAP` or `A_SCHEMA_TYPE` constants with regex when an AST gives you structured constant declarations

### When regex is acceptable

Regex is fine for:
- Simple pattern matching in output/log text (not source code)
- Filtering file names or paths
- Post-processing already-extracted string values (e.g., normalising type names)

## Rust tools

For tools that don't need source code parsing (JSON processing, state verification, report generation, API query automation), **Rust is the preferred language**. Rust tools:
- Run in the orchestrator sandbox (`bash tools/<name>` and `cargo *` are both allowed)
- Avoid the sandbox restrictions that block tools like `jq -f`
- Compile to fast, standalone binaries with no runtime dependencies
- Live in the `tools/rust/` Cargo workspace

See the **rust-tooling** skill for the full workflow (workspace structure, shell wrappers, conventions).

## Tool quality assurance (per Eva directive #516)

**Tools we rely on must be high quality.** PR #514 demonstrated that a fail-open bug in the `cycle-status` tool's commit-freeze check went undetected through initial development and review. If we rely on a tool to enforce a safety invariant, the tool itself must be built and reviewed to a higher standard than ad-hoc scripts.

### Fail-safe by default

Safety-critical tools (those that gate decisions like "is it safe to publish?" or "is the commit freeze intact?") MUST fail-closed:

- **If a check cannot be performed, report failure** — not success. A tool that says "all clear" when it can't actually verify anything is worse than no tool at all.
- **Distinguish "check passed" from "check could not run".** Use explicit status fields (e.g., `check_failed: bool`) or error states, not just `pass: true/false`.
- **Validate inputs before using them.** If a tool reads a commit SHA from state.json and passes it to `git`, validate the format first. If a tool reads a file path, verify it exists.

### Adversarial testing requirements

Every tool issue spec MUST include error-path test cases. The happy path is easy; bugs hide in error paths.

**Minimum test coverage for dispatched tool work:**

1. **Happy path** — the tool works correctly with valid inputs
2. **Invalid input** — malformed data, missing fields, empty strings, unexpected types
3. **External command failure** — if the tool shells out to `git`, `gh`, etc., test what happens when those commands fail (non-zero exit, no output, timeout)
4. **Edge cases** — boundary values, empty collections, single-element collections
5. **Safety invariant** — for safety-critical tools, explicitly test that failure modes produce the conservative (fail-closed) result

Include these in every agent issue spec:

```markdown
### Required test cases

1. Happy path: [describe expected behavior]
2. Invalid input: [describe what should happen with bad input]
3. Command failure: [describe fail-closed behavior]
4. Edge case: [describe boundary conditions]
```

### Tool review checklist

When reviewing a tool PR (whether from the coding agent or self-authored), verify:

- [ ] **Error paths fail-closed** — every `Err`, non-zero exit, or missing data case produces the conservative result
- [ ] **No silent swallowing** — errors are logged/reported, not silently ignored
- [ ] **Input validation** — external inputs (state.json values, CLI args, API responses) are validated before use
- [ ] **Test coverage** — unit tests exist for both happy and error paths
- [ ] **Output format** — both `--json` and human-readable output reflect the new behavior
- [ ] **Action items** — if the tool produces action items, error states generate appropriate (different) action items from success states
- [ ] **Deprecation warnings** — no use of deprecated APIs (e.g., `chrono::Duration::hours()` → `TimeDelta::try_hours()`)

### Tool maintenance

Existing tools accumulate debt as their environment changes. Every 10 cycles (during the tool audit):

1. **Run each tool's test suite** — `cargo test -p <tool-name> --manifest-path tools/rust/Cargo.toml`
2. **Check for deprecation warnings** — `cargo build 2>&1 | grep -i deprecat`
3. **Review error paths** — are they still fail-closed? Has any refactoring introduced fail-open behavior?
4. **Check for new edge cases** — has the data the tool processes changed in ways the tool doesn't handle?

## Verification anti-pattern: tools must not compensate for what they verify

**Verification and validation tools must check outcomes, not create them.** A verification tool must never contain workarounds, fallbacks, or compensating logic for the conditions it is testing. If a verification tool needs a workaround to pass, the root cause must be fixed instead.

This anti-pattern was discovered in `scripts/verify-build.mjs`, which contained logic to copy `../dist` into `dist` before checking the build output — masking a broken `tsup.config.ts` for 20+ cycles. The tool reported PASS despite the build configuration being incorrect.

**When reviewing verification/validation tools, flag:**
- File copy/move operations that "fix" the layout before checking it
- Default values substituted for things being verified
- Fallback paths that compensate for misconfiguration
- Any logic that creates the conditions it then checks

This applies to all tools in `scripts/` and `tools/` that perform verification, validation, or assertion.

## General tool principles

1. **Use existing dependencies first.** Check `package.json` and `composer.json` before adding new packages. TypeScript is already installed — its compiler API is available for free.
2. **Rust for non-AST tools.** For JSON processing, state verification, or report generation, prefer Rust (`tools/rust/crates/`) over jq or shell scripts. Rust tools can run in the orchestrator sandbox; `jq -f` and complex shell constructs cannot.
3. **Ask Eva for help.** If you need new dependencies installed, workflow changes, or permissions — create an issue. Eva is part of the team.
4. **Keep tools focused.** One tool, one purpose. Don't combine unrelated analyses into a single script.
5. **CI-ready exit codes.** Tools should exit 0 on success, non-zero on failure. This enables CI integration.
6. **Preserve output format.** When rewriting a tool's internals, keep the same output format unless there's a specific reason to change it.
7. **Dispatch tool-building to the coding agent.** For non-trivial tools, create an issue spec describing the tool's purpose, inputs, outputs, and constraints, then assign it to the Copilot agent. The agent can build Rust tools, TypeScript analysis scripts, and pipeline components.

## Pipeline composition

Tools should be designed to compose into pipelines:

- **Structured output**: Tools should support `--json` output for machine consumption alongside human-readable output.
- **Exit codes**: Exit 0 on success, non-zero on failure. Pipelines can short-circuit on failure.
- **Consistent `--repo-root` convention**: All tools accept `--repo-root <path>` to locate repo files.
- **Idempotent**: Running a tool twice with the same inputs should produce the same output.
- **Composable**: A tool's output should be usable as input to another tool or to the orchestrator's reasoning.
