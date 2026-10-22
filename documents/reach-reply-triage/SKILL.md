---
name: reach-reply-triage
description: Reads one reply and sets out what it actually says, what it asks of you and by when, the facts it adds to your brief and points for your answer, with "stop" recorded at once so the person is never written to again. Use for "run reach-reply-triage", "reply triage", "they replied what now", "how do I answer this reply", "is this a yes or a no", "what does this reply mean", "they said not now", "they asked me to stop emailing", part of the Claude Guide for Outreach Pack by Polar Bear.
---

# Reply Triage

## When To Use
A reply arrives and you are not sure whether it is interest, politeness or a no. So it sits for four days. This answers: what does the message say, what is it asking of me, and what do I owe in return?

## When Not To Use
If nobody has replied, the Follow-Up Tracker decides what is due. If they said yes to a call, read the reply here once, then move to First Call Prep. This skill reads a message; it never guesses how a person feels.

## Inputs
- The reply, pasted. Or, with the Gmail connector, the one thread you name: searched and read only, never drafted in or sent from.
- What you wrote to them, and the reason you chose.
- Your brief for this person or organisation, if you have one.
If you have none of this, I start from the reply alone and mark anything that depends on your original message as "cannot tell".

## Approach
Read the message, not the person. A reply is sorted by what its words say into six kinds: yes, a question, not now, wrong person, no, stop. A no is accepted, not handled, and a stop is honoured at once. The UK Information Commissioner's Office guidance on business-to-business marketing describes keeping a list of people who have objected so they are not contacted again; how such rules apply to you is a question for an adviser. The failure it prevents: reading "not for us right now, thanks" as an opening and replying with a calendar link.

## Workflow
1. Ask at most three questions: which reply, what you had asked for, and whether anything was said outside this thread.
2. Quote the lines that carry the answer and sort the reply into one kind: yes, a question, not now, wrong person, no, stop. If two kinds fit, say so and show both lines; I do not round a maybe up to a yes.
3. Say what it asks of you and by when, in their terms: an answer, a time, a document, another name, nothing.
4. If the kind is stop, or the words ask not to be contacted, record it first: the name goes on your do not contact list today and comes off every run. Nothing else in the triage outranks this.
5. Pull out the new facts the reply gives about their work, each marked "from their reply, [date]". They go into your brief as facts they told you, not as inferences.
6. Give points for your answer, matched to the kind: for a question, the answer and nothing more; for not now, a thank you and no date unless they offered one; for wrong person, thanks, and only write to the named colleague if they suggested it; for no, a short thank you or silence.
7. Stop before the reply itself. You write it.

## Output Format
```markdown
# Reply Triage
From: [name] | Received: [date] | In answer to: [your message of date, reason] | Kind: [yes / a question / not now / wrong person / no / stop]
## What the reply says
- "[the line that carries the answer]"
## What it asks of you
| They ask for | By when | You owe |
|---|---|---|
| [an answer / a time / a document / another name / nothing] | [date, or not stated] | [your action] |
## Do not contact
[Not requested / requested on [date]: added to your do not contact list and removed from all runs.]
## New facts from the reply
- [fact about their work] (from their reply, [date])
## Points for your answer
1. [point, matched to the kind]
## Decision
[Your name] writes and sends the answer by [date], or decides no answer is needed; a stop is recorded today.
```

## Done When
- The kind is one of six and rests on a quoted line.
- What you owe has an action and a date.
- A stop or a request not to be contacted is recorded before anything else.
- No reply text was written for you.

## Quality Bar
- No reading of tone, mood, interest level or likelihood; only what the words say.
- A no is not an objection to overcome.
- "Wrong person" does not license a message to a colleague unless the reply offers one.
- Legal points on objection and do not contact lists: check with a qualified adviser.
- Claude reads the reply and gives points; you write the answer and send it, and a stop is final.

## Next
Run reach-first-call-prep (First Call Prep) when the reply is a yes to a conversation.

## About the makers

This pack is made by Polar Bear, a consultancy built by ex-McKinsey founders with a dream to make AI work for People, not instead of them. We help our clients build people systems and AI-first ways of working, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
