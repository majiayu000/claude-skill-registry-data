---
name: falsify
description: Required loop whenever a change has to be right — study the affected code first, write down the claim with measurable finish criteria, shrink a failing test down to the cause if nobody knows it yet, make the edit, demonstrate the intended behavior, then work hard to BREAK the edit by executing every exit from the modified code. Keeps a single audit doc per claim, logging problem, investigation, hypothesis, test plan, results and verdict each cycle so cycles can be compared side by side. Finishes with a five-part report, or with a fresh hypothesis (up to 3 cycles, after which the user chooses how many more). Reach for it when repairing a bug, chasing down a failure, answering a reviewer's comment, or handling a bug report. Feature work qualifies too, but only when pointed at a single refutable statement about the code ("turning on X never changes Y") rather than the feature as a whole — if no outcome could show that statement false, this skill does not apply.
---

# Attacking a change

Left to habit, people change code by confirming: write the edit, add tests that show it doing its job, see them turn green, and stop. That routine is how an edit that handles the scenario you pictured, yet breaks the one right beside it, reaches production. Here the habit gets reversed — **aim your effort at breaking your own edit**, and only report after it has held up.

Bug repairs are where this gets used most, so most of the examples below involve them, but nothing in the steps is specific to bugs. New features go through the identical loop, pointed at one refutable statement rather than at the feature: *turning this on never shifts an existing label*, not *the feature works*. Should you be unable to describe some outcome that would show your statement false, you have no claim, and a different tool is needed.

Work through the steps in sequence. Only step 2a may be skipped, and only when the cause is already known. Never skip step 3, and don't report until step 6 is finished.

---

## The audit doc

A run maintains **one audit doc** per claim. Each new cycle lands in it as a fresh section; older cycles stay exactly as written, never revised or removed. What this buys is comparison: if cycle 3 falls, anyone reading — the user or you — must be able to line it up against cycles 1 and 2 and see what moved and what kept breaking.

**Location:** `tmp/falsify/<ID-or-slug>.md`, relative to the repo root. Name it after the ticket or issue if one exists (`tmp/falsify/ISSUE-123.md`); if not, a brief slug describing the problem works. Git ignores `tmp/`, so none of this ever gets committed. Found an existing doc for this claim? Add the next cycle to it rather than opening a second file.

**Fill in every part as its step happens** — never reconstruct it at the end. Once the results are in, a hypothesis or test plan written down records nothing about what you expected. Guard 2 in step 6, pre-registration, is the same idea.

Every cycle contains the following parts, in this sequence:

```markdown
## Cycle N — <one-line hypothesis>

### 1. Problem
The question this cycle sets out to settle or knock down. Repeat it each cycle; if the
framing has moved since the previous one, explain the shift.

### 2. Investigation
How you tracked down the mechanism (step 2a), or "Root cause already known: <where from>".
Include the squeeze, any queries, files you looked at, and runs you did.

### 3. Hypothesis
The claim, phrased so that some outcome could show it false.

### 4. Test plan
**Happy path** — tests that demonstrate the intended work (step 3's metrics), each paired
with the outcome you expect.
**Disproof** — attacks designed to break the claim (step 6), each paired with the outcome
you expect, all drafted before any code is written. Flag later additions *post-hoc*.

### 5. Results
- **Passed:** tests that passed on the changed code, each with its result on the
  pre-change code (that's the mutation gate).
- **Failed:** tests that failed on the changed code, along with what each one exposed.
- **Unexpected:** results that broke from their predictions, and any other surprise.
  No surprises at all? Name the nearest miss.
- **Not exercised:** exits nobody ran, with the reason why.

### 6. Verdict
Held → write the report (step 7). Broken → which outcome broke it, and how the next cycle
will differ. Side findings get listed here, not pursued.
```

---

## 1. Evaluate

Take in the request, then hunt down and study the **affected code**. A request describes the goal; what actually exists can only be learned from the code.

Have no opinion until you've read it from disk. Cycles are most often wasted by designing against a picture of the code that is one version out of date.

## 2. State the problem

Describe, in one tight sentence, what you're solving.

That sentence becomes part 1 of the current cycle in the audit doc. Step 8 also comes back to it — disproofs often reveal a faulty *framing* rather than only a faulty mechanism, and nobody can spot that if the problem was never written down.

## 2a. If the mechanism is not located yet — squeeze

Moving straight from step 2 to step 3 presumes you can already point at the faulty code. When you can make it fail but can't yet say why, narrow things down mechanically instead of poking around near the symptom. That's the **Saff Squeeze**, as Kent Beck describes it: start with the failing high-level test, paste in the code it invokes, cut whatever can be cut while it keeps failing, and go again. With each pass the suspect area gets smaller, until the bug is small enough to spot.

**Hold on to both tests** — Beck's "hit 'em high, hit 'em low". The high-level one shows the problem is real and remains the acceptance evidence for step 7. The squeezed one pinpoints where the bug lives, and pinpointing is its whole job.

That has two consequences, and each matters since it runs against another rule of this skill:

- **Squeezed tests usually plant state instead of generating it.** Cutting code strips out the production path deliberately — that's the method succeeding, not failing. So on its own it can't meet step 7's every-exit requirement; some test still has to invoke the writer. See [`references/falsify.md`](./references/falsify.md#choosing-fixtures).
- **It belongs to step 5, not step 6.** Having been carved from a failing case, a squeezed test automatically fails on the pre-change code. It clears the mutation gate for free, so filing it as a disproof attempt pads the tally with no real attack behind it.

Write down what you did as part 2 of the audit doc. If you already knew the root cause, say who or what told you.

## 3. State the change and its done-metrics

Describe how the edit will work. After that, write out the **definition-of-done metrics** — at least one, often more, since a typical fix affects several behaviors.

Each metric needs to be something you can verify by executing it.

Enter the hypothesis as part 3 of the audit doc. Next comes part 4, the test plan: happy-path tests built from these metrics, and disproof attacks of the kinds described in step 6, every one paired with the outcome you expect.

**All of this happens before any code is written.** Metrics dreamed up afterward merely describe whatever the code ended up doing; they never constrained it. When some piece of the fix has no metric you can put into words, you haven't understood that piece yet.

## 4. Implement

## 5. Prove the happy path

Write tests matching **the intended work** — step 3's metrics, never simply whatever was easy to assert.

## 6. Try to disprove the change

Everything else in this skill exists to support this step. `references/falsify.md` has the full treatment; the essentials:

- Your job is attack, not advocacy. Weight matters here: **surviving one real attempt to break the edit counts five times** as much as one more passing proof.
- **Map every exit** out of the modified code, then **run** an attack down each. Exits include each branch and early return, each caller (tests too), and each way a called thing can respond: success, failure, exception, timeout, empty result, lost race. They also include retries, a message arriving twice, a concurrent worker, the next scheduled run, and anything that later reads state you wrote.
- **Code you only read proves nothing.** Conclusions you reached by reasoning alone stay unverified, and you have to say so.
- **Test the tests**: put back the naive or previous version and rerun. Any test that stays green against the unfixed code is pinning nothing.
- **One successful disproof kills the claim in its current wording.** Settings, placement and the broad approach might be salvaged, but whatever you build from them is a *brand-new* hypothesis with **no evidence carried forward**.

**Four guards against disproof theater** — attacks that never had a chance of succeeding, scored as survived. See [`references/falsify.md`](./references/falsify.md#guarding-against-disproof-theater) for the full explanation, a worked example and the table:

1. **Mutation gate.** Run every attack on the **pre-change** code as well, and report both results. Unless it fails there, it scores zero.
2. **Pre-register.** Write the attack list in step 3, as part of the test plan, while no code exists yet. Later attacks are welcome, just **flagged post-hoc**.
3. **Predict first.** Write each expected outcome down before running. A perfect prediction record means no experiment took place; name your nearest miss.
4. **Describe, don't tally.** For each attack give what it was, what it could have caught, and its pre-change result, and then name the exits you **never** ran.

When the **framing** itself is off, the four guards are useless. Give more weight to someone outside challenging the question than to one extra attack on the answer — see step 8.

**Side findings get written down, never pursued.** Other bugs you run into go into a list for the report. Leave them unfixed. Keep the scope where it is. Stay with the problem you stated.

## 6a. Record the results

Complete part 5 of the audit doc: which tests passed (plus how each did on the pre-change code), which failed, what surprised you, and what went untested. Then part 6, the verdict.

## 7. If it holds — report

Five parts, in this sequence:

1. **The requested work** — what you were asked to do
2. **The hypothesis and plan** — how you settled on the edit and carried it out
3. **The testing plan** — which exits got tested, with outcomes
4. **Gains and gaps** — what the edit achieves, and bluntly what it leaves undone
5. **Other bugs** — anything else you found

To accept the edit, **every exit must be proven**. Not a single one may be left broken. *"Works except when X"* doesn't count as finished — it's a bug you can reproduce, and it gets reported as a bug.

An exit counts as proven in one of two ways: an executed test covers it, or it is unreachable and a test pins the invariant that keeps it so (see `references/falsify.md`, "Unreachable states"). Any other exit on the *Not exercised* list blocks acceptance. Listing it is still required, but the honest status is *iterating*, not done.

Keep what you **executed** clearly separate from what you only **read**. The two must never run together.

Include the audit doc's path in the report.

## 8. If it is disproven — re-hypothesize

Come up with a new hypothesis and **go back to step 2** — not step 4. The same audit doc gets a new `## Cycle N+1` section; earlier cycles stay untouched.

The revision's first test is **the disproof that just succeeded**. Should it succeed again, drop that revision before building anything on it — you're looking at the old hypothesis in disguise. Give its `## Cycle N+1` section a verdict of disproven (it counts toward the three-cycle limit), then form a genuinely different hypothesis as the next cycle, again from step 2.

**Three cycles at most.** When a third disproof lands, **halt and give the decision to the user.** Failing three times is a signal, not bad luck. Usually it means the problem is under-specified, the constraints conflict, or a person rather than a fourth attempt should decide.

Avoid an open-ended question here — the user should be able to reply with one click. Call `AskUserQuestion` offering precisely these options:

| Option | Meaning |
|---|---|
| **Stop and return the prompt** | Wrap up. Share what the cycles taught you and hand back the current problem statement, noting each hypothesis that died and what killed it. |
| **Try 1 more time** | A single extra cycle; afterward, ask again. |
| **Try 3 more times** | Up to three extra cycles; ask again only if every one gets disproven. |
| **Try X more times** | A custom count. **Get the number through a second `AskUserQuestion`**, listing a few sensible choices and leaving "Other" free for typing one in. |

Ahead of asking, sum up in a sentence or two **the thread running through all three disproofs**, and include the audit doc's path so the user can compare the cycles. That summary is what the decision actually rests on; a bare "three attempts failed, now what?" pushes onto the user analysis you already hold.

Whatever budget the user grants, counting starts from zero and the same limit applies once it's spent — an extension never becomes open-ended.

---

## Scope

Step 7's every-exit requirement governs **the claim, not the work**. Partial coverage midway through is expected — just don't label it finished. The honest in-progress status reads *"iterating, N exits still unticked."*

**Bugs aren't the only use for this skill.** Any change meant to be correct is covered — a bug repair, a refactor, a feature, a config change. Bugs just come up most, which is why they fill most examples. With features, point the loop at one refutable statement about the code, not the entire feature — if you can't picture any result disproving the statement, it's out of scope.

---

## Where these ideas come from

**Step 2a — the Saff Squeeze.** The technique carries the name of **David Saff**, who devised it during his MIT and JUnit years; Kent Beck popularized it in the essay *"Hit 'em High, Hit 'em Low: Regression Testing and the Saff Squeeze"* (~2007). That essay is the origin of keeping both tests: one demonstrates that the bug matters, the other explains it, and you can't swap one for the other. Beck's picture — two tests converging on a single defect from opposite directions — tends to vanish when others retell it.

A machine-driven counterpart exists: **Delta Debugging**, from Zeller & Hildebrandt's *"Simplifying and Isolating Failure-Inducing Input"* (IEEE TSE, 2002). Where the squeeze trims **code** by hand, Delta Debugging bisects the **input** automatically. If the puzzle is which input sets the bug off, use Delta Debugging; if the input is known and the puzzle is which code mishandles it, squeeze.

**Everything else** is just the scientific method wearing debugging clothes. Its nearest ancestor is **Scientific Debugging** from Andreas Zeller's *Why Programs Fail* (2005): guess, predict, test, refine the guess, and keep a log throughout. Steps 2, 3, 6 and 8 implement exactly that — step 8 sending you back to the hypothesis instead of the patch comes from there too.

**Step 6's four guards mostly come from outside software**, which explains why they read so differently from the rest. Only the first, the mutation gate, is a software-testing idea, and even that one is turned on the disproof attempts rather than the code:

- **Mutation gate.** Borrowed from mutation testing (DeMillo, Lipton & Sayward, *"Hints on Test Data Selection"*, 1978), except that here your disproof attempts are what get tested, with the original bug serving as the mutant.
- **Severity**, the idea underneath that gate, holds that passing a test counts as support only insofar as the test would have caught the mistake if it existed. Source: Deborah Mayo, *Statistical Inference as Severe Testing* (2018), and before that, more fully, *Error and the Growth of Experimental Knowledge* (1996).
- **Pre-registration and post-hoc flags.** These come out of clinical-trial methodology and the reforms prompted by the replication crisis. Their target is **HARKing** (Hypothesizing After the Results are Known), named by Kerr in 1998.
- **Framing.** Getting the right answer to the wrong question is what Kimball called a **Type III error**, in *"Errors of the third kind in statistical consulting"* (1957).

The habit this skill is meant to replace has a name as well: the **positive test strategy**, our natural tendency to check a hypothesis by hunting for examples that agree with it. The textbook demonstration is Wason's 2-4-6 task (1960); Klayman & Ha (1987) coined the term.

What seems to lack **any established name** is putting all of it together — holding the debugging loop itself to a severity standard. Plenty of methods explain how to locate a bug; hardly any ask whether your proof of the fix could ever have come out another way.
