---
name: experience-voice
description: Content-Manager-posture skill that authors a kensaiapp instance's verbal experience layer — the limits and the inherited voice every product under that instance holds, written into `system/experience/voice_restrictions.md` and `voice_direction.md`, each with an open-issues companion whose absence is the done signal. Instance-level, never per-product — where `product-content` writes one product's words, this writes how every product under the instance is allowed to sound. Requires Content Manager posture (halts if invoked outside a `content-manager:` session or the `content-manager` subagent). Non-interactive by design — it authors both documents best-effort from the instance's own identity, doctrine and evidence, and instead of interviewing live it surfaces its load-bearing calls into companion files the owner answers on their own time; a re-run folds those answers in, retires the answered companion to a permanent trail, and deletes the companion when nothing is left unresolved. It is the second half of an ordered pair — it reads the fence entries `experience-visual` marked in `system/experience/visual_voice_contract.md` and records its own there. Use when authoring, continuing, or revising an instance's verbal experience layer, at instance setup or any time after. Do not use for one product's words (`product-content`), the visual half (`experience-visual`), the instance's identity or Michi (`kensaiapp-michi`), or any product document.
license: MIT
metadata:
  author: Eyal Golan
  version: "1.6.6"
  created: "2026-08-12"
  category: instance-setup
  tags: experience-layer, instance-setup, content-manager, voice, ordered-pair
  risk: safe
---

# experience-voice

## Purpose

Author the **instance's** verbal experience layer — the two documents that say how this instance's
products are allowed to sound:

- `system/experience/voice_restrictions.md` — the limits.
- `system/experience/voice_direction.md` — what products inherit, and the fallback a run authoring
  one product's words reads when nothing else answers it.

This runs at the **instance** altitude. Nothing it writes says anything about any one product;
where that line sits, and the setup sequence this step belongs to, are
`<CORE>/doctrine/setup/setting_up_an_instance.md`, which owns them.

This file is the **orchestrator**: posture, the file loop, path resolution, the contract, staging,
and the commit. **How to author** — what belongs at this altitude, what evidence an entry needs,
which medium a limit reaches, the markers, when a category is left open, the bar an entry is worded
to, and what goes to the owner instead of being settled — is the authoring prompt
**`prompts/rich.md`**, applied at Step 2; a rule named
below without its content lives there. The documents' **section shape** is the templates
**`<CORE>/templates/experience-templates/voice_restrictions_template.md`** and
**`voice_direction_template.md`**; the companions' shape is **`voice_open_issues_template.md`**
beside them. None of the four is summarised here.

**Non-interactive.** The run never blocks on the owner. It authors both documents best-effort,
writes its load-bearing calls into companion files the owner signs off on their own time, and a
re-run folds those answers in. That is what lets it run headless (as the `content-manager` subagent)
as well as in an interactive `content-manager:` session.

**There is no machine gate, which is why this Workflow has four steps where its peer has five.**
`experience-visual` lints `visual_direction.md` against an external format before it commits;
neither document here has a machine-checkable format, so there is no such step and no exit code to
read. What stands in its place is the bar the prompt's § *There is no machine that can check this*
carries — met by how an entry is worded, never by passing anything.

---

## Posture

**Content Manager role required.** If invoked outside Content Manager posture (neither a
`content-manager:` session nor the `content-manager` subagent), stop and say: *"experience-voice
requires Content Manager posture. Switch? (Open a session with the `content-manager:` prefix, or run
the `content-manager` subagent.)"* Do not shed the role.

**The seat's reach over this altitude is the loader's, and this skill grants nothing.**
`<CORE>/roles/loaders/content_manager_global.md` § *What you own*, item 2, gives the Content Manager
the instance's own verbal rules — its writing bar and its verbal experience layer — and says what
makes them this seat's. Read it there.

---

## The files and the loop

Everything lands under `system/experience/` in the instance repo. A caller names nothing — there is
one instance, and this skill is running in it.

| File | What it is | Lifecycle |
|---|---|---|
| `system/experience/voice_restrictions.md` | The limits — best-effort complete on every run. | Permanent; one document, revised and versioned in place. |
| `system/experience/voice_direction.md` | What products inherit, plus the fallback section. | Permanent; one document, revised and versioned in place. |
| `system/experience/voice_restrictions_open_issues.md` | The limits document's companion — the calls awaiting the owner and the few things the run could not settle, in the buckets `voice_open_issues_template.md` defines. | Transient. **Its absence is the done signal for that document.** |
| `system/experience/voice_direction_open_issues.md` | The direction document's companion, same shape. | Transient. **Its absence is the done signal for that document.** |
| `system/experience/trail/voice/cycle-<N>.md` | Each answered companion, retired whole. | Permanent. |
| `system/experience/visual_voice_contract.md` | The handoff this run reads and records into — see the section below. | Permanent. **`experience-visual` creates it**, on the first run of the pair; never this skill, whose rows are always added to a file already there. |

**The two documents are tracked separately.** A run can finish the limits and still be open on the
direction document, so each companion's absence answers for its own document only. What answers for
the whole layer is a separate gate, and it is not this skill's.

**Cycle numbering:** `N` is one higher than the **highest** `cycle-<N>.md` already in
`trail/voice/` — list the directory and take the max, so a removed or renamed cycle cannot make you
collide with an existing one. The first is `cycle-1.md`; create `trail/voice/` if it isn't there.
Never overwrite an existing cycle. Where both companions are answered in one round, each is copied
to its own cycle file.

**The loop, repeated until clean:**

1. The run authors or updates both documents and writes each companion with what it could not
   ground.
2. The **owner answers inline** — filling the companion's answer slots, whose names and shape are
   `voice_open_issues_template.md`'s — and re-runs the skill.
3. The run **copies each answered companion whole to the next trail cycle**, folds the answers into
   its document, and rewrites the companion with only what is still unresolved. An answer that
   leaves something unsettled still drops its item, and the residue re-enters as a fresh unanswered
   item.
4. When the answers resolve everything in a companion, that companion is **removed** rather than
   rewritten — through the builder, Step 3's `--rm`, never a hand-`rm`. **No open-issues file = that
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

## The contract, which this run reads before it writes

`system/experience/visual_voice_contract.md` is **an input to this run, not only a place it leaves
rows.** It carries every fence entry the visual half wrote, with the ones reaching this medium
marked, and those marks are the work list this run starts from. Read it at Step 1, before either
document. Why the marks exist and what the order between the two halves buys is
`<CORE>/doctrine/setup/setting_up_an_instance.md` § The three rules, rule 1 — read there, not here;
what a mark obliges you to *write* is the prompt's § The marks you are reading.

**Neither this skill nor the prompt owns the contract's columns**, and neither restates them: they
are `<CORE>/templates/experience-templates/visual_voice_contract_template.md`'s, and the file on disk
carries them in its own header.

**If the file is not on disk, do not create it and do not guess its shape.** It is
`experience-visual`'s to create, on the first run of the pair — so its absence means step 4a has not
run, or ran without leaving one. The pair has run out of order, and that is a defect to report rather
than a hole to fill. Record in both companions that the handoff is missing and that this run
therefore started from no marks, name the file, and author what the rest of the evidence supports.
Creating it here would be worse than the gap twice over: a contract written by the second author
carries no marks, which is the state rule 1 exists to prevent — and a guessed header is one the first
author's real rows would not fit.

**Every entry this run writes into `voice_restrictions.md` gets a row**, on the contract's own terms
— not only the ones that reach the other medium. **`voice_direction.md` states no entries in that
sense and this run records none for it:** its lines carry no slug and no reach, so there is nothing
to key a row on. Where a line of direction looks as though it would bind the visual medium, what to
do with it is `<CORE>/doctrine/setup/setting_up_an_instance.md` § The three rules, rule 2's — read it
there rather than recording something the contract has no column for.

**An entry that originates here and reaches the visual medium is recorded, never authored across.**
Record its row and raise it in that document's companion under § *Owed to the visual half*, so the
owner can see a second `experience-visual` pass is owed. Do not write the visual entry, do not run
the other skill, and do not treat the crossing as resolved because the row exists. What such an
entry is owed is rule 1's, at the file named above.

---

## Inputs and where the files land

Every path below is instance-relative and resolves from the instance repo root — the directory the
session opened in. No step `cd`s away from it. There is no product path to resolve here; that is the
difference between this skill and the `product-*` family.

- **`system/experience/visual_voice_contract.md`** — the marks, read first. The section above says
  what to do when it is absent.
- **`kensaiapp.md` § "What this is about"** and **`system/michi.md`** — what this instance is for and
  the Way it steers by. Read both in full. They are your primary input for the direction document:
  how products sound is written *against* a settled statement of what the instance is for. If either
  is still an unfilled placeholder, **do not halt** — author what the rest of the evidence supports
  and raise the gap as an open issue, naming the file.
- **`system/doctrine/`** — the instance's own doctrine layer, including any writing bar this instance
  states for itself. Read what is there.
- **`system/experience/`** — **list the directory** and read everything in it, rather than reading a
  set of filenames remembered here. The two documents and their companions above are the loop's
  re-entry point. Anything else the folder holds is input this run is entitled to. A folder that
  does not exist yet means this is a first authoring; create it.
- **`system/experience/trail/voice/`** — every answer the owner has already given, and their
  reasoning. Read it; what an earlier cycle's answer authorizes, and what a re-run may move because
  of it, are the prompt's § On a re-run. It also gives you the next cycle number.
- **`system/experience/visual_restrictions.md` and `visual_direction.md`** — the other half, read
  for the origins behind the marks. Read, never edited: that seat's documents are not yours. **If
  either is absent, do not halt.** Rule 1 fixes the visual half to run first, so their absence means
  the pair has run out of order — record it in both companions the way a missing handoff is
  recorded, and author what the rest of the evidence supports.
- **Whatever the owner handed you** — a brief, a style guide, a regulator's requirement, a set of
  strings from something already shipped. Read it and treat it as evidence with an origin you can
  cite.

**No product's documents are inputs.** A product's PRD, UXD or `CONTENT.md` is downstream of this
layer, and reading one is how a single product's decisions end up fencing every product. Where you
believe a product's evidence should shape the instance's limits, that is an open issue for the
owner, not a derivation you make.

---

## Workflow

### Step 1 — Read current state

Read everything under *Inputs and where the files land*, in that order. Three things to establish
before writing anything:

- **Whether the handoff is on disk**, and which of its rows are marked as reaching this medium.
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
this step and Step 3 and report CLOSING at Step 4.

Author or revise both documents by applying the authoring prompt
**`prompts/rich.md`** and the templates
**`<CORE>/templates/experience-templates/voice_restrictions_template.md`** and
**`voice_direction_template.md`**. Write each companion from **`voice_open_issues_template.md`**
beside them. This step repeats none of the prompt's thinking.

**Record this run's rows in `system/experience/visual_voice_contract.md`.** Every entry this run
wrote into `voice_restrictions.md` takes a row there, and a crossing entry is owed something further
— which rows are owed, on what terms, and what else a crossing entry needs are § *The contract,
which this run reads before it writes*'s. This step is where the writing happens; `voice_direction.md`
states no entries and takes no rows.

Set each document's `Status:` line from Step 4's DONE condition — that document's companion being
absent — not from your tally of answers: **Settled** only when this run ends with no companion on
disk for it; **Draft** otherwise. Leave **Locked** alone; ratification is the owner's act, not
yours. Bump the document's `Version:` line on any run that changes its content.

**Do not introduce a check here that this skill cannot actually run** (§ Purpose, *There is no
machine gate*). Nothing mechanical will catch a limit too vague to check, so a limit that resists
being worded checkably goes to the companion rather than into the document unchecked.

Do **not** interview. When nothing is unresolved for a document, write no companion for it — an
empty companion would read as open and invert the done signal. If none existed at intake, this step
creates nothing; if one existed, Step 3's `--rm` removes it.

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

### Step 3 — Commit through the builder

Commit through the shared builder — read `<CORE>/doctrine/governance/commit_via_builder.md` and supply
its variables. The builder stages, derives `Role:`, and lays the whole trailer block; this step never
hand-writes a `git commit`, spells a trailer, `cd`s into the repo, or resolves the directional
*shape*. What follows is only the values this skill feeds it.

`<repo>` is the instance repo — `.`. There is no product repo in this skill.

**A run that changes nothing builds no commit — and touches no disk.** If this run folded no answer,
changed neither document, and has nothing to stage, make no file change at all. Report the state
(Step 4) and stop.

**The stage list — compose it from what this run actually did.** Pass every qualifying path in one
`--add` (and any removed companions in one `--rm`).

- `--add system/experience/voice_restrictions.md system/experience/voice_direction.md` — each one
  this run wrote or changed.
- Each companion, exactly one of: `--add` it (something is unresolved for its document) · `--rm` it
  (nothing unresolved *and* it existed at intake — its removal is the done signal) · **neither**
  (nothing unresolved and none existed, **or** Step 2's gate fired for its document). A gated
  document's companion takes **neither**, never `--rm`: its answers are the uncommitted ones the
  gate was detecting, `git rm` refuses a file with local modifications, and the refusal would take
  the other document's finished work down with it. The close is the re-run after the owner commits.
- `--add system/experience/trail/voice/cycle-<N>.md` — one per companion this run consumed. The
  trail copy rides the same commit as the fold it precedes; neither happens without the other.
- `--add system/experience/visual_voice_contract.md` — when this run recorded rows in it.

**Actor:** `--actor content-manager --skill experience-voice` when running as the `content-manager`
agent; from an interactive `content-manager:` session with no agent named, `--role "Content Manager"
--skill experience-voice` instead. Both derive `Role: Content Manager`.

**Provenance:** `--prompt experience-voice/rich` on every commit this skill builds.
Step 2 authored against that prompt, and the flag is what records it; omitting it positively records
that this run followed no prompt, which is the one thing that is never true here.

**The directional is `Michi:`, not `Shukuba:` or `Agari:`.** This commit touches no single project —
it is instance-level, and the directional trailer follows the commit's scope rather than what kind
of thing produced it (`<CORE>/doctrine/governance/commit_format.md` § Directional trailer). Resolve
it against `system/michi.md`. The recipe's parenthetical that producer skills are project-level
describes the `product-*` family; this skill is the exception, which is why it is said here.

Subject, body and the surface / co-author trailers are the recipe's variables — fill them per the
recipe, not from an example copied here.

### Step 4 — Close / report

Report:

- the paths of the documents this run wrote, and the commit SHA (or that the run changed nothing and
  built no commit);
- **what the handoff gave this run** — how many marked rows it started from, or that the file is
  absent and the gap was raised;
- whether rows were recorded back into `visual_voice_contract.md`, and how many of them name a
  crossing the visual half has yet to answer;
- on any run that consumed an answered companion, the **trail cycle path(s)** — so the owner can see
  their answers survived without opening the commit;
- the **loop status per document**, each exactly one of:
  - **DONE** — no companion remains for it and nothing is unresolved.
  - **CLOSING** — the owner's answers resolve everything, but the companion is dirty, so this run was
    the first closing touch and changed nothing for that document. The one ask is: commit the
    companion, then re-run.
  - **OPEN** — something is still unanswered. Give a count per bucket under the bucket names the
    companion on disk carries, name where they live, and name the next move: the owner answers
    inline, commits, and re-runs `experience-voice`.

Then name the one thing that comes next and stop. Where any entry this run wrote crosses into the
other medium, that next thing is a further `experience-visual` pass, which this skill neither runs
nor anticipates the result of. Do not enumerate anything further downstream — authoring the
instance's verbal layer is this skill's whole job.
