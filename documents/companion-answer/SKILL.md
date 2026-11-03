---
name: companion-answer
description: |
  Walk an open-issues companion with the owner, one item at a time, in plain language, and write their
  answers into it. A document authored non-interactively parks whatever its run could not settle in a
  `*_open_issues.md` companion beside it. This skill finds that file, learns from its own header which
  document it belongs to and which skill re-runs it, puts each unanswered item as a question a person can
  answer — offering an opinion and the grounds for it where it has one — writes the answer into that
  item's slot, commits it, and names the launchers to re-run. An item belonging to another document
  opens that document's companion. Then it stops.
  Use when the owner wants to go through an open-issues file, answer a companion's questions, settle what
  a run could not, or be walked through a document's open items — including when they merely report the
  state and expect the walk to follow, or name the document rather than the file.
  Trigger phrases: "we have a new companion", "there are open questions for X", "X has open issues", "the
  run left some questions", "a companion landed for X", "walk the companion", "go over the open issues",
  "answer the open-issues file", "one by one, plainly", "what's still open on X", "let's close the open
  items on X", "companion-answer".
  Do not use for: writing or revising the document itself, deleting a companion or creating the one it
  walks, running the producing skill (this names its launcher and stops), or a
  Nemawashi seed / Shukuba station (the journey skills).
license: MIT
metadata:
  version: "2.3.4"
  category: companion-loop
  risk: safe
  created: "2026-08-21"
---

# Companion Answer

## Purpose

**Turn a parked question into an answered one.** A document written without stopping to interview the
owner leaves what it could not settle in a companion file beside it. Answering that file is the owner's
move, and today it is made by opening the file and typing into slots, or by asking a session to go
through it. This skill *is* that ask: it walks the items one at a time, in plain language, and writes
down what the owner says.

**It fills slots. It does not write the document.** The owner's answers reach the document on the
producing skill's next run, which folds them in, copies the answered file to its trail, and clears the
resolved items. None of that is this skill's. It writes into the companion, commits, and names the run
that consumes it.

**A companion's absence is the done signal** — `<CORE>/doctrine/setup/setting_up_an_instance.md`
("**The companion's absence is the done signal, and that is when the item is ticked**", `:66-67`). So
the companion being walked is never created here, and no companion is ever deleted here. Creating the
file you are walking would announce work its document does not owe. Deleting one would declare a
document done that nobody folded anything into. Both of those are the producing skill's, on its own run.

**Opening a companion on a different document is a different act, and it is permitted** (owner,
2026-08-29). An item often belongs not to the document being walked but to one upstream of it:
a live `docs/fdr_open_issues.md` says of its first item that *"moving the terms after sign-in
is the CPO's change and not mine to draft"* (`:25`). That upstream document is settled, so no companion
sits beside it, so a re-run of the skill that owns it reads it as done and has nothing to act on. Until
now the owner opened those files by hand — `<Product path>/docs/trail/design/cycle-4.md` is one of them:
*"**This companion was opened by the owner, not by a `product-design` run.** … this document's loop has
no other channel"* (`:27-31`). Step 4 opens it instead, on the owner's word.

**The cited doctrine says what a companion's presence means, and names no one who may open one.** Its
sentence governs when a setup-seed item is ticked. Reading a general prohibition out of it was this
skill's own inference, and it is withdrawn here (2026-08-29); what survives is the narrower rule above,
which is the part the citation actually carries.

**It spawns nothing and runs nothing.** The skills that produce these documents halt outside their own
posture, so re-running one would mean spawning a posture agent — a decision that belongs to the owner,
not to the run that just took their answers. This skill names the launchers and stops. Naming them is the
last thing it does.

## It is general, and that is the feature

**This skill knows no list of producing skills, documents, or companion paths, and must never grow one.**
Every fact it needs is on the companion itself:

| What it needs | Where it reads it |
|---|---|
| Which files are candidates | the filename — every companion is `*_open_issues.md` — inside a document home, one level deep |
| Which document it belongs to | the header's "Companion to `<document>`" |
| Whether it is live or a copy | the same pointer — a live companion sits where it says its document is |
| Which skill re-runs it | the header's own "re-run `<skill>`" |
| Which sections exist | the `## ` headings actually present |
| Which slots the owner fills | the header's own "fill each **X** / **Y** slot" instruction |
| Which repo to commit in | `git rev-parse --show-toplevel` from the companion's directory |

A hard-coded list would be a copy of a set that already moves — a new producing skill would be invisible
to this one from the day it lands, and the failure would look like "no open issues" rather than like a
stale list. If a future edit is tempted to name one, that is the tell that a fact was not being read from
the file.

The two slot labels are the measured convention, not a guess:
`<CORE>/templates/authoring-templates/document_template_template.md:186-190` records them as exact across
every companion shape and states that **a consumed companion is detected by a filled slot** — which is
why this skill reads a label from the header in front of it rather than from memory, and why it leaves a
filled slot alone.

## Input

**Posture-neutral** — any session may walk a companion. The owner is present and answering; this skill
is useless unattended, because every item it walks is a question only they can close.

The invocation may name the companion (a path, or the document it belongs to), or name nothing at all —
Step 1 finds it either way.

## Workflow

### Step 1 — Find the companion

If the invocation named a file, use it, and run the liveness test below on it anyway — the file named is
as easily a copy as one you found yourself. Otherwise enumerate.

**Look in the document homes, and look only one level deep.** A companion sits *beside* the document it
belongs to, so the homes are wherever documents live, and each is globbed rather than walked:

```bash
ls "$root"/system/*/*_open_issues.md              # the instance's own documents
ls "$root"/system/projects/*/*_open_issues.md     # the project cards
ls "$product"/docs/*_open_issues.md               # each product, one per project
```

`$product` is each `Product path:` read from `system/projects/<name>/project.md` — relative resolves
inside the instance, absolute into the product's own repo. Where the run was pointed at a directory with
no project cards in it, that directory is the product and its own `docs/` is the third home.

**Non-recursive is the whole point, not an optimisation.** A `find` over the same roots returns every
companion-shaped file the tree happens to contain, and those are numerous: eval fixtures, harvested
evidence, archived guard trees, worktrees, layers extracted from other repos. Measured in this instance
on 2026-08-21, a repo-wide `git ls-files '*_open_issues.md'` returned 31 files and the three globs above
returned none — which is the correct answer, because every document here is settled. A recursive walk
would have offered thirteen of those 31 as live, all of them under a real `Product path:`, because a
fixture's `PRD_open_issues.md` genuinely does sit beside a `PRD.md`. Depth is what tells a document home
from a tree that contains one.

**Then keep only the live ones, by asking each candidate where it thinks it lives.** The homes narrow
the search; this is the check. A copy filed *into* a home still reads as a companion, and the header is
what catches it. Every companion's header opens "Companion to `<document>`", and that pointer is the
test:

- The header names a **path** — two conditions, both required. **Resolve the path against the root you
  searched**, never as a suffix of where the file happens to sit: the document must exist at
  `<root>/<the path>`, *and* the companion must be sitting in that same directory. A file naming
  `<dir>/<doc>.md` from anywhere else is a *copy*: an archived round, a tree extracted from another
  repo, a fixture. Nothing folds it in, and an answer written into it is lost.
  - Both conditions earn their place, and each catches what the other misses. Resolving as a suffix
    passes any nested tree whose tail happens to match — a fixture at
    `<somewhere>/system/standards/x_open_issues.md` reads as live against a root that has no
    `system/standards/` at all. And the document existing at the resolved path is not enough on its own:
    a reference copy filed under a project's `docs/` names a real document it is not beside, which is
    exactly what makes it a copy.
- The header names a **bare filename** — the companion is live only if that document is its sibling on
  disk.

```bash
grep -m1 -o 'Companion to `[^`]*`' "$candidate"
```

This test replaces the obvious alternative — a list of directories to skip — and it is worth knowing why.
The places companion-shaped files accumulate are not fixed: eval fixtures, evidence snapshots, archived
guard trees, worktrees and extracted layers each arrived at their own time, and a skip-list learns about
the next one only after it has misfired. A companion that names the document it belongs to is a
self-describing file, and asking it is a check that keeps working.

Then:

- **Exactly one** — that is the companion. Say which document it belongs to before you start.
- **Several** — list them with the document each belongs to, and **ask which**. Do not pick, and do not
  offer to do them all in one run: each has its own producing skill and its own commit.
- **None** — nothing is open, which is what a finished document looks like. Say so, and say **what you
  searched and what you rejected** — the homes you globbed, how many candidates they returned, and how
  many of those failed the liveness test. An empty result and a broken search look identical from the
  outside, and the search you can show is the only thing that tells them apart.

### Step 2 — Read the header, and derive the run's four facts

The header is the blockquote under the title. Read it whole, and take from it:

1. **The document** — "Companion to `<document>`". You will name it when you start, so the owner knows
   what they are answering about.
2. **The producing skill** — "re-run `<skill>`", backticked. This is what Step 5 names.
3. **The slot labels** — "fill each **X** / **Y** slot". These drive Step 3.
4. **The trail promise** — the header tells the owner their answers are copied whole to a trail folder
   before being folded in. **That copy is the producing skill's, on its fold — not yours.** Do not make
   it, and do not offer to: a trail copy made before the fold records a round that has not happened.

**When the header names no skill to re-run.** Some companions are the baton in a loop between two skills
rather than a re-run of one, and their header says so in prose without backticking a skill name. Do not
guess and do not grep for a plausible one. Carry what the header *does* say — the roles it names and the
order it gives them — into Step 5, and ask the owner who moves next. A named role with an honest question
is worth more than an invented skill name, which the owner would have to catch.

### Step 3 — Work out which items are yours to walk

Read the `## ` headings **present in this file**, never a remembered set — they differ between companions,
and a section you expect and do not find is normal. Under each heading, the `### ` entries are the items.

An item is **yours to walk** when it carries at least one slot from Step 2's labels *and* that slot is
still at its placeholder — an angle-bracketed stub like `<the owner fills this in>`. Anything else is not:

- **A filled slot is an answer already given.** Leave it exactly as it is. Count them and say how many
  you skipped, so the owner can see the run picked up where the last one stopped.
- **An item with no owner slot is addressed to someone else.** Some sections carry items for the
  *producing* skill to resolve on its next pass, with a slot that skill fills. Never write in one. List
  them at the end as "not yours to answer", with whose they are as the file states it, so the owner knows
  they were seen and left.

If nothing is left to walk, say so — the file is answered and only Step 5 remains.

### Step 4 — Walk them, one at a time

**One item per turn, and then wait.** The whole point of the skill is that a person can answer a question
without reading a document first; a batch of six defeats that as thoroughly as handing them the file.

For each item, in this shape:

- **Put the question in plain language.** Not the item's heading pasted back — what is actually being
  asked, in the owner's terms.
- **Give the context the item itself carries**, briefly: why it matters, what was searched, what the run
  drafted and on what grounds, what moves if it is overridden. That is the item's own supporting text,
  compressed, not new argument.
- **Offer your opinion where you have one**, marked as yours and with the grounds — the file line, the
  precedent, the consequence you can see. Where you have none, say that instead. An opinion invented to
  seem useful is worse than an honest "I have no basis to lean here": the owner answers on your reasoning,
  and reasoning you do not have will not survive their reading it back.
- **Say which section the item is in and what the answer will read as** — a confirm-or-override slot takes
  `confirm` or `override: <what instead>`; an open-issue slot takes the answer itself. The slot's own
  placeholder states its form; follow that, not this list.

Then write what the owner said into that item's slot, in their meaning and as close to their words as the
slot's form allows. Write it as you go, item by item — not in one pass at the end, where a stopped session
loses everything answered.

**Nothing else in the file changes.** Not the header, not the numbering, not the item's other fields, not
a section's presence. If an item's supporting text is wrong, say so out loud — it is the producing skill's
to correct, not yours to edit under an answer.

**If the item carries other placeholder fields plainly addressed to the owner**, raise them in the same
turn and record what the owner says. Never fill one they did not speak to.

#### When the item belongs to a different document

Some items name that document themselves; others turn out that way in the owner's answer. Either way the
change does not go into the document being walked, and the document that owes it is usually settled —
nothing beside it, so its own producing skill re-runs and finds nothing to act on.

- **Name it, and ask.** In the same turn, say which document owes the change and what would have to move
  there. Nothing is opened without the owner's word. **If they say no**, write what they said into the
  item's slot and carry on with the walk — the routing was the question, and they answered it.
- **A live companion already holds that document** — a `*_open_issues.md` beside it whose `Companion to`
  pointer names it among the names it lists, never one found by its filename, since a companion shared by
  two documents carries neither's name → append one item to the bucket that fits. Nothing else in that
  file moves: not its header, not its numbering, not its other items.
- **There is none** → write one from that document's own companion template, resolved the way Step 1
  resolves a live companion. Every template states in its own header which document — or documents — it
  is a companion to, so read the pointers whole and keep the one that names this document among the
  names it lists:

  ```bash
  grep -m1 -oE 'Companion to `[^`]+`( and `[^`]+`)*' <CORE>/templates/*/*_open_issues_template.md
  ```

  Measured 2026-09-11: twelve templates on disk, every one of them carries the pointer, and one names two
  documents — `architecture_open_issues_template.md`, *Companion to `adr/` and `nfdr.md`*. This is the
  same self-describing test as Step 1's, for the same reason — a list of documents here would be the
  defect.

  **A pointer naming more than one document is one companion for all of them, named after the
  template's stem** — `architecture_open_issues_template.md` → `architecture_open_issues.md`, the one
  file `product-architecture` reads (`<CORE>/../skills/principal-architect/.claude/skills/product-architecture/SKILL.md:79`).

  Fill the title's subject and one item in the bucket that fits, and **leave the owner's slots at their
  placeholders** — the owner is answering the walked document today, not this one.
- **Say in the file that no producing run wrote it.** A blockquote under the header, naming the companion
  and the item the change came from, and why the file exists at all. The measured shape is
  `<Product path>/docs/trail/design/cycle-4.md:27-31`. Without it, the producing skill's next run meets a
  companion it has no record of writing.
- **Never write an empty companion.** `<CORE>/../skills/cto/.claude/skills/product-srs/SKILL.md` guards against one because
  *"an empty companion would read as OPEN and invert the done signal"* (`:200-202`). Here that inversion
  is the point — a settled document has to read open again — which is exactly why the file has to carry a
  real item and not a shell.
- **No template names that document** → say so, name the document and the item, and write nothing. The
  header is a contract Step 1 reads back, so one written freehand is a companion no later run can walk.

**Then commit it, check it landed, and only then answer the item you were walking** (owner, 2026-08-29).
The order is load-bearing. The answer that goes into the walked item's slot says the change is carried
elsewhere, and the producing skill folds that answer and drops the item — so if the other companion is
not on disk and committed by then, the fold drops the change on the floor. In order:

1. Commit that companion — the one you opened, or the one you appended an item to — in its own repo and
   its own commit, by Step 5's recipe.
2. `git show --stat` that commit and confirm the file is in it.
3. Only then write the walked item's slot, naming by path the file that now carries the change.

**The owner may stop at any point.** A partly answered file is a normal outcome, not a failure — go to
Step 5 with what you have. What is not answered stays at its placeholder for the next run.

### Step 5 — Commit, then name the re-run

**Commit first, always, and never leave the file dirty.** The producing run that closes a round removes
this file, and git refuses to remove a file carrying uncommitted edits — so an uncommitted answer stops
that run before it can commit anything and strands the round's work. Every companion's own header says
this; it is the one hazard the loop actually has.

The repo is the one the companion lives in, which is not always this one:

```bash
companion_repo=$(git -C "$(dirname "$companion")" rev-parse --show-toplevel)
companion_rel="${companion#"$companion_repo"/}"
```

**Stage `$companion_rel`, never a path you retyped.** `$companion` is already bound from Step 1, and
retyping it by hand is where the case of a filename, or a directory that is not there, gets changed
without anyone noticing — the builder then stages nothing and the round is stranded uncommitted, which
is the one hazard this step exists to prevent.

Then the shared recipe, `<CORE>/doctrine/governance/commit_via_builder.md` — it owns the flag forms and the
staged-set guard, and this file restates neither:

```bash
python3 "<CORE>/tools/commit_builder.py" --repo "$companion_repo" commit \
  --add "$companion_rel" \
  --subject "answer <document> open issues — <n> of <m> items" \
  --body "<which items were answered, and anything the owner said that the slot could not hold>" \
  --role "<your posture Role>" \
  --skill companion-answer \
  --directional "<directional>" \
  --surface "Claude Code" --co-authored-by "<your model> <noreply@anthropic.com>"
```

- **One `--add`, carrying `$companion_rel` and nothing else.** A companion opened on another document
  was already committed in Step 4, in its own commit and often in its own repo — this commit carries the
  walked companion alone.
- **The directional follows the companion's scope**, per
  `<CORE>/doctrine/governance/commit_format.md:54-55`: a companion under `system/` that belongs to no one
  project is instance-level and takes `Michi:`; one belonging to a project takes `Shukuba:` when that
  project has an open station and `Agari:` when it does not.
- Check `git show --stat` after committing: exactly one file, the companion.

**Then name every launcher that must run, and stop.** That is one launcher on most runs, and two when
Step 4 opened a companion on another document — that document's producing skill has a round to run now
as well, and its launcher is derived the same way. Derive each — never assume a path, and never write one
you have not seen:

1. The producing skill's own `launcher.md`, in its skill directory — `<CORE>/../.claude/skills/<producing skill>/`
   or `skills/<group>/.claude/skills/<producing skill>/`. If it exists, the launcher is
   `<CORE>/launchers/skill/launcher.sh <producing skill>`, taking the arguments that file's
   `**Arguments:**` line declares.
2. Otherwise `<CORE>/launchers/<producing skill>/launcher.sh` — if that folder exists, that is it.
3. Otherwise `grep -rl "invoke the <producing skill> skill" <CORE>/launchers/*/launcher.sh` — launcher
   folders do not all carry their skill's bare name, and this matches the fixed prompt literal each one
   sends, so it resolves to exactly one. Grepping for the skill's name alone does not: several launchers
   mention a skill they were adapted from.
4. **None of them** — say so plainly: name the skill, and the posture its own file says it requires, so
   the owner can run it from a session in that posture. Do not invent a launcher path; a path that does
   not exist costs more than an honest absence.

The argument follows the companion's altitude, which its path already states — an instance-level
companion's launcher takes the instance, a project-level one's takes the project. Read the shape where it
is declared — the `launcher.md`'s `**Arguments:**` line, or a launcher's own `# USAGE` block — and quote
it rather than composing a command line from this description.

Then stop. Running it is the owner's move.

---

## Outputs

| File / effect | Produced when |
|---|---|
| The companion, answered in place, one commit | The owner answered at least one item (Steps 4–5) |
| A companion opened on another document, carrying one item and its provenance, in its own commit | An item belonged to that document and the owner said to open it (Step 4) |
| The launcher command (or the skill + posture), named to the owner | Every run that committed — one per document a round is now owed on |
| A list of items left for another actor, and of items already answered | Step 3 found either |
| No change; the homes searched, the candidate count, and how many were rejected as copies | No live companion found (Step 1) |
| No change; the candidates listed, and a question | Several companions found (Step 1) |
| The commit as usual, and in place of a launcher a question about who moves next | The header names no skill to re-run (Step 2) |
| The commit as usual, and in place of a launcher the skill's name and the posture it needs | No launcher exists for the producing skill (Step 5) |

No document is ever written. The companion being walked is never created, and no companion is ever
deleted. No producing skill is run and no agent is spawned, on any path.

---

## Critical Rules

- **Discover, never list.** Every fact about which document, which skill, which sections and which slots
  comes from the companion in front of you. A list of producing skills in this file is the defect, not the
  shortcut.
- **Answer a live companion, never a copy.** Companion-shaped files sit in archives, fixtures, evidence
  trees and extracted layers, and they read identically. The header's pointer is the test, and an answer
  written into a copy is silently lost — nothing will ever fold it in.
- **Slots only.** The companion is the only file this skill writes, and inside it only an owner slot at
  its placeholder. Never the document, never the header, never another actor's slot, never a filled one.
- **Never create the companion you are walking, and never delete any companion.** A companion's presence
  is its document's open state and its absence is the done signal. On the document being walked, both of
  those transitions are the producing skill's.
- **A companion on another document is opened on the owner's word, and never empty.** Write it from that
  document's own template, resolved by the header pointer rather than from a list, and say in it that no
  producing run wrote it.
- **It is committed and checked before the walked item is answered.** That answer says the change is
  carried elsewhere, and the producing skill folds it and drops the item — so a file that is not on disk
  and committed by then loses the change.
- **One item per turn.** Ask, wait, write, next. A batched question is the thing the owner already had.
- **An opinion carries its grounds, or it is not offered.** "I have no basis to lean here" is a complete
  answer and a useful one.
- **Commit before naming the re-run, always.** An uncommitted answer stops the run that would have folded
  it in, and the round's work is lost.
- **Name a launcher you have seen.** The skill's `launcher.md`, then its folder, then the prompt-literal
  grep, then an honest "there is none — here is the skill and the posture it needs."
- **It stops at naming.** No spawn, no posture check, no fold, no "shall I run it for you and see."
