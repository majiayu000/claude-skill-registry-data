---
name: reader-response-writer
description: "Drafts a thoughtful, on-brand response to a reader letter, subscriber email, or audience complaint — matching the publication's voice while addressing the reader's specific concern or question."
status: stable
category: newsletter
subcategory: writing
version: 1.0
eval_score: 4.50
tags: [newsletter, reader-response, audience, communication, writing, community]
---
# Reader Response Writer

## What This Skill Does
Drafts a thoughtful, on-brand response to a reader letter, subscriber email, or audience complaint — matching the publication's voice while addressing the reader's specific concern or question.

## When To Use This Skill
- A reader has written in with a question, correction, compliment, or complaint and you need to reply promptly and professionally
- You receive a high volume of reader emails and need to draft responses efficiently without sounding templated
- A reader has raised a sensitive issue — a factual error, an offensive passage, a cancellation threat — and the response needs to be carefully worded
- You want to turn a reader interaction into a relationship-building moment that increases loyalty and reduces churn

## What You Need To Provide
**Required:** The reader's original message (full text or a close summary); the publication name and a brief description of its voice and tone (e.g., "warm and informal," "authoritative but approachable," "journalistic and direct").

**Optional:** The reader's name and how they should be addressed; the context of what prompted the message (which edition, article, or episode they are responding to); any factual background the response needs to account for (e.g., "the statistic they flagged was actually correct — here is the source"); the desired outcome (retain the subscriber, acknowledge and move on, invite further dialogue, issue a correction); whether the response will be private (email reply) or public (published in a letters section or read on air).

## How the Assistant Approaches This
1. **Reads the reader's message for both content and emotional register.** Identifies what the reader is asking for (information, acknowledgment, correction, an apology) and how they are feeling (frustrated, curious, appreciative, hostile). The response must address both — answering the question while matching the emotional context.

2. **Matches the publication's voice, not the reader's.** If a reader writes angrily, the response does not mirror the anger — it responds in the publication's established voice. If the publication is warm and informal, the response is warm and informal even when addressing a complaint. Consistency of voice builds trust.

3. **Addresses the specific issue directly.** No generic "thank you for your feedback" filler. The response references the reader's exact point, demonstrates that it was read and understood, and provides a substantive answer. If the reader is right, the response acknowledges it. If the reader is wrong, the response corrects respectfully with evidence. If the issue is ambiguous, the response says so honestly.

4. **Calibrates length to the situation.** A simple compliment gets a warm 2-3 sentence reply. A factual correction gets a thorough response with the source. A cancellation threat gets a response that acknowledges the concern, addresses it, and makes one genuine offer — without begging. The response is as long as it needs to be and no longer.

5. **Closes with a forward-looking note.** Every response ends with something that keeps the relationship open — a question, an invitation to stay in touch, a note about upcoming content that relates to the reader's interest. This is not a sales pitch; it is a genuine gesture of continued engagement.

## Output Format

A complete, ready-to-send reply. Opens with a greeting using the reader's name (if provided). Body addresses the reader's message directly. Closes with a forward-looking note and sign-off. Length varies by context: 50-100 words for simple acknowledgments, 150-300 words for substantive replies, up to 400 words for sensitive or complex situations. Tone matches the stated publication voice throughout.

## Quality Criteria
- [ ] The response references the reader's specific point — not a generic acknowledgment
- [ ] The publication voice is maintained throughout, regardless of the reader's tone
- [ ] If the reader raised a factual issue, it is addressed with evidence — not deflected or ignored
- [ ] The length is appropriate to the complexity of the reader's message — no 300-word reply to "Great edition this week!"
- [ ] The closing line is forward-looking and genuine — not a sales pitch or a canned sign-off
- [ ] If the reader is upset, the response acknowledges their frustration before addressing the substance
- [ ] The response could be sent as-is without editing — correct grammar, appropriate formality, no placeholder text

## Example

### Input
**Reader message:**
"Hi — I've been a subscriber since your early days and I really value what you do. But I have to say, the last three editions have felt rushed. The analysis sections are shorter, the sourcing is thinner, and last week's piece on trade policy had two factual errors that I noticed (the tariff rate you cited for steel imports was from 2021, not 2024, and the EU commissioner you named left that role in January). I'm not trying to be difficult — I want this newsletter to stay great. But if the quality keeps slipping, I'll need to reconsider my subscription."

**Publication:** A paid weekly newsletter on international trade policy. Voice: authoritative, precise, appreciative of engaged readers.

**Context:** The editor confirms that both factual errors the reader identified are real. The last three editions were produced during a period of staff illness.

**Desired outcome:** Retain the subscriber. Acknowledge the errors honestly. Signal that quality is being restored.

### Output

Hi Marcus,

Thank you for writing — and for being specific. You are right on both counts. The steel tariff figure was from 2021, not the current rate, and the EU commissioner reference was outdated. We have corrected both in the archived edition and will publish a correction note at the top of this week's issue.

I will be honest with you: the last three editions were produced under difficult circumstances, and the quality did not meet our standard. That is not an excuse — it is context. You should expect the same level of rigour from every edition regardless of what is happening behind the scenes, and we fell short.

Here is what we are doing about it. We have reinstated our two-person fact-check review for every edition, effective immediately. The analysis sections will return to their usual depth starting this week — the trade policy piece on rare earth export controls will be the first test of that commitment.

Subscribers like you — the ones who catch errors and tell us — are the reason this newsletter stays honest. I genuinely appreciate it.

I hope you will give this week's edition a read and let me know if it meets the bar. Your feedback is the most useful quality check we have.

Best,
The Trade Briefing Team

## Known Limitations
- The assistant cannot verify the factual claims in the reader's message. If a reader says "you got this wrong," the skill takes the user's guidance on whether the reader is correct. Without that context, the response will acknowledge the concern without confirming or denying the error.
- For legally sensitive situations — defamation claims, threats of legal action, requests for retraction — this skill produces a first draft only. Legal review is essential before sending any response that could have legal implications.
- The skill matches publication voice based on the description provided, but it cannot replicate a specific editor's personal writing style from a brief description alone. For high-fidelity voice matching, provide a sample of previous reader responses as a style reference.

## Related Skills
- [audience-feedback-summarizer](../../strategy/audience-feedback-summarizer/SKILL.md) — summarize multiple reader messages before responding to individual ones
- [edition-writer](../edition-writer/SKILL.md) — write the next edition informed by reader feedback
- [re-engagement-email-writer](../re-engagement-email-writer/SKILL.md) — write a re-engagement email for subscribers at risk of churning
