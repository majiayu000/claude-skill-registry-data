---
name: reach-voice-guide
description: Builds your writing voice guide from messages you wrote and sent yourself, with how you open, ask and sign off, the words you use and never use, an AI-tell checklist and one real message before and after. Use for "run reach-voice-guide", "writing voice guide", "voice guide", "make my messages sound like me", "my outreach sounds like AI", "my tone of voice", "everything sounds generic", "how do I write", part of the Claude Guide for Outreach Pack by Polar Bear.
---

# Writing Voice Guide

## When To Use
Everything a tool drafts for you sounds like everyone else's, and the people you write to can tell. Run this once, before the first run. It gives the later checks something to measure against: how you actually write when nobody is helping.

## When Not To Use
If you have fewer than ten pieces you wrote and sent yourself, write a few real messages first; a guide built on three emails is a guess. This is not a check on one message: for that, use Message Checklist.

## Inputs
- Ten to twenty pieces you wrote and sent with no tool: emails, messages, notes to people you respect. Pasted or uploaded.
- One message you are about to send, for the before and after.
- Optional: words or phrases you already know you dislike.
If you have none of this, I start from five pieces you paste now and mark the guide as a first draft. Keep the guide in memory or in a Project (beta) so later checks can use it.

## Approach
Your voice lives in your own sent writing, so the guide is built from that and from nothing I wrote. It is then set against the public "Signs of AI writing" page kept by Wikipedia's WikiProject AI Cleanup, which lists the patterns readers recognise as machine text. That page was written for encyclopedia editors, so only the patterns that apply to a short personal note are used. The failure it prevents: a first message that opens with "I hope this finds you well" and three tidy bullet points, read in two seconds as a template.

## Workflow
1. Ask at most three questions: which pieces are truly yours and untouched by a tool, who you usually write to, and whether you write differently to people you do not know.
2. Read the pieces and pull out, each with one quoted example from your own text: how you open, how you ask for something, how you sign off, your usual sentence length, and how you take a no.
3. List the words and phrases you use often, and the ones you never use. A word counts as "never" only if it is absent from every piece; you confirm the list.
4. Build the AI-tell checklist by pattern, in your own terms: inflated significance, stock openers and closers, lists of three by habit, vague attributions such as "experts say", hedges stacked on hedges, a closing line that repeats the message.
5. Run the before and after on your one message: mark each change and the rule behind it, and leave alone every phrase that already sounds like you.
6. Say what the guide is for: checking what you wrote. It is never a licence for me to write, or send, in your name.

## Output Format
```markdown
# Writing Voice Guide
Built from: [number] pieces you sent between [dates] | Kept in: [memory / Project name / your own file]
## How I write
| Trait | My pattern | Example from my own text |
|---|---|---|
| Opening | [pattern] | "[quote]" |
| Asking for something | [pattern] | "[quote]" |
| Signing off | [pattern] | "[quote]" |
| Sentence length | [range] | "[quote]" |
## Words I use and words I never use
| I use | I never use |
|---|---|
| [word or phrase] | [word or phrase] |
## AI-tell checklist
- [ ] [pattern]: [what it looks like in a message]
## Before and after
| Before | After | Why |
|---|---|---|
| [line] | [line] | [rule] |
## Decision
[Your name] confirms the never-use list and the checklist by [date], and reviews the guide after [number] runs.
```

## Done When
- Every trait has an example quoted from your own sent writing.
- The never-use list is confirmed by you, not inferred alone.
- The before and after shows each change with its reason.
- The guide is saved where later checks can reach it.

## Quality Bar
- Only your own writing goes in; never messages other people sent you.
- The checklist describes patterns in your terms; it does not copy the source page.
- A rule that would change your natural phrasing is dropped.
- An informal habit is your style, not a fault to correct.
- The guide checks your writing and never replaces it; you write every word.

## Next
Run reach-talking-points (Talking Points) to line up the substance of one message before you write it.

## About the makers

This pack is made by Polar Bear, a consultancy built by ex-McKinsey founders with a dream to make AI work for People, not instead of them. We help our clients build people systems and AI-first ways of working, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
