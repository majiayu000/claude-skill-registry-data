---
name: autonomous-phase-execution
description: Execute a single phase from roadmap to working code autonomously
when_to_use: when executing one phase of a multi-phase roadmap
version: 3.0.0
---

# Autonomous Phase Execution

Execute one roadmap phase: think → plan → implement → handoff.

## Input

Receives from main executor:

- Phase goal (one sentence)
- Success criteria (list of outcomes)
- Project context (language, test command, lint command)
- Previous phase handoff (YAML file path, or "none" for phase 0)

## Process

### Step 1: Think (Internal - Not Saved)

Evaluate 2-3 architecture approaches internally:

- List components needed
- Consider patterns (MVC, Repository, Factory, etc.)
- Pick simplest that meets requirements
- Decision time: 2 minutes max per choice

Use decision framework:

- Prefer standard patterns over novel
- Prefer simple over complex
- Prefer loose coupling
- Avoid over-engineering

### Step 2: Plan (Internal - Not Saved)

Break phase into TDD task pairs:

- Each task: one test file + one impl file
- Sequence tasks logically (dependencies first)
- Estimate: 2-5 minutes per task
- Keep tasks focused (single responsibility)

### Step 3: Implement

For each task in sequence:

1. **Write test**
   - Create or update test file
   - Write test(s) for new functionality
   - Follow language conventions

2. **Verify RED**
   - Run test command
   - Confirm test FAILS
   - If passes unexpectedly, fix test

3. **Write implementation**
   - Create or update implementation file
   - Write minimal code to pass test
   - Follow language best practices

4. **Verify GREEN**
   - Run test command
   - Confirm test PASSES
   - If fails, fix implementation

5. **Run quality gates**
   - Compile: [language-specific build]
   - Lint: [language-specific lint]
   - All tests: [full test suite]
   - Verify: ALL pass

6. **Commit**
   - Stage test and impl files
   - Commit with descriptive message:

     ```
     feat: [component/feature name]

     - What: [what was built]
     - How: [pattern/approach used]
     - Integration: [dependencies]
     - Testing: [what tests cover]
     ```

### Step 4: Verify Success Criteria

After all tasks:

- Check each success criterion from roadmap
- Run integration tests if specified
- Verify all quality gates pass

### Step 5: Output Handoff

Create handoff document at `docs/handoffs/phase-[N]-handoff.yml`:

```yaml
built: [Component1, Component2]
api:
  - Component1.method(args)->return
  - Component2.method(args)->return
patterns: [MVC, Repository]
```

Include:

- `built`: List of components/modules created (names only)
- `api`: Key public interfaces (function signatures)
- `patterns`: Architectural patterns used

Keep handoff minimal: 50-100 tokens.

## Quality Gates (Non-Negotiable)

Before any commit, ALL must pass:

- ✅ Code compiles (no errors)
- ✅ Linter passes (zero issues)
- ✅ All tests pass (zero failures)
- ✅ No regressions (existing tests still pass)

If any gate fails:

- Fix immediately
- Re-run all gates
- Never commit broken code

## Language-Specific Commands

**Python:**

- Test: `pytest tests/ -v`
- Lint: `ruff check . && mypy .`
- Build: N/A (interpreted)

**Go:**

- Test: `go test ./... -race -cover`
- Lint: `golangci-lint run ./...`
- Build: `go build ./...`

**Rust:**

- Test: `cargo test`
- Lint: `cargo clippy --all-targets`
- Build: `cargo build`

**TypeScript:**

- Test: `npm test`
- Lint: `eslint . && tsc --noEmit`
- Build: `tsc`

**Java:**

- Test: `mvn test` or `gradle test`
- Lint: `mvn checkstyle:check`
- Build: `mvn compile`

## Decision Framework

When choosing architecture/technology:

1. Simplest solution that meets requirements
2. Well-known patterns (MVC, Repository, Factory)
3. Standard libraries over custom
4. 2 minutes max per decision
5. If unclear: pick most common approach

Avoid:

- Over-engineering
- Premature optimization
- Novel architectures
- Tight coupling
- Magic behavior

Prefer:

- Simple and clear
- Easy to test
- Standard patterns
- Loose coupling
- Explicit behavior

## Error Handling

If quality gate fails after 3 fix attempts:

- Document blocker
- Report to main executor
- Do not proceed to next task

If success criteria not met:

- Document gap
- Report to main executor
- Do not output handoff

## Output Summary

After completion, report:

- Components created
- Tests added (count and passing)
- Commits created (count and SHAs)
- Handoff location
- Success criteria status
- Quality gate results
