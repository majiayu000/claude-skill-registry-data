---
name: quality-coverage
description: Audit AICP's test coverage to find uncovered code paths, decide what's worth covering, and author tests for the gaps — scoped broader than a single feature (unlike feature-test). Loads when the operator says "check coverage" / "find uncovered code" / "what's not tested" / "coverage gaps", or as a periodic quality audit.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: high
---

# quality-coverage

Audits AICP's 1,758-test suite for coverage gaps, classifies gaps by risk, and
authors tests for the high-risk uncovered paths. Distinct from `feature-test`
(which covers ONE feature's code) — this skill operates at the SUITE level:
what's uncovered across the whole codebase, and what's worth fixing.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: operator says "check coverage", "find uncovered code", "what's not tested", "coverage gaps", "audit tests", "where are the blind spots"
- **Periodic quality cycle**: scheduled audit (monthly, per-release, post-incident) — coverage is one of the signals `pm-status-report` should surface
- **Post-incident analysis**: a bug shipped to production; load to find if the uncovered path was detectable by coverage analysis
- **Pre-release gate**: before a milestone ships, confirm coverage hasn't degraded
- **Refactor follow-up**: after a `refactor-*` skill touched significant code, verify coverage of the refactored paths hasn't silently dropped

Do NOT load when:

- A specific feature needs tests (load `feature-test` — narrower scope, inside the feature-development chain)
- A specific test is failing (load `systematic-debugging` or `feature-test` Gotcha flow)
- Coverage tooling itself needs setup (load `foundation-testing`)
- The issue is test quality rather than coverage (load `quality-audit` for broader quality concerns)

## Operations

This skill has 4 named operations. Execute in order.

### Operation 1: Generate the coverage report

**Trigger**: skill loaded; operator wants an audit.

**Process**:

1. Check if coverage tooling is configured: `grep -E 'pytest-cov|coverage' pyproject.toml requirements*.txt 2>/dev/null`. If missing, stop and load `foundation-testing` first — you can't audit what doesn't measure.
2. Run coverage across the suite: `pytest tests/ --cov=aicp --cov-report=term-missing --cov-report=json:coverage.json 2>&1 | tee /tmp/coverage-audit.log`. Capture the output.
3. Parse the JSON report (`coverage.json`) to get per-file coverage percentages. Flag files below thresholds:
   - **Critical gap**: <60% line coverage on any file in `aicp/core/`, `aicp/backends/`, `aicp/guardrails/`
   - **Significant gap**: <80% line coverage on any file in `aicp/core/`, `aicp/backends/`, `aicp/guardrails/`
   - **Notable gap**: <50% branch coverage on any file in the above (branch often lags line — trust the branch number)
4. Capture the BASELINE: overall suite coverage %, file counts per tier. Write the baseline snapshot to `wiki/decisions/00_inbox/coverage-audit-<date>.md` as a reference page (type=reference) so subsequent audits can compare.

**Quality bar (Operation 1 done when)**:

- [ ] Coverage tooling present (or `foundation-testing` loaded to add it)
- [ ] Full suite ran with `--cov=aicp --cov-report=term-missing --cov-report=json`
- [ ] Per-file coverage parsed; critical/significant/notable gaps identified
- [ ] Baseline snapshot written to `wiki/decisions/00_inbox/coverage-audit-<date>.md`

### Operation 2: Classify gaps by risk

**Trigger**: Operation 1 coverage data available.

**Process**:

1. For each gap file, classify risk using two axes:
   - **Blast radius**: how many consumers import this file? Low (1-2 callers) vs high (3+ callers). Use `grep -rn "from aicp.<module>" aicp/ tools/ tests/ | cut -d: -f1 | sort -u | wc -l`.
   - **Failure severity**: what happens if this code is wrong? Low (UI formatting, display helpers) vs high (routing decisions, guardrail checks, circuit breaker state, DLQ persistence). Judgment call — document reasoning.
2. Score each gap: risk = blast_radius × failure_severity (low/medium/high). High-risk gaps are the targets.
3. Author a risk table in the audit page from Operation 1:

   ```markdown
   | File | Line cov | Branch cov | Callers | Severity | Risk |
   |------|---------|-----------|---------|----------|------|
   | aicp/core/router.py | 72% | 58% | 12 | high | HIGH |
   | aicp/core/dlq.py | 45% | 38% | 3 | high | HIGH |
   | aicp/cli/display.py | 32% | 20% | 2 | low | LOW |
   ```

4. For each HIGH-risk gap, drill into the uncovered lines — `pytest --cov-report=term-missing` shows missing line numbers per file. Identify what BEHAVIOR is untested (not just what lines). Example: "router.py line 142-158 is the circuit-breaker-open fallback path — no test exercises it."
5. Flag gaps that can't be tested in principle (dead code? feature flag off? debug-only path?) — mark for deletion, not covering.

**Quality bar (Operation 2 done when)**:

- [ ] Every flagged file has blast_radius + severity assessment
- [ ] Risk table written in audit page
- [ ] HIGH-risk gaps have behavior-level description of what's uncovered
- [ ] Dead-code gaps explicitly flagged as deletion candidates (not coverage targets)

### Operation 3: Author tests for HIGH-risk gaps

**Trigger**: Operation 2 classification complete; operator approved the priority list.

**Process**:

1. Operator must confirm which HIGH-risk gaps to address in this pass (don't do all at once if the list is long; batching keeps reviews reasonable).
2. For each approved gap, load the relevant module + existing tests. Understand what's tested already so new tests complement, not duplicate.
3. Author tests following feature-test's authoring patterns (see `.claude/skills/feature-test/SKILL.md`):
   - Specific test names: `test_<verb>_<scenario>` (e.g., `test_router_fails_fast_when_circuit_breaker_open`)
   - Assert specific values, not just "didn't raise"
   - Mock only at system boundaries (HTTP, subprocess) — not internal AICP code
   - Use `pytest.mark.parametrize` for variation
4. Run the new tests: `pytest tests/test_<file>.py -v`. All pass.
5. Run the full suite: `pytest tests/ --tb=short`. Count stays ≥ prior count (no regression).
6. Re-run coverage: confirm the targeted gaps closed. New coverage should reflect the targeted lines/branches.
7. Commit: `test(coverage): cover <gap-name> (file.py L#-#)` per logical batch.

**Quality bar (Operation 3 done when)**:

- [ ] Operator approved the priority list before authoring
- [ ] New tests follow feature-test authoring patterns (specific names, real assertions, boundary-only mocks)
- [ ] Full suite passes (exit 0, count did not decrease)
- [ ] Coverage re-run shows targeted gaps closed
- [ ] Commits follow conventional format

### Operation 4: Update the audit page with results

**Trigger**: Operation 3 tests landed.

**Process**:

1. Re-open `wiki/decisions/00_inbox/coverage-audit-<date>.md`. Update:
   - Before/after coverage numbers (overall + per-HIGH-risk file)
   - Tests added (count + file list)
   - Gaps still open (with reasoning — "deferred to next audit because Y")
   - Dead-code flagged for deletion (separate follow-up task)
2. If the audit surfaced patterns (e.g., "circuit breaker paths consistently undertested"), contribute back to second brain as a lesson: `gateway contribute --type lesson --title "..."`.
3. Add the audit page path to the next pm-assess / pm-status-report references.
4. Run `python3 -m tools.lint wiki/decisions/00_inbox/coverage-audit-<date>.md`.

**Quality bar (Operation 4 done when)**:

- [ ] Audit page has before/after numbers
- [ ] Gaps still open documented with reasoning
- [ ] Dead-code deletion candidates listed (as follow-up tasks)
- [ ] Lesson contributed if a systemic pattern emerged
- [ ] Audit page lint passes

## Gotchas (known failure modes — read before doing)

### Gotcha 1: Coverage % as the goal (gaming the number)

The temptation: increase overall coverage from 72% to 85% by adding trivial tests on display helpers. Coverage % goes up; project safety doesn't. Per Quality Standards anti-pattern ("confident surface"): passing the metric isn't the goal — covering the HIGH-RISK behavior is.

**Detection**: you added tests for `aicp/cli/display.py` because it was easy; `aicp/core/router.py` gaps remain because they were hard.

**The rule**: prioritize by risk (blast_radius × severity), not by ease. A 2-point coverage increase in router.py is worth more than a 10-point increase in display.py.

### Gotcha 2: Mocking the thing under test (false coverage)

Covering `router.py` by mocking `router.route()` and asserting the mock was called. Coverage tool counts the line as covered because a test file imported router; actual behavior untested.

**Detection**: test file under `tests/test_router.py` contains `patch.object(router, 'route')` or similar — you mocked the function you claimed to test.

**The rule**: per feature-test Gotcha 1 and Quality Standards: mock only at SYSTEM BOUNDARIES. Internal AICP code (router, controller, profiles) must be tested with real instances. If real instances need setup, add fixtures to `conftest.py`.

### Gotcha 3: Adding tests for dead code (covering the undead)

A file has 45% coverage. Tempting to add tests to raise it. But the uncovered 55% is a feature that was removed months ago — the code should be DELETED, not covered.

**Detection**: `grep -r "from aicp.<module> import <func>" aicp/ tools/ tests/` returns 0 results for the uncovered function. The function is unimported, therefore unused.

**The rule**: delete dead code (refactor task) rather than covering it. Per CLAUDE.md hard rule #10 ("Stay in scope"), file the deletion as a separate refactor task; don't delete in the coverage-audit commit.

### Gotcha 4: Test count gaming (parametrize blowup)

Adding one test that parametrizes 50 trivial variations. Test count goes up 50; confidence doesn't. Quality Standards flags "assertion tampering" — this is its cousin, "test count inflation."

**Detection**: new test file has `@pytest.mark.parametrize` with >20 cases that all assert the same trivial property (e.g., "each string parses").

**The rule**: parametrize only when behavior genuinely varies across the parameters. If 20 cases all prove the same point, one test with a loop is clearer. The count isn't the goal.

### Gotcha 5: Skipping the baseline snapshot (no comparison possible next audit)

Running coverage, fixing gaps, but never writing the baseline. Next audit can't compare — you can't say "we went from X to Y," only "current is Y."

**Detection**: `wiki/decisions/00_inbox/` has no coverage-audit-* files from prior audits.

**The rule**: every audit writes a baseline snapshot. The snapshot IS the artifact — even if no gaps get fixed in this pass, future audits need the comparison point.

## Reference exemplars

Per Extension Standards, reference exemplars are second brain's `model-builder` and `wiki-agent` skills. For the OUTPUT artifact this skill produces:

- **Coverage audit page**: use the `reference` page standard (`wiki/config/templates/reference.md`). A coverage audit is a reference artifact — read later to compare, not a one-shot narrative.

## Domain context

This skill operates in **backend-ai-platform-python** — see [wiki/config/domain-profiles/backend-ai-platform-python.yaml](../../../wiki/config/domain-profiles/backend-ai-platform-python.yaml) for test-stage gate commands. The coverage audit itself spans all stages (it's not a stage-specific skill).

## Related skills

| Skill | When | Why distinct |
|-------|------|--------------|
| feature-test | test stage of ONE feature | Per-feature scope; this skill is suite-wide |
| foundation-testing | setting up the test infrastructure | Pre-audit; this skill uses the infrastructure |
| quality-audit | general quality review | Broader (quality patterns, not just coverage) |
| quality-lint | code style + lint audit | Different quality axis (style vs coverage) |
| refactor-extract | extracting covered-but-messy code | Different phase (refactor follows audit) |
| systematic-debugging | a specific test failing | Tactical; this skill is strategic |
