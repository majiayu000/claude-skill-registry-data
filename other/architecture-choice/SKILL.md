---
name: architecture-choice
description: Use when deciding whether a service should be hexagonal or flat-layered — a greenfield service whose family is unsettled, or an existing one that has outgrown the style it was built in. Decides from what the service itself must enforce, names what each choice costs, and states plainly which project shapes this catalogue does not cover rather than forcing one into a family. Routes to `hex-architecture` or `flat-layered` and teaches neither style; where a boundary goes at all is `coupling`'s. - Also fires on "which architecture for this service", "should this be hexagonal", "do we need ports here" and "is a plain layered layout enough", and on asking whether the catalogue's families fit a Django or Flask project, a package-by-feature tree, a library or SDK, a CLI tool, an orchestrator-shaped data-pipeline project, or a modular monolith.
---

# Architecture Choice — hexagonal, flat-layered, or neither

Which of the catalogue's two service-architecture families a service belongs to, settled before any
code exists. This skill decides and hands off: the layer contract, the package layout and every
artifact template belong to the family skill it routes to, and the question *where a boundary goes at
all* belongs to `coupling`. Both families assume the codebase chooses its own layout; where something
else already fixes it, this skill names the shape as uncovered instead of routing.

It is a universal skill, so it **names** the two family skills without requiring either. Everything
needed to reach a recommendation and state its reason is here; the family skills carry the how. See
`## Reading this with neither family installed`.

## When to use vs. neighbours

- A new service, no code yet, and the family is not settled → this skill.
- The family is settled as hexagonal — the four layers, dependency direction, ports, adapters, the
  composition root → `hex-architecture`, in the `pyhouse-hex` plugin.
- The family is settled as flat-layered — packages named for technical roles, no ports until a second
  implementation → `flat-layered`, in the `pyhouse-flat` plugin.
- Where a boundary goes at all — split or merge, contract or shared knowledge, how much design effort
  a component deserves → `coupling`. It loads alongside this skill and supplies the volatility
  judgement the cost question below runs on.
- Whether one particular dependency earns a `Protocol` → the chosen family's own rule decides; this
  skill chooses the family, not the port.
- Which trigger a flat service runs on — loop, schedule, stream, a thin HTTP wrapper, durable
  execution → `flat-entrypoint`,
  in the `pyhouse-flat` plugin.
- A workspace holding several services → `python-workspace` owns the workspace root; the
  family is still chosen once per service, here.
- Reviewing an existing service against the style it already has → not this skill; load that family's
  skill directly.
- A script, a single-purpose job, a one-shot migration → too small for either family; see
  `### Too small for either family`, and do not route to a family skill.
- A Django or Flask project, a package-by-feature tree, a library or SDK, a CLI tool, an
  orchestrator-shaped data-pipeline project, a modular monolith → outside this catalogue's two families; see
  `### Project shapes this catalogue does not cover`. Name the shape rather than routing to the nearer
  family. A CLI tool's commands, exit codes and their test are still `python-cli`'s. A CLI tool is a
  program its users install and run against inputs they choose; a program that does a service's work
  against a store or an upstream the team runs, started by a command, is a service of its family with
  a command trigger (`python-cli` rule 7).

## The question that decides it

Both answers below route into a family. If the project's shape is already fixed by a framework, an
orchestrator or a packaging form, read `### Project shapes this catalogue does not cover` first.

> **Does this service have business invariants of its own that it must enforce?**

A business invariant is a rule about what is *valid* that this codebase owns and must refuse to
break — not a payload shape, and not an upstream's rule being relayed. Its signature is a constructor
that rejects its own arguments: one raise per rule, checked in one place, because a rule enforced at
the call site is a rule the next call site forgets. A worker that validates a payload against a schema
and moves on has enforced nothing of its own; it has checked that someone else kept their contract.

- **Yes — the rules about what is valid live in this codebase and are its reason for existing.**
  Hexagonal. The layer split exists to keep those rules testable and changeable without touching a
  database, a queue or a framework.
- **No — the service orchestrates external systems, and its correctness is whether the data moved;
  or it serves requests over data it stores without rules of its own.** Flat-layered — what the
  literature calls package by layer, after Simon Brown, with what Fowler calls transaction scripts
  above it. There is nothing to protect, so the protection would be cost with no buyer, and choosing
  flat is not a compromise. A service of the second kind answers HTTP through `flat-entrypoint`'s
  HTTP shape, in the `pyhouse-flat` plugin.

Answer this first. It settles most services on its own. Everything below either confirms that answer
or flips a genuinely borderline one; nothing below outweighs it.

## Confirming evidence

Five more questions, each with what a "yes" implies. They are **evidence, not points**: they are not
commensurable and they do not sum, so three weak hexagonal signals do not outvote a clear "no
invariants".

**Does the service own a noun?** — a thing it creates, identifies independently of its field values,
and mutates over a lifetime while it stays the same thing. Yes → hexagonal; that noun is an aggregate,
and identity, lifecycle and construction-time rules all attach to it. A service that reads records
from one system, transforms them, writes them to another and owns no noun at all is the flat case in
its purest form. A noun that is only stored and served — records created, read and updated over
HTTP with nothing about them the service refuses — does not flip a "no" to the deciding question; it
stays flat.

**Will more than one entrypoint drive the same rules?** — REST plus a queue consumer plus a CLI, all
reaching the same logic. Yes → hexagonal, and strongly: a shared core with two callers is exactly what
ports exist to protect. One entrypoint is neutral, not evidence for flat.

**Does any outward dependency have a second real implementation, or credibly about to?** — judged from
the domain rather than from caution: a commodity dependency with a nameable alternative the business
could plausibly adopt qualifies; a sticky one — the main datastore, the identity provider — does not,
however generic it looks. If every port would have exactly one implementation forever and no second is
in prospect, that is evidence the ports are ceremony. It is evidence about ports rather than about the
family: a hexagonal service defines ports by default and does not need this answer to be yes.

**Is the part that keeps changing the rules, or the integrations?** — a core subdomain, the part the
business reshapes on purpose, is where the indirection earns its keep. A supporting or generic
workflow — internal glue, undifferentiated ETL — changes little, so an imbalance there costs nothing
and structure spent on it is taken from somewhere it would have paid. `coupling` owns this judgement
and the budget it turns into.

**Who calls it?** — the weakest signal, and never decisive on its own. A synchronous caller expecting
a response and an error contract correlates with hexagonal; a schedule, a queue or a stream correlates
with flat. Both correlations break easily: a flat service may expose a small HTTP surface — a thin
wrapper around the functions that do its work, which is `flat-entrypoint`'s HTTP trigger shape in `pyhouse-flat` —
and a hexagonal service may run entirely on a worker entrypoint. Nothing about a trigger implies durable
execution either — for flat services the default for scheduled work is a plain loop, a cron entry or a
timer, and a workflow engine is earned separately (`flat-entrypoint`, in `pyhouse-flat`).

## What each choice costs

Name both costs when recommending. A choice presented without its price is not one the reader can
disagree with.

**Hexagonal pays a structural price.** A protocol for every outward dependency, an adapter
implementing each one, a composition root that is the only place concrete classes are bound, DTOs
translated at two boundaries, and a layer split every new module has to be placed into. It buys rules
that are testable without a database and survive an infrastructure change untouched. **A service with
no rules pays that price and gets nothing back** — that asymmetry is the whole reason the flat family
exists.

**Flat pays by having no seam to hold a rule still.** When the first rule appears it lands in whichever
module needed it first, and the second caller copies it; two components then share knowledge with no
import to show for it, which is the coupling failure that is hardest to see in review. It buys the
shortest path from a trigger to the work — one concrete class per external system, direct construction,
no indirection to read through.

Neither cost is a defect. Spend structure where change is expected, and nowhere else.

## The cases that are not the two clean ones

### Too small for either family

A single-file script, a lambda whose whole body is one function, a one-shot migration, a couple of
modules run once and deleted. **Say so and route nowhere: you do not need an architecture skill for
this.** Write the script.

The universal skills still bind, and they are the whole of what applies — every universal skill whose
subject the script has, `python-versioning` among them only the day it is distributed to anyone, which
most scripts never are. Reaching for either family here produces
packages with nothing in them and a reviewer who assumes work lives there.

Run this skill again when the script stops being one: a second trigger, a second reader of the same
logic, or the first rule someone must not break.

### Project shapes this catalogue does not cover

Both families are **service** architectures, and both assume the layout is this codebase's to choose.
A project whose shape a framework, an orchestrator or a packaging form has already fixed is outside
them. These are the ones that come up in Python:

- **A framework-dictated layout** — Django apps, Flask blueprints. The framework owns the package
  shape, and the ORM models are the persistence and the rules at once.
- **Fat models carrying real invariants**, with no appetite for a protocol and an adapter per
  dependency. The rule belongs in one place and that place is a model method. This shape answers the
  deciding question "yes" and is still not hexagonal.
- **Package by feature, or vertical slices** — one package per feature holding its own router,
  schemas, service functions and queries. A deliberate alternative to both families, not a degenerate
  form of either.
- **A library, an SDK or any distributed package.** No entrypoint and no deployment; the public API is
  the only boundary that matters. It is not a script either, so the section above does not reach it.
- **A multi-command CLI tool**, where the command tree is the structure. Its commands, their exit codes
  and their test are `python-cli`'s, which gives no layout for a large command tree either.
- **A data-pipeline project shaped by its orchestrator** — Airflow, Dagster, Prefect. The DAG or asset graph
  dictates the directories, and that tool's conventions outrank anything here.
- **An ML or research project** — notebooks, experiment scripts, training and evaluation runs.
- **A modular monolith** — one deployable with enforced boundaries between internal modules. The
  catalogue's workspace skill covers a monorepo of separate services, which is a different thing.

**Name the shape and say plainly that this catalogue does not cover it.** Do not route to the nearer
family and do not supply a layout — there is none here to give, and a hexagonal layer split dropped
into a framework's tree fights the framework at every file.

The universal skills still bind in full — every universal skill whose subject the project has — and
they are not a consolation prize; they are the rules that were never architectural in the first
place. Where the framework dictates a module's name and contents — Django's `models.py` and
`admin.py` — the framework's convention wins, and `python-packaging` says so itself. The deciding
question is still worth answering, because knowing whether the project owns invariants tells the reader what to
protect. It just selects no family here.

Run this skill again if a service is carved out of the project: a deployable with its own entrypoint
and its own reason to exist is back in scope, and the choice is made for that service alone.

### Real invariants *and* heavy integration work

Recommend hexagonal. The reason is an asymmetry, not a preference: **the flat family has no answer for
invariants** — no place to put a rule where it stays testable and unduplicated — **while the hexagonal
family has an answer for integrations**, one adapter per external system behind a port
(`hex-capability-adapter`, in `pyhouse-hex`). A mixed service that chooses flat has to invent the missing half; one that
chooses hexagonal uses a skill that already exists.

### Flat now, invariants later

The likeliest real trajectory, and not a failure of the original choice. The migration signal is
specific: **the first domain rule that two entrypoints, or two jobs, both need.** One caller
needing a rule is a function; two needing the same rule is a domain with nowhere to live.

Move incrementally rather than rewriting: extract the rule, then the protocol it needs, then the
orchestration above it, leaving the concrete clients in place as adapters. The step-by-step procedure
is `hex-architecture`'s `## Moving code between layers`, which arrives with `pyhouse-hex`; the
signal above is what this skill owns, and it is enough to know that the migration is due. Do not take the structure before the rule arrives — flat → hexagonal is additive,
which is exactly what makes waiting cheap.

### A monorepo holding both

**The choice is per service, never per repository.** `python-workspace` lays a workspace
root that hosts several members; nothing about a shared root, a shared schema package or a shared toolchain requires
the members to share an internal layout. One member that owns `Foo` and enforces its invariants can
be hexagonal while the flat workers beside it stay flat, and the workspace is not inconsistent for it. Run this skill once per
member, at the point that member is created.

### The earlier choice was wrong

- **Flat → hexagonal is additive and normal.** The layers arrive beside the existing packages, one rule
  moves at a time, the clients become adapters, and most of the code survives. Do it when the signal
  above appears.
- **Hexagonal → flat is a demolition and rarely worth it.** Ports deleted, layers collapsed, wiring
  rewritten, and every test that substituted a protocol goes with them. A hexagonal service with no
  invariants is over-structured, not broken, and over-structure costs reading time — cheaper than a
  rewrite. Do it only when the structure is actively blocking the work, never because an audit found
  the invariants missing.

## Reading this with neither family installed

This skill ships in `pyhouse-universal`, which installs alone. The decision above is complete without
either family skill present: the question, the confirming evidence, both costs and all six cases are
stated here, and the recommendation is usable as written.

What a family skill adds is the *how* — the layer or role layout, what may import what, and the file
templates. To get it, install the plugin the recommendation names, from the `pyhouse` marketplace:

- **Hexagonal** → `pyhouse-hex`, which carries `hex-architecture` and the rest of the `hex-*` family.
- **Flat-layered** → `pyhouse-flat`, which carries `flat-layered` and the rest of the `flat-*` family.
- **Neither** — too small, or a shape this catalogue does not cover → nothing to install. The
  universal skills already beside this one are the answer.

Both family plugins depend on `pyhouse-universal` and Claude Code enables the dependency transitively,
so installing one keeps everything here.

## Rules

1. **Answer the invariants question first, and let it decide.** The other questions are read after it,
   to confirm or to flip a borderline case. A family chosen before that question is answered was chosen
   on something else. No invariants is flat, and that is the answer, not a concession; real invariants
   are hexagonal however heavy the integration work beside them, because flat has no answer for
   invariants and hexagonal has one for integrations.
2. **Never score the criteria.** No points, no weights, no tally. The criteria are not commensurable,
   and a total lets a reader accumulate weak signals into an answer the deciding question already
   refused.
3. **Name the invariant, or accept that there is none.** State the rule in one sentence — what is
   valid, and what the service refuses. A rule that cannot be written in a sentence is not yet an
   invariant, and "there might be rules later" is never one: flat → hexagonal is additive, so the
   structure is taken when the rule arrives, not in anticipation of it.
4. **Decide per service, never per repository, and give each service exactly one family.** A workspace
   is not a family, and a service is hexagonal or flat, never both — no `domain/` package beside role
   packages, no ports with one implementation each in a flat service.
5. **State the cost of the choice alongside the choice.** Both families have one, and a reader deciding
   needs the one they are buying named.
6. **Record the answer and its reason where the service's readers will find it** — a sentence or two in
   the service's own README or agent instructions, the same cheap form `coupling` asks for when a
   boundary is drawn. The next person's default is to copy the layout, and a layout with no stated
   reason gets copied into a service that does not warrant it.
7. **Re-run the decision on an event, not on a schedule.** The events are the first rule two callers
   share, a second entrypoint over the same logic, and a dependency gaining a second real
   implementation. An audit finding a working hexagonal service has no invariants is not one:
   over-structure costs less than the demolition, so hexagonal → flat is recommended only when the
   structure is actively blocking the work.
8. **When neither family applies, say so and route nowhere.** Two different cases end the same way —
   a project too small to need an architecture, and one whose shape this catalogue does not cover.
   Name what does apply and stop. Handing a script an architecture is as wrong an outcome as handing a
   rules-heavy service the wrong family, and routing an uncovered shape to the nearer family is worse
   than either, because the layout it lands in is one nothing else in the project expects.

## Hard stops

- A script, a lambda body or a one-shot migration is being given an architecture → stop, it needs none;
  name the universal skills and finish.
- A project whose layout a framework, an orchestrator or a packaging form already fixes — a Django or
  Flask tree, a package-by-feature service, a library, a CLI tool, an Airflow or Dagster project, a
  modular monolith — is being assigned hexagonal or flat → stop, this catalogue does not cover that
  shape; name it, name the universal skills — `python-cli` among them for a CLI tool — and finish.
- This skill is being asked for the layer contract, the package layout or a file template, or to review
  a service against the family it already has → stop, use `hex-architecture` or `flat-layered` —
  install `pyhouse-hex` or `pyhouse-flat` if it is absent.
- Asked where a boundary should go, or whether two components split or merge → stop, use `coupling`.
- Asked for the root of a workspace holding several services → stop, use `python-workspace`; the family
  is still chosen here, once per member.
