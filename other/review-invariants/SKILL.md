---
name: review-invariants
description: 'Walk the maintainer through every DEFERRED INVARIANT block in specs/IMPLEMENTED.md one at a time — showing the rules already shipping, the drafted wording, and every site a citation must reach — then ask for a verdict (register / hold / amend) and carry out the mechanical registration for the ones approved. Never signs off an invariant itself. Maintainer tool for developing the Senzing Bootcamp Claude Plugin (SBCP). The blocks it resolves are written by any maintainer command or run that ships or finds an invariant change, since none of them may edit specs/INVARIANTS.md itself (INV-365).'
argument-hint: "[block number to start from] (omit to start at the top of the pending queue)"
---

# Review Invariants

This is a **maintainer** tool for developing the Senzing Bootcamp Claude Plugin
(SBCP). It is never invoked during a bootcamp.

A deferred invariant is a **rule that is already shipping** in the plugin, guarded by a
test, and recorded in no invariant. `/implement-github-issue` *(user level)* and `unattended-issue-loop` produce
them by design: minting an invariant is the maintainer's alone, so an implementation that
ships a hard rule writes a `DEFERRED INVARIANT` block instead of registering one. This
skill is where those blocks get decided.

## Why this exists

Deciding one takes about a minute. Registering one correctly takes six steps across four
files, and every one of them has a way to go quietly wrong. On **2026-09-01** two
invariants were registered by hand and the mechanical half produced four separate defects:

- A count of pending blocks taken by **grepping for the phrase** returned 29 against a
  true 11 — ledger prose *about* deferrals matched too.
- A block the maintainer had **already held, twice**, with a recorded revisit condition,
  was presented as awaiting a first decision.
- A rule was cited at the **two sites the deferral listed** when it shipped in **three**;
  the third was named inside another bullet's prose and reached only by scanning.
- The guard checking that deferral quotes match their source **skipped 3 of 17 bullets**
  it could not parse, and reported a clean run over the rest.

None of those is a hard problem. All four are the same problem: the work is repetitive,
the failures are silent, and reading is what is being relied on. So the queue, the sites
and the quote check are computed by `pending_invariants.py`, and this file is the
procedure around them.

⛔ **This skill never signs off an invariant.** It presents, it asks, it waits, and it
executes what the maintainer decided. A verdict the maintainer did not give is not a
default this skill gets to choose — that is the whole reason the deferral exists.

## Two kinds of block, and they decide different things

The queue holds **two** shapes, and `list` says which each one is.

| | **DEFERRED INVARIANT** | **PROPOSED AMENDMENT** |
|---|---|---|
| Subject | a rule shipping with **no id** | a change to an invariant **already in force** |
| The decision | mint an id, or hold | append a dated correction, or hold |
| Cost of yes | an id, permanent | a note beneath the original, permanent |
| `list` shows | `new invariant` | `AMENDS INV-nnn — already registered` |

⛔ **An amendment is not a smaller registration; it is a different act.** Registering adds a rule
that binds future work. Amending changes a rule that is **already binding** — every citation to
it, every guard enforcing it, and every future reader is affected the moment the note lands.

⚠️ **`INVARIANTS.md` is append-only and stays that way.** An amendment **appends a dated
correction beneath the original**; it never rewrites, renumbers or deletes. The old text remains
readable, which is how a child port holding an earlier copy can tell what changed.

### Why amendments are queued at all (#79)

**11 of 311 invariants carry a dated correction**, 13 markers in all — the act is routine. Until
#79 **not one of them was ever queued**: the proposed wording reached the maintainer through a
pull-request body and the conversation, while `list` reported `pending: 0` throughout. That was
true to its own definition and misleading as a worklist.

⛔ **The precedent that decided the shape.** INV-207's correction claimed its pinned site had
**moved** to another file, and the content it pins was never written there. A **test** caught it
days later; review did not, because nothing scanned the claim. So an amendment carries the same
three things a deferral does — the proposed text, the sites it affects, and why — and `sites`
scans it like any other block.

### Writing one

```markdown
- **PROPOSED AMENDMENT to INV-nnn — awaiting the maintainer's sign-off; NOT applied.**
    - ⛔ **<the rule as it ships today, quoted verbatim>** — in `<path>`

  <why the wording needs to change, and what breaks if it does not>

  **INV-nnn** — <the exact text of the dated correction to append>
```

⚠️ **Write the real id, not `INV-NNN`.** The invariant exists; writing NNN would be false rather
than deliberate, and `check` resolves the quote against the file the bullet names either way.

⛔ **(INV-409) Applying one resolves it** — rewrite the end of its bold header so it leaves the queue,
exactly as `(resolved INV-nnn, …)` does for a deferral. The helper reads `— applied <date>`
inside the bold header and nowhere else:

```markdown
- **PROPOSED AMENDMENT to INV-nnn — applied YYYY-MM-DD by the maintainer.**
```

Re-offering a decision already made asks the maintainer to re-derive it.

## The three verdicts

Present all three every time. **Two of them are not "no".**

| Verdict | What it means | What happens |
|---|---|---|
| **Register** | The wording is right. | Mint the next free ID, cite it everywhere the rule ships, resolve the block. Permanent. |
| **Hold** | Not yet — and here is what would change that. | The block stays, with the maintainer's **reason and revisit condition** recorded. Not a rejection. |
| **Amend** | The rule is right, the wording is not. | Change the wording first, then register the changed text. |

**Amend includes splitting.** On 2026-08-27 a maintainer review split one draft into two
because it had grown a second subject — what an archive *is*, and what the Bootcamper
*consents to* — and bolting a second subject onto a statement is how the first omission
happened. Two subjects is two invariants.

## ⛔ What approving and disapproving actually differ by

State this in the maintainer's own terms at the first invariant of a session, because the
intuition is wrong in a way that matters:

> **Declining does not remove the rule.** It is already in the plugin, already shipped to
> Bootcampers, and already enforced by a test. Nothing about the product changes either
> way today.

What changes is whether the ruleset **knows about it**:

- **Register** → the guarantee has an address. A later change that contradicts it fails a
  guard or is caught by a conformance sweep, `citations.py verify` can resolve it, and a
  future editor who finds the rule can look up why it exists. The cost: IDs are permanent
  (`INVARIANTS.md` is append-only — never renumbered, never deleted), so a wrong invariant
  gets a dated correction note rather than a removal. Registering a rule whose wording is
  still moving means amending a fresh invariant.
- **Hold** → the rule keeps shipping and the ruleset stays silent about it. Nothing binds
  future work to it, and nothing notices when a later change contradicts it. That is not
  hypothetical: **INV-134** shipped as a guarantee with no invariant and two files then
  cited **INV-076** — an invariant about something else entirely — as its authority.

So the question is never *"is this rule good?"* — it is already shipping either way. The
question is **"is this wording one I am willing to be held to permanently?"** If yes,
register. If the rule is right but the words are still moving, amend. If something has to
happen before the wording can settle, hold and say what.

⚠️ **A hold is worth as much as its revisit condition.** *"Wait"* with nothing attached
comes back to the same question next month with nothing new to weigh. *"Revisit after
`dry-run` phases 2 and 3 have exercised the flow"* is a condition someone can check.

## Step 1: Load the queue

```bash
python3 .claude/skills/review-invariants/pending_invariants.py list
```

It prints the pending blocks numbered, the count, the next free ID, and — separately —
any block that is **held**, with the recorded reason.

⚠️ **(INV-409) A block is pending unless its own header records a decision** — in one of the six
forms `DECIDED_IN_HEADER` in `pending_invariants.py` matches: `(resolved INV-nnn`, `resolved as an
amendment`, `resolved by amendment`, `(resolved YYYY-MM-DD`, `— applied YYYY-MM-DD` or
`— superseded by` in the bold header — or it carries a hold (#770). A decision word in any other
form decides nothing: "not yet resolved" and "would be superseded" stay pending (#778). The
header's other wording does not matter: until #770 the queue admitted only blocks carrying the exact
"awaiting the maintainer's sign-off" marker, and seven blocks worded "a new id is owed" were
missing from a list that read `pending: 0`. So when you resolve or apply a block, put the
decision **in its header**, as Step 3 shows; a decision recorded only below it leaves the
block in the queue.

⛔ **Never present a held block as awaiting a decision.** It has one. Re-offering it asks
the maintainer to re-derive a decision they already made and recorded. The helper reads the
hold, and its reason, from the ledger only: the block's `**HELD <date>:**` paragraph ("Hold",
below). Mention held blocks
once, as context, and move on. Bring one back only when its revisit condition is **met** —
and say which condition, and what met it.

Then confirm the ledger is honest before quoting it:

```bash
python3 .claude/skills/review-invariants/pending_invariants.py check
```

Every rule quote must appear verbatim in the file it names. A mismatch means the block
quotes something the plugin does not say — truncated, paraphrased, or since reworded — and
**that is not a wording to approve from**. Fix the quote against its source first.

⛔ **(INV-308) Read all four counts, not the mismatch count alone.** `check` reports
`<n> checked, <n> mismatched, <n> unresolved, <n> no-prose-site`:

- **unresolved** — a bullet names a path that does not exist. ⛔ Its quote is **unverified**,
  and this is not a clean check. Fix the path before quoting the block.
- **no-prose-site** — the bullet names no path because the rule is encoded in code or tests
  rather than stated in prose. Legitimate; nothing is owed.
- **checked = 0** — nothing was verified. ⚠️ An **empty** check, not a clean one.

⚠️ Until #59 this printed only the first two counts and skipped the rest without counting
them, so a run that verified nothing read exactly like a run that verified everything — and
was presented to the maintainer as clean in three consecutive reviews.

## Step 2: Present one invariant

One at a time. Do not batch — the maintainer is deciding, not skimming. With no
argument, start at the first pending block; an argument naming a number starts there, as
the `<n>` that `show` and `sites` take.

```bash
python3 .claude/skills/review-invariants/pending_invariants.py show <n>
python3 .claude/skills/review-invariants/pending_invariants.py sites <n>
```

Present, in this order:

1. **What it is** — the spec it came from, in one line.
2. **The rules already shipping**, verbatim, with their locations. This is the concrete
   thing; the drafted wording is the abstraction over it.
3. **The drafted wording** in full. Never summarize it — it is the text being approved.
4. **Where a citation would land** — `sites` prints three groups. The **named** ones are
   definite; the **prose-named** ones are sites whose bullet nobody wrote and are where
   the misses have been; the **candidates** are leads to read, never sites to cite blind.
   ⛔ **(INV-308) Read the scope line under them.** The candidate scan reads the plugin and
   the host-side inputs (`hosts/`, `tools/bootcamp_build/`), while a **named** path resolves
   anywhere under the repository — so an empty candidate list is evidence about those roots
   and nothing else. `sites` prints what it scanned and what it did not on every run (#77);
   the numbers are the point.
5. **Anything the block already rejected.** Several blocks record a near-miss citation
   that was considered and turned down — INV-097 for the multi-select rule, INV-080 and
   INV-149 for the provenance rule. That reasoning is the expensive part and it is already
   written; surface it rather than making the maintainer re-derive it.
6. **What is different if this is held** — in this rule's own terms, not the general form.

Then ask, as **one** question, and stop. Register / hold / amend.

## Step 3: Carry out the verdict

### Register

⛔ **Read the ID again, now.** Do not carry a number from Step 1 or from the block text —
several deferrals are pending and **only the first one minted gets the ID any of them
would have named**. Every block writes `INV-NNN` deliberately for this reason.

```bash
python3 .claude/skills/review-invariants/pending_invariants.py next-id
```

Then, per `INVARIANTS.md`'s own maintenance rules:

1. **Index entry and invariant in ONE edit** (rule 3 — `tests/test_invariants_index.py`
   fails otherwise). Add the ID to the matching group under *Index by subject*, and append
   the invariant where the last few landed. Keep the provenance: `(Source: <spec-name>,
   YYYY-MM-DD.)`
2. **Keep the rejected-citation note in the invariant text.** It is the reason this is a
   separate rule rather than a citation to an existing one, and it is what stops the
   question being re-litigated.
3. **Cite the new ID at every site the rule ships** — `(INV-NNN)` first inside the rule's
   own bold, so it is on the rule's line. ⛔ **Derive the site set from `sites` and from
   scanning, never from the deferral's bullet list** (INV-246): the list is where the
   author noticed the rule, which is exactly what is unreliable. ⚠️ **And `sites` is not the
   whole derivation**, because its candidate scan reads the plugin and the host-side inputs
   only: for a rule shipping under `.claude/` or `tests/` — which INV-307, INV-308 and INV-309
   all do — the scan opens none of it and says so. Grep the rule's own distinctive words
   across the repository before concluding the set is complete.
4. **Back-cite from the enforcer.** If the invariant says *"Enforced by `tests/x.py`"*,
   that test must name the invariant back (`tests/test_invariant_enforcer_citations.py`).
   Say in the back-citation what the test does **not** establish — usually that a live turn
   obeys the rule, which only `dry-run` phase 3 can observe — so an `Enforced by` clause
   cannot be read as a compliance claim.
5. **Re-derive `EXPECTED_PAIRS`** in that guard by running its extractor. ⛔ Never
   increment it to make the assertion pass.
6. **Resolve the block** in `IMPLEMENTED.md`: `**DEFERRED INVARIANT (resolved INV-NNN,
   registered by the maintainer YYYY-MM-DD).**`, keeping the rules and wording in place —
   the block becomes the record of what was approved.

Verify:

```bash
python3 .claude/skills/compact-dev-environment/citations.py verify        # resolves, count +1
python3 .claude/skills/dry-run/coverage_reports.py shipped | grep INV-NNN # must be empty
python3 -m unittest discover -s tests
```

`shipped` listing the new ID means the plugin does not cite it — step 3 was incomplete.

### ⛔ Then stop at the working tree

⛔ **(INV-310) This skill does not commit and does not push.** It performs the registration and
stops with the changes in the working tree, the way `/propagate-to-public` does. Report every
file it touched and what changed in each:

```text
Registered INV-NNN across 4 file(s):
  specs/INVARIANTS.md        index entry + invariant
  specs/IMPLEMENTED.md       block resolved
  plugins/.../SKILL.md:41    citation added at the rule
  tests/test_x.py:12         back-citation

⛔ Nothing is committed. Review the diff, then commit it yourself.
```

⚠️ **Why the strictest stop rather than a pre-push pause.** Registering is the most permanent
act in this repository — `INVARIANTS.md` is append-only, so a wrong id is corrected by a dated
note beneath it and never removed, and every future change is bound by the wording. Everything
else here that is permanent or outward-facing is gated: `/implement-github-issue` *(user level)* waits twice,
`/release` never pushes, `/propagate-to-public` never commits. ⚠️ Those two are governed by
INV-301, which binds **releasing** specifically and does not reach this skill — the general rule
is drafted as a deferral in `IMPLEMENTED.md` rather than borrowed from an invariant about
something else. ⛔ **This skill was the one permanent act with no gate at all**, and the maintainer approving a *wording* is not the same as
approving a *commit* — which is what made the gap easy to miss, since they are standing right
there (#78).

⚠️ **One invariant per commit is now the maintainer's to keep.** A batch commit makes a later
revert take rules with it that nobody questioned, and the skill can no longer enforce that by
committing each one itself. Say so when handing the diff over, per registration.

⚠️ **A branch was considered and is not required.** The `git-conventions` hook names branches
`<issue-number>-<github-username>-<n>`, and a review session has no single issue — the
2026-09-14 session registered seven ids drawn from different sources. Rather than instruct a
bypass of the maintainer's own convention, this skill leaves the tree where they can commit it
wherever they judge right. Whether that convention needs a non-issue form is a separate
question and is not answered here.

### Hold

⛔ **(INV-308) Record the reason and the revisit condition inside the deferral block itself**, as
a `**HELD <date>:**` paragraph — that is where `hold_reason()` reads it, and a note only in the
conversation dies with it. Leave the block pending in every other respect. Nothing else changes.

```markdown
- **DEFERRED INVARIANT — awaiting the maintainer's sign-off; NOT minted.**
  …rules and drafted wording…

  **HELD 2026-09-21:** <the maintainer's reason, in their words>.
  Revisit after <a condition someone can check>.
```

⚠️ **Inside the block, not beside it.** The queue reads a block bullet-by-bullet, so a `HELD`
paragraph written as its own top-level bullet ends the block and is not seen — the run then
reports the block as **pending** and re-offers a decision the maintainer already made.

⚠️ **The spec file is no longer the place, and for issue-driven deferrals never could be.** Until
#58 this said *"in the spec file"*; a deferral that came from a GitHub issue has none, and
`specs/` is frozen under INV-307 so one cannot be created. The only reachable held state for such
a block was a generic string recording a property of the work rather than the maintainer's
decision. One block used the spec route and was migrated to the ledger on 2026-09-21; that spec
file still carries the same paragraph and is no longer read by anything.

### Amend

Change the wording in the block first, show the maintainer the changed text, and get a
second yes on **that**. Then register it. An amendment approved in passing is a wording
nobody read.

Then **resolve the prose, not only the block.** Applying one ends its bold header
`— applied YYYY-MM-DD by the maintainer.` ("Writing one", above), the way Register's step 6
resolves a deferral's block.
⛔ **(INV-386) The block is not the only place that called the amendment pending.** The guard enforcing
the amended rule says so in its own docstring, and that sentence survives the registration — so
its next reader concludes the rule the guard asserts is not yet binding, which is INV-308's
failure shape pointed inward. Rewrite each such sentence to state the note as registered, with
its date.

⛔ **Derive those sites by scanning, never from the block's own bullet list** (INV-246),
exactly as step 3 above derives a new id's citation sites: the pair that decides is the
invariant's id and the note's issue marker, and `specs/INVARIANTS.md` is what says whether the
registry already carries it. `tests/test_registered_amendments_are_not_called_pending.py`
scans `tests/` and `.claude/` for it and fails on a site left behind; it found **nine** where
#691's list of five had been written by hand.

⚠️ **Leave a legitimately pending amendment alone.** A block still queued, and a
`DEFERRED INVARIANT`, say "awaiting the maintainer's sign-off" correctly. What changed is the
registry, so the registry is what to read — never the words.

## Step 4: Next, and the session record

Move to the next pending block and repeat from Step 2. When the maintainer stops — whether
the queue is empty or not — write a dated `## invariant-review-YYYY-MM-DD` entry in
`specs/IMPLEMENTED.md`, marked **Not a spec**, recording what was registered, what was
held with its reason, what was amended, and what remains. That is the precedent set by
`invariant-review-2026-08-27`.

⛔ **A review record mints IDs and adds citations; it establishes no invariant of its
own.** Every invariant it registers was established by an earlier spec's implementation.

## Scope note

`.claude/` is not promoted to the public repo (`python3 -m tools.bootcamp_build promote`
writes only every assistant's package under `plugins/`, each assistant's catalog file,
`docs/` from `site/`, and each file under `public/` at the same path from the root), so this
skill never ships to bootcampers.
