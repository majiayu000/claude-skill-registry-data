---
name: defect-escape-taxonomy
description: "Classifies a defect that reached production into one of three root gap categories (test gap, process gap, tooling gap) and one of thirteen sub-patterns, applying the earliest-layer rule: the category is the earliest layer that should have caught the defect, expressed as a property of the system and never of a person. Each sub-pattern carries the typical prevention fix, so the finding names an actionable class of gap. Rejects blame language and generic prevention assets such as 'add more tests'. Does not triage or prioritize the defect, does not write the missing test, and does not run a full incident postmortem. Use when a defect has been confirmed in production and the team needs to name which class of gap let it through before deciding what to build."
---

# defect-escape-taxonomy

## What this classifies

A defect is "an imperfection or deficiency in a work product where it does
not meet its requirements or specifications or impairs its intended use"
([ISTQB, defect](https://glossary.istqb.org/en_US/term/defect)). When a
defect reaches production, the interesting question is not what the defect
was. It is which checking activity was supposed to stop it and did not.

ISTQB has a formal term for exactly this: an **escaped defect** is "a defect
that is not detected by a test activity that is supposed to find it"
([ISTQB, escaped defect](https://glossary.istqb.org/en_US/term/escaped-defect)).
That definition is the whole skill in one sentence. Classification means
naming the test activity that was supposed to find it, then naming why that
activity did not.

The three categories and thirteen sub-patterns below are a **practitioner
taxonomy**, not a standard. ISTQB and ISO/IEC/IEEE 29119 define the
vocabulary (defect, escaped defect, root cause, quality gate) but neither
publishes this three-way split. Treat the categories as a working
classification your team can amend, and treat the cited definitions as
fixed.

The output of this classification is a **root cause** in the ISTQB sense:
"a source of a defect such that if it is removed, the occurrence of the
defect type is decreased or removed"
([ISTQB, root cause](https://glossary.istqb.org/en_US/term/root-cause)).
Note "the defect type", not "the defect". A correct classification is one
that, acted on, prevents the next defect of the same shape.

## What this skill owns, and what it deliberately does not

Owns: naming the **class of gap** that allowed one already-confirmed
production defect through, so the class is actionable.

Does not own:

| Not this | Why it is separate |
|---|---|
| Triaging the defect (severity, priority, assignment) | Triage decides fix order. Classification runs after the fix is understood and changes nothing about fix order. |
| Writing the missing test or config change | Classification names the shape of the missing asset. Building it is a coding task with its own review. |
| Running a full incident postmortem | A postmortem covers timeline, detection, mitigation, customer comms, and action items across the whole incident. This covers one question inside it: which layer should have caught it. |
| Reproducing the defect | Classification takes a confirmed, understood defect as its input. If nobody can yet say what broke, classify nothing. |

The boundary test: if the answer changes the **fix**, it is not this skill.
If the answer changes **which checking layer the team invests in next**, it
is.

## The blameless constraint

This is a hard constraint on the output, not a tone preference.

An escape analysis that names a person produces silence in the next one.
Google's SRE Book states the mechanism directly: "If a culture of finger
pointing and shaming individuals or teams for doing the 'wrong' thing
prevails, people will not bring issues to light for fear of punishment,"
and warns that blame risks "a culture in which incidents and issues are
swept under the rug, leading to greater risk for the organization"
([Google SRE Book, Postmortem Culture](https://sre.google/sre-book/postmortem-culture/)).
The same chapter sets the standard a finding must meet: "For a postmortem
to be truly blameless, it must focus on identifying the contributing causes
of the incident without indicting any individual or team."

The productive reframing is also from that chapter: "You can't 'fix'
people, but you can fix systems and processes to better support people"
([Google SRE Book, Postmortem Culture](https://sre.google/sre-book/postmortem-culture/)).
Every category below is therefore a statement about a system. "Test gap"
means the suite lacked a case. It does not mean an author forgot one.

**"Earliest layer that should have caught it" is a statement about the
system, not about who was on duty.** The word "should" attaches to the
layer, never to a person. If a sentence in the finding could be rewritten
with a name in it and still parse, the sentence is wrong.

Two mechanical habits enforce this in the text:

1. **Write the layer as the grammatical subject.** Not "the author did not
   add a boundary test", but "the unit suite had no boundary case for empty
   input". Same fact, and only one of them is actionable.
2. **Ask how, not why.** Etsy's Debriefing Facilitation Guide: "steer clear
   of asking people 'why' and substitute 'how' instead. Asking 'how'
   enables us to hear other people's stories. Asking 'why' creates a story
   of our own and tends to elicit only the evidence that supports our story"
   ([Etsy, The Art of Asking Questions](https://github.com/etsy/DebriefingFacilitationGuide/blob/master/guide/05-the-art-of-asking-questions.md)).
   The same guide warns that "why" produces "a fabricated cause-and-effect
   chain that gets created after the fact by virtue of hindsight", which is
   precisely the artifact a blameful escape report ships.

For facilitation technique, the Google SRE Workbook's postmortem chapter
([Postmortem Culture: Learning from Failure](https://sre.google/workbook/postmortem-culture/))
extends this material with organizational adoption patterns.

## The classification rule

**Classify by the earliest layer that should have caught the defect.** The
categories are mutually exclusive at root level, and earliest wins.

A defect can plausibly be attributed to several layers at once. A null-input
crash might have been caught by a unit test, by an integration test, by a
staging soak, or by a runtime assertion. Attributing it to all four produces
four vague action items and no change. Attributing it to the earliest layer
produces one cheap, fast, specific check.

Apply the rule in this order and stop at the first "yes":

1. **Could an ordinary test at the cheapest available level have caught
   this, with the tooling the team already runs?** If yes, and no such test
   existed, it is a **test gap**. Stop.
2. **Did such a test exist, but not execute in the path that gates a
   release?** Then it is a **process gap**. Stop. The relevant concept is
   the quality gate: "a milestone at which a decision about proceeding to
   the next phase is taken based on predefined quality criteria"
   ([ISTQB, quality gate](https://glossary.istqb.org/en_US/term/quality-gate)).
   A test that runs but does not gate is not a quality gate.
3. **Otherwise: no test at any level the team can currently write would
   have caught it.** It is a **tooling gap**. The remedy is a different
   test type, a different environment, or a runtime check, not another
   test case.

Step 3 is a genuine terminal state, not a fallback for hard cases. If "could
a test have caught this?" is answered "no, no test ever could", classify
tooling gap and recommend observability, not a test.

### Rule of thumb for the boundary that gets confused most

Test gap and tooling gap both feel like "we needed a test". The
discriminator is capability, not effort:

- The team **can** write the test today with what is installed, and simply
  has not: **test gap**.
- The team **cannot** write the test today because the layer, environment,
  or determinism required does not exist in their toolchain: **tooling
  gap**.

"Hard to write" is still a test gap. "Impossible to write with these tools"
is a tooling gap.

## Category 1: Test gap

The team had the right framework, the right CI wiring, and the right
process. **No test existed for this specific case.**

| Sub-pattern | Typical fix |
|---|---|
| Edge case not exercised | Add a unit test for the edge case. |
| Untested input domain (empty, null, unicode) | Add boundary or property-based tests. |
| Untested output channel (HTTP error path, fallback UI) | Add a test for the alternate path. |
| Untested integration between two units | Add an integration test exercising the seam. |

Signature of this category: the fix commit changes production code, and the
matching test file already exists and passes both before and after, because
it never covered the input in question.

## Category 2: Process gap

The right test **existed** and **did not run in the gating path**.

| Sub-pattern | Typical fix |
|---|---|
| Test marked skipped or quarantined | Triage it back in under a quarantine policy with a hard expiry, so quarantine cannot become permanent. |
| Test on a non-blocking CI job | Move it to the blocking workflow. |
| Test ran but its result was ignored | Audit the pipeline and ensure exit codes propagate to the gate. |
| Required env var or fixture present only in some environments | Standardize test setup across environments. |

Signature of this category: a test that would have failed against the
introducing commit is already in the repository. Check for `skip`, `only`,
`xfail`, `Ignore`, `continue-on-error: true`, and jobs absent from the
required-checks list before concluding test gap.

Findings in this category are the ones most at risk of drifting into blame,
because a human decision is visibly upstream of every one of them (someone
skipped the test, someone marked the job non-blocking). Write the standing
state, not the decision: "the quarantine list has no expiry mechanism, so
entries persist indefinitely" is actionable; naming who added the entry is
not.

## Category 3: Tooling gap

The test **could not have been written** with the current toolchain. It
needs a different layer, a different environment, or a runtime mechanism.

| Sub-pattern | Typical fix |
|---|---|
| Race condition that appears only under real concurrency | Add chaos or load testing. |
| Memory or file-descriptor leak that manifests over hours | Runtime monitoring, not a test. |
| Browser-specific or device-specific behavior (one engine, one OS) | Expand cross-browser or cross-device coverage. |
| Production-data-only defect (shape or scale absent from fixtures) | Anomaly detection or sampling-based monitoring. |
| Configuration error (env var typo, missing secret) | Startup-time configuration validation. |

Signature of this category: writing the reproducing test requires
provisioning something the repository does not have. When the honest
prevention asset is an alert threshold rather than an assertion, this is the
category.

## Procedure

1. **Confirm the input is a defect, not a change request.** A behavior the
   system was never specified to have is not an escape. Classify nothing.
2. **State the checking activity that should have caught it**, in one
   sentence, with the layer as the subject. This is the sentence the whole
   finding hangs on.
3. **Walk the three-step classification rule above** and stop at the first
   "yes". Record the category.
4. **Select exactly one sub-pattern** from that category's table. If none
   fits, say so explicitly rather than forcing the nearest match, and
   propose the sub-pattern the taxonomy is missing.
5. **Name the prevention asset concretely**: a specific test file plus test
   name, a specific config key plus value, or a specific named metric plus
   threshold. The sub-pattern's "typical fix" column is the shape, not the
   answer.
6. **Verify the asset against the introducing commit.** State when the
   proposed check would have failed. An asset that would have passed
   against the buggy code is not a prevention asset.
7. **Run the blame scan** on the finished text. Search for personal
   pronouns, names, handles, and the words "should have", "forgot",
   "failed to", and "careless". Every hit is a rewrite, not a softening.

## Rejected findings

These four shapes are rejected outright.

| Rejected shape | Example | Why it fails |
|---|---|---|
| **Blame language** | "Engineer X should have written this test." | Produces silence in the next analysis ([Google SRE Book, Postmortem Culture](https://sre.google/sre-book/postmortem-culture/)). You cannot fix people; you can fix systems. |
| **Generic prevention asset** | "Add more tests." "Be more careful." "Improve code review." | Not a finding. It survives any defect unchanged, which is how you know it identifies nothing. The asset must be a named file, a named config key, or a named metric. |
| **Test gap conflated with tooling gap** | Filing a race condition that needs a load harness as "missing unit test". | Sends the team to write a test that cannot exist, and the same defect escapes again. |
| **Missing production-state evidence** | No first-observation timestamp, no time-in-production, no affected-user estimate. | These bound how much the prevention asset is worth. Without them the finding cannot be prioritized against any other work. |

Note the second row carefully: **"add more tests" and "be more careful" are
not findings.** They are the generic-prevention-asset anti-pattern in its
two most common disguises, one technical and one behavioral. "Be more
careful" additionally fails the blameless constraint, because carefulness
is a property of a person.

## Expected output shape

One markdown document per escaped defect, stored together under a stable
directory (for example `docs/escape-defects/`) with a date-prefixed,
slugified filename so the set reads as a trend. The full per-defect
template - fields table, section skeleton, and the load-bearing
**Prevention asset** section (empty or generic means the document is not
finished) - is in
[references/escape-defect-document-template.md](references/escape-defect-document-template.md).

## Worked example: test gap

**Input.** Defect #1234: `calculateTotal` throws on an empty cart. The fix
changed `src/checkout/total.ts` line 23. The existing test file
`src/checkout/total.test.ts` covered only populated carts.

**Step 2, the anchor sentence.** The unit suite for `calculateTotal` had no
case for a cart with zero items.

**Step 3, the rule.** Could an ordinary unit test with the installed runner
have caught this? Yes. Did one exist? No. First "yes" at step 1, so **test
gap**. Stop. Do not also file it as a missing E2E case, even though an E2E
checkout test would also have caught it. The unit level is earlier and
cheaper.

**Step 4, sub-pattern.** Edge case not exercised.

**Step 5, prevention asset.** A concrete case appended to the existing
file:

```typescript
import { describe, it, expect } from 'vitest';
import { calculateTotal } from './total';

it('returns 0 for an empty cart (regression for #1234)', () => {
  expect(calculateTotal({ items: [] })).toBe(0);
});
```

**Where it lives.** `src/checkout/total.test.ts`.

**Step 6, verification.** This case fails against `abc1234`, the
introducing commit, and locks empty-cart behavior in against future
refactors. Confirming that the fix removes the failure is
confirmation testing: "a type of change-related testing performed after
fixing a defect to confirm that a failure caused by that defect does not
reoccur"
([ISTQB, confirmation testing](https://glossary.istqb.org/en_US/term/confirmation-testing)).

**Step 7, blame scan.** No names, no pronouns, no "should have". The
finding reads as a property of the suite.

### The other two categories in one line each

- **Process gap.** The prevention asset is a CI configuration diff (move
  the job to the required-checks list, or return a quarantined test to the
  gating suite under an expiry policy), plus a populated
  `## Process changes` section.
- **Tooling gap.** The prevention asset is a named metric and threshold
  rather than an assertion. For a multi-hour heap leak, that is a
  process-heap-usage metric with a rolling one-hour window alert, and
  `## Open questions` carries the tradeoff the team must still decide, such
  as whether to also fund a soak test in CI.

## Limitations

- **The taxonomy is a convention.** Three categories and thirteen
  sub-patterns are a working split, not a standard classification. ISTQB
  supplies the terms cited above; the categories are the practitioner
  layer on top. Teams should add sub-patterns their history demands and
  record what they added.
- **One defect at a time.** Category counts become meaningful only in
  aggregate. A single tooling-gap finding says nothing about the
  toolchain; twelve of them in a quarter does.
- **Classification is not measurement.** If the team wants a number for
  how much is escaping, that is a separate metric, defect detection
  percentage: "the number of defects found by a test level, divided by the
  number found by that test level and any other means afterwards"
  ([ISTQB, defect detection percentage](https://glossary.istqb.org/en_US/term/defect-detection-percentage)).
  This classification explains individual escapes; it does not count them.
- **A defect with no understood cause cannot be classified.** Root cause
  analysis, "a process used to identify the root cause of a defect"
  ([ISTQB, root cause analysis](https://glossary.istqb.org/en_US/term/root-cause-analysis)),
  runs first. Classifying an unexplained defect produces a guess wearing a
  category label.
