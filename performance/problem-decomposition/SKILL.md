---
name: problem-decomposition
description: "A stakeholder asks to make search faster."
---

# Problem Decomposition (Verbose)

## Core Patterns

### A Worked Decomposition: "Make Search Faster"

A stakeholder asks to make search faster. As stated this cannot be started,
finished, or verified. Decomposition is the work of converting it into a tree
whose leaves each have an owner, a size, and a number that says when they are done.

**Step 1 — Make the root falsifiable.**

```
❌ "Make search faster"
✅ "p95 latency of GET /search for authenticated users drops from
    3.2s to under 800ms, without reducing result relevance
    (measured by click-through at position 1-3)."
```

The negative constraint matters as much as the target. Without it, the fastest
search is one that returns nothing, and someone will eventually optimize toward
exactly that.

**Step 2 — Spike before splitting.** Do not decompose a performance problem
along guessed lines. One day of measurement:

```
p95 = 3.2s, decomposed by span:
  app handler      210ms   ( 7%)
  database query  2600ms   (81%)
  serialization    180ms   ( 6%)
  network/TLS      210ms   ( 7%)
```

This single measurement kills three plausible workstreams. "Move rendering to
the client" has a ceiling of 180ms against a 2,400ms gap — it cannot succeed
even if executed perfectly. Amdahl's law is the sharpest decomposition tool
available: compute each branch's ceiling before staffing it.

**Step 3 — The tree.**

```
ROOT: p95 /search < 800ms, CTR@1-3 not down more than 2%
│
├── B. Database query: 2600ms → under 500ms          [ceiling: 2.6s ✔]
│   ├── B1. Add GIN trigram index on search_index.title
│   │       Done when: EXPLAIN ANALYZE shows Bitmap Index Scan,
│   │                  not Seq Scan, and query p95 < 400ms
│   │       Size: half a day.  Risk: index build locks writes → use
│   │             CREATE INDEX CONCURRENTLY
│   ├── B2. Bound the result set
│   │       Now: unbounded; p99 request materializes ~40k rows
│   │       Done when: keyset pagination, LIMIT 50, rows fetched < 100
│   │       Size: 2 days.  Depends on B1 (ordering must be index-backed)
│   └── B3. Cache facet counts
│           Done when: facet computation < 20ms p95 at 5-min TTL
│           Precondition to verify: facet values change < 1/5min
│
├── C. Serialization: 180ms       [ceiling: 180ms — defer]
├── D. Network: 210ms             [ceiling: 210ms — defer]
└── A. App handler: 210ms         [ceiling: 210ms — defer]
```

Deferring C, D, and A is not laziness; it is the decomposition doing its job.
Solving B alone reaches roughly 3.2s − 2.1s = 1.1s… which still misses the 800ms
target. That is worth knowing *now*: the tree tells you B is necessary but not
sufficient, and that C+D+A must eventually yield ~300ms combined. A decomposition
that cannot tell you this is not earning its keep.

### Work Backwards From the Output

Forward decomposition ("first we need a database, then…") reliably produces work
that turns out to be unnecessary. Backward decomposition starts from the artifact
and asks what must exist immediately prior.

```
The user sees: 50 ranked results in under 800ms
        ← a scored, ordered candidate set
              ← a retrieved candidate set (recall step)
                    ← an index queryable by term
                          ← a normalized document corpus
```

Each arrow is a candidate boundary, and each node has an obvious "is it right?"
test independent of the ones below it. You can validate ranking quality against
a hand-built candidate set before the index exists.

### Find the Seam

The test of a proposed split is whether you can write down what crosses the
boundary. If you can name the type, it is a seam; if you can only gesture at
"the search stuff", it is a wish.

```
✅ Seam — writeable as a contract:
   def retrieve(query: str, limit: int) -> list[DocId]
   def score(query: str, docs: list[DocId]) -> list[ScoredDoc]

   Two engineers can now work in parallel against a stub. The scoring
   engineer builds against a hardcoded DocId list on day one.

❌ Not a seam:
   "You take the backend performance, I'll take the frontend performance"

   Both need the same latency budget negotiated, both change the same
   response payload shape, and neither can verify their half alone.
```

### Vertical Slices Over Horizontal Layers

The most common decomposition failure is splitting by architectural layer,
because the layers are the most visible lines on the whiteboard.

```
❌ Horizontal
   Sprint 1: all schema migrations
   Sprint 2: all repository + service code
   Sprint 3: all API endpoints and UI
   → Nothing is demonstrable until sprint 3. Every wrong assumption
     made in sprint 1 is discovered in sprint 3, at maximum rework cost.

✅ Vertical
   Slice 1: single-field search, no facets, no paging, 10 hardcoded
            docs, real path through DB → service → endpoint → UI
   Slice 2: real index, still no facets
   Slice 3: paging
   Slice 4: facets
   → Integration risk is retired on day 3. Slices 3 and 4 can be cut
     entirely if the metric is already met.
```

The vertical slice is deliberately embarrassing in scope. That is the point: it
proves the path, not the product. See `incremental-implementation` for carrying
slices into code.

### Spike the Unknown First

Sequence by uncertainty, not by dependency order and not by what is easy to
start. The purpose of ordering is to buy information as cheaply as possible.

A well-formed spike states a question, a timebox, and what each answer implies:

```
Question: Can Postgres trigram search return p95 < 400ms at 12M rows
          on our current instance class?
Timebox:  2 days
If yes:   B1 proceeds; the tree above holds.
If no:    the whole B branch is replaced by "introduce a search engine",
          which is a 6-week project, not a 3-day one — and we need to
          know that before committing to the quarter.
```

Note the asymmetry: the spike costs 2 days and can save 6 weeks of misdirected
work. Spikes that cannot change the plan are not spikes, they are early
implementation.

### "What Would Have To Be True?"

Given a plan, enumerate the conditions required for it to work, then test the
cheapest and shakiest condition first. This finds fatal flaws before they are
expensive.

```
Plan: cache facet counts for 5 minutes (B3)

What would have to be true?
  1. Facet values change less than ~once per 5 min
       → check the write rate: 10-minute query. THIS FIRST.
  2. Stale facet counts are acceptable to users
       → one question to product
  3. Cache memory fits the facet cardinality
       → back-of-envelope: 200 facets × 8KB = 1.6MB. Fine.

Condition 1 turned out false — inventory writes ~40/min during
business hours. B3 is dropped for 30 minutes of investigation
instead of a week of implementation.
```

### Detecting Hidden Dependencies Between "Independent" Parts

Parallel sub-problems are the payoff of decomposition, and false independence is
the way that payoff evaporates. Two branches assigned to two people are only
independent if all of these hold:

| Check | Question | Failure smell |
|---|---|---|
| Data | Do both write the same table or key? | "We'll just merge the migrations" |
| Schema | Does either change a shared type or contract? | Both edit the same response model |
| Order | Does one need the other's output to *test*? | "I'll verify once yours lands" |
| Resource | Do both consume the same budget (latency, memory, quota)? | Two 300ms budgets, one 400ms allowance |
| Deploy | Must they ship together to be correct? | A flag that must flip for both at once |

The latency-budget case is the one teams miss most often, because it looks like
a resource conflict rather than a code conflict. In the worked example, B2 and
B3 both consume the same 500ms query budget. Solved separately and measured
separately, each looks successful; combined they can still miss. The fix is to
assign explicit sub-budgets up front — B1+B2 ≤ 400ms, B3 ≤ 20ms — and make each
leaf's done condition its own budget, not the global target.

For decomposing a *failure* rather than a *goal*, use `root-cause-five-whys`;
for turning a decomposition into scoped tickets, use `feature-planning`.

## Common Anti-Patterns

❌ **Decomposing before measuring** — the tree is built on guesses about where
time or complexity lives, and its branches have no ceilings.
✅ Spend one day measuring first. Compute each branch's maximum possible
contribution before staffing it.

❌ **Sub-problems with no done condition** — "improve the query layer",
"clean up search."
✅ Every leaf names a measurement: "EXPLAIN shows Index Scan and query p95 <
400ms."

❌ **Splitting by layer** — schemas this sprint, services next, UI after.
✅ Cut vertical slices that go end to end, however narrow.

❌ **Assuming independence because two people were assigned** — both branches
land, both pass their own tests, and the integration misses the target.
✅ Run the five-way check (data, schema, order, resource, deploy). Assign
explicit sub-budgets for shared resources.

❌ **Uniform decomposition depth** — every branch expanded to the same level of
detail regardless of risk.
✅ Expand the uncertain and expensive branches deeply; leave known-cheap ones as
single leaves.

❌ **A one-level list called a decomposition** — five bullet points with no
structure or dependency.
✅ If nothing has children and nothing has a ceiling, you have a to-do list.

❌ **Spikes that become the implementation** — the timebox passes silently and
the prototype ships.
✅ State the timebox and both branch outcomes before starting. Delete the spike
code.

❌ **Optimizing a branch with a ceiling below the target** — six weeks moving
a 180ms component against a 2,400ms gap.
✅ Check the ceiling first. A branch that cannot succeed at 100% is not a branch.

## Decomposition Checklist

- [ ] Root restated with a metric, a baseline, and a target number
- [ ] Negative constraint recorded (what must not get worse)
- [ ] Measurement or spike completed before the tree was built
- [ ] Each branch has a computed ceiling; branches below target are dropped
- [ ] Each leaf has a done condition containing a number
- [ ] Each leaf is small enough to finish in about a day
- [ ] Boundaries are seams — the crossing type is written down
- [ ] Slices are vertical; at least one goes end to end early
- [ ] Highest-uncertainty item is sequenced first and timeboxed
- [ ] "What would have to be true" answered for the shakiest assumption
- [ ] Parallel branches checked for shared data, schema, ordering, budget, deploy
- [ ] Shared resource budgets split explicitly per leaf
