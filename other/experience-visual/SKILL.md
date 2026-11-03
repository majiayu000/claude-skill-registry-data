---
name: experience-visual
description: CDO-posture skill that authors a kensaiapp instance's visual experience layer — the fence and the direction every product under that instance inherits, written into `system/experience/visual_restrictions.md` and `visual_direction.md`, each with an open-issues companion whose absence is the done signal. Instance-level, never per-product — where `product-design` writes one product's design language, this writes what every product under the instance may and may not look like. Requires CDO posture (halts if invoked outside a `cdo:` session or the `cdo` subagent). Non-interactive by design — it authors both documents best-effort from the instance's own identity, doctrine and evidence, and instead of interviewing live it surfaces its load-bearing calls into companion files the owner answers on their own time; a re-run folds those answers in, retires the answered companion to a permanent trail, and deletes the companion when nothing is left unresolved. It is the first half of an ordered pair — it creates `system/experience/visual_voice_contract.md`, records every fence entry it writes there and marks the ones reaching the verbal medium, and on a later pass answers the entries `experience-voice` records back. Use when authoring, continuing, or revising an instance's visual experience layer, at instance setup or any time after. Do not use for one product's design language (`product-design`), the verbal half (`experience-voice`), the instance's identity or Michi (`kensaiapp-michi`), or any product document.
license: MIT
metadata:
  author: Eyal Golan
  version: "1.5.6"
  created: "2026-08-12"
  category: instance-setup
  tags: experience-layer, instance-setup, cdo, visual, ordered-pair
  risk: safe
---

# experience-visual

## Purpose

Author the **instance's** visual experience layer — the two documents that say what this instance's
products may and may not look like:

- `system/experience/visual_restrictions.md` — the fence.
- `system/experience/visual_direction.md` — what products inherit, and what a design run falls back
  on when nothing covers its case.

This runs at the **instance** altitude. Nothing it writes says anything about any one product; the
first document that could only belong to a product is that product's own. Where that line sits, and
the sequence this step belongs to, are `<CORE>/doctrine/setup/setting_up_an_instance.md`, which owns
them and is not restated here.

This file is the **orchestrator**: posture, the file loop, path resolution, the contract, the
machine-gate step, staging, and the commit. **How to author** — the altitude test, what evidence an entry needs, the
markers, when a value is left absent, the machine gate's bar, and what goes to the owner instead of
being settled — is the authoring prompt **`prompts/rich.md`**,
applied at Step 2; a rule referenced below by name lives there. The documents' **section shape** is
the templates **`<CORE>/templates/experience-templates/visual_restrictions_template.md`** and
**`visual_direction_template.md`**; the companions' shape is **`visual_open_issues_template.md`**
and the contract's is **`visual_voice_contract_template.md`**, both beside them. None of them is
restated here.

**Non-interactive.** The run never blocks on the owner. It authors both documents best-effort,
writes its load-bearing calls into companion files the owner signs off on their own time, and a
re-run folds those answers in. That is what lets it run headless (as the `cdo` subagent) as well as
in an interactive `cdo:` session.

---

## Posture

**CDO role required.** If invoked outside CDO posture (neither a `cdo:` session nor the `cdo`
subagent), stop and say: *"experience-visual requires CDO posture. Switch? (Open a session with the
`cdo:` prefix, or run the `cdo` subagent.)"* Do not shed the role.

The CDO loader stack owns where the CDO ends and the delivery-tier **Architect** begins; that
boundary comes from there, never from a restatement here. One thing this skill does add, because no
loader states it: the CDO's usual subject is one product, and here it is the instance every product
sits under. Same seat, one altitude up.

---

## The files and the loop

Everything lands under `system/experience/` in the instance repo. A caller names nothing — there is
one instance, and this skill is running in it.

| File | What it is | Lifecycle |
|---|---|---|
| `system/experience/visual_restrictions.md` | The fence — best-effort complete on every run. | Permanent; one document, revised and versioned in place. |
| `system/experience/visual_direction.md` | What products inherit, plus the direction section a design run falls back on. | Permanent; one document, revised and versioned in place. |
| `system/experience/visual_restrictions_open_issues.md` | The fence's companion — the calls awaiting the owner and the few things the run could not settle, in the buckets `visual_open_issues_template.md` defines. | Transient. **Its absence is the done signal for that document.** |
| `system/experience/visual_direction_open_issues.md` | The direction document's companion, same shape. | Transient. **Its absence is the done signal for that document.** |
| `system/experience/trail/visual/cycle-<N>.md` | Each answered companion, retired whole. | Permanent. |
| `system/experience/visual_voice_contract.md` | The handoff. **This run creates it** if it is not there, records a row for every fence entry it writes, and marks the ones reaching the verbal medium; `experience-voice` reads those marks and records its own rows back. | Permanent, and never removed — a handoff's absence is a defect, not a done signal. See the section below. |

**The two documents are tracked separately.** A run can finish the fence and still be open on the
direction document, so each companion's absence answers for its own document only. What answers for
the whole layer is `<CORE>/tools/experience_gate.py`, which is not this skill's to run or to satisfy.

**Cycle numbering:** `N` is one higher than the **highest** `cycle-<N>.md` already in
`trail/visual/` — list the directory and take the max, so a removed or renamed cycle cannot make you
collide with an existing one. The first is `cycle-1.md`; create `trail/visual/` if it isn't there.
Never overwrite an existing cycle. Where both companions are answered in one round, each is copied
to its own cycle file.

**The loop, repeated until clean:**

1. The run authors or updates both documents and writes each companion with what it could not
   ground.
2. The **owner answers inline** — filling the companion's answer slots, whose names and shape are
   `visual_open_issues_template.md`'s — and re-runs the skill.
3. The run **copies each answered companion whole to the next trail cycle**, folds the answers into
   its document, and rewrites the companion with only what is still unresolved. An answer that
   leaves something unsettled still drops its item, and the residue re-enters as a fresh unanswered
   item.
4. When the answers resolve everything in a companion, that companion is **removed** rather than
   rewritten — through the builder, Step 4's `--rm`, never a hand-`rm`. **No open-issues file = that
   document is done.** The close has a precondition the ordinary cycle does not: the owner's answers
   must already be committed, because git will not remove a file with uncommitted edits in it and
   their words are not yours to commit. Re-entry is inline answers, so the first closing touch
   normally finds them uncommitted — and then it **changes nothing at all**: no fold, no trail copy,
   no rewrite, no commit. It reports the state, asks for that commit, and the re-run after it is the
   close. That stop is a report with an ask, not a live interview.

Step 3 is why the trail exists. Folding rewrites the companion and the close removes it, so without
the trail the owner's answers are destroyed twice and their reasoning survives only in git history.
The trail costs one `cp` on the same commit and makes every owner answer permanently citable. It is
this skill's job; the owner never manages it.

---

## The contract this run records into — and creates, if it is not there

`system/experience/visual_voice_contract.md` is the handoff to `experience-voice`, and **this skill
creates it.** Nothing upstream stamps it: on the first run of the pair the file does not exist, and a
run that leaves none hands the second half no marks at all — the state rule 1 exists to prevent. So
if it is absent, create it from
**`<CORE>/templates/experience-templates/visual_voice_contract_template.md`**, header and all,
before recording anything. If it is present, leave its header alone and add to it.

**Every entry this run writes into `visual_restrictions.md` gets a row** — not only the ones that
reach the verbal medium. Why it is exhaustive, and what a **handoff** is as opposed to a companion,
are the prompt's and `<CORE>/doctrine/setup/setting_up_an_instance.md` § The three rules'; read them
there.

**`visual_direction.md` states no entries in that sense, and this run records none for it.** Its
values carry no slug and no reach, so there is nothing to key a row on and nothing to mark — and
where a direction value looks as though it would bind the verbal medium, what to do with it is rule
2's, at the file named above. Read it there; this skill neither restates it nor improvises around
it.

**Mark every entry that reaches the verbal medium.** The mark *is* the row's **Mediums** cell naming
that medium, taken from the entry's own **Reaches** field rather than judged a second time here — and
those marks are the whole of what `experience-voice` starts from. An entry reaching both mediums and
left unmarked is invisible to the second author, and nothing downstream will catch it: this is the
one act of this run another run depends on.

**A row owed back to you.** `experience-voice` records its own entries in the same file, and one of
them may reach the visual medium — a limit that originates in words and has a visual breach too. That
is rule 1's second visual pass, and the contract is how you find it: **a row is owed to you when its
Mediums names the visual medium and no entry with that slug exists in `visual_restrictions.md`.**
Write that entry under the same slug, in visual terms — rule 2's split governs it — and update the
row that is already there rather than adding a second. Where you judge the crossing is not real,
**do not delete the row**: raise it in the companion for the owner. The row is the other seat's
record, and overriding it silently is outside yours.

**Neither this skill nor the prompt owns the contract's columns**, and neither restates them: they
are the template's, and the file on disk carries them in its own header.

---

## Inputs and where the files land

Every path below is instance-relative and resolves from the instance repo root — the directory the
session opened in. No step `cd`s away from it. There is no product path to resolve here; that is the
difference between this skill and the `product-*` family.

- **`system/experience/visual_voice_contract.md`** — the handoff, where it exists. On a first run it
  does not, and this run creates it (§ The contract this run records into, above). Where it does,
  read it before writing anything: it carries every fence entry either half has recorded, and the rows
  owed back to this half are found in it and nowhere else.
- **`kensaiapp.md` § "What this is about"** and **`system/michi.md`** — what this instance is for and
  the Way it steers by. Read both in full. They are your primary input: the fence and the direction
  are written *against* a settled statement of what the instance is for. If either is still an
  unfilled placeholder, **do not halt** — author what the rest of the evidence supports and raise
  the gap as an open issue, naming the file. What the identity means for the derivation is the
  prompt's.
- **`system/doctrine/`** — the instance's own doctrine layer. Read what is there. What a fence
  entry may do with a rule already stated in it is the prompt's § An entry needs an origin.
- **`system/experience/`** — **list the directory** and read everything in it, rather than reading a
  set of filenames remembered here. The two documents and their companions above are the loop's
  re-entry point. Anything else the folder holds is input this run is entitled to. A folder that
  does not exist yet means this is a first authoring; create it.
- **`system/experience/trail/visual/`** — every answer the owner has already given, and their
  reasoning. Read it. What a settled answer binds on a later run is the prompt's § On a re-run —
  fold, don't re-author. It also gives you the next cycle number.
- **`system/experience/voice_restrictions.md` and `voice_direction.md`**, if they exist — the verbal
  half, read and never edited: that seat's documents are not yours. On a first authoring they will
  not exist, which is normal and not a halt. Where they do, read them **both ways**: an entry of
  yours that reaches the verbal medium has a counterpart there sharing its slug, and an entry of
  *theirs* that reaches yours is a crossing you owe an entry for. The rules governing both
  directions are `<CORE>/doctrine/setup/setting_up_an_instance.md` § The three rules.
- **Whatever the owner handed you** — a brief, an asset, an existing style guide, a regulator's
  requirement. Read it and treat it as evidence with an origin you can cite.

**No product's documents are inputs.** A product's PRD, UXD or design language is downstream of this
layer and reading one is how a single product's decisions end up fenced across every product. Where
you believe a product's evidence should shape the instance's fence, that is an open issue for the
owner, not a derivation you make.

---

## Workflow

### Step 1 — Read current state

Read everything under *Inputs and where the files land*, in that order. Two things to establish
before writing anything:

- **Which of the two documents already exist**, and for each, whether a companion sits beside it.
  None of either means this run is a first authoring.
- **Whether an existing companion is clean in git** — run `git status --porcelain -- <companion
  path>` for each companion that exists. Output means the owner's answers are uncommitted, which
  Step 2's gate reads.

### Step 2 — Author or revise, and write the companions (no interview)

**Gate first — detect the first closing touch before you write anything.** Where a companion existed
at intake, its inline answers would resolve everything unresolved in it, and the file is uncommitted,
this run is the first closing touch **for that document** and writes nothing for it: no authoring or
fold, no trail copy, no companion rewrite. Where that is true of both documents, skip the rest of
this step and Steps 3–4 and report CLOSING at Step 5.

Author or revise both documents by applying the authoring prompt
**`prompts/rich.md`** and the templates
**`<CORE>/templates/experience-templates/visual_restrictions_template.md`** and
**`visual_direction_template.md`**. Write each companion from **`visual_open_issues_template.md`**
beside them. This step restates none of the prompt's thinking.

**Then record this run's fence entries into `system/experience/visual_voice_contract.md`.** Create
that file from its template first where it is absent. What a row carries, which entries are marked,
and how a row owed back to this half is answered are § The contract this run records into — and
creates, if it is not there, above. This step restates none of it.

Set each document's `Status:` line from Step 5's DONE condition — that document's companion being
absent — not from your tally of answers: **Settled** only when this run ends with no companion on
disk for it; **Draft** otherwise. Leave **Locked** alone; ratification is the owner's act, not
yours. Bump the document's `Version:` line on any run that changes its content.

Do **not** interview. When nothing is unresolved for a document, write no companion for it — an
empty companion would read as open and invert the done signal. If none existed at intake, this step
creates nothing; if one existed, Step 4's `--rm` removes it.

**Consuming an answered companion.** A companion that existed at intake with at least one answer
slot filled is **consumed**, in this order: copy it whole (an ordinary `cp`) to the next trail
cycle, *before* the fold rewrites it; fold the owner's answers into its document; then drop every
**answered** item from it. An answered item never survives the drop — where the answer settles it,
it is gone; where the answer leaves something unsettled, the item still drops and the residue
re-enters as a fresh item with an empty answer slot. Whether an answer settles its item is the
prompt's rule.

That drop is what keeps the loop's signal honest: a filled slot in a surviving companion is always
the owner's writing, never this run's, so a run's own rewrite can never look like an answer at the
next intake. A companion with no slot filled is not consumed — no trail cycle, nothing to fold.

### Step 3 — Run the machine gate

`visual_direction.md` is written in an external, machine-checkable format. Run the linter against
what this run wrote and hold the result to the bar in the prompt's **§ The machine gate** — the
pinned invocation, what counts as clean, and which diagnostics an instance-level document may accept
are stated there and nowhere else. **Do not read the exit code as the verdict.**

Route every diagnostic this run did not fix as the prompt directs: accepted with the record it
prescribes, or an item in the direction document's companion. Where that companion did not exist
because Step 2 had nothing unresolved, this step creates it from its template and **corrects Step 2's
`Status:` line to Draft**.

A result that does not meet the bar is not a reason to report finished, and not a reason to strand
the run's work either: continue to Step 4 with the companion carrying what is left, and report OPEN.

A run that wrote no direction document — Step 2's gate fired for it, or nothing changed — has
nothing to lint and skips this step. `visual_restrictions.md` has no machine format and is never
linted.

### Step 4 — Commit through the builder

Commit through the shared builder — read `<CORE>/doctrine/governance/commit_via_builder.md` and supply
its variables. The builder stages, derives `Role:`, and lays the whole trailer block; this step never
hand-writes a `git commit`, spells a trailer, `cd`s into the repo, or resolves the directional
*shape*. What follows is only the values this skill feeds it.

`<repo>` is the instance repo — `.`. There is no product repo in this skill.

**A run that changes nothing builds no commit — and touches no disk.** If this run folded no answer,
changed neither document, and has nothing to stage, make no file change at all. Report the state
(Step 5) and stop.

**The stage list — compose it from what this run actually did.** Pass every qualifying path in one
`--add` (and any removed companions in one `--rm`).

- `--add system/experience/visual_restrictions.md system/experience/visual_direction.md` — each one
  this run wrote or changed.
- Each companion, exactly one of: `--add` it (something is unresolved for its document, including an
  item Step 3's gate raised) · `--rm` it (nothing unresolved *and* it existed at intake — its
  removal is the done signal) · **neither** (nothing unresolved and none existed).
- `--add system/experience/trail/visual/cycle-<N>.md` — one per companion this run consumed. The
  trail copy rides the same commit as the fold it precedes; neither happens without the other.
- `--add system/experience/visual_voice_contract.md` — when this run created it or recorded rows in it.

**Actor:** `--actor cdo --skill experience-visual` when running as the `cdo` agent; from an
interactive `cdo:` session with no agent named, `--role CDO --skill experience-visual` instead. Both
derive `Role: CDO`.

**The directional is `Michi:`, not `Shukuba:` or `Agari:`.** This commit touches no single project —
it is instance-level, and the directional trailer follows the commit's scope rather than what kind
of thing produced it (`<CORE>/doctrine/governance/commit_format.md` § Directional trailer). Resolve
it against `system/michi.md`. The recipe's parenthetical that producer skills are project-level
describes the `product-*` family; this skill is the exception, which is why it is said here.

Subject, body and the surface / co-author trailers are the recipe's variables — fill them per the
recipe, not from an example copied here.

### Step 5 — Close / report

Report:

- the paths of the documents this run wrote, and the commit SHA (or that the run changed nothing and
  built no commit);
- on any run that ran Step 3, the **machine gate's result as counts**, read as the prompt's § The
  machine gate reads them;
- on any run that consumed an answered companion, the **trail cycle path(s)** — so the owner can see
  their answers survived without opening the commit;
- **what this run left in `visual_voice_contract.md`** — whether it created the file, how many rows
  it recorded, and how many of those are marked as reaching the verbal medium, since that count is
  `experience-voice`'s entire work list; plus any row owed back to this half that this run answered;
- the **loop status per document**, each exactly one of:
  - **DONE** — no companion remains for it and nothing is unresolved; on the direction document, the
    machine gate's bar is met too.
  - **CLOSING** — the owner's answers resolve everything, but the companion is dirty, so this run was
    the first closing touch and changed nothing for that document. The one ask is: commit the
    companion, then re-run.
  - **OPEN** — something is still unanswered, or the machine gate's bar is not met. Give a count per
    bucket under the bucket names the companion on disk carries, name where they live, and name the
    next move: the owner answers inline, commits, and re-runs `experience-visual`.

Then name the one thing that comes next and stop: the verbal half is `experience-voice`'s, and this
skill neither runs it nor writes anything it owns. Do not enumerate anything further downstream —
authoring the instance's visual layer is this skill's whole job.
