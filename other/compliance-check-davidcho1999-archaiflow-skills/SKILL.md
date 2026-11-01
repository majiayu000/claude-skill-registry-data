---
name: compliance-check
description: "Takes a drawing and the code text that governs it and works through them together, one requirement at a time: what the text demands, what the drawing shows, and whether the drawing shows enough to tell. The third answer is the common one and it is the useful one, because a drawing that does not say is not a drawing that complies. Trigger on \"does this drawing meet this code\", \"check this against the code text\", \"we pasted the section, now check the plan\", \"compliance-check\", or a drawing and a quoted requirement handed over together. Carries no code text and recalls no limit: everything comes from what you paste. `code-compliance-review` audits a plan across eight fixed axes without being given text; this checks whatever text you bring against whatever drawing you bring. It does not interpret the clause, does not certify anything, and does not replace the code consultant or the Architect of Record."
license: MIT
metadata:
  title: "Compliance Check"
  summary: "Hold a drawing against code text you paste, item by item"
  discipline: "code-life-safety"
  tags: "Compliance, Review"
---

# Compliance Check

Two things get merged: whether the design complies, and whether the drawing
shows that it complies. They are different, and the second is what a reviewer
actually decides on. A correct building drawn without the dimension is a
correction letter.

## Scope and limits — read first

**What this does.** Takes text you supply and a drawing you supply and works
through them together, reporting three states per requirement rather than two:
meets, does not meet, and the drawing does not say.

**What this does not do.**

- **It carries no text and no limits.** Everything comes from what you paste.
  Nothing is recalled, and a requirement without pasted text is not checked.
- It does not interpret the clause. `code-reader` takes a section apart and
  `explain-code` puts it in plain English.
- It does not verify the citation. `cite-check` does.
- It does not audit across a fixed set of topics. `code-compliance-review` does that
  without needing text, and the two are complements: run that for coverage and
  this for depth on one requirement.
- **It certifies nothing.** It reports what a drawing shows against what a text
  says. Compliance is determined by the authority.
- It does not replace the code consultant or the Architect of Record.

**What you need before starting.** The requirement, pasted, with its exceptions.
The drawing, at a scale that shows what has to be checked. The dimensions, if
they are not on the drawing.

## Workflow

### Step 1. Take both, and say what is missing before starting

Ask, in one message:

> 1. Paste the requirement in full, with its exceptions.
> 2. The drawing, and what it is: plan, section, detail, schedule, at what
>    scale and what revision.
> 3. Are the relevant dimensions on the drawing, or do you have them
>    separately?
> 4. Which jurisdiction and edition, and are there amendments? Point at
>    `cite-check` if the citation has not been verified.

If the text is not pasted, stop. **A check run against a remembered requirement
is worse than no check**, because it produces a result somebody will rely on.

### Step 2. Break the requirement into checkable items

Point at `code-reader` if the text is dense. Each item must be something a
drawing can show or fail to show.

| # | Requirement, quoted | What the drawing would have to show |
|---|---|---|

The second column is the discipline of this step. "Adequate egress" is not
checkable; "two exits at least this far apart, measured this way" is. Where the
text is not reducible to something a drawing shows, say so and mark the item
unverifiable rather than guessing.

### Step 3. Read the drawing against each item

| # | Required, quoted | Drawing shows | Result | Where on the drawing |
|---|---|---|---|---|

`Result` is one of:

- **Meets.** The drawing shows it and it satisfies the text.
- **Does not meet.** The drawing shows it and it does not.
- **Drawing does not say.** The information is not on the drawing.
- **Cannot tell.** The drawing shows something ambiguous, at the wrong scale, or
  contradicted elsewhere.

**Report the third and fourth counts before the first two.** Most findings on
most sets are `drawing does not say`, and that is the finding the design team
can act on today.

### Step 4. Check the exceptions in both directions

- Does an exception apply and reduce a finding?
- Does an exception apply that would have helped and was not used?
- Does the drawing rely on an exception without saying so? An exception relied
  on silently is a correction letter.

### Step 5. Report

- Counts by result, `drawing does not say` first.
- Every failing item with the quoted requirement, what the drawing shows, and
  where.
- Every item that could not be reduced to something a drawing shows.
- Every exception applied and every one left unused.
- What was not checked, and why.

Close with the standing limits, every run: the text was taken as given and not
verified, nothing was interpreted, and this is not a determination of
compliance.

### Step 6. Save, if asked

Ask whether to write the check to a file and where. CSV where it becomes a
mark-up list.

## Rules

- **Never check against text that was not pasted.** Stop instead.
- Reduce each requirement to something a drawing can show, or mark it
  unverifiable.
- **Report `drawing does not say` before pass and fail.**
- Say where on the drawing every finding is.
- Check the exceptions in both directions.
- Never write compliant, approved, or certified.

## Anti-patterns

- Checking against a remembered limit because the text was not to hand.
- Merging "does not meet" with "does not say".
- Reporting a pass rate.
- Reading the requirement and not its exceptions.
- Checking a drawing at a scale that cannot show the thing being checked.
- Interpreting the clause to make the drawing pass.
- Calling the result compliance.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
