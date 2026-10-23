---
name: gate
description: "Use when the code is written, before the review, mechanical lock: declaring a criterion \"passing\" without evidence is forbidden, a clean-context evaluator decides, and no claim of success is made without a command that proves it."
---

# gate

Step 7 of the pipeline (`WORKFLOW.md`). **The number one reinforcement from the scouting.**
Turns "tests are green" from a declarative wish into a **proven fact**. "Done" becomes
structural, not a claim.

## When
After `code` (implementation done), before `review`. Also, on a smaller scale, before any sentence that says
something works, is fixed or is finished (§8).

## Steps
1. For every `{ passes: false }` line in `test-results.json`, **produce evidence**: test
   output, a recorded run of the journey, or a log; then **read** it.
2. **A guard refuses to write `passes: true` until the matching evidence has been read.** You cannot declare
   yourself passing without observing. Where the runtime can enforce this, a pre-write hook does
   (the scripts and per-repo wiring are in [`hooks/`](../../hooks/README.md)); where it cannot, the same
   rule is kept by the evaluator in step 3 refusing any line whose evidence is not in the read log. "Exists" isn't
   enough, the evidence has to have been opened.
3. Run the **clean-context evaluator**: an agent **with no write access**, which didn't watch
   the build, examines the diff + the evidence and returns `PASS` or `NEEDS_WORK` + findings.
4. `NEEDS_WORK` → the findings become the prompt for the next `code` pass, and the loop re-runs steps 1-3
   until `PASS` or the attempt cap. The exit condition is exactly the evaluator's verdict, so this is a
   goal-based loop with a bound, not a manual relaunch.
5. **Gate on the artefact, not the exit code.** For anything that is not a test runner (a migration, a
   build, a deploy, an export, a script that calls an API), `rc=0` is not a success. Open the output: a
   `200` whose body carries an `errors[]` is a failure, a log line saying "0 rows processed" is a finding,
   and a command that printed nothing proves nothing happened as much as nothing went wrong. An instrument
   that reads zero because it was not attached is not a measured zero; say which of the two you have.
6. **Never invent a datum to fill a hole.** A default is not data: `return []` on an error fabricates an
   empty result, `0` for a failed measurement fabricates a measurement. Fail loudly, or return a value that
   carries its own absence. A value shown only as an illustration is labelled as one, and the test is
   whether the reader can see that it was not measured.
7. A journey that can run is driven as an inventory of controls (`skills/qa-exploratory-testing` §5); if
   nothing can run, say so and verify by reading the code, never by writing PASS.

The sections below are read **when their trigger is met**, not all at once. A section read is a section
that has to be applied.

| § | Covers | Read it when | File |
|---|---|---|---|
| 8 | The law of proof: which command proves which claim, the four proof states, reuse and stop | you are about to say that something passes, is fixed, is done, or to accept a worker's "done" | [`08-claims-and-proof.md`](./references/08-claims-and-proof.md) |
| 9 | The verification loop: build, types, lint, tests, diff sweep, one report per phase | the evaluator step is next, or the change is about to leave your hands | [`09-verification-loop.md`](./references/09-verification-loop.md) |
| 10 | Excuses and red flags | you notice yourself reasoning about why a check can be skipped | [`10-excuses-and-red-flags.md`](./references/10-excuses-and-red-flags.md) |
| 11 | Two independent evaluators | the change ships without a human reading it, or its failure is expensive and hard to undo | [`11-double-evaluation.md`](./references/11-double-evaluation.md) |
| 12 | In-flight doubt: triggers, artefact and contract without the claim, four-class reconciliation, stop signals, second model | a decision is non-trivial and about to stand, before the change exists in full | [`12-in-flight-doubt.md`](./references/12-in-flight-doubt.md) |

## Output / checkpoint
`verified`: every line `passes: true`, each backed by evidence that was read, evaluator `PASS`.

## Guardrails
- **No claim of success without fresh evidence from a command run in this turn.** The law of the block, and
  the reason for every step above.
- **Exit code 0 and a populated file are claims, not evidence** (step 5), and a fallback value is never evidence (step 6).
- The agent **cannot validate itself**: validation comes from the guard (evidence) + the evaluator (clean
  context). No homemade layer where the runtime already offers the loop or the hook: invoke it, don't
  reimplement it.
- Never lower a threshold, drop a case or skip a check to turn the verdict green (`skills/tdd`).

## Adaptation
The block is written for any agent runtime. In Claude Code the guard of step 2 is a `PreToolUse` hook, the
evaluator of step 3 is a subagent without `Write`/`Edit`, and the loop of step 4 is native `/goal`.

## Origin
Market long-running agent patterns (default-FAIL hook + fresh-context evaluator), rewritten
our way. The iteration itself is the runtime's own goal loop, not a block.

§8 rewritten from the `verification-before-completion` skill of `superpowers` (MIT) and the `verify-and-stop`
skill of `caveman` (Apache-2.0, no text copied); §9 from the `verification-loop` skill of `ECC` (MIT); §11 from
the `santa-method` skill of `ECC` (MIT); all read 2026-10-02. §10 is predicted, not recorded (see the file).

§12 rewritten from the doubt-driven-development skill of addyosmani/agent-skills (MIT, Copyright (c) 2025 Addy Osmani, `LICENSE` read 2026-10-21), read 2026-10-20, no text copied. Not taken: its claim that nested subagents cannot exist (our own measurement shows they can, and return fabricated results, `skills/dispatch-parallel`), its fixed three-cycle cap (we ask for a stated cap), and its tool-specific command lines. Point 9 is its doubt-theatre signal; points 10 and 13 are ours. Status 🟡, never dogfooded; the second-model rules are unverified against any installed tool.
