---
name: code-reader
description: "Takes a code section, a standard, or an ordinance you paste and pulls it apart into the separate requirements inside it: what each one applies to, what it demands, what triggers it, what exempts it, and which other section it hands off to. A single paragraph routinely contains four requirements and two exceptions, and reading it as one sentence is how half of it gets missed. Trigger on \"read this code section\", \"what does this clause actually require\", \"pull the requirements out of this\", \"code-reader\", or a pasted section that has to be worked through. Carries no code text and recalls no section: everything comes from what you paste or from the jurisdiction's own published source. `explain-code` puts one clause in plain English; this takes the clause apart into a table you can check a design against. It does not check the design — `compliance-check` does — and does not replace the code consultant or the Architect of Record."
license: MIT
metadata:
  title: "Code Reader"
  summary: "Turn a code section into the requirements it actually contains"
  discipline: "code-life-safety"
  tags: "Compliance, Reference"
---

# Code Reader

A code paragraph looks like one requirement and is usually four, with two
exceptions and a reference to a section nobody opened. Read as prose it produces
one thing to check. Taken apart it produces six, and the ones that get missed
are always the exceptions and the hand-offs.

## Scope and limits — read first

**What this does.** Takes the text and produces a table of separate
requirements, each with what it applies to, what it demands, what triggers it,
what exempts it, and where it sends you next.

**What this does not do.**

- **It carries no text and recalls no section.** Everything comes from what you
  paste or from the jurisdiction's own published source. A section quoted from
  memory is wrong even when the number is right, because editions differ.
- It does not explain in plain English. `explain-code` does that, and the two
  are read at different moments: this one before checking a design, that one
  before a conversation.
- It does not check a design. `compliance-check` holds a drawing against text.
- It does not verify that the section is the right one. `cite-check` does.
- It does not follow the hand-offs. It names them; opening each one is another
  run.
- It does not replace the code consultant or the Architect of Record.

**What you need before starting.** The section, pasted in full including its
exceptions and any table it references. The document and edition it came from.
The jurisdiction, and whether it amends this section.

## Workflow

### Step 1. Establish what you are reading

Ask, in one message:

> 1. Paste the section in full, including the exceptions and anything indented
>    under it.
> 2. Which document, which edition, and which jurisdiction?
> 3. **Has the jurisdiction amended this section?** Local amendments are part of
>    the text and they are not in the model code you pasted.
> 4. Are the tables and figures it references available, or only referenced?
> 5. What are you about to check against it?

Report immediately if the paste stops mid-section, if a referenced table is
missing, or if the amendments are unknown. Each of those makes the reading
partial and it should say so rather than produce a confident table.

### Step 2. Split the text into separate requirements

One row per requirement, not one row per sentence. A sentence with an "and" in
it is usually two.

| # | Applies to | Requires | Trigger | Exception | Sends you to |
|---|---|---|---|---|---|

- **Applies to.** The scope. Which occupancies, which construction types, which
  conditions. A requirement applied outside its scope is the most common
  over-reading.
- **Requires.** What must be true. Quote it rather than paraphrase; a
  paraphrase is where the meaning shifts.
- **Trigger.** What makes it apply: a threshold, an area, a height, a change of
  use, an alteration.
- **Exception.** Every exception, each on its own line. **An exception is a
  requirement in reverse and it is missed more often than anything else.**
- **Sends you to.** Every other section, standard, or table this one references.

### Step 3. Read the words that do the work

Go back through the text and flag each:

- **shall / should / may / is permitted to.** One binds, one advises, two
  permit. Report every instance and which it is.
- **and / or** in a list of conditions. Whether all or any of them apply changes
  everything, and the sentence rarely makes it obvious.
- **Numbers with units**, and whether they are minimums, maximums, or nominal.
- **Terms the code defines elsewhere.** Any capitalised or specially used word
  probably has a definition section, and the ordinary meaning is usually
  narrower or wider. Flag each and say the definition was not read.
- **"in accordance with"** followed by another document. That is a whole other
  document becoming binding.

### Step 4. List what you cannot answer from this text alone

- Every defined term whose definition was not supplied.
- Every referenced section, table or standard not supplied.
- Every place the amendments are unknown.
- Anything the text leaves to the authority's judgement.

Report the count. **A section read on its own is rarely complete**, and saying
how incomplete is more useful than a table that looks finished.

### Step 5. Report

The requirements table, the working-words flags, and the list of what is
missing. Then say plainly what the next section to open is, and why.

### Step 6. Save, if asked

Ask whether to write it to a file and where. Point at `jurisdiction-profile`,
which is where these belong if the project will use them more than once.

## Rules

- **Never supply or recall code text.** Pasted, or from the publisher.
- Ask about local amendments, every run.
- One row per requirement, never per sentence.
- Every exception gets its own line.
- Quote the requirement; never paraphrase it into the table.
- Flag every shall, should, may, and every and/or in a condition list.
- Count what could not be answered from this text alone.

## Anti-patterns

- Reading the paragraph as one requirement.
- Paraphrasing into the table, which is where the meaning quietly moves.
- Skipping the exceptions.
- Treating a defined term as its ordinary meaning.
- Producing a complete-looking table from a section whose references were never
  opened.
- Assuming the model code text is the adopted text.
- Answering what the design should do. Different skill.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
