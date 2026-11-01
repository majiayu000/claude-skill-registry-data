---
name: mockup-review
description: "Reviews a built enclosure mockup, visual or performance, against the documents rather than against how it looks: establishes what this mockup was built to prove before anyone walks up to it, works the observation in a fixed order so the buildable-but-wrong conditions get seen, separates what the mockup demonstrated from what it merely did not contradict, and records what becomes the accepted standard for the rest of the work. Trigger on \"mockup review\", \"reviewing the visual mockup\", \"performance mockup results\", \"what do we check at the mockup\", \"mockup punch list\", \"mockup-review\", or a mockup photographed or described with a request for what to look at. Carries no tolerances, no test criteria and no acceptance thresholds; every one of those comes from the specification. It is not a test report, does not witness testing, does not accept or reject on the Architect's behalf, and does not replace the enclosure consultant or the Architect of Record."
license: MIT
metadata:
  title: "Mockup Review"
  summary: "Review a built mockup against what the documents actually asked for"
  discipline: "envelope-performance"
  tags: "Review"
---

# Mockup Review

A mockup is the only chance to see the assembly built by the people who will
build it, with the materials they will use, before the decision costs a facade.
It is usually wasted twice: once by reviewing it against appearance instead of
against the documents, and once by never writing down what it established.

## Scope and limits — read first

**What this does.** Establishes what the mockup was built to prove, from the
specification and from the questions the design left open. Runs the observation
in a fixed order so that conditions which are buildable but wrong get seen
rather than admired. Separates three outcomes that get merged: what the mockup
demonstrated, what it failed, and what it simply did not address. Then records
what has become the accepted standard.

**What this does not do.**

- **It carries no tolerances and no acceptance criteria.** Joint widths,
  alignment tolerances, colour range, water test pressures and durations,
  air leakage limits: all specification text you quote. Without it, the review
  reports observations and no verdicts.
- It is not a test report and it does not witness testing. Where performance
  testing is involved, the testing agency's report is the record; this reads
  that report against the specification.
- It does not accept or reject. Acceptance is a contractual act by the Architect
  of Record. This produces the observations and the reasoning behind them.
- It does not review shop drawings. Run `curtain-wall-submittal-review` or
  `submittal-review` for those, before the mockup, because a mockup built from
  unreviewed shop drawings tests the wrong thing.
- It does not design a fix. Where something fails, it records what was observed
  and what the documents required. What to change is a design decision.
- It does not replace the enclosure consultant or the Architect of Record.

**What you need before starting.** The specification sections covering the
mockup, quoted. The approved shop drawings the mockup was built from. What kind
of mockup it is: visual, performance, or both. Photographs or a site visit.
Any test reports. The list of open questions the design team wanted answered.

## Workflow

### Step 1. Establish what this mockup is for, before looking at it

Ask, in one message:

> 1. What does the specification say this mockup has to demonstrate? Quote it.
> 2. Visual, performance, or both? If performance, which tests, and have they
>    been run?
> 3. Which shop drawings was it built from, and were those reviewed?
> 4. What did the design team want to learn from it? List the open questions.
> 5. Is this mockup the accepted standard for the work, or a trial?
> 6. Who was present, and when?

The list in question 4 matters more than it looks. A mockup reviewed without it
becomes a hunt for defects, and the questions the mockup was actually built to
answer go home unanswered.

### Step 2. Observe in a fixed order

Appearance last, deliberately. Work the order:

1. **What is behind.** Control layers, where visible or where a section was left
   open. If nothing was left open, record that the mockup cannot demonstrate
   them and that this was a decision.
2. **Junctions and terminations.** Every place the assembly stops or meets
   something else. Same list the design skills use: head, jamb, sill, base, top,
   corners, penetrations, movement joints.
3. **Sequence evidence.** What the build order was, and whether the laps run the
   way the drawings show. Ask the trades; they will tell you, and the answer is
   often not what the drawing shows.
4. **Workmanship in the field.** The repeating condition, done at the pace it
   will be done at.
5. **Appearance.** Colour, alignment, reflection, how it reads at distance and
   in different light.

Record each observation with where it was seen and what document clause it
relates to, or `no clause identified`.

### Step 3. Sort every observation into three outcomes

| Observation | Where | Clause | Demonstrated / Failed / Not addressed |
|---|---|---|---|

The third column is the one that gets skipped and it is the most useful.
**Not addressed** means the mockup did not put the question to the test, which
is different from passing. A mockup with no rain on it has not demonstrated
water tightness, however good it looks.

Count each category and report the counts.

### Step 4. Record what has become the standard

If this mockup is the accepted standard for the work, say precisely what about
it is the standard and what is not. Colour range, joint appearance, workmanship
level, sequence: name each explicitly.

Anything not named here will be argued about later, and the mockup will be gone
or weathered by then. State how the standard is being preserved: retained on
site, photographed, sampled.

### Step 5. Report

- The three counts, with **not addressed** first.
- Each failed observation with what was seen and what the quoted clause required.
- Each not-addressed item with what it would take to address it, and whether a
  second mockup or a test is proposed.
- What has become the accepted standard, itemised.
- What the design team's open questions got answered, and which did not.

Close with the standing limits: this is not acceptance, no criteria were
supplied beyond what was quoted, and performance claims rest on the testing
agency's report and not on this review.

### Step 6. Save, if asked

Ask whether to write the review to a file and where, and write it directly,
tables and photograph references included.

## Rules

- **Never supply a tolerance or an acceptance criterion.** They come from the
  specification, quoted.
- Establish the purpose before the first observation. A review that starts at
  the mockup starts in the wrong place.
- Appearance is reviewed last, every time.
- Report **not addressed** before **failed**, and never fold it into **passed**.
- Every observation carries a clause reference or the words `no clause
  identified`.
- Never write the words accepted or rejected. That is the Architect of Record's
  act.
- Say on every run that performance rests on the test report, not on this.

## Anti-patterns

- Reviewing the mockup against the rendering.
- Treating an absence of visible defects as a demonstration of performance.
- Reviewing a mockup built from shop drawings nobody reviewed.
- Recalling a joint tolerance or a colour range because the figure is common.
- Letting the trades' description of the build sequence go unrecorded because
  the drawing shows something else.
- Ending without naming what has become the standard.
- Quoting a specification clause from memory rather than from the section
  supplied.
- Proposing the fix inside the review.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
