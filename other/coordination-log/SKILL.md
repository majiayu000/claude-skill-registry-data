---
name: coordination-log
description: "Keeps one dated log of conflicts between disciplines and follows each to the only ending that counts: both sets showing the same thing. Records which two documents disagree, what each says, who resolves it, and then the step everyone skips — whether the agreed answer reached both drawings and at which revision. Consolidates what the review skills find rather than leaving each discipline's findings in its own report. Trigger on \"coordination log\", \"track the clashes\", \"did that conflict get fixed in both sets\", \"coordination issues\", \"coordination-log\", or the output of a discipline review handed over to keep. Carries no positions of its own; the conflicts come from `mep-review`, `structural-drawing-review`, `civil-drawing-review`, `penetration-review` and `design-ceiling`. It does not resolve anything and does not replace the Architect of Record."
license: MIT
metadata:
  title: "Coordination Log"
  summary: "Track a conflict until both sets show the same answer"
  discipline: "construction-admin"
  tags: "Tracking"
---

# Coordination Log

A conflict is found, discussed, and agreed. Then one discipline revises and the
other does not, and the set goes out still disagreeing with itself. The agreement
was never the deliverable; two drawings showing the same thing is.

## Scope and limits — read first

**What this does.** Consolidates conflicts from every discipline review into one
log, keeps both parties' values rather than one, and tracks each to closure —
which means verified in both sets at a stated revision.

**What this does not do.**

- **It holds no positions.** It does not decide which discipline is right. The
  conflicts come from the review skills and the resolutions from the people who
  own them.
- It does not find conflicts. `mep-review`, `structural-drawing-review`,
  `civil-drawing-review`, `penetration-review` and `design-ceiling` each read one
  relationship; this holds what they produce.
- It does not run clash detection or open a model.
- It does not replace `project-tracker`, which holds issues, decisions and risks
  generally. A coordination conflict has a shape that log does not carry: two
  documents, two values, and a closure that has to be checked twice.
- It does not track RFIs or changes. `rfi-tracker` and `change-order-tracker` do,
  and this records where a conflict became one.
- It does not replace the Architect of Record.

**What you need before starting.** The reviews that have been run and their
output. Which disciplines are on the project and who leads each. The issue and
revision dates of each set. The next issue date.

## Workflow

### Step 1. Establish the sets and the rhythm

Ask, in one message:

> 1. Which disciplines, who leads each, and how are they reached?
> 2. What is the current revision of each set, and its date?
> 3. Which reviews have been run, and do you have their output?
> 4. What is the next issue, and what has to be closed before it?
> 5. Is there a coordination meeting, and how often?
> 6. Is there a model, federated or otherwise, and does anyone run clash
>    detection on it?

**Record each set's revision.** A conflict logged against one revision and
checked against another is a conflict nobody closed.

### Step 2. Log each conflict with both values

| # | Conflict | Set A | A says | Set B | B says | Found by | Raised | Owner | Status |
|---|---|---|---|---|---|---|---|---|---|

**Both values, always.** A log recording only "duct clashes with beam" loses the
information needed to check the fix. Record the dimension, the level, the sheet
and the location on each side.

`Status` is one of: `open`, `with owner`, `resolved not drawn`, `drawn one set`,
`drawn both sets`, `closed`, `accepted as is`.

**`resolved not drawn` and `drawn one set` are the two that matter.** Everything
gets to `resolved` in a meeting; most of the failures live in the gap between
that and both sets being revised. Report their count first in every read-back.

`accepted as is` is a legitimate ending and it needs a name and a date against
it, because it will be questioned later.

### Step 3. Give each conflict one owner and one resolver

Two different roles and they get confused:

- **Owner.** Who chases it. One name.
- **Resolver.** Which discipline has to change something, and often it is both.

Where the resolver is "both", the conflict has two closures and neither is done
until the other is. Log them as one row with two closure checks rather than as
two rows, so it cannot be half-closed.

**A conflict with two owners has none.**

### Step 4. Close only against a revision, in both sets

Closure is a check, not a report:

| # | Resolution | Set A revision showing it | Set B revision showing it | Verified by | Date |
|---|---|---|---|---|---|

A row is `closed` only when both revision columns are filled and somebody's name
is in `verified by`. Nothing else counts. A resolution agreed in a meeting, an
email confirming it, or a consultant saying it is done are all `resolved not
drawn`.

Re-check at every issue. A conflict closed at one revision can reopen when a
later revision changes one set and not the other, and that reopening is invisible
unless somebody looks.

### Step 5. Read back

At every coordination meeting and before every issue:

- `resolved not drawn` and `drawn one set`, first, with how long each has been
  there.
- `open` by age, oldest first.
- Everything with no owner.
- Everything `accepted as is`, listed, so it is a decision that stays visible.
- Conflicts that have reopened.
- Which reviews have not been run since the last issue, because a set revised
  without being re-reviewed has conflicts nobody has found yet.

Report elapsed time. Never predict when something will close.

### Step 6. Write the log

One dated file per project, appended to rather than rewritten. Ask where it
lives on the first run and use the same path after. Every entry carries a date, a
source and the revision it applies to.

## Rules

- **Never take a position on which set is right.**
- Record both values on every conflict, with sheet and location on each side.
- Log the revision of each set at the time the conflict was raised.
- One owner per conflict, or flag that there is none.
- **`closed` requires both revision columns and a verifier's name.** Nothing
  else.
- Report `resolved not drawn` and `drawn one set` first in every read-back.
- Re-check closed conflicts at every issue.
- Append; never rewrite an earlier entry.

## Anti-patterns

- Logging the conflict without both values.
- Closing on the strength of a meeting or an email.
- Treating a consultant's word that it is fixed as verification.
- One row per discipline for a conflict that needs both to change.
- Losing the revision, so nobody can tell whether a fix landed before or after.
- Letting `accepted as is` disappear into the closed pile.
- Issuing a set without re-running the reviews on what changed.
- Keeping coordination conflicts in the general issues log, where the second
  closure check does not exist.

## Resources

None. This skill is one file. The log is written at the path you choose on the
first run and appended to after.
