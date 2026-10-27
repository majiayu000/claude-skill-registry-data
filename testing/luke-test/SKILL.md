---
name: luke-test
description: >
  QA control plane for the Luke monorepo. Decides what deterministic evidence
  is sufficient to consider a change correct, across lint, typecheck, Node
  unit, real-browser component, Postgres integration and Playwright E2E — then
  assesses, writes or executes that evidence. Reports PASS / FAIL / SKIPPED /
  QA GAP with residual risk rather than a bare green tick.
  Use after implementing a feature or fixing a bug, before committing.
  Modes: /luke-test (assess, read-only) | write | verify.
  Scoping: default = diff vs merge-base. /luke-test write apps/api | --since <ref>
argument-hint: '[assess|write|verify] [path] [--since <ref>]'
---

# Luke QA Control Plane

The question this skill answers is:

> **What deterministic evidence is sufficient to consider this change correct?**

Not "which tests should I write". Writing tests is one of its three modes, and
usually not the first one.

## Modes

| Mode                | Does                                                          | Writes |
| ------------------- | ------------------------------------------------------------- | ------ |
| _(empty)_ / `assess` | scope → risk → required evidence → what is missing            | **no** |
| `write`             | create or update tests for the scope                          | tests only |
| `verify`            | run the evidence the scope requires, and report it honestly   | **no** |

**Invocation arguments:** $ARGUMENTS

The first token of the bound value above is the mode: an empty value or
`assess` selects assess; `write` and `verify` keep the meanings in the table.
The remainder is the scope selector, resolved per `audit-protocol.md` §1 — an
explicit form wins, and an empty selector derives the default diff vs
merge-base.

**Any other first token fails closed.** Matching is exact and case-sensitive,
and the scope always follows the mode (`/luke-test assess apps/api`, never
`/luke-test apps/api`). Print

```
luke-test: usage — [assess|write|verify] [<scope>]
```

and stop, having read nothing and written nothing.

**Bare `/luke-test` is `assess`.** The default QA action is to decide what
proof is required, not to mutate the repository. `write` is one word away and
the assessment names the command.

**Read `.claude/skills/luke-shared/audit-protocol.md` first** and apply the
sections its applicability table assigns to `/luke-test`: §1 scoping
(default: diff vs merge-base) and §7 concurrent sessions — in `write` mode you
are a skill that writes files, so §7.2 applies. Read `lessons.md` per §4 too —
the Always row and the rows naming `luke-test` — as guidance on how tests here
fail, not as a checklist to promote into rules.

**Read `.claude/skills/luke-test/references/evidence-matrix.md`** before
selecting evidence in any mode. It holds the tiers, the change→evidence table,
and the result model. Do not restate them here.

## Ownership

`.claude/skills/luke-shared/governance-map.md`. This skill owns **verification
adequacy**: which evidence a change needs, whether it exists, and what running
it proved.

- It does **not** own application code. If the code under test has a bug, flag
  it and write the test that exposes it, marked `.fails` or `.todo` with the
  reason. Changing behavior is `/luke-fix`'s job and the user's decision.
- It does **not** own the test toolchain's versions or compatibility — that is
  `/luke-deps`. This skill owns strategy; that one owns whether the runner
  still works after a bump.
- `/luke-bugs` and `/luke-security` may **prescribe** the regression evidence a
  finding requires. Implementing and executing it is this skill's job.
- `/luke-full` may only ever call `assess`.

## The result model in one line

PASS · FAIL · SKIPPED *with reason* · **QA GAP** · residual risk LOW/MEDIUM/HIGH.

A required tier that does not exist is a **QA GAP**, never an implicit PASS.
`PASS WITH QA GAP` is a legitimate verdict; `PASS` with a required tier missing
is not. Definitions and the risk scale: the evidence matrix, §3.

---

## 1. Tier map

Tiers, membership and the change→evidence table live in
`.claude/skills/luke-test/references/evidence-matrix.md`. Read it there; this
section covers only what writing a test in this repo requires.

Picking the wrong tier is the costliest mistake: a unit test that touches the
database ends up in the wrong project and fails in CI.

Membership is **the file name and the project config**, never a list. There
used to be a hand-written list (`test/integration-specs.ts` <!-- skill-check-ignore -->),
removed: a list has an asymmetric failure mode — a missing entry is noticed
right away, but a stale entry after a rename isn't, and a suite can silently
drop out of the run.

Choice rule for `apps/api`: **does it need a real Prisma table?**

- No → unit. Mock `ctx.prisma` with only the methods used.
- Yes → integration: name the file `<name>.integration.spec.ts` and you're in.

Commands:

```bash
pnpm test                          # unit
pnpm test:integration:local        # integration: starts the container and passes TEST_DATABASE_URL
pnpm --filter @luke/web test:e2e   # smoke, with the app stack running
```

Without `TEST_DATABASE_URL` the suite **fails**, it doesn't skip: that's
intentional — a green job with zero tests run is worse than a red job.
Values and explicit shape live in `docker-compose.test.yml`.

**Procedure coverage**: the integration suite has a gate that checks which
tRPC procedures are _actually invoked_ (`test/procedure-coverage.ts`). If you
add a procedure without a test, `pnpm test:integration` fails and prints the
entry to paste in. Don't work around it by declaring it uncovered without
reason: the gate rejects placeholder reasons.

---

## 2. Existing helpers — use these, don't reinvent them

**`apps/api/test/helpers.ts` is the single barrel: its export list _is_ the
test API. Read it there.**

This section used to list the signatures one by one and drifted: it cited
`hasTestDatabase()` months after its removal and `teardownTestDb(prisma)` <!-- skill-check-ignore -->
after the parameter had disappeared. It duplicated the codebase, and a
duplicate always rots. The fix isn't a fresher duplicate.

The modules under `test/helpers/` (`database`, `logger`, `testContext`,
`storageTestHelper`) are all re-exported from the barrel — partly because
that re-export is what makes identically-named exports collide at compile
time. If you add an export to a helper module, add it to the barrel too.

Three rules that the code itself doesn't make obvious:

1. **Never `new PrismaClient()` directly**: in Prisma 7 the constructor
   doesn't accept a URL, it needs the adapter — and a client without an
   adapter points at the development database.
2. **Missing `TEST_DATABASE_URL` = the suite fails, never skips.**
   `describe.skipIf` on database availability is forbidden: it reports the
   job green with zero tests run, which is worse than a red job. That's why
   `hasTestDatabase()` was removed instead of fixed. <!-- skill-check-ignore -->
3. **No database teardown hook.** Disconnection happens once per file, in
   the global setup (`test/setup.ts`), and isolation is by truncation.
   `teardownTestDb()` was the no-op that outlived its own callers <!-- skill-check-ignore -->: it
   was removed along with them. Don't reintroduce it.

---

## 3. Writing rules

All of these come from real breakages that already happened in this project.

### 3.1 Assert invariants, not numbers

A hardcoded count is a time bomb: it breaks the moment an action is added,
and the failure looks like a regression when it's just a stale test.

```ts
// ✗ breaks the moment `audit` gains an action
expect(auditPerms.length).toBe(2);

// ✓ derives from the source of truth
for (const [resource, actions] of Object.entries(VALID_RESOURCE_ACTIONS)) {
  expect(permissions.filter(p => p.startsWith(`${resource}:`)).length).toBe(
    actions.length + 1
  );
}
```

### 3.2 Go through the public surface, not internals

tRPC middlewares (`requirePermission`, `withSectionAccess`) return a
`MiddlewareBuilder`, not a callable function. Test them through a real
procedure — it's the production path and survives tRPC upgrades.

```ts
const probeRouter = router({
  probe: publicProcedure
    .use(requirePermission('brands:create'))
    .query(() => 'ok'),
});
await expect(probeRouter.createCaller(ctx).probe()).resolves.toBe('ok');
```

### 3.3 Mocks must be as complete as the path under test

A partial mock doesn't make the test fail: it makes it fail **for the wrong
reason**. A `logger: {}` turned an expected `FORBIDDEN` into
`INTERNAL_SERVER_ERROR`, masking what was actually going on.

Before writing a mock, follow the execution path and include **every**
method it will touch — including the ones hit by the middlewares along the
way (`ctx.logger`, `ctx.prisma.appConfig` for `getRbacConfig`, etc.).

### 3.4 Recurring timers: never `runAllTimersAsync`

On a scheduler with `setInterval`, "run all timers" doesn't terminate by
definition — vitest aborts after 10,000 iterations.

```ts
// ✗ infinite loop
vi.advanceTimersByTime(60_000);
await vi.runAllTimersAsync();

// ✓
await vi.advanceTimersByTimeAsync(60_000);
```

### 3.5 Never write tautological tests

A test that asserts "the code does what the code does," written by reading
the implementation, gives coverage without giving guarantees — and it's
worse than no test, because it looks like protection.

Before every assertion, ask yourself: **what plausible bug would make this
test fail?** If you can't answer, don't write it. Derive the expectation
from the contract (Zod schema, type, a CLAUDE.md rule, required behavior),
not from the function body.

---

## 4. Luke-specific assertions per change

Tier selection is the evidence matrix's job. This table is the layer below it:
once the tier is chosen, these are the assertions this codebase has learned it
needs.

| Change                        | What the test must actually assert                                                                |
| ------------------------------ | --------------------------------------------------------------------------------------------------- |
| New tRPC procedure              | Permission granted/denied for admin, editor, viewer, anonymous                                     |
| New field on a Zod schema       | Valid input accepted, invalid input rejected with the right message                                 |
| New RBAC rule / section         | The three sources (`sectionEnum`, `SECTION_TO_PERMISSION`, `SECTION_ACCESS_DEFAULTS`) stay in sync |
| Mutation                        | `withAuditLog`/`logAudit` produces the expected audit row                                          |
| Multi-table write                | Transaction rollback leaves state consistent                                                        |
| New rate-limited route          | Present in `RATE_LIMIT_CONFIG`, `RATE_LIMIT_POLICY_DEFAULTS` and `RateLimitConfigSchema` (enforced by `apps/api/test/ratelimit.spec.ts`) |
| Interactive component           | The behavior, not the markup: what the user can reach, focus and trigger                            |
| Bug fix                         | The test fails on the pre-fix code — actually verify this, don't assume it                          |

---

## 5. Reports

One shape per mode. Never report a bare green tick: the point of this skill is
that "the tests passed" and "this change is proven" are different claims.

### `assess` — read-only

Writes nothing. Ends by naming the command that would close each gap.

```
QA ASSESSMENT
Scope: <paths>   Risk: <area: LOW|MEDIUM|HIGH, per area>

Required evidence        Status
  lint                   ✓ exists
  production typecheck    ✓ exists
  test typecheck          ✓ exists
  unit                    ✓ exists — <file>
  component               ✗ QA GAP — <what nothing can currently catch>
  integration             ○ not required — <why>
  e2e                     ○ not required — <why>

QA gaps
  <gap>  →  close with: /luke-test write <scope>

Residual risk: LOW | MEDIUM | HIGH
VERDICT: ADEQUATE | ADEQUATE WITH QA GAP | INADEQUATE
```

### `write`

1. Tests written or updated, with paths.
2. The actual result of the suites you touched. **Report the output, not a
   paraphrase**, and report the **test count** as well as the exit code — a
   runner that discovers nothing exits green.
3. If the coverage gate asked to update `test/procedure-coverage.ts`, say so
   and show the changed entry.
4. What you did **not** cover and why — an honest list is worth more than
   inflated coverage. Anything required and absent is a QA GAP, named as one.
5. For a regression test: the evidence it went **red on the broken code**. A
   test written against already-fixed code proves nothing.
6. Test files from other live sessions you left alone (§7.2), if any. Leave
   the line blank if the set was empty: it's not a section to pad.

### `verify`

Runs the evidence the scope requires and nothing else. Writes nothing — if a
required tier is missing, that is a QA GAP to report, not a test to go and
write.

```
QA RESULT
Scope: <paths>

Evidence                 Result
  <tier>                 PASS | FAIL | SKIPPED (<reason>) | QA GAP
  ...

Counts: <tier> N tests   (not just exit codes)
QA gaps: <list, or None>
Residual risk: LOW | MEDIUM | HIGH
VERDICT: PASS | PASS WITH QA GAP | FAIL
```

Never run the whole monorepo suite because it is easier than deciding. The
scope and its risk choose the tiers; the evidence matrix says which.
