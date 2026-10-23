---
name: chaos-drill-protocol
description: "Run protocol and run workflow for a chaos experiment that has already been designed: the four pre-flight gates (non-production target, measured healthy baseline, live observability, a rollback that has actually been exercised), how to pick a conservative blast-radius bound, the sampling cadence and abort criteria fixed in writing before injection, the per-runner inject and abort commands (Chaos Mesh / Litmus / Gremlin / Toxiproxy), the refuse-to-start rules (no blast-radius bound, production context, degraded baseline, offline observability, unexercised rollback), and the recovery-validation step with its tolerance and timeout. Owns execution safety only, not experiment design: the steady-state hypothesis, the fault to inject, and the experiment file come from chaos-experiment-author. Use when an experiment definition exists and a fault is about to be injected into a running system, and the go/no-go gates, abort thresholds, and recovery check still need to be agreed and written down before the fault starts."
---

# chaos-drill-protocol

[cp]: https://principlesofchaos.org/
[sre-mon]: https://sre.google/sre-book/monitoring-distributed-systems/
[sre-risk]: https://sre.google/sre-book/embracing-risk/
[sre-emer]: https://sre.google/sre-book/emergency-response/
[sre-test]: https://sre.google/sre-book/testing-reliability/
[cm]: https://netflix.github.io/chaosmonkey/
[cm-term]: https://netflix.github.io/chaosmonkey/Termination-behavior/
[ctk]: https://chaostoolkit.org/reference/api/experiment/
[istqb-rec]: https://glossary.istqb.org/en_US/term/recoverability

## What this skill owns, and what it does not

This is the **run** protocol. It covers the window that opens when someone is
about to inject a real fault into a running system and closes when the system
has been confirmed back at baseline: what must be true before the fault starts
(pre-flight gates), how wide it is allowed to reach (blast-radius bound), what
is watched while it is live and what ends it early (sampling and abort
criteria), and how recovery is confirmed rather than assumed.

**Not owned here:** designing the experiment. Choosing the steady-state
hypothesis and its metric, choosing which real-world event to inject, and
writing the experiment definition are a separate job that happens earlier. Per
[principlesofchaos.org][cp], an experiment starts "by defining 'steady state'
as some measurable output of a system that indicates normal behavior" and then
hypothesizes "that this steady state will continue in both the control group
and the experimental group." This protocol assumes a written hypothesis with a
numeric threshold already exists. If it does not, stop and go do that first: a
drill with no hypothesis produces a story, not a result. Also out of scope:
aggregating results across drills into a trend, and the vendor-specific syntax
of whichever injection tool is in use.

## Why this protocol is strict

A chaos drill and an outage differ only by preparation: Google's SRE account of a
test-induced emergency shows a test scoped to one database cascading into a
multi-service outage because the dependency assumptions were incomplete and the
rollback had never been tested in a test environment
([sre.google/sre-book/emergency-response][sre-emer]). Every gate below exists
because skipping it is how that outcome happens.

## The drill contract

Fill this in and get it agreed **before** anything is injected. Every field is
a number or a name, never a judgment to be made later.

| Field | Meaning | Fixed before injection? |
|---|---|---|
| `hypothesis` | The steady-state metric and its numeric threshold, from the experiment definition | Yes |
| `target` | The exact scope: environment, namespace, service, replica count `N` | Yes |
| `fault` | The single event being injected | Yes |
| `blast_radius` | Max fraction of `N` affected, plus max duration | Yes |
| `abort_criteria` | The numeric thresholds that end the drill early, each with a dwell time | Yes |
| `sample_interval` | How often observability is read while the fault is live | Yes |
| `recovery_criteria` | The signals that must return to baseline, with tolerance and timeout | Yes |
| `rollback` | The named action that removes the fault, and who runs it | Yes, and rehearsed |

A drill missing any row is not ready to run. This mirrors how the Chaos Toolkit
experiment format treats safety as structural rather than optional: the format
has a first-class `rollbacks` property whose actions "attempt to put the system
back to its initial state", and if the steady-state hypothesis is not met up
front then "the Method element is not applied and the experiment MUST bail out"
([chaostoolkit.org/reference/api/experiment][ctk]).

## Stage 1: pre-flight gates

**These four are gates, not a checklist to feel good about.** Each one is
pass or fail. **A single failure stops the drill.** There is no partial pass,
no "we will watch it closely instead", and no waiving a gate because a
maintenance window is expiring. A failed gate is fixed and the drill is
rescheduled.

### Gate 1: the target is not production

Read the environment identity from the tooling itself (the active cluster or
account context), not from what someone typed in the ticket. If the resolved
context names production, the drill stops.

Running in production is a legitimate long-term goal, not a starting point.
[principlesofchaos.org][cp] does state that "Chaos strongly prefers to
experiment directly on production traffic", and Netflix's Chaos Monkey "is
responsible for randomly terminating instances in production"
([netflix.github.io/chaosmonkey][cm]). Both describe mature programs with years
of tooling behind them. This protocol gates on non-production and treats
promotion as a separate decision made after repeated clean runs.

### Gate 2: the baseline is healthy, and measured

Take a real baseline measurement immediately before injection. Not last week's
dashboard screenshot: a fresh reading over a window long enough to be stable.
Record the actual numbers for every signal the abort and recovery criteria
reference, because those criteria are expressed relative to this baseline.

If the target is already degraded, the drill stops. The experiment method is to
look "for a difference in steady state between the control group and the
experimental group" ([principlesofchaos.org][cp]), so a degraded starting point
means any difference observed cannot be attributed to the injected fault: an
uninterpretable result carrying full risk.

Gating on "at least 99% of instances healthy" is a practitioner convention, not
a standard. Treat it as a starting default. The defensible version is stricter
and local: the baseline must sit inside the range the service normally holds at
this time of day, and be stable across the measurement window.

### Gate 3: observability is live

Confirm that fresh samples for every abort-criterion signal have arrived within
the last sampling interval. Stale dashboards fail this gate exactly as hard as
missing ones.

The signals to confirm are the ones the drill will abort on. A useful default
set is the four golden signals - latency, traffic, errors, saturation - defined
verbatim in [references/golden-signals.md](references/golden-signals.md) after
[sre.google/sre-book/monitoring-distributed-systems][sre-mon].

Without live signals there is no way to detect that a bound has been crossed,
which means the drill has no abort path that fires on evidence. That is not a
riskier drill. It is a fault injection with no stopping rule.

### Gate 4: the rollback has been exercised, not documented

**Verified means someone ran it and watched it succeed.** A runbook entry, a
tool's advertised time-to-live, or a colleague's recollection that "it worked
last time" do not clear this gate.

Exercise it like this, before injection:

1. With no fault present, run the exact rollback action against the exact
   target, from the exact account or context that will run it during the drill.
2. Confirm it returns success and leaves the system unchanged.
3. Record who ran it, when, and how long it took. That duration becomes the
   assumed abort latency in the drill contract.

Where the injection tool offers an automatic expiry as well, set it, and treat
it as a backstop behind the manual action rather than as the rollback itself.

This gate is the direct lesson of the SRE test-induced emergency, where the
rollback path failed because it had never been tested in a test environment
([sre.google/sre-book/emergency-response][sre-emer]). An untested path lets an
unrelated environment change silently alter its result
([sre.google/sre-book/testing-reliability][sre-test]).

### Gate summary

| Gate | Passes when | On failure |
|---|---|---|
| Non-production target | Resolved context does not name production | Stop. Re-target, or run the separate production-readiness decision |
| Healthy measured baseline | Fresh reading, inside normal range, stable across the window | Stop. Fix the service, take a new baseline, reschedule |
| Live observability | Fresh samples present for every abort-criterion signal | Stop. Restore telemetry first |
| Exercised rollback | Rollback action was just run successfully against this target | Stop. Rehearse it, record the duration, then reschedule |

## Stage 2: choosing a blast-radius bound

Per [principlesofchaos.org][cp], "It is the responsibility and obligation of
the Chaos Engineer to ensure the fallout from experiments are minimized and
contained." That principle sets the direction but not the number. Derive the
number instead of asserting it.

**The load argument.** If a fraction `f` of `N` replicas is removed, each
surviving replica absorbs the redirected share, so its load multiplies by
`1 / (1 - f)`. That is arithmetic, and it is the reason a large bound quietly
turns into two experiments at once:

| Fraction removed | Surviving replicas | Load per survivor |
|---|---|---|
| 1 of 12 (about 8%) | 11 of 12 | about 1.09x |
| 25% | 3 of 4 | about 1.33x |
| 50% | 1 of 2 | 2.00x |
| 100% | none | no surviving capacity |

At 50% the drill is testing the injected fault **and** a doubling of per-replica
load simultaneously, so a failure cannot be attributed to either one. At small
fractions the confound is small and the result is readable. That is the whole
argument for starting small and widening only after clean runs.

**The reference point for "small".** Netflix's Chaos Monkey, running against
production, ships a deliberately tiny bound: every weekday it "flips a weighted
coin to decide whether to terminate an instance from that group", and when the
coin comes up heads it schedules **one** termination in a daytime window
([netflix.github.io/chaosmonkey/Termination-behavior][cm-term]). One instance
per group per day, on purpose, in the most mature chaos program there is. A
first drill has no case for being bolder than that.

**Expressing the error bound.** State the error-rate ceiling against the
service's remaining error budget rather than as a bare percentage. Per
[sre.google/sre-book/embracing-risk][sre-risk], the error budget is the
difference between the SLO target and measured actual uptime, "the 'budget' of
how much 'unreliability' is remaining". A drill spends that budget. Deciding in
advance what share of it this drill may spend is what keeps a series of drills
from consuming the quarter.

**Duration.** Bound it in wall-clock time, and make the bound short enough that
the full duration plus the rehearsed rollback duration fits inside the window
the team has agreed to stay attentive for. A drill that outlives its watchers
has no abort path.

## Stage 3: monitoring while the fault is live

### Abort criteria are written before injection, never judged live

Every abort criterion is a **signal, a threshold, and a dwell time**, written
into the drill contract before injection and unchanged once the fault starts.

This is not a formality. Once a fault is live, the person watching is under
time pressure, has already invested effort in getting the drill scheduled, and
is looking at a graph that is supposed to be moving. Those are the conditions
under which a threshold gets renegotiated in the moment. Writing the number in
advance removes the decision from that moment: the sampler compares, it does
not deliberate. The scientific framing demands the same, since the experiment
exists to "try to disprove the hypothesis" ([principlesofchaos.org][cp]), and a
hypothesis whose bounds move during the run cannot be disproved.

Nobody may loosen a criterion mid-run. Anyone may abort early. Those are not
symmetric, and should not be.

### Sampling cadence

Read every abort-criterion signal on a fixed interval. **A 10-second interval
is a practitioner convention, not a standard.** Two constraints set the real
value:

- **Shorter than the tightest dwell time, by several samples.** A criterion of
  "p99 above 10x baseline for 60 seconds" needs enough samples inside that
  60 seconds to establish the condition held rather than spiked. Ten seconds
  gives six. One sample per minute gives one, which cannot distinguish a
  sustained breach from a single noisy point.
- **No shorter than the telemetry backend's own resolution.** Sampling faster
  than the backend aggregates returns repeated values and creates false
  confidence in the cadence.

Pick the interval from those two constraints for the actual stack, then write
it into the contract.

### What ends the drill early

Each row is filled in with the specific numbers before injection. The example
values below are illustrative shapes, not recommended defaults.

| Abort criterion | Shape | Why it ends the drill |
|---|---|---|
| Error rate above budget | `errors > X%` sustained for `D` seconds, where `X` came from the agreed error-budget share | The drill is spending more reliability than it was authorized to spend ([sre.google/sre-book/embracing-risk][sre-risk]) |
| Blast radius exceeded | More than the bounded fraction of `N` affected | The fault has spread past the scope the bound was reasoned against, so the load argument above no longer holds |
| Latency collapse | `p99 > M x baseline` sustained for `D` seconds | Sustained, not spiked, means the system is not absorbing the fault |
| Downstream breach | Any dependent service crosses its own SLO | The drill is now affecting systems that never consented to be in scope, which is how a contained test becomes an incident ([sre.google/sre-book/emergency-response][sre-emer]) |
| Manual abort | Any participant calls it | Human judgment may always stop a drill early; it may never extend one |

### The abort itself

1. Run the rehearsed rollback action. It is the one from Gate 4, unchanged.
2. Record the timestamp, the criterion that fired, and every signal value at
   that moment, before anything is cleaned up.
3. Proceed to Stage 4. An aborted drill still gets recovery validation.

**Never abort silently.** An abort is the drill's most informative outcome: it
is the moment the system told you where its bound is. Discarding it because the
run "did not complete" throws away the only data the drill produced.

## Stage 4: recovery validation

Recovery is confirmed, not assumed. The property under test is
**recoverability**, defined in the ISTQB glossary (V4.7.2) as "the degree to
which a component or system can recover the data directly affected by an
interruption or a failure and re-establish the desired state of the component
or system", after ISO 25010
([glossary.istqb.org/en_US/term/recoverability][istqb-rec]).

Removing the fault is not recovery. Recovery is the system returning to the
baseline recorded at Gate 2.

### The checks

| Check | Passes when |
|---|---|
| Capacity | Ready replica count is back to the Gate 2 baseline count |
| Errors | Error rate is back inside the recovery tolerance around the Gate 2 baseline |
| Latency | p95 and p99 are back inside tolerance around their Gate 2 baselines |
| Downstream | Every dependent service touched during the run is back inside its own SLO |
| Stability | All of the above hold continuously for a settle window, not at a single instant |

### Tolerance and timeout

**"Baseline plus 10%" is a practitioner convention, not a standard**, and a
poor final answer because it is unrelated to how noisy the specific signal is.
The tolerance has two opposing constraints:

- **Wide enough to clear.** Inside the signal's own run-to-run variation,
  recovery never validates and the team learns to ignore the check.
- **Narrow enough to mean something.** Too wide, and a system left measurably
  degraded passes as recovered, which is the failure this stage exists to catch.

Derive it from the Gate 2 measurement: set the tolerance from the observed
variation of that signal across the baseline window and write the number into
the contract. Keep the 10% default only where no baseline variance was
captured, and say so in the record.

Set a maximum wait too. **Five minutes is a common convention**; the right
value depends on the system's own restart and warm-up behavior. Reaching the
timeout is a result, not an error: recovery did not complete unassisted, which
is a finding worth more than a clean pass.

### Verdicts

| Verdict | Meaning |
|---|---|
| `RECOVERED` | All checks passed inside the timeout, with no manual intervention |
| `RECOVERED_ASSISTED` | Checks passed, but a human had to act. Record exactly what they did; that action is a gap in automated recovery |
| `PARTIAL` | Some checks passed inside the timeout, others did not |
| `NOT_RECOVERED` | Timeout reached with checks still failing. Treat as an incident and follow the normal incident process |

**Never run the next drill from an unrecovered state.** A follow-up launched
before recovery validates starts from an unknown baseline, which fails Gate 2
by definition, and its blast-radius reasoning is void because the
surviving-capacity arithmetic assumed a full complement of healthy replicas.

## Running the drill

The four stages execute as one workflow per drill: pre-flight gates, then
injection, then the live monitor, then recovery validation. No team should
delegate live fault injection; a human runs each step against this protocol.

**Required before anything starts:** the target (environment, namespace,
service, replica count), one specific experiment intent (latency-injection /
pod-kill / network-partition / disk-pressure / cpu-stress / dns-failure), and
the blast-radius bound (max fraction of replicas, max duration, max
error-rate budget). Read the environment identity from the tooling itself
(`kubectl config current-context` for K8s; `gremlin env` for Gremlin), never
from the ticket. The experiment file comes from `chaos-experiment-author`;
for network-layer faults at the application boundary use
`failure-injection-test-author` (host-side harness) instead.

**Per-runner inject and abort commands.** Record the injection timestamp and
the experiment's unique ID at inject time - the abort path needs both.

| Runner | Inject | Abort |
|---|---|---|
| Chaos Mesh | `kubectl apply -f <experiment>.yaml` | `kubectl delete -f <experiment>.yaml` |
| Litmus | `litmusctl chaos run -f <experiment>.yaml` | `litmusctl chaos abort <experiment-id>` |
| Gremlin | `gremlin attack new --command <type> --args <args>` | `gremlin halt <attack-id>` |
| Toxiproxy | `toxiproxy-cli toxic add --type <type> --attribute <name=value> <proxy>` | `toxiproxy-cli toxic delete --toxicName <name> <proxy>` |

The abort command doubles as the Gate 4 rollback action to exercise before
injection. While the fault is live, sample every abort-criterion signal on
the contract's interval (Stage 3) and abort on any breach; recovery
validation (Stage 4) runs regardless of how the run ended.

**Refuse-to-start rules.** Each maps to a gate or contract row; a drill that
trips one does not start:

- No blast-radius bound supplied - unbounded chaos is an incident, not a drill.
- The resolved context names production (Gate 1).
- The baseline is degraded at pre-flight (Gate 2) - the result would be uninterpretable.
- Observability is offline or stale (Gate 3) - no live signals, no stopping rule.
- The rollback was not exercised against this target (Gate 4) - a configured TTL is a backstop, not a verified rollback.
- The request says "test the system end-to-end" with no specific experiment type - ask for one.

## Worked example

A full end-to-end run - the frozen drill contract, the pre-flight table, the
live-run trace ending in an `error-budget` abort, and recovery validation to
`RECOVERED` - is in
[references/worked-example.md](references/worked-example.md).

## Expected output shape

One record per drill, aborted runs included.

```markdown
## Chaos drill record: checkout-pod-kill-2026-07-19

**Target:** staging / checkout-staging / checkout (N=12)
**Fault:** pod-kill, bound 3 of 12, max 5m
**Hypothesis:** checkout_completion_rate >= 95% over 5m
**Outcome:** ABORTED at T+1:00 | **Recovery:** RECOVERED (4m14s, unassisted)

### Pre-flight
| Gate | Result | Evidence |
|---|---|---|
| Non-production target | PASS | context checkout-staging |
| Healthy measured baseline | PASS | 12/12 ready, 5xx 0.2%, p99 240ms, stable 10m |
| Live observability | PASS | freshest sample 4s old, all 4 signals |
| Exercised rollback | PASS | rehearsed T-8m, success in 6s |

### Run
Injected T+0:00, aborted T+1:00 on `error-budget` (5xx > 2% sustained 30s),
rollback complete T+1:06. Signal values at abort: ready 8/12, 5xx 3.3%,
p99 1140ms.

### Observed blast radius
| Measure | Peak observed | Bound |
|---|---|---|
| Replicas unready | 4 of 12 | 3 of 12 |
| Error rate | 3.3% | 2% |
| p99 latency | 1140ms | 10x baseline (2400ms) |
| Downstream | payments within SLO throughout | any breach aborts |

### Recovery
Capacity 12/12 at T+3:20; errors 0.3% (inside baseline + 0.4%); p99 262ms
(inside baseline + 12%); payments within SLO; held through the 2m settle
window. Verdict `RECOVERED`.

### Findings and next step
- Hypothesis did not hold: completion rate fell below 95% before the bound.
- Cascade beyond the target: a fourth replica went unready without being
  targeted. Investigate the shared dependency before widening the bound.
- Do not widen the blast radius; re-run the same contract once understood.
```

## Anti-patterns

The nine drill anti-patterns, each with why it fails and what to do instead, are
in [references/anti-patterns.md](references/anti-patterns.md): 100% blast radius,
deciding the abort threshold live, treating a documented rollback as verified,
skipping a gate for a window, injecting onto a degraded baseline, stale
telemetry, silent aborts, starting the next drill before recovery, and widening
a bound after a breach.

## Limitations

- **Gates reduce risk, they do not remove it.** The SRE test-induced emergency
  passed internal review and still took out dependent services because the
  dependency model was incomplete
  ([sre.google/sre-book/emergency-response][sre-emer]). A drill can always
  surface a coupling nobody knew about: that is the point, and the residual risk.
- **Non-production is a weaker signal than production.** Staging differs in
  traffic shape, data volume, and dependency versions, so a clean drill there is
  evidence, not proof. Production experiments are what
  [principlesofchaos.org][cp] prefers, and reaching them is a separate
  organizational decision, not an extension of this protocol.
- **The tolerances and intervals here are conventions.** The 10-second sampling
  interval, the "baseline plus 10%" recovery tolerance, and the five-minute
  recovery timeout are common practice, not standards. Replace each with a value
  derived from the system's own measured behavior.
- **Recovery validation confirms signals, not correctness.** Metrics returning
  to baseline does not prove data written during the fault is consistent.
  Correctness after a fault needs its own verification.
