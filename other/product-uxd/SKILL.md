---
name: product-uxd
description: CDO-posture skill that authors a project's UXD — the experience source of truth, written off the settled PRD alongside the CTO's SRS and read by the SDD. Requires CDO posture (halts if invoked outside a cdo session or the cdo subagent). Non-interactive by design — it derives the whole UXD best-effort from the CPO's PRD, and instead of interviewing live it surfaces everything it can't settle into a companion open-issues file (open issues, choices to confirm) for the owner to answer async. On re-run it consumes both files, retires the owner's answered companion whole to a permanent trail, folds their answers into the UXD, and when nothing is left unresolved it clears the companion — its absence means the UXD is done. The skill resolves where the files land from the project's Product path. Use when authoring, continuing, or revising a product's UXD. Do not use for per-change specs (development-specs), the PRD (product-prd), the SRS (product-srs), the design language (product-design), the project's Agari (project-agari), or downstream documents (SDD / Delivery Plan / FDR / ADR / NFDR).
license: MIT
metadata:
  author: Eyal Golan
  version: "0.8.5"
  created: "2026-08-01"
  category: product-definition
  tags: uxd, cdo, product-definition, experience-source-of-truth, upstream-chain
  risk: safe
---

# product-uxd

## Purpose

Author a project's **UXD** (UX Design Specification): the experience source of truth — the
experience-level **what**, derived from the CPO's PRD. It is written **alongside the CTO's SRS**:
both come off the settled PRD, neither derives from the other, and the SDD needs both. The sequence
is `<CORE>/doctrine/setup/setting_up_a_project.md`, which owns it and is not restated here.

This file is the **orchestrator**: posture, the file loop, path resolution, staging, and the
commit. **How to author** — the UXD-completeness lens, the anti-default discipline, the PRD
critique, the sorting test, the provenance gate, the stability rule, and the tone —
is the authoring prompt **`prompts/rich.md`**, applied at Step 2; a rule
referenced below by name lives there. The UXD's **section shape** is the template
**`<CORE>/templates/product-templates/uxd_template.md`**; the companion's shape is
**`uxd_open_issues_template.md`** beside it. None of them is restated here.

**Non-interactive.** The run never blocks on the owner: it derives the whole UXD best-effort,
writes what it can't settle into a companion open-issues file the owner answers on their own time,
and a re-run folds those answers in. That is what lets it run headless (as the `cdo` subagent) as
well as in an interactive `cdo:` session.

---

## Posture

**CDO role required.** If invoked outside CDO posture (neither a `cdo:` session nor the `cdo`
subagent), stop and say: *"product-uxd requires CDO posture. Switch? (Open a session with the
`cdo:` prefix, or run the `cdo` subagent.)"* Do not shed the role. Where the CDO ends and the
delivery-tier **Architect** begins is a posture fact the CDO loader stack already owns — the two
share the word "design" and nothing else, and the boundary comes from there, never from a
restatement here.

---

## The files and the loop

product-uxd produces the files below under the product's `docs/` — the skill resolves the
locations (next section); a caller names the **project**, never the paths.

| File | What it is | Lifecycle |
|---|---|---|
| `<Product path>/docs/UXD.md` | The UXD — best-effort complete on every run. | Permanent; one document, revised and versioned in place (the bump-on-material-change rule is the template's own header note), never forked. |
| `<Product path>/docs/UXD_open_issues.md` | The companion, holding what the run couldn't settle, in the buckets `uxd_open_issues_template.md` defines — kept distinct, never blurred. Which bucket an item lands in, and how it is led, is the prompt's. | Transient — exists only while something is unresolved. **Its absence is the done signal.** |
| `<Product path>/docs/trail/uxd/cycle-<N>.md` | Each answered companion, retired whole. | Permanent. |

**Cycle numbering:** `N` is one higher than the **highest** `cycle-<N>.md` already in `trail/uxd/` —
list the directory and take the max, so a removed or renamed cycle can't make you collide with an
existing one. The first is `cycle-1.md`; create `trail/uxd/` if it isn't there. Never overwrite an
existing cycle.

**The loop, repeated until clean:**

1. The run derives/updates the UXD and writes the companion with what it couldn't settle.
2. The **owner answers inline** — filling the companion's answer slots, whose names and shape are
   `uxd_open_issues_template.md`'s, stated there and not here — and re-runs the skill.
3. The run **copies the answered companion whole to the next trail cycle**, folds the answers into
   the UXD, and rewrites the companion with only what is still unresolved — an answer the fold
   leaves unsettled still drops, its residue re-raised as a fresh unanswered item. This is the
   ordinary cycle — something survives the fold. A run where nothing would is step 4's, and step 4
   alone says what it may touch.
4. When the answers resolve everything, the run is the close: one run that folds, copies the
   answered companion to the trail, and **removes** the companion instead of rewriting it — through
   the builder, Step 3's `--rm`, never a hand-`rm`. **No open-issues file = the UXD is done.** The
   close has a precondition the ordinary cycle does not: the owner's answers must already be
   committed (Workflow Step 3 owns the rule and why). Re-entry is inline answers, so the first
   closing touch normally finds them uncommitted — and then it **changes nothing at all**: no fold,
   no trail copy, no rewrite, no commit; the companion survives intact, answers and all, for the
   owner to commit. It reports the state and asks for that commit; the re-run after it is the close,
   start to finish, in one run. That stop is a report with an ask, not a live interview.

Step 3 is why the trail exists. Folding rewrites the companion and the close removes it — so
without the trail the owner's answers are destroyed twice, and their reasoning for a decision
survives only in git history. The trail costs one `cp` on the same commit and makes every owner
answer permanently citable. It is the skill's job; the owner never manages it.

---

## Inputs and where the files land

- **The PRD** — your primary input; read it in full, status line included. Its location is
  `product-prd`'s to name — that skill wrote it, and its own file table owns where the PRD lands
  under the product's `docs/`; resolve the path from `<CORE>/../skills/cpo/.claude/skills/product-prd/SKILL.md`, never
  from a path remembered here. It must exist: if nothing is at the resolved path, halt and report —
  there is nothing to derive a UXD from. What the status line means for the derivation — including
  a line that is missing or carries a value the PRD template's vocabulary does not hold — is the
  prompt's rule; whatever it raises reaches the owner through the companion like any other item.
- **`system/projects/<name>/agari.md`** — the project's 上がり Agari, the declared terminus, beside
  the card below. Read it in full. What it means for the derivation is the prompt's rule; it is the
  scope boundary, not a source of experience requirements, and the prompt says how that binds.
  **Its absence does not halt the run** — neither does a file still carrying the placeholder
  `project-stamp` stamps. Agari and UXD gate each other in neither direction
  (`<CORE>/doctrine/setup/setting_up_a_project.md`), so a project may legitimately reach the UXD
  first; the state reaches the owner through the companion, exactly as
  an unreadable PRD status line does.
- **`system/projects/<name>/doctrine/`** — the project's own doctrine, if the folder holds anything.
  Read what is there. An empty or absent folder is silence, not a halt.
- **The product's `docs/` folder** — read it by **listing the directory**, not by recalling a set of
  filenames. Beyond the PRD and the UXD loop files named here, whatever else the folder holds is
  input the run is entitled to: the product request the PRD was derived from, the PRD's own trail of
  owner answers, anything a later round adds. What each carries, and which supersedes which, is the
  prompt's § *Inputs you work from*. Skip binary assets. Enumerating rather than naming is
  deliberate — a list of filenames kept here goes stale the day the product gains a document, and
  the run would never know what it had missed.
- **Context and constraints** — whatever the owner hands you, or the docs it points at. What counts
  as one is the prompt's § *Inputs you work from*; read the list there, it is not restated here.
- **`system/projects/<name>/project.md`** — the directed project's card. Its `Product path:` field
  resolves where every output lands; the field is the card template's
  (`<CORE>/templates/project_template.md`, the shape `project-stamp` stamps the card from), so
  read it from the card in hand. Every later `Product path:` in this file means that field.

**Path resolution.** A relative `Product path:` is inside the instance repo; an absolute one is
outside it, in whatever repo holds the product (which need not be its root — Step 1 resolves that
repo as `<repo>`). Every instance-relative path this file names (`system/…`, `.claude/…`) resolves
from the instance repo root — the directory the session opened in; no step `cd`s away from it. If
`Product path:` is a placeholder or awaits an owner value, halt and report: both outputs resolve
from it, so there is nowhere to write even an open issue recording the gap. Never invent one.

---

## Workflow

### Step 1 — Identify the project, read current state

Identify the target project and read:

- `system/projects/<name>/project.md` — the binding. Resolve the file locations from
  `Product path:`, and resolve **`<repo>`** with it — the repo the commit lands in: the instance
  repo (`.`) for a relative path; for an absolute one,
  `git -C "<Product path>" rev-parse --show-toplevel`, because a product with its own repo need not
  sit at that repo's root. If more than one project exists and the target is ambiguous, halt and
  report the candidates — nothing can be resolved or filed without a project.
- the PRD, at the path resolved under *Inputs and where the files land* — in full. **It must be on
  the record:** run `git -C <repo> status --porcelain -- <the resolved PRD path>`; any output halts
  the run, naming the file, for the owner to commit or discard it before re-running. Settled UXD
  content is derived from the PRD and then held stable against re-derivation (the prompt's
  *stability rule*), so deriving from an uncommitted PRD can leave settled experience decisions
  sourced to text the owner later discards — settled output whose source was never on the record.
  One path, one question: this asks about no other file, and the PRD's existence is established
  above, so the only states left to tell apart are clean and not-clean.
- `<Product path>/docs/UXD.md` — the existing UXD, if any. It is the settled baseline the prompt's
  *stability rule* reproduces; no UXD here means this run is a first authoring.
- `<Product path>/docs/UXD_open_issues.md` — the existing companion, if any. **This is the loop's
  re-entry point,** and it holds two kinds of thing. The owner's inline answers are read here — and
  so is a **pointer item**, which another actor writes into the companion to name a **design-run**
  output produced away from this loop (the pointer is written there, never executed there). Read
  both, and open what a pointer names. Whether what you find may be folded, and how narrowly, is the
  prompt's *stability rule*, which carries it as a permitted delta; this file only tells you to read
  it. A pointer naming something you cannot open is an item for the owner, not a fold.
- `<Product path>/docs/trail/uxd/` — every answer the owner has already given, and their reasoning.
  Read it: a value the owner set in an earlier cycle is authorized, and changing it needs a fresh
  authorization (the prompt's *stability rule*). The prompt's *provenance gate* cites these files by
  path, and a citation you have not opened is not one. It also gives you the next cycle number.
- `system/projects/<name>/agari.md` — the declared terminus, in full. Absent or still the
  placeholder: record it as an open issue and derive best-effort; never halt.
- `system/projects/<name>/doctrine/` — the project's own doctrine, if any is there.
- `system/experience/visual_restrictions.md` — the instance's **visual fence**: the visual limits
  every product under this instance holds, and which no product may relax. The UXD is written inside
  it.
- `system/experience/voice_restrictions.md` — the instance's **verbal fence**, the same thing in
  words: the limits on what the product's own text may do. The UXD's wording, and any interface text
  it specifies, is written inside it.
- the rest of `<Product path>/docs/` — **list the directory** and read what the bullets above have
  not already named. Skip binary assets.

**The two fences bind as written, whatever `Status:` they carry, and neither is a halt.** This skill
reads the instance layer's *limits* and inherits no *values* from it, so an unratified or still-Draft
layer changes nothing about this run: there is nothing here to wait for and no gate to consult. A
file that is absent is silence, the same as an empty doctrine folder. What a fence entry means for a
particular experience decision is the prompt's to reason about, not this file's.

Gather any context and constraints the owner handed you, and read them.

### Step 2 — Derive/revise the UXD and write the companion (no interview)

**Gate first — detect the first closing touch before you write anything.** When a companion existed
at intake, its inline answers would resolve everything unresolved, and the file is uncommitted
(check the companion's git cleanliness in `<repo>`), this run is the first closing touch and
**writes nothing**: no derivation or fold, no trail copy, no companion rewrite. Skip the rest of
this step and Step 3, and report CLOSING at Step 4. Why the close needs committed answers is
Step 3's (`--rm` mechanics); the two touches are the loop's, step 4. Everything below runs only when
this gate passes.

Derive or revise `<Product path>/docs/UXD.md` by applying the authoring prompt
**`prompts/rich.md`** (how to think — the UXD-completeness lens, the anti-default
discipline, the PRD critique, the sorting test, the provenance gate, the stability rule, and the
tone) and the template **`<CORE>/templates/product-templates/uxd_template.md`** (the UXD's section
shape). Write the companion from
**`<CORE>/templates/product-templates/uxd_open_issues_template.md`** (its bucket and slot shape).
The prompt's *stability rule* reads its baseline where that baseline lives — the UXD on disk at the
UXD path, which Step 1 has already read; no UXD there is a first authoring, and the rule does not
bind it. This step restates none of the prompt's thinking.

Set the template's `Status:` line from Step 4's DONE condition — the companion's absence — not from
your tally of answers: **Settled** only when this run ends with no companion on disk (it removed
one, or a first run settled everything from its inputs and never wrote one); **Draft** otherwise.
The two cannot diverge: the only run that folds every answer is the close itself, which ends with
the companion removed, and the first closing touch writes nothing at all — UXD included — so no UXD
is ever stamped Settled beside a companion still on disk (the loop, step 4). Leave **Locked**
alone — ratification is the owner's act, not yours. Bump the template's `Version:` line on any run
that changes the UXD's content.

Do **not** interview. When anything lands in any bucket, write/update the companion from its
template. When nothing is unresolved, write none — an empty companion would read as OPEN and
invert the done signal: if none existed at intake, this run creates nothing (Step 3's *neither*);
if one existed, Step 3's `--rm` removes it.

**Consuming an answered companion.** A companion that existed at intake with at least one answer
slot filled is **consumed** — what counts as an answer slot is the companion template's, read from
its current shape, never from a name remembered here, so a template rename cannot make filled
answers read as unfilled. Consuming is three moves, in this order: copy the companion whole (an
ordinary `cp`) to the next trail cycle, *before* the fold rewrites it; fold the owner's answers
into the UXD; then drop every **answered** item from the companion.

**An answered item never survives the drop.** Where the prompt's fold rule settles the answer, the
item is resolved and gone. Where the answer leaves something unsettled, the item still drops and
the residue **re-enters as a fresh item with an empty answer slot** — a new item this run raises,
never the old one surviving. Whether an answer settles its item is the prompt's fold rule; this
step only moves the files that rule implies. What the drop buys is the invariant the rest of the
loop keys on: a filled slot in a surviving companion is always the owner's writing, never this
run's, so a run's own rewrite can never re-fire this detection at the next intake.

A companion with no slot filled is not consumed — no trail cycle, nothing to fold. And when the
drop resolves **every** item, the *write none* rule above owns the disk: leave the companion as
intake read it (the trail copy already holds it) and let Step 3's `--rm` remove it. No state of
this run — a halt between Step 2 and Step 3 included — ever leaves an empty companion behind.

### Step 3 — Commit through the builder

Commit through the shared builder — read `<CORE>/doctrine/governance/commit_via_builder.md` and supply
its variables (`<repo>` from Step 1, the `--add`/`--rm` paths, the actor, subject/body, the
directional). The builder stages, derives `Role:`, and lays the whole trailer block; this step
never hand-writes a `git commit`, spells a trailer, `cd`s into the repo, or resolves the
directional *shape*. What follows is only the values product-uxd feeds it.

**A run that changes nothing builds no commit — and touches no disk.** If this run folded no
answer, changed no UXD content, and has nothing to stage, make no file change at all: don't copy to
the trail, don't rewrite the companion. (This is *not* the recipe's `--allow-empty` marker case —
product-uxd makes no commit at all on an empty run.) Report the state (Step 4) and stop.

**The stage list — compose it from what this run actually did.** Pass every qualifying path in
**one** `--add` (and the companion as the one `--rm` path, when removed) — the recipe's flag rule
owns why. `<D>` below is the resolved docs directory, `<Product path>/docs` expressed relative to
`<repo>` (plain `docs` when the product *is* the repo's root; the subpath when it sits deeper; the
instance-relative path when `<repo>` is `.`).

- `--add <D>/UXD.md` — always, on any run that builds a commit.
- The companion, exactly one of: `--add <D>/UXD_open_issues.md` (something is unresolved) ·
  `--rm <D>/UXD_open_issues.md` (nothing unresolved *and* one existed at intake — its removal is
  the done signal) · **neither** (nothing unresolved and none existed). The owner answers *inside*
  the companion, so the close needs their answers already committed — git won't remove a dirty
  file, and their words aren't yours to commit. A dirty companion when everything would resolve
  marks the first closing touch: Step 2's gate stopped that run before any write, so it never
  reaches this step.
- `--add <D>/trail/uxd/cycle-<N>.md` — only if this run consumed an answered companion. The trail
  copy rides the same commit as the fold it precedes; neither fires without the other.

**Actor:** `--actor cdo --skill product-uxd` when running as the `cdo` agent (the usual path —
the subagent, or a `--bg` run launched `--agent cdo`); from an interactive `cdo:` session with no
agent named, `--role CDO --skill product-uxd` instead. Both derive `Role: CDO`; why `--skill` is
explicit is the recipe's to say. Subject/body, the directional, and the surface / co-author
trailers are the recipe's variables — fill them per the recipe, not from an example copied here.

**And `--prompt product-uxd/rich`**, naming the body this skill is the carrier for. A thin skill over a fat prompt is recorded by both lines and neither implies the other (`<CORE>/doctrine/governance/commit_format.md` § *`Prompt-Version:` trailer*); it takes the bare name, never a path.

### Step 4 — Close / report

Report:

- the UXD path, and the commit SHA (or that the run changed nothing and built no commit);
- on any run that consumed an answered companion, the **trail cycle path** —
  `<Product path>/docs/trail/uxd/cycle-<N>.md`, the copy Step 2 made. The loop (its step 4)
  owns why that copy is the surviving record of the owner's answers; the report names it so
  the owner can verify their answers survived without opening the commit;
- the **loop status**, exactly one of:
  - **DONE** — no open-issues file remains. Nothing is unresolved; the UXD is complete.
  - **CLOSING** — the owner's answers resolve everything, but the companion is dirty, so this run
    was the first closing touch and changed nothing (the loop, step 4; Step 3's companion rule).
    Nothing is left to answer; the one ask is: commit the companion, then re-run — that re-run is
    the close.
  - **OPEN** — something is still unanswered. Give a count per bucket, under the bucket names the
    companion on disk carries (its shape is `uxd_open_issues_template.md`'s, so read the names
    there, never from a name remembered here), name where they live, and name the next move: the
    owner answers inline, commits, and re-runs product-uxd.

Do not enumerate downstream steps; authoring the UXD is this skill's whole job.
