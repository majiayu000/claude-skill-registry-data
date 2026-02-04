---
name: codegen-bug-fix
description: Fix bugs using TDD starting from README + Issue (following codegen-test), aligning with existing implementation conventions, and leveraging Serena MCP semantic search/editing to implement changes with high performance and race-safety in mind.
---

# Codegen Bug Fix Skill

## Purpose
- Understand the bug and the remediation approach based on README.md and the Issue, then produce a Go implementation.
- Proceed in a **test-driven** manner and match the **existing code style** (naming, design, structure, error handling).
- Use Serena MCP tools to “read less, find precisely, and edit accurately.”

## When to use
- When a bug fix is required based on an Issue.
- When you want to fix only the problem without changing existing behavior.
- When the change requires attention to performance or data races (race conditions).

## Deliverables (expected output)
- Create **tests** that reproduce the bug and verify the fix (**conform to the generate-test skill**).
- **Tests** that transition from failing → passing (**conform to the generate-test skill**).
- **Production code** that makes the tests pass.
  - All tests and static analysis must complete successfully.
- Minimal README/comment/documentation updates (only if necessary)

---

## Execution steps (follow this order)

### 0) Safety measures before changes
- Do not break existing APIs/behavior.
  - Ensure the fix does not unintentionally change the specification.
  - Only change behavior when there is clear evidence in the Issue/README.
  - If a behavior change is necessary, ask for confirmation.
- Keep changes minimal. Do **not** do opportunistic refactors.
  - If refactoring is needed, create a separate Issue.
  - Use GitHub MCP to create the Issue.

### 1) Identify the Issue and confirm requirements (read README + Issue)
1. Get the **current branch name**:
  - `git rev-parse --abbrev-ref HEAD`
2. Extract the **Issue number** from the branch name (example):
  - `feature/issue-<issue_number>-`
3. Read the Issue
  - Use GitHub MCP.
4. Check README.md / CONTRIBUTING / docs for the **expected usage, constraints, and compatibility**.
5. Finalize acceptance criteria as bullet points and convert them into **test perspectives**.
  - Test perspectives must follow the `codegen-test` skill.

> If you cannot extract the Issue number, look for clues in README / Issue list / PRs / commit messages. If still unclear, ask the user which Issue should be targeted.

### 2) Find the project’s existing style (grep + Serena)
**Goal:** Match existing patterns (structs, errors, return values, naming, test style).

- First, create an “entry point” using grep / git grep:
  - `grep -En "keyword|TypeName|funcName" -r .`
  - `grep -En --include='*.go' "keyword|TypeName|funcName" -r .`
  - `git grep -nE "keyword|TypeName|funcName" -- '*.go'`
- Then use Serena MCP to locate the “right place” without over-reading:
  - `get_symbols_overview` (high-level symbol overview)
  - `find_symbol` (jump to type/function/method definitions)
  - `find_referencing_symbols` (find call sites/usages)
  - Use `insert_after_symbol` / `replace_symbol_body` etc. for **pinpoint edits**
  - Avoid reading entire large files; fetch only what you need

### 3) Write tests first (follow the generate-test skill)
- **First, add a test that reproduces the bug** and confirm it fails (red).
- Test strategy:
  - Table-driven tests (happy path / error cases / boundary values)
  - A testable design with injectable dependencies
    - But do not overuse interfaces.
    - Keep the design simple.
  - For external I/O, use interfaces/mocks/in-memory approaches
    - Do not use external modules.
- In this step, the `codegen-test` skill instructions are the **top priority**.

### 4) Implement (minimal changes, high performance, idiomatic Go)
**Design principles**
- Keep names **short and unambiguous**, so the meaning is clear in a single word. Avoid vague words or overly long compounds.
- Follow `gofmt` / `gopls`, and prefer the standard library.
- Think about **data structures first**, then logic—choose structures suited to the problem to improve performance and maintainability.
- Avoid nested if/else; prefer early returns and happy-path flows.
- A bug fix should be minimal: do not add new features.

**Performance checklist (apply as needed)**
- Avoid unnecessary allocations:
  - Pre-allocate slices when appropriate: `make([]T, 0, n)`
  - Estimate capacity if appending in loops
- Use `map[string]struct{}` for sets (no value payload)
- Aim for “zero-copy”:
  - Avoid repeated `[]byte`↔`string` conversions (do it once at boundaries)
  - Handle large data via references/slices
- Do not overuse `fmt.Sprintf` in hot paths; consider `strings.Builder` or `bytes.Buffer` when needed.

### 5) Tests, static checks, and race checks
- Run tests (including race checks):
  - `task go:test`
- If the change might impact performance, run benchmarks:
  - `task go:bench`

### 6) Rules to avoid data races
- Make reads/writes to shared state explicit and protect them with one of:
  - mutex / RWMutex
  - ownership transfer via channels
  - atomic (only when applicable)
- Do not share “apparently safe” maps/slices (even read-only requires careful construction timing).
- Increase reproducibility by running concurrency in tests (`t.Parallel()` and/or goroutines) for race-prone areas.

---

## Final report output (keep it short)
- Output as a Markdown report:
  - Filename: `<issue_number>_<datetime>_bug_fix_report.md`
- Issue summary (acceptance criteria)
- Changes (by file)
- Added test perspectives
- Commands executed
- Performance/race considerations (if applicable)