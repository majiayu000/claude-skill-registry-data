---
name: debug
description: Use when a bug, an unexpected test failure or a repeated error shows up during the code step, trace the cause backwards to its origin before proposing a fix, then make the bug structurally impossible rather than locally absent.
---

# debug

Support block for step 6 (`code`). Find the **root cause**, not the symptom, and know the difference:
the place the error appears is almost never the place it started.

## When
During `code`, at the first unexpected error or the second identical failure.

## Steps

### 1. Reproduce, then form one hypothesis
1. Reproduce reliably: an exact command plus the minimal input. A bug you can't reproduce on demand
   can't be shown fixed either. That command is the **feedback loop**, and it comes before any hypothesis:
   `references/05-feedback-loop-first.md` says what it must satisfy, how to build, tighten and minimise it, and how
   to tag temporary logs so they are all removed. The loop is the precondition of the single hypothesis below, not
   another method.
2. State **a single** hypothesis and verify it (a targeted log or test) **before changing anything**.
   Changing code to see what happens is how a second bug gets introduced next to the first.
3. When the cause is still open after a first round, or several people or agents investigate, test competing
   hypotheses one at a time with criteria written before looking, and arbitrate on evidence:
   `references/07-competing-hypotheses.md`. It extends this rule; it does not allow several fixes at once.

### 2. Trace backwards to the origin
The error surfaces deep in the stack; the instinct is to fix it there, which fixes the symptom.

1. **Note where it actually appears**: the real message, the real location.
2. **Find what directly produced it**, then ask **what called that**, then its caller. Follow the
   chain, not the intuition.
3. **Follow the data, not just the calls**: where did this invalid value enter the system? Usually
   several frames above where it finally caused damage.
4. **Stop at the original trigger**: the point before which nothing else caused it. Before editing,
   grep every caller of the function you are about to change and fix at the point they all route through;
   patching only the path the report names leaves its siblings broken.
5. When manual tracing stalls, **capture the call chain at the suspicious operation** rather than
   guessing: log the parameters, the surrounding context, and a captured stack trace, immediately
   before the failing call. In tests, write to stderr — a logger may be suppressed, and then you're
   debugging your own silence.
6. **When the failure crosses several components** (a pipeline, API then service then database) and the loop is
   red but no stage is named, instrument every boundary once and read the one trace to find the failing layer
   before tracing inside it: `references/06-component-boundaries.md`.

### 3. Fix at the source, then make the class of bug impossible
Fixing the origin removes this bug. Adding checks along the path removes the next one of its kind.

1. **Fix at the origin.**
2. **Validate at the boundaries the bad value crossed**: at the entry point (reject what's obviously
   invalid), and in the business logic (reject what's invalid *for this operation*, which also catches
   the path that bypassed the entry point, including via a mock).
3. **Guard the context** where the consequence was severe: an operation that must never run outside a
   sandbox refuses to, rather than trusting the caller.
4. **Add or adjust the test that captures the case** — at the origin, not at the symptom, or it'll pass
   again the day the path changes. "Adjust" means adding the case the origin fix actually introduces,
   never loosening, deleting or retargeting an assertion that already existed before this bug was
   found: a pre-existing test going from red to green because the implementation changed is the goal, the
   same test going green because its expectation moved to match the broken output is the regression this
   whole block exists to prevent — see the sharper statement of the same rule below.
5. Validate **where data crosses a boundary**, not inside every function: a check in every frame is
   noise, and noise gets deleted wholesale later.

### 4. Know when to stop
Still looping after more than 2 attempts with no progress → `escalate`. Three failed hypotheses means
the model of the problem is wrong, and more attempts inside a wrong model cost more than asking.

## Output / checkpoint
No checkpoint of its own: resumes `code`. What it owes is the chain — symptom, origin, why the origin
explains the symptom — not just a diff that makes the error stop.

## Guardrails
- **No random fixes, no retry loops.** One hypothesis at a time.
- **Never fix only where the error appeared.** If you can't say why the origin produces this symptom,
  you haven't found it, you've found somewhere the symptom disappears.
- **Never make an error quieter to make it stop**: a swallowed exception, a widened type, a removed
  assertion. Same bug, now undetectable.
- A fix with no test capturing the case is a fix that comes back.
- **A pre-existing test that fails is a verdict on the implementation, not on the test.** The fix goes
  in the code being debugged. Editing the failing test itself is legitimate only to add the new case a
  genuine spec change introduced — never to loosen, delete, comment out, or change an existing
  assertion's expected value so it matches what the code currently does: that specific move is how a
  regression ships behind a green suite, silently, which is exactly the failure mode `gate`/`galadriel`
  exist to catch and this rule exists to prevent from reaching them in the first place. If the test is
  genuinely wrong (the spec changed, the case it captures no longer applies), that's a decision to
  surface explicitly and route back through `tdd`/`dozer`, never a silent edit inside this loop.

## Origin
Native / internal `systematic-debugging`, rewritten. Sections 2 and 3 are rewrites of
`debugging/root-cause-tracing` and `debugging/defense-in-depth` from a market skills repository (the
companion of the upstream this framework responds to): the backwards call-chain walk, the
stack-capture instrumentation and the layered-validation model are theirs, and they filled a real hole
— our own version said "fix the cause, not the symptom" while offering no technique for finding it.
The "validate at boundaries, not in every frame" limit and the three-failed-hypotheses stop rule are
ours; the source is deliberately silent on over-validation, and unqualified layering would collide
with our standing preference for less logic to maintain.

The explicit no-test-tampering rule (§3.4, Guardrails) added 2026-08-11: a gap named directly by the
operator, not sourced from any catalogue — the concrete failure mode of a coding agent making a red
test green by editing the test's expectation instead of the implementation, which reports a regression
as a passing suite. `tdd`'s existing guardrail already forbade writing a weak test in the first place;
this is its sibling for the later moment, when a pre-existing (and correct) test gets edited instead of
the code once it's inconvenient. Same rule stated for the build agents themselves (`code`'s own
guardrails, and `neo`/`morpheus`/`trinity`'s), so it's caught before the diff, not only after it at
`galadriel`. A rule alone holds until it's inconvenient, so it's also mechanical now:
`hooks/guard-test-changes.sh` blocks the edit at the tool layer when a pre-existing assertion
disappears, the same "written instruction + hook" pairing as `gate`'s evidence rule.

Section 5 (`references/05-feedback-loop-first.md`: the feedback loop first, minimising, tagged logs, the correct-seam rule) was added 2026-10-19; its provenance and the reconciliation with the single-hypothesis rule are in [`references/origin.md`](./references/origin.md).

Section 6 (`references/06-component-boundaries.md`: instrument each component boundary once, locate the failing layer from the evidence) was added 2026-10-19; its provenance and what it deliberately does not duplicate are in [`references/origin.md`](./references/origin.md).

Section 7 (`references/07-competing-hypotheses.md`: competing hypotheses, the evidence protocol, arbitration) was added 2026-10-20; its provenance is in [`references/origin.md`](./references/origin.md).
