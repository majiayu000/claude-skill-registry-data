---
name: kensaiapp-writing-bar
description: Content-Manager-posture skill that authors an instance's writing bar — the bar every document kensaiapp authors in that instance is held to — and writes it to `system/doctrine/writing_bar.md`. Producing that document is the run's output; core states no bar to fall back on, so every instance holds its own. Instance-level, never per-product, and never about a product's words. Requires Content Manager posture (halts if invoked outside a `content-manager:` session or the `content-manager` subagent). Non-interactive by design — it states the bar best-effort from the instance's identity, Michi and domain doctrine and the writing craft this seat holds, and instead of interviewing live it puts whatever it could not settle, and the calls it made on its own authority, into a companion open-issues file the owner answers on their own time; a re-run folds the answer in, retires the answered companion whole to a permanent trail, and deletes the companion when nothing is left unresolved. Step 3 of instance setup, mandatory, after identity and Michi and before the experience pair; it halts where either is still a placeholder. Use when authoring or revising an instance's writing bar, at instance setup or any time after, and whenever someone asks what bar this instance's own documents are written to. Do not use for the instance's identity or Michi (`kensaiapp-michi`), the experience layer (`experience-visual`, `experience-voice`), one product's words (`product-content`), or any product document.
license: MIT
metadata:
  author: Eyal Golan
  version: "6.3.6"
  created: "2026-08-16"
  category: instance-setup
  tags: writing-bar, instance-setup, content-manager, doctrine, house-style
  risk: safe
---

# kensaiapp-writing-bar

## Purpose

State the **instance's** writing bar — the bar every document authored here is held to.
`prompts/rich.md` owns which documents that reaches, and this
skill does not enumerate them: the list has one owner, and a copy here would be a second.

**The run's output is the bar.** An instance authors documents, those documents have a reader, and
this is the one file where what that reader needs is written down. Nobody else states it, and a bar
nobody stated is not some other bar quietly holding, and every future author guesses.

This runs at the **instance** altitude, as **step 3** of `<CORE>/doctrine/setup/setting_up_an_instance.md`,
which owns the sequence, why step 3 sits where it does, and that the step is mandatory. Nothing this
skill writes says anything about any one product.

This file is the **orchestrator**: posture, the file loop, path resolution, staging and the commit.
**What a bar states and how to author it** — what a writing bar covers, what grounds each rule in it,
what a writing bar reaches, how a rule is worded so a reader can check it, and what goes to the owner
instead of being settled — is the authoring prompt
**`prompts/rich.md`**, applied at Step 2; a rule named below without
its content lives there. The documents' **section shape** is
**`<CORE>/templates/writing-bar-templates/writing_bar_template.md`** and
**`<CORE>/templates/writing-bar-templates/writing_bar_open_issues_template.md`** beside it. Neither is summarised here. That prompt names this skill as its carrier from its own side,
and this paragraph is the other half of the same declaration — the pair is declared on both sides
rather than inferred (`<CORE>/doctrine/setup/authoring_layers.md` § The carriers).

**Non-interactive.** The run never blocks on the owner. It reaches its recommendation best-effort,
writes what it cannot settle into the companion, and a re-run folds the answer in. That is what lets
it run headless (as the `content-manager` subagent) as well as in an interactive `content-manager:`
session.

---

## Posture

**Content Manager role required.** If invoked outside Content Manager posture (neither a
`content-manager:` session nor the `content-manager` subagent), stop and say: *"kensaiapp-writing-bar
requires Content Manager posture. Switch? (Open a session with the `content-manager:` prefix, or run
the `content-manager` subagent.)"* Do not shed the role.

**Why this seat holds the writing bar, and the seat's reach over the instance's own bar, are
`<CORE>/roles/loaders/content_manager_global.md` § What you own** — stated there, argued there, and
not restated here. Read it before Step 2.

---

## The files and the loop

Everything lands under `system/doctrine/` in the instance repo. A caller names nothing — there is one
instance, and this skill is running in it.

| File | What it is | Lifecycle |
|---|---|---|
| `system/doctrine/writing_bar.md` | The instance's own bar, and this skill's output. | Permanent, revised and versioned in place. |
| `system/doctrine/writing_bar_open_issues.md` | The companion — the calls awaiting the owner: what the run could not settle, and what it decided on its own authority. | Transient. **Its absence is the done signal.** |
| `system/doctrine/trail/writing_bar/cycle-<N>.md` | Each answered companion, retired whole. | Permanent. |

**The companion's absence is the only done signal here.** No writing bar does not mean a settled
state — a missing `system/doctrine/writing_bar.md` means this skill has not landed in this instance
yet, not that the instance is fine without one
(`<CORE>/doctrine/setup/kensaiapp_structure.md` § Instance-shared doctrine).

Step 3 of the loop is why the trail exists. Folding rewrites the companion and the close removes it —
so without the trail the owner's answers are destroyed twice, and their reasoning for a decision
survives only in git history. The trail costs one `cp` on the same commit and makes every owner answer
permanently citable. It is the skill's job; the owner never manages it.

**Cycle numbering:** `N` is one higher than the **highest** `cycle-<N>.md` already in
`trail/writing_bar/` — list the directory and take the max, so a removed or renamed cycle cannot make you
collide with an existing one. The first is `cycle-1.md`; create `trail/writing_bar/` if it isn't there.
Never overwrite an existing cycle.

**The loop, repeated until clean:**

1. The run **authors the writing bar**, and writes the companion with whatever it could not settle and
   whatever it decided on its own authority — or writes none, where there is nothing of either.
2. The **owner answers inline** — filling the companion's answer slots, whose names and shape are
   `writing_bar_open_issues_template.md`'s — and re-runs the skill.
3. The run **copies the answered companion whole to the next trail cycle**, folds the answers in, and
   rewrites the companion with only what is still unresolved. This is the ordinary cycle — something
   survives the fold. Step 2's § *Consuming an answered companion* owns the moves and their order.
4. When the answers resolve everything, the companion is **removed** rather than rewritten — through
   the builder, Step 3's `--rm`, never a hand-`rm`. **No open-issues file = the writing bar is
   settled.** The close has a precondition the
   ordinary cycle does not: the owner's answers must already be committed, because git will not remove
   a file with uncommitted edits in it and their words are not yours to commit. Re-entry is inline
   answers, so the first closing touch normally finds them uncommitted — and then it **changes nothing
   at all**: no fold, no trail copy, no rewrite, no commit; the companion survives intact, answers and
   all, for the owner to commit. It reports the state, asks for that commit,
   and the re-run after it is the close. That stop is a report with an ask, not a live interview.

---

## Inputs and where the files land

Every path below is instance-relative and resolves from the instance repo root — the directory the
session opened in. No step `cd`s away from it. There is no product path to resolve here; that is the
difference between this skill and the `product-*` family.

- **`kensaiapp.md` § "What this is about"** and **`system/michi.md`** — what this instance is for and the
  Way it steers by. Read both in full. They are the primary grounds for the bar — what an instance is
  for is what its bar answers to. If either is still an unfilled placeholder, **halt**: name the file
  you found, say that step 2 (`kensaiapp-michi`) has to land first, and write nothing. A bar derived
  from a placeholder binds every document in the instance and rests on nothing, and there is nothing at
  core to fall back on (`<CORE>/doctrine/setup/setting_up_an_instance.md` § What fixes the order,
  *2 before 3*, which owns that gate).
- **`system/doctrine/`** — **list the directory** and read everything in it. The instance's domain
  doctrine is one of the grounds the prompt names, and the prompt says what to take from it. The
  writing bar, its companion and the trail above are the loop's re-entry point.
- **`system/doctrine/trail/writing_bar/`** — every answer the owner has already given, and their
  reasoning. Read it. A decision the owner settled in an earlier cycle is authorized, and this run does
  not reopen one on its own initiative: where it has fresh grounds, they go to the companion as a
  choice to confirm and the bar changes only if the owner answers (the prompt's § *On a re-run — fold,
  don't re-author*). It also gives you the next cycle number.
- **Whatever the owner handed you** — a brief, a standard this instance holds, a regulator's
  requirement, a house style from something already shipped. Read it and treat it as evidence with an
  origin you can cite.

**The experience layer is not an input.** `system/experience/` is written at step 4, *after* this one,
by two runs whose own sentences this bar governs — the order `setting_up_an_instance.md` § What fixes
the order fixes at *3 before 4*. Where it already exists from an earlier setup, reading it is allowed
and deriving the bar from it is not: it would ground the standard for every document here in one
later layer's wording.

**No product's documents are inputs.** A product's PRD, UXD or `CONTENT.md` is downstream of this bar,
and a product's *words* are a different object with a different owner. Where you believe a product's
evidence should shape the instance's bar, that is an open issue for the owner, not a derivation you
make.

---

## Workflow

### Step 1 — Read current state

Read everything under *Inputs and where the files land*, in that order. Three things to establish
before writing anything:

- **Whether `system/doctrine/writing_bar.md` exists**, and if so what it states. None means this is a
  first run.
- **Whether a companion sits beside it.** No writing bar and no companion and no trail means this is a
  first run.
- **Whether an existing companion is clean in git** — run `git status --porcelain -- system/doctrine/writing_bar_open_issues.md`.
  Output means the owner's answers are uncommitted, which Step 2's gate reads.

### Step 2 — Author the bar (no interview)

**Gate first — detect the first closing touch before you write anything.** Where a companion existed
at intake, its inline answers would resolve everything unresolved in it, and the file is uncommitted,
this run is the first closing touch and writes nothing: no decision, no authoring or fold, no trail
copy, no companion rewrite. Skip the rest of this step and Step 3 and report CLOSING at Step 4.

**Author the bar.** Apply **`prompts/rich.md`** — it owns what a
writing bar covers, what grounds each rule, and how a rule is worded so a reader can check it. Write
or revise `system/doctrine/writing_bar.md` from
`<CORE>/templates/writing-bar-templates/writing_bar_template.md`.

**This skill never removes a writing bar.** Where the run disagrees with the bar already on disk it
changes nothing that bar states — no rule, no recorded absence — and raises the disagreement in the
companion. The `Status:` line and the `Version:` bump below are not what *disagrees* reaches: they are
the loop's bookkeeping, and a run that raises a disagreement has just put a companion on disk, which
is what `Status:` reports.

**Removing an instance's writing bar is the owner's alone.** Removing that file leaves every document
in the instance with no bar at all, so no run makes the call on its own reasoning. It happens on the
owner's explicit instruction and nowhere else.

**And the grounds are preserved before the file goes.** A writing bar is the only place its own
reasoning is written down, so a removal that does not first copy it somewhere permanent takes the
argument with it and leaves the next owner re-deriving a decision that was already made. This skill
runs no removal, so that copy is the remover's — the rule is that the copy exists, not which mechanism
made it.

Write the companion from `writing_bar_open_issues_template.md` beside it — **only where something is
unresolved.** The companion carries what the evidence could not settle and what the run decided on its
own authority; the bar itself is never an item in it. A first round with nothing unresolved therefore
writes no companion and stamps the bar **Settled**, which is the honest state and not a skipped step.

Set the writing bar's `Status:` line from Step 4's DONE condition — the companion being absent — not from
your tally of answers: **Settled** only when this run ends with no companion on disk, which is the run
that removed one; **Draft** otherwise. The two cannot diverge: the only run that folds every answer is
the close itself,
which ends with the companion removed, and the first closing touch writes nothing at all — the writing
bar included — so no writing bar is ever stamped Settled beside a companion still on disk (the loop,
step 4). Leave **Locked** alone — ratification is the owner's act, not yours.

**Bump the document's `Version:` line on any run that changes its content, and the `Status:` line is
content.** A fold that settles no rule but leaves companion items still stamps that line, so the run
has changed the document and takes a bump like any other.

**This run invokes no linter, and there is no exit code to read.** A writing bar has no
machine-checkable format, so nothing mechanical will catch a bar too vague to check; the bar that
replaces the machine is the prompt's, and the run meets it by wording rather than by passing
anything. Do not introduce a check here that this skill cannot actually run.

Do **not** interview. When nothing is unresolved, write no companion — an empty one would read as
open and invert the done signal.

**Consuming an answered companion.** A companion that existed at intake with at least one answer slot
filled is **consumed** — what counts as an answer slot is the companion template's, read from its
current shape, never from a name remembered here, so a template rename cannot make filled answers read
as unfilled. Consuming is three moves, in this order: copy the companion whole (an ordinary `cp`) to the
next trail cycle, *before* the fold rewrites it; fold the owner's answers into the writing bar; then
drop every **answered** item from the companion.

**An answered item never survives the drop.** Where the prompt's fold rule settles the answer, the item
is resolved and gone. Where the answer leaves something unsettled, the item still drops and the residue
**re-enters as a fresh item with an empty answer slot** — a new item this run raises, never the old one
surviving. Whether an answer settles its item is the prompt's fold rule (§ *On a re-run — fold, don't
re-author*); this step only moves the files that rule implies. What the drop buys is the invariant the
rest of the loop keys on: a filled slot in a surviving companion is always the owner's writing, never
this run's, so a run's own rewrite can never re-fire this detection at the next intake.

A companion with no slot filled is not consumed — no trail cycle, nothing to fold. And when the drop
resolves **every** item, the *write no companion* rule above owns the disk: leave the companion as
intake read it (the trail copy already holds it) and let Step 3's `--rm` remove it. No state of this
run — a halt between Step 2 and Step 3 included — ever leaves an empty companion behind.

### Step 3 — Commit through the builder

Commit through the shared builder — read `<CORE>/doctrine/governance/commit_via_builder.md` and supply its
variables. The builder stages, derives `Role:`, and lays the whole trailer block; this step never
hand-writes a `git commit`, spells a trailer, `cd`s into the repo, or resolves the directional *shape*.
What follows is only the values this skill feeds it.

`<repo>` is the instance repo — `.`. There is no product repo in this skill.

**A run that changes nothing builds no commit — and touches no disk.** If this run folded no answer,
changed no document, and has nothing to stage, make no file change at all. Report the state (Step 4)
and stop. **A first round always has something to stage** — it writes the bar.

**The stage list — compose it from what this run actually did.** Pass every qualifying path in one
`--add` and every removed path in one `--rm`.

- `--add system/doctrine/writing_bar.md` — **always, on any run that builds a commit.** Not only when
  this run changed a rule: the bar carries the `Status:` line the run just set, and a commit that
  leaves it unstaged is what lets the bar and the companion disagree about whether anything is still
  open.
- The companion, exactly one of: `--add` it (something is unresolved) · `--rm` it (nothing unresolved
  *and* it existed at intake — its removal is the done signal) · **neither** (nothing unresolved and
  none existed, **or** Step 2's gate fired). A gated run's companion takes **neither**, never `--rm`:
  its answers are the uncommitted ones the gate was detecting, and `git rm` refuses a file with local
  modifications.
- `--add system/doctrine/trail/writing_bar/cycle-<N>.md` — when this run consumed an answered companion.
  The trail copy rides the same commit as the fold it precedes; neither happens without the other.

**Actor:** `--actor content-manager --skill kensaiapp-writing-bar` when running as the `content-manager`
agent; from an interactive `content-manager:` session with no agent named, `--role "Content Manager"
--skill kensaiapp-writing-bar` instead. Both derive `Role: Content Manager`.

**And `--prompt kensaiapp-writing-bar/rich`**, naming the body this skill is the carrier for. A thin skill over a fat prompt is recorded by both lines and neither implies the other (`<CORE>/doctrine/governance/commit_format.md` § *`Prompt-Version:` trailer*); it takes the bare name, never a path.

**The directional is `Michi:`, not `Shukuba:` or `Agari:`.** This commit touches no single project —
it is instance-level, and the directional trailer follows the commit's scope rather than what kind of
thing produced it (`<CORE>/doctrine/governance/commit_format.md` § Directional trailer). Resolve it
against `system/michi.md`. The recipe's parenthetical that producer skills are project-level describes
the `product-*` family; this skill is the exception, which is why it is said here.

Subject, body and the surface / co-author trailers are the recipe's variables — fill them per the
recipe, not from an example copied here.

### Step 4 — Close / report

Report:

- **the bar, in one line** — its reader and what it turns on — and the grounds it rests on;
- **all five parts a bar states, and where each landed** — the rule it produced, the companion item it
  became, or the recorded absence. Every part gets its line, including the ones that produced nothing.
  This is where the prompt's never-silently-dropped guarantee is checked, so it is not abbreviated on a
  run that settled little;
- the path of the writing bar, and the commit SHA — or that the run changed nothing and built no
  commit;
- on any run that consumed an answered companion, the **trail cycle path** — so
  the owner can see their answers survived without opening the commit;
- the **loop status**, exactly one of:
  - **DONE** — no companion remains and nothing is unresolved. The bar on disk is what binds every
    document authored here.
  - **CLOSING** — the owner's answers resolve everything, but the companion is dirty, so this run was
    the first closing touch and changed nothing. The one ask is: commit the companion, then re-run.
  - **OPEN** — something is still unanswered. Give a count per bucket under the bucket names the
    companion on disk carries, name where they live, and name the next move: the owner answers inline,
    commits, and re-runs `kensaiapp-writing-bar`.

Then name the one thing that comes next and stop. On a first setup that is step 4a, `experience-visual`
— which this skill neither runs nor anticipates the result of. Do not enumerate anything further
downstream; settling this instance's bar is this skill's whole job.
