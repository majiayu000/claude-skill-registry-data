---
name: testing-unit
kind: pattern
rule: testing
description: Pattern of rule testing. Load when creating or editing *.spec.ts under Vitest — the ready-made layout of describe and it, the fixture builder, the scenario id in the title, a Connect procedure test with a hand-written database double. Not for end-to-end tests — that is pattern testing-e2e.
---
<!-- rt-kit v0.34.0 · patterns/testing-unit.md · 1d97fe499563 · правится надстройкой, не здесь -->

# A test on a pure function and on a procedure

Pattern of the rule `testing`. What must be true — the law
`docs/constitution/verifiability.md`.

## When to use

- A `*.spec.ts` next to the source is being created or edited.
- Logic has to be moved out of a component or a service so that there is something to check it
  with.
- A test on a Connect procedure is being written.

## Imports are explicit

`globals: true` stands in the config, but the list is written anyway:

```typescript
import { describe, expect, it } from 'vitest';
```

## One `describe` per function

The block name matches the function name word for word; the `it` titles are sentences in Russian,
present tense, about behaviour, not about the internals:

```typescript
describe('applyDayClick', () => {
    it('SC-BK-19 — клик по занятому дню ничего не меняет', () => {
        expect(applyDayClick(day('2026-08-12'), selection)).toEqual(selection);
    });
});
```

The scenario id from `docs/specs/<domain>/scenarios.md` stands at the start of the title, followed
by a dash. Edge cases are separate `it` blocks in the same `describe`, not one test with a dozen
assertions.

## A fixture is built by a function with `Partial<T>`

Not by a repeated literal:

```typescript
function day(iso: string, overrides: Partial<ICalendarDay> = {}): ICalendarDay {
    return {
        iso,
        dayOfMonth: Number(iso.slice(8)),
        priceThb: 6000,
        busyNight: isNightBusy(iso, BUSY),
        past: false,
        ...overrides,
    };
}
```

Shared constants (`PRICING`, `BUSY`) lie at the top of the file, at module scope.

## A decision is moved into a pure function

The dominant form in this tree: the logic moves into `*.logic.ts`, `*.util.ts` or
`*.calculator.ts` and is checked by a call — without `TestBed`, without substituting dependencies.
Samples — `libs/site/common/booking/util/src/lib/availability-calendar.logic.ts` and
`libs/api/<quote domain>/util/src/lib/quote.calculator.ts`.

## A procedure is called directly

The handler is the `handle` method of the procedure class in the `feature` layer of its domain. The
database double is written by hand; the sample is `FakePrismaClient` in
`libs/api/<booking domain>/feature/src/lib/link-booking.procedure.spec.ts`:

```typescript
const prisma: FakePrismaClient = new FakePrismaClient();
await procedureWith(prisma, emitter).handle(request());
```

What is checked is the order of actions, the rollback when half of it is refused, the idempotence
of a repeat and what exactly went into the database. The layout of fields is guarded by the tests
of the `api` layer and is not repeated here.

## A one-off proof test

A defect that is otherwise confirmed only by reading the code is proved by a test written for the
time of the investigation: it raises the real procedure, substitutes its only way out and counts
the calls.

```typescript
globalThis.fetch = (): Promise<Response> => Promise.resolve(Response.json({ success: false }));
```

The number before the edit and the number after are the only form of answer such a check gives. "A
hundred calls out of a hundred" and "twenty out of a hundred" can be told apart, and "the code looks
right" cannot.

The second way to take the "before" is to put back the version of the file from the point where
the branch diverged and run the branch's test: the test failing is the reproduction of the defect.
After that the file is restored from the copy, and the restoration is checked by running the same
test, not by memory.

Doubles of the neighbours are not invented: the working set is taken from the test of a
neighbouring procedure of the same domain. A double assembled by type fails not on the assertion
but on the call of a method it does not have.

**Such a file is not committed.** It lives until the end of the investigation and is removed
together with it; a check worth keeping is rewritten as an ordinary `*.spec.ts` with the scenario
id in the title and goes in the branch. The sign of a temporary file is that its title names no
scenario at all.

## Green that checks nothing

**A probe that expects silence goes paired with a probe that expects a refusal.** Silence also comes
when there was nothing to check with. A prefix before a command in the pipeline acts on one link,
and a hook that got an empty value is silent exactly like a hook that has nothing to refuse. Two
probes out of three are green then — they expected silence — and the miss is visible only by the
third, which expects a refusal.

**A probe on a mine that does not go off is green without the fix.** A scenario on the table of
refusal codes for a spec without procedures would have passed before the edit too: the audit
never has to read that table at all. Such a probe is checked from both sides — the previous state
is brought back for a minute and the probe is run: it did not turn red, so the probe guards
nothing.

## Common misses

- A lib without its own `vitest.config.mts`: `nx test <project>` passes green without running a
  single file. Before writing the first test in a lib, check that the config is next to it.
- **The compiler import goes into the harness file, not into the spec.** A lib that renders nothing
  still pulls the framework when its test imports a barrel with a framework service, and the first
  import fails on JIT. The import goes into the file named in `setupFiles` of the lib's run config:
  in the spec the linter moves it below its neighbours, and the test turns red only in the full set.
- Substituting a module (`vi.mock`) would hide what the test is created for — which call went to
  the database and in what order. The double is written by hand.
- Do not create your own helpers for assertions: `expect(...).toBe(...)` and `.toEqual(...)`
  directly.
- A title with a scenario id that does not exist takes `npm run check:specs` down, while the tests
  themselves stay green.
