---
name: unit-testing-js-ts-react-nextjs
description: Unit tests that catch real regressions, not just coverage, for software developers and QA engineers. Writes and reviews behavior-first tests for JavaScript/TypeScript, React and Next.js with Jest, Vitest and React Testing Library. Use when writing tests for a module, component, hook, route handler or server action; writing tests for a commit, branch, PR or diff; reviewing or auditing existing tests (brittle, over-mocked, snapshot-heavy, testing implementation details, flaky); or when asked to raise coverage or find missing test cases.
---

# Unit testing: JavaScript, TypeScript, React and Next.js

A test earns its place when it goes **red** because a behavior someone relies on broke, and stays green when only the implementation changed. Coverage is a by-product of testing behaviors, never the goal: a line can be executed by a test that checks nothing.

The **user** of a unit is whoever consumes it, and tests act the way that user does:

- a React component's user is a person: they see text, roles and labels, they click and type.
- a module's user is the calling code: it passes arguments and reads return values or thrown errors.
- a route handler's or server action's user is an HTTP client or a form: it sends a request and reads the response.

## The four pillars

Every test is judged on these (Khorikov, *Unit Testing Principles, Practices, and Patterns*):

1. **Protection against regressions**: it goes red when the behavior breaks.
2. **Resistance to refactoring**: it stays green when behavior is unchanged. A test that breaks on a rename or a `useState` → `useReducer` swap is a false alarm, and false alarms teach people to ignore red.
3. **Fast feedback**: milliseconds, no real network, no real waiting.
4. **Maintainability**: a reader understands it without opening the source.

Pillars 1 and 2 are the non-negotiable pair. A test weak on either is rewritten, not kept for coverage.

## Rules for every test

These apply both when writing and when reviewing.

- **Go through the public interface.** Call the exported function. Render the component and drive it with `user-event`. Call the route handler with a `Request`. Private helpers are tested through the public behavior that uses them.
- **Find elements the way users do**, in Testing Library's priority order: `getByRole` with its accessible `name` (`getByRole('button', { name: 'Subscribe' })`), then `getByLabelText` for form fields, then `getByText` for non-interactive content. `getByTestId` is the last resort, for elements with no role, label or text, and `container.querySelector` stays out. An existing `data-testid` in the source is no reason to use it when a role or label works. When an element can't be found by role or label, that is an accessibility gap: report it, and offer the markup fix (a `<label>`, a real `<button>`, an `aria-label`) rather than adding a test id.
- **Assert observable outcomes**: return values, thrown errors, what is rendered, the HTTP status and body, and calls that leave the system (payment API, analytics, email, `router.push`). Internal state, which of your own modules got called, and the order of internal calls are implementation details.
- **Mock only at the boundary**: network (MSW or a `fetch` stub), the clock, randomness, third-party SDKs, the database client, and the framework runtime (`next/navigation`, `next/headers`, `next/cache`). Your own modules stay real, so a test covers the unit together with its in-process collaborators.
- **The name is the spec.** `describe` names the unit; each test is a sentence about one behavior under one condition: `it('shows an error when the email is already registered')`. A failing test name alone should tell someone what broke.
- **Arrange / Act / Assert, one behavior per test.** Several assertions about the same outcome are fine.
- **Expected values are literals written by hand.** `expect(total).toBe(1495)`, not a value computed with the same formula as the source. Variations go in an `it.each` table.
- **Deterministic**: fake timers and a fixed system time for anything time-based, fixed data, no real sleeps, each test independent of the others' order and leftovers.
- **DAMP over DRY**: what matters to a test is visible in that test. Small factories (`buildOrder({ status: 'paid' })`) hide the irrelevant fields.

Stack details, loaded when the branch needs them:

- React components, hooks, forms, async UI, providers, MSW: [references/react-testing-library.md](references/react-testing-library.md)
- Next.js server and client components, route handlers, server actions, middleware/proxy, `next/*` mocks: [references/nextjs.md](references/nextjs.md)
- Jest vs Vitest APIs, module mocking, fake timers, environments, mutation testing: [references/jest-vitest.md](references/jest-vitest.md)
- Test smells with IDs, how to spot them, and their fixes: [references/anti-patterns.md](references/anti-patterns.md)

## Step 1: Read the project's setup

Look before writing anything; the project's conventions win over the examples in this skill.

- Runner: `vitest` or `jest` in `package.json`, and its config file (`vitest.config.*`, `jest.config.*`, `next/jest`).
- Setup files (`setupFiles`, `setupFilesAfterEnv`): is `@testing-library/jest-dom` loaded, is MSW started, is `cleanup` registered.
- A custom render helper (`test-utils.tsx`, `renderWithProviders`) and how existing tests use it.
- Where tests live (`__tests__/` or next to the source), file naming (`.test.ts` or `.spec.ts`), and path aliases.

If no test runner is set up, tell the user and propose the setup from the relevant reference. Installing packages is the user's call.

Done when you know the command that runs a single test file once (not in watch mode), where a new test file goes, and which render helper to use.

## Step 2: Pick the branch

- Write tests for a file, component or feature: **Writing tests**.
- Write tests for a commit, branch, PR or uncommitted changes: **Scoping a diff**, then **Writing tests**.
- Review, audit or improve existing tests: **Reviewing tests**.
- "Increase coverage": **Writing tests**. Use the coverage report to find untested *behaviors* and report behaviors covered, not percentages.

## Scoping a diff

1. Get the change:
   - a commit: `git show <sha>`
   - a branch: `git diff $(git merge-base HEAD origin/main)...HEAD` (use the repo's default branch)
   - a PR: `gh pr diff <number>`
   - uncommitted work: `git diff HEAD`, plus `git ls-files --others --exclude-standard` for new files
2. For each changed source file, list its **behavior changes**: new behavior, changed behavior, removed behavior, bug fixed. A pure refactor has none; the existing tests should still pass unchanged, which is itself the check.
3. For each behavior change, search the existing tests for the unit and mark it **covered**, **asserts the old behavior** (update that test), or **missing**.
4. A bug fix gets a **regression test**: one that would have been red on the parent commit. Say which input reproduces the old bug.
5. Write the missing and updated tests with **Writing tests**, scoped to these behaviors.

Done when every behavior change maps to a test (new, updated or already existing) or to a stated reason it isn't unit-testable.

## Writing tests

1. **Build the behavior inventory** from the outside first: the signature and types, props, docs, the ticket or spec, and how callers use the unit. Then read the implementation to find branches you missed, and name each by its outcome, not its code path. Work through:
   - happy path, written for UI as the user's steps ("types email, submits, lands on /welcome")
   - input boundaries: empty, zero, one, many, the limit and one past it, `null`/`undefined`, malformed input, whitespace
   - failures: rejected promises, network errors, 4xx and 5xx responses, thrown errors
   - state over time: loading → success or error, double submit, retry after error, stale results
   - who may do what: roles, ownership, feature flags
   - time: expiry, "now", time zones
   - what users with assistive tech get: accessible names, `role="alert"`, disabled state, focus
   
   When the code does something that looks wrong, keep it out of the expected values. Write the test for the behavior you believe is intended and report the suspected bug to the user, or ask which is intended.
2. **Pick the level** for each behavior: pure logic → call the function, `it.each` for tables; component → RTL render plus `user-event`; hook → through a component that uses it, or `renderHook` for a reusable hook; route handler or server action → call it with a `Request` or `FormData` and mock the boundaries; async Server Component → see [references/nextjs.md](references/nextjs.md).
3. **Write the tests** following the rules above.
4. **Run the file** once. A failing test means a wrong test or a real bug. A real bug is reported to the user with the failing test; the source changes only if they ask.
5. **Sabotage check** each important behavior (at least three, or all of them in a small unit): make the smallest source edit that breaks it (flip a condition, `<` → `<=`, drop a call, return early), run the file, and confirm it goes **red** with a failure message that names the problem. Then restore the edit exactly and confirm the file is green again and `git diff` on the source shows nothing of yours. A test that stays green under sabotage protects nothing: fix it or delete it. If the project already has Stryker configured, run it on the file instead and report the surviving mutants (see [references/jest-vitest.md](references/jest-vitest.md)).
6. **Refactor check** each test: would it survive renaming an internal function, splitting the component in two, swapping state management, or changing a CSS class? Rewrite the ones that would not.

Done when every inventory behavior has a test or a stated reason for skipping it, the file is green, every sabotaged behavior went red, and every source file is back to its original content.

### Report

```
## Tests for <unit or diff>

Behaviors (N tested, M skipped):
- ✓ shows an error when the email is already registered
- ✓ ...
- – skipped: <behavior>: <reason, e.g. async Server Component → E2E>

Sabotage check: <edit> → red (<test name>); ... All source files restored.
Suspected bugs: <input> → <actual> (expected <x>). Not fixed.
Run: <command>
```

## Reviewing tests

Scope is the test files the user named, the tests for the files in a diff, or a folder.

1. Read each test file and the unit it tests.
2. Build the unit's behavior inventory (Writing tests, step 1) and mark each behavior **covered**, **covered weakly** (the test would stay green if it broke), or **missing**.
3. Check every test against the rules and the smell catalog in [references/anti-patterns.md](references/anti-patterns.md).
4. For the one or two most suspicious tests, run a sabotage check. A test that stays green under sabotage is the strongest evidence a review can give.
5. Write the report below. Offer to apply the fixes; when applying, follow Writing tests steps 3 to 6.

Done when every test in scope has been read and is either clean or has a finding, and every inventory behavior is marked.

### Report

```
## Test review: <scope>

Verdict: <one sentence: would these tests catch a real regression?>

| Pillar | Rating | Evidence |
| --- | --- | --- |
| Protection against regressions | strong / weak / none | ... |
| Resistance to refactoring | ... | ... |
| Fast feedback | ... | ... |
| Maintainability | ... | ... |

Findings (worst first):
- HIGH `file.test.tsx:42` [no-assertion] "handles server failure" asserts nothing; it passes even if the error message is removed. Fix: assert the alert text.
- ...

Behaviors:
- covered: ...
- covered weakly: ...
- missing: ...

Suspected bugs in the source: ...

Rewrite of the worst test:
<before → after code>
```

Severity: **HIGH** gives false confidence (it cannot go red, or it goes red on a refactor). **MEDIUM** is flaky, slow, or misleading. **LOW** is readability.
