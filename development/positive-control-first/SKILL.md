---
name: positive-control-first
description: Use whenever you write a new test, canary, gate, guard regex, or alarm. Run it against the UNFIXED code first and record the failure shape. A test that has never failed is a silent instrument, not coverage.
triggers: new test, canary, gate, guard regex, alarm, unfixed code, failure shape, red first, silent instrument, mutation, noisy alarm, true case, red-green
---

# Positive Control First

> **A new test is not done until it has been run against the code it is
> meant to catch, and the failure recorded in the PR body.**

A green test proves nothing until you have seen it go red for the right
reason.

## The base rate

Every new test in the 2026-09-01 wave was run against unfixed code first
and its failure shape recorded — middleware 6f/8p · ingest-gmail 5f/1p ·
recall 5f/1p · N-1 2f/1p. **Two of those four runs caught test-harness
bugs that would otherwise have shipped as green tests of nothing:**

- `vi.restoreAllMocks()` stripped factory resolved values, so
  ingest-gmail crashed on `.length` rather than asserting.
- A `mockImplementationOnce(throw)` was left unconsumed by a read-only
  control and fired in the **next** test.

Cost of running the control: none. That is the point.

## Three ways a canary lies

1. **A mutation that SURVIVES.** Two independent layers rejected the
   input, so removing either left behaviour correct and the suite green.
   **Pin layers separately** — a single end-to-end assertion cannot tell
   you which layer holds.
2. **A red for the WRONG reason.** `vi.clearAllMocks()` does not drain a
   `mockResolvedValueOnce` queue, so the "failure" was a harness artifact.
   **A red you did not diagnose is not a passing canary** — read the
   message, not the colour.
3. **The scanner matched NOTHING.** A detector that returns an empty list for
   every input looks like a clean subject, and a mutation arm does not always
   catch it (#2359: a depth counter started at 0 after the opening brace, so
   the live-tree arm was green over a dead detector). Add an arm that asserts
   the scanner LOCATED its subject: a non-zero count of matched units and the
   exact expected count of each named one
   (`scripts/agent-os/ciMemorySampler.test.mjs:189-200`).

## Fixing a noisy alarm

When the change makes a *false* alarm stop firing, the test must prove it
**still fires on the true case**. Silencing and fixing produce the same
green suite otherwise. Assert both halves: quiet on the false input, red
on the real one.

## A positive control can pin a falsehood

The control must assert something that is *true*, not merely something
that is *present*. Live example on `main`:
`apps/nickstire/client/src/__tests__/canonical-business-truth.test.ts`
asserted `"the new-ownership statement is still on the site"` — but the
owner confirmed 2026-09-03 that Nick's is the **same owner** who renamed
Moe's, so the invariant was false. It stayed green on **exactly one** line:
an unrelated consumer-advice sentence in `shared/guides.ts` about shops in
general. (A comment in `shared/voice.ts` repeats the retired phrase but was
never counted — that scanner already strips comment lines before building
`LINES`, which is the remedy, not the bug. An earlier draft of this skill
named it as a second cause; that was wrong.) Fixed in #2206. See
`empty-vs-error` — "when a test resists a correct fix, read the test as a
finding."

**So: after writing a control, ask what it would take to make it fail
dishonestly.** If a comment or an unrelated string can satisfy it, scope
it (strip comments, anchor the pattern, name the file).

**And the dual: once the scanner strips comments, the mutation must target
the LIVE text.** `String.replace` takes the first match, which after a repair
is usually inside the comment documenting it; the stripper then erases the
mutation and the arm passes having changed nothing the scanner reads
(`ciMemorySampler.test.mjs:154-165`). Anchor the mutation on the executable
line and assert it occurs exactly once before mutating.

## Checklist

1. Write the test.
2. Run it against the **unfixed** code. Record `Nf/Mp` and the message.
3. Confirm the failure is the one you meant, not a harness artifact.
4. Apply the fix; confirm green.
5. Mutate the fix back out; confirm red again.
6. Paste steps 2 and 5 into the PR body.
7. **A control about module RESOLUTION, binary availability or environment
   shape is evidence only in the runtime the consumer uses.** Vitest
   workers carry `NODE_PATH` into pnpm's hoisted store, so a bare
   `require.resolve("sharp")` inside a test RESOLVES and proves nothing
   (witnessed 2026-09-15, #2339: the first draft of that control was
   green for exactly this reason); scripts resolve from their own file's
   directory, not the cwd. Spawn the consumer's runtime (a `tsx`/`node`
   child with `NODE_PATH` removed, cwd as in production), import the REAL
   symbol, and run step 5 against that child.
8. **A scan or grep control must find a PLANTED positive in the same
   invocation shape as the real scan** (same cwd, same path form, same shell).
   Two shapes return empty with a success exit code, the same as "nothing
   found" (2026-10-20, secret-history scan): `git grep --no-index` given a
   path outside the working directory matches nothing; and Windows PowerShell
   5.1 strips `"` from native-command arguments, so a regex containing `"`
   never matches.

Related: `assert-the-consumer` · `empty-vs-error` · `guard-red-team`
(the same discipline for deny-lists and guard regexes).
