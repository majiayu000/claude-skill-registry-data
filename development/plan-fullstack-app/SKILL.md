---
name: plan-fullstack-app
description: >-
  Load this skill when planning a software project into SKELETON.md and ITER_NN.md files, one
  release at a time or the complete build to a working MVP in one session. Next-release mode (the
  default) writes one scoped artifact. Whole-build mode plans the skeleton plus every iteration
  upfront, behind a complexity gate. Trigger on "plan the next feature", "create a skeleton plan",
  "plan this whole app to MVP". Not for building the plan (use implement-from-plan) or a small
  non-feature change to a built version (use apply-small-fix-to-version).
disable-model-invocation: false
user-invocable: true
license: Apache-2.0
---

# Plan Fullstack App

Produce plan artifacts, `SKELETON.md` and `ITER_NN.md`, saved under `.agents_workspace/planning/`.
Two modes: **Next release** writes one minimal, scoped artifact that unblocks the next build, and
**Whole build to MVP** writes the complete set from an empty repo to a working MVP. Done means the
artifacts are saved, audited, and the summary under Output is delivered.

## Procedure

Triage first, and announce the label in one line before anything else:

| Label             | The work                                                              | Path                                                  |
| ----------------- | --------------------------------------------------------------------- | ----------------------------------------------------- |
| **Spike**         | Throwaway code to answer one question ("can this library do X?")      | No plan artifact. Say so, name the question, and stop |
| **Bounded**       | One change inside the existing design: no new component or data model | Next release, an iteration plan                       |
| **Architectural** | A new app, component, data model, or major version                    | The mode table below                                  |

The label may move up mid-session, never down: a spike that turns into a keeper is replanned as
bounded or architectural, but architectural work never loses its plan because it shrank.

Pick the mode from the request, then run only that mode's path. When the request does not say,
default to Next release: it is the safe mode, because it commits to nothing past the next build.

| Request                                                                                                                         | Mode                                      |
| ------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| "plan the next feature", "plan this iteration", "create a skeleton plan", a vague idea, or one piece of work on an existing app | [Next release](#next-release)             |
| A large, novel, or uncertain app, however the request is phrased                                                                | [Next release](#next-release)             |
| "plan this whole app to MVP", "plan everything upfront", "lay out all the iterations", and the whole build is foreseeable       | [Whole build to MVP](#whole-build-to-mvp) |
| Finish planning the rest of a family already partly on disk, to its MVP                                                         | [Whole build to MVP](#whole-build-to-mvp) |

Read [Plan families and versions](#plan-families-and-versions) first when the request is a new
major version or continues plans already on disk.

Both modes write and audit artifacts the same way:

- Read `${CLAUDE_PLUGIN_ROOT}/references/plan-schema.md` for the file naming and the required
  frontmatter, including `depends_on`, the `mvp: true` marker, and the `## Out of MVP scope` block.
- Read `${CLAUDE_PLUGIN_ROOT}/references/section-specs.md` for the expected contents of each
  section (§01–§06) at skeleton and iteration level.
- Read and apply `${CLAUDE_PLUGIN_ROOT}/references/implementation-gotchas.md` before writing any
  §04, §05, or §06 content, and address applicable traps proactively.
- Run the pre-delivery audit checklist in `${CLAUDE_PLUGIN_ROOT}/references/audit-checklist.md`
  over every artifact before delivering it.

## Next release

Produce a **minimal, scoped plan** for the current development intent, no more, no less. The goal
is to unblock the next build, not to specify the finished product. Each session produces one
artifact scoped to one release.

### 1. Assess intent

Before writing anything, determine:

1. **What is the app?** Capture the core concept in one sentence.
2. **Greenfield or continuing?** Is this a new project, or adding to or changing something that
   already exists?
3. **Which plan family?** Is this work part of the current plan set, or the start of a **new major
   version** (v2, v3, …)? See [Plan families and versions](#plan-families-and-versions).
4. **What is the scope of this session?** Skeleton, a specific feature, a rework?

Use the answers to select the output:

| Situation                                                   | Output                                                                                             |
| ----------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| New project, nothing built yet                              | [Skeleton plan](#skeleton-plan), default (untagged) family                                         |
| Existing project, same version, adding / changing something | [Iteration plan](#iteration-plan), current family                                                  |
| New major version that reshapes the scaffolding             | [Skeleton plan](#skeleton-plan), new `vN` family                                                   |
| New major version that builds directly on the prior one     | [Iteration plan](#iteration-plan), new `vN` family — first iteration `depends_on` the prior family |

Infer every answer you can from the description and the repo first. Put whatever is still unclear
into **one round** of questions, each with your recommended answer, then plan without stopping
again: a question per turn costs the human a turn each and stalls the run between them. With no
human to answer (a headless run), take each recommended answer, list it under Assumptions in the
closing summary, and plan.

### 2. Apply the anti-overplan check

Before writing any section, apply this filter:

> _Is this decision required to build what the developer described right now?_

If no, leave it out. Mark it as deferred in the relevant section with a one-line note.

Do not spec behaviour that has not been decided. Do not add features "while we're at it". Do not
describe the finished app: describe the next release.

Overplanning is a blocking risk: a developer who reads ahead into unresolved detail will pause to
resolve it before building. Keep the plan narrow.

### 3. Write the artifact

Write the [Skeleton plan](#skeleton-plan) or the [Iteration plan](#iteration-plan) selected in
step 1.

### 4. Audit and deliver

1. Run the anti-overplan check over the draft: remove anything that is not required for the
   current release.
2. Run the audit checklist over the artifact.
3. Save the file to `.agents_workspace/planning/`.
4. Present the file to the user.
5. Close with the summary under Output.

## Whole build to MVP

Produce the **complete plan from nothing to a working MVP** in one session: a skeleton plus every
iteration needed to reach a first usable version, all detailed upfront.

The reason this mode exists: for small, well-understood apps, re-planning each iteration on its
own is wasted effort and context-switching. If the developer can already foresee the whole build,
planning it once is faster and gives a coherent arc.

The reason it is dangerous if misused: planning everything upfront is only safe when the build is
actually foreseeable. The moment real uncertainty enters (a novel core mechanic, a decision that
depends on seeing the data first, a sprawling surface area) detailed plans for later iterations
become fiction. A developer who builds against fictional plans wastes more time than re-planning
would have cost.

So this mode polices itself. **Step 1 is a gate, not a formality.** If the app is too big or too
uncertain, the right move is to stop and fall back to [Next release](#next-release). Honest verdict
over a plan you cannot trust.

### 1. Run the complexity gate

Before planning anything, decide whether this app is simple and certain enough to plan end-to-end.
Gather what you need by inferring from the user's description first, then ask only for what is
genuinely missing, in the single round described under [Assess intent](#1-assess-intent).

You are judging foreseeability: can the whole build be planned now without guessing at decisions
that can only be made by building first?

**Signs it IS suitable (plan to MVP):**

- The MVP is a bounded, well-understood set of features: you can name them all now.
- Conventional domain and patterns: CRUD, standard auth, one or two well-known integrations.
  Nothing research-grade or performance-critical-unknown.
- A manageable data model, on the order of a dozen entities or fewer.
- The stack is conventional and either decided or obvious from the problem.
- The developer can state what "done with the MVP" means in a sentence or two.
- Few hard external unknowns: no "it depends what the third-party API actually returns" or "we'll
  know after we see real usage."

**Signs it is NOT suitable (fall back to Next release):**

- The developer cannot pin down the MVP, or it keeps growing as you discuss it.
- A core mechanic is novel or unproven and needs a prototype to validate (ML feasibility, a hard
  algorithm, tight performance budgets, unproven integration).
- Very large surface area (many subsystems, many roles): a soft signal, not a stop on its own, but
  a reason to look harder for hidden uncertainty underneath it.
- Decisions that genuinely depend on building-and-seeing, where any plan you write for iteration 3
  is a guess you would likely throw away.
- The app already has substantial code and the user only wants the next feature (that is squarely
  Next release's job).

**The threshold (adjust to taste).** Default to PROCEED: plan to MVP unless there is a real reason
not to. Size alone rarely earns a fallback: a larger app that is _conventional and well-understood_
is still foreseeable, so plan it. As a rough guide, ~8 core features and ~12 entities are both
comfortably plannable upfront, and even more is fine when the domain is familiar.

What actually earns a fallback is **uncertainty**, not size. Stop and fall back if any one of these
is strongly true:

- A core mechanic is novel or unproven and needs a prototype to validate.
- A real decision cannot be made without building-and-seeing first.
- The developer cannot pin down what the MVP is, or it keeps growing as you discuss it.

Treat very large surface area (many subsystems, many roles) as a soft signal: a reason to look
harder for hidden uncertainty, not an automatic stop on its own.

**Verdict. Be explicit, do not hedge:**

- **PROCEED** → state in one line why the app clears the gate, then continue to step 2.
- **STOP** → state plainly that this app is better planned incrementally, give the specific reason
  (which signal tripped), and offer Next release mode, starting with the skeleton. Run it only
  once the user agrees, since it changes what they asked for. With no human to agree, write the
  Next release skeleton and report the fallback and its reason. Do not produce a partial full-MVP
  plan as a consolation: that is the exact fiction this gate exists to prevent. If the user insists
  after a clear recommendation, proceed but flag the later iterations as low-confidence and likely
  to change.

### 2. Define the MVP boundary

The MVP is the terminator for the whole plan. Without a hard edge, "plan everything" has no
stopping point and silently becomes overplanning. So pin it down before sequencing anything.

Write two short lists. If there is any doubt, confirm them in the question round. With no human to
answer, keep the shorter "In the MVP" list and list the call under Assumptions:

- **In the MVP:** the minimal set of capabilities that makes the app genuinely usable for its core
  purpose. If a feature can be removed and the app still delivers its core value, it is not in the
  MVP.
- **Deferred (post-MVP):** everything the user mentioned or will obviously want that is _not_
  required for first usefulness. This list is the plan's hard edge: nothing past it gets planned in
  this session.

Everything planned from here drives toward the "In the MVP" list and stops there.

Record both lists on the **terminator iteration** (the final iteration, which carries `mvp: true`)
so the boundary is durable, not just something you reasoned about and discarded: `mvp_target` in
its frontmatter, and a short `## Out of MVP scope` block in its body holding the deferred items.
Keeping the whole boundary on the terminator leaves the SKELETON frontmatter identical to Next
release's, which is what lets a family planned partly in each mode stay consistent. The deferred
list is the plan's visible hard edge: a reader should be able to see what was consciously left out,
not just what is in.

### 3. Sequence the iterations

Decompose the path from skeleton to MVP into an ordered series of iterations. Do this in two passes
so you can sanity-check the arc before committing to detail.

**Pass A, the arc (one line each).** List the skeleton and each iteration with a one-line scope, in
build order. Stop when the cumulative state equals the MVP from step 2. Read this list back: does
each step move the app measurably closer? Is anything out of order? Is any step doing too much
(split it) or too little (merge it)?

**Pass B, confirm ordering.** Each iteration must be buildable using **only** what the skeleton and
earlier iterations established. This is the rule that makes upfront planning safe:

- Foundational concerns first: data model and auth (if the MVP needs it) before the features that
  depend on them.
- No forward references: ITER_N may rely only on content defined in SKELETON or
  ITER_01…ITER\_(N−1), never on something a later iteration introduces.
- Prefer thin vertical slices (one feature end-to-end) over horizontal layers, so each iteration
  leaves the app runnable and demonstrable, but do not force it. The first iteration is often a
  foundational layer (auth, core data model) that is not independently demoable, and that is
  expected: when the two pull against each other, foundational-first wins.

A good decomposition for a small app is usually 2–5 iterations after the skeleton. If you are
producing more than that, re-check the gate: you may be past the point where upfront planning is
wise.

### 4. Write all artifacts

Produce the full set for this family in one session. For the default family:

- `.agents_workspace/planning/SKELETON.md`
- `.agents_workspace/planning/ITER_01.md` … `ITER_NN.md` (the sequence from step 3)

For a new major version, tag every filename in the family with `_vN` and restart the counter at 01:

- `.agents_workspace/planning/SKELETON_v2.md` (omit if this version reuses the prior scaffold)
- `.agents_workspace/planning/ITER_01_v2.md` … `ITER_NN_v2.md`

The final iteration of the family is the **terminator**: it carries `mvp: true` plus `mvp_target`
and the `## Out of MVP scope` block. Every other iteration **omits** the `mvp` key entirely
(absence means false), which keeps non-terminal iterations schema-identical to Next release's. If
the version has its own `SKELETON_vN`, that skeleton is self-contained and iterations depend only
on it and earlier `vN` iterations. If it is iterations-only, `ITER_01_vN` sets `depends_on` to the
prior family's terminal artifacts (skeleton plus its `mvp: true` iteration) so it inherits across
the boundary. See [Plan families and versions](#plan-families-and-versions).

Each artifact uses the same §01–§06 section structure, in the formats under
[Skeleton plan](#skeleton-plan) and [Iteration plan](#iteration-plan). Detail level:

- **Skeleton:** stubs and shapes: screens render, routes respond, functionality is stubbed. Enough
  to run the app and feel the concept. Because you have planned the whole arc, the skeleton's §02
  may state the _full_ target data model and API surface up front. That is expected and useful
  here, unlike in Next release, where you would not know them yet. Just keep the implementations
  behind them stubbed.
- **Each iteration:** full scoped detail for what _that_ iteration adds or changes. You have the
  whole set in view, so make pointers precise, and ensure every artifact a pointer names is
  reachable through `depends_on`.

When a feature's UI would naturally appear before the iteration that builds its backend (e.g. a
"Send" button planned before the send endpoint exists), pick one explicit convention and state it
(omit the control until its iteration, or render it disabled with a clear note) rather than leaving
an either/or. Unresolved waffle is exactly what the audit's completeness scan flags.

### 5. Audit and deliver

Run two audits before delivering.

**Per-artifact audit.** Run the audit checklist over the skeleton and over each iteration.

**Cross-iteration audit** (unique to upfront planning: this is where the set holds together or
falls apart):

- **No forward references.** Every entity, route, type, or dependency an iteration uses is
  established in the skeleton or an earlier iteration, or, for a new version's first iteration, in
  the prior family it `depends_on`. Trace each `depends_on`: it must point only backward, never to
  a later iteration or version.
- **The data model only grows.** Later iterations extend earlier entities. They never silently
  redefine or contradict a field already specified, including across a version boundary, where a
  new version extends what the prior family established.
- **Terminates exactly at the MVP.** The cumulative state after this family's `mvp: true` iteration
  equals the "In the MVP" list from step 2: no less, and nothing planned past it. Exactly one
  iteration in the family carries `mvp: true`. Every other artifact omits the `mvp` key. The
  terminator also carries `mvp_target` and the `## Out of MVP scope` block, and no other artifact
  does.
- **Version tagging is consistent.** Every file in the family carries the same `_vN` tag (or none,
  for the default family), and the `NN` counter restarts within the family.
- **Pre-existing artifacts are untouched.** If this was a continuation, no skeleton or earlier
  iteration written in a prior session was rewritten. New iterations only chain off them via
  `depends_on`.
- **Decomposition is sound.** No empty or trivial iteration, no mega-iteration that should be
  split.

Then deliver:

1. Save all files to `.agents_workspace/planning/`.
2. Present them to the user.
3. Close with the summary under Output.

## Plan families and versions

A **plan family** is one skeleton/iteration sequence for the app, identified by an optional version
tag. Next release adds one artifact to a family per session. Whole build to MVP plans one whole
family per session.

- The first version of the app is the **default family**: untagged filenames `SKELETON.md`,
  `ITER_01.md`, `ITER_02.md`, … (with `mvp: true` on the final iteration once the MVP is planned).
- A **new major version** (v2, v3, …) is a fresh family with a version tag. Each major version is a
  new start: the `NN` iteration counter **restarts at 01** within the family, and the version tag
  goes in the filename, `SKELETON_v2.md`, `ITER_01_v2.md`, … (canonical emit form: `_vN` suffix;
  the implementation step also accepts a `v2_` prefix on read). In Whole build mode the family gets
  its **own** `mvp: true` terminator and `mvp_target`, and the whole of that mode applies _to that
  version's scope_: gate it, define its MVP boundary, sequence its iterations, write its family.

Families are **linked, not isolated**, but how a new version inherits depends on whether it has its
own skeleton, and a skeleton is always a resolution _terminus_ (the implementation step never
traces past one):

- **New version with its own skeleton** (`SKELETON_vN`, when the scaffold is reshaped): the
  skeleton is **self-contained**. It re-states every section the version needs, because a pointer
  cannot resolve past it into the prior family. Its iterations `depends_on` `SKELETON_vN` and
  earlier `vN` iterations only. Lineage to the prior version is conceptual, not a resolution link.
- **New version without a skeleton** (iterations-only, when the prior scaffold is reused):
  `ITER_01_vN` `depends_on` the prior family's terminal artifacts, skeleton plus its `mvp: true`
  iteration (or its final iteration if none), e.g. `depends_on: [SKELETON, ITER_03]`, and
  inheritance resolves _across_ that link. This is the case where cross-version `depends_on` does
  real work.

In both cases `depends_on` names artifacts by **stem** (filename without `.md`, which carries the
version tag), and only ever points **backward**: earlier in this family or into an earlier version,
never forward. Within a family it is simply the same-sequence chain, e.g.
`[SKELETON_v2, ITER_01_v2]`. Skeletons themselves carry **no** `depends_on`.

### Continuing an existing family

The family may already be partly planned on disk, typically a skeleton and a few iterations
produced earlier in Next release mode. Planning the rest of it to MVP is a **continuation**, not a
fresh family, and the same-family rules apply (no version tag, no new skeleton):

- Read every existing `.agents_workspace/planning/` artifact first to establish current state. **Do
  not rewrite the skeleton or any existing iteration**: they are delivered artifacts.
- Run step 1's gate and step 2's boundary against the **remaining** path to MVP, not the whole app.
  What is already built is given. You are sequencing only what is left.
- Number new iterations from the next available `NN` in that family (existing `ITER_01`, `ITER_02`
  → start at `ITER_03`).
- The first new iteration's `depends_on` chains back through the existing artifacts it relies on
  (e.g. `[SKELETON, ITER_01, ITER_02]`). Later new iterations chain normally.
- The new terminator carries `mvp: true` + `mvp_target` + the `## Out of MVP scope` block, exactly
  as a from-scratch terminator would. Because the boundary lives on the terminator, the
  pre-existing skeleton needs no edit and stays valid as written.

## Skeleton plan

**When:** new project, nothing built yet, **or** the start of a new major version that reshapes the
scaffolding.

**Goal:** produce just enough to build a working skeleton: screens render, routes respond, but
functionality is stubbed. The developer should be able to run the app and get a first impression of
whether the concept is right.

**File:** a single file `.agents_workspace/planning/SKELETON.md` for the default family, or
`.agents_workspace/planning/SKELETON_vN.md` for a version family (e.g. `SKELETON_v2.md`). Skeletons
carry no `depends_on` (see [Plan families and versions](#plan-families-and-versions)).

Include all applicable sections inline. Keep each section brief: stubs and shapes, not full
implementation detail. Skip sections that do not apply (e.g. no backend → skip §04, no LLM → skip
§06).

```text
§01 · Concept
§02 · Architecture
§03 · Tech Stack
§04 · Backend
§05 · Frontend
§06 · LLM / Prompts
```

Skeleton rules:

- Every route/endpoint exists but may return hardcoded or empty data.
- Every screen exists but may render with placeholder content.
- No auth, no error handling, no edge cases, unless the concept cannot be understood without them.
- Dependencies listed but not fully justified. Rationale comes in iteration plans.
- No deployment, no CI/CD, no production config.

## Iteration plan

**When:** adding to or changing an existing project, within an existing or new version family. In
Whole build mode, every step after the skeleton is one.

**File:** a single file `.agents_workspace/planning/ITER_NN.md` (default family) or
`.agents_workspace/planning/ITER_NN_vN.md` (version family), where `NN` is the next available
two-digit number **within that family**. The counter restarts per family: `ITER_01_v2.md` is the
first iteration of the `v2` family, independent of `ITER_01.md`.

Use the same section numbers as the skeleton. For each section:

- **If the section is affected by this iteration:** write the full scoped content for what changes.
- **If the section is untouched:** include a one-line pointer only.

**Pointer format.** Reference the artifact by stem (the filename without `.md`, including any
version tag):

```markdown
## §03 · Tech Stack

> Unchanged — see SKELETON_v2 § 03
```

or

```markdown
## §04 · Backend

> Unchanged — see ITER_02_v2 § 04
```

Always point to the last artifact where that section was substantively written, not to the skeleton
by default, because the latest write is the current spec. A pointer may cross a version boundary,
e.g. a `v2` iteration whose §03 was last written in the `v1` skeleton points to `SKELETON § 03`.

**`depends_on` frontmatter.** Every iteration lists the artifacts it builds on, by stem, so the
implementation step can resolve pointers by walking the chain backward:

- Within a family, this is the same-sequence chain up to here, e.g.
  `depends_on: [SKELETON_v2, ITER_01_v2]`.
- The **first iteration of a new version** depends on `SKELETON_vN` if this version has its own
  skeleton. If it is an iterations-only version reusing the prior scaffold, it points back into the
  prior family's terminal artifacts instead, e.g. `depends_on: [SKELETON, ITER_03]`. See
  [Plan families and versions](#plan-families-and-versions).
- Every artifact named in a pointer must appear in (or be reachable through) `depends_on`.
  `depends_on` only points backward, never to a later iteration or version.

Iteration rules:

- Scope strictly to what this iteration adds or changes.
- Do not restate unchanged decisions: use pointers.
- `depends_on` must list every artifact a pointer relies on, and must point only backward.

## Rules

- Ask once: one round of questions, each with a recommended answer. Headless, take the
  recommended answers and list them under Assumptions.
- Do not produce a `CLAUDE.md` unless the user asks, or any file beyond the planning set.
- Never rewrite a skeleton or iteration delivered in a prior session.
- Next release only: one artifact per session, scoped to one release. Do not plan the iteration
  after this one, and keep deferred decisions deferred until they become relevant. Do not produce
  multiple files unless the user asks.
- Whole build to MVP only: plan one whole family per session, and nothing past its `mvp: true`
  terminator.

## Output

Next release: one file under `.agents_workspace/planning/` (`SKELETON.md`, `ITER_NN.md`, or their
`_vN` forms). Whole build to MVP: the full planning set for the family. Every file opens with the
frontmatter from `${CLAUDE_PLUGIN_ROOT}/references/plan-schema.md`. Close the reply with a brief
summary, ending with an Assumptions list of every recommended answer taken without a reply.

Next release:

- What this plan covers
- What is explicitly deferred
- Suggested scope for the next iteration (one sentence only, do not plan it)

Whole build to MVP:

- The MVP definition (the "In the MVP" list).
- The iteration sequence, one line each, in build order.
- What is deferred to post-MVP.

## Stop conditions

- Intent is unclear (the app, greenfield vs continuing, the plan family, or the session scope) →
  ask the single round from Assess intent, with a recommended answer each, instead of planning on
  a silent guess. Headless, take the recommended answers and list them under Assumptions.
- The complexity gate returns STOP → state the reason, offer Next release mode, and produce no
  partial full-MVP plan. Proceed to a full-MVP plan only if the user insists, flagging later
  iterations as low-confidence.
- The audit finds gaps that need user input → collect them and present them together before
  finalising. Headless, finalise with each gap listed as an open item in the closing summary.
