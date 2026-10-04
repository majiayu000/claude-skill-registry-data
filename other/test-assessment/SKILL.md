---
name: test-assessment
description: Assess the test suite of a codebase — where tests are missing, where they exist but are weak, and which gaps actually matter. Use this skill whenever the user asks about test coverage, test quality, "are there enough tests", "where should we add tests", testing gaps, test debt, untested code paths, flaky tests, or generally wants to know whether a codebase is well-tested. Trigger even on casual phrasings ("is this tested?", "what's the test situation?", "audit our tests"). This skill does NOT write tests — it only assesses what exists and identifies what's missing. For test generation, this is the wrong skill.
license: MIT
---

# Test Assessment

A structured assessment of a codebase's test suite that produces a prioritized report of testing gaps and weaknesses.

## What this skill does (and doesn't)

**Does:** Inventory tests, measure where coverage is missing, evaluate quality of existing tests, identify untested high-risk code, flag test smells and anti-patterns, produce a risk-ranked report.

**Does not:** Write new tests. Run the test suite. Modify code. If the user wants tests authored, stop and tell them this is the wrong skill.

## Core principle

Coverage percentage is a vanity metric. **What matters is the relationship between risk and coverage.** A 90%-covered logging module is less interesting than a 30%-covered payments module. Every finding in the report should answer: *"why does this gap matter?"*

## Workflow

Do these phases in order. Don't skip ahead — earlier phases set up context for later ones.

### Phase 1: Test inventory

Run `scripts/test_inventory.sh <repo-path>`. This produces:
- Test framework(s) detected (Jest, Pytest, RSpec, Go test, PHPUnit, etc.)
- Test file count, source file count, ratio
- Test location pattern (alongside source, separate `tests/` dir, mixed)
- CI test invocation (does CI actually run tests?)

If the script can't run (no shell, restricted env), do the inventory manually: look for `test/`, `tests/`, `spec/`, `__tests__/`, `*.test.*`, `*_test.*`, `*.spec.*` patterns and the test framework in the manifest file.

For per-language test conventions and framework detection details, see `references/language-notes.md`.

**Stop and report** if there are zero tests. That's the entire finding.

### Phase 2: Coverage data

Look for existing coverage artifacts before running anything:
- `coverage/`, `htmlcov/`, `.coverage`, `coverage.xml`, `lcov.info`, `coverage.json`
- CI config that uploads to Codecov, Coveralls, etc.

If coverage data exists, parse it. If not, **do not try to generate it** — running the test suite is out of scope and may have side effects. Note in the report that no coverage data was available and assessment is based on static analysis.

### Phase 3: Risk map (this is the heart of the assessment)

For each significant module/directory, determine **risk level** and **coverage level** independently, then map them. Run `scripts/risk_map.sh <repo-path>` for the mechanical risk pass, then apply the rubric in `references/risk-mapping.md` to refine it.

**Risk signals** (high-risk modules show these):
- Handles money, payments, billing, refunds
- Auth, authn, authz, sessions, tokens, permissions
- Data deletion, account deletion, GDPR endpoints
- External API calls (especially writes — POST/PUT/DELETE)
- Database writes, migrations, schema changes
- File system writes, especially user-controlled paths
- Cryptography, hashing, signing, key handling
- Concurrency, locking, queues, retries
- Input parsers, especially for untrusted input
- Anything in the request/response path of public endpoints

**Coverage signals** (use static analysis since you may not have runtime data):
- Existence of corresponding test file (`foo.ts` → `foo.test.ts` or `tests/foo.test.ts`)
- Number of test cases vs. number of exported functions/methods
- Whether the test file imports the module under test directly or only mocks it
- Whether tests appear to exercise error paths (look for `throws`, `rejects`, `Error`, error-case test names)

Read `references/risk-mapping.md` for the full rubric. Output: a table of modules with risk level (Critical/High/Medium/Low) × coverage level (None/Sparse/Partial/Solid). The interesting cells are **Critical+None** and **High+Sparse** — these become top findings.

### Phase 4: Test quality scan

Run `scripts/test_smells.sh <repo-path>`. This finds:
- Tests with no assertions
- Tautological assertions (`expect(x).toBe(x)`, `assertEqual(a, a)`)
- `.skip`, `.only`, `xit`, `xdescribe` left in
- `@Disabled`, `@Ignore`, `pytest.mark.skip` annotations
- Snapshot tests (often overused, often blindly updated)
- Tests that hit real network/DB (look for actual hostnames, no mocks)
- Tests with hardcoded sleeps/timeouts (flakiness signal)
- Over-mocking (test files that mock everything they import)

Read `references/test-smells.md` for what each finding means and how to triage.

### Phase 5: Test type coverage

A codebase needs different *kinds* of tests. Identify which exist and which are missing:

- **Unit tests** — fast, isolated, test single functions/classes
- **Integration tests** — test modules together, real DB, real I/O at module boundaries
- **API/contract tests** — exercise the public API surface end-to-end
- **End-to-end tests** — full user journeys through the running app
- **Property-based / fuzz tests** — for parsers, validators, anything with input space
- **Regression tests** — test cases for previously-fixed bugs

A repo with only unit tests and no integration tests has a real gap. A repo with only E2E tests has a different (worse) gap. See `references/test-types.md`.

### Phase 6: CI and hygiene

Check whether tests are actually running and being taken seriously:
- Does CI run tests on every PR?
- Are failing tests blocking merges or are they advisory?
- Are skipped/disabled tests tracked? (Count them — if growing, it's a sign of decay.)
- Is there a flaky-test quarantine that's becoming a graveyard?
- Are tests run on the same OS/runtime as production?

A test suite that exists but isn't enforced is barely better than none.

### Phase 7: Compose the report

Use `assets/report-template.md`. The report has these sections:

1. **Executive summary** — 3-5 sentences. State the headline: is the suite healthy, struggling, or absent? What's the single biggest gap?
2. **The numbers** — file counts, ratios, frameworks, coverage if available. Two paragraphs max.
3. **Risk map** — the table from Phase 3. This is the centerpiece.
4. **Top gaps** — the Critical+None and High+Sparse cells expanded into findings, each with: what's untested, why it matters, what kind of test would help.
5. **Quality findings** — smells, anti-patterns, hygiene issues from Phases 4-6. Severity-ranked.
6. **What's working well** — earn credibility for the negatives by acknowledging strengths. Don't fabricate; if there's nothing good, say "the suite has structural issues that should be addressed before evaluating test quality."
7. **Recommended next steps** — a 30/60/90-style plan. Not a backlog — a *prioritized* list. The owner should be able to start Monday morning and know which test to write first.

## Severity guide

Use this consistently. Inflation makes real Criticals invisible.

- **Critical** — Untested code that handles money, auth, data deletion, or PII. A bug here = incident or breach.
- **High** — Untested code in core business logic, or a structural test problem (no integration tests at all, CI doesn't run tests).
- **Medium** — Sparsely-tested complex modules; quality smells that affect reliability of the suite (skipped tests, no assertions).
- **Low** — Style issues, minor smells, modules that probably should have tests but the risk is low.
- **Info** — Observations worth flagging but not actionable on their own.

## Sampling for large codebases

If the repo is over ~100k LOC or has thousands of files, don't try to assess everything. Instead:

1. Run the inventory and smell scans across everything (cheap).
2. For risk mapping, focus on:
   - Top 20 most-changed files (use `git log --pretty=format: --name-only | sort | uniq -c | sort -rn`)
   - Files in directories named like `auth/`, `billing/`, `payments/`, `users/`, `api/`
   - Files with names suggesting risk: `*payment*`, `*auth*`, `*permission*`
3. State the sampling approach in the report's intro.

## Graceful degradation

If shell scripts can't run (web environment, no bash, etc.):
- Do the inventory by reading directory structure and manifest files manually
- Do the smell scan by reading test files directly and checking for the patterns listed in `references/test-smells.md`
- Skip Phase 6 hygiene scoring if you can't read CI config; note the gap in the report

The point is to deliver a useful report even with reduced tooling, not to abort.

## When the user is also asking for test generation

If the user says "find gaps and write tests for them," do the assessment and then **stop**. Output the report and tell them: "I've identified the gaps. Test generation is a separate task — want me to run the test-suggest skill to design concrete test cases for the top 3 findings?" Don't silently do both.
