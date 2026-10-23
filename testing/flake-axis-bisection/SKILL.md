---
name: flake-axis-bisection
description: "Locates the condition a known-flaky test actually depends on by holding the test constant and varying one axis at a time (isolation, execution order, worker count, viewport, network latency, repetition depth), recording a pass/fail count per variation, and testing whether the gap between two conditions exceeds sampling noise. Covers choosing the run count N from the failure rate you need to detect, binomial confidence intervals on a measured reproduction rate, a two-proportion comparison rule, what a zero-failure result does and does not prove, and the resource-collision walk (DB row, DB schema, file path, port, env var, module state, inode, cookie jar) used once parallelism is implicated. Use when a specific test is already known to fail intermittently, reading its source has not explained why, and a decision about what to change must rest on measurement rather than on a plausible-sounding guess."
---

# flake-axis-bisection

A non-deterministic test is one that "sometimes pass[es] and sometimes
fail[s], without any noticeable change in the code, tests, or
environment" ([Fowler, Eradicating Non-Determinism in
Tests](https://martinfowler.com/articles/nonDeterminism.html)). That
definition is the problem in a nutshell: nothing visible changed, so
inspection has nothing to grip. This skill is the experiment that
manufactures a visible change. Pick one condition, move it, and see
whether the failure rate moves with it.

The term "flaky test" is practitioner-emergent, popularized by the
Google Testing Blog ([Flaky Tests at
Google](https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html));
there is no standards-body definition behind it.

## What this owns, and what it does not

**Owns:** the empirical protocol. One test, one axis at a time, a
counted outcome per variation, and an explicit rule for deciding
whether the difference between two counts is signal or noise.

**Does not own: the catalog.** A flake-pattern catalog (for example
`flake-pattern-reference`) classifies a flake by *inspection*: read the
symptom, match it to a named pattern, apply the pattern's remediation.
This protocol classifies by *experiment*: you do not need to recognize
the symptom, because you produce the evidence. Use a catalog to give
the result a name and a fix once the sweep points at an axis. Use this
skill when the catalog's decision tree has already been walked and two
or more patterns still fit.

**Does not own: commit search.** Finding which commit introduced a
failure is a search over revision history and applies to a test that
now fails every time. This is a search over *execution conditions* for
a test that fails only sometimes. If the test fails 20 times out of 20,
stop: it is not flaky, and the sweep below will tell you nothing.

**Does not own: the fix.** The output is an implicated axis plus the
evidence for it. Remediation is a separate step.

## Vocabulary used below

| Term | Meaning |
|---|---|
| Axis | One condition being varied (worker count, execution order, viewport). |
| Variation | One setting of an axis (`--workers=1`, `--workers=4`). |
| N | Number of executions of the target test at one variation. |
| k | Number of those executions that failed. |
| Reproduction rate | The point estimate `k/N`. An estimate, never the truth. |
| Baseline | The project's standard configuration, measured the same way. |

## Step 1: pin everything except one axis

The sweep is only interpretable if exactly one thing differs between a
variation and the baseline. Before the first run, freeze:

- the commit under test, and the dependency lockfile,
- the machine class or container image (a sweep split across a laptop
  and a CI runner silently varies the environment axis inside every
  other axis),
- the random seed policy. Either seed every source to a fixed value, or
  record the seed per run so a failure can be replayed. Jest prints the
  seed with `--showSeed` and accepts `--seed=<num>`, and its docs note
  that "when dealing with flaky tests, rerunning with the same seed
  might help reproduce the failure" ([Jest
  CLI](https://jestjs.io/docs/cli)).

If the target test cannot be run in isolation from the rest of the
suite, that fact is itself the first result: the isolation axis is
already implicated.

## Step 2: choose N before you run anything

N is not a taste question. It follows from the smallest failure rate you
need to be able to see. If a test truly fails with probability `p` on
independent runs, the chance that N runs produce zero failures is
`(1 - p)^N`; solving `(1 - p)^N = 0.05` gives the N at which you have a 95%
chance of seeing at least one failure. The full p-to-N table and its
derivation are in
[references/reproduction-rate-statistics.md](references/reproduction-rate-statistics.md).
The one number to remember: a test that really fails 5% of the time still
shows a clean 0/20 more than a third of the time. N=20 is a *screening*
depth - enough to separate a roughly 40% flake from a roughly 5% flake, not
enough to separate 5% from 10%.

**Cost.** Total executions are `axes x variations x N`. The sweep below
has 8 axes with 2 to 4 variations each, so N=20 costs roughly 320 to 640
executions of one test, and N=60 costs roughly 1,000 to 1,900. This is
the reason the protocol is run against a single named test rather than
across a suite. Runners support the repetition directly: Playwright's
`--repeat-each <N>` runs "each test `N` times (default: 1)"
([Playwright CLI](https://playwright.dev/docs/test-cli)).

**Practical compromise (a convention, not a standard):** screen all
axes at N=20, then re-measure only the baseline and the one or two
implicated variations at N=60 or higher before acting. Nothing in the
statistics endorses N=20; it is a budget choice, and its consequences
are the ones tabulated in the reference.

## Step 3: measure the baseline

Run the target test N times under the project's standard configuration.
Record, per run: pass or fail, wall-clock duration, and the seed. Keep
the raw per-run outcomes, not just the total. Duration is worth keeping
because a rate that is flat while durations creep upward points at the
repetition axis rather than at any of the configuration axes.

The baseline is a measurement like any other, with the same
uncertainty as every variation. It is not a reference truth.

## Step 4: sweep one axis at a time

Order the axes cheapest and most discriminating first, and stop early
when an axis reproduces strongly: there is no prize for completing the
sweep.

| # | Axis | Variations | What a rate increase implicates |
|---|---|---|---|
| 1 | Isolation | Target test alone, versus the full suite. | Order dependence, or state shared across parallel workers. |
| 2 | Worker count | 1 worker, then 4, then the CI setting. | Shared parallel state. A rate that climbs monotonically with worker count is contention. |
| 3 | Execution order | Fixed file order, versus randomized order with a recorded seed. | Order dependence: the test consumes state a sibling left behind. |
| 4 | Network latency and bandwidth | Unconstrained, versus a constrained profile. | Async and timing assumptions, or a real dependency on an external service. |
| 5 | Viewport | Narrow, medium, wide. | Locator drift: the selector matches by position, and layout moved it. |
| 6 | Animation and transition suppression | Enabled versus suppressed. | Async and timing: the assertion races a transition. |
| 7 | OS or runner image | The CI image, versus a second OS or image. | Environment variance: path separators, line endings, filesystem case sensitivity, timezone. |
| 8 | Repetition depth | N sequential executions in one process, N large. | Resource leak: file descriptors, sockets, browser processes. |

Axes 1, 3, 4, 7, and 8 line up with the five causes of non-determinism
Fowler enumerates: lack of isolation, asynchronous behavior, remote
services, time, and resource leaks
([Fowler](https://martinfowler.com/articles/nonDeterminism.html)). Axes
2, 5, and 6 are the ones a browser-driven suite adds on top.

Knobs that realize the axes, by runner:

| Axis | Playwright | Jest |
|---|---|---|
| Worker count | `--workers=<n>`, "use 1 to run in a single worker" ([Playwright CLI](https://playwright.dev/docs/test-cli)) | `--maxWorkers=<num>`, or `--runInBand` to "run all tests serially in the current process" ([Jest CLI](https://jestjs.io/docs/cli)) |
| Repetition | `--repeat-each <N>` ([Playwright CLI](https://playwright.dev/docs/test-cli)) | rerun the invocation N times |
| Order | (fixed file order by default) | `--randomize`, which shuffles order within a file based on the seed and is "only supported using the default `jest-circus` test runner" ([Jest CLI](https://jestjs.io/docs/cli)) |

For the network axis, a Chromium-backed runner can constrain the
connection through the DevTools Protocol `Network` domain, whose
throttling command takes `offline`, `latency`, `downloadThroughput`,
and `uploadThroughput`. Note the version drift before you script it:
`Network.emulateNetworkConditions` is marked deprecated in the current
protocol, superseded by `emulateNetworkConditionsByRule` and
`overrideNetworkState` ([Chrome DevTools Protocol, Network
domain](https://chromedevtools.github.io/devtools-protocol/tot/Network/)).
Any transparent proxy or OS-level traffic shaper serves the same
purpose.

## Step 5: decide whether a difference is real

This is the step the protocol exists for. Two counts always differ. The
question is whether they differ by more than sampling noise.

### 5a. Report an interval, not just a rate

`k/N` is a point estimate of a proportion; attach a confidence interval to
it. The Wilson interval, recommended "for virtually all combinations of n
and p", is the standard choice ([NIST/SEMATECH e-Handbook, Confidence
intervals for a
proportion](https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm)).
The lookup table of computed 95% Wilson intervals for the counts that come
up most often is in
[references/reproduction-rate-statistics.md](references/reproduction-rate-statistics.md).
The two rows that matter most: 1/20 and 2/20 have intervals that overlap
across almost their entire width, so a sweep reporting "5% baseline, 10%
under randomized order" has measured nothing.

### 5b. Compare two variations with a stated rule

For baseline `x1/n1` against a variation `x2/n2`, compute the pooled
two-proportion statistic `z = (p1 - p2) / sqrt(p(1-p)(1/n1 + 1/n2))` where
`p = (x1+x2)/(n1+n2)`, and compare `|z|` against the normal table value
`z(1-alpha/2)` ([NIST/SEMATECH e-Handbook, Comparing two
proportions](https://www.itl.nist.gov/div898/handbook/prc/section3/prc33.htm)).
At alpha = 0.05 that threshold is 1.96; the handbook notes Fisher's exact
test as the small-sample alternative. Worked comparisons against a 3/20
baseline are tabulated in
[references/reproduction-rate-statistics.md](references/reproduction-rate-statistics.md).
The load-bearing case: a 6/20 result is a doubling of the observed rate
(15% to 30%) and still does not clear 1.96 at N=20. A screening rule phrased
as "a relative change above 2x implicates the axis" is a convention for
deciding *which axis to re-measure*, not a finding: treat a 2x hit as a
shortlist entry, re-run that axis and the baseline at higher N, then apply
the z rule.

### 5c. Two caveats that bound everything above

**Independence.** The binomial model assumes independent, identically
distributed runs. Twenty repetitions inside one process, against one
warmed cache, on one machine, are not independent. Where they are
correlated, the true uncertainty is *wider* than the intervals in 5a,
never narrower. Prefer fresh processes per run, and treat every
interval here as a floor on the uncertainty.

**Multiplicity.** Sweeping 8 axes means running many comparisons at
alpha = 0.05, so an occasional false positive is expected by
construction. This is exactly why an implicated axis is confirmed by a
second, deeper measurement before anyone edits code.

## Step 6: when parallelism is implicated, walk the collision classes

If the worker-count axis moved the rate, the next question is narrower:
which resource are two workers stepping on? Fowler's isolation rule is the
target state - "Keep your tests isolated from each other, so that execution
of one test will not affect any others"
([Fowler](https://martinfowler.com/articles/nonDeterminism.html)). Walk the
eight collision classes (DB row, DB schema, file path, port, env var,
module state, filesystem inode, cookie or storage jar) in order, each with
its discriminating probe and the fix that makes the resource per-worker:
[references/parallel-collision-classes.md](references/parallel-collision-classes.md).
Two sources that walk cannot reach - kernel socket state held in
`TIME_WAIT`, and cross-worker external-service state such as a shared
third-party rate limit - are what remains if every class comes back clean
and the axis still reproduces.

## Report shape

```markdown
## Axis bisection: `tests/checkout.spec.ts:42`

Commit: a1b2c3d   Image: ci-node20:2026-07-02   N per variation: 20
Baseline: 3/20 (15%), 95% CI 5.2% to 36.0%

| Axis            | Variation      | Result       | 95% CI          | z vs baseline | Verdict |
|-----------------|----------------|--------------|-----------------|--------------:|---------|
| Isolation       | alone          | 3/20 (15%)   | 5.2% to 36.0%   |          0.00 | noise   |
| Worker count    | 1              | 2/20 (10%)   | 2.8% to 30.1%   |         -0.48 | noise   |
| Worker count    | 4              | 4/20 (20%)   | 8.1% to 41.6%   |          0.42 | noise   |
| Execution order | randomized     | 4/20 (20%)   | 8.1% to 41.6%   |          0.42 | noise   |
| Network         | constrained    | 17/20 (85%)  | 64.0% to 94.8%  |          4.43 | IMPLICATED |
| Viewport        | 375            | 6/20 (30%)   | 14.5% to 51.9%  |          1.14 | shortlist  |

Confirmation run, N=60: baseline 8/60 (13%), network constrained 49/60 (82%).

Implicated axis: network latency and bandwidth.
Not implicated: isolation, worker count, execution order.
Undecided: viewport. Shortlisted on a 2x screening hit; z=1.14 at N=20
does not clear 1.96, and the confirmation run was not spent on it.
Next: inspect the test's waits for a fixed sleep or an
assertion that races the response, not a parallelism fix.
```

Report every axis, including the ones that came back flat. A reader who
sees only the implicated row cannot tell whether the others were
measured or skipped.

## Reading a negative result

A sweep in which no axis clears the threshold is a real outcome, and it
is the one most often misreported.

**What a 0/20 licenses you to say:** the failure rate under this
variation is bounded above. The rule of three states that if an event
did not occur in a sample of n subjects, "the interval from 0 to 3/n is
a 95% confidence interval for the rate of occurrences" ([Rule of three
(statistics)](<https://en.wikipedia.org/wiki/Rule_of_three_(statistics)>),
which notes the approximation is intended for n greater than 30). So
0/20 bounds the rate at roughly 15%, 0/50 at 6%, 0/100 at 3%.

**What it does not license:** "the flake is gone", "the test is
deterministic", or "the fix worked". A test failing 2% of the time
sails through 0/20 two-thirds of the time by the table in Step 2. After
a remediation, re-measure at an N chosen from the rate you are willing
to ship, not at the N you used for screening. If the team's tolerance
is 1%, that is roughly 300 runs to have a 95% chance of catching it,
and a clean 0/300 still only bounds the rate at 1%.

**When no axis reproduces at all,** the remaining explanations are a
genuinely low-rate flake that N=20 cannot see, an unseeded random input
whose failing value has not recurred, or an axis outside this sweep.
Record the seed for every run so that the failing case can be replayed
rather than hunted again, and escalate N on the axis with the largest
observed gap rather than declaring the test healthy.

## Anti-patterns

- **Varying two axes at once.** Running the alone-test at 1 worker
  changes isolation and worker count together, and no comparison
  separates them afterward.
- **Comparing a variation to a remembered baseline.** The baseline is
  re-measured on the same image, same commit, same N, in the same
  session. A rate quoted from last week's CI dashboard is a different
  experiment.
- **Reporting a rate without an interval.** "10% under randomized
  order" reads like a finding and is compatible with anything from 3%
  to 30%.
- **Acting on a screening hit.** A 2x relative change at N=20 selects
  the axis to measure next. It does not select the code to change.
- **Sweeping the whole suite.** At hundreds of executions per test,
  this protocol is affordable for one test the team has already decided
  is worth the CI time, and unaffordable as a screen.
- **Calling a 20/20 failure flaky.** A test that always fails is a
  regression, and the search that solves it ranges over commits, not
  over conditions.
- **Silently retrying instead of measuring.** Retries convert the
  measurement you need into a green build. Quarantine is the honest
  holding action, and Fowler's rule is to "place any non-deterministic
  test in a quarantined area", with the caveat to "fix quarantined
  tests quickly"
  ([Fowler](https://martinfowler.com/articles/nonDeterminism.html)).

## A note on where flakes concentrate

Google's analysis across 4.2 million tests found that larger tests are
substantially more flaky than smaller ones, with a roughly linear trend
across size buckets ([Where do our flaky tests come from?
](https://testing.googleblog.com/2017/04/where-do-our-flaky-tests-come-from.html)).
The practical consequence for this protocol: the tests that justify a
600-execution sweep are usually the large end-to-end ones, which are
also the slowest to run. Budget the sweep against the test's own
runtime, and reach for the shallower N=20 screen plus one deep
confirmation rather than a uniformly deep sweep.

## Deep references

- **Reproduction-rate statistics** - the p-to-N sizing table, the Wilson
  confidence-interval lookup, and the two-proportion worked comparisons
  behind Steps 2 and 5:
  [references/reproduction-rate-statistics.md](references/reproduction-rate-statistics.md).
- **Parallel-execution collision classes** - the eight-resource walk (DB
  row, schema, file path, port, env var, module state, inode, storage jar)
  for Step 6:
  [references/parallel-collision-classes.md](references/parallel-collision-classes.md).
