---
name: tobiishi-open
description: |
  The FDR-optional front door to the change pipeline — a PM-posture skill that places the change_request.md the chain then carries. Requires PM posture and halts outside a pm session or the pm subagent. Its path is derived, never chosen: where a 宿場 Shukuba station is open, the next change is the one that reaches that station, and the skill writes and commits it without asking. Where no station is open it writes nothing and asks nothing — it reads the project's journey state, names the one next move that state determines, and returns, so a project with no route yet is routed rather than turned away. Never requires a docs/fdr.md — FDR/ADR/NFDR are optional context, never a gate.
  Use when: an existing project needs a new change opened and there is no active Tobiishi yet — "open the next change", "start a change for <project>", "open the tobiishi", "what should we build next for <project>", "run tobiishi-open".
  Do not use for: expanding an already-placed change request into a spec (that is development-specs / the change pipeline), turning a loose idea into journey work (that is seeds-from-idea, the Principal PM's cut — this skill opens the change an open station names, it does not take a direction from its caller), new-project setup (product-fdr / product-architecture / project-stamp), or running the pipeline (the chain).
license: MIT
argument-hint: <project>
metadata:
  version: "4.18.0"
  category: product
  risk: safe
  created: "2026-07-05"
---

# Development Request

## Purpose

The **front of the change pipeline**. It places one `change_request.md` — the single 飛び石 Tobiishi
that `<CORE>/launchers/chain-development/launcher.sh <project>` discovers and carries (spec → design →
plan → content → implement → seal).

**Mode:** derived where a station is open, routing where none is — neither path asks anything. **Posture:** PM only — § *Posture* below is the gate.

**The station decides, and that is the whole change here.** A 宿場 Shukuba station carries a
reached-when, and a change unit exists to reach it — so with a station open the next change is not an
open question and the PM does not ask one. `stations-from-seed` settled the route already; offering
the owner a menu at this point asks them to re-decide what the split just decided. The PM derives the
change from the station, writes it, and commits.

**The case with no route is routed, not asked.** A project with no open station has nothing to derive
from, and inventing the change there would be the machine deciding what to build — so this run writes
nothing there. It reads the journey state, names the **one** move that state determines, and returns.
That is not a refusal: the caller is left holding a named next action inside their own project. Offering
them a menu instead would hand back a decision another move already makes, and turning them away would
push a downstream gate onto the front door — the failure the FDR-optional rule below already records
once.

**Produces:** `system/projects/<project>/journey/tobiishi/<key>/change_request.md` (`<key>` =
`<YYYY-MM-DD>_<slug>`), and overwrites the project's `contexts/CONTEXT_PM.md` with the opened change.

## Input

- **Project name** `<project>` — the `system/projects/<project>/` folder. Take it from the invocation
  where it names one; otherwise it is the project this session was directed at. **There is no undirected
  case for this skill to ask about.** The PM seat cannot be entered without a directed project — with
  none, it asks which project the session is for *before it reads anything*
  (`<CORE>/roles/loaders/pm_global.md:10-11`) — so by the time this skill runs the answer already
  exists, and asking again would be the same question twice. A session that somehow has neither is not
  in PM posture, and § *Posture* below is what catches it.

## Posture

**PM only.** Run in a `pm:` session or as the `pm` subagent. Invoked from anywhere else, halt at once,
say the posture is wrong, and name the way in. The seat's contract is
`<CORE>/roles/loaders/pm_global.md`, and the gate is what makes this skill that seat's — its
§ *Skills toolbox (reminder)* names it, and its § *Responsibilities* places this move fourth, after the
station is open.

It was a soft nudge until 2026-09-06, when the run stopped asking the owner anything — first on its
primary path, and then on every path (§ *Purpose*). A skill that derives a change and commits it
unattended is doing the PM's job with the PM's
judgment, and the per-project PM context it overwrites is that seat's alone — so the seat is now
checked rather than suggested.

**Where the product's code runs.** If seeing what the product does today means running any of its
code — a check, its command, an import — run it in a disposable copy: a fresh clone at the commit you
are reading (`git clone --quiet <repo> <scratch> && git -C <scratch> checkout --quiet <sha>`), never
the product's main checkout. Running it there leaves files behind — a Python `__pycache__/`, a build
directory — and the chain halts this run for every entry it finds there that was not there at launch
(`<CORE>/roles/CROSS_ROLE.md` § *Every seat — a run leaves the product's main checkout as it found
it*). Run the checks from a subshell, never `cd` your own shell into the copy, and remove the copy when you have read the result, in a command of its own run from outside it. Reading the code needs no copy.

## Workflow

### Step 1 — Read the project and its seedbed

Resolve `system/projects/<project>/` and read, in this order of importance:

1. **The open 宿場 Shukuba — the primary source.** The one file at `journey/shukuba/`'s root
   (`<YYYY-MM-DD>_<slug>.md`), if there is one. Its **reached-when** is what the next change exists to
   make true and its **guardrail** is what that change must not break. Then
   **`journey/nemawashi/`** — the active seed at the root (the same filename rule as § *Name the one
   determined next move* below, `<YYYY-MM-DD>_<slug>.md` or the folder form) and its station checklist,
   which say where this station sits on the route and what comes after it; and `unpicked/` as secondary
   context.
2. **`agari.md` — the destination.** The product's "done"; the change opened here points toward it.
3. **`project.md`** — take `Product path:` (relative → in-instance, absolute → external) to locate the
   product's `docs/`.
4. **`docs/SDD.md` / `docs/fdr.md` / `docs/adr/` / `docs/nfdr.md` — optional context, read only when
   present.** Resolve under `Product path`. If any is absent, **proceed without it.** A project that has
   not run `product-fdr` yet is the normal starting case, not an error. **Record which of the four are
   present**, not only what they say: that is the fact Step 4's last two rows key on.
5. **The product's current state** — what already exists, what the last sealed change delivered.

**Never halt on a missing FDR** (or ADR/NFDR). The journey is where the change comes from; the
decision files are context that sharpens it *when they exist*. (See *The FDR-optional rule* in
Critical Rules — this is the load-bearing correction this skill exists to hold.)

### Step 2 — Guard: exactly one active Tobiishi

Run the chain's read-only discovery command from the instance root:

```bash
python3 "<CORE>/tools/chain_development.py" --list-open-changes --instance-root "$PWD" --project <project>
```

The returned JSON array is the authority for active keys; do not infer them from folder names.
A command failure is not an empty array: report the error and stop without writing.

- **One or more keys returned** → stop and name every active key. Do not create a second change;
  the existing change must be carried and sealed through the pipeline.
- **Empty array** → proceed. Leave any other files and folders untouched; they are not active changes.

### Step 3 — Derive the change from the station, or route to the next move

**A station is open — derive, and ask nothing.** The change is the one that reaches this station's
**reached-when** without crossing its **guardrail**. Read both, and write the change that makes the
reached-when true. Where the station needs more than one change to reach it — `<CORE>/docs/michi_agari.md`
§ *How we work — walking a project's journey* step 3 allows that — take the **next** one: the smallest
honest merge that leaves the product better and moves the reached-when closer, given what the station's
already-sealed Tobiishi in `journey/tobiishi/trail/` have delivered. Right-size it by
`<CORE>/prompts/pm_right_size.md` § *Right-size to one honest merge*, which owns the test. Carry its
sizing decision into the request so the next seat can check the same boundary. Then go to Step 5;
Step 4 does not fire.

**No station is open — route, and write nothing.** There is no route to derive from, so no change is
opened here and none is invented. What that state does have is one determined next move, and naming it
is this run's whole output: go to **Step 4**. Steps 5 and 6 do not fire.

### Step 4 — Name the one determined next move — *the no-station path only*

Skip this step entirely when Step 3 derived the change from a station: the station named the change and
there is nothing to route.

Otherwise, take the journey state Step 1 already read — the active seed at `journey/nemawashi/`'s root,
its route section, and the candidate pool in `unpicked/` — and name the **first row that matches**.

**Read the state by these two rules, so the table keys on the journey and not on a spelling:**

- **A seed is `<YYYY-MM-DD>_<slug>.md` at the seedbed root, or a folder `<YYYY-MM-DD>_<slug>/` holding
  `seed.md`.** `README.md` is not a seed, and neither are the `unpicked/`, `trail/` and `drop/`
  subfolders. The rule is the seedbed's own — `journey/nemawashi/README.md`, "Each idea is its own file
  — `<YYYY-MM-DD>_<slug>.md`" (and the folder form, once a `shukuba-refine` run has reported on it) and
  "An **empty root means no idea is active**" — and `<CORE>/../skills/pm/.claude/skills/stations-from-seed/SKILL.md` resolves
  the picked seed the same way ("the **single item at that root** — a file, or a folder holding
  `seed.md`"). **Every seedbed root holds a `README.md` permanently**, so a read without this filter
  never sees an empty seedbed at all and sends the fresh-user case to row 1 instead of to the last two.
- **The route is the section whose heading begins `## Stations`** — match that prefix, never a full
  title, and read it from `seed.md` for a folder-seed. `<CORE>/templates/journey-templates/nemawashi_template.md`
  writes two spellings itself (`## Stations` in its SECTIONS note at `:32`, `## Stations — dynamic
  checklist` in the body it stamps at `:64`), and 20 of the 218 seeds on disk carrying such a section
  spell it a third way or beyond. Read the `- [ ]` and `- [x]` items **inside that section only**:
  checkbox lines elsewhere in a seed are prose, not stations.

| The journey state | The one next move | Whose |
|---|---|---|
| A seed at the root with **no route section at all** | Cut its route — `stations-from-seed` writes the first checklist, which is the same act as re-cutting one. A seed arrives without a route whenever it was seeded as the idea arose, and `<CORE>/templates/journey-templates/nemawashi_template.md:32-35` says so: inventing a checklist before the work is picked is the fixed-plan the checklist exists to avoid | yours |
| A seed at the root, with an unticked item in its route section | Open that station — `shukuba-open` (`<CORE>/docs/michi_agari.md` § *How we work — walking a project's journey*, step 2). Where the checklist is still the proposal the seed arrived with, `stations-from-seed` re-cuts it first: that is the PM's first act on a picked seed (same §, step 1) | yours |
| A seed at the root, every item in its route section ticked | Retire the idea — `nemawashi-retire` — then answer it — `nemawashi-refine` — then pick the next seed from `unpicked/` (same §, step 4) | the retire is the **Scrum Master**'s — that skill halts outside the seat, and a `scrum-master:` session or `<CORE>/launchers/skill/launcher.sh nemawashi-retire <project>` is the way in; the answer is the **Principal PM**'s (`<CORE>/launchers/skill/launcher.sh nemawashi-refine <project>`); the pick that follows is yours |
| No seed at the root, `unpicked/` holds candidates | Pick the one worked now — `nemawashi-pick` — then re-cut its checklist with `stations-from-seed` (same §, step 1) | yours |
| No seed at the root, `unpicked/` empty, **and Step 1 found the draw-from documents** — any of `docs/SDD.md`, `docs/fdr.md`, `docs/adr/`, `docs/nfdr.md` | Cut seeds from those documents — `seeds-from-product-docs`. The work is already drawn there and this cut draws it out. Whether they are settled *enough* to cut is that skill's own check and not this one's, so a `Draft` document is still this row | the **Principal PM**'s — that skill halts outside the seat, and a `principal-pm:` session is the way in (`<CORE>/docs/michi_agari.md` § *Who owns each step — and where the seeds come from*) |
| No seed at the root, `unpicked/` empty, **and none of those four documents present** — including a project whose seedbed does not exist yet | Cut seeds from a direction — `seeds-from-idea`. With no settled documents to draw from, this is the only cut available, and the direction it cuts is the one its caller brings to that run | the **Principal PM**'s — same gate, same way in (same §) |

Report the state you read, the move it determines, and where that move happens — the caller leaves with
one named next action inside the project they invoked this on. Then stop: nothing is written and nothing
is committed, because Steps 5 and 6 are the derived path's.

**The rows are exhaustive, and both ways out of them are closed.** They partition on three questions:
whether the seedbed root holds a seed; where it does, whether there is a route to walk; and where it
does not and `unpicked/` is empty, whether the product holds documents to cut from. The second question
has **three** answers, not two, which is the trap: no route section at all, an unticked item, every item
ticked. Drop the first and the table looks complete while quietly misrouting, because *every item is
ticked* is **vacuously true over no items at all** — a picked seed that has not been cut yet would be
read as a finished one and sent to retirement instead of to `stations-from-seed`. Order matters for the
same reason: take the **first** row that matches.

**The last two rows are one question this run answers, not a choice it hands back.** The seat's two
cutters "differ only in their input"
(`<CORE>/doctrine/setup/kensaiapp_structure.md`, the seedbed's producers), and one of those two inputs
is on disk: `seeds-from-product-docs` draws from the product's `docs/SDD.md`, `docs/fdr.md`, `docs/adr/`
and `docs/nfdr.md`. **So this run reads them** — Step 1 item 4 already resolves that folder, and
recording which of the four are there is the whole cost of deciding the row. Where they are present, the
work is already drawn and drawing it out is what the state determines; where they are absent, cutting
from a direction is the only cut left. Naming both with an *or* would have been a menu — the one thing
§ *Purpose* forbids this path — and a menu the run could have avoided by reading four paths it was
resolving anyway. **The residue is not a second option:** on the last row the caller supplies the
direction, exactly as they supply the judgment inside "pick the one worked now" two rows above. A
caller who already holds a direction they want cut is not asking the project what comes next, and this
skill does not serve them — the frontmatter sends them straight to `seeds-from-idea` (`:6`).

So there is no state the table misses and no further answer to reach for. You do not ask the caller
which row applies, and you do not fall back to proposing a change. A state you genuinely cannot place
is a defect *in this table*: say what you found and that the table does not cover it, which is a bug
report rather than a question.

### Step 5 — Write the change request

Coin the change key `<key>` = `<YYYY-MM-DD>_<slug>` (today's date + a short slug from the change's title).
**This skill owns key-coinage** — `development-specs` *discovers* this folder name and never coins it.

Create `system/projects/<project>/journey/tobiishi/<key>/change_request.md` from
`<CORE>/templates/change_request_template.md`:

- **Request** — expand the derived change into a clear, casual natural-language description of it.
  Carry the station's guardrail into it as what must not be weakened, never a stop: a guardrail
  reading "stop if the schema changes" comes out as "the schema must not change". This skill never
  carries a guardrail as a stop or a halt, even where the station's own words say "stop".
- **Category and Behaviour — yours to set, every time.** The request fixes both axes
  (`<CORE>/doctrine/flow/change_classification.md` § *Constraints* — "Classification is set at entry"),
  and nothing downstream sets them for you. Decide Behaviour first, because it decides what Category may be:
  - **Behaviour** — `changing` if the change alters or adds to the FDR-level contract (the behaviours the
    existing suite pins), or any public name, or what a public name accepts or returns; otherwise
    `preserving`, even where logs, latency or internal layout change (§ *Behaviour-preserving —
    definition*). **"It touches nothing existing" is not a reason for `preserving`:** a change that adds a
    new behaviour, or for a product with no code a new document or a section a reader will act on, adds
    to the contract and is `changing`. Text only reworded, reordered, split or moved, its meaning
    unchanged, adds nothing, even into a new file made only to hold it, and so does a line left at the
    old place saying only where the text now stands. **Read
    the station's reached-when for it:** a line saying something will return, accept or be named
    differently is a changed signature, and the change is `changing` whatever the request calls it.
    **An `nfdr` change has a fourth test, and no product behaviour has to move for it to fire:** it is
    `changing` where it alters what an enforcement command reports — a check that gains a rule, or a
    rule identifier that moves, is a new observable (§ *Category notes*, `nfdr`). A check rewritten to
    decide its verdict on a different basis, a new check script, and a new CI job each meet it. So an
    `nfdr` change touching nothing but tooling is still `changing` whenever the tooling is what says
    pass or fail.
  - **Category** — `refactor` only when Behaviour is `preserving`: refactoring preserves behaviour by
    definition, so a change that alters a signature is never a refactor, however much of it is moving code.
    `feature` only when Behaviour is `changing`: `feature` adds behaviour; `bug` answers a violated contract; `nfdr` is tooling, observability, build, or
    a change an NFDR row drives (§ *Category notes*).
  - **The reason, on its own line** — `**Classified because:** <the station or request line the labels rest
    on>`. A label with no reason is a guess a later step cannot check.
  - The vocabulary is closed — never write a value outside it (`additive`, `new`, … would halt
    `development-specs`), and never `refactor` with `changing` or `feature` with `preserving`, which
    `development-specs` halts as a
    contradiction.
- **No `Project:` field** — the project is implied by which `journey/tobiishi/` this sits in.

**Also overwrite the PM context.** The per-project PM context
`system/projects/<project>/contexts/CONTEXT_PM.md` is the PM's cache of the project's current change, and
this skill owns its **open**-side write. Overwrite its "Current change — PM view" item with the change
just derived — what it is, its scope boundary, how it sits against the FDR (when one exists), any
product-fit note not already in the journey. **One item, replaced in place** — never appended, never
struck through, no log. If the project has no `contexts/CONTEXT_PM.md` yet, create it (and the `contexts/`
folder) from `<CORE>/templates/context_template.md` first. This is the write half of the lifecycle the
manifest already declares — `<CORE>/doctrine/setup/kensaiapp_structure.md` § *2. Per-project*, the
`CONTEXT_PM.md` bullet: "kept fresh by the change lifecycle (`tobiishi-open` overwrites, `tobiishi-seal`
marks it done)". `tobiishi-seal` is what marks it done, flipping the status to `Sealed` and retaining
the content.

Commit it without a confirm. The station already carries the owner's decision, and a second look at
drafted prose adds a stop and settles nothing. Report what was written when the run closes.

### Step 6 — Commit on the base checkout

Commit the new `change_request.md` **and** the overwritten
`system/projects/<project>/contexts/CONTEXT_PM.md` (plus any folder scaffolding for either), on the
**current checkout — not a worktree.** The branch `<key>` is created later by `create_change_worktree.py`
(run by `development-specs`); the change request must pre-exist on the base so the branch inherits it. Do
**not** create a worktree or branch here.

Commit through the shared builder — read `<CORE>/doctrine/governance/commit_via_builder.md` and
supply its variables, with **`--actor pm`** (the agent `launcher.md` launches this skill as — name it,
never derive it) and `--skill tobiishi-open`. Never hand-write `git commit` or a trailer.

The commit carries the `Shukuba:` trailer (topmost) per `<CORE>/doctrine/governance/commit_format.md`,
naming the open station by its dated stem — the station file's name without `.md` — before the
reading: `Shukuba: <YYYY-MM-DD>_<slug> — progress: <how this change request moves toward the
station>`. The builder refuses a line that puts `progress:` where the station belongs. The remaining
standard trailers follow the doctrine.

**Do not run `<CORE>/launchers/chain-development/launcher.sh <project>`.** This skill stops at the placed change request; running the pipeline is the
owner's next move.

## Outputs

| File | Produced when | Where |
|---|---|---|
| `change_request.md` | A station is open — Step 3 derives it | `system/projects/<project>/journey/tobiishi/<key>/` on the base checkout |
| `CONTEXT_PM.md` (overwritten; created from template if absent) | Same, in the same commit | `system/projects/<project>/contexts/` on the base checkout |
| No change; the one determined next move named, and where it happens | No station is open (Step 4) | nothing is written |
| No change; the active `<key>` named | A Tobiishi is already open (Step 2 guard) |  |
| No change; the posture named, and the way in | Invoked outside PM posture (§ *Posture*) |  |

No worktree, no branch, no spec — those all belong to the change pipeline.

## Critical Rules

- **PM posture, checked not suggested.** Halt outside a `pm:` session or the `pm` subagent. This run
  derives a change and commits it with no owner in the room, and it overwrites the PM's own context —
  neither is another seat's to do.
- **The FDR-optional rule — never halt on a missing FDR.** The journey is the primary source of the
  change; `docs/SDD.md` / `docs/fdr.md` / `adr/` / `nfdr.md` are optional context, read only when present. A
  first cut at this skill was built and reverted because it forced a `docs/fdr.md` — it copied
  `development-specs`' `missing-fdr` halt *upstream*, so the front door refused to open for a fresh user
  who hasn't done project setup. This skill exists to hold that door open: FDR sharpens the change when it
  exists; its absence is never an error.
- **A station open means no question is asked.** The reached-when says what the change must make true and
  the guardrail says what it must not break, so the change is derived and committed without a stop. The
  route was settled by `stations-from-seed`; asking here re-opens a decision that seat already made.
- **No station open means the run routes, and routing is not refusal.** With no station there is
  nothing to derive from, so nothing is written — the run reads the journey state, names the **one**
  move that state determines, and returns (Step 4). **The line between routing and refusal is what the
  caller is left holding:** a refusal says no and stops, while routing leaves one named next action
  inside the project they invoked this on. So a project with no route gets a route, not a door — which
  is how the protection above survives the pick that used to carry it. The caller the FDR-optional rule
  was written for, the fresh user who has not done project setup, is exactly the last row of Step 4's
  table: no seed, no station, no product documents, and told to cut seeds rather than turned away — and
  the row before it is the same caller once those documents exist. It is never a menu and never
  a wait — the route is `stations-from-seed`'s and the pick is the PM's own, so handing either back
  re-opens a decision already made. If the derivation cannot name a move, that is a defect in Step 4's
  table and it is reported as one; it is never a licence to ask.
- **Never confirm the drafted request.** It is written and committed, and the report says what landed.
  A confirm on drafted prose settles nothing the station has not already settled.
- **One active Tobiishi at a time.** Guard in Step 2 before creating a new `<key>/`. Downstream discovery
  (`development-specs`) assumes exactly one non-`trail/` folder.
- **This skill coins the key.** `<key>` = `<YYYY-MM-DD>_<slug>`, coined here from the change's title.
  `development-specs` discovers it — it never coins it.
- **Commit on the base, not a worktree.** `change_request.md` lands on the current checkout so
  `create_change_worktree.py`'s branch inherits it. No worktree/branch is created by this skill.
- **Overwrite the PM context on open.** Write the directed project's
  `system/projects/<project>/contexts/CONTEXT_PM.md` — one item ("Current change — PM view"), replaced in
  place, never appended or struck through; create it from `<CORE>/templates/context_template.md` when
  absent. Same path the `pm` loader reads and the same single-item shape the template declares, so read
  and write agree by construction. This is the **open**-side of the lifecycle the manifest declares;
  `tobiishi-seal` marks it done (not this skill).
- **No `Project:` field.** The project is implied by the `journey/tobiishi/` the request sits in.
- **Right-size the derived change to one flow.** One honest merge that moves the product forward — the test is `<CORE>/prompts/pm_right_size.md` § *Right-size to one honest merge*, which owns it.
- **Don't run the pipeline.** Stop at the placed change request; the owner runs
  `<CORE>/launchers/chain-development/launcher.sh <project>` next.
