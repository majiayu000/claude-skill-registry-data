---
name: cite-check
description: "Takes a citation somebody handed you — in a review comment, a consultant's report, a contractor's letter, a manufacturer's claim, or your own earlier drawing — and checks the three things that make it usable: does the document exist and in which edition, does the section number resolve inside it, and does the text actually say what it is being used to say. Reports which of the three could be verified and which could not, rather than a yes or a no. Trigger on \"is this citation right\", \"check this code reference\", \"they quoted a section at us\", \"does this clause say that\", \"cite-check\", or a section number pasted with a claim attached. Carries no code text: verification comes from the document you supply or from the jurisdiction's own published source, never from recall and never from a search result that is not the publisher. It does not interpret the clause — `explain-code` does — and does not replace the code consultant or the Architect of Record."
license: MIT
metadata:
  title: "Cite Check"
  summary: "Check whether a citation someone gave you is real and current"
  discipline: "code-life-safety"
  tags: "Compliance, Review"
---

# Cite Check

Citations get repeated. A reviewer quotes a section, a consultant repeats it in
a report, it goes into a drawing note, and two years later nobody can say which
edition it came from or whether the text ever said that. Most of them are fine.
The ones that are not are expensive and they look identical.

## Scope and limits — read first

**What this does.** Splits the citation into three separate questions and
answers each one independently: the document, the section, and the claim.
Reports what could be verified and what could not.

**What this does not do.**

- **It carries no code, standard, or contract text.** Verification comes from
  the document you supply, or from the publisher's own source. **A search result
  that is not the publisher is not verification** and is never treated as one.
- It does not interpret. What a clause means for your project is
  `explain-code`'s and the code consultant's.
- It does not check whether the design complies. `compliance-check` holds a
  drawing against text; this checks whether the text is what it claims to be.
- It does not say the citation is wrong when it cannot be verified. Those are
  different findings and conflating them is how a correct reviewer gets
  argued with.
- It does not replace the code consultant or the Architect of Record.

**What you need before starting.** The citation exactly as it was given, and
what it is being used to prove. The document, if you have it. What jurisdiction
and what project stage, so the edition question can be asked properly.

## Workflow

### Step 1. Take the citation exactly as given, and separate the claim

Ask, in one message:

> 1. The citation, verbatim, including the edition or year if one was stated.
> 2. Who gave it, in what document, and on what date?
> 3. **What is it being used to prove?** Write that as a sentence separate from
>    the citation itself.
> 4. Do you have the document, or a published source for it?
> 5. Which jurisdiction, and what edition does it adopt? Point at
>    `jurisdiction-profile`.

Question 3 is the whole exercise. A citation and a claim are two things, and a
real section is routinely attached to a claim it does not support.

### Step 2. Check the document

- Does the document exist under that name?
- Which edition, and is it the one this jurisdiction adopts? Local amendments
  are part of the answer and they are the part most often missed.
- Was the edition stated at all? An unstated edition is a finding, because
  section numbers move between editions and the same number is a different
  requirement.
- Is it a code, a referenced standard, or a guideline? A guideline quoted as
  though it binds is a common and quiet error.

### Step 3. Check the section

- Does that number resolve inside that document?
- Does it resolve to a section about the subject at hand, or has a number been
  transposed?
- Is the number complete, or is a subsection missing that changes it?
- If it is a referenced standard, does the code actually reference that edition
  of it?

### Step 4. Check the claim against the text

Only with the text in hand. Quote the operative sentence, then set it beside the
claim from Step 1:

| | |
|---|---|
| Claim | what it is being used to prove |
| Text says | the operative sentence, verbatim |
| Supports it? | fully / partly / no / cannot tell |

`partly` is the most common answer and the most useful one. A clause that
supports half a claim is not a clause that supports the claim, and saying so is
more useful than a verdict.

Read the exceptions. **A requirement quoted without its exceptions is the single
most common way a real citation misleads**, and the exception is usually the
sentence after the one that got quoted.

### Step 5. Report as three answers, not one

| Question | Answer | How it was verified |
|---|---|---|
| Does the document exist, in which edition | | |
| Does the section resolve | | |
| Does the text support the claim | | |

Then:

- What could not be verified, and what would verify it.
- Whether the edition question is open.
- Any exception or qualifier in the text that the citation left out.
- If the claim is not supported, the sentence that would have supported it, if
  there is one elsewhere in what you were given.

**Never report a single verdict.** A citation can be a real section of the right
document and still not say what it is being used to say, and that is a different
conversation from a wrong section number.

### Step 6. Save, if asked

Ask whether to write the check to a file and where. Where the citation came from
a reviewer or a claim, keep it.

## Rules

- **Never verify from memory.** The document, the publisher, or not verified.
- **A search result that is not the publisher is not verification.**
- Separate the claim from the citation in Step 1, always.
- Answer the three questions separately and report them separately.
- Read the exceptions and report any the citation omitted.
- `cannot verify` and `wrong` are different findings and are never merged.
- Ask which edition the jurisdiction adopts, every run.

## Anti-patterns

- Confirming a section number from recall because it looks familiar.
- Treating a code aggregator site as the publisher.
- Reporting yes or no.
- Checking the section and not the claim.
- Quoting the requirement and not the exception under it.
- Ignoring the edition because the number resolves in the one you have.
- Calling an unverifiable citation wrong.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
