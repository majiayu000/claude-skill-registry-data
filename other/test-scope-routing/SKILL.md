---
name: test-scope-routing
description: Route validation by changed boundaries and risk, choosing the smallest sufficient checks for code, docs, UI, data, auth, sync, build, security, and release work. Use when deciding test commands, reducing unnecessary full-suite runs, auditing test layering, or documenting what was and was not verified.
---

# Test Scope Routing

Choose validation from the changed surface and risk. Keep the local feedback loop small, while reserving complete regression and release gates for merge, release, and high-risk boundaries.

For compact routing examples, read [references/usage-examples.md](references/usage-examples.md) when needed.

## Establish the project contract

Before selecting commands:

1. Read the applicable `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, and test-scope documentation.
2. Inspect `package.json`, Makefiles, task runners, test configuration, CI workflows, and release workflows.
3. Identify the repository, branch, worktrees, submodules, and uncommitted changes. Preserve changes that are outside the request.
4. Use project-defined commands and prerequisites. Do not invent a global command name or assume that `verify`, `fast`, or `full` has a standard meaning.
5. Check whether a command starts a database, browser, production connection, deployment, or other external state before running it.

Treat project documentation as the authority for exact commands and boundaries. This skill supplies the routing method, not project-specific command names.

## Write a small spec first

For behavior changes, record before implementation:

- in-scope behavior and explicit non-goals;
- user-observable acceptance conditions;
- affected code, UI, data, permission, offline, conflict, error, and compatibility boundaries;
- the smallest validation tier and any additional tiers;
- checks intentionally not run and why.

If a requirement is materially ambiguous, resolve the spec or decision first. For a behavior change, add a focused failing test when practical, then implement the smallest change.

## Select the smallest sufficient tier

Use semantic tiers. Projects may rename or combine them, but the responsibilities must remain distinct.

| Tier | Responsibility | Typical scope |
| --- | --- | --- |
| L0 static | Syntax, formatting, repository policy, static assets, and documentation constraints | Docs, copy, low-risk CSS, static configuration |
| L1 fast | Deterministic local logic and state behavior | Utilities, models, reducers, controllers, rule calculations |
| L2 targeted UI | User-visible rendering and interaction in the affected journey | Navigation, forms, settings, offline UI, PWA, accessibility-sensitive flows |
| L3 integration | External boundaries and data correctness | Database schema/RLS, functions, auth, sync, export, deletion, network errors |
| L4 full | Merge, release, or high-risk system boundary | Full build, security, dependency, complete E2E, database, release, and production checks |

Route by the union of touched boundaries:

- Documentation-only changes normally need L0 or no executable test when the project has no documentation checker.
- Pure logic changes need L1; use a related-test or explicit-test-file route when the project supports it.
- UI changes need L1 only when logic is affected, plus the smallest relevant L2 journey.
- Auth, synchronization, data lifecycle, schema, RLS, or server-function changes need the relevant L1 and L3 checks. Do not treat a UI test as permission or database evidence.
- Dependency, build, Service Worker, CSP, public-resource, or release changes need the project’s L4 checks.
- Merge, release, and explicitly high-risk changes require L4 even when lower tiers already passed.

Do not run every tier merely because a command is convenient. Do add tiers when the change crosses a boundary. If no targeted check exists, report the gap as unverified instead of hiding it behind an unrelated full suite.

## Inspect command composition

Before composing or recommending shortcuts:

- Expand each command and identify nested checks. Avoid running the same unit, coverage, build, or E2E suite twice.
- Do not assume `verify` means full regression. Confirm whether it excludes database, functions, E2E, or production probes.
- Prefer a test-file, project, tag, or related-test selector for local iteration when supported.
- Treat a command named `fast` as only a label; verify whether it runs all unit tests or only impacted tests.
- Keep local database checks local and follow the project’s migration/control-plane rules. Never substitute a production write for validation.
- Separate code failure, flaky behavior, missing dependency, unavailable Docker/browser, missing environment variables, and missing production URL. Environment blockage is not a passing test.
- Keep CI and release gates appropriately complete even when local iteration is targeted.

## Record evidence

In the task or PR, record:

1. Scope and acceptance conditions.
2. Selected tier(s) and the exact command(s) run.
3. Results, including counts and relevant artifacts when available.
4. Tiers not run and the reason.
5. Environment blockers, flaky tests, or unverified production behavior.
6. Remaining merge or release gates.

Do not describe a change as fully verified from an exit code, HTTP 200, empty output, pending CI check, or unit coverage percentage alone. State the actual boundary covered and the boundary that remains unverified.

## Keep the global and project layers separate

- Keep this skill framework-level: risk classification, tier responsibilities, command inspection, and evidence reporting.
- Keep project-specific facts in the project’s test-scope and contribution documents: exact commands, path mappings, thresholds, environments, browser/database prerequisites, and release exceptions.
- Keep one-off audits and handoffs as task records, not as the permanent global source of truth.
