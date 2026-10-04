---
name: sourcer
category: simulation
tier: D
description: "Crawl a set of sites into a verified entity graph — companies, the people who run them, the relationships between them — where every claim points at the bytes it came from and nothing expands until it verifies. Agents read pages that are already on disk and return byte spans; a fetch daemon is the only thing that may put bytes there, so fabricating evidence is not a callable path rather than something a check must catch. Twelve gates run over what the run left on disk, eleven of them fail closed, and the suite proves itself each time by planting known-false claims its own gates must reject. Use it to supply the entities and edges that parallax and data-provider have no source for. USE WHEN map a company, who runs this company, find the relationships between these organisations, crawl this site into a graph, build an entity map, sourcer, recursive search, whole-site traversal, sitemap crawl, extract entities and relationships, verified crawl, expand only what verifies. NOT FOR reading one page you already have the URL of (fetch it); general web research you will read rather than model (just search); anything needing recall guarantees, which this deliberately does not publish; and anything that needs the crawled claims to be TRUE rather than verifiably stated — no crawler can establish that."
triggers:
  - map a company
  - crawl this site into a graph
  - build an entity map
  - who runs this company
  - sourcer
  - expand only what verifies
effort: high
---

# sourcer

`parallax` runs an accepted ontology forward. `data-provider` turns findings into
the table parallax ingests. Both are machines with no fuel: something has to
supply the entities and the relationships in the first place. This is that
layer.

It crawls a set of sites into a graph of organisations, people and the relations
between them — and it is built so that the result is worth trusting **without
the operator checking it**, because a map you have to hand-verify is one you may
as well have built yourself.

## What it guarantees, stated exactly

> A page at this URL, held at this digest, verifiably says this.

The precise wording is the value. It does **not** guarantee that what the page
says is true. Nothing in this architecture binds bytes to reality and no
crawler's can: an inflated title, a phantom advisory board, a shell company
listing a nominee director each produce a fully green `observed` claim. That is
a strong, checkable guarantee and it is not omniscience, and a reader who
confuses the two will be misled by a perfectly honest map.

## The two rules everything else follows from

**Record everything.** Nothing is deleted. A refuted claim is kept *with its
refutation attached*, because a reader can filter what it can see and cannot
filter what was discarded. Quarantine is a marked partition, never a `DELETE`.

**Expand only what verifies.** Only `observed AND entailed` records seed the next
hop. Without this the first rule is ruinous — one hallucinated company at hop two
spends the whole fetch budget on its imaginary descendants.

## How fabrication is made impossible rather than detected

Crawl agents get **no network tool and no write access to the snapshot store**.
A separate fetch daemon is the only thing that can put bytes on disk. So an
agent cannot produce a citation to a page it invented; there is no call it could
make. Three further devices remove whole classes of lying rather than checking
for them:

- **An entity's name is the bytes.** A mention is a *kind* and a *byte span*; the
  name is whatever sits at those offsets and the canonical key is recomputed
  from it. There is no field in which to write a name, so there is nothing to
  write falsely.
- **A relation is a bounded span containing both mentions.** "Not mere
  co-mention" is hard to judge and easy to measure: the relation's span must
  contain both endpoint spans *and* be at most 600 bytes. A company in the header
  and a person in the footer can satisfy the first and can never satisfy both.
- **Byte offsets, not substring search.** `bytes.find(quote)` lets a producer
  pick the needle after seeing the haystack; an offset is a location it had to
  commit to before the check ran.

The custody split is what makes the second signature worth anything. The daemon
attests *these bytes came from this URL*; the extractor attests *this claim came
from these bytes*; the verifier attests *these bytes support this claim*. Three
propositions with genuinely disjoint upstreams, rather than one claim signed
three times.

One honest limit: the tool-surface half of that split is a **deployment
property**. It holds because the crawl agents are defined without a network
tool, and it is the one part of the architecture the gate set cannot verify
about itself from the inside.

## Install

```bash
git clone https://github.com/broomva/skills
cd skills/skills/simulation/sourcer
export SOURCER_CHAIN_KEY="$(openssl rand -hex 32)"   # required; see below
```

The chain key is not optional and there is no default. The fetch log is an
HMAC-keyed chain, not a plain hash chain: a plain chain is recomputable by
anyone who can read the log, which makes it evidence against accident but not
against someone routing around it. An unkeyed chain verifies and proves nothing,
so the daemon refuses to construct without a key.

## Run it

The workflow drives the whole cycle:

```
Workflow({ scriptPath: "<skill>/workflows/depth-loop.js",
           args: { scripts: "<skill>/scripts",
                   seeds: ["https://example.com/"],
                   maxDepth: 2, budget: 40,
                   run: "/tmp/crawl/r1", db: "/tmp/crawl/map.db" } })
```

Or drive the four verbs directly. `take` and `land` are separate commands
because the agent's work sits between them:

```bash
python3 scripts/sourcer.py plan   --run RUN --db DB --seed https://example.com/ \
                                  --max-depth 2 --budget 40
python3 scripts/sourcer.py take   --run RUN --db DB        # -> a path to read
python3 scripts/sourcer.py land   --run RUN --db DB --url … --digest … \
                                  --depth … --token … --claims c.json --verdicts v.json
python3 scripts/sourcer.py status --run RUN --db DB

# and the three that turn a finished map into something downstream can use
python3 scripts/sourcer.py resolve --run RUN --db DB   # identity candidates
python3 scripts/sourcer.py emit --run RUN --db DB      # -> parallax propose ...
python3 scripts/sourcer.py project --run RUN --db DB --entities <entities-dir>
python3 scripts/gates.py          --run RUN --db DB --json  # 0 VALID, 2 INVALID
```

`--verdicts` maps a **claim index** to true or false — not a record id, because
ids are derived during admission and the verifier runs before it. A `true`
entails the whole claim; a `false` refutes only the edge, since the entities may
be named correctly on a page that does not state the relation between them.
A claim with no verdict stays `unchecked`, which is not a synonym for
`inconclusive` and is emphatically not permission to expand.

## The loop

```
claim -> fetch -> extract -> verify -> expand
                               |
                         refuted stops here
```

Verification is a stage **inside** the per-node pipeline, not a pass at the end.
In a batch model a fabricated node at hop two has seeded fifty descendants before
anyone checks it, and the refutation arrives with a subtree hanging off it. Here
the refutation prunes before the subtree exists — the same checks, a very
different blast radius.

Recursion is expressed as a depth loop rather than as recursion, because the
workflow substrate permits one level of nesting and a node therefore cannot spawn
a sub-workflow for what it discovers. Breadth-first falls out of that.

A crawl moves from one entity to the next through exactly one route: a verified
`profile` node's name is a URL read out of the page, and that URL enters the
frontier. There is no argument in which the loop is handed somewhere to go.
Letting an extractor return "discovered" URLs would put the crawl's whole
trajectory in the model's gift.

## The gates

Twelve gates, five stages, eleven fail closed.

| Stage | Gate | On failure |
|---|---|---|
| ingest | `plan-sealed-and-log-chained` | closed |
| ingest | `transport-custody` | closed |
| per node | `record-admissible` | closed |
| per node | `span-verbatim` | closed |
| per node | `span-entails-claim` | closed |
| per edge | `edge-admissible` | closed |
| per edge | `triple-entailed` | closed |
| whole map | `lattice-exact` | closed |
| whole map | `inventory-closed` | closed |
| whole map | `corroboration-grade` | annotate |
| pre-ship | `projection-fidelity` | closed |
| pre-ship | `gate-suite-proven` | closed |

`corroboration-grade` annotates and never gates: it did not survive attack, since
two outlets reprinting one press release corroborate each other. It still marks
single-sourced claims, because "how much of this rests on one page" is a real
question.

Three properties keep the suite from being decoration, each aimed at a failure
this workspace has actually shipped:

- **Recorded denominators.** Every gate reports how many items it examined.
  Passing at zero is often correct — a map with no edges has no inadmissible
  edges — so the rule is not "never zero" but that a zero denominator must carry
  a stated reason, enforced where a new gate cannot forget it.
- **A gate that could not run is not a pass.** `inconclusive` is its own status
  and makes a fail-closed run `INVALID` exactly as a failure does. Reading "no
  verifier configured" as "nothing to object to" would turn the two judgement
  gates into decoration.
- **The suite proves itself every run.** `gate-suite-proven` puts 25 probes
  through the deterministic gates — 18 planted decoys they must reject and 7
  honest maps they must accept — and requires **both polarities per gate**, not
  in aggregate. The accepting half is not ceremony: a gate that fails everything
  rejects every decoy, so decoys alone could be satisfied by breaking the gate
  rather than by it working. Counting the accepting half globally was its own
  hole — an always-failing gate passed all of its own decoys while other gates
  supplied the suite's accepting total.

## What is in the box

| Path | What it owns |
|---|---|
| `scripts/store.py` | records, verdicts, the frontier and its leases |
| `scripts/fetchd.py` | the only writer of bytes; the HMAC-keyed chain; robots.txt |
| `scripts/traverse.py` | `robots.txt` → sitemap → a bounded page set |
| `scripts/extract.py` | typed `(subject, predicate, object)` over a closed vocabulary |
| `scripts/loop.py` | the depth loop; verification before expansion |
| `scripts/gates.py` | the twelve gates, the probes, and the CLI |
| `scripts/identity.py` | exact keys merge; everything softer becomes an edge |
| `scripts/emit.py` | the node + edge tables Parallax ingests |
| `scripts/project.py` | the map as Layer-3 entity pages |
| `scripts/sourcer.py` | `plan` · `take` · `land` · `status` · `resolve` · `emit` · `project` |
| `workflows/depth-loop.js` | the agent orchestration |

```bash
PYTHONDONTWRITEBYTECODE=1 SOURCER_CHAIN_KEY=test python3 -m pytest tests/ -q
```

## What leaves the map

Two handoffs, and both refuse to say more than the map does.

**`emit` → Parallax.** A node table and an edge table, in the `--table` grammar
`data-provider` already owns — **imported, never re-spelled**, because two
spellings of one contract is the drift that keeps both sides green while they
agree with neither. If `data-provider` is absent this refuses rather than
falling back to a local copy, since the fallback *is* the second spelling. Only
`entailed` rows go, the observed/simulated grade survives into the proposal, and
an edge whose endpoint did not ship is dropped **and counted** — a table
asserting a relation between two things it does not contain says more than the
map does.

**`project` → `research/entities/`.** One page per observed, entailed node,
each carrying the URL, digest and byte span its claim was read from, and each
stamped `generated: sourcer` with "do not edit by hand" — a projection is
regenerable, so a hand edit is a claim with no evidence behind it. Simulated
records do **not** project: a page is what a later reader cites, and an
inference cited as a page loses its grade on the way. Dry-run by default,
because writing into a permanent shared graph is not something a command should
do because you forgot a flag.

## Identity

`resolve` proposes; it never merges. Two records with the same canonical key are
already one entity — the store merged them at birth. Two that merely *look*
alike become a `possibly_same_as` edge, and the asymmetry is the whole design:
**a wrong merge is much harder to notice than a missing one.** A missing merge
is two nodes a reader can see and join; a wrong merge silently attributes one
company's leadership and subsidiaries to another, and the evidence for both now
hangs off one id.

Every proposal is `simulated` — no page says two records are the same entity —
so `expandable()` refuses to let one spend the fetch budget on descendants. A
similarity score is not evidence.

Comparison is token overlap after stripping accents and legal forms, not edit
distance, because the failure that matters is the one edit distance gets
backwards: `Banco Agrario` and `Banco Agrícola` are two banks a few characters
apart, while `Nacional de Café` and `Café Nacional` are one company in a
different order.

## Known limits, named rather than discovered later

- **Recall is not guaranteed and no recall number is published.** The map covers
  what the sitemaps listed and the budget reached. `inventory-closed` tells you
  every page that *was* fetched is accounted for; it cannot tell you what was
  never found.
- **`span-entails-claim` and `triple-entailed`'s judgement half need a model.**
  Run without a verifier, those gates are `inconclusive` and the run is
  `INVALID` — deliberately, rather than quietly green.
- **Social profiles are out of reach here.** They are browser-session-bound and
  serial; this skill's daemon speaks plain HTTP.
- **`possibly_same_as` is an edge, not a merge.** Only exact-key identity merges
  automatically, because a wrong merge is much harder to notice than a missing
  one.
- **The vocabulary is closed and small.** A predicate outside it is refused
  rather than stored loosely, which means a relation the vocabulary cannot
  express is a relation this skill will not record.
- **A refuted relation leaves its endpoints `inconclusive`, not `entailed`.**
  The relation being unstated does not make the entities misnamed, but nobody
  settled that either — so they are kept, reported, and excluded from every
  handoff and from the next hop.
- **Conflicting re-sightings are retained and carry no verdict of their own.**
  Every gate that reads a verdict reads the canonical record; the structural
  gates see everything, because a conflict payload is a record that exists.
- **The lease is narrowed, not fenced.** `land` authorises before it mutates and
  re-checks immediately before touching the frontier, so a worker whose lease
  died cannot expand someone else's item. It is still a check followed by a
  write, and closing that properly needs one transaction spanning the whole of
  `land` — which the store does not offer across a process boundary. What a
  lapsed lease can still do is admit records, and that is deliberate: records
  are content-addressed, and `put_record` records a differing re-sighting as a
  **conflict** that `select()` returns and `payloads_held` counts. Nothing is
  lost, which is the whole point of *record everything*.
- **Profile keys are unversioned.** The key shape is `profile::<slug>-<digest>`
  with no version marker, so changing the derivation invalidates any store
  written by an earlier build. That is acceptable only because nothing has
  shipped; the first release that people run against a persisted map needs a
  key version or a migration.
