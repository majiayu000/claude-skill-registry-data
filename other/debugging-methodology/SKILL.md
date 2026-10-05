---
name: debugging-methodology
description: "Debugging is the scientific method under time pressure."
---

# Debugging Methodology (Verbose)

## Core Patterns

### The Diagnostic Loop

Debugging is the scientific method under time pressure. The loop is: observe a
fact, form a hypothesis that explains it, design the cheapest experiment that
can *disprove* the hypothesis, run it, update.

The step engineers skip is designing the experiment. They jump from hypothesis
straight to a fix, and a fix that appears to work confirms nothing — it may have
perturbed timing, masked the symptom, or been irrelevant to a bug that is
intermittent anyway.

Keep a running log. It costs seconds and stops you re-testing the same theory at
hour three:

```
FACT   17:02  500s began 16:40, exactly at deploy of a3f19c2.
FACT   17:05  Only /checkout. /cart and /orders are clean.
HYP-1  Serialiser regression in a3f19c2.
TEST   Revert a3f19c2 in staging, replay the failing payload.
RESULT Still fails. HYP-1 DEAD.
FACT   17:20  Staging fails too — so it is not traffic volume.
HYP-2  Data-shape dependent: fails only for carts with a null variant.
TEST   Construct one cart with a null variant, one without.
RESULT Null variant reproduces at 100%. HYP-2 LIVE.
```

Two properties make an experiment good: it is **discriminating** (its two
possible outcomes point at different causes) and it is **cheap** (seconds, not a
deploy). Prefer a query over a deploy, a local call over a query, a unit test
over all of them.

### Binary Search Over Space

A request crosses many components. Rather than tracing it end to end, test the
midpoint and discard half the system.

```
client → CDN → load balancer → API → cache → database
                                ↑
                        check here first
```

If the API access log shows the request with a 200, everything to its left is
fine and the problem is downstream. One observation, half the system eliminated.
Repeat: about three checks to isolate one component in an eight-hop path.

The same trick works inside a process — bisect by removal:

```bash
# 30 middlewares, one is dropping the auth header. Disable half.
MIDDLEWARE_DISABLE="$(sed -n '1,15p' middleware.list | paste -sd,)" ./run-repro.sh
```

If the bug persists, it is in the enabled half; if it vanishes, in the disabled
half. Feature flags, plugin lists, and config blocks all bisect the same way.

### Binary Search Over Time

When the code used to work, the failing change is findable in logarithmic time.

```bash
git bisect start
git bisect bad HEAD              # known broken
git bisect good v2.14.0          # known working
# git checks out the midpoint. Test it, then report:
git bisect good                  # this revision is fine
git bisect bad                   # this revision is broken
git bisect skip                  # unbuildable — exclude it
git bisect reset                 # done; return to your branch
```

Automate the verdict and walk away. Any command whose exit status is 0 for good
and non-zero for bad will do:

```bash
git bisect run pytest -x tests/test_checkout.py::test_null_variant
git bisect run ./scripts/repro.sh          # exit non-zero when it reproduces
```

Two cautions. First, have a custom script exit 125 to mean "cannot test this
revision" — bisect treats that as a skip rather than a verdict. Second, if the
last good revision is weeks back, bisect over merge commits first
(`git bisect start --first-parent`) to find the offending merge, then bisect
inside that branch.

If the bug is likely in one file's history, narrow the candidates before you
bisect at all: `git log -S'connection_pool'` finds commits that changed the
number of occurrences of a string, and `git log -L :price_cart:engine.py` shows
the history of a single function.

### "It Works on My Machine"

Treat this as a successful experiment, not an excuse. You have two systems, one
passing and one failing, and the bug must live in their difference. The work is
to enumerate and shrink that difference:

| Axis | How to compare |
|---|---|
| Runtime version | `python -V`, `node -v` on both |
| Dependency graph | Diff the lockfile, not the manifest |
| Environment | `env \| sort` on both, then diff |
| Data | Row counts, nulls, encodings, one real failing record |
| Config | Diff the rendered config, not the templates |
| Clock / locale | Timezone, `LANG`, DST edges |
| Network | Egress rules, proxies, DNS resolution |
| Build | Debug vs release, optimisation level |

Then bisect the diff: move one axis of the working machine toward the broken one
until it breaks. That axis is the cause. Containers help by shrinking the diff
in advance, but they do not eliminate it — the host kernel, mounted data, and
injected secrets still differ.

### Reading a Stack Trace

Three questions, three places to look.

```
Traceback (most recent call last):
  File "app/api/checkout.py", line 88, in post          <- your code: the entry point
    total = price_cart(cart)
  File "app/pricing/engine.py", line 41, in price_cart
    return sum(line_total(l) for l in cart.lines)
  File "app/pricing/engine.py", line 52, in line_total
    return item.variant.price * item.qty               <- your code: deepest frame you own
  File "site-packages/orm/proxy.py", line 210, in __getattr__
    raise AttributeError(...)                          <- library frame: where it surfaced
AttributeError: 'NoneType' object has no attribute 'price'
```

- *What broke?* The innermost frame and the exception message. Here: something
  is `None` where a variant was expected.
- *Where did the bad value come from?* The deepest frame in **your** code —
  `engine.py:52`. Library frames below it are usually just the messenger.
- *Why was it called?* The outermost of your frames — the entry point and its
  inputs, which you need in order to reproduce.

For chained exceptions, the block after `The above exception was the direct
cause of` (or Java's `Caused by:`) holds the original failure; the outer layers
are wrapping. Read to the *first* cause.

Async and threaded traces are truncated at the scheduling boundary — the frames
that queued the work are absent. Propagate a request id through a context
variable, or you will get a trace that starts at the event loop and tells you
nothing about who asked.

### Minimal Reproduction

A bug you can reproduce in one file is a bug you have nearly explained. Shrink
aggressively:

1. Fix determinism first — pin the seed, freeze the clock, use one fixed input
   record. An intermittent repro cannot be shrunk, because you cannot tell
   "removed the cause" from "got lucky".
2. Cut breadth: one request instead of load, one row instead of the table, one
   service instead of the mesh.
3. Cut depth: replace the framework with a direct call, the database with a
   literal, the queue with a function call.
4. After each cut, re-verify it still fails. If it stops failing, the thing you
   just removed is implicated — put it back and keep it.

This is delta debugging done by hand, and tools automate it (`creduce` for C,
property-test shrinkers such as Hypothesis for the input space). The shrunken
case becomes the regression test, so the effort is never wasted.

### Choosing Your Instrument

| Situation | Reach for | Why |
|---|---|---|
| Fast local repro, tangled state | Interactive debugger | Inspect everything, step, mutate, retry |
| Production, cannot pause | Structured logging | No stop-the-world; queryable after the fact |
| Latency or causality across services | Distributed tracing | Spans show where the time and the failure went |
| Intermittent, low frequency | Sampling profiler / always-on tracing | Catches the rare event without a repro |
| Hang or deadlock | Thread/stack dump of the live process | Shows what every thread is blocked on |
| Hard crash | Core dump + post-mortem debugger | The only surviving state |
| "Something changed" | Metrics diff around the deploy | Cheapest first look, always |

Conditional breakpoints beat stepping when the failure is on iteration 40,000:
break on `cart.id == 88213` rather than holding down continue. Log at the
boundaries you cannot step across — process edges, network calls, queue handoffs
— and carry a correlation id so lines from different processes can be joined.

### Heisenbugs

A heisenbug changes or disappears when you observe it. The mechanism is real,
not mystical: a log statement adds I/O and a lock, allocation shifts memory
layout, a debugger halts one thread while others run on, and a debug build
disables the optimisation that exposed the race.

If instrumentation makes the bug vanish, you have learned something concrete —
it is timing- or layout-sensitive, which points at data races, unsynchronised
shared state, uninitialised memory, or use-after-free. Adapt the technique:

- Observe from outside the process — tracing, `strace`, packet capture, kernel
  counters — so you do not perturb the window.
- Record cheaply inside a hot path: a fixed-size ring buffer written without
  locks, dumped only on failure.
- Use tools built for the class: thread and address sanitizers, race detectors,
  deterministic record/replay.
- Increase pressure rather than visibility: more concurrency, slower disks,
  injected latency, fewer cores. Make the race *more* likely, then catch it.

Never "fix" a heisenbug with the sleep or the log line that made it go away.
That converts a reproducible failure into a rare one that will return in
production at a worse time.

### Handing Off

Live diagnosis ends when the defect is understood and mitigated. The systemic
question — why the class of bug was possible, and why detection took as long as
it did — belongs to the postmortem process (`root-cause-five-whys`), and the
minute-by-minute record belongs in `incident-timeline-creation`. Do not try to
run all three at once during an outage; capture facts with timestamps as you go
so the other two are cheap afterwards.

## Common Anti-Patterns

❌ **Changing code to see what happens.** Shotgun edits produce a system that
works for unknown reasons and will break again.
✅ State a hypothesis and the expected result before editing anything.

❌ **Making several changes at once.** When it passes, no single change is
credited, and you carry three unexplained edits forward.
✅ One variable per experiment.

❌ **Reading only the exception's top line.** The message says what surfaced,
not what caused it.
✅ Find the deepest frame you own and the first "caused by".

❌ **Debugging where the symptom appeared.** The trace shows where the bad value
exploded, not where it was created.
✅ Trace the value backwards to its origin.

❌ **Dismissing "works on my machine".** It is a passing control in an
experiment you have already run.
✅ Enumerate and bisect the environment difference.

❌ **Never shrinking the reproduction.** A ten-minute end-to-end repro caps how
many hypotheses you can test per hour.
✅ Spend twenty minutes making it a ten-second test; you will get it back.

❌ **Adding `sleep` or retry until the failure stops.** The race is still there,
now rarer and harder to catch.
✅ Fix the synchronisation or the ordering assumption.

❌ **Bisecting by hand across hundreds of commits.**
✅ `git bisect run` with a scripted verdict.

❌ **Trusting memory over a written log.** By hour two you will re-test a dead
theory and argue about whether you already tried it.
✅ Keep the fact/hypothesis/result log in the incident channel.

❌ **Stopping at the first plausible explanation.** Plausible is not verified.
✅ Confirm by prediction: the theory must say what happens when you change X,
and it must be right.

❌ **Ignoring a fact that does not fit.** The one unexplained observation is
usually the whole bug.
✅ A correct theory accounts for every fact, including the inconvenient one.

## Debugging Checklist

- [ ] Symptom stated precisely — what, when it started, for whom, how often
- [ ] Reproduction exists and is deterministic
- [ ] Reproduction shrunk toward a single file / single input
- [ ] Current hypothesis written down and falsifiable
- [ ] Next experiment is the cheapest one that splits the space
- [ ] One variable changed per experiment
- [ ] Fact/hypothesis/result log kept as you go
- [ ] Stack trace read to the deepest owned frame and the first cause
- [ ] Recent changes checked; `git bisect run` used if it is a regression
- [ ] Environment diff enumerated when only some machines fail
- [ ] Instrument chosen deliberately: debugger, logs, tracing, or dump
- [ ] Timing sensitivity considered before adding in-process logging
- [ ] Explanation accounts for every observed fact, not just the loudest
- [ ] Fix verified by prediction, not only by the symptom going away
- [ ] Shrunken reproduction committed as a regression test
- [ ] Systemic cause handed to the postmortem process, not fixed and forgotten
