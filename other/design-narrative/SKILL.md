---
name: design-narrative
description: "Writes the project description that gets asked for again and again in different lengths and for different readers: a planning submission, a design review board, an award entry, a website page, a client's own report. Establishes who is reading and what they can do about it before writing a word, since a board that can refuse and a magazine that cannot are different documents, then builds one account of the project that the shorter versions are cut from rather than rewritten. Trigger on \"design narrative\", \"project description\", \"write up the project\", \"we need a paragraph for the submission\", \"award entry text\", \"design-narrative\", or a request for words about a building. Carries no house voice and no claims of its own; every fact comes from the project and every claim has to be true of the drawings. It does not replace the Architect of Record."
license: MIT
metadata:
  title: "Design Narrative"
  summary: "Write what the project is, for a reader who was not in the room"
  discipline: "design-building-types"
  tags: "Documentation, Design"
---

# Design Narrative

The same project gets written up five times: a planning statement, a board
presentation, an award entry, a website page, a paragraph for the client's
annual report. Each is written from scratch, each says something slightly
different, and the differences turn up later in a hearing.

## Scope and limits — read first

**What this does.** Establishes who reads it and what they can do about it, then
builds one full account from which the shorter versions are cut. Checks every
claim against the drawings.

**What this does not do.**

- **It carries no voice and no claims.** The practice's voice is the practice's;
  every fact comes from the project and every claim has to be true of what is
  drawn.
- It does not translate for a client conversation. `client-translator` does.
- It does not build a submission. `rfp-response-builder` and `sf330-builder`
  answer solicitations, and this supplies the project text they use.
- It does not make the design better or explain away a weakness. A narrative
  that argues around a problem is read by people who see the problem.
- It does not replace the Architect of Record.

**What you need before starting.** The project. Who is asking, for what, at what
length, by when. The drawings. What has already been said in writing about this
project, and to whom.

## Workflow

### Step 1. Establish the reader and what they can do

Ask, in one message:

> 1. Who reads it, and what can they do about it? Refuse it, fund it, publish
>    it, or nothing?
> 2. What length, and is there a prescribed structure or a set of headings?
> 3. What do they already know: the site, the brief, the practice?
> 4. What has already been said about this project in writing, and to whom?
> 5. What must not be said: confidential, not yet agreed, or a client
>    sensitivity?
> 6. What is the deadline?

**Question 1 decides everything.** A board that can refuse wants to know how the
scheme answers the thing they might refuse it for. An award jury wants to know
what is different about it. A website reader wants to know what it is like to be
in. The same paragraph does not do all three, and a narrative written for the
wrong reader is the most common reason it does not land.

**Question 4 matters more than it looks.** Anything already said in a planning
statement is on the record, and a later account that differs is a gift to
somebody objecting.

### Step 2. Build the full account once, in a fixed order

Longer than any version that will be used. The short ones are cut from it.

1. **What it is.** One sentence: type, size, where, for whom. No adjectives.
2. **What was asked for.** The brief and the constraints, honestly, including
   the ones that were awkward.
3. **What the site decided.** Point at `site-analysis`. Readers respect a
   scheme that answers a site more than one that arrived with an idea.
4. **The organising idea, in one sentence.** Point at `parti-study`. If there
   isn't one, do not invent one for the narrative; describe what does organise
   it.
5. **How the idea meets the awkward parts.** The constraints from point 2. This
   is the section that convinces and it is the one usually left out.
6. **What it is made of, and why.** Materials as decisions, not as a list.
7. **What it does about the things this reader will ask about.** Energy,
   context, access, cost, neighbours, whatever is live for them.
8. **What is not resolved yet**, where the reader is entitled to know.

### Step 3. Check every claim against the drawings

The step that separates a narrative from marketing:

| Claim | Where in the drawings | True as drawn? |
|---|---|---|

Go through every sentence that asserts something: that a space is generous, that
a route is direct, that a material is durable, that the building is quiet, that
it opens to the south. **Each is either visible in the drawings or it is not.**

Mark anything not yet true as an intention rather than a fact, and say so in the
text. A claim about a building that has not been built is a promise, and boards
and juries both read it as one.

Flag every superlative. Most cannot be checked and none of them survive a
reader who was not persuaded already.

### Step 4. Cut the versions from the account

For each requested version, cut rather than rewrite:

| Version | Reader | Length | Sections kept | What it opens with |
|---|---|---|---|---|

- **Planning or board.** Sections 2, 3, 5, 7. Opens with how it answers the
  thing they might refuse it for.
- **Award or publication.** Sections 1, 4, 5, 6. Opens with what is different.
- **Website or client.** Sections 1, 3, 6. Opens with what it is like to be
  there.
- **One paragraph.** Sections 1 and 4, and nothing else.

Keeping the versions cut from one account is what stops them contradicting each
other, which is the whole reason to do it this way.

### Step 5. Read it as three people

Before it goes:

- **Someone who will refuse it.** What is the weakest sentence, and does the
  narrative pretend it is not there?
- **Someone who was not in the room.** Is there jargon, an unexplained acronym,
  a reference to a decision they never heard about?
- **The client.** Is anything said about their project, their budget or their
  business that they have not agreed to?

### Step 6. Report

The full account, the version table, the claims check with everything unverified
listed, and anything that contradicts what has already been said in writing.

Then ask where to write it, and keep the full account, because the next request
is cut from it too.

## Rules

- **Establish who reads it and what they can do**, before writing.
- Build one full account and cut the versions from it. Never write a version
  from scratch.
- Every claim resolves to something in the drawings, or is marked an intention.
- Never invent an organising idea for the text.
- Flag every superlative.
- Check against what has already been said in writing.
- Never argue around a weakness. Name it or leave it out.

## Anti-patterns

- Writing the award entry and the planning statement separately.
- Adjectives instead of decisions.
- Claiming a quality the drawings do not show.
- Leaving out the awkward constraints, which are the part that makes the scheme
  legible.
- A concept invented for the narrative after the building was designed.
- Saying something about the client's budget or business without their
  agreement.
- Writing for a reader who cannot do anything about it, when the reader can.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
