---
name: coupling
description: Use when asking whether something should be one module or two — splitting a package, extracting a service, merging two, or why a simple area keeps breaking. Weighs shared knowledge, distance and volatility to place a boundary — not which layer layout a service uses (`hex-architecture`, `flat-layered`), nor module and import mechanics (`python-packaging`). - Should these two packages be one; do we need a contract here or can they share the model; how much structure does this component deserve; a change that keeps cascading into unrelated code; reviewing a diff for knowledge that leaked across a boundary.
---

# Coupling — where boundaries go and what may cross them

Every architecture skill in this set answers "given a boundary, what goes on each side, what is each
part called, and what may import what". This one answers the question *before* that: **where the
boundary goes, how much knowledge may cross it, and how much design effort the components on either
side deserve.** It is architecture-neutral — a hexagonal app, a flat-layered worker and a monorepo
of both get the same answers — and it is loaded *alongside* whichever architecture skill owns the
layout, never instead of it.

The vocabulary below — shared knowledge, distance, volatility, the counterbalance between them — is
**Vlad Khononov's Balanced Coupling model**, set out in *Balancing Coupling in Software Design*
(Addison-Wesley) and at [coupling.dev](https://coupling.dev). The model is his. What follows is this
catalogue's own restatement of it in this set's terms rather than a reproduction of his text, and where
the two differ the book is right. Read it for the full treatment — the continuous form of the balance
rule, the worked cases and the connascence detail all live there and are only gestured at here.

It absorbs the two older models rather than competing with them. Constantine's module coupling
supplies the rungs of the strength ladder — content, common/external/control, stamp and data coupling
are the classic names for intrusive, functional, model and contract. Connascence grades *within* a
rung: its static levels (name, type, meaning, algorithm, position) separate a weak contract from a
strong one, its dynamic levels (execution, timing, value, identity) separate degrees of functional
coupling. A team fluent in either keeps it — neither one weighs distance or volatility, which is the
gap this model fills and the reason rule 1 exists.

Coupling is not a defect to minimise. A set of components with no coupling achieves nothing
together — the connections are what make the parts a system. Every integration shares some
knowledge between its two sides, and the design questions are always the same three: *which*
knowledge is shared, *how far apart* the sides sit, and *how likely* either is to change. Get them
wrong and a change in one place breaks another in a way no single reader could have predicted; get
them right and changes stay local and boring. That unpredictability — not aesthetic ugliness — is
what "complexity" means here, and it is always a property of connections, not of components.

## When to use vs. neighbours

- Splitting or merging anything — two modules, two packages, two services, two systems → this skill.
- Deciding whether two components integrate through a contract or by sharing knowledge → this skill.
- Deciding how much design effort a component deserves, or why a "simple" area keeps breaking →
  this skill.
- Which architecture family a whole service belongs to — hexagonal or flat-layered →
  `architecture-choice`. It loads alongside this skill and costs its decision out using the volatility
  judgement below; this skill supplies that judgement but never picks the family.
- Which package a module belongs in *once the boundary is drawn*, and what it may import →
  `hex-architecture` (in the `pyhouse-hex` plugin) or `flat-layered` (in `pyhouse-flat`), whichever
  style the project uses.
- What the module is called → `naming`; how it is packaged, exported and imported — one class per
  module, `__all__`, `__init__.py`, relative vs absolute → `python-packaging`, which owns the mechanics
  of a boundary this skill has already decided to draw.
- Whether a specific dependency gets a `Protocol` → the architecture skill's own rule decides
  (`flat-layered`, in the `pyhouse-flat` plugin — no port before a second real implementation;
  hexagonal defines ports by default); this skill supplies the judgment that rule runs on.
- Reviewing a diff for knowledge that leaked across a boundary → this skill.

## The three dimensions

**Fix the level of abstraction before judging any of them.** The model is fractal — methods within a
module, modules within a service, services within a workspace, systems within a landscape all get the
same three questions — and the answers move with the level. A class's public interface is a contract
between two callers and an implementation detail one level up; a model shared by two objects inside one
module is model coupling at the object level and invisible at the service level. The same pair of
components reads as balanced or unbalanced depending on which level the reader had in mind, so name the
level first and classify second.

### Shared knowledge — how much one side must know about the other

Every integration works by the two sides knowing something in common. The less they must know, the
less likely a change in one forces a change in the other. Four levels, strongest to weakest:

| Level | What is shared | Shape it takes |
|---|---|---|
| **intrusive** | the other side's internals — its tables, private objects, undocumented behaviour | one service querying another's database; reaching into a module's `_private` helpers |
| **functional** | the other side's requirements — a rule both sides know, so both change when the rule does | a flag one component passes to steer another's branch; the same validation written in a client and again in a job over its output |
| **model** | the other side's domain model — entities and vocabulary, but not its rules | two components both importing one set of entity or table definitions |
| **contract** | an explicit interface only — what it does, never how | a repository method signature, a queue message schema, an HTTP endpoint |

Two properties of the ladder matter more than the labels. **Explicitness rises as strength falls**:
a contract is written down and greppable, while an intrusion can exist without the intruded-upon
side even knowing. And **strength is about cascades, not line count** — a two-line shared SQL
query can carry more coupling than a fifty-method interface.

One level deserves its own warning: **duplicated knowledge is functional coupling with no import to
show for it.** Two components implementing the same rule — the same retry policy, the same "what
counts as active", the same normalisation — are coupled even if neither imports the other, because
a rule change must land in both or the system quietly disagrees with itself. Imports are how you
*find* coupling; they are not what coupling *is*.

### Distance — what a coordinated change costs

Distance is the cost of changing both sides at once, and it climbs by level of separation: two
methods in one module are near; two packages in one service are farther; two services in one
workspace farther still; separate systems, and components owned by different people, are the
farthest. Three things add distance that code structure alone does not show:

- **Ownership.** Two components worked on by different people are farther apart than the same code
  structure owned by one — coordination is a cost even inside one repository.
- **Runtime.** A synchronous call is nearer than a queue: with sync, one side's failure and
  deployment freeze the other's; async raises distance and, with it, the required contract
  discipline.
- **Lifecycle.** The counterforce — components placed close together are tested, versioned and
  deployed together whether they like it or not. So distance is a trade, not a virtue: less of it
  means cheaper co-evolution and tighter lifecycles; more means freer lifecycles and dearer
  co-evolution. "Decouple" is not a direction, it is a price change.

Distance is **relative to the level being designed**: the highest distance available is the boundary
of that level. Within one service, the service boundary is that ceiling, so two packages sharing deep
knowledge inside a single deployable are exactly as unbalanced, at their own level, as two services
doing it across a network. Never excuse a boundary with "but it's all one process".

### Volatility — how likely the change is at all

Strength is the likelihood a change cascades; distance is its cost. Volatility is the probability
the change happens in the first place — and it decides whether an imbalance matters at all. A
badly-coupled component that never changes harms no one; the same component under constant change
is a standing emergency.

The honest estimator is the business domain, in DDD's terms:

- **Core** — the part the business competes on and keeps reshaping on purpose (pricing, matching,
  ranking). Highest volatility; this is where boundary mistakes actually bite.
- **Supporting** — needed, undifferentiated, no off-the-shelf answer: CRUD back-office, internal
  ETL, glue. Low volatility, and most of what most codebases contain.
- **Generic** — a solved problem with ready-made providers (auth, mail delivery, commodity APIs).
  The *function* is stable, but the *implementation* can turn over: providers get switched, run in
  parallel, replaced. Contract discipline here is proportional to how realistic the switch is — a
  commodity API with live rivals earns a narrow contract, while a sticky dependency (the main
  datastore, the identity provider) may not. That last one is an assumption to test, not to assert:
  name the plausible switch and price it before concluding it will never happen.

Distinguish **essential** from **accidental** volatility. Frequent commits can mean a volatile
domain — or a badly drawn boundary forcing every change to fan out, which is accidental volatility,
a *symptom* of the disease this skill treats, not an input to its diagnosis. And a quiet component
is not always stable: sometimes nobody dares touch it. Judge from the domain — would the business
*want* to change this if it were cheap?

## The balance rule

Strength and distance must **counterbalance** — one high, one low:

| | low distance | high distance |
|---|---|---|
| **low strength** | low cohesion — unrelated things sharing one boundary that names nothing; the cost is cognitive and it compounds | **loose coupling** — balanced |
| **high strength** | **high cohesion** — balanced; co-evolution is cheap because the sides are close | tight coupling — cascading changes at coordination prices; the distributed-monolith signature |

"Loose coupling" and "high cohesion" are not two goals to trade off; they are the same rule read
from its two ends. Volatility turns the rule into a budget:

```
modular  = strength XOR distance        (one high, one low)
balanced = modular OR NOT volatility    (or it simply will not change)
```

A supporting or generic component with an ugly shortcut is not a sin to apologise for — low
volatility neutralises the imbalance, and effort spent polishing it is effort taken from somewhere
it would have paid. Spend structure where change is *expected*: core subdomains first, and generic
dependencies whose provider is realistically replaceable.

## Applying it — the recurring decision shapes

### Split or merge?

The two failure modes of the table give both answers. Low strength + low distance — unrelated
things held together by a boundary that names nothing — merge them or separate them honestly; the
fake boundary costs cognition and protects nothing. High strength + high distance — do **not**
reach for a split reflexively: decomposition *raises* distance. Lower the strength (introduce a
contract) or lower the distance (co-locate), and choose by which kind of change you expect more of.

### Contract or shared knowledge?

What crosses a high-distance boundary crosses as a contract — explicit, named, owned. Components
integrate through whatever contract the boundary publishes — an endpoint, a message schema, a function
signature — and never through each other's internals. A client class translates its SDK's world into the service's
own types at the boundary, and `exception-catalog` does the same for errors.
A contract is worth exactly the distance it serves — an interface in front of a same-module call is
ceremony, and ceremony is how this rule gets a bad name.

### How much effort does this component deserve?

In proportion to volatility, not to the engineer's caution. A core subdomain earns the full
armour — layers, ports, contract discipline. A supporting workflow gets the flat shapes and is
allowed its shortcuts. A generic dependency gets a narrow contract exactly when a provider switch
is a realistic change vector; this is the judgment `flat-layered`'s "second real implementation" rule
(in the `pyhouse-flat` plugin) runs on — a commodity dependency with a credible, nameable alternative
is where a port stops being anticipatory, and a sticky one rarely reaches that bar. Structure added
anywhere else is cost without a buyer.

### Naming a boundary — encapsulated knowledge and change vectors

Before creating a module, a package or a whole workspace member, be able to write two things:

1. **Encapsulated knowledge** — what this component knows that no other may assume: which tables it
   owns, which upstream it speaks, which vocabulary it defines. If nothing can be named, there is
   no boundary — only a category word, which is `naming`'s vague-noun failure at a larger scale.
2. **Change vectors** — two or three plausible changes that would touch *only* this component. A
   boundary is drawn where change is expected to stop; if every plausible change drags a sibling
   along, the boundary is in the wrong place and no amount of interface discipline will save it.

Both are two sentences in the PR description, not documents. Their value is at creation time: they
are the cheapest possible test of a boundary, run before any code exists to be coupled.

### Worked example — a library's public surface

A library's importers sit at the highest distance it has — separate repositories, separate release
cycles — so what they import is a contract: the names its root re-exports, versioned, and nothing
else. Its internals sit at the lowest distance and may share model knowledge freely. The same
counterbalance decides a CLI's command modules against the work they call, several services sharing
one store, and two functions in one file.

## Rules

1. **Never judge a boundary on one dimension.** Strength, distance and volatility, every time. A
   review that counts imports has measured a shadow of one of them.
2. **Name the level of abstraction before classifying anything.** What counts as a contract, and
   what counts as far apart, are both properties of the level being designed, not of the code. An
   unstated level is how two readers reach opposite verdicts on the same pair of components.
3. **Never "just decouple".** Decomposition raises distance and buys lifecycle freedom you may not
   need. Every split or merge proposal states which imbalance it fixes and what price the new
   distance charges; one with no strength-and-distance reasoning behind it is fashion, not design.
4. **Judge volatility from the domain, not the commit log.** Commit frequency conflates essential
   volatility with accidental volatility — the latter is a finding about the boundaries, not an
   input to drawing them.
5. **Effort follows volatility.** The depth of structure a component gets — ports, layers, contract
   discipline — is proportional to how likely the business is to change it, which is a property of
   the domain, not of the engineer's caution. Low volatility is a licence, not a debt: a pragmatic
   shortcut in a supporting or generic component is a decision with a reason, and polishing it is
   effort misallocated from the core.
6. **What crosses a high-distance boundary crosses as a contract.** Intrusive knowledge — tables,
   private objects, undocumented behaviour — across a service or ownership boundary is the worst
   square on the board, with nothing to neutralise it but luck. A contract that is inconvenient is
   fixed, or the distance lowered; it is never bypassed.
7. **Duplicated knowledge is coupling even with zero imports.** A rule implemented twice must
   change twice; that is functional coupling wearing camouflage, and grep will not find it for you.
   A business rule is owned once and shared, never written a second time.
8. **A boundary must have nameable encapsulated knowledge and survive its change vectors.** The
   two-sentence test at creation time: knowledge that cannot be written in one sentence is only a
   category word, and a boundary every plausible change crosses is drawn where change does not stop.
   On failure, merge or redraw — do not proceed and hope.
9. **Strength and distance counterbalance — one high, one low — wherever volatility is expected.**
   High knowledge shared at high distance — one service reading another's tables, two services
   mutating one shared model — is the distributed-monolith signature: lower the strength with a
   contract or lower the distance by co-locating, and do not split reflexively. Unrelated components
   held together by a boundary that names no knowledge is low cohesion: merge them or split them for
   real.

## Hard stops

- Asked which family a whole service belongs to — whether it gets ports and layers at all → stop, use
  `architecture-choice`; this skill supplies the volatility judgement and never picks the family.
- Asked which package a module goes in once the boundary is drawn, or what it may import → stop, use
  `hex-architecture` (in `pyhouse-hex`) or `flat-layered` (in `pyhouse-flat`), whichever the project
  uses, or the project's own layout where neither applies.
- Asked what a module is called, or how it is exported and imported → stop, use `naming` or
  `python-packaging`.
