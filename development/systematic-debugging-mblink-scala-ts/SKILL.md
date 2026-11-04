---
name: systematic-debugging
description: Structured debugging workflow adapted for Compiler Driven Development in scala-ts. Use when fixing bugs, investigating wrong generated TypeScript, macro failures, or test failures.
---

# Systematic Debugging

<EXTREMELY-IMPORTANT>
One hypothesis at a time, tested by ONE minimal change. Revert the change the moment
the hypothesis misses. After 3 failed hypotheses, stop and re-read the problem.
The compiler is the first diagnostic tool, not the last.
</EXTREMELY-IMPORTANT>

## Phase 1: Read the actual signal

Confirm the stack underneath before debugging the generator:

- TS toolchain installed? The round-trip tests run `yarn ts-node` in `tests/`; a missing `tests/node_modules` fails every suite's second property. Run `cd tests && yarn`.
- Stale output? `tests/output/` is deleted after each suite; a crash mid-run can leave files behind. They are gitignored and safe to delete.
- Right scala-ts in the consumer? BondLink uses this checkout only when sbt runs with `SCALATS_DEVELOPMENT=1` and the checkout is at `~/scala-ts`; otherwise it uses the published version.

Then read the compile-time signal:

1. Run `sbt Test/compile` — read compiler errors first.
2. Categorize:

| Category | First action |
|----------|-------------|
| Scala type error / warning | Read the full message; `-Werror` makes warnings fatal |
| Macro error at a `parse[T]` call site | The error is reported at the call site but comes from `TsParser`; find which `parse` branch handles `T` |
| Golden mismatch | Read the munit diff; identify which renderer produced the differing line |
| ts-node `TSError` in the round-trip | The generated TS doesn't type-check; reproduce with the printed file under `tests/output/` |
| Round-trip value mismatch | Compare the circe JSON (`_tag` discriminator) with what the codec decodes/encodes |
| `UnresolvedTsImportException` | A referenced type was never generated in any file passed to `writeAll` |

## Phase 2: Find the difference

1. Find a suite whose output for a similar shape is correct (`src/test/scala/scalats/tests/`).
2. Trace the model: what `TsModel` does `parse[T]` produce? (Print it from a scratch test.)
3. Trace the render: which of `generateCodecType` / `generateValueType` / `generateCodecInstance` / `generateValueInstance` emits the wrong text?

## Phase 3: One hypothesis at a time

1. Form a **single hypothesis** about the root cause.
2. Make **ONE minimal change** to test it.
3. Run the narrowest check (`sbt Test/compile` or `sbt 'testOnly scalats.tests.<Suite>'`).
4. If it resolves the specific failure, proceed to Phase 4; if not, **revert** and form a new hypothesis.
5. Log each hypothesis and result.

### 3+ failed hypotheses — STOP

Re-read the original failure, question the model, consider whether `TsModel` needs a new case rather than a patch in one renderer, and ask the human for context with your debugging log.

## Phase 4: Fix at the root, then verify

1. **Can this bug become a type constraint?** If an invalid state was representable in `TsModel` or the generator, change the type so it isn't.
2. Pin the corrected output with a golden expectation.
3. Lift the fix out and confirm the test fails again for the reason you claim — a fix never seen failing is unproven.
4. Run full verification per `verification-before-completion`.

## Debugging log

```text
Bug: [description]
Category: [compile / macro / golden / ts-node / round-trip / import resolution]

Hypothesis 1: [what you think is wrong]
Change: [what you changed]
Result: [what happened] ← REVERT if wrong
```

## Anti-patterns

- "One more thing" after 3 failures — STOP.
- Editing the golden string to match wrong output.
- Adding a runtime check for something the model should rule out.
- `asInstanceOf` or `@nowarn` to get past an error while debugging.
- Declaring victory without lifting the fix out to confirm the failure returns.
