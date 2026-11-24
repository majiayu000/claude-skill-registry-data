---
name: failing-test-first
description: "Use when adding behaviour or fixing a bug where a test runner exists, even if tests went unmentioned. Skip throwaway work, docs, config and anything the user excluded."
user-invocable: false
---
# Failing test first
Job: Change behaviour through thin red-green steps at public seams.
Takes: a behaviour or `slice` card.   Gives: code and behavioural tests.
Team moves: claim files, remember

## Steps

1. **Fetch the work.** Read any reference you were given, card, issue or chart, and state its title. If it could mean two things, ask. A worker puts that under `Open`.
2. **Pick seams before the first test.** A card that carries an agreed seam settles this. Otherwise note what each seam catches and what it misses, announce that in a line or two, and carry on. Ask only if the choice changes what gets built. If the interface's shape is unclear, use the skill `module-depth`.
   `Seam: POST /refunds. Catches validation, rounding and storage. Misses the gateway's real replies.`
3. **Run the loop, one seam and one test at a time.**
   1. Write one test that states a capability. Run it and see it fail for the reason you expected.
   2. Write the least code that makes it pass.
   3. Run that test file and the typecheck. Let what you learned choose the next test.
4. **Close the loop.** Once every behaviour has a test, run the full suite once. Refactoring waits for the check stage.
5. **Hand on.** Use the skill `finish-line`, then commit. That is the route `one-card`.

## A test worth keeping

It sits at a public interface and reads as a capability statement: `refuses a refund above the captured amount`, rather than `calls validateAmount`.

Reject these, and rewrite them before moving on:

| Reject | How to spot it | Write instead |
|---|---|---|
| Coupled to internals | Breaks on a refactor with behaviour unchanged, asserts call order or call counts, or verifies through a side channel such as reading a table directly | Assert what a caller can see, through the same interface a caller uses |
| Self-confirming | The expected value comes from the logic under test: `expect(tax(200)).toBe(200 * RATE)` | An independent known answer: `expect(tax(200)).toBe(15)` |
| Bulk, ahead of code | Several tests exist before any code does, checking an imagined shape | One test, its code, then the next test |

## Mocks

- Mock only what sits outside your system: third-party APIs, the clock, randomness, and sometimes databases and filesystems. Code you own stays real.
- Inject each external dependency, so a test can pass its stand-in.
- Give each external operation its own function, `chargeCard` and `fetchRates` over one generic `request`, so each mock returns one shape.

## No runner

Say so, and use the closest real check: run the program, call the endpoint, inspect the output. Adding a runner is the user's call.

## In a team

This is the worker's default loop.

- In a shared tree, claim your files before editing. An isolated tree needs no claim.
- Read the pinned notes on the files you touch before you change them.
- Pin any trap you hit, short and tied to its location.

## Done when

- Every behaviour asked for has a test you saw fail, then pass.
- Each seam was announced with what it catches and misses, or came from the card.
- No test matches a row of the reject table.
- Mocks stand only for what sits outside the system.
- The typecheck is clean and the full suite passed once at the end, each quoted as `[observed]`. Without a runner, the closest real check is named with its result, and the missing runner is stated.
- Refactoring is left to the check stage, and nothing the user excluded was touched.
