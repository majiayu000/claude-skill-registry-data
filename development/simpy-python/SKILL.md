---
name: simpy-python
description: Use for writing, reviewing, debugging, testing, or analyzing Python SimPy discrete-event simulations. Trigger on Environment, Event, Process, timeout, Resource, PriorityResource, PreemptiveResource, Container, Store, queues, interrupts, simulation clocks, replications, or SimPy monitoring. Do not use for asyncio services, wall-clock schedulers, continuous ODE solvers, or Monte Carlo code without an event-process model.
argument-hint: "[SimPy model, process, queue, experiment, or error]"
---

# SimPy Python

Build reproducible discrete-event models whose clock, state transitions,
resource ownership, stopping rule, randomness, and observations represent the
real system rather than an accidental execution order.

## Boundary and core objects

| Object | Meaning | Use it for |
|---|---|---|
| `Environment` | Scheduler, simulation clock, and event queue. | One simulated world/replication. |
| `Event` | A future state that becomes triggered, processed, and optionally carries a value/failure. | Synchronization and completion signals. |
| `Process` | An event wrapping a generator's lifecycle. | Active entities that yield events. |
| `Timeout` | An event scheduled after simulated delay. | Duration, not wall-clock sleep. |
| `Resource` family | Capacity tokens with queues. | Exclusive/shared service and congestion. |
| `Container` | Homogeneous numeric level. | Bulk inventory or fuel. |
| `Store` | Queued Python objects. | Items, messages, or jobs with identity. |

A process function is a generator recipe; `env.process(generator)` registers it
and returns a `Process` event. `yield event` suspends simulated activity until
that event is processed. Calling a generator normally does not run the model.
Read [the event and process model](references/event-model.md) before mixing
callbacks, interrupts, conditions, or resource requests.

## Ordered workflow

1. Define the question, time unit, warm-up, horizon/stopping event, and measured
   population before modeling implementation details.
2. Separate domain state from the environment and random-number generator.
3. Express every delay, wait, acquisition, release, failure, and cancellation as
   an event transition.
4. Select `Resource`, `Container`, or `Store` from what is constrained—not by
   superficial queue vocabulary.
5. Record observations at defined transitions and with clear denominators.
6. Run independent replications with controlled seeds; report uncertainty, not
   one trace, when making stochastic claims.
7. Test tiny deterministic timelines, contention, boundary times, interruption,
   empty/full queues, and the stopping rule.

## Decision rules

- Use `Resource` when entities compete for interchangeable usage slots. Use a
  `with resource.request() as request: yield request` block so ownership is
  released on normal exit or interruption.
- Use `PriorityResource` when waiting order follows an explicit priority. State
  whether lower numeric values mean higher priority and define tie behavior.
- Use `PreemptiveResource` only when an admitted user can be interrupted. Handle
  `simpy.Interrupt`, remaining work, cleanup, and measurement bias.
- Use `Container` for an aggregate quantity without item identity. Use `Store`
  when objects and selection/filtering matter.
- Use `env.timeout(duration)` for simulated time. Reject negative durations and
  define whether zero delay is a legitimate same-time event.
- Use `env.any_of`/`event1 | event2` for races and `all_of`/`&` for barriers.
  Inspect which events completed; a losing event may still need cancellation or
  cleanup.
- Use `env.run(until=t)` knowing events scheduled exactly at `t` are not a vague
  “through time t” promise; write a boundary test for the chosen stopping form.
- Use `RealtimeEnvironment` only when coupling to wall-clock behavior is an
  explicit requirement. It is not a way to make simulation more accurate.

Read [resources, time, and experiments](references/modeling.md) for ownership,
queues, monitoring, randomness, and replication rules.

## Canonical anchor

```python
from collections.abc import Generator
from dataclasses import dataclass

import simpy


@dataclass(frozen=True)
class Visit:
    customer: int
    queued_at: float
    started_at: float
    finished_at: float


def customer(
    env: simpy.Environment,
    server: simpy.Resource,
    customer_id: int,
    service_time: float,
    visits: list[Visit],
) -> Generator[simpy.Event, object, None]:
    queued_at = env.now
    with server.request() as request:
        yield request
        started_at = env.now
        yield env.timeout(service_time)
        visits.append(Visit(customer_id, queued_at, started_at, env.now))
```

The record captures state-transition times rather than sampling a mutable queue.
Arrival creation and random service draws belong outside this process so a test
can inject a deterministic schedule.

## High-risk rules

- Do not mutate state “after a delay” without yielding that delay.
- Do not hold a resource while waiting for unrelated work unless the real entity
  occupies it during that time.
- Do not manually release a context-managed request twice.
- Never share one mutable RNG implicitly across replications. Derive and record
  per-replication seeds; common random numbers require an intentional design.
- Avoid global `random` calls inside processes. Inject distributions or an RNG.
- A queue-length time average requires time weighting between changes; averaging
  observations at arrivals answers a different question.
- Distinguish censored entities still in the system at the horizon from
  completed entities. Do not silently discard them from denominators.
- Same-time events are ordered by scheduler rules and creation sequence. If the
  answer must not depend on that order, encode priorities or redesign the event.
- An interrupted process must release resources and decide whether work resumes,
  restarts, or is lost. Catching and ignoring the interrupt is not a model.

## Version grounding and completion

The authoring baseline is official SimPy 4.1.2 stable documentation; the local
foundry has not yet executed the package. Check the installed version with
`simpy.__version__` and inspect signatures before relying on exception fields, resource variants, or
environment behavior. Read [verification](references/verification.md).

Completion requires an explicit clock/stopping contract, correct resource
ownership, injected randomness, traceable observations, deterministic
micro-tests, stochastic replication checks where relevant, and evidence that
the result does not depend accidentally on global state or one seed.

## References

- [Event and process model](references/event-model.md)
- [Resources, time, and experiments](references/modeling.md)
- [Verification and grounding](references/verification.md)
