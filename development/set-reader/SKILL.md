---
name: set-reader
description: "Reads a complete drawing set rather than a drawing: works out what phase it actually is regardless of what the title block claims, what is in it and what is missing for that phase, which disciplines are present and at what revision, how the set is organised, and what somebody receiving it would have to ask about first. Built for the set that arrives from somewhere else — a previous architect, a client, a design-build partner, a project you are taking over. Trigger on \"read this set\", \"what have we been given\", \"we are taking over this project\", \"is this set complete\", \"set-reader\", or a whole set handed over. Carries no standards and no phase definitions; completeness is judged against what the set itself claims to be. `drawing-reader` reads one sheet, `plan-review` reads a plan, `drawing-standards-audit` sweeps for conventions. It does not replace the Architect of Record."
license: MIT
metadata:
  title: "Set Reader"
  summary: "Read a whole drawing set and say what kind of set it is"
  discipline: "construction-admin"
  tags: "Review"
---

# Set Reader

A set arrives: from a previous architect, a client's archive, a design-build
partner, a project being taken over. The title block says what phase it is and
the drawings say something else. The first hour is spent finding out what you
actually have, and it is usually spent badly, sheet by sheet.

## Scope and limits — read first

**What this does.** Reads the set as a set. Establishes what phase it really is,
what is present and missing, what has been revised and what has not kept up,
how it is organised, and the questions somebody receiving it should ask first.

**What this does not do.**

- **It carries no standards and no phase definitions.** Completeness is judged
  against what this set claims to be, and against what the phase would normally
  carry, stated as an expectation rather than as a rule.
- It does not read one drawing. `drawing-reader` does, and `plan-review` reads a
  plan.
- It does not sweep for conventions and broken references.
  `drawing-standards-audit` does, and it runs after this.
- It does not check code or coordination. `code-compliance-review`,
  `consultant-drawing-review` and `coordination-log` do.
- It does not replace the Architect of Record.

**What you need before starting.** The set, ideally as one PDF or one directory.
The sheet index. Whose set it is, from when, and why you have it.

## Workflow

### Step 1. Establish what you have been given and why

Ask, in one message:

> 1. Whose set, from when, issued for what according to the title block?
> 2. Why do you have it: taking over a project, bidding, reviewing somebody
>    else's work, buying a building, your own set at a milestone?
> 3. Is it complete as issued, or an extract?
> 4. Are the consultants' sheets included?
> 5. Is there a specification with it?
> 6. Is there anything that supersedes it that you do not have?

**Question 2 decides what to look for.** A set you are taking over is read for
what you are inheriting. A set you are bidding is read for what is not there. A
set at your own milestone is read against what you intended.

### Step 2. Say what phase it actually is

Regardless of the title block. Judge from the content:

| Signal | What it suggests |
|---|---|

- Are there details, and at what scale?
- Are there schedules, and are they filled in?
- Are dimensions on the plans, and do they close?
- Are wall types drawn and legended?
- Are the consultants' sheets present and at a comparable level?
- Are there general notes, and do they say anything?
- Is there a code analysis, and does it show its arithmetic?

Say plainly when the content and the title block disagree, and which way. **A
set labelled construction documents that carries schematic content is the single
most useful finding this produces**, and it changes a fee conversation.

### Step 3. Inventory what is present and what is not

- The sheet index against the sheets. Both directions.
- Which disciplines are present, at what revision, and what date.
- **Which disciplines are at a different revision from the architectural.** A
  consultant's set two revisions behind is a set that disagrees with everything.
- Numbering gaps, and whether they are deliberate.
- Whether every sheet has a title block that is filled in.
- What a set of this phase would normally carry and does not.

### Step 4. Read the revision history as a story

The revisions tell you what happened to the project:

- What has been revised most? That is where the trouble was.
- What has never been revised? Either it was right, or nobody looked.
- Do the revision dates cluster around something: a submission, a value
  engineering round, a change of consultant?
- Is anything clouded with no revision entry, or entered with no cloud?

### Step 5. Say what a receiver would ask first

The output somebody can act on today. Ordered by what blocks work:

- What is missing that stops you from doing anything.
- What is present but at a phase you cannot rely on.
- What has to be verified rather than trusted: dimensions, existing conditions,
  consultant coordination.
- What has to be obtained: the specification, the consultants' sets, the current
  revision, the code analysis, the survey.
- Who has to be asked, and for what.

Where the set is being taken over, add plainly: **what of this you are now
responsible for, and what should be re-verified rather than adopted.**

### Step 6. Report

- What phase it actually is, against what it says.
- The inventory, with revision mismatches between disciplines named.
- What the revision history suggests happened.
- The first questions, ordered.
- What could not be read, and why.

Then name the next skills: `drawing-standards-audit` for the conventions,
`consultant-drawing-review` for the coordination, `code-compliance-review` for the code.

### Step 7. Save

Ask where. A set reading is worth keeping, especially on a project being taken
over, because it is the record of what was inherited.

## Rules

- **Ask why you have the set** before reading it.
- Judge the phase from the content, not from the title block, and report the
  disagreement.
- Check the index against the sheets in both directions.
- Report revision mismatches between disciplines.
- Read the revision history for what it says about the project.
- On a takeover, say what should be re-verified rather than adopted.

## Anti-patterns

- Reading sheet by sheet from the front.
- Believing the title block.
- Missing that a consultant's set is two revisions behind.
- Judging a set against a construction set when it is not one.
- Reporting completeness without saying what phase it was judged against.
- Adopting inherited dimensions and existing conditions as verified.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
