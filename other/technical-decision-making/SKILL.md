---
name: technical-decision-making
description: "The single most useful question before analysing anything is: *what does it cost"
---

# Technical Decision Making (Verbose)

## Core Patterns

### Reversibility Governs Rigour

The single most useful question before analysing anything is: *what does it cost
to undo this?* Bezos framed it as one-way and two-way doors, and the framing
holds up because it maps directly onto how much process a decision deserves.

**Two-way doors** — reversible in days to a couple of weeks, with contained
blast radius:

- A logging library, an HTTP client, a test framework
- A caching layer added in front of an existing store
- CI provider, linting rules, formatter
- Anything behind a feature flag with a working kill switch
- An internal API you control both sides of

**One-way doors** — reversible only at high cost, or not at all:

- Primary datastore and its data model, once a year of writes has landed in it
- A public API contract with external consumers
- Programming language / runtime for a service that will grow
- A vendor holding customer data (exit cost is migration *plus* legal)
- Anything that alters data irreversibly (a destructive backfill)
- Organisational splits encoded in service boundaries

Two things make this harder than it looks. First, decisions can be *made*
two-way with modest effort: an adapter interface turns a vendor choice into a
two-way door; an anti-corruption layer does the same for a framework; versioning
an API from day one makes contract change reversible. Investing in reversibility
is usually cheaper than investing in certainty.

Second, doors close over time. Choosing Kafka on day one is fairly reversible.
Choosing Kafka after 40 services publish to it is not. The right question is not
just "is this reversible" but "how long until it isn't, and what should we learn
before then".

| | Two-way door | One-way door |
|---|---|---|
| Time to analyse | Hours | Days to weeks |
| Decider | The engineer doing the work | Team or tech lead, named owner |
| Evidence needed | Docs read, quick prototype | Spike with numbers, references, cost model |
| Written output | PR description | ADR with alternatives and consequences |
| Bias | Toward acting | Toward gathering evidence |
| Failure mode | Analysis paralysis | Expensive irreversible mistake |

The asymmetry matters: on a two-way door, deciding fast and being wrong costs
less than deciding slowly and being right, because the correction is cheap and
you learn from production rather than from speculation.

### The Weighted Decision Matrix

A matrix does not make the decision. It makes the *disagreement* explicit, which
is what unblocks a stuck team. Two engineers arguing about Kafka versus SQS are
usually not disagreeing about Kafka and SQS; they are disagreeing about how much
weight operational burden deserves relative to throughput headroom. The matrix
moves the argument to that question, where it can actually be resolved.

Worked example. Choosing a background job system for a Python API: ~200 jobs/sec
peak, jobs are 50–500 ms, existing Postgres 15 and Redis in the stack, 4
engineers, no dedicated ops.

Criteria and weights agreed *before* scoring:

| Criterion | Weight | Why this weight |
|---|---|---|
| Ops burden of new infra | 0.30 | 4 engineers, no ops; new infra costs us features |
| Team familiarity | 0.25 | Two engineers have shipped Celery; nobody has run Kafka |
| Delivery guarantees | 0.20 | Jobs post invoices; loss is visible to customers |
| Observability | 0.15 | Current pain: no visibility into stuck work |
| Throughput headroom | 0.10 | 200/sec today; 5x growth is the plausible ceiling |

Scoring 1–5, with the scale defined per criterion (5 on ops burden = no new
component; 1 = a new stateful cluster we must operate):

| Criterion | W | Celery+Redis | SQS+workers | Postgres queue | Kafka |
|---|---|---|---|---|---|
| Ops burden | 0.30 | 3 | 4 | 5 | 1 |
| Familiarity | 0.25 | 5 | 2 | 4 | 1 |
| Delivery guarantees | 0.20 | 3 | 5 | 4 | 5 |
| Observability | 0.15 | 2 | 4 | 4 | 3 |
| Throughput headroom | 0.10 | 5 | 5 | 2 | 5 |
| **Weighted total** | | **3.55** | **3.85** | **4.15** | **2.55** |

Reading it honestly:

- **Postgres queue wins (4.15)** largely because it adds nothing to operate and
  the team already knows Postgres. `SELECT ... FOR UPDATE SKIP LOCKED` is a
  well-trodden pattern at this scale.
- **SQS (3.85) is within 0.3** — that is inside the noise of subjective 1–5
  scoring. Treat the two as tied and decide on something the matrix does not
  capture (here: we want zero new IAM surface, so Postgres).
- **Kafka scores badly (2.55)** and the matrix shows exactly why: it is a
  log, not a job queue, and the team would be learning a stateful distributed
  system to solve a problem two simpler options already solve.
- Throughput headroom at 0.10 is doing almost nothing. That is correct — every
  option clears 200/sec — but it is worth noticing, because a criterion that
  cannot discriminate is decoration.

Rules for keeping this honest:

1. Agree weights before you score. Weights chosen after scoring are how people
   launder a preference into an analysis.
2. Define each scale. "3 on observability" must mean something specific.
3. Include the incumbent / do-nothing option. It often wins, and omitting it
   biases everything.
4. Cap at 5–7 criteria. Beyond that, everything gets a middling score and the
   totals converge.
5. If your preferred option loses, either change your mind or say which weight
   you think is wrong. Do not quietly re-score.

### Spike Before Deciding — But Only for the Load-Bearing Unknown

A spike is a time-boxed experiment to resolve a specific factual uncertainty. It
is not "let's play with it for a week". Every spike needs three things: the
question, the box, and the decision rule.

```markdown
## Spike: Postgres queue throughput
Question: Can `SELECT ... FOR UPDATE SKIP LOCKED` on db.r6g.large sustain
  200 jobs/sec claim-rate alongside current OLTP write load?
Time-box: 2 days.
Method: replay a production write trace, add synthetic job load, measure
  claim latency p99 and primary CPU.
Decision rule:
  - p99 claim < 20 ms and primary CPU delta < 15%  -> Postgres queue
  - otherwise                                       -> SQS
Result (2026-02-11): p99 claim 7 ms at 200/s, 340/s before p99 exceeded 20 ms;
  CPU delta 9%. -> Postgres queue. Headroom ~1.7x, below our 5x growth case,
  so recorded as a revisit trigger.
```

Decide without spiking when the options are similar in cost, the choice is a
two-way door, or the uncertainty is about *preference* rather than fact — no
experiment resolves "which API do we find nicer". Spike when a single number
would flip the decision and you do not have that number.

The failure mode is the spike as procrastination: no question, no box, no rule,
and at the end a team that feels informed but still cannot state why one option
won. If you cannot write the decision rule up front, the spike will not decide
anything.

### Writing Down What Would Change Your Mind

Record falsifiers at decision time. This is the highest-leverage habit in the
whole practice and the most commonly skipped.

```markdown
## Revisit triggers (ADR-0033, Postgres job queue)
- Sustained job rate > 500/sec for 7 consecutive days (measured: 1.7x headroom)
- Queue-wait p99 > 5s for 3 consecutive days
- Job table > 50M rows or vacuum falling behind
- A second service needs to consume the same job stream
Owner: platform. Reviewed at each quarterly architecture review.
```

Why up front and not later: after a system is built, everyone involved is
motivated to conclude it is still the right choice. Sunk cost is not a bias you
can talk yourself out of by being aware of it. A trigger written before you were
invested is evidence from a less biased version of your team.

It also disarms the retrospective argument. "We should never have used Postgres
for this" becomes a checkable claim: did a trigger fire? If yes, the decision was
sound and we should have acted on the trigger. If no, the complaint is aesthetic.

Wire triggers to something that observes them — a dashboard panel, an alert, a
recurring review — or they are just prose.

### Disagree and Commit

Teams need a way to stop deliberating that is neither consensus (too slow, and
it rewards whoever is most stubborn) nor authority alone (fast, but wastes the
dissent). Disagree-and-commit is that mechanism, and it has preconditions people
routinely skip.

It works when:

1. **There is a named decider**, known before the discussion, not discovered
   afterwards.
2. **Dissent is heard first.** Committing before objections are on the table is
   just compliance, and the objection resurfaces as passive resistance.
3. **The objection is recorded**, in the ADR, in the objector's words. This is
   the load-bearing part. It converts "I don't like this" into a specific
   prediction that can be checked.
4. **Commitment is real.** The dissenter implements the chosen option properly.
   No shadow prototype, no deliberate under-investment, no "well, I said so" in
   the incident review.
5. **New evidence reopens it; repetition does not.** Restating the same
   objection with no new information is not reopening a decision.

In the ADR:

```markdown
## Dissent
J. Okonkwo argued for SQS on the grounds that a Postgres queue couples job
throughput to primary-database health, so a slow query in the API can stall
fulfilment. Recorded and accepted as a known risk; mitigated by a separate
connection pool capped at 20 and a queue-wait alert. Reconsider if the coupling
causes any customer-visible incident.
```

That paragraph is worth more than the agreement that surrounds it. If a slow
query does stall fulfilment eighteen months later, the team does not argue about
who saw it coming — the mitigation and the reversal condition are already
written down.

### Sizing the Effort

A rough calibration for how much process a decision earns:

| Decision | Door | Effort | Output |
|---|---|---|---|
| HTTP client library | Two-way | 1 hour | PR description |
| Add a Redis cache | Two-way | Half day | PR + a note on invalidation |
| Job queue technology | Mostly one-way | 3–5 days + spike | ADR |
| Primary datastore | One-way | 1–3 weeks, spike required | ADR + review |
| Public API contract shape | One-way | 1–2 weeks | ADR + consumer review |
| Cloud provider | One-way | Weeks, exec involvement | ADR + cost model |
| Splitting the monolith | One-way | Months, incremental | ADR per boundary |

If a decision is taking effort wildly out of proportion to its row here, that
mismatch is the thing to fix first.

## Common Anti-Patterns

❌ **Treating every decision as irreversible.** Three weeks and four meetings to
choose a date library.
✅ Classify the door first. Two-way doors get decided by whoever is doing the
work, in hours.

❌ **Treating irreversible decisions as reversible.** The data model that will
carry two years of writes gets chosen in a PR at 6pm.
✅ One-way doors get a spike, a matrix, an ADR, and a second reader.

❌ **The reverse-fitted matrix.** Weights adjusted until the preferred option
wins, then presented as analysis.
✅ Fix weights before scoring. If your option loses, name the weight you think is
wrong and defend that instead.

❌ **The unbounded spike.** "Let's prototype it and see" with no question, box,
or decision rule; two weeks later the team knows more and has decided nothing.
✅ Write the question and the decision rule before you write any code.

❌ **No named decider.** Discussion circles until the most persistent person
wins, or until someone merges code that settles it by default.
✅ Name the decider up front. Ambiguous ownership does not avoid a decision, it
just makes the decision arbitrary.

❌ **Consensus as the bar.** Everyone must agree, so the team optimises for the
least objectionable option and takes weeks to reach it.
✅ Decider decides, dissent is recorded, everyone commits.

❌ **Committing without recording dissent.** The objection goes underground and
returns as half-hearted implementation or a shadow project.
✅ Write the objection into the ADR, in the objector's words, with a reversal
condition.

❌ **No revisit triggers.** The decision is either defended forever or abandoned
in a fit of frustration, both without evidence.
✅ Write the falsifier at decision time and put it on a dashboard.

❌ **Resume-driven selection.** The technology is interesting rather than
suitable; the matrix criteria quietly mirror its strengths.
✅ Derive criteria from the requirements before looking at any candidate.

❌ **Ignoring the do-nothing option.** "Should we adopt X" is asked without
"what if we keep doing what we do", which is often the highest-scoring row.
✅ Always score the incumbent.

❌ **Deciding with no exit cost estimate.** A vendor is chosen without anyone
asking what leaving would take.
✅ For any one-way door, write down the migration path out, even roughly.

## Technical Decision Making Checklist

- [ ] Reversibility classified: one-way or two-way door
- [ ] Effort proportional to that classification
- [ ] A named decider, agreed before the discussion started
- [ ] The do-nothing / incumbent option is on the list
- [ ] Criteria derived from requirements, not from a favoured candidate
- [ ] Weights agreed and written down before any scoring
- [ ] Each score scale defined so scores mean something
- [ ] Options within ~0.3 treated as tied, not as a winner
- [ ] Spikes have a question, a time-box, and a decision rule
- [ ] Spike results recorded, including the ones that changed nothing
- [ ] Exit cost estimated for anything hard to reverse
- [ ] Decision recorded as an ADR with alternatives and consequences
- [ ] Revisit triggers written at decision time, with numbers
- [ ] Triggers wired to a dashboard, alert, or scheduled review
- [ ] Dissent heard before commitment and recorded verbatim
- [ ] Everyone, including dissenters, implementing the chosen option properly
- [ ] Decision communicated to the people who must live with it
