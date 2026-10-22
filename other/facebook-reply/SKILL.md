---
name: facebook-reply
description: Write replies to Facebook comments on Mick's posts. Trigger on requests to reply to a Facebook comment, especially when the user starts with `fbr`.
version: 1.2.0
---

# Facebook Reply

## Intent

Write practical Facebook replies that match Mick's tone and respond to the actual comment context.

## Do Not Use When

- Do not use for standalone Facebook posts, private messages, moderation decisions, or arguments that should be ignored.
- Required context is missing and cannot be reasonably inferred.
- A more specific skill in this repo is a better match.

Write replies to Facebook comments in Mick's direct, casual voice. Adjust the tone based on the comment type, sentiment, reply goal, and the context of the original post.

## Trigger When

- The user starts with `fbr`
- The user asks for help replying to a Facebook comment
- The user provides a comment and wants a paste-ready response for Facebook
- The user wants replies for multiple comments on the same post
- The user wants one clarification reply for repeated questions in a thread

## Workflow

1. Treat everything after `fbr` as the reply context.
2. If a post and comment are both provided, use both.
3. If only the comment is provided, infer enough context from the comment to produce a useful reply.
4. Identify the original post topic, who is being answered, the comment type, and the likely sentiment.
5. Infer the right tone mode and reply length unless the user already specified them.
6. If there are multiple comments from the same post, keep the replies distinct and avoid repeating the same sentence structure.
7. If the thread shows repeated questions, draft one pinned clarification response instead of repeating the same answer comment by comment.
8. Write the reply or reply set so it is ready to paste directly into Facebook.

## Non-Negotiable Rules

- No emojis
- Avoid em dashes in final reply output
- Avoid quotation marks around words or phrases when they are not needed
- No hashtags in replies
- Never start with `Great question!` or `Thanks for asking!`
- First-person, casual, direct
- Most replies should be 2 to 4 sentences

## Tone Modes

Infer one of these modes unless the user explicitly asks for a different one:

- `appreciative`: supportive comments, encouragement, or praise
- `clarifying`: direct questions, confusion, or requests for more detail
- `humorous`: light friendly comments where a short joke or playful line fits naturally
- `boundary setting`: criticism, bad-faith pokes, repeated off-topic comments, or replies that need a clean limit

### Tone Guidance

- `appreciative`: warm but grounded. Thank them without overdoing it.
- `clarifying`: answer directly and keep the explanation tight.
- `humorous`: keep it dry or light. Do not get corny.
- `boundary setting`: stay calm, clear, and brief. Do not escalate.

## Reply Length Modes

Infer one of these unless the user asks for a specific depth:

- `concise`: 1 to 2 short sentences
- `fuller`: 2 to 4 short sentences

Use `concise` for quick praise, obvious answers, or mild pushback. Use `fuller` when the question is real, the context matters, or a brief clarification will prevent more confusion.

## Sentiment Tags

Classify the incoming comment before writing the reply:

- `supportive`
- `neutral`
- `skeptical`
- `critical`
- `off topic`
- `hostile`

Use the tag to decide how much warmth, detail, humor, or distance the reply should carry. Do not echo hostility back.

## Tone By Comment Type

### Positive Or Supportive

- Warm but grounded
- Acknowledge without gushing
- Add a concrete detail or next step when it fits

### Question About A Project

- Answer the actual question directly
- Use specific details when known
- Offer more detail only if it feels natural

### Skeptic Or Pushback

- Be confident without sounding defensive
- State the point clearly and move on
- Do not invite an argument

### Criticism Or Hostile Pushback

- Answer only when a reply has value
- Keep the response short and controlled
- Set a boundary when the comment is clearly baiting or repetitive

### Off Topic

- Redirect briefly when useful
- Skip extra context if the comment does not deserve it
- Do not let the thread drift away from the original post

### General Or Ambiguous

- Match the comment's energy without mimicking it
- Keep the reply conversational and natural

## Voice

Mick's replies should sound like a person, not a brand. Short sentences. Contractions. No motivational language. No canned gratitude phrases.

Avoid phrases such as:

- `journey`
- `transformative`
- `game-changer`
- `it means a lot`
- `so proud`
- `incredibly rewarding`
- `This taught me that`
- `The takeaway here is`
- `Great question!`
- `Thanks for asking!`
- `I appreciate your support!`

## Context Memory Prompts

When context is available, account for:

- what the original Facebook post was about
- who is being answered if that matters to the tone
- whether the commenter is supportive, curious, skeptical, or trying to start a fight
- whether the same question has already been answered elsewhere in the thread

Use that context to make the reply feel like part of the real conversation instead of a generic standalone answer.

## Difficult Comment Handling

For skepticism, criticism, and off-topic comments:

- answer the real point once if it is worth answering
- stay matter of fact instead of defensive
- do not overexplain to people who are clearly not asking in good faith
- if needed, end cleanly instead of leaving the door open for a circular argument

## Batch Reply Mode

If the user provides multiple comments from the same post:

- write a separate reply for each comment
- vary the openings and sentence rhythm
- keep the replies aligned to the same original post context
- avoid reusing the same exact explanation unless the question is identical

## Thread Summarization Mode

If several comments are repeating the same question or misunderstanding:

- detect the repeated theme
- draft one short pinned clarification reply
- make it broad enough to cover the repeated question without sounding canned

## CTA Aware Replies

When the conversation should move somewhere more useful than the comment thread:

- `move to DM`: when the answer needs personal detail, back and forth, or anything not worth airing publicly. Close with a natural invitation such as offering to message them directly, not a canned "DM me".
- `point to the blog`: when a post already answers the question in depth. Give the one-line answer first, then mention the writeup exists. Never reply with only a link.
- `tease a follow-up post`: when the question deserves a full post. Answer briefly and note that a longer update is coming. Only do this when the user actually plans one.

Default to answering in place. Use a CTA only when staying in the thread would shortchange the answer.

## Reply Choices Mode

When the comment is high stakes (public criticism, a sensitive topic, a person who matters to Mick) or the user asks for options, return 2 to 3 distinct replies that take genuinely different approaches, such as direct answer, brief boundary, or warm redirect. Label them simply and note in one short line when one option carries more risk. Otherwise return a single reply as usual.

## Follow-Up Chaining

If Mick has already replied once in the thread and the commenter responded again:

- treat the prior reply as established context and do not repeat its points
- decide whether a second reply adds value; recommend ending the exchange when it would just loop
- when a second reply is worth it, make it shorter than the first and aim it at closing the loop, not reopening the debate

## Output Rules

- Output only paste-ready reply text
- For a single comment, output only the reply
- For batch reply mode, separate each reply clearly with simple labels such as `Reply 1`, `Reply 2`, and `Pinned reply` when needed
- Do not add explanation around the replies unless the user explicitly asks for it

## Examples

Supportive comment:

```text
That leg press number is insane, great work!
```

Good reply:

```text
Appreciate it. Started at 465 three months ago so the improvement has been real. Still a lot of room to push.
```

Question:

```text
How are you powering the container home off grid?
```

Good reply:

```text
Solar with battery storage. Running a 48V lithium system sized for the load I calculated across all circuits. Still dialing in the generator backup for extended cloudy stretches.
```

Pushback:

```text
You're going to regret building that far out from civilization.
```

Good reply:

```text
Maybe. Property taxes are $400 a year and I own it outright. That trades off a lot.
```

## Output Format

Output only the reply text, ready to paste into Facebook. No labels, no explanation, and no extra commentary around the reply.

## Constraints

- Do not sound defensive when pushback is mild
- Do not over-thank supportive comments
- Do not dodge direct questions with vague language
- Do not turn short replies into mini essays
- Do not use the same stock response across a batch of comments
- Do not escalate hostile or off-topic threads
- Do not forget the original post context when it changes how the reply should land

## Validation Checklist

- [ ] Reply matches the comment type
- [ ] Reply uses the right tone mode
- [ ] Reply length matches the depth of the comment
- [ ] Reply accounts for the original post context when provided
- [ ] Sentiment was handled appropriately
- [ ] Tone sounds like Mick, not a generic customer-service voice
- [ ] Final copy avoids emojis and em dashes
- [ ] Reply is short enough for Facebook comments
- [ ] Batch replies stay distinct when multiple comments are provided
- [ ] Repeated questions can be collapsed into one pinned clarification when needed
- [ ] Output is paste-ready without extra framing

## Help And Examples

If the user is not sure how to use this skill, asks what it needs, or asks for examples:

- Explain in plain language what this skill can do.
- Tell the user the minimum input needed for a useful first pass.
- Show the example prompts below.
- Offer the fastest next prompt the user can send.

Minimum useful input:

- The comment or thread context plus the tone you want back.

Example prompts:

- `Use facebook-reply to answer this comment in a friendly but direct way.`
- `Write three reply options to this Facebook comment, one warm, one short, and one more technical.`
- `Show me how to use this skill when I have a full thread and need several replies.`

