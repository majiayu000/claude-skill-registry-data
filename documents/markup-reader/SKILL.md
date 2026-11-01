---
name: markup-reader
description: "Reads a marked-up drawing — a redline, a scanned sketch over a print, a PDF with comments, a photograph of a drawing somebody wrote on — and turns it into a numbered list of what each mark asks for, who it is for, and whether it can be acted on as drawn. Separates the marks that instruct from the marks that ask, and flags every mark whose meaning cannot be determined, because a guessed markup is worse than an unread one. Trigger on \"read this redline\", \"they marked up the drawing\", \"what does this markup say\", \"turn these comments into a list\", \"markup-reader\", or a marked drawing handed over. Carries no conventions: what a colour or a symbol means is the office's or the marker's, and it is asked rather than assumed. `drawing-diff` compares two issued revisions; this reads what somebody wrote on one. It does not replace the Architect of Record."
license: MIT
metadata:
  title: "Markup Reader"
  summary: "Read a marked-up drawing and turn it into a list somebody can act on"
  discipline: "construction-admin"
  tags: "Review, Documentation"
---

# Markup Reader

A marked-up drawing is a conversation that happened without you. Half the marks
are instructions, some are questions, a few are somebody thinking out loud, and
one is a circle around something with no words at all.

The cost of guessing which is which is that the guess gets built.

## Scope and limits — read first

**What this does.** Turns a markup into a numbered list: what each mark asks
for, what kind of ask it is, who it is for, and whether it can be acted on as
drawn. Flags every mark that cannot be read confidently.

**What this does not do.**

- **It carries no conventions.** What red means, what a cloud means, what a
  circle with no note means: that is the office's or the marker's, and it is
  asked rather than assumed. Conventions differ between firms and between
  people in one firm.
- **It guesses nothing.** An illegible or ambiguous mark is reported as such.
  A guessed markup is worse than an unread one, because it gets acted on.
- It does not compare revisions. `drawing-diff` does that between two issued
  drawings.
- It does not decide whether to make the change. That is a scope and design
  question. Point at `draft-additional-services` where a markup carries new
  scope.
- It does not replace the Architect of Record.

**What you need before starting.** The markup, at a resolution where the
handwriting is legible. The underlying drawing, at what revision. Who marked it
and when.

## Workflow

### Step 1. Establish who marked it and what they can decide

Ask, in one message:

> 1. Who marked it up, in what role, and when?
> 2. What drawing and revision is underneath? Is that the current one?
> 3. Was this discussed, or did the markup arrive on its own?
> 4. Does the office or this person use colour or symbols to mean anything
>    specific?
> 5. Is there a covering note, an email, or minutes that go with it?

**Question 1 decides how each mark is read.** A principal's markup instructs. A
consultant's asks. A client's is a wish that may not survive contact with the
budget. A contractor's may be a proposal, a question, or a record of what they
already built.

**Question 2 matters more than it looks.** A markup on a superseded revision may
already be resolved, or may be about to un-resolve something.

### Step 2. Number every mark and read it as it is

Go over the sheet systematically rather than by what catches the eye. Number in
reading order and never renumber.

| # | Where on the sheet | The mark, described | The words, verbatim |
|---|---|---|---|

Transcribe the words exactly, including the ones that are hard to read, and mark
uncertain transcription as uncertain. Do not tidy the wording; "make this
bigger" and "increase to suit" are different instructions and the second one is
not an instruction at all.

Include marks with no words. A circle, an arrow, a cross, a question mark: each
is a mark and each needs an answer about what it meant.

### Step 3. Sort each mark by what it asks

| # | Kind | For whom | Actionable as drawn? |
|---|---|---|---|

`Kind` is one of:

- **Instruction.** Do this.
- **Question.** Answer this.
- **Observation.** Noted, nothing to do.
- **Correction.** Something is wrong; fix it.
- **Unclear.** Cannot be read, or the words could mean two things.

`Actionable as drawn` is separate and is the useful column: an instruction can
be perfectly legible and still not actionable, because it does not say by how
much, or to what, or which of two things it points at.

**Report the unclear and the not-actionable counts before anything else.** Those
are what go back in one message rather than in five over two weeks.

### Step 4. Find what the marks imply beyond themselves

Marks travel:

- Does a mark on this sheet change another sheet, a schedule, or the
  specification?
- Does it change something a consultant has drawn? Point at `coordination-log`.
- Does it change scope, cost or programme? Point at `draft-additional-services`.
- Does it contradict another mark on the same sheet?
- Does it contradict something already agreed in writing?

### Step 5. Report

- Counts: total marks, unclear, not actionable as drawn.
- The numbered list with kind, for whom, and the verbatim words.
- Every mark that changes something off this sheet.
- Every contradiction between marks or with a prior agreement.
- The questions to send back, as one list.
- Whether the underlying revision is current.

### Step 6. Save

Ask where. Keep it with the markup. A transcribed markup is the record when the
original is a photograph on somebody's phone.

## Rules

- **Never guess a mark.** Unclear is a result.
- Transcribe words verbatim, including the awkward ones, and mark uncertain
  transcription.
- Number in reading order and never renumber.
- Include marks with no words.
- Ask what colours and symbols mean rather than assuming.
- Report unclear and not-actionable counts first.
- Check whether the underlying revision is current.

## Anti-patterns

- Reading the marks that catch the eye and calling it a list.
- Tidying the wording into an instruction it was not.
- Ignoring a circle with no note.
- Assuming red means one thing.
- Acting on a markup made on a superseded revision.
- Sending back questions one at a time over two weeks.
- Treating a client's markup as an instruction, or a principal's as a
  suggestion.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
