---
name: build-a-baseline
description: Stop conclusions drifting between sessions by turning a judgement call into a fixed scoring rule over measured data, with the subjective inputs frozen in a file, the measuring instrument validated against a known-good source, and falsification thresholds written down before the test is run. Use when the user says you keep changing your mind, contradicting yourself, or have no baseline; when the same question has produced three different confident answers; when a decision rests on a vendor score nobody has checked; or before acting on any ranking you derived by reasoning rather than by rule.
---

# Build a baseline

Some questions get re-answered every session: which keywords matter, which
channel to spend on, which feature to build next. Each pass gathers what it can,
reaches a confident conclusion, and the conclusion is different from last time.
That is not carelessness. It is what happens when the answer is produced by
judgement over whatever happened to be in context, because context changes and
judgement follows it.

The user experiences this as being unable to trust anything you say. They are
right to, and the fix is not to try harder. It is to move the answer out of your
judgement and into a rule that produces the same output from the same data.

One founder put the failure exactly: "you do research, you conclude something,
then you look at more research, then change your mind. you have no baseline. so
you just make it up every single time."

## When this applies

Reach for it when any of these is true:

- The same question has had two or more confident, different answers.
- The user says you contradict yourself, or asks what your baseline is.
- A recommendation rests on a number from a vendor's tool that nobody has ever
  checked against anything.
- You are about to rank things (keywords, channels, features) by reasoning.
- New data keeps arriving and each batch feels decisive.

It does not apply to one-off factual lookups, or to genuinely new questions with
no prior answer to drift from.

## The five parts

A baseline is not a document of conclusions. It is four mechanical parts plus a
rule about who may change them.

### 1. A fixed scoring rule, preferably somebody else's

Write the ranking as an arithmetic formula over named inputs. Prefer a formula
published by an outside source over one you invent, for one reason that has
nothing to do with it being better: **a formula you invented is a formula you can
quietly adjust**, and the user cannot tell the difference between you refining it
and you rationalising a new favourite answer.

If the outside source publishes more than one version, that is not a problem to
resolve by taste. Test them (part 4).

### 2. The subjective inputs frozen in a file, with a date

Most scoring rules need at least one human judgement, like how relevant a thing
is to this product. Put those numbers in their own file, date them, define the
bands they come from, and write at the top: **change a number only with a stated
reason and a date, never to make a favoured option win.**

This is the part that actually stops the drift. The formula was never the problem;
the problem was re-deriving the inputs each time with a different mood.

### 3. An instrument whose limits you have validated

You will need to measure something at scale, and the cheap way to measure it is
usually an approximation of the expensive way. **Validate the cheap instrument
against the trusted one on one case before using it on a hundred, and write down
what it is not good for.**

A worked example. A free public search endpoint returned substantially the same
set of competing apps as the paid ranking tool, with correct numbers attached,
but in a different order: it placed one app second that the paid tool did not
show at all, and omitted two the paid tool did. So it is sound for "who competes
here and how big are they" and must never be used for "who ranks where". Stating
that limit in the script's own comments is what stops the next session using it
for the wrong question.

### 4. Falsification thresholds, written before the test runs

For every input you are trusting, name the quantity that would show it is
informative, the threshold it must clear, and what you will do if it fails.
Write all of that down **before** running the test, in the script, so the result
cannot be reinterpreted into a pass.

The worked example again: "does this vendor's difficulty score predict anything
real? Test it against an independently measured quantity. Falsified if the rank
correlation is below 0.4, in which case the vendor score is near noise for us and
the measured quantity replaces it." It came back at 0.788 and monotonic across
every band, so it passed, and that pass means something because it could have
failed.

Expect to be wrong about which way a test will go. In the same session the
assumption that a multiplicative formula would beat an additive one was tested
and lost, 0.552 against 0.665. Being tested and losing is the skill working.

### 5. Two scores, never one, when attractiveness and feasibility differ

The most common silent error in a ranking is folding "how good would this be" and
"could we actually do it" into one number. They are different questions, they are
measured differently, and the second one is a gate rather than a term in a sum.

Keep them separate and make the feasibility check mandatory. In the worked
example, even the better of the two published formulas separated achievable
options from impossible ones at only 0.665, where 0.5 is a coin flip. That is the
argument for the gate: **a high attractiveness score is never sufficient on its
own**, and discovering that is only possible once the two are measured apart.

## How to do it

1. **Name the recurring question** and find every previous answer to it. Those
   answers are the evidence that a baseline is needed, and the list of things it
   will supersede.
2. **Find an outside scoring rule.** Search for a published method before
   inventing one. Note every version it publishes.
3. **Write the inputs file** and freeze the judgements, with bands and a date.
4. **Write the scorer as a script**, not as a table in a document. A script
   reruns; a table rots. Have it read the measured data from wherever it already
   lands, so the baseline updates when the data does and not otherwise.
5. **Validate the instrument** on one case against a trusted source. Write the
   limit into the script's comments.
6. **Write the validation script** with thresholds stated in its own comments,
   and run it. Report n, the statistic, the threshold, and the verdict.
7. **Fold the validated result back in.** If an input failed, replace it. If a
   feasibility gate exists, make it change the tiers.
8. **Write the baseline document**, which carries: the vocabulary, the formula
   and its source, the inputs and where they live, the validation results, what
   the baseline currently says, **and a list of the decisions it supersedes so
   they cannot be resurrected**.
9. **Point everything at it.** The project's rules file, and any older document
   that used to hold the answer, should say the ranking lives in the baseline now.

## The rules that go in the finished document

Put these in the baseline file itself, because the next session reads that and
not this skill.

1. Check the feasibility gate by hand before acting on any item. The score
   cannot see it.
2. Never quote a number from the baseline from memory. Re-run it and say the
   date.
3. Do not change a frozen input to win an argument. Changing one changes every
   ranking derived from it.
4. One position at a time. A new measurement updates the baseline. It does not
   start a fresh opinion in conversation.
5. Record superseded decisions with the reason and the date.

## What this skill will not do

- It will not make a wrong formula right. It makes a formula's output stable and
  its failures visible, which is a different and more useful thing.
- It will not remove judgement. It moves judgement into a named, dated, reviewable
  file instead of leaving it implicit in each session's reasoning.
- It will not tell you the answer is correct. A baseline that passes its own
  validation can still be measuring the wrong thing, which is why the superseded
  list and the stated thresholds matter.
