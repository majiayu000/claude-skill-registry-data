---
name: feature-test
description: Execute the TEST stage of a feature-development task — author + run tests that verify the feature works end-to-end, gated by full pytest pass + no test count regression. Loads when a task is at implement→test transition or when the operator says "test X" / "verify X" / "add tests for X".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: medium
---

# feature-test

The TEST stage skill in the feature-development methodology chain
(`document → design → scaffold → implement → test`). Author the tests that
verify the implemented feature, run the full pytest suite, fix failures,
and advance the task to readiness=100 / status=done.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Stage transition**: a task in [wiki/backlog/tasks/](../../../wiki/backlog/tasks/) has `current_stage: implement` AND `readiness: 80-95` AND implement-stage Done When all checked
- **Direct verb**: operator says "test X", "add tests for X", "verify X works", "cover X with tests", "now test it"
- **After feature-implement completes**: implement skill emitted "Implement done; test stage is next"
- **bug-fix model test step**: bug-fix chain (`document → implement → test`) reaches its test stage
- **Coverage gap surfaced**: `quality-coverage` audit identifies an uncovered code path that maps to a recently-implemented feature

Do NOT load when:

- Task `current_stage` is `document`, `design`, `scaffold`, or `implement` (those are different skills)
- The change being tested is unrelated to a feature (load `quality-coverage` for general coverage work)
- Tests are already written and only verifying coverage (load `quality-coverage`)

## Operations

This skill has 4 named operations. Execute in order.

### Operation 1: Plan test coverage

**Trigger**: skill loaded; current_stage is implement-complete confirmed.

**Process**:

1. Read the task file. Get the Done When list — this is the spec the tests must verify.
2. Read the implement-stage artifacts (the new code from `aicp/`). Identify: public API surface (functions, classes, methods) + integration points (callers).
3. Read existing related tests to understand: pytest fixtures available, test patterns used in this domain (mocking conventions, parametrize style), where tests for this code area live.
4. List the test cases:
   - **Unit**: each public function/method, happy path + edge cases
   - **Integration**: at least one test that exercises the feature through its real entry point (CLI, MCP tool, router decision, etc.)
   - **Negative**: at least one test that verifies failure modes (bad input, missing dependency, timeout, etc.)
   - **Done When verification**: one test per Done When item that ASSERTS the verifiable evidence
5. Present the test plan to the operator and wait for "go" before authoring.

**Quality bar (Operation 1 done when)**:

- [ ] Each Done When item has ≥1 test case planned
- [ ] Each new public function/class has ≥1 unit test planned
- [ ] At least 1 integration test planned (not just unit tests)
- [ ] At least 1 negative test planned
- [ ] Operator approved the plan

### Operation 2: Author the tests

**Trigger**: Operation 1 plan approved.

**Process**:

1. Write tests in `tests/` mirroring the structure of the code under test (`aicp/core/foo.py` → `tests/test_foo.py`). One file per module under test, unless the existing pattern groups them differently.
2. Use existing fixtures from `tests/conftest.py` — don't duplicate fixture setup. If a needed fixture doesn't exist, add it to conftest.py with a brief docstring explaining its scope.
3. Each test function: name it `test_<verb>_<scenario>` (e.g., `test_router_routes_simple_query_to_local`). Test names ARE documentation — vague names like `test_works` are forbidden (Quality Standards: Done When items must be specific).
4. Each test ASSERTS specific values, not just "didn't raise":
   - Bad: `assert result is not None`
   - Good: `assert result.backend == "local"` and `assert result.tokens > 0`
5. Use `pytest.mark.parametrize` for variations of the same logic with different inputs — don't copy-paste tests.
6. Mock external services at the boundary (LocalAI HTTP calls, Claude subprocess, etc.) — DO NOT mock internal AICP code (per Quality Standards: integration tests must hit real internal code, mocks only at system boundaries).

**Quality bar (Operation 2 done when)**:

- [ ] All planned test cases written
- [ ] Test names follow `test_<verb>_<scenario>` convention
- [ ] Each test asserts specific values (not just non-None)
- [ ] Mocks only at system boundaries (no `Mock()` for internal AICP modules)
- [ ] `ruff check tests/` exits 0
- [ ] `ruff format --check tests/` exits 0

### Operation 3: Run + fix

**Trigger**: Operation 2 tests written.

**Process**:

1. Run the full suite: `pytest tests/ --tb=short`. Expect pass; if not, fix the FIRST failure and re-run.
2. After clean pass: capture the test count: `pytest tests/ --co -q | tail -1`. Compare to the previous count from CI or a recent commit. If it DECREASED, you accidentally deleted or renamed a test — investigate before continuing (Quality Standards: "no_test_deletions" — assertion tampering anti-pattern).
3. Run with coverage if the project has it configured: `pytest tests/ --cov=aicp --cov-report=term-missing`. Note: coverage is advisory, not blocking — focus on whether the FEATURE is covered, not the absolute coverage %.
4. Verify each Done When item: produce the evidence the spec asks for. If Done When says "router returns local for simple Q&A" and your test for that is `test_router_routes_simple_to_local`, run it specifically with `-v` and quote its passing output.
5. Run the wiki lint on the task file: `python3 -m tools.lint wiki/backlog/tasks/<task-id>.md`. The task page must still validate.

**Quality bar (Operation 3 done when)**:

- [ ] `pytest tests/` exits 0 (full suite pass, no `-x`, no `-k`)
- [ ] Test count did not decrease from prior commit
- [ ] Every Done When item has a passing test mapped to it (with command output captured)
- [ ] No skipped tests added without justification (Quality Standards anti-pattern: test skipping)
- [ ] Coverage of new code is materially exercised (advisory check, not a hard gate)

### Operation 4: Close out the task

**Trigger**: Operation 3 verifications all pass.

**Process**:

1. Open the task file. Update frontmatter: `current_stage: test` (already there from implement) → ready to mark `status: done` (per CLAUDE.md hard rule #6, the operator confirms 99→100 — see Gotcha 2).
2. Set `readiness: 100` ONLY after operator confirms (per Methodology Standards: "99→100 is human-only on both dimensions — adversarial review required").
3. Append the new test files to the task's `artifacts:` list.
4. Add a brief note to the task body: tests added (count), Done When verifications (each item + the test that proves it), full-suite result.
5. Commit: `test(<scope>): T<id> add tests for <feature>` followed by `chore(backlog): T<id> test → done`.
6. Re-run lint on the task file to confirm validation.
7. Inform the operator: "Test stage done; awaiting your sign-off to mark readiness 100 / status done."

**Quality bar (Operation 4 done when)**:

- [ ] All produced test files listed in `artifacts:`
- [ ] Task body documents Done When verification (item → test → output)
- [ ] Task lint passes
- [ ] Operator sign-off received before flipping `readiness: 100` and `status: done`
- [ ] Commits follow conventional format with one logical unit per commit

## Gotchas (known failure modes — read before doing)

### Gotcha 1: Mocking internal code (creates false-pass tests)

The temptation: mock the router so the test runs faster / is more isolated. But per Quality Standards: integration tests must hit a real database / a real router / real internal code. Mocking internal code creates tests that pass when production fails (the mock didn't model the real behavior).

**Detection**: search your test for `Mock()`, `MagicMock()`, `patch.object` targeting `aicp.*`. If you find any, remove them and use the real internal class with appropriate setup.

**The rule**: mock at SYSTEM BOUNDARIES (HTTP to LocalAI, subprocess to Claude, file I/O to ~/.aicp/, network to OpenRouter). Internal classes get real instances, even if that requires setup fixtures.

### Gotcha 2: Marking done without operator sign-off (false readiness)

Operation 4 says "set readiness 100 ONLY after operator confirms." The temptation: tests pass cleanly, lint passes, everything green — surely we can mark done. NO. Per Methodology Standards: "99→100 is human-only on both dimensions — adversarial review required." The agent moves to readiness 99; the human inspects and approves the 99→100.

**Detection**: are you about to write `readiness: 100` to the task file without operator saying "approved" or equivalent? Stop.

**The rule**: emit "Test stage done; awaiting sign-off." The operator's "go" is the only thing that flips readiness 99→100 and status review→done.

### Gotcha 3: Adding `pytest.mark.skip` to make the suite pass (assertion tampering)

A test fails. You don't have time to fix it. Tempting to add `@pytest.mark.skip(reason="flaky")` and move on. Per Quality Standards anti-pattern table: this is "test skipping" — the assertion-tampering category, alongside coverage reduction.

**Detection**: `git diff tests/` shows newly-added `@pytest.mark.skip` or `@pytest.mark.xfail` lines.

**The rule**: if a test is genuinely flaky, file a bug task and fix the flakiness in its own task. Don't skip it during the test stage of an unrelated feature. If a test asserts something the feature changed, update the assertion (and document WHY in the commit message). Never just skip.

### Gotcha 4: Vague test names ("test_works", "test_main", "test_basic")

Test names are read more often than they're run. A failing test named `test_works` tells you nothing. A failing test named `test_router_routes_simple_query_to_local_when_local_healthy` tells you exactly what's broken.

**Detection**: `pytest tests/ --co -q | grep -E "test_(works|main|basic|simple|case_1|case_2)"` — any matches are vague.

**The rule**: every test name must read as `test_<subject>_<verb>_<scenario>`. If you can't name it that way, the test is doing too much — split it.

### Gotcha 5: Testing implementation, not behavior (over-coupled tests)

Tempting to write tests that assert on internal data structures (`assert obj._cache == {"foo": 1}`). These break when the implementation refactors even if behavior is unchanged. Tests should assert on the BEHAVIOR (what the function returns, what side effects happen at the boundary), not the internals.

**Detection**: tests assert on `obj._private_attr`, `obj.__dict__`, mock call counts to internal methods.

**The rule**: tests assert on what the operator/consumer of the feature would observe — return values, log outputs, file contents at boundaries, network calls made (not received). Internal restructuring shouldn't break tests.

## Reference exemplars

Per Extension Standards, the reference exemplars are the second brain's `model-builder` and `wiki-agent`. This skill follows their structure: trigger phrases, multiple named operations, per-operation Process + Quality bar, Gotchas with detection + rule + reasoning. See also the [feature-implement](../feature-implement/SKILL.md) skill (preceding stage) for shape consistency across the feature-development chain.

## Domain context

This skill operates in **backend-ai-platform-python** — see [wiki/config/domain-profiles/backend-ai-platform-python.yaml](../../../wiki/config/domain-profiles/backend-ai-platform-python.yaml) for the test-stage gate commands (ruff check + ruff format --check + full pytest + test count drift check).

## Related skills

| Skill | When | Why distinct |
|-------|------|--------------|
| feature-implement | implement stage (preceding) | Writes the feature; this skill verifies it |
| quality-coverage | general coverage work, not tied to a specific feature | Audits coverage gaps across the codebase; feature-test scopes to one feature's tests |
| feature-review | post-test review of the feature as a whole | Reviews the assembled feature; feature-test is the test-stage execution |
| ops-deploy | shipping the verified feature | Deployment is its own stage, runs after test |
