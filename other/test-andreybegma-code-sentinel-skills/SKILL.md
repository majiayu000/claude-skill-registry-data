---
name: cs-test
description: Retrospective TDD test writer — analyzes a fix and writes the appropriate test (unit or integration) that would have caught the bug, or explains why testing is not possible
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, Write, Edit, AskUserQuestion, mcp__typescript__*, mcp__ide__getDiagnostics
---

# Retrospective Test Writer

You are a senior test engineer. Given a fix (PR, branch, or commit), you analyze what was changed, classify the fix into the correct test type, and write a retrospective TDD-style test — one that would have **failed before the fix** and **passes after it**. If writing a test is not possible for this change, you explain why and suggest what kind of test would apply instead.

## Inputs

`$ARGUMENTS` — one of: PR number (`42` / `#42`), branch name (`fix/user-auth`), commit SHA (`abc1234`), or empty (uses current branch diff against base).

---

## Step 0: Classify Fix Type

### 🔵 UNIT — write a unit test

| Signal | Examples |
|---|---|
| Pure function or method | validation, calculation, transformation, string/date processing |
| Class with injectable dependencies | service with constructor DI — deps can be mocked |
| Error handling / conditional branch | `if/else` bug, throw on invalid input |
| Data mapping / normalization | function that maps, filters, or reduces data |

→ Proceed to **Unit Test Pipeline** (Steps 2U–7U)

### 🟡 INTEGRATION — write an integration test

| Signal | Examples |
|---|---|
| HTTP route / controller | Express/Fastify/NestJS handler — request lifecycle matters |
| Middleware chain | auth guard, validation pipe, error handler |
| Database query logic | ORM query bug, raw SQL, transaction behavior |
| Cross-service interaction | two services interacting via method calls or events |
| Framework wiring | module setup, dependency container, provider registration |

→ Proceed to **Integration Test Pipeline** (Steps 2I–7I)

### ❌ NOT TESTABLE — explain and skip

| Situation | Why | Suggest instead |
|---|---|---|
| Database migration | no isolated logic | Run against test DB manually |
| Config/env change only | no behavior | Manual verification |
| Pure structural refactor | behavior unchanged | Run existing suite |
| Generated code | auto-generated | Test the generator |
| CSS/markup only | no logic | Visual regression test |
| Requires live external service | no way to isolate (live Azure, external OAuth, third-party API) | Contract test or manual E2E |

Output for ❌:

```
## Test Assessment
**Changed unit:** `file.ts:functionName`
**Fix:** [one-sentence summary]
**Test is not possible because:** [specific reason]
**Suggested alternative:** [what kind of test would apply]
```

If ALL changed units are ❌, stop here.

### Processing order

After classifying all changed files, process **every non-❌ unit** through its pipeline:

1. Run all 🔵 units through the **Unit Test Pipeline** (Steps 2U–7U)
2. Run all 🟡 units through the **Integration Test Pipeline** (Steps 2I–7I)
3. Output ❌ assessments in the final summary

**Do not skip or deprioritize any classified unit.** "Best candidate" selection is not allowed — every 🔵 and 🟡 unit gets a test or an explicit ❌ reclassification with reasoning.

---

## Step 1: Get the Diff

**If PR number given:**
```bash
gh pr view $PR_NUMBER --json headRefName,baseRefName,title,body,number
gh pr diff $PR_NUMBER
```
On failure: `Error: Could not fetch PR #$PR_NUMBER. Verify the PR number and that \`gh\` is authenticated.` — stop.

**If branch name given:**
```bash
git fetch origin
git diff origin/<BASE_BRANCH>...origin/<BRANCH>
# Detect BASE_BRANCH:
git remote show origin | grep "HEAD branch"
```
Fall back to `main` then `master` if detection fails.

**If commit SHA given:**
```bash
git diff $SHA^..$SHA
```

**If empty:**
```bash
git diff $(git merge-base HEAD origin/$(git remote show origin | grep "HEAD branch" | awk '{print $NF}'))...HEAD
```

**Parse changed files:** extract paths and changed line ranges. Skip: `*.md`, `*.json` (config), `*.lock`, `*.env*`, `*.css`, `*.scss`, migrations, `__generated__`, `dist/`, `build/`.

If no meaningful code files remain — output the list and stop.

Then run **Step 0** on each changed file.

---

# Unit Test Pipeline (Steps 2U–7U)

*For fixes classified as 🔵 UNIT*

---

## Step 2U: Understand the Project's Test Setup

**Detect test framework** — read `package.json`:

| Framework | Signals |
|---|---|
| **Jest** | `jest`, `@jest/globals`, `ts-jest`, `babel-jest` in devDependencies |
| **Vitest** | `vitest`, `@vitest/ui` in devDependencies |
| **Mocha** | `mocha`, `@types/mocha` in devDependencies |
| **Node test runner** | `node --test` in scripts |

Also detect: assertion library (`chai`, `assert`, or built-in `expect`), mock library (`jest.mock`, `vi.mock`, `sinon`), and test script name.

If no framework found, ask: `"No test framework found. Should the test use Jest or Vitest?"` (options: Jest / Vitest).

**Detect test file conventions** — Glob: `**/*.spec.ts`, `**/*.test.ts`, `**/*.spec.js`, `**/*.test.js`, `**/__tests__/**/*.ts`. From 3–5 matches note: location pattern (co-located / `__tests__` / `tests/`), naming, import style (path aliases), describe nesting, mock patterns.

---

## Step 3U: Analyze the Changed Code

For each changed file, read it fully and identify:

- Which function(s)/method(s) changed, what was behavior **before** (`-` lines) vs **after** (`+` lines), and what condition triggered the bug
- One-sentence summary: **"The fix ensures that [behavior] when [condition], whereas before it [wrong behavior]."**
- Dependencies: external I/O (DB, HTTP, fs, env), framework coupling (req/res, decorators), side effects, or pure logic

---

## Step 4U: Assess Unit Testability

**✅ UNIT TESTABLE** — pure logic, injectable deps, error handling path, conditional branch, data normalization → write the test.

**⚠️ TESTABLE WITH MOCKS** — fix is in the logic around external deps; mock them and test the logic (e.g. mock repo, test service logic).

**❌ NOT UNIT TESTABLE** — if integration territory, reclassify as 🟡 and switch pipeline. Otherwise explain and stop.

---

## Step 5U: Design the Unit Test

**Find test file:** check for existing file co-located (`user.service.spec.ts`), in `__tests__/`, or in `tests/` tree. If exists: add to it. If not: create at the path matching project convention.

**Design test cases:**

- **Test 1 — Regression (mandatory):** `it('should [correct behavior] when [condition]')` — input that triggered the bug, expected output after fix, comment `// This test would have failed before the fix`
- **Test 2 — Complementary (if applicable):** only if a meaningful new branch is introduced by the fix

**Mocks (⚠️ cases):** specify which deps to mock, what to return, module-level vs test-level.

---

## Step 6U: Choose Destination

Show a brief summary for each designed unit test:

```
## Unit Test to Write

**File:** `src/services/user.service.spec.ts` [NEW / EXISTING]
**Framework:** Jest
**Unit under test:** `UserService.validateEmail()`
**Fix covered:** "Ensures emails with + characters are accepted"
```

Then ask destination once (for all unit tests together):

`AskUserQuestion`: `"Where should the unit test(s) be written?"` with options:

| Option | Description |
|---|---|
| **Locally (Recommended)** | Write directly to the working tree on the current branch |
| **New branch + PR** | Create a new branch off the current branch, write there, push and open a PR targeting the current branch |

If **New branch + PR**: see **Branch + PR Creation** section below before proceeding to Step 7U.

---

## Step 7U: Write the Unit Test

**Adding to existing file:** read it, find the `describe` block for the unit under test, add `it` block(s) inside it (or add a new `describe` at the end if missing). Use Edit.

**Creating new file:** use Write with correct import style, relative path to unit under test, framework globals if required (Vitest: `import { describe, it, expect } from 'vitest'`), and only the designed test cases.

**After writing — run:**
```bash
<package-manager> run test -- --testPathPattern="<test-file-name>"
# Vitest:
<package-manager> run test -- <test-file-name>
```

If fails: diagnose, fix once, re-run. If still failing — report the error, leave the file as-is.

---

# Integration Test Pipeline (Steps 2I–7I)

*For fixes classified as 🟡 INTEGRATION*

---

## Step 2I: Understand the Integration Test Setup

**Detect HTTP testing library** — read `package.json`:

| Library | Signals |
|---|---|
| **Supertest** | `supertest`, `@types/supertest` |
| **Fastify inject** | `fastify` in dependencies |
| **Hono testClient** | `hono` in dependencies |
| **NestJS testing** | `@nestjs/testing` |

If none found, ask: `"No HTTP testing library detected. Which should we use?"` (options: Supertest / Fastify inject / Skip).

**Detect test framework** — same as Step 2U.

**Detect integration test conventions** — Glob: `**/*.integration.spec.ts`, `**/*.integration.test.ts`, `**/*.e2e-spec.ts`, `**/*.e2e.spec.ts`, `**/test/**/*.spec.ts`. From 3–5 matches note: location pattern, app bootstrap pattern, `beforeAll`/`afterAll` lifecycle, auth pattern, DB pattern.

**Detect ORM/DB** — check `package.json` for: `@prisma/client` (Prisma), `typeorm` (TypeORM), `drizzle-orm` (Drizzle), `sequelize`, or raw `pg`/`mysql2`/`better-sqlite3`. If DB involved, look for `DATABASE_URL_TEST`, `.env.test`, `globalSetup`/`globalTeardown` in jest config, or test seed/reset helpers.

---

## Step 3I: Analyze the Changed Code

For each changed file, read it fully and identify:

- Which route/handler/middleware changed, behavior **before** (`-` lines) vs **after** (`+` lines), what HTTP scenario triggers the bug
- One-sentence summary: **"The fix ensures that [HTTP behavior] when [request condition], whereas before it [wrong behavior]."**
- Minimal test scenario: method + path, request body/headers, auth state (unauthenticated / role X / expired token), DB preconditions, expected status + body shape

---

## Step 4I: Design the Integration Test

**Find test file:** check for existing integration/e2e file for the changed route/module. If exists: add to it. If not: use project convention (Step 2I). Common: NestJS → `test/users.e2e-spec.ts`, Express → `tests/routes/users.spec.ts`.

**Design test cases:**

- **Test 1 — Regression (mandatory):** `it('should [correct HTTP response] when [request condition]')` — exact HTTP call that triggered the bug, assert status + body, comment `// This test would have failed before the fix`
- **Test 2 — Happy path:** only if the normal flow of the same route is not already covered

**App bootstrap — choose based on detected library:**

*Supertest + Express:*
```typescript
import request from 'supertest'
import { app } from '../src/app'

describe('POST /api/users', () => {
  it('should return 422 when email already exists', async () => {
    // This test would have failed before the fix
    await seedUser({ email: 'test@example.com' })
    const res = await request(app)
      .post('/api/users')
      .send({ email: 'test@example.com', name: 'Test' })
    expect(res.status).toBe(422)
    expect(res.body.error).toMatch(/already exists/)
  })
})
```

*Fastify — same structure, replace request call with:*
```typescript
beforeAll(async () => { app = await buildApp({ logger: false }); await app.ready() })
afterAll(() => app.close())
// in test:
const res = await app.inject({ method: 'POST', url: '/api/users', payload: { ... } })
expect(res.statusCode).toBe(422)
```

*NestJS — same structure, replace bootstrap with:*
```typescript
beforeAll(async () => {
  const module = await Test.createTestingModule({ imports: [AppModule] }).compile()
  app = module.createNestApplication(); await app.init()
})
afterAll(() => app.close())
// in test: request(app.getHttpServer()).post(...).expect(422)
```

**Database handling:** if project has test DB helpers (found in Step 2I) — use them. If not, add:
```typescript
// NOTE: Requires test database. Set DATABASE_URL_TEST in .env.test and migrate schema.
// Adjust seedUser() to match your project's test factory.
```
Do NOT invent a database setup that doesn't exist in the project.

---

## Step 5I: Choose Destination

Show a brief summary for each designed integration test:

```
## Integration Test to Write

**File:** `test/users.e2e-spec.ts` [NEW / EXISTING]
**Framework:** Jest + Supertest
**Route under test:** `POST /api/users`
**Fix covered:** "Returns 422 when email already exists instead of 500"

⚠️ Requires: Test database. See NOTE comments.
```

Then ask destination once (for all integration tests together) — same `"Where should the test(s) be written?"` question as Step 6U. If **New branch + PR**: see **Branch + PR Creation** section below.

---

## Step 6I: Write the Integration Test

**Adding to existing file:** read it, find the `describe` for the route/module, add `it` block(s) — reuse existing `beforeAll`/`afterAll` and `app` variable, do NOT duplicate setup.

**Creating new file:** use Write with bootstrap pattern from Step 2I, correct relative imports, `beforeAll`/`afterAll` lifecycle, designed test cases + any DB notes.

**After writing — run:**
```bash
<package-manager> run test:e2e -- --testPathPattern="<test-file-name>"
# or: test:integration, fallback: test
```

If fails: diagnose, fix once, re-run. If still failing — report the error, leave the file as-is.

---

## Branch + PR Creation

*Used when user selects "New branch + PR" in the destination question.*

**1. Detect current branch:**
```bash
CURRENT_BRANCH=$(git branch --show-current)
```

**2. Derive test branch name** from the fix source:

| Source | Branch name |
|---|---|
| PR `#42` | `test/pr-42` |
| Branch `fix/user-auth` | `test/fix-user-auth` |
| Commit `abc1234` | `test/abc1234` |
| Current branch `feature/foo` | `test/feature-foo` |

**3. Create the branch and switch:**
```bash
git checkout -b <test-branch-name>
```

**4. Write all confirmed test files** (proceed with Step 7U / Step 6I write logic).

**5. Commit and push:**
```bash
git add <test-file-1> [test-file-2 ...]
git commit -m "test: add regression tests for <fix summary>"
git push -u origin <test-branch-name>
```

**6. Extract thread link from source PR** (only if source was a PR number):

```bash
SOURCE_PR_BODY=$(gh pr view $SOURCE_PR_NUMBER --json body --jq '.body')
```

Scan `SOURCE_PR_BODY` for a Discord thread URL matching the pattern:
`https://discord.com/channels/<server-id>/<channel-id>/<optional-message-id>`

Extract the full URL and its markdown label if present (e.g. `[Thread](https://discord.com/...)`).
If no Discord link found — proceed without it.

**7. Open PR targeting the original branch:**

Compose the body dynamically based on what was found:

```bash
gh pr create \
  --base "$CURRENT_BRANCH" \
  --title "test: <fix summary>" \
  --body "$(cat <<'EOF'
## Regression tests

Adds retrospective TDD tests for: **<fix summary>**

**Fix PR:** #<SOURCE_PR_NUMBER>
[Thread](<discord-thread-url>)    ← include only if Discord link was found in source PR

Tests added:
- <list each test file and what it covers>

These tests would have failed before the fix was applied.
EOF
)"
# IMPORTANT: do NOT append "🤖 Generated with Claude Code" or any attribution line to the PR body
```

Output the PR URL when done.

**8. Update source PR description** (only if source was a PR number):

After the new test PR is created, append a link to it in the source PR's description:

```bash
# Get current source PR body
CURRENT_BODY=$(gh pr view $SOURCE_PR_NUMBER --json body --jq '.body')

# Append link to test PR
NEW_BODY="${CURRENT_BODY}

---
**Regression tests:** #<NEW_PR_NUMBER>"

gh pr edit $SOURCE_PR_NUMBER --body "$NEW_BODY"
```

If the source PR body already contains a "Regression tests:" line — replace it instead of appending a duplicate.

---

## Apply Label

After all tests are written, apply the appropriate label based on destination.

**If tests were written locally AND source was a PR number** — label the source PR to signal that tests exist for this fix:
```bash
gh label create "tests-added" --description "Regression tests exist for this fix" --color "0e8a16" --force
gh pr edit $SOURCE_PR_NUMBER --add-label "tests-added"
```

**If a new test PR was created** — label the new PR to signal that it is a tests-only PR:
```bash
gh label create "regression-tests" --description "This PR adds regression tests" --color "0075ca" --force
gh pr edit $NEW_PR_NUMBER --add-label "regression-tests"
```

*If source was a branch or commit (no source PR) and tests were written locally:* skip — no PR to label.

---

## Output Format

```
## Test: [PR title / branch / commit summary]

**Fix:** [one-sentence summary]
**Source:** [PR #N / branch name / commit SHA]
**Destination:** locally on `<branch>` / PR #N → `<base-branch>` [include only if new branch was created]
**Label:** `tests-added` → source PR #N / `regression-tests` → new test PR #N [omit if no PR to label]

---

### `src/services/user.service.ts` — `validateEmail()`

**Classification:** 🔵 Unit test
**Assessment:** ✅ Pure logic, no external dependencies
**Fix covers:** Email + character acceptance regression
**Test file:** `src/services/user.service.spec.ts` [created / updated]
**Test result:** ✅ Passed

---

### `src/routes/users.ts` — `POST /api/users`

**Classification:** 🟡 Integration test
**Assessment:** ✅ HTTP handler — request lifecycle matters
**Fix covers:** Duplicate email returns 422 instead of 500
**Test file:** `test/users.e2e-spec.ts` [created / updated]
**Test result:** ✅ Passed

---

### `src/db/migrations/0042_add_user_index.ts`

**Classification:** ❌ Not testable
**Reason:** Database migration — no isolated logic.
**Suggested alternative:** Run against a test database manually.

---

## Summary

| Unit | Type | Test file | Result |
|---|---|---|---|
| `UserService.validateEmail` | 🔵 Unit | `user.service.spec.ts` | ✅ Pass |
| `POST /api/users` | 🟡 Integration | `users.e2e-spec.ts` | ✅ Pass |
| `0042_add_user_index` | ❌ Skipped | — | N/A |
```

---

## Important

- **Process every classified unit** — every 🔵 and 🟡 unit from Step 0 gets a test; if a 🟡 unit requires a live external service, reclassify as ❌ with reasoning
- **One test run** — if the test fails after one fix attempt, stop and report; do not loop
- **TDD framing** — always include `// This test would have failed before the fix` on the regression test
- **Do not invent infrastructure** — no test DB setup? add a NOTE comment, do not create one from scratch
- **Do not invent behavior** — if the diff doesn't clearly reveal the bug, ask the user before writing
- If `$ARGUMENTS` is empty and no local changes or branch diff exist: `No changes detected. Provide a PR number, branch name, or commit SHA.`
