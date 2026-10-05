---
name: python-backend-review
description: Review Python backend repositories at the foundation layer for target Python version compatibility, Python implementation quality, type system clarity, async/sync correctness, exception semantics, configuration and environment handling, logging and observability, packaging and dependency hygiene, Python package hygiene, testing and maintainability, and Python complexity/readability. Use when Codex needs a version-aware Python backend fundamentals review against a user-specified or inferred Python version. Do not use for architecture review, deep agent-legibility review, framework-specific FastAPI, SQLAlchemy, Pydantic, or Django review, security audit, performance deep dive, onboarding review, or business-domain review unless the user explicitly asks to include those scopes.
---

# Python Backend Review

Review a Python backend repository against a target Python version and durable production Python standards. Keep the review focused on Python backend fundamentals: implementation quality, verification, and maintainable use of the language. Do not evaluate architecture strategy, business-domain design, framework-specific best practices, or onboarding quality.

Do not modify code during the review unless `review_only` is explicitly false. If fixes are allowed, complete the review first, then make only the requested or clearly justified Python-fundamentals changes.

## Review Principles

- Review baseline-first: use an existing project Python baseline as the current project profile before proposing new conventions.
- Treat official version guidance as a compatibility and quality reference, not a mandate to adopt every available feature.
- Prefer consistency, correctness, readability, verification, and operational reliability over syntax novelty.
- Recommend a change only when its expected benefit exceeds migration, review, testing, rollback, tooling, and production costs.
- Keep recommendations small, location-specific, and testable.
- Stay within Python backend fundamentals; defer architecture, deep agent-legibility, framework, business-domain, onboarding, and developer-experience concerns to other review skills.
- Every finding is a hypothesis. Before reporting it, actively attempt to disprove it. A finding should only survive if the available repository evidence does not invalidate it.

## Inputs

Support these inputs:

- `target_python_version`: target version such as `3.12`, `3.13`, `3.14`, or a future supported version.
- `allow_web_research`: `true` or `false`.
- `allow_persistent_baseline`: `true` or `false`.
- `frameworks_in_scope`: optional list such as `FastAPI`, `Django`, `SQLAlchemy`, or `Pydantic`; use only to evaluate how those frameworks interact with Python backend fundamentals.
- `review_only`: default `true`.

If `target_python_version` is not specified, infer it from local evidence in this order:

1. `pyproject.toml`, especially `requires-python`.
2. `.python-version`.
3. `Dockerfile`, compose files, runtime images, and build args.
4. CI config, test matrix, tox/nox config, and task runners.
5. README, deployment docs, and project notes.

If still unclear, state the uncertainty and use the most conservative version supported by the project config. Do not silently guess.

## Web Research Policy

If `allow_web_research` is `true`, research the target Python version before making version-specific recommendations. Prefer sources in this order:

1. Official Python documentation.
2. Official "What's New in Python X.Y".
3. Relevant PEPs.
4. Official packaging and typing documentation.
5. Official framework documentation only when `frameworks_in_scope` includes that framework.

Avoid blogs, Reddit, social media, and generic SEO articles as primary sources. Treat web results as advisory, cite official sources when used, and distinguish:

- version compatibility issues
- stable modernization opportunities
- optional new-language-feature adoption
- experimental or not-yet-worth-it features

## Persistent Baseline Policy

If `allow_persistent_baseline` is `true`, create or update a concise project-local Python profile such as `.manifest/python-version-baseline.md`.

If `.manifest/` does not exist, suggest creating it when useful, but do not assume it is mandatory. Keep the baseline concise and do not copy long sections from official documentation.

When a persistent baseline exists, use it as the project's current Python profile. Review code against the baseline before proposing new conventions. Do not contradict the baseline unless there is a clear compatibility, correctness, maintainability, or tooling reason. If the baseline is stale or wrong, recommend updating the baseline explicitly.

Use this shape when creating or refreshing the baseline:

```markdown
# Python Version Baseline

- target_python_version:
- version_source:
- reviewed_at:
- sources_consulted:

## Baseline Status

- current:
- stale:
- needs_update:
- reason:

## Project Python Profile

### Adopted Python Practices

Practices this project should consistently use.

### Avoided Python Practices

Practices this project intentionally avoids.

### Typing Policy

Expectations for type clarity, `Any`, raw dictionaries, aliases, protocols, and runtime validation boundaries.

### Async Policy

Expectations for blocking work, timeouts, cancellation, background tasks, and resource lifecycle.

### Error Handling Policy

Expectations for exception types, wrapping, context, and broad `except` usage.

### Packaging Policy

Expectations for dependency groups, lock files, build backend, runtime/dev dependency separation, and target-version compatibility.

### Revisit Triggers

Review this baseline when the Python version, major dependencies, framework stack, runtime image, packaging toolchain, or deployment target changes.
```

## Review Workflow

1. Establish the version baseline.
   - If a project-local Python baseline exists, read it first and treat it as the current project Python profile.
   - Review the repository against the existing baseline before applying new official version-specific guidance.
   - Compare Python declarations, runtime images, CI, lock files, dependency metadata, and local tooling.
   - Flag version mismatches before suggesting modernization.
   - If the baseline should change, say so explicitly and explain whether it is outdated, inconsistent with the target version, incompatible with tooling/dependencies, contrary to official guidance, or violated by project code.

2. Apply Python backend standards.
   - Inspect source packages, tests, configuration, packaging files, dependency files, task runners, and relevant docs.
   - Evaluate Python implementation quality, not architecture ownership or business-domain design.

3. Prioritize findings.
   - Separate compatibility/correctness risks from useful cleanup and optional improvements.
   - Prefer small, reviewable, testable improvements.
   - Run the Finding Disproof Pass before reporting findings.

4. Keep maintainability lightweight.
   - Ask whether future contributors can find relevant code, understand names, see important rules, and verify changes quickly.
   - Do not perform architecture review, framework review, or deep agent-legibility review.

## Finding Disproof Pass

Generate candidate findings first, then challenge each one against repository evidence before reporting it.

For each candidate:

- Search for counter-evidence in the project baseline, version declarations, lock files, CI, runtime images, tests, existing conventions, and official documentation when version-specific claims matter.
- Ask whether the candidate is a true compatibility or correctness issue, or only optional modernization.
- Check whether the project baseline intentionally avoids the newer pattern.
- Verify that the current library version or official documentation is enough to support the claim.
- Ask whether the recommendation would increase migration, review, testing, rollback, or production cost without improving correctness, maintainability, readability, verification, compatibility, or operational reliability.
- Downgrade or reject findings when counter-evidence is strong; preserve uncertainty instead of overstating modernization or compatibility claims.
- Avoid letting the same reasoning path both create and validate the finding without challenge.

When useful, list rejected modernization candidates under "Non-Issues / Intentionally Not Flagged" instead of reporting them as findings.

## Review Standards

### Version Compatibility

The declared, tested, packaged, and deployed Python versions should agree with the target version. Dependencies, build tools, lock files, runtime images, and CI should support the same version range. Code should avoid APIs, syntax, and dependency versions that are unavailable or deprecated for the target version.

Flag mismatches that can cause local/CI/production drift, unsupported dependency resolution, or future upgrade blockers.

### Version-specific Modernization

Modernization should use language features that are stable for the target version, supported by project tooling, and easier to read or verify than the older pattern. Older patterns may remain acceptable when replacing them would create churn without improving correctness or clarity.

Classify recommendations as compatibility fixes, stable modernization, optional adoption, or intentionally avoided features. Avoid features that are too new for the team/tooling, poorly supported by dependencies, unfamiliar without clear payoff, or likely to make code harder to debug.

### Stability And Change Cost

Can adopt does not imply should adopt. A version-specific modernization should only be recommended when its expected benefit exceeds the migration, review, testing, rollback, and operational costs.

Justify modernization by clear improvement in correctness, maintainability, readability, verification, compatibility, or operational reliability. Consider migration effort, review effort, test impact, rollback complexity, team familiarity, dependency/tooling compatibility, and production risk. Avoid recommendations whose main benefit is novelty, stylistic preference, using a newly released feature for its own sake, or replacing stable code without meaningful benefit.

### Type System And Static Analysis

Type information should be compatible with the target Python version, explicit at public boundaries, locally understandable, and strict enough to prevent common misuse. Return annotations should be present where absence obscures behavior. Avoid unnecessary `Any`, vague raw dictionaries, and untyped interfaces that force readers to infer shapes from distant code.

Use aliases, protocols, enums, literals, dataclasses, typed mappings, or similar tools only when they reduce ambiguity. Do not over-model simple values. Keep runtime validation clear where external input crosses into trusted code. If mypy, pyright, ruff, or similar tools are configured, evaluate whether their expectations are coherent and applied to the reviewed code.

Do not turn typing feedback into business-domain modeling review.

### Async/Sync Correctness

Async boundaries should make blocking behavior, concurrency, cancellation, timeouts, background work, and resource lifecycle explicit. Async functions should not perform blocking I/O or CPU work without isolation. Sync functions called from async paths should have a clear containment strategy. Resource acquisition and cleanup should remain reliable during errors and cancellation.

Flag code that can stall an event loop, leak resources, swallow cancellation, run unbounded work, or hide timeout assumptions.

### Exceptions And Error Handling

Exception handling should preserve meaning and context. Errors should be specific enough for callers and logs to distinguish expected failures from defects. Broad `except` blocks should be justified, narrow in scope, and avoid swallowing failures. Wrapping should add useful context without hiding the original cause.

Flag defensive branches that would be better guaranteed by types, validation, constraints, or tests. Prefer error paths that are easy to trace from a failing test or log entry.

### Configuration And Environment

Configuration should make runtime assumptions explicit and testable. Environment variables, defaults, secrets, and per-environment differences should have clear handling. Configuration should not be scattered in ways that make the effective runtime state hard to determine.

Flag implicit defaults, hidden environment dependencies, test/prod/dev drift, unsafe secret handling, and configuration patterns that make backend behavior hard to reproduce.

### Logging And Observability

Backend logging should consistently expose meaningful operation context without hiding failures or creating noise. Prefer logger usage over `print` in backend code. Logs should support debugging requests, jobs, integrations, and background work without leaking secrets.

Flag missing context, inconsistent logger setup, noisy success logs, suppressed failure details, and places where structured fields would materially improve troubleshooting.

### Packaging And Dependency Management

Packaging should make Python backend execution reproducible for the target version. Runtime and development dependencies should be separated when the project tooling supports it. Lock files, dependency groups, build backend, constraints, and dependency metadata should be coherent with CI and deployment.

Focus on reproducibility, target-version compatibility, dependency constraints, runtime/dev separation, lock file health, and the minimal tooling commands needed to verify review findings. Avoid broad onboarding comments unless they directly affect Python backend verification.

### Python Package Hygiene

Python packages should avoid import cycles, surprising import-time side effects, unclear public/private APIs, heavy `__init__.py` behavior, and generic `utils`, `helpers`, or `common` modules that hide unrelated behavior. Dependency direction between packages should be understandable at the Python package level.

Discuss package-local boundaries only as Python package hygiene. Do not evaluate domain ownership, service ownership, architectural layering, bounded contexts, team ownership, or business-domain boundaries.

### Python Complexity And Readability

Python code should be easy to reason about locally. Prefer explicit control flow over clever compactness. Avoid dynamic behavior unless it has a clear payoff. Be cautious with metaprogramming, runtime monkey-patching, dynamic imports, decorators with hidden behavior, reflection, implicit registration, and module import side effects.

Flag surprising mutation, hidden global state, clever comprehensions or lambdas where named functions are clearer, and abstractions that move complexity elsewhere instead of reducing it. Prefer small, testable units with clear inputs and outputs.

### Testing And Maintainability

Tests should verify critical Python behavior, compatibility-sensitive code, async boundaries, error paths, configuration loading, packaging assumptions, and risky refactors. Fixtures should make setup clear without over-mocking important behavior. Tests should be easy enough to run that review findings can be checked quickly.

Flag missing regression tests for risky behavior, tests that encode unclear rules, excessive mocking that hides integration failures, and verification gaps for proposed modernization.

## Priority Scale

- P0: correctness, compatibility, or serious maintainability risk.
- P1: high-value modernization or clarity issue.
- P2: useful cleanup.
- P3: optional improvement.

## Output Format

Use this structure unless the user explicitly asks for a different format:

```markdown
# Python Backend Review

## 1. Executive Summary

- target Python version:
- version source:
- web research used:
- persistent baseline updated:
- overall Python backend maintainability:
- top 3-5 risks:

## 2. Python Version Baseline

- baseline found:
- baseline status:
- baseline update recommended:
- declared version:
- detected runtime/tooling versions:
- mismatches:
- adopted version-specific practices:
- avoided version-specific practices:
- revisit triggers:

## 3. High-priority Findings

| Priority | Location | Issue | Standard violated | Recommendation | Risk if unchanged |
|---|---|---|---|---|---|
| P0/P1/P2/P3 | file/module/function/config/test or repo-wide | concrete issue | review standard not met | targeted action | likely consequence |

## 4. Area-by-area Review

### Version compatibility

Concrete findings with file/module/function/config references.

### Version-specific modernization

Concrete findings with file/module/function/config references.

### Stability and change cost

Concrete findings with file/module/function/config/test references.

### Type system and static analysis

Concrete findings with file/module/function/config references.

### Async/sync correctness

Concrete findings with file/module/function references.

### Exceptions and error handling

Concrete findings with file/module/function references.

### Configuration and environment

Concrete findings with file/module/function/config references.

### Logging and observability

Concrete findings with file/module/function references.

### Packaging and dependency management

Concrete findings with file/config references.

### Python package hygiene

Concrete findings with package/module references.

### Python complexity and readability

Concrete findings with file/module/function references.

### Testing and maintainability

Concrete findings with test/config/module references.

## 5. Recommended Improvement Plan

### Phase 1: low-risk, high-confidence improvements

- goal:
- changes:
- risk:
- acceptance criteria:

### Phase 2: changes requiring tests or careful review

- goal:
- changes:
- risk:
- acceptance criteria:

### Phase 3: optional longer-term improvements

- goal:
- changes:
- risk:
- acceptance criteria:

## 6. Follow-up Prompts

1. Directly executable, easy to review, easy to revert, preferably testable.
2. ...
```

Provide 3-5 follow-up prompts. Keep each prompt narrow and suitable for a small, reviewable change.

Add a compact `Non-Issues / Intentionally Not Flagged` subsection when it helps explain why optional modernization or apparent compatibility issues were rejected by the disproof pass.

## Behavior Rules

- Be concrete and location-specific.
- Avoid generic clean-code advice.
- Avoid architecture, business-domain, ownership, or large-scale repository-structure consulting.
- Avoid framework-specific recommendations unless `frameworks_in_scope` includes that framework.
- Even when `frameworks_in_scope` is provided, check only the framework's interaction with Python backend fundamentals. Do not perform a full framework review.
- Avoid onboarding or developer-experience review unless the issue directly blocks Python backend verification.
- Avoid changing code unless `review_only` is explicitly false.
- Read an existing project Python baseline before proposing new Python conventions.
- Prefer consistency with the existing baseline unless there is a clear reason to change it.
- If recommending a change that conflicts with the baseline, explicitly mark it as a proposed baseline update.
- Separate must-fix issues from nice-to-have cleanup.
- Reject or downgrade candidate findings that fail the Finding Disproof Pass.
- Do not recommend modernization only because the target Python version supports it.
- Evaluate modernization against migration cost, review cost, test impact, rollback complexity, team familiarity, tooling compatibility, and production risk.
- Treat web results as advisory and prefer official sources.
- Record uncertainty instead of guessing.
- Recommend tests before risky refactors.
- Use file, module, function, config, or test references for meaningful claims.
- State sampling boundaries for large repositories instead of implying exhaustive coverage.

## Composition And Exclusions

This skill composes with, but does not replace:

- `architecture-review` for business-domain boundaries, ownership, service boundaries, architectural layering, and refactor sequencing.
- `agent-legibility-review` for deeper review of future-agent readability, hidden rules, and repository-level modification risk.
- Framework-specific review skills such as `fastapi-review`, `sqlalchemy-review`, `pydantic-review`, or Django review.

Do not treat this as architecture review, deep agent-legibility review, framework review, security audit, performance deep dive, onboarding review, developer-experience review, or business-domain review unless explicitly requested.
