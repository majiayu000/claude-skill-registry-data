---
description: A reusable decision procedure, and a copyable prototype for the guard that encodes it — derive the population, set one threshold by what being wrong costs, name the offender, and break it once to prove it can fail. Use when writing a check, guard, gate or validation of any kind, or when deciding whether something is safe, done, duplicated, stale, or worth doing — so the shape is the same every time instead of re-derived per session.
---

# Decide from counted evidence, not from an impression

**Code calculates. A model reasons. This decides.** The pattern is borrowed openly from the
decision models now being built for agent systems, and one thing is deliberately different: the
confidence here does **not** come from a model. It comes from evidence you counted. Nothing in this
procedure calls out, and nothing about it needs a network.

That difference is the whole reason it can be trusted offline — and the reason step 3 is the one
that cannot be skipped.

---

## 1 · Name the decision, and what being wrong costs

Write both before looking at anything. The cost sets the threshold; there is no global one.

> *"Is this file safe to edit?" Being wrong means the edit is silently discarded.*
> *"Does this component already exist?" Being wrong means a wasted afternoon, recoverable.*
> *"Is this a credential?" Being wrong once is the whole product failing.*

**One threshold per action, scaled to that cost.** A single number for the whole system is how a
gate ends up too strict for cheap mistakes and too loose for expensive ones.

## 2 · Write the questions before you look

Each question gets a **type**, and the type is one of three:

| type | shape | example |
|---|---|---|
| **choice** | one value from a set you named | generated · hand-written · cannot tell |
| **count** | a number, with what it is out of | 26 of 28 planted credentials caught |
| **yes/no** | with the evidence that decides it | is a test command in this session's log? |

**Never a free-prose answer.** Prose cannot be thresholded, cannot be compared to last week's, and
cannot be checked by anybody else. If a question can only be answered in prose, it is not a
decision — it is a discussion, and it belongs with a person.

## 3 · Answer each from something you counted — and record the count

This is the step that makes the rest honest.

> **A number you did not count is an impression wearing a number's clothes.**

Where the counts come from, offline:

| question shape | what counts it |
|---|---|
| is this name used anywhere else | `chamnan-where <name>` — uses, not lines that mention it |
| what breaks if this changes | `chamnan-impact <file>` — importers, covering tests |
| has this been decided before | `chamnan-recall <subject>` |
| does the behaviour hold | the check, run — and **seen to fail** before it is believed |
| does it hold on somebody else's code | the corpus, with the count it returns |

**Record what you EXAMINED, not only what you found.** "No references" from a scan that skipped a
file is not the same answer as "no references", and the difference is invisible unless the skipped
count is on the line. Every report in this procedure carries both numbers.

## 4 · Three bands, and the middle one is not a failure

| band | what happens |
|---|---|
| the evidence is complete and agrees | **act** |
| the evidence is partial, or two signals disagree | **say so and continue** — name what is missing |
| the evidence cannot be counted, or being wrong is expensive | **hand it to a person** |

**The bottom band is an answer.** Routing a decision to a human is the procedure working, not the
procedure giving up — and pretending to a number you could not count is the only real failure here.

## 5 · Test the threshold before trusting it

A threshold nobody has tested is a guess with a number on it.

Find a case where the answer is already known and check the band lands right. Where there is no
such case, **build one**: a repository that has the defect, a file that names a path that has gone.
Then break it the other way and confirm the band moves.

**A credential-shaped fixture is the one case with a hard boundary, and it is not a style rule.**
Build it in a throwaway directory outside any repository, or in a corpus repository that exists for
the purpose — **never in a tracked file, and never anything that can be pushed.** GitHub's secret
scanning forwards a live-looking key to the provider within minutes of it reaching a remote, and the
account that owns it is marked. A test fixture is not worth that, and the damage is not yours to
undo. If a threshold can only be tested with a real-looking key, test it against a corpus somebody
built for testing rather than against the repository you are working in.

> A threshold that has never been seen to reject anything has not been tested, only run.

## 6 · Log the decision, then compare it with what actually happened

Write down the question, the count, the band and what was done. Later, check whether the decision
was right. **A threshold that is never compared with the outcome drifts silently**, and the drift is
only visible against a record.

---

## 7 · Encode the decision in a guard, so nobody decides it again

Steps 1-6 are how a decision gets made once. This is how it stops costing anything afterwards.

A model can reason its way to a good judgement every time — and pays for it every time, in the
thinking and in the code it writes to express it. Where the answer is already settled, the cheap
form is a guard that carries the decision, not a person or a model re-deriving it.

**The prototype. Copy it and change the subject; do not re-invent the shape.**

```python
# 1 · the population, DERIVED — never a list you typed
subjects = scan(where)                    # glob, walk, parse — anything but a literal list

# 2 · the measurement is a failure when it finds nothing
assert_that("the scan found the things it judges", len(subjects) >= floor,
            saw=f"{len(subjects)} found — every assertion below is vacuously true on zero, "
                f"which is how a broken measurement reports itself as a pass")

# 3 · one threshold, set by what being wrong costs (step 1), stated here and not in a model
offenders = [s for s in subjects if not holds(s)]

# 4 · the message says what to DO, and names the offender
assert_that("<the property, as a sentence that is true when it passes>", not offenders,
            saw=f"{offenders} — <what goes wrong for the reader if this is false>")
```

**Six decisions it encodes, so they are made once and not per use:**

| in the prototype | the decision it carries |
|---|---|
| `scan(where)` | derive the population; a typed list forgets the member added tomorrow |
| `len(subjects) >= floor` | an empty population is a failure, not a quiet pass |
| `offenders` as a list | report WHO, not just that something is wrong |
| `saw=` | the reader acts without opening the guard |
| the name as a true sentence | it reads as a property, not as a test id |
| threshold in the code | not in a prompt, not in a model, not re-argued |

**Then the one step that makes it real: break the thing and watch it go red.** A guard never seen
to fail has been run, not tested. If breaking it is impractical, assert the inverse in the same
breath — `assert_that("...", A and not B)` — so a change in either direction is caught.

**And the half everybody skips: show it can go GREEN for the right reason.** Red proves the guard
reacts to something; it does not prove it reacts to the thing you meant, and a guard that can only
ever fail is indistinguishable from a broken measurement. So keep a known-good case beside the
broken one and check it passes — the same shape a benchmark calls an *oracle*, a solution shipped
with the task so that "nobody can pass this" and "the scorer is broken" stop looking identical.

    assert_that("<the property>", holds(known_bad) is False)   # it can go red
    assert_that("<the property>", holds(known_good) is True)   # ...for the right reason

The cheap version costs one extra line: whenever you build a fixture that the guard should reject,
build its twin that it should accept, and assert both.

Four traps, each of which has produced a guard that passed while measuring nothing:

- **searching a whole document** for a name that appears in it twice — slice to the region first
- **reading a value before the thing that sets it** — compute into a name, then assert
- **pinning the spelling of an implementation** instead of its behaviour — run it and read the
  outcome; pin text only where there is no runtime signature, and say why
- **a mutation that changes no verdict** — it proves nothing; find the case that discriminates

## What this is not

**It is not a gate that blocks.** Every decision here ends in an action, a notice, or a person —
never in a refusal the reader cannot override. A tool that stops work on a number it could not
fully justify will be turned off, and then none of its decisions matter.

**It is not for choices with one obvious answer.** Running six steps on something a glance settles
is overhead dressed as rigour.

**It is not a confidence generator.** If step 3 has nothing to count, the honest output is the
bottom band. Inventing a number to get past it is the one thing this procedure exists to prevent.
