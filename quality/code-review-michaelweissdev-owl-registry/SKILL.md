---
name: code-review
description: >
  Conduct systematic, actionable code reviews assessing correctness, security,
  architecture, performance, maintainability, and test coverage. Use when
  reviewing pull requests, inspecting diffs, providing constructive code feedback,
  identifying edge cases and regressions, or prioritizing findings by severity.
compatibility: >
  Agent Skills-compatible coding agents analyzing code diffs, pull requests,
  or codebase refactorings.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "code-review, quality, testing, security, maintainability, pr-review"
  topics: "software-development, devtools"
---

# Systematic Code Review

A professional code review evaluates whether proposed changes solve the user's problem correctly, securely, and maintainably without introducing regressions. Effective reviews provide constructive, prioritized feedback with concrete line references and proposed remediations.

## Core Rules

1. **Prioritize correctness and security first**: Functional bugs, security vulnerabilities, race conditions, and data loss risks take precedence over stylistic preferences.
2. **Review the whole context, not just the diff**: Inspect the calling code, unit tests, and dependent modules to understand downstream side effects.
3. **Structure findings by severity**: Clearly distinguish between blocking defects and optional suggestions.
4. **Be constructive and actionable**: Don't just say "this is bad"; explain *why* it fails and provide a concrete snippet or alternative approach.
5. **Verify test coverage**: Does the PR include tests for edge cases, failure paths, and boundary conditions? Untested fixes are incomplete.
6. **Separate style from logic**: Let automated linters and formatters enforce formatting; humans and agents should focus on semantics, contracts, and architecture.

---

## 1. Finding Severity Hierarchy

Use standardized severity tags in review comments:

- **[Blocker / Critical]**: Bugs causing crashes, security vulnerabilities (SQLi, XSS, RCE), data corruption, race conditions, or breaking public API contracts. Must be fixed before merge.
- **[Major]**: Architectural regressions, significant performance bottlenecks (e.g. N+1 queries), missing error handling at boundaries, or lack of unit tests for new logic.
- **[Minor]**: Suboptimal naming, minor code duplication, missing docstrings on public functions, or edge cases with low probability of impact.
- **[Suggestion / Nit]**: Non-blocking improvements, minor idiomatic refactors, or stylistic preferences.

---

## 2. Systematic 6-Pillar Review Checklist

### Pillar 1: Correctness & Logic
- Does the code actually implement the stated requirement?
- Are off-by-one errors present in loop boundaries or slices?
- Are null/nil/None values handled defensively?
- Does the change handle empty collections, zero values, and Unicode text safely?

### Pillar 2: Security & Privacy
- Are user inputs sanitized, validated, and parameterized in SQL/shell commands?
- Are secret credentials, API keys, or tokens hardcoded?
- Are authentication and authorization checks enforced before data access?
- Is sensitive PII masked in log outputs?

### Pillar 3: Performance & Scalability
- Are there N+1 queries in loops fetching database records?
- Are large collections loaded entirely into memory when streams/iterators are suitable?
- Are locks held across slow network I/O calls?

### Pillar 4: Architecture & Design
- Does the change violate the Single Responsibility Principle?
- Are public API contracts backward-compatible?
- Is there unnecessary tight coupling between independent modules?

### Pillar 5: Error Handling & Resilience
- Are exceptions caught specifically or swallowed with broad `catch`/`except`?
- Are external resources (sockets, file descriptors, transactions) guaranteed to close on failure?
- Are error messages informative without leaking internal system traces to clients?

### Pillar 6: Test Completeness
- Are both positive (happy path) and negative (error conditions) tested?
- Are mocks used judiciously without mocking out the actual unit under test?
- Are tests deterministic (no reliance on real timers or external network)?

---

## 3. Formatting an Exemplary Review Comment

```markdown
### Review Summary
The PR implements the caching layer as described in RFC-88. The core logic is sound,
but there is one critical data-race issue during cache expiration and missing tests
for Redis connection drops.

---

#### 1. [Blocker] Potential Cache Stampede & Race Condition
**Location**: `src/cache/manager.py#L45-L52`

**Problem**: When a cache key expires, all concurrent worker threads simultaneously
miss the cache and issue identical heavy queries to the primary database.

**Suggested Fix**:
Use a mutex lock or probabilistic early expiration to ensure only a single worker
refreshes the cache:

```python
with self._lock_for_key(key):
    # Re-check cache inside lock to prevent redundant fetches
    cached = self._store.get(key)
    if cached is not None:
        return cached
    data = self._fetch_from_db(key)
    self._store.set(key, data, ttl=300)
    return data
```

---

#### 2. [Major] Missing Negative Test Cases
**Location**: `tests/test_cache.py`

**Problem**: Tests only verify cache hit and cache miss under ideal conditions.
There are no tests simulating Redis connection timeouts or network resets.

**Recommendation**: Add a test using `unittest.mock` simulating `ConnectionError`
to ensure the application falls back gracefully to database reads.
```

---

## 4. Verification Checklist

- [ ] Every finding has an exact file path and line reference.
- [ ] Every finding explains the risk/impact and proposes a concrete resolution.
- [ ] Findings are prioritized using standard severity labels ([Blocker], [Major], [Minor], [Nit]).
- [ ] Confirmed that automated CI checks (linting, tests) pass.
