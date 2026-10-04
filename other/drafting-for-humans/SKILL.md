---
name: drafting-for-humans
description: Use when writing or editing any text with a reader — documentation, tickets, PR descriptions, release notes, design docs, specs, announcements, emails, customer-facing copy, and files written for an agent to read such as CLAUDE.md, skills, and memories. Also use when unsure how much context a reader needs, or when text written for teammates is heading somewhere wider.
---

# Drafting for Humans

Reader tier governs how much context the draft transfers, and how much evidence it carries. Two separate concerns sit elsewhere: voice belongs to a `write-like-me` skill, and shape and plain-English rules to the `plain` output style. Neither is required for this skill to work — where one is absent, apply the reader-tier judgement here, write plainly, and see Delegation for how to get it.

Applies to everything written, including replies to the person you are talking to and files written for an agent to read. There is no exempt category.

## The gate

Before drafting, answer: **what does this reader do differently after reading it?**

If nothing, it does not need writing. If the only answer is "understand that work happened", it is a status line, not a document — say it in one sentence and stop.

Correctness is not the bar. A document can be entirely true and still worthless, because the reader's question is never "is this right?" It is "why should I spend attention on this?" Answer that in the first two sentences or the rest goes unread.

## Tiers

| Tier         | Reader                                                                  | Orientation                  | Jargon                                 | Evidence                   |
| ------------ | ----------------------------------------------------------------------- | ---------------------------- | -------------------------------------- | -------------------------- |
| **peer**     | people who share your context, including the person you are replying to | none                         | full                                   | assert; backing on request |
| **org**      | colleagues outside your immediate team                                  | one sentence, in their terms | expand on first use, or replace        | assert; backing on request |
| **external** | customers, vendors, public                                              | full framing                 | none; no internal names or ticket keys | every claim traceable      |

### peer

Shared context is assumed — shared **facts**, not just shared vocabulary. Name systems directly. Lead with what changes for the reader's own work.

### Files an agent reads

CLAUDE.md, skills, memories, and prompts are `peer` — the reader shares the context and needs no orientation. The gate binds _harder_ here, not softer: every line is re-read on every future turn and spends context budget, so text that changes no future action is a recurring tax. Prefer the rule over the anecdote that produced it, and state it once in the place it will be looked for.

### org

The reader has no shared context and stops after the first line. State the problem in _their_ world — user impact, timeline, cost, risk — not in yours.

> Yours: "`LineItemMutationService` swaps line IDs on concurrent PATCH."
> Theirs: "Quotes can silently reprice when two people edit at once."

### external

Assume adversarial reading: this reader is looking for what you got wrong and what you are not saying. Every claim traceable. Commitments stated as what will happen, never what you hope. No speculation, no internal process detail.

## Evidence is pulled, not pushed

**Assert the conclusion. Keep the backing in reserve.** The reader trusts that you did the work — that trust is what a colleague extends by default, and spending it is the point of having done the work in the first place.

Include a number, a log line, or a citation only where the reader would otherwise doubt the claim. Never in proportion to what you gathered. The test is _"would this reader have asked for it?"_ — not _"can I support this?"_

Over-proving is not merely long, it misinforms. A reader who gets more support than the claim needs infers that the claim needed it, so piling on evidence makes a settled change read as contested. This is Grice's maxim of Quantity: as informative as required, and no more.

The failure mode is mistaking your own doubts for the reader's. After an investigation you hold questions the reader never had; writing to answer them produces a document addressed to yourself. Investigation detail belongs in the conversation, and in the artifact only once someone pushes back.

`external` is the exception — adversarial reading means the backing ships by default. Safety- and correctness-relevant detail is never cut to save words, at any tier.

## Anchor on what the reader already holds

**Describe a new thing as a change to something the reader already has.** A reader can load one structure and swap a slot. Given a fresh structure, the reader has to build it first — so an unanchored explanation costs more even when it is shorter.

Establishing the similarity is not padding. A difference is only visible against shared structure, so the anchor is what makes the contrast land. This is why a comparison to something known beats a correct description built from scratch, and why it is worth a sentence to name the anchor before stating the delta.

The anchor is tier-specific, and a wrong one costs more than none:

| Tier         | Anchor                                                                                                                                                              |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **peer**     | a system or change this reader has already worked on — "same as the other services' release gate, except what gets pinned is a commit rather than a build artifact" |
| **org**      | something in _their_ world: a tool they use, an incident they remember. Never a system of yours. Hardest here, and worth the most                                   |
| **external** | common knowledge only, or build the structure explicitly first. An analogy this reader cannot check reads as a claim, and adversarial reading will test it          |

When two things genuinely share no shape, say so and describe them separately.

## Artifact → default tier

| Artifact                                                 | Tier     |
| -------------------------------------------------------- | -------- |
| Chat reply to the person you are talking to              | peer     |
| CLAUDE.md, skill, memory, prompt                         | peer     |
| PR description, PR comment, code comment, commit message | peer     |
| Issue tracker ticket or comment                          | peer     |
| Spec artifact (proposal, design, spec, tasks)            | peer     |
| Internal wiki page, README                               | org      |
| Release notes, incident writeup, exec summary            | org      |
| Design doc read outside the immediate team               | org      |
| Anything leaving the organization                        | external |

Override inline: "draft this for org".

## Orientation is not preamble

Preamble is banned. Orientation is not preamble, and org and external drafts require it.

- **Orientation** transfers context the reader lacks — one sentence naming the system, the user-visible symptom, or the decision at stake.
- **Preamble** restates what the reader already has — the request, the title, or the fact that an explanation is coming.

At `peer` there is nothing to orient. Skip it.

## Delegation

| Concern                                       | Present                                                                                    | Absent                                              |
| --------------------------------------------- | ------------------------------------------------------------------------------------------ | --------------------------------------------------- |
| Voice, register, tone                         | a `write-like-me` skill — invoke it                                                        | `/build-voice-profile` builds one from your writing |
| Reply and document shape, plain-English rules | the `plain` output style — it is already applying                                          | `/install-output-style` puts it in place            |
| Sentence-level copyedit on long prose         | `elements-of-style:writing-clearly-and-concisely` — 12k tokens, only when actually editing | —                                                   |

Check which of the first two are actually there before pointing at either. Recommending a command for something already installed wastes the reader's time; assuming a skill exists when it does not leaves voice ungoverned. The three are independent — one being absent says nothing about the others.

Do not restate register rules here. If a draft sounds wrong rather than misjudging its reader, that is a `write-like-me` problem.

## Common mistakes

| Mistake                                                                         | Fix                                                                 |
| ------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| Writing an org doc in peer voice — correct, unreadable                          | Apply the org value test: restate the problem in the reader's world |
| Padding an org doc to seem substantial                                          | Orientation is one sentence; length is not credibility              |
| Stripping all jargon at `peer`                                                  | Shared vocabulary is faster; only expand where context is missing   |
| Speculating in external copy                                                    | Every claim traceable, or cut it                                    |
| Proving a claim the reader already believes                                     | Assert it; the backing is for a challenge                           |
| Writing to answer the questions your investigation raised                       | Answer the reader's question; yours belong in the conversation      |
| Explaining a new thing from scratch when the reader already knows its neighbour | Name the neighbour, then state the delta                            |
