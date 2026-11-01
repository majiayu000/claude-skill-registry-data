---
name: document-diff
description: "Compares two versions of a written document — an agreement, a specification section, a programme, a code analysis, an owner's requirements — and reports every change, not the ones the covering note listed. Separates a wording change from a change in obligation, flags every deletion because deletions are what a redline is worst at showing, and reports what moved rather than changed, since relocated text reads as unchanged in most comparisons. Trigger on \"what changed between these two versions\", \"compare these contracts\", \"diff this spec section\", \"they sent a revised agreement\", \"document-diff\", or two versions of anything written handed over together. Carries no view on what any clause should say; `contract-review` and `spec-review` read one version on its merits. It is not legal advice and does not replace the attorney or the Architect of Record. For drawings use `drawing-diff`."
license: MIT
metadata:
  title: "Document Diff"
  summary: "Compare two versions of a document and find what nobody mentioned"
  discipline: "construction-admin"
  tags: "Review"
---

# Document Diff

"We made a few small changes" is the sentence this exists for. A revised
agreement arrives with a covering note listing three edits, and the useful
question is what the note did not list. Deletions in particular are almost
invisible: a clause that is simply gone leaves no mark to notice.

## Scope and limits — read first

**What this does.** Takes two versions of one written document and reports every
difference, sorted by whether it changes an obligation rather than by where it
sits in the text. Treats deletions and relocations as first-class findings.

**What this does not do.**

- **It does not judge the clauses.** Whether a provision is acceptable is
  `contract-review`'s work on the current version, or `spec-review`'s on a
  spec book. This says what moved between two versions.
- **It is not legal advice.** Where a change alters a legal obligation, the
  finding is that it changed and the attorney reads it.
- It does not compare drawings. `drawing-diff` does.
- It does not merge, accept, or reject anything.
- It cannot see what it was not given. A document incorporating something by
  reference has changed if that reference changed, and this will say so as a
  question rather than checking it.
- It does not replace the attorney or the Architect of Record.

**What you need before starting.** Both versions, complete, with their dates or
version marks. Any covering note or redline the sender provided. What kind of
document it is. Whether either version was already executed or issued.

## Workflow

### Step 1. Establish what the two versions are

Ask, in one message:

> 1. What are the two documents, and how are they identified: dates, version
>    numbers, "as issued" and "as returned"?
> 2. Which is the earlier one? Say which explicitly; a comparison run backwards
>    reports every addition as a deletion.
> 3. Did a covering note or a redline come with it? What does it claim changed?
> 4. Was either version executed, issued, or relied on?
> 5. Does the document incorporate anything by reference?

**Take the covering note as a claim, never as the scope of the comparison.** It
is the most useful single input and it is also the thing being checked.

### Step 2. Compare, and classify every difference

Do not report in document order. Classify first:

| # | Where | Old | New | Kind | Changes an obligation? |
|---|---|---|---|---|---|

`Kind` is one of:

- **Added.** New text.
- **Deleted.** Text gone. Report these first, always.
- **Changed.** Text replaced.
- **Moved.** The same text, in a different place. Most comparison tools show
  this as a deletion plus an addition, or as nothing at all, and moving a clause
  can change what it governs.
- **Renumbered.** A reference elsewhere may now point at the wrong thing.
- **Formatting.** No change in meaning. Grouped and counted, never listed.

### Step 3. Separate wording from obligation

For every difference that is not formatting, ask one question: **does anyone
have to do something different?**

Report as two lists:

- **Changes an obligation.** Scope, standard of care, indemnity, limits,
  payment, timing, notice, ownership, who does what, what is included, what is
  excluded, what a rating or performance has to achieve.
- **Wording only.** Clearer, tidier, or house style.

A change of "shall" to "will", or "may" to "shall", belongs in the first list
however small it looks. So does a deleted "not".

### Step 4. Check the note against the findings

Two comparisons, and both matter:

- Every change the covering note claimed, found or not found in the document.
- **Every change found that the note did not mention.** This is the output the
  whole exercise exists for. Count it and lead with it.

Where the note describes a change in different terms from what the text
actually does, report both descriptions.

### Step 5. Chase the consequences

Changes have effects the diff does not show:

- Renumbering: does anything else in the document, or in another document,
  reference the old number?
- Definitions: did a defined term change meaning? Every use of it changed too.
- Deleted clauses: did anything rely on the deleted clause?
- Incorporated documents: has the reference changed, and has the referenced
  document itself changed? Flag as a question.
- Exhibits and attachments: were they compared, or only the body? Say which.

### Step 6. Report

- Count of unmentioned changes, first.
- Deletions, listed individually.
- Changes to obligations, listed individually with old and new text.
- Moved and renumbered text with what may now be wrong.
- Wording-only and formatting, counted rather than listed.
- What was not compared: exhibits, incorporated documents, attachments.
- What to take to the attorney.

Close by saying no clause was judged on its merits and naming the skill that
would.

### Step 7. Save, if asked

Ask whether to write the comparison to a file and where.

## Rules

- **Establish which version is earlier**, explicitly, before comparing.
- **Report deletions first.** They are the hardest to see and the most
  consequential.
- Treat the covering note as a claim to be checked, never as the scope.
- Lead the report with the count of changes the note did not mention.
- Report moved text as moved, never as a deletion plus an addition.
- Never judge a clause. Say what changed and point at the skill that reads it.
- Say plainly what was not compared.

## Anti-patterns

- Reporting in document order, so a deleted indemnity sits between two
  formatting fixes.
- Trusting the redline the sender supplied.
- Grouping a deletion with formatting because the text was short.
- Missing a changed defined term, which quietly changes every clause using it.
- Comparing the body and not the exhibits, without saying so.
- Reading "shall" to "will" as wording.
- Giving an opinion on whether the new version is acceptable.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
