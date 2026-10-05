---
name: init-project
description: Use this skill to turn an idea into a structured new repo. It runs a trigger gate (throwaways and single scripts skip it), a value gate over fed-in discovery, records a foundation (an ADR plus a reference.md golden path), authors a walking-skeleton spec via new-spec and hands the build to work-loop, then hands off to the normal build loop. Triggers on "start a new project", "greenfield init", "idea to repo", "bootstrap a new codebase". Do NOT use inside an existing repo (use adapt-to-project) or to author one feature (use new-spec).
---

# Skill: init-project

The greenfield front door. An idea arrives and there is no repo yet — no
foundation recorded, no first slice built. The temptation is to *yolo* a
throwaway prototype, get it sort-of working, then retrofit structure and lose
the rationale. This skill gives that path a home: it turns an idea into a
structured repo by **composing the skills the repo already owns**. It
orchestrates; it does not reinvent, and it is **not** an autonomous code
generator — the human stays in the loop and the existing skills do the work.

It is the twin of `adapt-to-project` (the brownfield front door, for an
*existing* repo). Both converge on the same downstream loop:
`brief → reference.md → spec → low-level design → work-loop`.

## When to invoke

Invoke when the unit of work is a **brand-new repo from an idea** and there are
real **stack / structure / tooling decisions** ahead — a service, a library, a
multi-component app someone will maintain. The tells: "start a new project",
"bootstrap this idea into a repo", "we're greenfielding X".

Do **not** use it when:

- You are inside an existing codebase → `adapt-to-project` is the brownfield
  front door.
- You want to author one feature from scratch → `new-spec`.
- The thing ahead is a script, a spike, or a throwaway with no real structural
  decisions → the **trigger gate** (stage 1) sends it straight to scaffolding;
  don't force the flow onto it.

## The flow — five phases, fluid not waterfall

The five stages below are **fluid phases of attention, not a waterfall**. You
revisit them as understanding firms up — authoring the walking skeleton
routinely sends you back to amend the foundation, and that's the flow working,
not failing. Each phase practises a **scoped handoff**: it passes the next phase
only the artifacts that phase needs, nothing more.

The skill **composes** existing skills and assets by *reference* — it names them
and hands off to them; it never restates their procedures and never imports
their code.

### 1. Trigger gate — run this first

Before any other work, decide whether the flow even applies:

- **Real stack / structure / tooling decisions ahead?** (Which runtime? How is
  it partitioned? What's the persistence and transport story?) → **continue** to
  stage 2.
- **A script, a spike, or a throwaway?** → **scaffold it directly and skip the
  rest of this skill.** The flow's ceremony is wasted on code nobody will
  maintain.

Worked example. *"A 40-line script to rename files in a folder"* → no
architecture decisions → skip the flow, just write the script. *"A webhook
ingestion service with a queue, a worker, and a datastore"* → real decisions →
continue.

### 2. Value gate — over fed-in discovery

Discovery is **fed in**, never performed here (see anti-patterns). Consume a
discovery shape from one of four upstream sources:

- the `research` skill's output (when the `research` pack is installed),
- an `intent` shaped by `frame-intent` (when the `product-engineering` pack is
  installed) — its `frame → de-risk → decompose` loop hands its leaf in here: at
  `app` scale a feature-level leaf intent *is* a `core` brief,
- a provided PRD, or
- a brief produced by `receive-brief`.

The `product-engineering` source is **optional upstream**, named the same way the
`research` source is — "when the pack is installed". A `core`-only adopter has the
other three and reads this one as a clearly-optional source, not a dangling
reference.

From that input, derive the **business value** and the **MVP**: what outcome
this serves and the smallest thing that delivers it. **Gate on it** — if you
cannot state the business value plainly, *pause and send discovery back
upstream* rather than guessing. Don't paper over a thin idea with a plausible
mission.

The phase's output is the first **brief** (`docs/product/briefs/<slug>.md`, the
artifact `receive-brief` owns) — the *what / why* that the rest of the flow and
the downstream loop read. Hand that brief forward; nothing else.

### 3. Foundation — decide the stack, record the rationale

Choose the stack and architecture, and **record the decision with its
rationale** — a foundation you can hold later work to. Two artifacts:

- **An ADR** capturing *what* you chose, *why*, the *alternatives* weighed, and
  a *re-evaluation date*. A stack chosen with no recorded rationale is the thing
  to stop and fix before going further.
- **`docs/architecture/reference.md`** — the normative golden path (constraints,
  solution strategy, building blocks, cross-cutting standards). Instantiate it
  from the arc42 `reference.md` template the `adapt-to-project` skill bundles
  (the same golden-path template its reference-architecture harvest fills) —
  here you fill it forward from a decision rather than harvesting it from
  existing code. The core methodology stays stack-neutral; the chosen stack is
  *yours*, recorded in your ADR and your `reference.md`. If the project will
  deploy, this is also the moment to record the **deployment platform** and
  **where verification tooling will live** in the `reference.md` slots (and the
  matching one-liners in the `AGENTS.md` infra block) — optional grounding the
  work-loop infra preflight reads if present, never a prerequisite.

Hand the foundation forward as the steering every later design conforms to.

### 4. Walking skeleton — author the spec, hand the build to work-loop

Author a **walking skeleton**: a thin, end-to-end slice that links the main
architectural components — the smallest thing that exercises the real wiring
(an inbound request reaching a real datastore through the real transport, say),
not a sketch and not a throwaway. It is **kept and minimal**, held to a real
feature contract.

- Author it as a **single spec via `new-spec`** — one thin slice, with its own
  acceptance criteria and `Shape:`.
- **Hand the build to `work-loop`.** This skill orchestrates; `work-loop`
  executes. Do not build the skeleton here — that would duplicate the loop the
  repo already owns.

If building the skeleton reveals the foundation was wrong, go back to stage 3
and amend it — that's the fluid-phase posture, not a failure.

### 5. Handoff — into the normal build loop

From the skeleton onward, the project runs the ordinary loop:
`brief → spec → low-level design → work-loop`, with `reference.md` in place for
every feature's low-level design to conform to. The greenfield front door has
done its job: a recorded foundation, a validated walking skeleton, and the
normal loop running — instead of a throwaway someone has to clean up later.

## Anti-patterns to refuse

- **Performing discovery / research yourself.** Discovery is fed *in* (stage 2)
  from the `research` pack, an `intent` from `frame-intent` (when
  `product-engineering` is installed), a PRD, or a `receive-brief` brief. This
  skill consumes a discovery shape; it does not own the research phase and does
  not shape product intent itself.
- **Building an autonomous multi-agent "software company" generator.** The human
  stays in the loop and the existing skills do the work. The wins of a swarm of
  agents auto-generating a codebase are survivorship-bias stories; the boring,
  composed, human-in-the-loop path is the one that ships maintainable code.
- **Forcing the flow onto throwaways.** The trigger gate exists to keep scripts
  and spikes on the fast path. A flow that adds ceremony to a 40-line script is
  friction, not discipline.
- **Producing a throwaway prototype in place of the walking skeleton.** The
  skeleton is kept and minimal, authored as a real spec and built through
  `work-loop` — not a sketch you'll discard.
- **Choosing a stack with no recorded rationale.** The foundation's ADR comes
  before the skeleton is authored, so the *why* survives.
- **Adding a new top-level directory, or importing another pack's code.** This
  skill lives beside the other core skills and composes the rest **by reference,
  not import** — it names `research`, `receive-brief`, the arc42 `reference.md`
  template, `new-spec`, and `work-loop`, and hands off to them. The
  `product-engineering` seam is by reference too: `frame-intent` is named only as
  an *upstream discovery shape this skill receives* (when that pack is installed),
  never imported.
- **Restating what a composed skill already documents.** Reference `new-spec`,
  `work-loop`, and the brief; don't copy their procedures into this file.

## When this skill is wrong

If you're inside an existing repo, this is the wrong door — use
`adapt-to-project`. If the idea is a one-off script, the trigger gate should
already have sent you to scaffold it directly. And if the flow ever feels like
ceremony getting in the way of a genuinely small thing, trust the trigger gate
over the procedure.
