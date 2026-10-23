---
name: ci-failure-triage
description: "Decides what kind of failure a red CI test is before anyone starts fixing it. Extracts seven failure signals from the runner output, stack trace, run history, and environment metadata, then walks an ordered first-match-wins rule set to exactly one verdict: flaky-known, environment-drift, defect, timeout, flaky-pre-incident, or flake-of-unknown-cause. Emits the verdict together with the alternatives that were rejected and the specific condition each one failed, so the triage decision is auditable rather than asserted. Use when a test has just gone red and the next action depends on whether the cause is a product defect, a non-deterministic test, or drifted infrastructure."
---

# CI failure triage

One test is red. Before anyone opens a ticket, reruns the job, or edits a
line, someone has to answer a prior question: what kind of failure is this?
This is the method for answering it, and for writing the answer down in a
form a second person can check.

The cost of getting it wrong is measurable. Google reports that about 84% of
the pass-to-fail transitions its CI observes involve a flaky test, and that
almost 16% of its tests show some level of flakiness (Google 2016). A triage
step that treats every red as a defect files mostly noise; one that treats
every red as a flake ships regressions.

## What this owns, and what it does not

This owns **classification**: turning one failed run into one verdict, with
the rejected alternatives recorded.

It deliberately does not own:

- **Report formatting.** A bug-report schema (summary, environment, steps to
  reproduce, expected, actual, severity, priority, reproducibility) is a
  separate job that starts *after* you already know the failure is a defect.
  This decides which kind of failure you are looking at; that fills in the
  form once you know.
- **Remediation.** No fix hypothesis, no patch, no rerun, no quarantine
  action. The verdict names the next step; it does not take it.
- **Suite-wide prediction.** One failure at a time. Screening a whole green
  suite for tests likely to flake next is a different technique with
  different inputs.
- **Retrieval.** How you obtain the log, the run history, or the environment
  metadata is out of scope. This assumes they are in front of you.

## Terminology

A red test is a **failure**: an error (a human action) introduces a defect (the
fault in the work product), and the failure is the observed event during
execution. Whether a defect actually sits behind this failure is exactly what
this method decides.

**The ISTQB glossary has no entry for "flaky test."** Querying its API for
`flaky-test`, `flaky`, and `non-deterministic-test` returns 404 in all three
cases (glossary.istqb.org), so do not cite a flaky-test definition to ISTQB.
Use Martin Fowler's canonical definition instead: "A test is non-deterministic
when it passes sometimes and fails sometimes, without any noticeable change in
the code, tests, or environment" (Fowler). Google's operational definition is
narrower and worth keeping alongside it: "a test that exhibits both a passing
and a failing result with the same code" (Google 2016).

The `environment-drift` verdict below is about the **test environment** - the
hardware, tooling, and support elements a test runs against - changing
underneath a test that did not.

## Step 1 - Extract the seven signals

Record all seven before applying any rule. A rule that fires on a signal you
never extracted is a guess.

| # | Signal | What to record |
|---|---|---|
| S1 | **Failure mode** | One token from the pattern table below. |
| S2 | **Reproducibility window** | Pass-to-fail ratio over the last 50 runs; length of the current red streak; the first red commit. |
| S3 | **Co-failure pattern** | Did other tests fail in the same run? Same suite? Same shard? |
| S4 | **Time clustering** | Are failures concentrated in one window (a deploy, off-hours, peak load)? |
| S5 | **Environment delta** | Did the runner image, container tag, or base build hash change inside the failure window? |
| S6 | **Change-set proximity** | Did files in the test's call graph change inside the window? |
| S7 | **Quarantine status** | Is the test on a formal quarantine list (an annotation, a decorator, a CI quarantine tag, a checked-in flake list)? |

The 50-run and 7-day windows are **practitioner conventions**, not values from
any standard. Pick windows your history actually covers and state them in the
verdict, because every rule below is relative to them.

### S1: the failure-mode pattern table

Match in the order listed. The order is by decreasing specificity, and crash
signatures come first because a dying process frequently emits a trailing
timeout that would otherwise capture the match.

| Mode token | Pattern in the runner output or trace |
|---|---|
| `runner-crash` | `SIGSEGV`, `Segmentation fault`, `OutOfMemoryError`, `panic:`, an unhandled exception that kills the process. |
| `assertion-mismatch` | Paired expected and actual values. googletest prints `Value of: ...` / `Actual: ...` / `Expected: ...` (googletest); xUnit, Jest, and pytest print equivalent pairs. |
| `setup-error` | A `BeforeEach`, `setUp`, `@BeforeAll`, or fixture frame in the trace. |
| `selector-breakage` | `no such element`, the W3C WebDriver error for a locator that matches nothing (W3C WebDriver); `NoSuchElementException`; Playwright's `strict mode violation` for a locator resolving to the wrong count (Playwright). |
| `environmental` | `ENOENT`, `FileNotFoundException`, a missing environment variable, `connection refused`. |
| `timed-out` | `Timeout` or `exceeded N ms` with no other exception attached. |
| `unclassified` | None of the above matched. |

`timed-out` is the **mode**. `timeout` is a **verdict**. They are not the same
claim: the mode says the clock ran out, the verdict says the CI infrastructure
is why. R3 and R4 below decide between them.

### S6: read the diff, do not skim it

Change-set proximity means files on the test's call graph changed inside the
window, and you read the change. Google's engineering practices put the
obligation plainly for reviewers: read and understand the change before acting
on it (Google eng-practices). A diff you only counted commits in does not
satisfy S6.

## Step 2 - Walk the rules, first match wins

The verdicts are mutually exclusive and single-valued. Evaluate R1 through R6
in order and stop at the first rule whose conditions all hold. A failure with
several plausible causes gets the earliest matching verdict, not two verdicts.

### R1 - `flaky-known`

Fires when S7 shows the test on a **formal** quarantine list **and** the
observed S1 mode matches the flake category already recorded for it.

Next step: rerun, and let the existing quarantine process handle it. No new
triage. Fowler's advice is to quarantine non-deterministic tests out of the
main pipeline and cap how long they may stay there (Fowler); R1 only
recognises that state, it does not create it.

Informal evidence does not count. A code comment saying "this one sometimes
fails" is not a quarantine list. If the project has no detectable quarantine
convention, R1 can never fire and you fall through to R2.

### R2 - `environment-drift`

Fires when **all** hold:

- S5 shows a runner image, container tag, or base build hash change inside the
  window, and
- the test passed on the old environment and fails on the new one, and
- S1 is `runner-crash`, `setup-error`, or `environmental` (never
  `assertion-mismatch`).

Next step is **not** a defect ticket. It is a re-pin of the image or an
investigation of how the environment is provisioned, routed to whoever owns
the CI platform.

An `environmental` mode with **no** S5 delta is not drift. The environment did
not change; the test depends on state nobody controls. That case falls through
to R5 or R6 as a test-isolation problem.

### R3 - `defect`

Fires when **all** hold:

- the test was green for the previous N runs (N=5 is a common default, a
  convention rather than a standard; state the N you used), and
- S6 shows files on the call graph changed inside the window, and
- S1 is `assertion-mismatch`, `selector-breakage`, or `setup-error`; or S1 is
  `timed-out` **and** the diff touched a timing constant or the code path under
  test, and
- the failure reproduces on a rerun of the same commit, where the history
  contains such a rerun.

This is the highest-confidence verdict available, because four independent
signals agree. Next step: capture whatever trace or artifact the runner can
produce, draft the defect report against the schema the team uses, and lock
the reproduction in a committed failing test before anyone edits production
code.

### R4 - `timeout`

Fires when S1 is `timed-out` with no other exception **and** either:

- S3 or S2 show similar timing-edge failures on *different* tests in the same
  window, which points at shared infrastructure rather than this test's logic,
  or
- the runner's CPU or memory profile for the run shows resource saturation.

Next step is a suite time-budget review or runner resource tuning, not a
defect ticket. R3 has already claimed the timeouts that have code-change
proximity, so anything reaching R4 has none.

### R5 - `flaky-pre-incident`

Fires when **all** hold:

- S2 shows at least one prior failure of this same test inside the last 50
  runs, so the pattern is intermittent rather than a clean break, and
- S6 shows no change-set proximity, and
- the S1 mode and the trace are shaped like async-wait, concurrency, or
  test-order dependency.

Those three are the top root-cause categories in the largest published study
of flaky-test fixes: of 161 classified fixes drawn from 201 flaky-test commits
across 51 Apache projects, 45% were async wait, 20% concurrency, and 12% test
order dependency (Luo et al., FSE 2014).

This is the "flaking, not yet quarantined" verdict. Next step: pattern
attribution, then quarantine if the pattern is confirmed.

### R6 - `flake-of-unknown-cause`

The fallback. Nothing above matched, or S1 came back `unclassified`. Emit a
low-confidence verdict and recommend bisection-style narrowing across run
conditions. R6 is an honest answer, and it is a better one than a `defect`
verdict propped up on two of four signals.

### Why this order

R2 sits ahead of R3 on purpose. Both can look plausible when a test starts
failing after an image bump that also landed near a code change, and routing
drift to the defect tracker sends the work to the wrong team while the tracker
fills with false positives. Putting the environment check first makes the
precedence explicit rather than leaving it to the mode preconditions.

R3 sits ahead of R5 on purpose too: when there is code-change proximity, an
async-wait timeout is more likely a product that got slower than a test that
got unlucky.

## Step 3 - Emit the verdict

One fixed shape. The **Not classified as** block is mandatory, including when
the verdict is high-confidence.

```markdown
## Failure classification - `<test-id>`

**Verdict:** <flaky-known | environment-drift | defect | timeout | flaky-pre-incident | flake-of-unknown-cause>
**Confidence:** <high | medium | low>
**Windows used:** <e.g. last 50 runs, 7 days of history, N=5 green-run threshold>

**Evidence:**
- <one line per signal that carried the verdict, naming the signal (S1..S7) and the observed value>

**Recommended next step:**
1. <action>
2. <action>

**Not classified as:**
- `<verdict>` - <the specific condition that failed, with the observed value>
- `<verdict>` - <the specific condition that failed, with the observed value>
```

### The Not-classified-as block is the load-bearing part

A bare verdict is an assertion. A verdict plus the rejected alternatives and
the exact condition each one failed is a decision another person can audit,
reopen, and overturn when a signal later turns out to be wrong.

Rules for the block:

- List **every** verdict that was evaluated and not returned. Do not list only
  the near miss.
- For each, name the **one specific condition** that failed and the value you
  observed, not a restatement of the rule. "`environment-drift` - runner image
  and container tag unchanged across the window" is auditable. "Does not look
  like environment drift" is not.
- When a signal was unavailable rather than negative, say so: "`environment-drift`
  - no environment metadata captured for this run, S5 could not be evaluated."
  That distinction is what tells a reader whether to re-triage once the missing
  signal arrives.
- Keep it even at high confidence. The high-confidence verdicts are the ones
  nobody re-examines later, which is exactly when a silent misroute is
  expensive.

## Worked example

A full end-to-end walk-through - the seven signals extracted, the rules
evaluated in order, and the emitted verdict with its Not-classified-as block -
is in [references/worked-example.md](references/worked-example.md).

## Anti-patterns

The catalogue of triage anti-patterns, each with why it fails and the rule that
prevents it, is in [references/anti-patterns.md](references/anti-patterns.md).

## Confidence and limits

- **Confidence tracks signal availability, not conviction.** Without S5, R2
  cannot be evaluated and no verdict may exceed medium. Without S6, R3 cannot
  reach high. Say which signal was missing rather than lowering the label
  silently.
- **New tests cannot be classified for the first window.** A test merged two
  days ago has no S2, so R3 and R5 are both unavailable and R6 is usually the
  only honest answer.
- **Co-failure detection is heuristic.** S3 reports that other tests failed in
  the same run, suite, or shard. It does not prove shared-state coupling; that
  needs targeted isolation analysis.
- **`unclassified` is a real outcome.** When S1 matches nothing in the pattern
  table, record `unclassified` and let it flow to R6. Forcing a mode token to
  make a rule fire is how a wrong verdict acquires false confidence.
- **One failure per pass.** For an overnight run with forty reds, run the
  method forty times. It is not a report-summarising technique, and batching
  it destroys the per-failure signal set the rules depend on.

## References

- Google 2016 - "Flaky Tests at Google and How We Mitigate Them": https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html
- Fowler - "Eradicating Non-Determinism in Tests": https://martinfowler.com/articles/nonDeterminism.html
- ISTQB glossary: https://glossary.istqb.org/
- googletest advanced guide: https://google.github.io/googletest/advanced.html
- W3C WebDriver errors: https://www.w3.org/TR/webdriver2/#errors
- Playwright locators: https://playwright.dev/docs/locators
- Google eng-practices, code review: https://google.github.io/eng-practices/review/reviewer/looking-for.html
- Luo et al., "An Empirical Analysis of Flaky Tests," FSE 2014: https://mir.cs.illinois.edu/marinov/publications/LuoETAL14FlakyTestsAnalysis.pdf
