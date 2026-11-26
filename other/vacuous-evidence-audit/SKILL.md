---
name: vacuous-evidence-audit
description: >-
  Evidence discipline for a width-reduction or optimisation campaign where many agents land many small
  changes into one tree. Distilled from the ecdsa.fail 793-to-792 rung (2,036 over-cap cells to 216,
  23 merges, 12 workers), in which a census counted cells on a circuit that could never build, a
  patch applied cleanly and silently deleted a merged class, a gate pass could not be reproduced, eight
  distinct kinds of negative control turned out to prove nothing, two classes passed review on
  structural arguments and were later found unsound, a "120-cell" change turned out to be three
  stacked 40-cell changes, and a retired worker left 19 GB of
  orphans after reporting it had stopped. Use when evidence from parallel workers is being merged into a
  shared artefact; when a change "passes" and you want to know whether the test could have failed; when a
  premise is about to be accepted on sampled data; or when deciding whether to continue a campaign.
---

# Schuumlöffel (vacuous-evidence-audit)

The failure mode this skill is about is not a wrong answer. It is a **right-looking answer produced by a
check that could not have failed**. Every incident below passed its own test.

**The one-line rule: prefer evidence that measures the EFFECT over evidence that measures the ACTION.**
A process count is an action; free memory is an effect. A gate that passes is an action; a control that
fails is an effect. A knob that is "applied" is an action; a cell count that moves is an effect.

## 1. Eight ways a negative control proves nothing

A control is supposed to break the change and make the test fail. All eight of these were reported as
passing controls by competent workers, in one codebase. The first five turned up in a single day.

| # | Mode | How it looks | How to catch it |
|---|---|---|---|
| 1 | **The branch is never emitted.** | Control passes 16/16. | Probe the walk: count how many times the broken statement is actually emitted. One case had 370 calls, all with the branch's inputs `None`. |
| 2 | **The condition is too rare in the test walk.** | Control passes 64/64, or fails 1 of 64. | Ask what makes the broken code matter, then check the test reaches that state. One control only mattered when a counter hit its maximum. |
| 3 | **An operation and its undo share a view.** | Control passes; the error cancels itself. | Break the operation and its inverse *asymmetrically*, or check an intermediate state. |
| 4 | **The control selects its break by an environment variable the code does not read.** | Control "passes" because nothing fired. | Verify the break fires at all before interpreting a pass. A typo in a variable name is indistinguishable from success. |
| 5 | **The harness cannot represent the production configuration.** | Everything passes and the knob is inert. | Sweep the harness parameter. One route was room-dependent; the harness ran 28 scratch lanes against production's 256, and *no representable count* fired it. |
| 6 | **The regime is too rare for random seeds; only forced construction finds it.** | Random gating passes 8/8; the class is broken. | Construct inputs that force the regime. Two unsound classes passed random gates and then failed **37/37** and **13/13** on forced parent-passing shots. |
| 7 | **The configuration shifts under the evidence.** | Every measurement is honest and the shipped artefact differs. | Ask what the evidence's configuration was. A whole campaign's room-dependent gates were measured at peak width 793 while the row would ship at 792 — where those gates **re-decide**. |
| 8 | **The gate cannot observe the quantity the control perturbs.** | Control passes 64/64 *and* the change is fine *and* you have learned nothing. | Ask what the harness actually reads. Controls dropping a carry-in term passed every gate because no gate observed that term; only a failure-rate comparison could. |

Modes 5, 7 and 8 are one family seen from three sides: **the test's configuration is not the shipped
one, the test's instrument does not read the broken quantity, or both.** Write down, for every gate,
*what it would take for this to pass while the change is wrong* — that question finds all three.

**Therefore: tune a control until it fails, then say which reason it fails for.** Distinguish a **value**
failure (a result is wrong) from a **structural assert** (an invariant tripped before the value was
computed). A structural failure is a weaker control and must be labelled as one. Report the variants you
rejected and why — the rejected ones carry most of the information.

**The strongest form, when the input space allows it: exhaustive enumeration through the real emitted
gates.** One component was proved over all 8,192 of its inputs, checking the result, the restoration of
every input lane, and zero phase. That beats any seeded gate and needs no control at all — though build
one anyway, as a second test using the same counting function, so it cannot be vacuous by construction.

**When a control will not bite, stop tuning it and enumerate instead.** A seeded gate could not reach
a one-monomial defect on four slots: 16/16 passed and proved nothing (mode 2). Replacing it with an
exhaustive harness over the kernel's own input space — **33,988,608 states in 1.3 s**, all lane
patterns x all 5-bit parameters, checking value, zero phase, and bit-for-bit restoration of every
input lane, every *dirty* lane and the borrowed register — returned **0 bad**, and its three controls
bit at 17M, 13M and 1.6e9 states. **The control that the seeded gate could not make fail was the
control that bit hardest here.** Decisive: identify the kernel's true parameters and check none is
slot- or site-specific; if none is, the enumeration covers every site, and the remaining risk moves
entirely into the plumbing — say so, and name the plumbing you did not cover.

## 2. Merging many workers' changes into one tree

1. **Diff against a COMMIT, never the live tree.** A worker diffed its change against the integration
   tree *after another class had been merged into it*. The resulting patch legitimately encoded "add
   mine **and remove theirs**". It applied cleanly, built, and censused plausibly.
2. **After every merge, re-measure with the new knob ON and OFF.** Identical counts both ways means the
   knob is not firing — a different failure from "closes nothing", and invisible otherwise. This caught
   both the silent deletion above and, later, a patch that had not applied at all.
3. **Keep a tripwire on the other classes.** Track a global the other changes contribute to (here, raw
   gate count). One candidate knob silently *disabled* a merged class; the tripwire showed a 1.42M drop
   where the expected delta was a few thousand. The same technique on another block moved it by 2,960 —
   the tripwire is what distinguishes them.
4. **Every gate result must cite the binary it ran on — path and hash — and the commit that built it.**
   One command line produced three different figures in an afternoon. The cause was binary provenance,
   not non-determinism. A gate figure without a binary identity is not evidence.
5. **State where the test configuration differs from production, and which branches no test reaches.**
   Five such divergences surfaced in one day. *None was found by the author of the class.*
6. **Prefer a three-way merge to applying a patch** when the contributing tree may predate the head.
7. **A composite is not a unit — measure every knob ALONE and in every subset you might ship.** A
   change presented as one 120-cell closure was **three stacked 40-cell closures**, and the two knobs
   that moved **nothing** on their own each owned a third of it: they were composition-dependent on
   the third, which freed the resource they spent. **A knob that moves nothing alone is not inert.**
   This cuts both ways, and the second way is what matters at review time: when one component of a
   composite rests on an unestablished premise, the only way to know whether you can **drop** it is
   the subset measurement. Here the answer was no — it was load-bearing for 40 cells — but the
   question took three 3-second runs to settle and had been open for a day because the parts were
   only ever reported together. **Ask it before the review, not after.**

## 3. Premises and sampled evidence

**Rare-regime absence is not evidence of impossibility.** A premise was nearly accepted on 9,221 samples
in which **two of the four states the premise itself permits appeared zero times** — a sample that never
reaches the tails of the permitted set cannot rule out a rarer forbidden one.

- **Report the histogram, not the violation count.** If states the premise *allows* never appear, the
  honest verdict is "not established", not "no violations found".
- **A parent-failing shot is not a violation.** A measured failure rate of 6.6e-4 turned out to be
  counting inputs the unmodified circuit already loses. It was within one message of being written into
  a submission note as a cost of the change.
- **Argue structurally where you can.** One premise was closed in a paragraph by finding a flag the code
  already set that guaranteed the property. Another was proved by showing the representation *cannot
  hold* the violating value. A paragraph beats a billion samples.
- **But a structural argument is not self-certifying, and its failure mode is always the same one.**
  The two classes that passed review and were later found unsound both died on **the frame at the
  site**: one read a table column for the *unswapped* cofactor at a site that runs *after* the
  un-swap; the other inherited a premise audited on a neighbouring slot range. Both authors were
  competent, both arguments read as correct, and **neither was caught by its author.** So when a
  component's only backing is "the argument is structural", say out loud that **this is the same
  evidence shape as the ones that were wrong**, and have someone else attack the frame specifically:
  which column, in which basis, at which site, after which transformation.
- **Declare the premise before building on it**, as a quantified sentence, naming which classes of input
  it must hold for **and whether your evidence can reach them**. The one defect found this way was found
  by the author, pre-emptively, because it had to write the sentence down.
- **Two independent attacks beat one.** A reviewer bounded a failure it never observed; the author found
  it only when told to attack its own work. Neither alone settled it.

## 4. Technique notes that generalise

- **What binds is usually clean workspace, not information.** Check whether the live *information* fits
  in fewer lanes before hunting for a lane to free.
- **Clean workspace is replaceable by borrowed dirty lanes at a cost — with one boundary.** Dirty
  borrowing works where the borrowed lane **controls an operation into a separate target**. It **fails
  where the target and the source are the same register**: a dirty value leaves a cross-term that needs
  the original, which has already been overwritten. This rule killed a 1M-unit lever *and* correctly
  predicted which of two remaining constructions would survive.
- **Look for a shared plateau.** If several over-cap moments share one inventory, one lane out of it
  covers all of them. Removing a binder that does *not* share the plateau merely **moves** the moment —
  five separate attempts in one day closed one moment and gained nothing.
- **Feasibility before construction.** A count-only measurement with deliberately invalid circuits — "if
  this relief existed, would the count move?" — collapsed a four-piece plan to three in minutes. Label
  the result feasibility, not closure.
- **A reported failure is a live lead, not a closed door.** One route was reported as failing because it
  pushed the problem elsewhere; two later changes relieved exactly there, and the same unmodified code
  then worked, and was cheaper. It survived only because the failure was written down with its mechanism.

## 5. Operational traps

- **A worker's "nothing is running" can be sincerely wrong.** One left eight parallel jobs holding 19 GB
  after an honest wind-down. **Reap by inspecting processes, not by asking.**
- **Killing a timing or `env` wrapper does not kill the child.** The wrapper dies, the child is orphaned,
  the process count improves and the memory does not move. Target the child.
- **A job that stops early still leaves a file that looks like a result.** Check exit status before
  reading numbers. Three unattended runs died silently in one day.
- **Compressed size is not a proxy for content size.** A stream shrank 16 % from a change worth 1.3 % —
  the change made the output more regular, so it compressed better. Compare decoded content and its hash.
- **A build that merely compiles is not a verified port.** When hand-resolving a conflict or inserting a
  constant, check the *value* against the source, not just that it builds.
- **Environment-first configuration is a reproduction hazard.** If a parameter reads the environment and
  falls back to a source constant, a build with that variable still exported produces a *different
  artefact that builds and runs normally*. Build clean and say so in the note.

## 6. Deciding whether to continue

Write the stop condition **before** you need it, and in falsifiable terms. For an all-or-nothing target,
**90 % closed is worth exactly zero**, so the question is never "how much have we closed" but "does every
remaining block have a route".

Keep a live table of blocks against routes. A block whose only route needs an unaudited premise is not a
route. Require, at the checkpoint: a plan that closes **on paper**, and at least one piece independently
tested. **Make the paper gate precede the code** — a one-page plan killed a day's work twice in one
afternoon, once by showing the planned relief targeted the wrong lane and once by collapsing four pieces
to three.

**When you stop, write the ledger that makes stopping reversible.** Not "these routes failed" but, for
every dead route, **the constraint whose movement would revive it**, named precisely enough to
recognise if it moves. The reason this pays: a bound that had blocked four slots for the whole
campaign turned out to be **inherited from a configuration that no longer existed** — the band it
guarded had been removed days earlier, and nobody had re-asked. Dead routes accumulate against
constraints, and constraints move. A route list without revival conditions is a list of regrets; one
with them is a work queue for whoever arrives next. Flag separately any dead route you suspect rests
on an inherited bound, and mark leads you could not audit **do-not-trust** rather than dropping them.

And keep a short resume document separate from the running log. A 1,600-line append-only log is an
archive, not a handover.
