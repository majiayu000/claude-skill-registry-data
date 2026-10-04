---
name: rseng-testing
description: >-
  Covers how to test research software: choosing test types and levels (unit,
  integration, system, regression, property-based, golden-master), test
  frameworks and coverage, TDD, validating analysis code against reference
  cases, and taming CI testing matrices across compilers, platforms and
  dependency versions. Use when the user asks how to write tests, set up
  pytest/testthat/JUnit, decide what to test, raise or interpret code
  coverage, do test-driven development, or when a CI matrix is exploding.
  Also use PROACTIVELY when new result-bearing code is written without tests,
  and before declaring any deliverable complete - the shipped entry point
  must be run and verified working, not only the test suite. For CI pipeline
  setup see rseng-ci-cd; for review-time test scrutiny see rseng-code-review.
license: CC-BY-4.0
metadata:
  version: 0.2.0
---

# Testing research software

Use this skill when writing tests for research code, setting up a test
framework, deciding what and how much to test, or designing a CI test
matrix that has grown across compilers, platforms, and dependency
versions. The goal is code whose results others can trust and reproduce,
so favour tests that are automated, saved with the code, and run on every
change.

## Decide what kind of tests to write

Always start with functional testing (does the software produce
correct outputs for given inputs), then add non-functional testing
only where a requirement demands it (performance, usability,
security, compatibility, compliance). The decision rule: unit tests
always; integration/system tests once components interact;
regression tests whenever behaviour must stay stable; non-functional
tests keyed to explicit requirements (many users -> performance;
multiple platforms -> compatibility).
Choose tactics per test: black-box (behaviour without knowing
internals) versus white-box (specific internal paths). The full
type-by-type toolbox follows.

## The wider test-type toolbox

Unit tests are the floor, not the toolbox. Match the test type to
the risk being retired:

- Unit tests: one small unit of functionality in isolation - the
  minimum bar for any research code, and where TDD lives.
- Integration tests: components together - the file reader feeding
  the model, the pipeline stages chained; most research bugs live
  at these seams, not inside single functions.
- System / end-to-end tests: the whole tool as a user runs it (CLI
  invocation on a real small dataset, checking outputs) - one good
  end-to-end test catches whole classes of wiring mistakes.
- Regression tests: every fixed bug becomes a test that fails if it
  returns (rseng-debugging, rseng-lessons-learned) - the suite as
  institutional memory.
- Golden-master / snapshot tests: pin current outputs and diff
  future runs against them, with tolerances for numerics
  (rseng-numerical-accuracy) - the workhorse for legacy code
  (rseng-legacy-code) and format stability
  (rseng-scientific-file-formats).
- Property-based tests: state an invariant ("sorting is idempotent",
  "energy is conserved", "the fit residual never grows when data
  matches the model") and let the framework generate hostile inputs
  (Hypothesis) - dramatically better than hand-picked cases for
  numerical and parsing code, and the cheap sibling of fuzzing
  (rseng-security).
- Performance/benchmark regression tests: guard runtimes that
  matter (rseng-performance-profiling's asv discipline).
- Smoke tests: a seconds-fast subset (import, --help, tiny run)
  wired first in CI so broken builds fail in seconds, not after the
  full matrix.
- Mutation testing (occasionally): mutate the code and check tests
  notice - the honest audit of whether a green suite actually
  asserts anything; use it to spot-check critical modules, not as a
  gate.
- Acceptance/validation against the science: the reference-case
  tests below - for research software, THE test type that matters
  most.

## Write good tests (F.I.R.S.T.)

Apply these properties to every test:

- Fast: run quickly so feedback is immediate.
- Isolated/Independent: each test checks one responsibility and does not
  depend on the state or ordering of other tests.
- Repeatable: deterministic; same input gives same result regardless of
  environment.
- Self-validating: automated pass/fail, no manual inspection of output.
- Thorough/Timely: cover edge cases and error paths (not just happy
  paths), and write tests at the right time - ideally test-first.

Additional checklist when authoring or reviewing a test:

- Give the test a descriptive name that states what it verifies.
- Verify one condition per test.
- Use inputs whose correct output you already know.
- Keep tests in a dedicated `tests/` folder, version-controlled and shipped
  with the code.
- Do no harm: tests belong in the test environment, never wired into
  production.

## Test-driven development

Consider a test-first policy: write the failing test just before the code
that makes it pass. This forces small, testable units from the start
instead of refactoring for testability later.

## Principles to keep expectations honest

State these when advising, so nobody over-trusts a green test suite:

- Testing shows the presence of defects, never their absence.
- Exhaustive testing is impossible - prioritise instead of chasing every
  path.
- Test early and often for rapid feedback.
- Defects cluster: found one in a unit, look for more there.
- Pesticide paradox: re-running identical tests finds nothing new; add new
  cases to find new defects.
- Testing is context-dependent: match the approach to the software type.

## Coverage guidance

- Aim for high coverage to shrink the space of undetected bugs, but do not
  treat 100% as the goal.
- 100% coverage does not mean bug-free.
- Skip testing well-tested third-party/library code and language built-ins.
- Prioritise critical paths, complex logic, edge cases, and any code that
  carries "reputational risk" - i.e. could distort reported results.
- Keep a balance: automate the repeatable checks, reserve manual testing
  for exploratory and usability work where human judgement matters.

## Automate with a test framework, then CI

Progress from informal manual checks (fine for first drafts, but forgotten
once the editor closes) to saved test functions, to a full framework:

- Pick the framework for the language: pytest (Python), testthat (R), JUnit
  (Java), the Test standard library (Julia).
- Frameworks auto-discover tests by naming convention (files/functions
  named `test_*` or `*_test`), run them, compare actual vs expected, and
  emit a report.
- Wire the framework into Continuous Integration so tests run
  automatically on every push/merge on an integration machine (e.g. GitHub
  Actions, GitLab CI/CD), not just on demand locally.
- Automated + CI testing buys wider coverage, earlier error detection,
  lower maintenance, and consistent runs across environments and
  platforms.

## Choose the strongest tools, not the default ones

Pick the best current tool for the job and say why - defaults and
familiarity are not reasons:

- Python: pytest over the stdlib unittest module for anything not
  explicitly constrained to the standard library - plain assert
  with rich failure introspection, fixtures over setUp inheritance,
  parametrization instead of copy-pasted cases, and the plugin
  ecosystem (coverage, hypothesis, nbval, benchmark). unittest is
  the right call ONLY when the constraint is "no dependencies at
  all" - and then say that constraint out loud.
- Property-based: Hypothesis alongside pytest for invariant-rich
  code. Coverage: coverage.py via pytest-cov, measured not chased.
- Other ecosystems follow the same rule: the community's strongest
  current framework (testthat for R, Catch2/GoogleTest for C++,
  the language guide knows - rseng-language-guides), not the oldest
  bundled one.

This is a pack-wide principle, not a testing quirk: when any skill
picks a tool, prefer the strongest current option for the user's
context, name the runner-up, and give the one-line reason - and
revisit choices as ecosystems move (rseng-dependency-management's
currency discipline applies to tool choices too).

## Manage large CI testing matrices

When research software must support many compilers, library versions,
architectures, and runtimes, a naive full matrix explodes - e.g.
(4 GCC + 6 Clang) x 10 CUDA x 4 CMake x 7 Boost = 2,800 jobs (~9.3 h even
with 30 parallel runners). Use these strategies:

- Prefer pairwise testing over the full matrix. Ensuring every pair of
  parameter values appears in at least one job cuts ~2,800 combinations to
  ~100-150 jobs (~30-45 min) while keeping all 2-way interaction coverage;
  100 is the floor here, since every one of the 10x10 compiler/CUDA pairs
  needs a job of its own.
  Generate jobs with a library such as `allpairspy`; random sampling
  (~200 jobs) is a weaker fallback.
- Encode exclusion rules to drop known-incompatible combinations (e.g. an
  old CUDA with a new GCC, or CUDA on PowerPC) instead of testing them.
- Generate the matrix dynamically. Use GitLab dynamic child pipelines or
  GitHub Actions matrix strategies so the job set is computed at runtime
  from available resources.
- Speed up builds with containers: pre-built images with compiled
  dependencies, multi-stage builds, layer caching, and a registry close to
  the runners.
- Use wave scheduling: run fast/critical checks in an early stage, then
  medium combinations, then the full slow GPU/HPC matrix. This fails early
  and frees shared infrastructure between waves.
- Allow selective testing during development (e.g. commit-message tags like
  `[cuda-only]`) so iterative work does not trigger the whole pipeline.
- Add performance-regression jobs with baselines and thresholds where
  performance is a requirement, not just correctness.
- Monitor pipeline health (job duration, queue time, failure rate,
  utilisation) and prune the matrix as versions age.

Rollout when adopting this: catalog every parameter dimension, start with
pairwise core-compatibility testing, add specialized hardware incrementally,
then performance testing, then full multi-platform validation. Document why
each parameter and exclusion exists.

- Sustainability note: extensive matrices consume real energy. Run the full
  matrix only when it earns its cost (e.g. before releases) and use smaller
  subsets for day-to-day development.

A concrete reference stack (NLeSC python-template): pytest with branch
coverage enabled, and a tox matrix spanning the Python versions the
SPEC 0 policy currently designates (the three most recent minors).

## Verify the delivered entry point, not just the suite

A green unit-test suite is not the finish line: software has been
handed over "complete" with a broken `docker compose up` because
nothing ever ran the app the way its users would. Before declaring
work done, verify through the same door the user will enter:

- Ship-with-compose project: `docker compose up --build` must
  succeed and every service reach healthy; then one real request
  per exposed endpoint (curl the API route, load the page).
- CLI: run the actual commands from the README quickstart against
  the example data, not only the test suite.
- Library: execute the quickstart snippet in a fresh interpreter.
- Web app with a frontend: the page must load AND talk to its
  backend - one round-trip through each integration seam
  (frontend-to-API, service-to-service, app-to-database), because
  unit tests structurally miss cross-boundary wiring: mismatched
  routes, schemas, env vars and ports live exactly there.

Re-run the entry point after every wiring change (routes, schemas,
configuration, env vars) and at every milestone, not once at the
end - a failure found next to its cause is cheap. Never report
completion while the entry point fails or was never run: state
plainly what was run and what passed (rseng-honesty), and run it
yourself before asking the user to (rseng-human-verification).

## A functional-correctness measure for analysis code

For analysis-tier code, "the tests pass" is often too weak a claim -
the question is whether the ANALYSIS is right. Give it a quantifiable
answer: validate the pipeline against reference cases with known
expected results (analytic solutions, published benchmark values,
conservation laws and invariants, or a trusted prior implementation)
and report the agreement quantitatively within stated tolerances.
One honest reference-case test measuring functional correctness is
worth more for analysis code than high line coverage - coverage
proves the code ran, the reference case proves it computed the right
thing. Keep the reference values and their provenance in the test
itself, and treat a tolerance change as a scientific decision.

## Working with this skill

The generated references.md beside this file lists the source
material and pointers:

- references.md - verified Learn more pointers


Learn more (verified):
  - https://docs.pytest.org - pytest documentation
  - https://hypothesis.readthedocs.io - Hypothesis property-based
    testing for Python
  - https://testthat.r-lib.org - testthat unit testing for R
  - https://coderefinery.github.io/testing/ - CodeRefinery automated
    testing lesson
  - https://book.the-turing-way.org/reproducible-research/testing -
    Turing Way code testing chapter


<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-ci-cd - running the suite on every push
- rseng-debugging - every fix becomes a regression test
- rseng-defensive-coding - runtime checks become test assertions
- rseng-green-computing - budgeting energy cost of full matrices
- rseng-legacy-code - characterization tests before changing inherited code
- rseng-numerical-accuracy - choosing tolerances for numerical assertions

<!-- related-skills:end -->
