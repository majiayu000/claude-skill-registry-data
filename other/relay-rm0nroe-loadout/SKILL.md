---
name: relay
description: Write a message addressed to a specific person or team who was NOT part of this conversation, which the user will hand off, paste, forward, or read aloud to them. Use this whenever the user says "draft a message to...", "write this up for my teammate", "write it addressed to them", "I'll relay this", "I'll pass this along", "send this to the author", "write feedback for whoever built this", "put this in a message for the team", or asks for a note, brief, handoff, or write-up that someone else will read. Also use it proactively when the user has just received findings, a review, a decision, a status, or a diagnosis and the obvious next step is telling someone else about it. The distinguishing signal is a named third-party reader plus an intermediary carrying the message, not that the content is technical.
---

# Relay a Message

## The core constraint

Someone who was not in the room is going to read this, and the person who was in the room will not be there to explain it. That single fact drives every choice below.

The reader cannot ask a follow-up question in the moment. They cannot see the conversation, the tool output, the files you read, or the reasoning that got you here. They may not know who wrote it or why they are receiving it. And the intermediary handing it over wants to paste it without rewriting it.

So the message has to survive alone. Everything else in this skill follows from that.

## Before writing, settle four things

Answer these from the conversation. If one is genuinely unresolvable and would change the message, ask, but most of the time the conversation already contains all four.

1. **Who is the reader and what do they own?** A plan's author, a team, a manager, a vendor. Their ownership determines what counts as news, what counts as insulting, and what they can actually act on.
2. **What is the ask?** Exactly what should they do after reading. Just as important, what should they *not* do. Unstated non-asks are the most common way a relay message causes damage: the reader helpfully starts work nobody wanted yet.
3. **What is already decided versus still open?** Readers relitigate anything you leave ambiguous. Mark settled things as settled so their energy goes to the open parts.
4. **Where does the full detail live?** A file path, a doc, a PR, a ticket. The message is the summary and the ask; the artifact is the reference. If no artifact exists and the detail is substantial, write one first and point to it.

## Structure

This spine holds for almost every relay message. Sections in the middle flex by message type; the opening and closing do not.

**Header.** To / From / Re. Put the ask or the boundary directly in the Re line so it survives even if the reader skims. `Re: Review results and required updates. Do not start work yet.`

**Boundary block, first.** Before any content, state what you are asking for and what you are explicitly not asking for. Put the non-asks in a visible list. This goes first because it is the part most likely to be misread, and because a reader who stops after this paragraph still behaves correctly.

**Credit, where it is real.** Name what the reader got right, specifically, with the same evidence standard as the criticism. This is not politeness padding, and generic praise reads as exactly that. Specific credit tells the reader you actually read their work, which is what makes the critical part land instead of triggering defensiveness. Skip it entirely if there is nothing genuine to say; inventing it is worse than omitting it.

**The one-sentence diagnosis.** Compress the whole finding into a single sentence a reader could repeat to someone else. If you cannot write that sentence, you do not understand the situation well enough to relay it yet.

**The substance.** Organized by what the reader must do about it, not by how you discovered it. Severity tiers, a status table, or plain sections all work. Chronology of your investigation almost never works, because the reader does not care how you got there.

**Actions, grouped by when.** Split into what to do now and what comes later, with effort estimates where you can. A flat list of twenty items reads as unstartable; the same twenty split into "four edits, about 20 minutes" and "the larger rewrite" reads as tractable.

**The root-cause change.** When there is a structural fix that prevents recurrence, call it out separately from the item list. Individual fixes get made and the pattern repeats; naming the pattern is often the highest-value part of the message.

**Close with one action and the boundary restated.** One concrete next step, then repeat any hold instruction. The end is the other place people stop reading, so it carries the same weight as the top.

## Principles

**Evidence the reader can check themselves.** `plan:1951-1955 defines shouldSkip including isRetry` beats "the dedupe logic is wrong." Citations let the reader verify without trusting you, which matters most when you are delivering something unwelcome through a third party. File and line, a quote, a command and its output, a version number.

**Verify anything expensive to be wrong about.** Before asserting a claim that would send someone on a multi-hour goose chase, check it. Run the snippet, read the file, confirm the version. A relay message is harder to correct than a conversation, because the correction has to travel back through the intermediary.

**Separate what you know from what you infer.** Readers act on both, so mark which is which. "I ran this and got X" and "this probably means Y" deserve different phrasings.

**Do not import conversational context.** No "as we discussed", no "the thing you mentioned earlier", no pronouns pointing at things outside the message. Every reference must resolve inside the text.

**Write for the reader's reaction, not just their comprehension.** A message that is technically complete but reads as an attack gets argued with rather than acted on. Lead with what is right, be specific about what is wrong, attribute problems to the artifact rather than the person, and never speculate about why they made a mistake.

**Match the user's voice and rules.** Check for style constraints in effect (a CLAUDE.md, a persona file, a house style) before drafting. If the user has punctuation or formatting rules, they apply here in full, because this text goes out under their name.

**Length follows the ask.** A three-line relay is correct when the ask is small. Do not inflate a simple handoff into a report. Conversely, do not compress a genuinely complex handoff into a paragraph the reader cannot act on.

## Message types

The spine holds, but weight shifts. Read `references/message-types.md` when the message is not review feedback, for the specific adjustments for status updates, asks and requests, decisions, bad news, and escalations.

## Worked example

`references/worked-example.md` is a complete annotated relay message: adversarial review findings sent to the author of a plan, with a hold instruction. Read it when you want to see the structure fully realized rather than described, particularly the boundary block and the credit section, which are the two parts most often done badly.

## Failure modes

**Burying the boundary.** The hold instruction lands in paragraph nine and the reader has already started work. Put it in the Re line and the first block.

**Generic credit.** "Great work overall" reads as a setup for the criticism and costs you the trust that specific credit would have bought.

**Assertion without evidence.** Every unsupported claim becomes a round trip through the intermediary.

**Relitigating settled decisions.** If the user tells you something is locked, it is locked. You may flag an unhandled consequence of that decision, which is useful, but proposing a reversal wastes the reader's attention and undermines the parts of the message that are actionable.

**Dumping the investigation.** The reader wants the conclusion and the ask. How many agents ran, what you searched, which hypothesis you discarded: mention method in one line if it establishes credibility, then move on.

**Writing a document instead of a message.** A message has a reader, an ask, and an ending. If it reads like a report with a To: line stapled on, restructure around what the reader must do.

**Silent scope drift.** If the user asked for a message and you also want to change files, ask first. Relay work is communication, not implementation.

**Sending it yourself.** Drafting is the task; the user is the send gate. If the message is destined for somewhere outward-facing (a PR comment, Slack, email, a ticket), do not post it without explicit approval, and remember that approval to draft is not approval to send.
