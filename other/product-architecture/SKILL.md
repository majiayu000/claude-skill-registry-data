---
name: product-architecture
description: Principal Architect-posture skill that records a product's architecture decisions and binds its quality constraints — the append-only decision log under docs/adr/ and the constraint set docs/nfdr.md, written off the settled SRS, SDD and FDR as the second half of the foundation step. Requires Principal Architect posture (halts if invoked outside a principal-architect session or the principal-architect subagent). Non-interactive by design — it derives both records best-effort from the upstream documents, and instead of interviewing live it surfaces everything it can't settle into one companion open-issues file (open issues, choices to confirm) for the owner to answer async. On re-run it consumes the companion, retires the owner's answered file whole to a permanent trail, folds their answers in, and when nothing is left unresolved it clears the companion — its absence means both records are done. An accepted record is never rewritten; a reversal is a new record that supersedes it. The skill resolves where the files land from the project's Product path. Use when authoring, continuing, or revising a product's decision log or constraint set. Do not use for per-change specs (development-specs), per-change design (development-design), the PRD (product-prd), the SRS (product-srs), the SDD (product-sdd), the FDR (product-fdr), or the project's Agari (project-agari).
license: MIT
metadata:
  author: Eyal Golan
  version: "1.1.6"
  created: "2026-08-30"
  category: product-definition
  tags: adr, nfdr, principal-architect, foundation-step, decision-log, constraint-set
  risk: safe
---

# product-architecture

## Purpose

Author a product's two architecture records: the **decision log** (`<Product path>/docs/adr/`) — one
append-only file per architecturally significant decision, plus an index — and the **NFDR**
(`<Product path>/docs/nfdr.md`), the constraint set every later change is verified against. They are
written from the settled **SRS**, **SDD** and **FDR**, as the second half of the foundation step; the
FDR beside them is the Principal PM's. The sequence is
`<CORE>/doctrine/setup/setting_up_a_project.md` § *The foundation step*, which owns it and is not
restated here.

This file is the **orchestrator**: posture, the file loop, path resolution, staging, and the commit.
**How to author** — the inputs and their authority order, where a decision is found, the three gates
that decide what earns a record, the ownership test, the constraint bar and its two verification
classes, what to do when upstream is silent, faithful recording, the two lifecycles, the finish walk
and the tone — is the authoring prompt
**`prompts/rich.md`**, applied at Step 2; a rule referenced
below by name lives there. The **shapes** are the templates
**`<CORE>/templates/product-templates/adr_record_template.md`** (one record),
**`adr_index_template.md`** (the index), **`nfdr_template.md`** (the constraint set) and
**`architecture_open_issues_template.md`** (the companion). None of them is restated here.

**Non-interactive.** The run never blocks on the owner: it derives both records best-effort, writes
what it can't settle into one companion the owner answers on their own time, and a re-run folds those
answers in. That is what lets it run headless (as the `principal-architect` subagent) as well as in
an interactive `principal-architect:` session.

**One companion for both records.** One run writes both — the constraint set derives from the records
that run just wrote — so a single companion carries every unsettled item and each item says which
artifact it lands in. Two companions would ask the owner the same question twice whenever a decision
and the obligation it binds are unsettled together, which is the common case.

**There is no machine gate and no acceptance hand-off.** Nothing publishes a schema or a lint for
either document, so no step here shells out to a checker, and no acceptance skill exists to hand
to — that absence is stated, not an omitted step. What stands in place of a gate is the prompt's finish walk and, for the
constraint set, its own § 9 verification map: a table of the entries that *are* machine-checkable.
**Executing that map is not this skill's** — the pipeline reading it is this stack's, running its
rows is sequenced after (owner, 2026-08-30).

---

## Posture

**Principal Architect role required.** If invoked outside Principal Architect posture (neither a
`principal-architect:` session nor the `principal-architect` subagent), stop and say:
*"product-architecture requires Principal Architect posture. Switch? (Open a session with the
`principal-architect:` prefix, or run the `principal-architect` subagent.)"* Do not shed the role.
Where the **Principal Architect** ends and the CTO or the delivery-tier **Architect** begins is a
posture fact the Principal Architect loader stack already owns — the last two share a noun and
nothing else — so take the boundary from there, never from a restatement here.

---

## The files and the loop

product-architecture produces the files below under the product's `docs/` — the skill resolves the
locations (next section); a caller names the **project**, never the paths.

| File | What it is | Lifecycle |
|---|---|---|
| `<Product path>/docs/adr/NNNN-slug.md` | One decision record. **Many files, one per decision.** | Permanent and **append-only**. Once its Status reads Accepted the file is never rewritten; the only line that ever changes in it is that Status line, and only to record its supersession. |
| `<Product path>/docs/adr/README.md` | The index over the records — number, title, status, date. | Permanent, and the one file here that **is** rewritten: it is a projection of the records and is regenerated whenever one lands or changes status. |
| `<Product path>/docs/nfdr.md` | The constraint set. | Permanent; one document, **revised in place** and versioned, under provenance. |
| `<Product path>/docs/architecture_open_issues.md` | The one companion for both records, in the buckets `architecture_open_issues_template.md` defines. Which bucket an item lands in, and how it is led, is the prompt's. | Transient — exists only while something is unresolved. **Its absence is the done signal.** |
| `<Product path>/docs/trail/architecture/cycle-<N>.md` | Each answered companion, retired whole. | Permanent. |

**The append-only rule is a mechanic, and it is this file's to enforce.** *Why* the history is worth
protecting is the prompt's; *what the loop may touch on disk* is here. On any run:

- A record whose Status reads **Accepted** is **never** rewritten, reworded, renumbered or deleted —
  not to improve it, not to fold an owner's answer into it, not because this run would have phrased
  it differently.
- A reversal or a change of mind is a **new record**, at the next number, whose Status names the one
  it supersedes. The superseded record's Status line is then edited to
  `Superseded by ADR-NNNN` — that single line, and nothing else in the file.
- A record still at **Proposed** is this run's to revise freely; it has not been accepted by anyone.
- An owner's answer that contradicts an accepted record produces a superseding record, never an edit.
  If that reading is wrong — the owner meant a correction, not a reversal — that is a companion item,
  because guessing between the two destroys the log's only unique asset.

**Record numbering:** `NNNN` is four digits. Scan `<Product path>/docs/adr/` for the **highest**
existing number and increment — list the directory and take the max, so a removed or renamed record
cannot make you collide with an existing one. The first is `0001-<slug>.md`; create `docs/adr/` if it
is not there. Numbers are never reused and never renumbered.

**Cycle numbering:** `N` is one higher than the **highest** `cycle-<N>.md` already in
`trail/architecture/` — same rule, same reason. The first is `cycle-1.md`; create
`trail/architecture/` if it is not there. Never overwrite an existing cycle.

**The loop, repeated until clean:**

1. The run derives or updates both records and writes the companion with what it could not settle.
2. The **owner answers inline** — filling the companion's answer slots, whose names and shape are
   `architecture_open_issues_template.md`'s, stated there and not here — and re-runs the skill.
3. The run **copies the answered companion whole to the next trail cycle**, folds the answers into
   the records, and rewrites the companion with only what is still unresolved — an answer the fold
   leaves unsettled still drops, its residue re-raised as a fresh unanswered item. This is the
   ordinary cycle.
4. When the answers resolve everything, the run is the close: one run that folds, copies the answered
   companion to the trail, and **removes** the companion instead of rewriting it — through the
   builder, Step 3's `--rm`, never a hand-`rm`. **No open-issues file = both records are done.** The
   close has a precondition the ordinary cycle does not: the owner's answers must already be
   committed (Step 3 owns the rule and why). Re-entry is inline answers, so the first closing touch
   normally finds them uncommitted — and then it **changes nothing at all**: no fold, no trail copy,
   no rewrite, no commit; the companion survives intact for the owner to commit. It reports the state
   and asks for that commit; the re-run after it is the close, start to finish, in one run. That stop
   is a report with an ask, not a live interview.

Step 3 is why the trail exists. Folding rewrites the companion and the close removes it — so without
the trail the owner's answers are destroyed twice, and their reasoning survives only in git history.
The trail costs one `cp` on the same commit and makes every owner answer permanently citable. It is
the skill's job; the owner never manages it.

---

## Inputs and where the files land

- **The SRS, the SDD and the FDR** — the three documents both records are written from. Read each in
  full, status line included. Their locations are the skills that wrote them to name — resolve each
  path from `<CORE>/../skills/cto/.claude/skills/product-srs/SKILL.md`, `<CORE>/../skills/cto/.claude/skills/product-sdd/SKILL.md` and
  `<CORE>/../skills/principal-pm/.claude/skills/product-fdr/SKILL.md`, never from a path remembered here. **All three must exist:
  if any is missing at its resolved path, halt and report which** — every entry carries an upstream
  trace tag, and with a source absent there is nothing to trace to.

  **A status is read and recorded, never demanded** — the rule and the one form it is recorded in are
  `<CORE>/doctrine/governance/unsettled_inputs.md`'s, for every document in the chain. What is this
  skill's: **no step here gates on `Locked`, on `Settled`, or on the absence of any marker.** The
  pre-flight asks whether the inputs *exist*, and nothing else about their content.
- **`system/projects/<name>/agari.md`** — the project's 上がり Agari, beside the card below. Read it
  in full; it is the scope boundary, not a source of constraint. **Its absence does not halt the
  run** — neither does a file still carrying the placeholder `project-stamp` stamps. The state
  reaches the owner through the companion.
- **`system/projects/<name>/doctrine/`** — the project's own doctrine, if the folder holds anything,
  and the engineering doctrine it points at. A default the run applies comes from here, cited. An
  empty or absent folder is silence, not a halt.
- **The product's `docs/` folder** — read it by **listing the directory**, not by recalling a set of
  filenames. Beyond the three inputs and this loop's own files, whatever else the folder holds is
  input the run is entitled to: the trails of owner answers on the upstream documents, the UXD, the
  design and verbal language where they exist, anything a later round adds. Which supersedes which is
  the prompt's § *Inputs you work from*. Skip binary assets. Enumerating rather than naming is
  deliberate — a list of filenames kept here goes stale the day the product gains a document, and the
  run would never know what it had missed.
- **Context and constraints** — whatever the owner hands you, or the docs it points at.
- **`system/projects/<name>/project.md`** — the directed project's card. Its `Product path:` field
  resolves where every output lands; the field is the card template's
  (`<CORE>/templates/project_template.md`), so read it from the card in hand. Every later
  `Product path:` in this file means that field. It also carries the execution context — execution
  type, test command, parallelism — which the constraint set's § 7 points at rather than restating.

**Path resolution.** A relative `Product path:` is inside the instance repo; an absolute one is
outside it, in whatever repo holds the product (which need not be its root — Step 1 resolves that
repo as `<repo>`). Every instance-relative path this file names (`system/…`, `.claude/…`) resolves
from the instance repo root — the directory the session opened in; no step `cd`s away from it. If
`Product path:` is a placeholder or awaits an owner value, halt and report: every output resolves
from it, so there is nowhere to write even an open issue recording the gap. Never invent one.

---

## Workflow

### Step 1 — Identify the project, read current state

Identify the target project and read:

- `system/projects/<name>/project.md` — the binding. Resolve the file locations from `Product path:`,
  and resolve **`<repo>`** with it — the repo the commit lands in: the instance repo (`.`) for a
  relative path; for an absolute one, `git -C "<Product path>" rev-parse --show-toplevel`, because a
  product with its own repo need not sit at that repo's root. If more than one project exists and the
  target is ambiguous, halt and report the candidates.
- the **SRS, the SDD and the FDR**, at the paths resolved under *Inputs and where the files land* —
  each in full, and note the status each carries for the trace tags. **All three must be on the
  record:** run `git -C <repo> status --porcelain -- <the three resolved paths>`; any output halts
  the run, naming the file, for the owner to commit or discard it before re-running. This asks about
  the git state of the source, never about its status line — the two are different questions and only
  the first is a gate. It matters more here than anywhere upstream: an accepted record can never be
  rewritten, so a record derived from text the owner later discards is permanent and wrong.
- `<Product path>/docs/adr/` — **list it and read every record**, including superseded ones. This is
  the settled baseline, it gives you the next record number, and a decision already recorded must not
  be recorded twice under a new number.
- `<Product path>/docs/adr/README.md` — the existing index, if any.
- `<Product path>/docs/nfdr.md` — the existing constraint set, if any. It is the settled baseline the
  prompt's stability rule holds against re-derivation; none here means this run is a first authoring.
- `<Product path>/docs/architecture_open_issues.md` — the existing companion, if any. **This is the
  loop's re-entry point:** the owner's inline answers are read here.
- `<Product path>/docs/trail/architecture/` — every answer the owner has already given, and their
  reasoning. Read it: a value the owner set in an earlier cycle is authorized, and changing it needs
  a fresh authorization. It also gives you the next cycle number.
- `system/projects/<name>/agari.md` — the declared terminus, in full. Absent or still the
  placeholder: record it as an open issue and derive best-effort; never halt.
- `system/projects/<name>/doctrine/` — the project's own doctrine, if any is there.
- the rest of `<Product path>/docs/` — **list the directory** and read what the bullets above have
  not already named. Skip binary assets.

Gather any context and constraints the owner handed you, and read them.

### Step 2 — Derive/revise both records and write the companion (no interview)

**Gate first — detect the first closing touch before you write anything.** When a companion existed
at intake, its inline answers would resolve everything unresolved, and the file is uncommitted (check
the companion's git cleanliness in `<repo>`), this run is the first closing touch and **writes
nothing**: no derivation or fold, no trail copy, no companion rewrite. Skip the rest of this step and
Step 3, and report CLOSING at Step 4.

Derive or revise the records by applying the authoring prompt
**`prompts/rich.md`** (how to think) and the templates
(the shapes): `adr_record_template.md` for each record, `adr_index_template.md` for the index,
`nfdr_template.md` for the constraint set. Write the companion from
`architecture_open_issues_template.md`. This step restates none of the prompt's thinking.

**Order within the step matters, because the second output derives from the first.** Write or update
the records first, then the index over them, then the constraint set — whose entries trace to the
records this run just wrote. A constraint set written first would trace to records that do not exist
yet, which is the shape of an invented requirement.

**The append-only rule binds this step**, per *The files and the loop* above: accepted records are
inputs here, never outputs. A run that would change one writes a superseding record instead.

Set the constraint set's `Status:` line from Step 4's DONE condition — the companion's absence — not
from your tally of answers: **Settled** only when this run ends with no companion on disk (it removed
one, or a first run settled everything from its inputs and never wrote one); **Draft** otherwise.
Leave **Locked** alone — ratification is the owner's act, not yours. Bump the constraint set's
`Version:` line on any run that changes its content. A record's own Status is per-record and follows
the prompt's rule, not this line.

Do **not** interview. When anything lands in any bucket, write/update the companion from its
template. When nothing is unresolved, write none — an empty companion would read as OPEN and invert
the done signal: if none existed at intake, this run creates nothing; if one existed, Step 3's `--rm`
removes it.

**Consuming an answered companion.** A companion that existed at intake with at least one answer slot
filled is **consumed** — what counts as an answer slot is the companion template's, read from its
current shape, never from a name remembered here, so a template rename cannot make filled answers
read as unfilled. Consuming is three moves, in this order: copy the companion whole (an ordinary
`cp`) to the next trail cycle, *before* the fold rewrites it; fold the owner's answers into the
records; then drop every **answered** item from the companion.

**An answered item never survives the drop.** Where the fold settles the answer, the item is resolved
and gone. Where the answer leaves something unsettled, the item still drops and the residue
**re-enters as a fresh item with an empty answer slot** — a new item this run raises, never the old
one surviving. What the drop buys is the invariant the rest of the loop keys on: a filled slot in a
surviving companion is always the owner's writing, never this run's.

A companion with no slot filled is not consumed — no trail cycle, nothing to fold. And when the drop
resolves **every** item, the *write none* rule above owns the disk: leave the companion as intake
read it (the trail copy already holds it) and let Step 3's `--rm` remove it. No state of this run — a
halt between Step 2 and Step 3 included — ever leaves an empty companion behind.

### Step 3 — Commit through the builder

Commit through the shared builder — read `<CORE>/doctrine/governance/commit_via_builder.md` and supply
its variables (`<repo>` from Step 1, the `--add`/`--rm` paths, the actor, subject/body, the
directional). The builder stages, derives `Role:`, and lays the whole trailer block; this step never
hand-writes a `git commit`, spells a trailer, `cd`s into the repo, or resolves the directional
*shape*. What follows is only the values product-architecture feeds it.

**A run that changes nothing builds no commit — and touches no disk.** If this run folded no answer
and changed no record content, make no file change at all: don't copy to the trail, don't rewrite the
companion. Report the state (Step 4) and stop.

**The stage list — compose it from what this run actually did.** Pass every qualifying path in **one**
`--add` (and the companion as the one `--rm` path, when removed). `<D>` below is the resolved docs
directory, `<Product path>/docs` expressed relative to `<repo>`.

- `--add <D>/adr/NNNN-slug.md …` — **each record this run wrote or restatused, named individually.
  Never the `<D>/adr/` directory as a prefix.** The prefix would cover whatever happens to be
  modified under it, which is exactly how a wrongly-rewritten accepted record reaches a commit
  unnoticed: the builder's staged-set guard is satisfied by the prefix and raises nothing. Naming
  each path makes staging a rewritten record a deliberate act a reader can see in the command and in
  the diff. This is the append-only rule's one mechanical surface — everywhere else it is prose.
- `--add <D>/adr/README.md` — on any run that wrote or restatused a record, since the index is its
  projection.
- `--add <D>/nfdr.md` — always, on any run that builds a commit.
- The companion, exactly one of: `--add <D>/architecture_open_issues.md` (something is unresolved) ·
  `--rm <D>/architecture_open_issues.md` (nothing unresolved *and* one existed at intake — its
  removal is the done signal) · **neither** (nothing unresolved and none existed). The owner answers
  *inside* the companion, so the close needs their answers already committed — git won't remove a
  dirty file, and their words aren't yours to commit.
- `--add <D>/trail/architecture/cycle-<N>.md` — only if this run consumed an answered companion. The
  trail copy rides the same commit as the fold it precedes; neither fires without the other.

**Actor:** `--actor principal-architect --skill product-architecture` when running as the
`principal-architect` agent (the usual path — the subagent, or a `--bg` run launched
`--agent principal-architect`); from an interactive `principal-architect:` session with no agent
named, `--role "Principal Architect" --skill product-architecture` instead. Both derive
`Role: Principal Architect`.

**And `--prompt product-architecture/rich`**, naming the body this skill is the carrier for. A thin skill over a fat prompt is recorded by both lines and neither implies the other (`<CORE>/doctrine/governance/commit_format.md` § *`Prompt-Version:` trailer*); it takes the bare name, never a path.

**The directional** is `Agari:` or `Shukuba:`, resolved against
`<CORE>/doctrine/governance/commit_format.md` § *Directional trailer*, whose rule is that the trailer
follows the commit's **scope** rather than what produced it. These records are project-scoped and the
foundation step runs upstream of the delivery loop, so a project with no open station resolves to its
Agari. Read the rule there; this step does not restate it.

### Step 4 — Close / report

Report:

- the constraint set's path and the record directory, **naming each record this run wrote or
  restatused by number and title**, and the commit SHA (or that the run changed nothing and built no
  commit);
- on any run that consumed an answered companion, the **trail cycle path** —
  `<Product path>/docs/trail/architecture/cycle-<N>.md` — so the owner can verify their answers
  survived without opening the commit;
- **any constraint whose `verified by:` is a review gate rather than a machine check**, with the
  reason each gave. This is the run's own honesty surface: the prompt makes class 2 a downgrade that
  must be argued, and the report is where the owner sees how many were argued rather than checked;
- the **loop status**, exactly one of:
  - **DONE** — no open-issues file remains. Nothing is unresolved; both records are complete.
  - **CLOSING** — the owner's answers resolve everything, but the companion is dirty, so this run was
    the first closing touch and changed nothing. Nothing is left to answer; the one ask is: commit
    the companion, then re-run — that re-run is the close.
  - **OPEN** — something is still unanswered. Give a count per bucket, under the bucket names the
    companion on disk carries (its shape is `architecture_open_issues_template.md`'s, so read the
    names there), name where they live, and name the next move: the owner answers inline, commits,
    and re-runs product-architecture.

Do not enumerate downstream steps; authoring these two records is this skill's whole job.
