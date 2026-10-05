---
name: test
description: "Assess test state and run the right action (default, no args): run the suite, then find failures, coverage gaps, and quality issues and route into fix, generate, or review. Explicit modes: review (--review, check test quality), generate (--generate <target>, create tests). Scope: --staged, --changed, --all, or context-based. Use when unsure what the tests need, or for test quality and creation."
argument-hint: "[ (no args = assess) | --review | --generate <target>] [--staged | --unpushed | --changed | --all]"
effort: high
---

<!-- Generated from https://github.com/nielsmadan/agentic-coding — edits here are overwritten. -->

# Test

Assess, review, and generate tests following consistent principles.

## Which mode runs — read first

**Bare `/test` with no mode flag → Assess, over the whole suite. Always.**

- Do **not** infer `--review` or `--generate` from conversation context. "We
  just finished a feature", "just committed", or "recent changes" do **not**
  narrow a bare `/test` — assess runs the whole suite and surveys the full state.
- Run an explicit mode **only when the user types the flag** (`--review`,
  `--generate`). Don't pick one for them.
- Don't substitute "I know what's needed, so I'll just review/generate." Run the
  full assess and let its plan (Fix/Generate/Review) surface what you'd skip.

## Modes

All modes share one lens — *compare the tests against the code and the
principles* — and differ in what they do with the result:

| Mode | Intent | Writes? | Default scope |
|------|--------|---------|---------------|
| **(no args) — assess** | Run the suite, survey failures / gaps / quality, propose & run an action plan | No → plan, then runs your picks | whole suite + code surface |
| `--review [target]` | Check test quality against the principles | No → findings | context (or `<target>`) |
| `--generate <target>` | Create tests for code that lacks them | Yes — new/extended test files | the target |

**Assess is the default** — it's what a bare `/test` runs (see "Which mode runs"
above). It runs the suite, classifies what's required, and routes into the modes
below. The explicit modes are opt-in via their flag.

## Usage

```
/test                              # Assess test state (run suite, find failures/gaps/issues), propose a plan, run your picks (default)
/test --staged                     # Assess, scoped to what staged changes touch
/test --review                     # Explicit review mode (quality only)
/test --review --staged            # Review staged test files
/test --review --unpushed          # Review test files changed across all unpushed commits
/test --review --changed           # Review unstaged test files
/test --review --all               # Review all tests (parallel agents)
/test --generate <target>          # Generate tests for file/module/feature
/test --generate --staged          # Generate tests for staged code changes
/test --generate --unpushed        # Generate tests for code changed across unpushed commits
/test --generate --changed         # Generate tests for unstaged code changes
```

## Testing Principles

Both review and generate modes follow these principles. Review checks conformance; generate applies them.

### 1. Test Behavior, Not Implementation

Assert observable outputs and side effects — not internal state or private methods.

### 2. Mock Only External Boundaries

Mock third-party services and I/O; keep internal modules real so the test exercises actual code.

### 3. Meaningful Assertions

Every test must have at least one `expect` that can fail; a test with no assertions proves nothing.

### 4. No Brittle Timing

Never use `setTimeout`/`sleep` to wait for async work; wait for the actual condition instead.

### 5. Independent Tests

Each test must set up its own state and not rely on execution order or shared mutable state.

### 6. Cover Edge Cases

- Empty inputs
- Null/undefined
- Boundary values (0, -1, MAX_INT)
- Error conditions
- Concurrent access
- Unicode/special characters

### 7. Focused Tests

One concern per test — avoid multi-step flows that test several behaviors in a single `it` block.

### 8. Named Constants Over Magic Values

Use named constants for test inputs and expected values so the intent is clear at a glance.

For BAD/GOOD code examples of each principle, see `references/principles-examples.md`.

---

## Gotchas
- `--staged`, `--unpushed`, and `--changed` review filter by filename pattern (`*test*`, `*spec*`). A test file in `__tests__/payment.ts` (no "test" in the filename) is missed by the glob.
- Red-Green Verification (run → green, revert → red, re-apply → green) is described for bug fixes only, but is equally important for new feature tests to confirm the test actually validates the implementation.

## Assess Mode (default)

The no-args entry point. Use it when you don't know what the tests need: it
establishes the current state of the suite, classifies what's required, hands
you a prioritized action plan, then runs the parts you choose. It never
generates or rewrites without your go-ahead — the plan comes first.

### Workflow

1. **Establish the suite state.**
   - Detect the framework and test command (`package.json` scripts,
     `pyproject.toml`/`pytest`, `go test`, `flutter test`, `Makefile`). Show the
     command before running it.
   - **Run the suite** — or the scoped subset (see Scope). Capture pass/fail
     counts and each failure. If it's long-running, run it in the background. If
     running isn't feasible or safe (missing deps, integration tests that hit
     real services), say so and fall back to static analysis only.
   - If a coverage script exists, run it (or read the latest report) for the
     in-scope files.
   - Map the code surface → existing tests to find untested modules/functions.

2. **Classify into action lanes (priority order):**
   - **Failing tests → Fix (top priority).** A red suite outranks everything;
     per the repo's "all green" policy, don't generate or review on top of a
     broken suite. List each failure as `file:test` with the error. Escalate per
     policy: after 2 failed fix attempts use `second-opinion`, after 4 use
     `hard-fix`; for failures waved off as "pre-existing" use `pre-existing`.
   - **Coverage / untested code → Generate.** Functions, modules, and branches
     with no tests; missing error paths and edge cases.
   - **Quality issues → Review.** Existing tests that violate the principles
     (over-mocking internals, no meaningful assertions, brittle timing,
     order-dependence, implementation-coupling).

3. **Report state + action plan.** One categorized, sequentially-numbered list:
   ```markdown
   ## Test Assessment: {scope}
   State: {suite green/red — X passed, Y failed} · coverage {Z}% · {N} untested modules in scope

   ### Fix (failing — do first)
   1. {file}:{test} — {error}

   ### Generate (missing)
   2. {code_file}:{fn} — no tests / missing {edge case}

   ### Review (quality)
   3. {test_file} — {smell}

   ### Healthy
   - {what's already solid — so the user knows it was checked}
   ```
   Always emit *this* assess report (titled **Test Assessment**) with **every
   lane present even when empty** (write "none — …" with the reason). Don't let
   a passing suite collapse assess into a plain quality review and skip the
   **Generate** (coverage/gaps) lane — checking existing tests is only one lane.
   Number actionable findings sequentially across tiers so the user can select by number.

4. **Offer to execute.** Ask which to run (numbers, `all`, or `none`;
   multi-select where supported). **Generate** and **Review** run the matching
   mode's logic from this skill; **Fix** drives the failing tests back to green
   (escalating per the policy above). `none` → stop. Nothing is generated or
   rewritten without a selection.

### Scope

Defaults to the whole suite + code surface. To bias toward recent work, add
`--staged` / `--unpushed` / `--changed` (assess only what those changes touch —
run just those tests, check coverage/gaps there) or a `<target>` (assess one
feature/area).

---

## Review Mode (`--review`)

Checks tests against the principles above. (Assess routes here for the quality
lane; run it explicitly to review without running the suite first.)

### Scope

| Flag | Scope | Method |
|------|-------|--------|
| (none) | Context-related tests | Find tests for recently discussed code |
| `--staged` | Staged test files | `git diff --cached --name-only -- '*test*' '*spec*'` |
| `--unpushed` | Test files changed across unpushed commits | `git diff --name-only $(git rev-list HEAD --not --remotes \| tail -1)^..HEAD -- '*test*' '*spec*'` |
| `--changed` | Unstaged test files | `git diff --name-only -- '*test*' '*spec*'` |
| `--all` | All test files | Glob `**/*test*.{ts,js,py,dart}` etc. |

`--unpushed` derives its range from `git rev-list HEAD --not --remotes` (oldest unpushed commit's parent → HEAD). If nothing is unpushed, or there is no remote/upstream (or the range walks back to the root commit) so it can't be determined reliably, stop and ask the user to pick another scope.

### Workflow

1. **Get file list** based on scope
2. **Review** (directly if ≤5 files, parallel workers if more). Workers return
   findings without editing files. Disable delegation tools where supported;
   any coordinating role needs explicit subtasks, a descendant limit, and a
   stopping condition.
3. **Report findings** by priority

### Checklist

For the review checklist, see `references/generate-templates.md`.

### Coverage Check

If a coverage script exists, run it to identify gaps:

```bash
# Check for coverage scripts
grep -E "coverage|test:cov" package.json 2>/dev/null
cat pyproject.toml 2>/dev/null | grep -A5 "pytest"
```

**Common coverage commands:**
- `npm run test:coverage` or `npm run coverage`
- `pytest --cov`
- `go test -cover`
- `flutter test --coverage`

Report uncovered lines/branches for files in scope.

### Output Format

```markdown
## Test Review: {scope}

### Critical Issues
- {file}:{test} - {issue}

### Completeness Gaps
- {code_file}:{function} - no tests found
- {code_file}:{function} - missing test for error case
- {code_file}:{function} - missing test for edge case: {scenario}

### Coverage Report
(if coverage script available)
- Overall: {X}% statements, {Y}% branches
- Uncovered in scope:
  - {file}:{lines} - {description}

### Pattern Violations (--staged)
- {test_file} - setup pattern differs from existing tests
- {test_file} - mocking approach inconsistent with {example_file}

### Test Smells
- {file}:{test} - {smell}

### Suggestions
- {improvement}
```

---

## Generate Mode (`--generate`)

Create tests for code following the principles above.

### Red-Green Verification (for bug fixes)

When generating tests for a bug fix, verify the test actually catches the bug:

1. Run the new test with the fix applied -- confirm PASS (green)
2. Temporarily revert the fix
3. Run the test again -- confirm FAIL (red)
4. Re-apply the fix
5. Run the test -- confirm PASS again (green)

Only claim the test is valid if it fails without the fix and passes with it. This prevents tests that pass for unrelated reasons.

### Scope

| Flag | Scope | Method |
|------|-------|--------|
| `<target>` | Specific file/function/module | Read the code, generate tests |
| `--staged` | Staged code changes | Generate tests for what changed |
| `--changed` | Unstaged code changes | Generate tests for what changed |

### Workflow

1. **Detect framework** - Jest, pytest, go test, vitest, etc. from project
2. **Analyze existing test patterns** - read 2-3 existing test files to learn:
   - File naming and location conventions
   - Describe/it structure and nesting style
   - Setup/teardown patterns (beforeEach, fixtures, factories)
   - Mocking approach (jest.mock, manual mocks, DI)
   - Assertion style and common matchers
   - Test data patterns (inline, fixtures, builders)
3. **Read the code** - understand what needs testing
4. **Check existing tests** - avoid duplicates, extend if needed
5. **Generate tests** following both principles AND project patterns

For framework detection rules and cross-framework terminology, see `references/framework-mapping.md`.

### Test File Placement

Follow project conventions:
- `__tests__/` directory (common in JS/TS)
- `*.test.ts` or `*.spec.ts` alongside source
- `test/` directory at project root
- `*_test.py` alongside source or in `tests/`

### What to Generate

For generate templates (function, component, service, staged changes), see `references/generate-templates.md`.

### Output

Generate test files directly, matching project patterns:
- Place in location matching existing test file structure
- Use same describe/it nesting style as other tests
- Match setup/teardown patterns (beforeEach, fixtures, etc.)
- Use same mocking approach as existing tests
- Match assertion style and matchers
- Use consistent test data patterns (inline, fixtures, builders)
- Add brief comments for non-obvious test cases

**Before generating, show the patterns found:**
```markdown
## Detected Test Patterns

**Location:** `__tests__/` alongside source
**Structure:** `describe` per class/module, `it` per behavior
**Setup:** `beforeEach` with factory functions
**Mocking:** jest.mock for external, DI for internal
**Assertions:** jest matchers, testing-library queries

Generating tests following these patterns...
```

---

## Examples

**Not sure what the tests need — just triage them:**
> /test

Detects the framework, runs the suite, and checks coverage, then reports a
numbered plan: failing tests to fix first, untested code to generate tests for,
and existing tests with quality smells to review — plus what's already solid.
Asks which to run and executes your picks (fixing red tests, generating, or
reviewing).

**Generate tests for a payment function:**
> /test --generate lib/services/payment.ts

Detects the project's test framework and patterns, then generates a test file covering happy path (successful charge), error handling (declined card, network failure), and edge cases (zero amount, currency mismatch). Places the file following existing test conventions.

**Review staged tests catches over-mocking:**
> /test --review --staged

Reviews staged test files against the testing principles. Flags tests that mock internal modules instead of only external boundaries, and identifies tests with no meaningful assertions that would pass regardless of behavior.

## Troubleshooting

### Generated tests fail immediately on first run
**Solution:** Verify the correct test framework was detected by checking the "Detected Test Patterns" output. If imports or setup are wrong, point `--generate` at an existing passing test file so the generator can match its patterns exactly.

### Cannot detect the project's test framework
**Solution:** Ensure a framework config file exists (`jest.config.*`, `vitest.config.*`, `pytest.ini`, or `pyproject.toml` with pytest section). If the project uses a non-standard setup, run `test --generate <target>` and specify the framework in your prompt.

### Assess wants to run a slow suite, or one that hits real services
**Cause:** Assess runs the suite to establish state. **Solution:** Scope it
(`/test --staged` or a `<target>`) to run only the relevant tests, let it run in
the background, or — if running isn't safe — tell it to skip the run and do a
static gap/quality assessment instead.

### Assess proposes generating tests while the suite is red
**Cause:** Misread priority. **Solution:** The plan orders **Fix** before
**Generate** for a reason — don't pile new tests on a broken suite. Fix the
failures first, then re-assess for gaps.

## Notes

- Default (no args) is assess mode: run the suite, survey failures/gaps/quality,
  propose a plan, and run the user's picks. It's the entry point when you don't
  yet know what the tests need.
- All modes share the same principles — review checks, generate applies, assess
  triages and routes.
- Reach for an explicit mode when you already know the action: `--review` for a
  quality pass; `--generate <target>` for new tests; assess when unsure.
- Use `--staged` before commits to catch issues or generate missing tests
- Use `--all` periodically for comprehensive review
- Sub-agents parallelize large reviews/generations
- Integration tests > unit tests with heavy mocking
