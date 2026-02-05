---
name: expert-debugging-and-lint-fixing
description: Systematic debugging workflow to reproduce, isolate, and fix hard software bugs, resolve related lint issues, and add tests and guardrails to prevent regressions. This skill should be used for complex bugs that teams struggle to fix, flaky/intermittent failures, production-only bugs, and environment-specific issues where code changes must be lint-clean.
version: 1.0.0
dependencies:
  - python>=3.8
---

# Expert Debugging & Lint Fixing

## Overview

This skill provides a systematic debugging playbook for extremely hard bugs that teams struggle to fix. It focuses on reproducing and isolating bugs through hypothesis-driven experiments, fixing root causes, explicitly resolving lint issues and static analysis findings in touched code, and adding tests and guardrails to prevent regressions.

## When to Use This Skill

Use this skill for:

- Complex bugs that were not solved by normal debugging approaches
- Flaky or intermittent failures that are difficult to reproduce
- Production-only or environment-specific bugs
- Cases where code changes also need to be lint-clean and align with project lint rules
- Bugs requiring systematic investigation with measurable progress
- Heisenbugs that change behavior when being debugged
- Performance issues, race conditions, or data corruption bugs

## Core Principles

Follow these principles throughout the debugging process:

- **Always define a precise bug contract**: "Given X, expect A, got B"
- **Prioritize reproducibility before attempting to fix**: If it cannot be reproduced, the current task is to make it reproducible
- **Use hypothesis-driven debugging, not random code edits**: Each change must test a specific hypothesis
- **Aggressively shrink the search space**: Use divide-and-conquer to isolate the failure
- **Treat lint and static analysis violations as bugs**: These must be resolved in changed areas
- **Finish with root-cause prevention, not just symptom fixes**: Add systemic guardrails to prevent recurrence

## Step-by-Step Debugging Protocol

### 1. Frame the Problem Precisely

Convert vague bug reports into a precise bug contract that can be verified.

**Actions:**
- State the bug as: "Given state X and input Y, expected A, got B"
- Capture all relevant context:
  - Who: Which user/role/environment
  - What: Exact behavior observed
  - When: Timing/frequency/conditions
  - Where: Component/service/layer
  - How often: Always/intermittent/once
  - Since when: Recent change or longstanding issue
- Identify the primary symptom and impact (user-visible, data corruption, performance degradation, security risk)
- Write one precise sentence describing the bug

**Gate:** If the bug cannot be stated in one precise sentence, do not touch code yet. Continue refining the problem statement.

### 2. Make It Reproducible (or Tightest Approximation)

Create the smallest, fastest, most reliable reproduction case possible.

**Actions:**
- Start from the real failing path (same API/UI/job and environment if possible)
- Strip down to the smallest input + environment that still fails
- Turn this into a script, unit test, or integration test that can be re-run
- For flaky bugs:
  - Run in a loop (100+ iterations)
  - Log every run with timestamps and relevant state
  - Capture failing cases for analysis
  - Look for patterns (timing, resource usage, specific inputs)
- Document the repro steps clearly

**Gate:** If the bug is not reproducible, the current task is: make it reproducible. Do not proceed until there is a way to trigger the failure on demand or with high probability.

### 3. Add/Improve Observability

Ensure logs, metrics, and traces illuminate the failing path.

**What to log:**
- Key parameters and branch decisions at each step
- External calls (database, cache, HTTP, queue operations)
- Concurrency boundaries (locks acquired/released, queues, async operations)
- State transitions and invariant checks
- Timing information (timestamps, durations)

**Logging quality:**
- Each log should answer: "What did we know? What did we decide? What happened next?"
- If logs are noisy and uninformative, refine them as part of the fix
- Use structured logging with correlation IDs to track requests through the system
- Include context that helps differentiate between different executions

### 4. Shrink the Search Space

Use systematic techniques to narrow down where the bug occurs.

**Binary search on time:**
- Use `git bisect` between known-good and known-bad commits
- Identify the exact commit that introduced the bug

**Binary search on code path:**
- Temporarily short-circuit sections or use feature flags to disable blocks
- See if the bug disappears when specific code paths are bypassed

**Isolate layers:**
- Replace real dependencies with fakes/mocks
- Try in-process vs over-the-network variants
- Test with minimal/maximal configurations

**Evaluation criteria:**
- Each step must move the bug closer or farther
- Avoid inconclusive changes that provide no information
- Document what each experiment revealed

### 5. Classify the Bug Type

Understanding the bug category dictates which tools and experiments to run next.

**Bug categories:**
- **Logic**: Wrong condition, off-by-one error, incorrect algorithm
- **Data**: Bad/inconsistent records, violated invariants, corrupted state
- **Environment/config**: Environment variables, version mismatches, feature flags
- **Concurrency/race**: Shared mutable state, timing-dependent behavior, deadlocks
- **Performance**: Memory leaks, excessive CPU usage, inefficient algorithms
- **Integration**: API contract violations, dependency issues, protocol errors

**Actions:**
- Identify the most likely category based on symptoms
- Select appropriate debugging tools for that category
- Prepare specific experiments to confirm or rule out the classification

### 6. Hypothesis-Driven Experiments

Conduct systematic experiments to identify the root cause.

**Process:**
1. List top hypotheses (3–5 most likely causes)
2. For each hypothesis, define:
   - "If this is the cause, then doing X should produce observable Y"
   - How to test it (minimal change, log addition, config tweak)
   - What outcome would falsify it
3. Run minimal, fast experiments to falsify hypotheses
4. Discard falsified hypotheses quickly; don't cling to favorite theories
5. After each experiment, explicitly state:
   - What was tested
   - What was observed
   - What was learned
   - Which hypotheses remain viable

**Avoid:**
- Testing multiple hypotheses at once (confounds results)
- Making large changes without clear predictions
- Confirmation bias (looking only for evidence that supports preferred theory)

### 7. Use the Right Tools (Including Linters)

Select debugging tools appropriate for the bug type.

**For logic bugs:**
- Debuggers with breakpoints, conditional breakpoints, watchpoints
- Print debugging with strategic log placement
- Unit tests that isolate specific functions

**For performance/leak issues:**
- Profilers (CPU, memory, I/O)
- Memory leak detectors
- Performance monitoring tools

**For concurrency issues:**
- Thread sanitizers
- Race condition detectors
- Stress testing with high parallelism

**For all bugs:**
- Run all relevant linter and static analysis tools on:
  - The changed files
  - Ideally the impacted module/package
- Tools include: ESLint, Flake8, mypy, Pylint, go vet, clippy, custom linters
- **Treat new or existing lint violations in the changed area as part of the work to fix**

### 8. Handle Flaky and Heisenbugs

For bugs that appear/disappear unpredictably, use amplification techniques.

**Amplify the bug:**
- Run repro in tight loops (1000+ iterations)
- Run in parallel with multiple processes
- Run under stress (high CPU/memory/disk usage)
- Introduce jitter and delays to surface race conditions
- Use chaos engineering techniques (network delays, packet loss, resource constraints)

**Capture evidence:**
- Take snapshots/dumps on detected bad states if tools allow
- Correlate logs/traces/metrics with unique request or correlation ID
- Record timing information to identify patterns
- Save state before/after failure for comparison

**Reduce noise:**
- Disable unrelated jobs/traffic/features to simplify
- Use minimal test data
- Isolate the system under test from external dependencies

### 9. Implement the Fix

Make the smallest, clearest change that eliminates the failing behavior.

**Fix quality criteria:**
- Eliminates the failing behavior in the repro case
- Respects the system's invariants and constraints
- Maintains or improves code clarity
- Does not introduce new bugs or performance issues
- Aligns with team coding standards

**Approach:**
- Prefer refactors that increase clarity over patchy hacks
- Keep commits focused and well-described for easy review
- Include comments explaining non-obvious aspects
- Consider edge cases and boundary conditions
- Update any affected documentation

**Before committing:**
- Verify the fix resolves the original bug
- Check for unintended side effects
- Ensure the fix doesn't just move the problem elsewhere

### 10. Validation: Tests, Lint, and CI

Ensure the fix is complete and won't regress.

**Test the fix:**
- Turn the repro into an automated test that fails on the old code
- Confirm:
  - The new test fails on the pre-fix commit
  - The new test passes on the fix
- Add negative/edge-case tests around the bug
- Test related functionality for regressions

**Lint and static analysis:**
- Run the full lint suite relevant to the project
- Fix all lint issues in the changed files
- Do not ignore or suppress lint errors unless there is a clear, documented reason
- Ensure static analysis tools pass (type checkers, security scanners)

**CI validation:**
- Run the existing test suite (or at least impacted subset)
- Ensure all CI checks pass (build, tests, linting, security scans)
- Verify no new warnings are introduced
- Check that code coverage hasn't decreased

### 11. Root Cause Analysis & Systemic Prevention

Prevent similar bugs from occurring in the future.

**Write a root cause summary:**
- When was the bug introduced? (specific commit/release)
- When was it detected? (how long did it exist?)
- Why was it not caught earlier? (gaps in testing, code review, monitoring)
- What was the underlying cause? (not just the symptom)

**Conduct "5 Whys" analysis:**
1. Why did the bug occur? (immediate cause)
2. Why did that happen? (contributing factor)
3. Why was that possible? (system weakness)
4. Why wasn't this caught? (process gap)
5. Why does this pattern exist? (root cause)

**Add systemic guardrails:**
- New tests (unit, integration, property-based, regression)
- Stronger validation and type checks
- Runtime invariant assertions
- Lint rules or static checks that catch similar issues early (when possible)
- Monitoring/alerting to detect similar failures
- Documentation updates (architecture docs, code comments, runbooks)
- Code review checklist items for this module

**Share learnings:**
- Update team documentation
- Present findings in team meetings
- Add to incident postmortem if applicable

### 12. Team Protocol for "Impossible Bugs"

When escalating difficult bugs to the team, provide comprehensive context.

**Required information:**
1. One-sentence bug contract ("Given X, expect A, got B")
2. Repro script or test that demonstrates the failure
3. Logs/metrics/traces for a failing run
4. Top hypotheses and experiments tried with outcomes
5. Relevant commit range and config/environment diffs
6. Impact assessment (severity, affected users, workarounds)

**Escalation gate:**
- Use this checklist as a gate before escalating to senior engineers
- Ensures sufficient investigation has been done
- Provides context for effective collaboration

## Linting and Static Analysis Protocol

Linting and static analysis are integral to the debugging process, not optional cleanup.

### Always Run Relevant Tools

For every file modified during debugging:
- Run all relevant linters (language-specific and project-specific)
- Run static analyzers (type checkers, security scanners)
- Run code formatters if the project uses them

**Common tools by language:**
- **JavaScript/TypeScript**: ESLint, Prettier, TSLint
- **Python**: Flake8, Pylint, Black, mypy, Bandit
- **Go**: go vet, golint, staticcheck
- **Rust**: clippy, rustfmt
- **Java**: CheckStyle, SpotBugs, PMD
- **Ruby**: RuboCop
- **C/C++**: clang-tidy, cppcheck

### Fix Lint Issues

**What to fix:**
- All newly introduced lint issues (from the changes made)
- Existing lint issues in the touched code region (where feasible)
- Critical security or correctness issues flagged by static analysis

**When to suppress:**
Only suppress or relax lint rules when:
- There is a clear, written justification
- The justification is documented in a code comment
- Preferable to update configuration rather than scattered inline disables
- The team agrees this is an appropriate exception

**Never:**
- Ignore lint errors by disabling the linter
- Commit code with unresolved lint violations without justification
- Suppress entire categories of checks without review

### Treat Passing Lint as Part of "Done"

A bug fix is not complete until:
- The bug is fixed
- Tests are added
- All lint checks pass
- CI pipeline is green

## Example Usage

### Example 1: Flaky CI Test

**User prompt:** "We have a flaky test in our CI that fails randomly on our Node service. Help us track it down and fix it."

**How this skill applies:**

1. **Frame the problem**: Identify which test fails, under what conditions, and how frequently
2. **Make it reproducible**: Run the test in a loop locally (1000+ iterations), capture failing cases
3. **Add observability**: Add detailed logging around the failing assertions, log timing information
4. **Shrink search space**: Isolate the test from others, run with minimal fixtures
5. **Classify**: Likely a race condition or timing issue
6. **Hypothesize**: Test hypotheses like "async operation not awaited", "shared state between tests", "timing-dependent assertion"
7. **Use tools**: Run with stress testing, check for race conditions
8. **Fix**: Add proper awaits, isolate test state, or fix timing assumptions
9. **Validate**: Ensure test passes 10,000+ times in a row, run ESLint/Prettier on changed files
10. **Prevent**: Add test isolation guards, document async patterns

### Example 2: Production 500 Errors

**User prompt:** "Production is throwing intermittent 500s on checkout; logs are unclear. Guide me through reproducing and fixing this."

**How this skill applies:**

1. **Frame the problem**: "Given checkout request with cart X, expect 200 OK, got 500 Internal Server Error"
2. **Make it reproducible**:
   - Gather production logs with correlation IDs
   - Identify common patterns in failing requests
   - Create test with similar cart composition/state
3. **Add observability**:
   - Enhance logging in checkout flow
   - Log all external service calls (payment, inventory)
   - Log state transitions
4. **Shrink search space**:
   - Test each checkout step in isolation
   - Mock external services to identify which dependency causes failures
5. **Classify**: Likely an integration issue (external service) or data issue (bad cart state)
6. **Hypothesize**: Test theories like "payment service timeout", "inventory service race condition", "invalid cart state"
7. **Fix**: Add proper error handling, validate cart state earlier, implement retry logic
8. **Validate**: Run lint tools on modified files, add integration tests for edge cases
9. **Prevent**: Add input validation, monitoring alerts for 500s, circuit breakers for external services

### Example 3: Lint Violations After Quick Patch

**User prompt:** "I applied a quick patch to stop a crash, but now our linter is complaining all over that file."

**How this skill applies:**

1. **Re-evaluate the patch**: Check if the quick fix actually addresses the root cause or just the symptom
2. **Frame the original problem**: Define what crash was occurring and why
3. **Improve the implementation**:
   - Refactor the patch to follow code standards
   - Address the root cause properly, not just the symptom
4. **Fix lint issues**:
   - Run linter and address all violations in the file
   - Do not suppress the linter without justification
   - Ensure the fix follows team coding standards
5. **Validate**: Add tests that prove the crash is fixed, ensure lint passes
6. **Prevent**: Add guardrails to prevent similar crashes, document the fix

### Example 4: Memory Leak in Long-Running Service

**User prompt:** "Our API service's memory usage grows unbounded over days. Find and fix the leak."

**How this skill applies:**

1. **Frame the problem**: "After X hours of operation, memory usage reaches Y GB and service crashes"
2. **Make it reproducible**:
   - Create load test that simulates days of traffic in minutes
   - Monitor memory usage during test
3. **Add observability**:
   - Add memory profiling
   - Log object creation/destruction for suspected components
4. **Classify**: Memory leak (performance bug)
5. **Use tools**:
   - Memory profilers (heapdump, valgrind, etc.)
   - Analyze heap snapshots over time
6. **Hypothesize**: Test theories like "event listeners not removed", "cache growing unbounded", "circular references"
7. **Fix**: Remove event listeners, add cache eviction, break circular references
8. **Validate**:
   - Run extended load test, verify memory stays stable
   - Run linter on changed files
   - Add regression test that monitors memory growth
9. **Prevent**: Add memory monitoring alerts, document lifecycle management patterns

## Related Skills

This skill focuses on systematically debugging hard bugs. For related tasks, use:

- **test-specialist**: Writing comprehensive tests after fixing bugs (TDD approach, test coverage analysis)
- **code-validation**: Validating fixes don't introduce red flags (secrets, test disabling, security issues)
- **test-quality-audit**: Auditing test quality after adding regression tests
- **test-standards**: Ensuring test code follows project standards
- **webapp-testing**: Browser-based debugging and E2E test creation for web applications
- **chrome-devtools**: Browser performance debugging and Core Web Vitals measurement

## Resources

This skill does not require bundled scripts, references, or assets. The debugging protocol is entirely procedural and can be applied to any programming language, framework, or bug type.

If language-specific debugging scripts or checklists would be helpful for your team's common debugging scenarios, they can be added to the `scripts/` directory. Similarly, team-specific debugging runbooks or reference materials can be added to `references/`.
