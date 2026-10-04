---
name: testing-setup
description: Set up a complete testing framework in any codebase — survey the full project, install and configure the correct test runner, then produce and execute a prioritized test plan covering every architectural layer. Use this skill whenever the user wants to add testing to a project that has no tests, set up pytest or vitest or jest, create test infrastructure, scaffold a test suite, or says anything like "I have no tests", "add testing", "set up testing", "configure pytest", "configure vitest", "set up jest", "write initial tests", "create test scaffolding", or "make this testable". Also use when the user has a partially configured test setup that isn't working — the survey will detect what exists and fill in what's missing. This skill handles real codebases with hundreds of source files, not just tutorials.
---

# Testing Setup

Stand up a working test framework in an existing codebase and produce a test suite with meaningful coverage across the full architecture.

## Phase 1: Survey

Run the survey script to produce a JSON manifest:

```bash
python scripts/survey.py /path/to/project
```

The manifest contains: every source module in the project categorized by architectural layer (routes, services, models, utilities, components, hooks, middleware, config), plus language detection, build tool, package manager, existing test infrastructure, framework detection, and async usage.

Read the full manifest. The `testable_modules.summary` field tells you the shape of the codebase — how many modules exist per layer and per language. The `testable_modules.modules` field groups every module by layer with its exported functions, classes, or named exports.

If the project has both Python and JS/TS, both need test frameworks. They're independent — set up both.

## Phase 2: Framework Selection and Installation

The survey's `recommendation` field gives the test runner. The logic is deterministic:

- **Python** → pytest. Always. Add pytest-asyncio when async code exists. Add httpx when FastAPI exists (async test client). Add pytest-cov for coverage.
- **JS/TS with Vite** → vitest. It shares Vite's transform pipeline and plugin system — using Jest here means duplicating that entire config for no reason.
- **JS/TS without Vite** → jest. The standard choice with the widest ecosystem support.
- **React** → @testing-library/react + @testing-library/user-event + @testing-library/jest-dom, on top of whichever runner was selected. Plus jsdom or jest-environment-jsdom for DOM simulation.

**Before writing any configuration**, read the reference file for the selected runner:
- `references/pytest.md`
- `references/vitest.md`
- `references/jest.md`

These contain current configuration options sourced from framework documentation. Do not configure from memory.

Install using the package manager the survey detected. Respect existing dependency management — if the project uses poetry, use poetry. Don't introduce new package management.

## Phase 3: Configuration and Infrastructure

Create the test runner configuration and the supporting files tests depend on.

**Config file principles:**
- Only set options that differ from defaults. Don't dump every possible option.
- Match the project's patterns — TypeScript config for TS projects, path aliases that match tsconfig, coverage targeting the actual source directory.
- Set the correct environment — jsdom for DOM code, node for backends. Don't set jsdom for a pure API server.

**Infrastructure files:**
- **Python**: `tests/` directory with `__init__.py` and `tests/conftest.py` for shared fixtures.
- **JS/TS (Vitest)**: `test/setup.ts` for jest-dom matchers. If React, `test/utils.tsx` with a custom render wrapping the app's providers (inspect the entry point to find what providers exist).
- **JS/TS (Jest)**: Same as Vitest, plus `test/__mocks__/styleMock.js` and `test/__mocks__/fileMock.js` for asset mocking (Vitest handles this through Vite's pipeline).

## Phase 4: Test Plan

This is where the real work happens. The survey gave you a categorized module map. Now produce a test plan.

Create `test-plan.md` in the project root. This file is the source of truth for what needs tests, what has tests, and what's next. It persists across sessions.

### Priority ordering

Testing priority follows risk — where incorrect behavior causes the most damage:

**P0 — Services / Business Logic.** This is the core of what the application does. Services contain the most complex branching, the most business rules, the most potential for bugs that directly affect users or data. A wrong calculation in a billing service is worse than a wrong label on a button. Test every public method. Cover the branches — happy path, error cases, edge cases.

**P1 — Routes / API Endpoints.** These are integration boundaries — the contract between the application and its consumers. Test that endpoints accept correct input, reject bad input, return the right status codes and response shapes, and enforce auth. For FastAPI, use the async test client (httpx + ASGITransport). For Express, use supertest. For React with API routes, test the handler functions.

**P2 — Models / Data Layer.** Data integrity. Test that models validate correctly, that required fields are enforced, that relationships work, that serialization produces the expected output. For ORM models, test against a real (in-memory or test) database, not mocks — mock-heavy model tests catch nothing.

**P3 — Utilities.** Pure functions with no side effects. These are the easiest to test and the tests are the most stable. Every exported utility function should have tests covering normal input, boundary conditions, and error cases. High coverage here is cheap.

**P4 — Hooks** (React). Stateful logic extracted into hooks. Test with @testing-library/react's renderHook. Cover state transitions, cleanup, and edge cases.

**P5 — Components** (React/Vue/Svelte). Render the component, query by accessible roles and text (not CSS classes or test IDs), simulate user interactions with userEvent. Test behavior — what happens when the user clicks, types, submits — not implementation details.

**P6 — Middleware.** Request/response pipeline. Test that middleware transforms requests correctly, rejects unauthorized requests, handles errors.

**P7 — Config.** Low priority. Test only if config parsing is complex or has validation logic. A config file that loads environment variables rarely needs its own tests.

### Test plan format

```markdown
# Test Plan

## Summary
- Total modules: {from survey}
- By layer: {from survey}

## P0 — Services
| Module | Functions/Exports | Test File | Status |
|--------|------------------|-----------|--------|
| src/services/billing.py | calculate_total, apply_discount, ... | tests/test_billing.py | ❌ |

## P1 — Routes
...

## P2 — Models
...
```

Status values: ❌ not started, 🔧 in progress, ✅ complete.

Every module from the survey appears in the plan. Nothing is omitted.

## Phase 5: Execute

Work through the test plan by priority tier. For each module:

1. Read the source file to understand what it does.
2. Write tests that import and exercise the actual code — real inputs, real assertions on outputs. Not empty shells, not `assert True`, not mocks of the thing being tested.
3. Run the tests. Fix failures caused by import errors, missing deps, or config problems.
4. Update the test plan status.

**How much to write per module:** Every public function or exported symbol gets at least one test. Functions with branching logic (if/else, try/except, switch) get tests for each significant branch. This is not optional — a test file that covers 2 of 8 exported functions is incomplete.

**When a session can't finish the full plan:** That's expected for large codebases. Complete as many priority tiers as the session allows. The test plan file records progress. The next session reads the plan, sees what's done and what's next, and continues.

**When tests reveal problems in source code:** Note them. The purpose of the test suite is to test the code as it exists, not to refactor it. If a function is untestable because of tight coupling or hidden dependencies, write what you can and note the issue in the test plan.

## Phase 6: Verify

After each tier of tests is written:

```bash
# Python
pytest -v

# JS/TS
npm test -- --run   # vitest
npm test            # jest
```

All tests must pass before moving to the next tier. If tests fail, fix the test or the test infrastructure — not the source code (unless the source has an obvious bug the test revealed).

## What Not to Do

- **Don't install both Jest and Vitest.** Pick one based on the build tool.
- **Don't set `globals: true` in Vitest without adding `"types": ["vitest/globals"]` to tsconfig.** Editor type errors everywhere.
- **Don't use `ts-jest` with Next.js.** Use `next/jest` — it handles SWC transforms. Adding ts-jest breaks it.
- **Don't create `jest.config.js` when the project has `vite.config.ts`.** Add the `test` block to the Vite config, or create `vitest.config.ts`.
- **Don't add pytest-asyncio if there's no async code.** The survey checks.
- **Don't mix INI-style and TOML-style pytest config.** Use `[tool.pytest]` for new projects.
- **Don't write tests that import nothing from the project.** Every test file tests real code.
- **Don't mock the thing you're testing.** Mock its dependencies if needed, never the subject.
- **Don't stop at one tier.** The skill's job is to work through the full plan, not write a token number of test files and declare success.
