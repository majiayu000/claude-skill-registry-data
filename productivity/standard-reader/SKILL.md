---
name: standard-reader
description: "Reads any referenced standard — a test method, a product standard, a design standard, an industry guideline — and answers the four questions that decide whether it means anything on this project: what it actually covers, whether it binds here or is only advisory, which edition is the one that binds, and what it deliberately does not address. A standard cited in a specification is often doing none of the work anybody assumes. Trigger on \"what does this standard say\", \"is ASTM E-something relevant here\", \"they referenced a standard\", \"does this standard apply to us\", \"standard-reader\", or a standard cited in a spec, a submittal, or a manufacturer's claim. Carries no standard text: everything comes from the document you supply or the publisher, never from recall, since standards are revised and paraphrase drifts. It does not certify compliance and does not replace the code consultant or the Architect of Record."
license: MIT
metadata:
  title: "Standard Reader"
  summary: "Read a referenced standard for what it covers and what it does not"
  discipline: "code-life-safety"
  tags: "Compliance, Reference"
---

# Standard Reader

Standards get cited more than they get read. A specification references six, a
manufacturer claims three, a submittal lists two, and almost nobody has opened
any of them. Most of the time this is fine. When it is not, the reason is
usually that the standard is a test method being quoted as though it were a
performance requirement.

## Scope and limits — read first

**What this does.** Answers four questions about a cited standard: what it
covers, whether it binds, which edition binds, and what it does not address.

**What this does not do.**

- **It carries no standard text.** Standards are copyrighted, revised, and
  paraphrased badly from memory. Everything comes from the document you supply
  or from the publisher.
- It does not certify compliance with anything.
- It does not verify that a product meets a standard. That is a test report,
  and reading one is a different exercise.
- It does not verify the citation itself. `cite-check` does.
- It does not take a code section apart. `code-reader` does.
- It does not replace the code consultant or the Architect of Record.

**What you need before starting.** The standard's designation exactly as cited,
including its year. Where it was cited: a spec section, a code, a submittal, a
manufacturer's claim. The standard itself, if you have it. What it is being
relied on to prove.

## Workflow

### Step 1. Establish what kind of standard it is

The distinction that resolves most confusion. Ask, and say which:

| Kind | What it does | What it does not do |
|---|---|---|
| Test method | Describes how to perform a test | Says nothing about what result is acceptable |
| Classification | Sorts results into classes | Says nothing about which class you need |
| Product standard | What a product must be to carry the name | Says nothing about whether you need that product |
| Design standard | How to design something | Binds only where adopted or specified |
| Practice or guideline | Recommends | Binds nothing on its own |

**A test method quoted as a requirement is the most common misuse.** A material
"tested to" a method has been tested; that is all it says. The acceptable result
comes from somewhere else, and that somewhere else is what should have been
cited.

### Step 2. Establish whether it binds here, and how

A standard binds on a project by one of three routes, and it matters which:

- **Adopted by the code**, which makes it code. Then the edition that binds is
  the one the code names, not the current one.
- **Specified**, which makes it contractual. Then the edition is the one the
  specification names.
- **Neither**, in which case it is a reference somebody quoted and it binds
  nothing.

Report which route, and say plainly when the answer is the third. Point at
`cite-check` if the citation itself has not been verified.

### Step 3. Establish which edition

- Which edition was cited, and was a year given at all?
- Which edition does the code adopt, if it is adopted?
- Which edition does the specification name, if it is specified?
- Are those the same? **They frequently are not**, and a manufacturer testing to
  the current edition of a standard the code adopted six years ago has produced
  a result that may not be the one required.
- Has the standard been withdrawn, superseded, or split since?

### Step 4. Say what it covers, and what it does not

From the document itself, and only from it:

- Its stated scope, quoted.
- What is in it: the procedure, the classes, the requirements.
- **What its scope explicitly excludes.** Standards say this and it is where the
  gap usually is.
- What it references in turn, which becomes binding with it.
- What somebody is trying to use it to prove, and whether its scope reaches
  that.

That last comparison is the point. A standard can be real, current, properly
adopted, and simply not about the thing it is being cited for.

### Step 5. Report

- What kind of standard it is, first.
- How it binds here, or that it does not.
- Editions: cited, adopted, specified, and whether they agree.
- Its scope, quoted, and its stated exclusions.
- Whether it reaches the claim it is being used for.
- What could not be answered without the document, if you did not have it.

Say plainly on every run that nothing was certified and that the standard's text
was taken from the document rather than recalled.

### Step 6. Save, if asked

Ask whether to write the reading to a file and where. Point at
`jurisdiction-profile`, which is where an adopted standard's edition belongs so
it is established once.

## Rules

- **Never quote or paraphrase standard text from memory.**
- Establish which of the five kinds it is, first.
- Say which of the three routes makes it bind, or that none does.
- Compare the cited, adopted and specified editions, every run.
- Report the standard's stated exclusions.
- Say whether its scope reaches the claim it is being used for.
- Never certify compliance.

## Anti-patterns

- Quoting a standard from recall because the designation is familiar.
- Reading a test method as a performance requirement.
- Assuming the current edition is the one that binds.
- Treating a guideline as mandatory because it is cited.
- Accepting "tested to" as evidence of a result.
- Ignoring what the scope excludes.
- Certifying anything.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
