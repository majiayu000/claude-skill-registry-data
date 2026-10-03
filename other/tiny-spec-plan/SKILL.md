---
name: tiny-spec-plan
description: Turn the active ticket's SPEC.md into a technical design and an executable task list — produce PLAN.md (design narrative plus a ## Tasks checklist) and harden the shared constitution.md. The ## Tasks section is a flat, ordered checklist executed sequentially by tiny-spec-build. Re-run in update mode to reconcile it after a SPEC change.
---

# tiny-spec-plan

Decides **how** the requirements get built, slices that into the tasks that build it,
and — just as important — hardens the **constitution** (`constitution.md`) that every
task will be implemented and reviewed against.

It writes **one file**, `PLAN.md`: the design narrative, ending in a `## Tasks`
section — the flat checklist `tiny-spec-build` executes and ticks. Design and checklist
go stale together, so they share one `status:` flag, and this skill is the only one that
sets it. `tiny-spec-build` touches nothing in the file but the checkboxes and `updated:`.

Artifacts live under `.spec/`: the **shared** constitution at the root
(`.spec/constitution.md`), the per-ticket `SPEC.md`/`PLAN.md` under
`.spec/<slug>/`. Both skeletons are inline below — write them from there, no file to
read. Requires `.spec/<active>/SPEC.md`.

**Resolve the active ticket dir**, in order: the `.spec/<slug>/` whose slug matches the
current git branch (one branch per ticket); else the sole ticket dir if exactly one
exists; else ask. **Ask instead** when more than one dir matches the branch, or when
ticket dirs exist while you are on `main`/`master` with no name match — neither has a
safe tie-break. Detached HEAD or no git repo is **degraded**, not an ask: branch match is
simply unavailable, so fall through to sole-dir and ask as written.

## Step 1 — harden the constitution (`constitution.md`)

Do this **first**. The constitution is the spine of the whole flow and **project-wide**
— it lives at `.spec/constitution.md` (the root, shared across every ticket), and is
injected whole into every executor and reviewer. Make it strong and specific to *this*
project, not generic boilerplate. Fill in / sharpen all seven fixed sections:

1. **Style** · 2. **Engineering standards** · 3. **Guiding invariants** ·
4. **Glossary** · 5. **Layout** · 6. **Definition of Done** ·
7. **Verification commands**.

Two sections carry the most weight — get them right:

- **Guiding invariants** — the non-negotiables a reviewer can *fail a task on*. Be
  concrete ("all timestamps are UTC ISO-8601", "no network calls in unit tests"), not
  aspirational ("write clean code").
- **Verification commands** — the exact, runnable gate (install → lint → test → build →
  run). The reviewer executes these literally, so they must actually work from a clean
  checkout. If setup is needed (e.g. install the package first), say so explicitly.

**If the project came in through `tiny-spec-adopt`**, the constitution was *derived from
the codebase* and its sections are marked inferred or declared. Hardening means
confirming the inferred ones against the plan you are about to write — an inferred gate
that has never been run is the single most dangerous thing in the file.

**If there is a `## Design system` section**, it belongs to `tiny-spec-design`; harden
its *values*, don't restructure it:

- **Every token needs a concrete value.** "A consistent spacing scale" fails nothing.
  `space.1`=4px … `space.8`=32px fails a `padding: 19px`. A token with no value is worse
  than no token, because it looks like a contract and isn't one.
- **Check the `SPEC.md` `D<n>` entries resolve.** Every token a screen names must exist
  here. An entry naming `color.accent.primary` when the system defines no such token is
  a broken anchor — route it back to `tiny-spec-design`, don't leave it dangling.
- **Confirm the `visual:` command actually runs.** It is the gate for every task carrying
  `design:`; an aspirational command means the visual gate silently never fires. If it
  doesn't work from a clean checkout, fix it or drop the `design:` refs.

## Step 2 — write `PLAN.md`

Write `.spec/<active>/PLAN.md` with the structure below, filling it in:

```markdown
---
status: current
updated: <ISO date>
---

# Plan — <project / feature name>

## Approach

<The design narrative: how the requirements will be met. Key decisions, the shape
of the solution, notable trade-offs. Enough that someone could derive the tasks
from it. Optional `### Phase` headings are fine for readability — they do NOT
parallelize or gate anything.>

<!-- optional: omit if N/A -->
## Architecture

<The moving parts and how they fit: components, data flow, key interfaces or
modules. A small diagram or bullet map is fine. Skip for changes too small to need it.>

## Requirement coverage

<Every REQ-N maps to where it's addressed. No requirement left unaddressed.>

- REQ-1 — <where/how addressed>
- REQ-2 — <where/how addressed>
- REQ-3 — <where/how addressed>

<!-- optional: omit if N/A -->
## Risks & mitigations

<What could go wrong (technical risk, unknowns, fragile areas) and how the plan
de-risks it.>

<!-- optional: omit if N/A -->
## Test strategy

<How the work will be verified beyond the constitution's gate — what to test, at
what level, and any fixtures/data needed.>

<!-- optional: omit if N/A -->
## Open questions

<Design questions still unresolved. A question that blocks the task list must be
answered here or routed back to tiny-spec-create before you slice.>

## Tasks

<Written in Step 3 — the ordered checklist tiny-spec-build executes.>
```

- `## Approach` *(required)* — the design narrative: the shape of the solution, key
  decisions, trade-offs. Detailed enough to derive a task list from.
- `## Requirement coverage` *(required)* — map **every** `REQ-N` to where it's
  addressed. A requirement with no home is a gap: fix the approach or route back to
  `tiny-spec-create`.
- Optional sections (`Architecture`, `Risks & mitigations`, `Test strategy`,
  `Open questions`) where they add value — omit any that don't apply.
- `## Tasks` *(required)* — always last; Step 3 fills it.

Keep it proportional: a small change is a few paragraphs, not a phased epic.

**An unresolved `## Open questions` entry that blocks the slice is a stop.** Don't guess
past it into a task list — say what's unresolved and route back to `tiny-spec-create`.

## Step 3 — slice the approach into `## Tasks`

Walk the `## Approach` you just wrote and break it into tasks. No waves, no
parallelism, no `owns:` contracts — tasks run one at a time, top to bottom.

**The unit is one coherent commit** — what a competent engineer does in one focused
sitting and commits as a single unit of work. That typically touches several files and
often satisfies several `REQ-N` at once. It is the size you would open as one reviewable
change, not the smallest thing you could name.

**Know what a task costs, so size has something to trade against.** Every task you write
spends two cold-start agents that must re-orient in the codebase from scratch, a reviewer
that runs the gate and exercises the acceptance end-to-end, and two commits. That
overhead is **fixed** — it does not shrink for a small task. A task the executor
finishes in thirty seconds still pays all of it. Size each task so the work inside it
clearly outweighs the machinery around it.

So:

- **Split on independent failure, not on sentence length.** Split a task when it carries
  two **unrelated** observable outcomes that could fail independently of each other. Do
  **not** split because the acceptance got long — a good acceptance is usually several
  clauses covering the happy path *and* its negatives. See `T4` in the `examples/todo-cli`
  task list: two CLI commands, four requirements, and three negative cases, in one task,
  with one acceptance. That is the calibration point, not the exception.
- **One task may satisfy several `REQ-N`** — `req:` takes a list. Coverage means every
  requirement has a *home*, not that every requirement gets its *own* task. **A 1:1
  REQ→task mapping is the single most common way this list comes out too granular.**
  Group the requirements that one coherent change delivers together.
- **Ordered so each builds on the last.** Tasks run sequentially, so a later task may
  freely assume an earlier task's code already exists. Put foundational work (types,
  schema, scaffolding) first. Order by dependency, not by guesswork.

**Smells that mean you sliced below the commit line** — fold each of these back into the
task it belongs to:

- a task that only defines types, interfaces, or schema with no behavior behind them;
- a task that only adds tests for the task before it (the constitution's **Definition of
  Done** already requires the tests to ship with the code);
- one task per file, or one task per function;
- a "wire it up" / "integrate the pieces" task trailing the pieces it wires;
- a **leading pure-scaffold task** — a skeleton, a dispatch stub, a module that imports
  cleanly and does nothing. Fold it into the first task that gives it behavior;
- a **trailing end-to-end verification task**. `tiny-spec-build`'s Completion step already
  runs the whole gate against the whole project from a clean state, exercised the way a
  user would. A task that re-does it buys nothing and costs the full per-task overhead.

The shipped `examples/todo-cli` task list predates these two smells and shows both: its
`T1` is a pure scaffold and its `T5` is an end-to-end verification pass. Today `T1` folds
into `T2` and `T5` doesn't exist. Read that list for `T4`'s sizing, not for its edges.

**Count is a smell, not a cap.** A feature sized the way `tiny-spec-scope` describes
usually lands in **2–5 tasks**. If you are past about six, re-read the list: you have
either sliced below the commit line, or the feature itself was too big and should have
been split upstream. Check the list against that; do **not** enforce a number, and never drop
or merge coverage just to hit one.

For each task, write:

```
- [ ] T<n> — <imperative description>
  - acceptance: <one user-observable outcome that proves it's done — happy path and the
                 negatives that bound it, in one entry>
  - type: feat            # optional; Conventional Commit type (defaults to feat)
  - req: REQ-n, REQ-n     # optional; the REQ-N this task delivers — a list, not one
  - design: D-n           # optional; the SPEC.md D<n> screen this task builds — arms the visual gate
  - pause: <why>          # optional; halt the build before this task so a human looks first
  - files: <comma-separated hint of files it will touch>
```

The **acceptance** is what the reviewer checks against — make it observable
("`spec --version` prints the version and exits 0"), not internal ("version logic
added"). It states **one outcome**, but one outcome is not one clause: spell out the
happy path and the negatives that bound it in the same acceptance, separated by
semicolons. A long acceptance is a well-specified task, not an oversized one — it is the
*number of unrelated things that could fail* that decides whether to split, not the
length of the line. **type** picks the Conventional Commit type `tiny-spec-build` uses for this
task's code commit (`feat | fix | docs | refactor | test | chore | build | ci | perf | style`);
set it when the task is clearly not a feature, otherwise omit and it defaults to `feat`.
**req** ties the task to the requirement it satisfies (traceability). The **files** line
is a hint to focus the executor and reviewer; it is not enforced, so approximate paths
are fine.

**design** is the explicit opt-in to the **visual gate** — the one field that changes
how a task is graded. Set it when the task builds a surface described by a `D<n>` in
`SPEC.md`; the reviewer then renders that surface, measures the selectors the entry
names against the constitution's Design system tokens, and can **fail** the task on a
numeric deviation or a missing state. Omit it and the task is graded exactly as any
other. Two rules:

- Set it only on tasks that actually build the visible surface — not on the API call or
  the state store behind it. The gate is per-task, so this is how you keep the blast
  radius where you want it.
- Only set it if the constitution has a `visual:` verification command. Without one the
  reviewer cannot render anything and will raise a blocker instead of a verdict.

**pause** is the other field that changes what happens rather than what gets written —
but where `design:` changes how a task is **graded**, `pause:` changes whether the build
**continues**. Set it and `tiny-spec-build` halts *before* that task, leaving it
unchecked, so a human reviews the approach while redirecting it is still cheap. The
value is one line saying what to look at.

Propose it only on work that is genuinely **irreversible or wide-blast-radius**:

- a data migration, or anything that writes to real rows;
- a destructive or bulk file operation;
- pulling in a new third-party dependency;
- an auth, permissions, or trust boundary;
- a public API or schema contract other people's code depends on.

**When in doubt, leave it out.** A pause the user didn't want is worse than no pause at
all — it trains them to wave past the ones they did want, which is exactly the reflex
that makes the mechanism useless the one time it matters. Most task lists should carry
zero or one.

**A caller may hand you a standing pause policy** — *"halt before anything that touches
auth"*, *"stop before any schema migration"* (`tiny-spec-run` passes one through in a
build-through run). Apply it to **this** task list: any task matching the description
gets a `pause:` naming the policy that put it there, on top of whatever you'd have set
anyway. A policy that matches nothing here is not an error — say so and move on, rather
than stretching a task to fit it.

Cover **every** part of the approach — together the tasks must deliver all `REQ-N`.
Don't leave a requirement with no task. Coverage is about requirements having a home,
not about the shape of the mapping: several `REQ-N` on one task is the normal case, and
a task per requirement is the anti-pattern. Likewise, if `SPEC.md` has a `## Design`
section, every `D<n>` in it needs at least one task carrying that `design:` reference —
a screen nobody is graded against is a screen that will be built wrong.

Write the tasks into `PLAN.md`'s `## Tasks` section — all `[ ]` unchecked — with the
structure below:

```markdown
## Tasks

> Executed top to bottom, one at a time. A checked `[x]` task is implemented AND
> reviewed. `type:`, `req:`, `design:`, and `pause:` are optional; `files:` is a hint,
> not an ownership contract. A task with `design:` is also graded against that screen's
> `D<n>` entry and the constitution's Design system. A task with `pause:` halts the
> build before it runs, so a human looks first.

- [ ] T1 — <one coherent commit's worth of foundational work; usually several files>
  - acceptance: <the observable outcome; happy path; and the negative case that bounds it>
  - type: feat            # optional; Conventional Commit type for this task's commit (defaults to feat)
  - req: REQ-1, REQ-2     # optional; the REQ-N this task delivers — several is normal
  - files: <path, path, path>

- [ ] T2 — <next coherent change; assume T1's code exists>
  - acceptance: <observable outcome; plus what it rejects and how it fails>
  - type: feat
  - req: REQ-3, REQ-4, REQ-5
  - design: D1            # optional; only on tasks that build the visible surface
  - files: <path, path>

- [ ] T3 — <…>
  - acceptance: <observable outcome>
  - req: REQ-6
  - pause: <optional; what to check before this runs — irreversible work only>
  - files: <path, path>
```

The `req:` lists above are the shape to aim for, not filler: a handful of tasks each
carrying the requirements one coherent change delivers. A skeleton filled in as
`REQ-1`, `REQ-2`, `REQ-3` down a column of single-requirement tasks is the granularity
failure described above.

## Update mode (SPEC changed → PLAN is stale)

When `PLAN.md` is `status: stale` (or its `## Tasks` is empty), reconcile it in one pass:

1. Read the latest `.spec/<active>/decisions.md` change entry to see what moved.
2. Reconcile `.spec/<active>/PLAN.md`'s design sections and the shared
   `.spec/constitution.md` — adjust only what the change requires; preserve the rest.
3. Reconcile `## Tasks` — add/alter/remove tasks to match the new approach, preserving
   existing `T<n>` ids where the task still exists; new tasks get the next free id.
4. **Completed-work guardrail:** if a change touches a task already `[x]`, **uncheck it**
   (`[ ]`) and record the unchecked ids in `.spec/<active>/decisions.md` for human
   review, using the fixed skeleton. Never assume built work survived a change.

   ```
   ## D-NNN — <short title>
   - type: change
   - date: <ISO date>
   - affects: T<n>, T<m>
   - note: <which tasks were unchecked and why>
   ```

5. Set `PLAN.md` to `status: current` and bump `updated`.

**A legacy `tasks.md`** (written before 2.0, when the checklist was its own file): if
`.spec/<active>/tasks.md` exists, move its tasks into `PLAN.md`'s `## Tasks` **verbatim —
ids, fields, and `[x]` state preserved** — then delete `tasks.md`. Do this first, before
reconciling, and never re-slice a legacy list just because you are moving it.

## When done

Confirm the constitution is hardened and every `REQ-N` is covered, then report the task
count — and any `pause:` points you set, with their reason, so the user can drop one
before it fires.

Then point them at `tiny-spec-build` (one task at a time, reviewing as it goes), or
`tiny-spec-run` to drive it through.
