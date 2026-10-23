---
name: testing-blocks
description: "Use when a skill or agent in this framework has been written but never proven to change behaviour: validate it with a pressure scenario, run without the block then with it, keep the recorded excuses as a table, test the routing text, and measure compliance across prompt strictness."
---

# testing-blocks

Cross-cutting, meta (`WORKFLOW.md` §2). This block exists because most of this framework was written
and never proven. `CATALOG.md` marks that honestly as 🟡, but a status isn't a test.

It's the `tdd` discipline turned on the framework itself: **a block's output is agent behaviour**, so
the test is behavioural. And it's cheaper than what we were waiting for — you don't need a real
project and a real feature to find out a block doesn't work.

The protocol is a method, not a tool: it needs a way to run the same scenario with and without the block
and a way to record what the agent said it was doing. Any evaluation harness that offers a baseline arm
(the run without the block) mechanises step 1; without one, run the two arms by hand. The harness never
invents the pressure scenario or records the rationalisation for you. The adaptation for the harness this
repository is developed on is in the note at the end.

## When
Before a block moves out of 🟡. Also when a block was followed in the calm case and ignored the one
time it mattered: that's not bad luck, that's a failed test nobody ran.

## Steps

### 1. RED: watch it fail without the block
1. **Write a realistic scenario** in the block's domain, with a concrete choice to make: real file
   paths, actual options A/B/C, work the agent believes is genuine rather than a quiz.
2. **Run it with the block absent.** You need to see the wrong behaviour happen.
3. **Record the exact reasoning used to justify it, verbatim.** Not "it skipped the check" but the
   sentence it told itself: "the tests are probably fine", "the user is in a hurry so I'll verify
   after". Those sentences are the specification for what the block has to counter. Paraphrasing
   them loses the thing you're building against.

### 2. Apply pressure, or you've tested nothing
A block that holds in a calm scenario tells you nothing about the moment it's needed. Combine at
least two of these:

- **time**: a deadline, a demo in ten minutes
- **authority**: someone senior already said it's fine
- **consequence**: the fix is blocking someone else
- **sunk cost**: two hours already spent down this path
- **fatigue**: the fourth attempt at the same failure
- **social**: being seen as obstructive for insisting
- **pragmatism**: "this is the exception, obviously"

Combined pressure is the realistic case. The single-stressor version is the academic one, and passing
it is not evidence.

### 3. GREEN: write against the recorded rationalisations
1. Target the sentences from step 1.3 **specifically**. A generic "don't skip verification" doesn't
   engage a reasoning chain; the counter to "the tests are probably fine" is "probably is the word
   that means you haven't looked".
2. Re-run the same scenario with the block present. Success is behavioural: the right option chosen,
   ideally with the block's reasoning cited back.

### 4. REFACTOR: close the loophole it finds next
1. An agent that can no longer take the old shortcut will find a new one. That's the expected result,
   not a failure of the block.
2. Add the specific counter, re-run. **Don't stop at the first compliance**: the first pass usually
   closes the obvious route and leaves the clever one open.
3. Stop when a round of pressure produces no new workaround.

### 5 to 8. The rest of the method
The four steps above are the core. The rest lives one file per section under `references/`; read the rows
whose trigger the task meets.

| § | Covers | Read it when | File |
|---|---|---|---|
| 5 | Keep what the runs taught as a table, not as prose | a block has been run under pressure and the recorded sentences have to be kept | [`05-rationalisation-table.md`](./references/05-rationalisation-table.md) |
| 6 | Test the routing text on its own | a block's description is written or changed, or a block loads on the wrong tasks | [`06-routing-text.md`](./references/06-routing-text.md) |
| 7 | Measure compliance across prompt strictness | a block, a rule or an agent definition has to be measured across runs | [`07-compliance-measurement.md`](./references/07-compliance-measurement.md) |
| 8 | Model matrix, exit gate and the three-arm protocol on a pinned fixture | a block is about to leave 🟡 on measured runs, or a result is compared across models or against no block | [`08-matrix-gate-arms.md`](./references/08-matrix-gate-arms.md) |

## Output / checkpoint
For each block tested: the scenario, the pressures applied, the verbatim rationalisation from the RED
run, the behaviour in the GREEN run, and the block's table of excuses and counters fed from those sentences
(§5), and, where it was measured, the compliance rate per prompt level (§7). That's what promotes a block out of 🟡 in `CATALOG.md` —
and the maturity note says *tested under pressure*, which is a different and weaker claim than *used
on real work*. Both are worth having; don't let one stand in for the other.

## Guardrails
- **A block that passes only an academic test is untested.** Record the pressures applied, so the
  claim can be judged.
- **Don't skip RED.** Writing the block first means writing against imagined failures, and the real
  rationalisations are consistently more specific and more reasonable-sounding than the invented ones.
- **Don't grade your own homework in the same context.** The run that judges compliance shouldn't be
  the one that wrote the block; same reason `galadriel` exists.
- **A predicted rationalisation is labelled as predicted.** Only verbatim sentences from a run may be
  presented as observed.
- This tests whether a block **changes behaviour**, not whether its content is correct. A confidently
  wrong block can pass this and still be wrong: correctness comes from the source, from review, and
  from real use.

## Adaptation note: Claude Code
The platform's evaluation runner (`claude plugin eval`: scored cases in `evals/**/case.yaml`, graders in
`graders/*.md`, run against a plugin, a skills directory or a `plugin@marketplace` id) adds a no-plugin
baseline arm automatically, which is the RED run of step 1 mechanised. As of 2026-09-07 this protocol
predates the runner and has not been re-expressed as eval cases; that is the open item in `CATALOG.md` §2.
The runner was in early access then (on CLI 2.1.218 `claude plugin eval init` answered that it was
currently in early access), so the manual protocol is the only one available until that opens: check the
runner again rather than assuming the gate moved.

## Origin
Rewrite of `testing-skills-with-subagents` from a market skills repository (the companion repo of the
upstream this framework is a response to). The RED/GREEN/REFACTOR structure, the pressure taxonomy and
the "record the rationalisation verbatim" rule are theirs and are taken as-is because they're better
than what we had, which was nothing.

Found late, and the omission is worth recording: this framework's own sourcing pass had enumerated a
137-agent per-technology catalogue while never listing the contents of the project it takes its
premise from. The distinction between *tested under pressure* and *used on real work* is ours, added
so this block can't be used to quietly retire the dogfooding requirement.

Sections 5 to 7 added 2026-10-02: the table of recorded excuses and the list of tells come from the public
Superpowers repository's skill-writing guidance (MIT licence, read 2026-10-02), rewritten so the table is
fed only from verbatim runs and a predicted row is labelled as predicted; the description-only test
comes from its observation that an agent follows a description that summarises the process instead of
opening the block. The compliance measurement of §7 (an expected sequence of observable actions, three
levels of prompt support, classification of the trace by meaning with a deterministic order check, and
promotion of low-compliance steps to a hook) comes from the `skill-comply` skill of the public ECC repository
(MIT licence, read 2026-10-02), rewritten harness-neutral: its scenario generator, its trace capture and its
model prompts were not taken, and the three levels are renamed in our terms. The mechanisms were rewritten in
our terms and no text was copied.

Section 8 added 2026-10-02 is ours and has no external source: the pinned fixture, the three arms (absent,
routed, forced), the model matrix and the exit gate (no criterion at 0% in every cell, no negative delta) are
built on §1-§7. It has not yet been run on a real block.
