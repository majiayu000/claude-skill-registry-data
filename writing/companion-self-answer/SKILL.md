---
name: companion-self-answer
description: |
  Answer an open-issues companion when nobody is in the room — the run decides, and writes its own
  decisions into the file. A document authored non-interactively parks what it could not settle in a
  `*_open_issues.md` companion beside it, which the owner ordinarily answers item by item. This skill
  takes that seat. **It is given the companion to answer — a path, required — and halts without one.**
  It proves the file is live, reads from the header which document it belongs to and which skill
  re-runs it, decides every open item it is given — all of them, or only the items its invocation
  lists — by the judgment in `prompts/rich.md`, and writes each answer
  into its slot. It also raises a
  change on that companion where the document is owed one no item asked for, opens or updates another
  document's companion where a change belongs there, and leaves a committed report of every verdict —
  carrying, for an item only the owner may settle, the answer it would have given. Then it commits,
  names the launchers owed a run, and stops.
  Use when a companion must be answered with no owner present — an unattended or launcher-driven run,
  a chain that would stall waiting on an answer, or an ask for the run to decide for itself.
  Trigger phrases — "answer the companion yourself", "decide the open issues", "self-answer the open
  issues", "answer it without me", "companion-self-answer".
  Do not use for walking a companion with the owner present (that is `companion-answer`), writing the
  document itself, running the producing skill, or a Nemawashi seed / Shukuba station.
license: MIT
metadata:
  author: Eyal Golan
  version: "2.11.0"
  created: "2026-08-29"
  category: companion-loop
  risk: safe
---

# Companion Self-Answer

## Purpose

**Turn a parked question into an answered one, with nobody in the room.** A document written without
stopping to interview the owner leaves what it could not settle in a companion file beside it.
`companion-answer` walks that file with the owner and fills no slot without a person present, so a
chain of producing skills stops at every step, waiting. This skill is that walk **with the run in the
person's seat**.

**Same finding, same slots, same commit, same stop at naming the launchers. What differs is who
decides.** Both skills are run by a model; only the decider moves. So everything mechanical below is
taken from `companion-answer` rather than derived a second time, and it is named where it is taken.

**It writes. It does not decide.** The deciding — all of it — is
**`prompts/rich.md`**. This file restates none of that prompt and never
summarises it: a summary here would be a second copy of a judgment that already has one home, and the
copy is what drifts. Read the prompt whole at Step 4, before deciding anything.

**It fills slots. It does not write the document.** The answers reach the document on the producing
skill's next run, which folds them in, copies the answered file to its trail, and clears the resolved
items. **None of that is this skill's** — not the loop's cycles, not the trail's lifecycle, not the
re-run. Those exist outside it and are not restated here. It writes into the companion, writes its
report, commits, and names the runs that consume it.

**It spawns nothing and runs nothing.** The skills that produce these documents halt outside their own
posture, so re-running one would mean spawning a posture agent — a decision that belongs to the owner.
This skill names the launchers and stops. Naming them is the last thing it does.

## It is general, and that is the feature

**This skill knows no list of producing skills, documents, or companion paths, and must never grow
one.** Every fact it needs is on the material in front of it
(`<CORE>/../skills/interactive/.claude/skills/companion-answer/SKILL.md:72`, the same rule and the same reason):

| What it needs | Where it reads it |
|---|---|
| Which file to answer | the invocation — it is required, and the run halts without it (§ Input) |
| Which document it belongs to | the header's "Companion to `<document>`" |
| Whether it is live or a copy | the same pointer — a live companion sits where it says its document is |
| Which skill re-runs it | the header's own "re-run `<skill>`" |
| Which sections exist | the `## ` headings actually present |
| Which slots take an answer | the header's own "fill each **X** / **Y** slot" instruction |
| Which open items are its own | the invocation's item list when it carries one, else every open item |
| Which template opens a companion on another document | that template's own "Companion to `<document>`" pointer |
| Which repo to commit in | `git rev-parse --show-toplevel` from the companion's directory |

A hard-coded list would be a copy of a set that already moves — a new producing skill would be
invisible from the day it lands, and the failure would look like "no open issues" rather than like a
stale list. If a future edit is tempted to name one, that is the tell that a fact was not being read
from the file.

## Input

**Posture-neutral** — the *launcher* picks the posture per run, and this skill gates on none. Nothing
about the deciding depends on a posture, and a gate here would refuse runs the launcher intended.

**Unattended by construction.** Nobody is watching, so the run never asks a question, never offers a
choice, and never waits. Where `companion-answer` would put a question to the owner, this run decides
by the prompt and records what it decided. The one thing it still cannot do is decide an item the
prompt sends back as the owner's — that item stays open, and the report is what tells them.

**The invocation names the companion, and it is required** (the owner's call, 2026-08-29). A path to one
`*_open_issues.md` file. **A run given none halts** — it says it needs the companion's path and stops,
and it does not fall back to searching for one.

The reason is the same "nobody is watching" that shapes everything else here. A search can return more
than one live companion, and choosing among them unattended is a choice nobody sees and nobody can
correct — while a companion is precisely the thing a cycle consumes, so a run pointed at the wrong file
spends a real round on a document nobody asked about. Being handed the file is what makes the run's
target reviewable before it starts rather than after it commits.

**The invocation may also list the items this run answers.** A launcher that sends each seat its own
items gives the run one more sentence after the path, in exactly this form:

> `Answer only these items: <n>, <n>.`

Each `<n>` is an item's number as the companion's own headings print it (`1.2`, `2.1`), in the
companion's order. **With the sentence, only the listed open items are this run's to write.** Every
other open item belongs to another seat's run, and its slots stay exactly as they were. **Without it,
every open item is eligible**, under the slot rules of Step 3. A number the companion has no open item
for names nothing to write; leave it, and say so in the report. Everything else this run does is the
same with a list as without one.

---

## Workflow

### Step 1 — Take the companion you were given, and prove it is live

The invocation named one `*_open_issues.md` file (§ Input). **If it named none, stop there** — say that
the companion's path is what the run needs, and do not go looking. A search would answer a question
nobody asked and could answer it wrongly with nobody watching.

**Being handed a path is not evidence that it is a live companion.** Companion-shaped files sit in
archives, fixtures, evidence trees and extracted layers, and they read identically to a live one — so
the file you were given gets the same test a file you found would get. Ask it where it thinks it lives:

```bash
grep -m1 -o 'Companion to `[^`]*`' "$companion"
```

- The header names a **path** — the document must exist at that path **and** the companion must sit in
  that same directory, resolved against the repo root and never as a suffix of where the file sits.
  *"Two conditions, both required"*, and why each catches what the other misses, is
  `<CORE>/../skills/interactive/.claude/skills/companion-answer/SKILL.md:138-148`.
- The header names a **bare filename** — live only if that document is its sibling on disk.
- **No `Companion to` pointer at all** — not a companion. Stop.

**Live** → that is the run's companion. Bind its path, say which document it belongs to, and go on.

**Not live** → stop, and say which test it failed and what was on disk instead. A run that answers a
copy writes into a file no producing skill will ever fold, and the answers are lost silently — the one
outcome worth halting for, because nobody is present to notice it.

### Step 2 — Read the header, and derive the run's facts

The header is the blockquote under the title. Read it whole, and take from it:

1. **The document** — "Companion to `<document>`". Read that document whole before Step 4, and its
   inputs as the header and items name them. The prompt's § *Inputs you work from* says why.
2. **The producing skill** — "re-run `<skill>`", backticked. This is what Step 6 names for this document.
3. **The slot labels** — "fill each **X** / **Y** slot". These drive Step 3.
4. **The trail promise** — the header says the answers are copied whole to a trail folder before being
   folded in. **That copy is the producing skill's, on its fold — not yours.** Do not make it: a trail
   copy made before the fold records a round that has not happened.

**When the header names no skill to re-run.** Some companions are the baton in a loop between two
skills rather than a re-run of one, and their header says so in prose without backticking a skill
name. Do not guess and do not grep for a plausible one. Carry what the header *does* say — the roles
it names and the order it gives them — into Step 6 and state it there. A named role with an honest
gap is worth more than an invented skill name, which nobody is present to catch.

### Step 3 — Work out which items are yours to write

Read the `## ` headings **present in this file**, never a remembered set — they differ between
companions, and a section you expect and do not find is normal. Under each heading, the `### ` entries
are the items. **Read the section headings as you go**, because they name the bucket an item sits in
and the prompt reads the bucket.

An item is **yours to write** when it carries at least one slot from Step 2's labels *and* that slot
is still at its placeholder — an angle-bracketed stub like `<the owner fills this in>` — *and*, when
the invocation lists items (§ Input), its number is on that list. Anything else is not:

- **A filled slot is an answer already given.** Leave it exactly as it is, whoever gave it. Count them
  and record how many you skipped in Step 5's report. This is why the labels are read off the header in
  front of you rather than from memory: *"The skill detects a consumed companion by a FILLED SLOT, so
  renaming a label silently breaks the loop's re-entry"*
  (`<CORE>/templates/authoring-templates/document_template_template.md:186-190`).
- **An item with no owner slot is addressed to someone else.** Some sections carry items for the
  *producing* skill to resolve on its next pass, with a slot that skill fills. Never write in one.
  Record them in the report as "not yours to answer", with whose they are as the file states it.
- **An open item the list does not name is another seat's run's.** Leave every one of its slots at
  its placeholder. Record it under `## Skipped`, saying it is carried by another seat's run, and give
  it **no `**Verdict:**` field**: the reporter tallies every `**Verdict:**` line in the file, so a
  verdict on an item this run did not decide would be counted as worked here and again in the report
  of the run that does decide it.

If nothing is left to write, the file is answered — go to Step 5 with that as the finding. With a
list, that means nothing *listed* is left; unlisted open items do not keep this run from finishing.

### Step 4 — Decide each item, and write the answer into its slot

**Read `prompts/rich.md` whole, then apply it to each item that is yours
(Step 3).**
Everything about the deciding is there, and nothing about it is here. Do not paraphrase it into this
run's output either — a decision made from a paraphrase is made from the drift.

What this step owns is the writing:

- **The slot takes the answer, in the slot's own form.** A confirm-or-override slot takes `confirm` or
  `override: <what instead>` — the colon form, which is what every companion template on disk prints
  (`grep -h -o 'override: [^>]*' <CORE>/templates/*/*_open_issues_template.md`, 2026-08-29). An
  open-issue slot takes the answer itself. The slot's own placeholder states its form; follow that,
  not this sentence.
- **The answer names the report.** Where the slot's form allows a sentence, end it with the report
  file Step 5 writes, by the path Step 5's own naming rule gives. The companion is read on its own by the run that folds it, and the
  reasoning is in the report.
- **An item the prompt leaves for the owner keeps its placeholder** — and its answer goes in the
  report. Do not write a hedge into the slot and do not mark it decided: an unanswered slot is what
  keeps the item open through the fold. The prompt requires that verdict to carry the answer the run
  would have given, so the report's entry for it has both the reason it was left and that answer.
  Writing the reason without the answer loses the half the owner actually reads.
- **Write as you go, item by item**, never in one pass at the end, where a stopped run loses
  everything decided.
- **Nothing that is already in the file changes.** Not the header, not an existing item's numbering,
  not an item's other fields, not a section's presence. What a run may *add* is an item, on two grounds
  and no third — § *Raising a change on the companion you are answering* and § *When an item splits, the
  answered half moves out*, both below; everything already written stays as it stands. If an item's
  supporting text is wrong, record that in the report — it is the producing skill's to correct, not
  yours to edit under an answer.

**If the item carries other placeholder fields plainly addressed to the owner**, decide them the same
way and record them in the report. Leave at its placeholder anything the prompt did not reach.

#### When a change belongs to another document

**Two ways in, one mechanism.** Whichever way you arrived, everything below is the same:

1. **An item you are answering routes there** — the prompt's check 1 puts its seat on a different
   document.
2. **A document you read is owed a change no item raised** — the prompt's § *The items are not the
   whole of what a document is owed*, applied to a document you opened while answering.

Only the first has a slot waiting on the result, which is the one difference between them and is
stated where it matters below.

The change does not go into the document being answered, and the document that owes it is usually
settled — nothing beside it, so its own producing skill re-runs and finds nothing to act on. Opening
that document's companion is how the change reaches the seat that can act on it. **Here it is opened
on the run's own judgment**, with nobody to ask — the one authority this skill has that its sibling
does not.

**That other document is not written either.** You are holding a decision about it and nobody is
watching, which is the moment the edit looks cheapest and is most wrong: the change is that document's
producing skill's to fold, on its own run, in its own posture. Opening its companion *is* the action
here — the document is left exactly as it stands.

- **A live companion already holds that document** — a `*_open_issues.md` beside it whose `Companion to`
  pointer names it among the names it lists, never one found by its filename, since a companion shared
  by two documents carries neither's name → append one item to it. Nothing else in that file moves —
  not its header, not its numbering, not its other items.
- **…unless an item already there is the one your finding changes** → revise that item instead of
  appending a near-duplicate. Two items asking the same question with different reasoning is worse for
  the round than one item that is current: the owner answers both, the fold takes both, and nothing
  records that they were the same question. **Only an item whose slot is still at its placeholder may
  be revised** — a filled slot is an answer somebody gave and is never rewritten, and an item carrying
  a slot addressed to another actor is not yours at any point. Revise the reasoning fields and leave
  the slot at its placeholder. **Say in the report which item you revised and what it said before**,
  because the file itself no longer carries that and a reader who disagrees needs it.

**Which bucket a raised item goes in is settled, not judged per run.** It goes in **choices to
confirm**, carrying the reasoning that raised it. The prompt's rule decides this and the skill does not
re-derive it: an open issue is *"one you have no basis to decide; if you have a lean it belongs in
bucket 2"* (`prompts/rich.md` § *The two buckets ask different questions*).
A run raising an item has already judged that document owed a change and why — that reason **is** the
lean, so the item is never a bucket-1 open issue. Its confirm-or-override slot stays at its
placeholder: the reasoning is this run's, the decision is the next round's.
- **There is none** → write one from that document's own companion template. Every template states in
  its own header which document — or documents — it is a companion to, so read the pointers whole and
  keep the one that names this document among the names it lists — Step 1's liveness test applied to a
  template, and for the same reason a list here would be the defect:

  ```bash
  grep -m1 -oE 'Companion to `[^`]+`( and `[^`]+`)*' <CORE>/templates/*/*_open_issues_template.md
  ```

  Measured 2026-09-11 in this instance — twelve templates on disk, all twelve carry the pointer, and one
  names two documents: `architecture_open_issues_template.md`, *Companion to `adr/` and `nfdr.md`*. A
  pattern that stops at the first closing backtick reads that one as `adr/` alone, and an `nfdr.md`
  change then finds no template — a live run left one unraised that way on 2026-09-08.

  **Name the file after the document, never after the template.** The pointer you just read gives the
  document as it is named — `SRS.md` — and the companion is that name with `_open_issues` before the
  extension, its case included: `SRS.md` → `SRS_open_issues.md`, `fdr.md` → `fdr_open_issues.md`. That
  is the name the producing skill reads; the template's **own filename** is lower-case, and for a
  one-document template it is not a source for this.

  **A pointer naming more than one document is one companion for all of them, named after the
  template's stem** — `architecture_open_issues_template.md` → `architecture_open_issues.md`, the one
  file `product-architecture` reads (`<CORE>/../skills/principal-architect/.claude/skills/product-architecture/SKILL.md:79`). No one
  document's name is the companion's.

  The first live run took the template's stem and wrote `srs_open_issues.md` beside `SRS.md`
  (2026-08-30, reverted). `product-srs` reads `SRS_open_issues.md`
  (`<CORE>/../skills/cto/.claude/skills/product-srs/SKILL.md:57`), and the sibling skills pair document case with companion
  case the same way, with no exception. On a case-insensitive volume the fold opened it
  anyway; on a case-sensitive one the companion is invisible, and **a companion's absence is the done
  signal** — the document would read settled and the raised change would be gone with nothing
  recording it.

  Fill the title's subject and one item — the bucket above — and **leave the answer slots at their
  placeholders.** That companion is not this run's to answer; it is the next round's — the
  round Step 6 owes it — and answering it now would decide a document you have
  not been through the prompt on.
- **Say in the file that no producing run wrote it.** A blockquote under the header naming the
  companion and the item the change came from, that this run opened it, and why the file exists at
  all. The measured shape is `<Product path>/docs/trail/design/cycle-4.md:27-31`. Without it, the producing
  skill's next run meets a companion it has no record of writing.
- **Never write an empty companion.** `<CORE>/../skills/cto/.claude/skills/product-srs/SKILL.md:200-202` guards against one
  because *"an empty companion would read as OPEN and invert the done signal"*. Here that inversion is
  the point — a settled document has to read open again — which is exactly why the file has to carry a
  real item and not a shell.
- **No template names that document** → record the document and the item in the report, and write
  nothing. The header is a contract Step 1 reads back, so one written freehand is a companion no later
  run can walk.

**Then commit it, check it landed, and only then write the item you were on.** The order is
load-bearing. The slot's answer says the change is carried elsewhere, and the producing skill folds
that answer and drops the item — so if the other companion is not on disk and committed by then, the
fold drops the change on the floor. In order —

1. Commit that companion, in its own repo and its own commit, by Step 6's recipe.
2. `git show --stat` that commit and confirm the file is in it.
3. Only then write the slot, naming by path the file that now carries the change.

**Entry 2 has no slot waiting on it, so the ordering does not bind it** — nothing is about to be
folded and dropped. Commit it the same way anyway: a separate commit in the target's own repo,
checked.

#### Raising a change on the companion you are answering

The document in front of you is a document you read whole, which is more of it than any single item's
author needed to — so it is the document you are most likely to find something in. Until now there was
nowhere to put that. **There is now** (the owner's call, 2026-08-29): the change is raised as **one new
item on the companion you are answering**.

The prompt decides whether the document is owed a change, by the same section and the same bar as any
other document. This step owns only where the item goes:

- **One item, appended to *choices to confirm*.** Which bucket is settled and not judged per run, for
  the reason stated above — a run raising an item has already judged the document owed a change and
  why, and that reason is the lean.
- **It takes the next free number in that section**, continuing the section's own numbering. No
  existing item is renumbered, and no other section moves.
- **The confirm-or-override slot stays at its placeholder.** The reasoning is this run's; the decision
  is the next round's. Answering it here would be deciding twice on your own reasoning with nothing in
  between.
- **It carries the same provenance blockquote a companion opened elsewhere gets**, adapted: this run
  raised it, no producing run wrote it, and what in the document prompted it. That marking is doing
  real work here — the producing skill is about to fold this very file, and the blockquote is how its
  run tells an item nobody derived from the ones it wrote.
- **It rides the ordinary commit.** No separate commit and no ordering: this is the companion Step 6
  already stages, and the item is part of the same act as the answers around it.

**One item, not a list.** If the document is owed several changes, they belong in one item naming
them, or in the one worth a cycle — a companion that grows a queue on a run nobody watched is the
shape the bar in the prompt exists to prevent.

#### When an item splits, the answered half moves out

The prompt's § *An item with two seats splits* decides **whether** an item is two questions with two
seats, what each half's answer is, and what verdict each ends in. None of that is restated here. This
step owns which half moves, where it lands, and how the file says so.

- **The half that moves out is the one you answered**, never the remainder — and the fold is what
  decides it. The original item's slot is what the producing run reads as *that item's* verdict, and it
  drops a resolved item; so an answer written into the original slot carries the item's heading out of
  the file with the owner's remainder underneath it. Moving the answered half out instead leaves the
  original exactly as it stood, slot at its placeholder — § Step 4's *"Nothing that is already in the
  file changes"* holding, not excepted.
- **It lands where a raised item lands.** Appended to *choices to confirm*, taking the next free number
  in that section, confirm-or-override slot left at its placeholder. Same mechanism and the same settled
  reason as above: the reasoning is this run's and the decision is the next round's, and a run holding
  its own answer has a lean, which is what keeps the item out of bucket 1. Nothing here is re-derived
  per run, and **no second append routine is written** — if you find yourself numbering items by a rule
  that is not the one above, that is the tell.
- **Its provenance blockquote says what the original item now means.** The ordinary marking — this run
  raised it, no producing run wrote it, what prompted it — plus the item it came out of, which half of
  that item this is, and **what the original is left asking**. That last clause is doing work nothing
  else does: the original item's heading still names the whole compound question and this skill may not
  edit it, so without the sentence a fold reading the original alone folds a question wider than what
  remains of it.
- **It rides the ordinary commit**, exactly as an item raised on the companion being answered does. No
  separate commit and no ordering — nothing outside this file is waiting on it.
- **One split per item.** Only where the prompt reached one, and never a second pass over an item to see
  what else might come out of it.

**The report carries both halves and the link between them** (Step 5's file):

- **The moved-out half goes in `## Items worked`**, with the verdict the prompt gave it and its
  `**Bucket:**` naming the section it now sits in. It does **not** go in `## Raised on this document`,
  which the template scopes to a change *"no item raised"*
  (`<CORE>/templates/self_answer_report_template.md:127`) — and a split half is one an item raised.
  The wrong section costs the owner the count, not just the filing: the completion notification tallies
  `**Verdict:**` fields, and a `## Raised on this document` entry carries none, so a run that split an
  item and answered half of it would report that it worked nothing.
- **The remainder's `## Left for the owner` entry names the item number the other half now sits under.**
  The prompt already requires each *why* to name the other half; the number is the part only this step
  knows, because it is assigned here.

### Step 5 — Write the run's report beside the companion

**The report is a file, because terminal output dies.** A launcher-driven run has nobody watching, and
after a few cycles the report is the only place the run's residue is visible. Measured on this
instance as a close-out list that *"existed only as scrollback"*.

**Where.** In the answered document's own trail, `<the companion's directory>/trail/<doc>/`, where
`<doc>` is the companion's stem before `_open_issues`, lower-cased. Take that stem and number the run:

```bash
doc=$(basename "${companion%_open_issues.md}" | tr '[:upper:]' '[:lower:]')
report="$(dirname "$companion")/trail/$doc/self_answer-<N>.md"
```

**The trail is the document's record, not the producing skill's**, which is what lets this report sit
in it. `kensaiapp_structure.md` § *A trail is not the document's sibling* states the folder and what
goes in it: the producing skill's `cycle-<N>.md` and this run's `self_answer-<N>.md`, two filename
patterns that cannot collide. Create `trail/<doc>/` if it isn't there.

`N` is one higher than the **highest** `self_answer-<N>.md` already in that directory — list it and
take the max, so a removed or renamed report cannot collide with an existing one. The first is `1`.
Never overwrite an existing report; each is one run's record and they accumulate. The numbering rule
is `product-srs`'s for its trail cycles — *"list the directory and take the max, so a removed or
renamed cycle can't make you collide with an existing one"*
(`<CORE>/../skills/cto/.claude/skills/product-srs/SKILL.md:61-64`), which has the same collision to avoid.

**What it carries** — stamp from **`<CORE>/templates/self_answer_report_template.md`**, the run's own
record, not a retelling of the companion. Its `## ` headings are the parser's contract for
`<CORE>/tools/reporters.py`'s `companion-self-answer` reporter, which composes the run's completion
notification from this file — keep every one, whether or not its section has anything in it, and
write each as you decide its items (never in one pass at the end, per Step 4's own rule). Which
heading fails which way is the template's own note at its head; this skill restates none of its
contents, and reads it there.

**Step 6's launcher list is one of those sections**, `## Launchers owed` — derived there and written
here, which is what puts it in the notification rather than only in a terminal nobody is watching.

**Two of its sections carry what this run reaches beyond the slots**: `## Raised on this document`,
when the document being answered was judged owed a change, and `## Companions opened`, whose entries
say which of opened / appended / updated each was. Both are omitted-or-written by the template's own
rule, which differs from the five required headings; read it there.

A run that halted at Step 1 — no companion named, or the named file not live — **writes no report
file**. There is no companion for one to sit beside, and inventing a home for a file about nothing is
the guess this skill refuses everywhere else. Say what was named and which test it failed instead.

### Step 6 — Commit, then name every launcher

**Commit, and never leave a file dirty.** The hazard is the loop's only real one and every companion's
own header states it: the producing run that closes a round removes the companion, and git refuses to
remove a file carrying uncommitted edits, so an uncommitted answer strands the round.

The repo is the one the companion lives in, which is not always this one:

```bash
companion_repo=$(git -C "$(dirname "$companion")" rev-parse --show-toplevel)
companion_rel="${companion#"$companion_repo"/}"
report_rel="${report#"$companion_repo"/}"
```

**Stage the bound variables, never a path you retyped.** Both are already bound from Steps 1 and 5,
and retyping is where the case of a filename, or a directory that is not there, gets changed without
anyone noticing — the builder then stages nothing and the round is stranded uncommitted.

Then the shared recipe, `<CORE>/doctrine/governance/commit_via_builder.md` — it owns the flag forms, which
of `--actor` and `--role` your run passes, and the staged-set guard, and this file restates none of
them:

```bash
python3 "<CORE>/tools/commit_builder.py" --repo "$companion_repo" commit \
  --add "$companion_rel" "$report_rel" \
  --subject "<document> open issues answered — <n> of <m> items" \
  --body "<the verdict counts, what was left for the owner, and any companion opened elsewhere>" \
  --role "<your posture Role>" \
  --skill companion-self-answer \
  --prompt companion-self-answer/rich \
  --directional "<directional>" \
  --surface "Claude Code" --co-authored-by "<your model> <noreply@anthropic.com>"
```

- **The companion and its report ride one `--add`.** They are one act and one unit — the report is
  what makes the answers reviewable, and a commit carrying only one of them leaves a reader with
  answers and no reasoning, or reasoning about a file that did not move. **Two runs stage less than
  both**, and each is a real path rather than a slip: a companion that was already answered when the
  run reached it (Step 3) leaves the companion untouched, so the commit carries the report alone.
- **A companion opened on another document is its own commit**, made earlier at Step 4 and often in
  another repo — because where an item's slot points at it, it must not be written before it lands.
  Entry 2 has no such slot, and it is committed separately all the same: it belongs to another
  document's round, not to this companion's.
- **`--prompt companion-self-answer/rich`** records the judgment this run followed, which is the one
  thing about a self-answered companion that a later reader most needs and cannot recover.
- **The directional follows the companion's scope**, per
  `<CORE>/doctrine/governance/commit_format.md:54-55` — a companion under `system/` belonging to no one
  project is instance-level and takes `Michi:`; one belonging to a project takes `Shukuba:` when that
  project has an open station and `Agari:` when it does not.
- Check `git show --stat` after committing — exactly the files this run wrote, and nothing else.

**Then name every launcher that must run, and stop.** This run may have answered across documents
and opened companions on several, so it closes with **the whole list** rather than a name. The list
holds one entry per document a round is now owed on, this run's own included. When an answer this
run wrote owes a field of a project's card, the list ends with one more entry, for that card, as
*When an answer owes a field of a project's card* below states. **Which launcher a document's entry
names depends on what its companion holds:**

- **The document this run answered is owed its producing skill**, which folds the answers this run
  wrote. Derive that launcher by the four outcomes below.
- **A document whose companion this run opened, appended to or revised is owed `companion-self-answer`**,
  not its producer. The item this run put there keeps its slot at its placeholder (Step 4), so that
  companion holds a question and no answer, and a producer run on it has nothing to fold. The answer
  run is what sends the item to the seat it names, and that run's own report then owes the producer.
  Its launcher is `<CORE>/launchers/companion-self-answer/launcher.sh`; its `<document>` is the
  companion's filename with `_open_issues.md` taken off — `SDD_open_issues.md` → `SDD`,
  `architecture_open_issues.md` → `architecture`.
- **…unless that companion sits where the answer launcher cannot find it.** It looks in two homes
  only, the product's `docs/` and `system/projects/<project>/`, and refuses anything else (its
  `# USAGE` block). A companion on an instance-level document — `system/doctrine/writing_bar.md`, a
  `system/experience/` document — keeps its producing skill, derived as below. A bullet the launcher
  refuses ends the walk; a producer that folds nothing is the lesser cost.

Measured 2026-10-13 on a live product: a Principal Architect run opened the SDD's companion with one
item seated `cto` and owed `product-sdd` for it. The chain ran that producer, which folded nothing,
walked past the SDD's answer step, and ended with the CTO's item handed to the owner.

Derive each; never assume a path, and never write one you have not seen. A producing skill's launcher
is the first of these that holds:

1. The producing skill's own `launcher.md`, in its skill directory — `<CORE>/../.claude/skills/<producing skill>/`
   or `skills/<group>/.claude/skills/<producing skill>/`. If it exists, the launcher is
   `<CORE>/launchers/skill/launcher.sh <producing skill>`, and its arguments are the ones that file's
   `**Arguments:**` line declares.
2. Otherwise `<CORE>/launchers/<producing skill>/launcher.sh` — if that folder exists, that is it.
3. Otherwise `grep -rl "invoke the <producing skill> skill" <CORE>/launchers/*/launcher.sh`. Why the
   prompt literal and not the skill's name is `companion-answer`'s — *"several launchers mention a skill
   they were adapted from"* (`<CORE>/../skills/interactive/.claude/skills/companion-answer/SKILL.md:346-349`).
4. **None of them** — say so plainly: the skill, and the posture its own file requires. A path that does
   not exist costs more than an honest absence.

The argument follows each companion's altitude, which its path already states. Read the shape where it
is declared — the `launcher.md`'s `**Arguments:**` line, or a launcher's own `# USAGE` block — and write
the **filled-in invocation**: the launcher path, the skill name for the skill launcher, and the
positional arguments declared, with the real values standing where `<project>` and its kind do. Not a command composed from this description, and not that line copied across: it ends
`[--dry-run] [--keep-awake]`, and the brackets are how a usage block spells *optional*, not something
a caller types.

**When an answer owes a field of a project's card, the card's entry comes last.** A project's card,
`system/projects/<project>/project.md`, is written by the `product-card` skill, and a round on it is
a `product-card` run. When an answer this run wrote into a slot states that a field of a project's
card is owed a value the card does not hold, that card is owed a `product-card` run, and the list
names it.

- **Only an answer written into a slot counts.** An item whose verdict is `left for the owner` keeps
  its slot at its placeholder. An item whose verdict is `raised upstream` has its answer written on
  another document's companion, not into a slot here. Neither owes the card anything this run,
  whatever field its question names or its answer would have given.
- **Every field the card carries counts.** The card states its own fields. Read them there, and keep
  no list of them in this file.
- **One entry per card.** However many answers or fields owe the same card, it gets one bullet. A
  second bullet for the same card would name the same command twice.
- **Last.** The card's bullet comes after every document's bullet, the honest absences included.
- **The launcher is `<CORE>/launchers/product-card/launcher.sh`, seen on disk.** Its one positional
  argument is the project's name. Write the bullet in exactly this shape, with the real project name
  in place of both `<project>`s and `<CORE>` written as it stands:

  ```markdown
  - **system/projects/<project>/project.md** — `<CORE>/launchers/product-card/launcher.sh <project>`
  ```

  The launcher's `# USAGE` line ends `[--dry-run] [--keep-awake]`. Neither flag belongs in the
  bullet, and nothing follows the command's closing backtick, as for every other bullet in this list.

A run whose answers owe no card field writes no card bullet, and adds no section to the report.

**Every document under `## Companions opened` gets a bullet here. No exceptions.** Opening a
companion on a document *is* owing that document a round — that is what a companion is — so every
document `## Companions opened` names is also named under `## Launchers owed`. This is the sentence
that says so, rather than leaving it to be inferred from "a round is now owed on". The rule runs one
way only. `## Launchers owed` also names the document this run was invoked against, and a project's
card when an answer owes it a field, and neither of those is a companion this run opened. Each
opened companion's entry is its answer step, above, wherever that launcher can find it.

**The chain refuses the whole walk when an opened companion has no bullet**, and it does so hours
later, in a session nobody is watching. `<CORE>/tools/chain.py`'s `unrouted_companions` looks for
each document under `## Companions opened` among the `## Launchers owed` bullets, and ends the cycle
`no_runnable_command` when one is missing — *"a report the chain cannot route whole is not a round it can measure
progress across"* — because a companion nothing runs takes its whole sub-graph with it. Measured
2026-09-03: `docs/trail/sdd/self_answer-5.md` opened `docs/SRS_open_issues.md` under
`## Companions opened`, listed only `docs/SDD.md` under `## Launchers owed`, and the definition chain
stopped on it — forfeiting the `product-sdd` fold that same report had correctly asked for, and
leaving the SRS companion with no route at all.

**So check the two sections against each other before Step 6's commit**, while the cost is one line
of editing rather than a dead walk: read `## Companions opened`, and for each document it names,
find that document's bullet under `## Launchers owed` and confirm it runs `companion-self-answer`
wherever that launcher can find the companion.

**Do not reach for outcome 4 to satisfy this.** Outcome 4 is about a producing skill's launcher, so it
bears only on the answered document and on a companion the answer launcher cannot find. The honest
absence below is written when a launcher
genuinely cannot be derived, and it is a bullet naming a producing skill rather than a path — a shape
`validate_owed_command` refuses, because a bare name fails `os.path.commonpath` against an absolute
launchers directory (`<CORE>/tools/chain.py`, which records it as a live shape at that raise). It
halts the chain exactly as a missing bullet does, so it buys nothing here. Where a companion has a
derivable launcher, derive it; where the absence is real, write it knowing the walk will stop on it
and that the stop is what brings a person in. Whether that forfeit should end at all is open work
elsewhere, not this file's to pre-empt.

**The bullet is run, not read.** `<CORE>/tools/chain.py` takes the backticked command apart into
tokens and executes it, so what belongs inside the backticks is what a shell would accept and nothing
that only means something to a person. The flags are not this bullet's to carry in any form:
`--keep-awake` is the caller's own instruction and the chain appends it after validating, and
`--dry-run` would make the launcher print a command instead of running one — the run would look like
it happened. Measured 2026-09-01, on the chain's first live walk: one report quoted the usage line
whole for all four of its bullets, and all four were refused.

**The bullet ends at that command. Nothing follows it.** Not the block's flag descriptions, not a
condition, not an ordering. Two things happen when something does, and both were seen on a live FDR
report (2026-08-30). The flag lines came across as *"(run from the instance root; `--dry-run` prints
the command …)"*, which is *read the `# USAGE` block* above taken as the block rather than as the one
invocation in it.
And one bullet gated its command on the owner filling *"§ 2.1's confirm-or-override slot"* — a
section number carrying no file, written into a report holding a § 2.1 of its own. They were
different items in different files: the report's own § 2.1 was answered, the one the bullet meant was
still empty. **A reader resolves the tail against the file in front of them and reaches the opposite
answer** — the gate looks met and is live. That is what makes a tail unreadable rather than merely
redundant, and what recovers it is a sentence elsewhere in the report naming the other file, which no
parser and no hurried reader will reach. What the tail wanted to say is already carried where it stays true — the
`**Verdict:**` field, `## Left for the owner`, and `## Companions opened`.

The list goes
in the report as well as to the session — its `## Launchers owed` section, Step 5 — for the same
reason the report exists at all, and because the completion notification reads it from there: a
launched run has nobody in the terminal to read the list out to.

Then stop. Running them is the owner's move.

---

## Outputs

| File / effect | Produced when |
|---|---|
| The companion, answered in place, with its report, in one commit | At least one item was worked (Steps 4–6) |
| One item raised on that same companion, appended with its provenance, in that same commit | The document being answered was judged owed a change no item raised (Step 4) |
| The answered half of a split item, appended to *choices to confirm* with its provenance, in that same commit, and reported under `## Items worked` | The prompt found an item to be two questions with two seats and reached an answer on one of them (Step 4) |
| A companion opened on another document, or an item appended to or revised on an existing one, carrying its provenance, in its own commit | A change belonged to that document — routed by an item, or found while reading it (Step 4) |
| Open items outside the invocation's list, recorded under `## Skipped` as another seat's, with no `**Verdict:**` field and their slots untouched | The invocation listed items and the companion holds open items it did not list (Step 3) |
| The report file, one per companion worked, numbered and never overwritten | Every run that touched a companion (Step 5) |
| The launcher list — one entry per document a round is now owed on: the producing skill for the document answered, `companion-self-answer` for each companion opened elsewhere that its launcher can find, and last, when an answer this run wrote owes a field of a project's card, `product-card` for that card | Every run that committed (Step 6) |
| No change; what was named and which liveness test it failed | The invocation named no companion, or the file it named is not a live one (Step 1) |
| The commit as usual, and in place of a launcher the roles the header named, or the skill and the posture it needs | The header names no skill to re-run (Step 2), or no launcher exists (Step 6) |

No document is ever written. No companion is ever deleted. No producing skill is run and no agent is
spawned, on any path.

---

## Critical Rules

- **The deciding is the prompt's, and it is read whole every run.**
  `prompts/rich.md` holds the checks, the seats and the verdicts. This file
  holds none of them, and a run that decides from a remembered summary decides from the drift.
- **Discover, never list.** Which document, which skill, which sections, which slots, which template —
  every one comes from the file in front of you. A list of producing skills in this skill is the
  defect, not the shortcut.
- **Answer a live companion, never a copy.** Companion-shaped files sit in archives, fixtures,
  evidence trees and extracted layers, and they read identically. The header's pointer is the test, and
  an answer written into a copy is silently lost.
- **Three kinds of file, and no fourth.** This run writes the companion it is answering, a companion on
  another document, and its own report. **No document is ever written** — not the one being answered,
  not the one a companion is opened on, not one read and judged owed a change. A change reaches a
  document only through that document's own producing skill, on its fold, which is the whole reason a
  companion is opened instead of the document edited.
- **Slots at their placeholder, plus what it appends — nothing else.** Inside a companion: never its
  header, never another actor's slot, never a filled one, never an unlisted one when the invocation
  lists items, never an existing item's number. The three
  additions this skill may make are a raised item on the companion it is answering, the answered half of
  an item the prompt found to be two questions with two seats, and a raised or revised item on another
  document's. Each is bounded where it is stated.
- **A listed run writes its own items and no others.** Given `Answer only these items: <n>, <n>.`,
  it decides the listed open items and leaves every other open item untouched under `## Skipped`,
  with no verdict field. Given no list, it decides every open item. Raising, splitting, opening
  another companion, numbering the report, committing and naming the launchers are the same either
  way, and an item can only split off a listed one, because only a listed one is decided.
- **An item left for the owner keeps its placeholder, and its answer goes in the report.** The
  unanswered slot is what carries it through the fold; the report is what tells the owner it is theirs
  and what this run would have decided. A left item with no answer under it is half a verdict.
- **A companion opened elsewhere is committed and checked before the item that points at it is
  written.** The producing skill folds that answer and drops the item, so a file not on disk by then
  loses the change.
- **Never create the companion you are answering, and never delete any companion.** A companion's
  presence is its document's open state and its absence is the done signal — *"The companion's absence
  is the done signal, and that is when the item is ticked"*
  (`<CORE>/doctrine/setup/setting_up_an_instance.md:66-67`). On the document being answered, both
  transitions are the producing skill's. Opening one on a *different* document is a
  different act, and it is this skill's.
- **Never write an empty companion.** A shell inverts the done signal without carrying the change that
  justified it.
- **The report is written and committed with the companion.** A run whose record exists only as
  scrollback is a run nobody can review, and nobody was watching it.
- **Owe each document the step its companion is ready for.** The document answered is owed its
  producing skill, which folds the answers. A companion opened elsewhere holds only an unanswered
  item, so it is owed `companion-self-answer`, and that run owes the producer — unless the companion
  sits outside the two homes that launcher reads, where it keeps its producer.
- **Name a launcher you have seen.** For a producing skill: its `launcher.md`, then its folder, then the
  prompt-literal grep, then an honest "there is none — here is the skill and the posture it needs." For
  an answer step: `<CORE>/launchers/companion-self-answer/launcher.sh`, on disk. For a project's card
  that an answer this run wrote owes a field: `<CORE>/launchers/product-card/launcher.sh <project>`,
  on disk, once per card, as the last bullet.
- **It stops at naming.** No spawn, no posture check, no fold, no re-run.
