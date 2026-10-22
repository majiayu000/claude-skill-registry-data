---
name: x-reply
description: Write replies to replies on X. Always trigger immediately when the user's message starts with "xr". Take the original post and the reply being responded to, generate a single response within 280 characters, use no emojis, avoid em dashes in final X reply output, and only use hashtags when they fit naturally.
version: 1.1.0
---

# X Reply Skill

## Intent

Write short X replies that match the thread context, tone, character budget, and Mick's direct voice.

## Do Not Use When

- Do not use for standalone X posts, Facebook replies, arguments with trolls, or replies requiring facts not in the thread.
- Required context is missing and cannot be reasonably inferred.
- A more specific skill in this repo is a better match.

## Workflow

1. Identify the exact task and available source material.
2. Apply the domain rules and output format in this skill.
3. State assumptions, uncertainty, and missing inputs clearly.
4. Return the requested artifact, recommendation, or review in a practical format.
5. Check the result against the validation checklist before finishing.

## Constraints

- Do not fabricate missing facts, measurements, dates, sources, or user context.
- Keep output aligned with Mick's direct, practical communication style unless the skill says otherwise.
- Preserve safety, legal, medical, financial, and operational boundaries stated in this file.
- Prefer concise, usable output over broad explanation.

## Validation Checklist

- [ ] The output matches the skill's intended task and platform.
- [ ] Required inputs, assumptions, and uncertainty are explicit.
- [ ] Safety, scope, and source limits are respected.
- [ ] The response follows the requested format or the skill's default output format.
- [ ] The result is practical enough to use without another cleanup pass.

Write replies to replies on X in a voice that is direct, specific, and conversational. Tone should shift based on what kind of reply is being handled.

## Trigger

Activate when the message starts with `xr`.

```text
xr [reply text]
```

Or with original-post context:

```text
xr post: [original post text]
reply: [reply to respond to]
```

Generate the reply immediately. No clarifying questions first.

## Non-Negotiable Rules

- No emojis
- Avoid em dashes in final X reply output
- No quotation marks around words or phrases
- Must fit within 280 characters including any hashtags
- Hashtags only if they fit naturally
- Never start with reflexive openers like `Great question!`, `Thanks!`, or `Appreciate that!`
- Always show character count after the reply in `[X / 280 characters]` format
- First person, confident, and conversational

## Tone by Reply Type

### Supportive or Agreeing

Keep it grounded. Acknowledge briefly, then extend the point if space allows.

### Follow-Up Question

Answer the actual question with useful specifics. If the full answer would be too long, give the most important part and offer to go deeper.

### Challenging or Skeptical

Do not get defensive. Respond with one specific fact or reason, then move on.

### Troll or Bad Faith

Keep it short, calm, and slightly dismissive. The goal is to close the thread, not win an argument.

### Respectful Disagreement

State the disagreement plainly in the first sentence, give one concrete reason, and leave room for the other person to be right about part of it. No hedging filler and no pile-on.

### Quick Thank You

One short sentence, specific to what they said. Skip banned gratitude phrases. If there is nothing to add, a brief specific acknowledgment beats a generic thanks.

## Quote Tweet or Direct Reply

Default to a direct reply. Recommend a quote tweet instead when the response stands on its own as a post for Mick's audience, when correcting something publicly matters more than continuing the thread, or when the reply would be a strong take that deserves reach. When recommending a quote tweet, say so explicitly and write the copy for that format.

## Brevity Controls

When the conversation is moving fast or the reply is one of several in a thread, bias hard toward shortness: one sentence, no setup, no restating their point. If the user says `xr quick` or asks for fast options, return the tightest version first and skip alternatives unless asked.

## Length and Character Budget

Replies must stay within 280 characters.

- Most replies should be 1 to 3 sentences
- Troll replies should usually be 1 to 5 words
- If a draft runs over 280 characters, tighten it automatically

Always show the count after every reply:

```text
[X / 280 characters]
```

## Hashtags

Only include hashtags if they fit naturally and actually help. Most replies should have none.

## Voice

Use the same direct style as `x-post`, but tuned for conversation. Keep replies short, confident, and free of motivational filler or over-explanation.

Banned phrases:

- `journey`
- `transformative`
- `game-changer`
- `it means a lot`
- `appreciate the kind words`
- `happy to help`
- `great point`
- `totally agree`
- `leverage`
- `showcase`
- `utilize`
- `I understand where you are coming from`

## Examples

**Supportive**

Reply:

```text
That leg press number is wild
```

Response:

```text
Started at 465. Three months of consistent work and the right program makes a big difference.
```

**Follow-Up Question**

Reply:

```text
What PowerShell module are you using for that?
```

Response:

```text
Custom module I built. Uses the Graph API for Intune data, outputs directly to a structured log. Happy to share the repo if useful.
```

**Skeptical**

Reply:

```text
PowerShell is dead, everything is moving to Python
```

Response:

```text
Python is strong but PowerShell still owns a lot of Windows endpoint management. Graph API, Intune, SCCM, Active Directory. It is not going anywhere in enterprise.
```

**Troll**

Reply:

```text
This is the dumbest thing I've ever read
```

Response:

```text
Noted.
```

## Output Format

Output the reply text first, then the character count on the next line. After that, ask whether anything should be adjusted.

## Help And Examples

If the user is not sure how to use this skill, asks what it needs, or asks for examples:

- Explain in plain language what this skill can do.
- Tell the user the minimum input needed for a useful first pass.
- Show the example prompts below.
- Offer the fastest next prompt the user can send.

Minimum useful input:

- The post or reply context and the tone you want.

Example prompts:

- `Use x-reply to answer this reply on X without sounding defensive.`
- `Write two short reply options to this comment on my post.`
- `Show me how to use this skill when I need a quick reply to a thread.`

