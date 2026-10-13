---
name: write-tests
description: Write missing tests for existing code, or raise a package's coverage toward 100%, with the right kind of test for each path. Use when the user asks for tests or more coverage, when `bun run test:coverage` names a file below 100%, or when code landed without tests.
argument-hint: <package or file>
---

# Write tests, raise coverage

The `test-writer` agent does this end to end; this is its procedure, for doing it by
hand or checking its work. `.claude/rules/tests.md` has which kind of test goes where.

1. **Measure.** `bun run --filter @repo/<name> coverage` for one package (unit and
   integration together, so the full Docker profile must fit), or `bun run test:coverage`
   for all of them; `bun run --cwd apps/ai coverage` for Python,
   `bun run --filter @repo/mobile coverage` for mobile. They take minutes: run them in
   the background. Note every uncovered line and branch.
2. **Pick the kind** for each gap:
   - pure logic: a unit test next to the file (`src/<file>.test.ts`);
   - anything touching Postgres, Valkey, email, auth, queues or HTTP: an integration test
     in the package's `test/` (apps name them `*.integration.test.ts`), against the real
     service, as the service's own role, data from `factories(db)` in `@repo/db/testing`.
     In apps/api, `test/harness.ts` (`startApi(<redis db>)`, `createSession`);
   - a user flow: a Playwright spec in `apps/web/e2e/` or `apps/mobile/e2e/`;
   - a component: a story with a `play` function in `packages/ui`.
3. **Write them.** Error branches too: the typed `AppError` codes, the early returns,
   another organization seeing nothing. Third parties through the local fakes, never
   `vi.mock` of Prisma, Redis, BullMQ or a provider. No fixed sleeps: wait for the
   condition. No `.skip`, `.only` or coverage pragma (the edit hook refuses them).
4. **Can't be tested automatically?** Write the test anyway, skipped with the reason
   (`it.skipIf(!process.env.<CREDENTIAL>)`), and add a row to "Not tested automatically"
   in `docs/testing.md` saying why and how to run it by hand.
5. **Reach 100%.** `bun run test:coverage` merges every suite and names each file below
   100%, with the lines, branches and functions no test reaches. A shared package counts
   what its callers' tests reach too. A line that truly can't be tested is either deleted
   or listed, with the reason, in "Coverage exceptions" in `docs/testing.md`.

## Done when

- The new tests pass on their own and in the package's suite.
- Every file you touched is at 100% in `bun run test:coverage`.
- `bun run lint`, `bun run check-types` pass; the verify skill for anything that ran
  integration tests.
