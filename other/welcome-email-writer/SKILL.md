---
name: welcome-email-writer
description: "Writes the automated welcome email that new subscribers receive immediately after signing up, establishing the newsletter's voice, making the editorial promise concrete, and setting expectations that reduce early unsubscribes."
status: stable
category: newsletter
subcategory: writing
version: 1.0
eval_score: 4.5
tags: [newsletter, writing, onboarding, welcome-email, subscriber-retention]
---
# Welcome Email Writer

## What This Skill Does
Writes the automated welcome email that new subscribers receive immediately after signing up, establishing the newsletter's voice, making the editorial promise concrete, and setting expectations that reduce early unsubscribes.

## When To Use This Skill
- You are launching a new newsletter and need a welcome email before your first subscriber arrives
- Your current welcome email is the default platform auto-reply ("Thanks for subscribing!") and you are losing early subscribers
- You have rebranded or significantly changed editorial direction and need a welcome email that reflects the new positioning
- You are building a paid newsletter and need a welcome sequence that primes free subscribers for eventual upgrade

## What You Need To Provide
**Required:** Newsletter name and a 2–3 sentence description of what it covers and for whom; the publishing cadence (daily, weekly, etc.); the newsletter's tone and voice in your own words
**Optional:** What prompted you to start the newsletter (if personal origin helps the voice); what you want subscribers to do immediately after reading (reply, whitelist, follow on social, etc.); any paid tier details if applicable; one concrete example of the type of story or insight a subscriber can expect

## How the Assistant Approaches This
1. Opens with a brief, human acknowledgment of the subscription — not "You've been added to our list" but something that recognises the reader made a deliberate choice and honours that
2. Delivers the editorial promise in specific, concrete terms: not "we cover the media industry" but "every Monday we give you the one story the media industry spent the week avoiding"; the specificity is what converts a vague interest into an expectation the reader will look forward to
3. Sets practical expectations: cadence, typical length, what a reader should do if they miss issues (archive links, search tips), and any important logistical notes (whitelist instructions if the newsletter has deliverability issues)
4. Ends with a single, clear call to action — ideally one that invites a reply, because early replies dramatically improve deliverability by signalling to email providers that the newsletter is wanted

## Output Format
Single email, 200–350 words. Signed by name or newsletter brand voice, not a generic "The Team." Short paragraphs — maximum three sentences each — for mobile readability. No bullet lists unless the newsletter style explicitly uses them. Subject line included at the top of the output as: **Subject:** [line]

## Quality Criteria
- [ ] The editorial promise is specific enough that a reader could predict the next edition's general shape
- [ ] The email does not begin with "Welcome to [newsletter name]!" as its opening line — that is the most common and least effective opener
- [ ] There is exactly one call to action, not three
- [ ] The tone is consistent with the newsletter's voice description — a dry analytical newsletter does not get a warm effusive welcome
- [ ] Practical information (cadence, whitelisting) is present but not dominant — the email is a welcome, not an instruction manual

## Example

### Input
Newsletter: *The Long View*
Description: Weekly essay newsletter covering economic history — what past financial crises, inflations, and market panics can teach us about the present. For people who want depth over speed and are tired of hot takes.
Cadence: Weekly, Sunday mornings
Voice: Calm, authoritative, slightly contrarian. The writer is a former economic historian who left academia. Readers are professionals — finance, policy, journalism — who want intellectual rigour without the jargon.
Call to action: Reply with what you want to understand better
No paid tier currently.

### Output

**Subject:** You subscribed to something slower

Thank you for signing up — and for choosing slow.

*The Long View* arrives every Sunday morning with one essay on economic history and what it illuminates about the present moment. Not a summary of last week's news. Not a thread turned into a paragraph. A proper piece of thinking, usually 1,200–1,800 words, built on primary sources and the kind of research that doesn't fit into a 48-hour news cycle.

This week's essay goes out Sunday. In the meantime, the archive is here if you want to see what you've signed up for — I'd suggest starting with the piece on the 1970s inflation cycle, which keeps turning out to be more relevant than I'd like.

One thing that helps more than you'd expect: hit reply and tell me what you're trying to understand. Not what you want me to cover — I'm not taking assignments — but what question you're carrying around right now. I read every reply. It shapes what I write, even when I don't say so.

See you Sunday.

*— Marcus*

*P.S. If you use Gmail, drag this email into your Primary tab. It keeps the next ones from going to Promotions, which is where good things go to be ignored.*

## Known Limitations
- The welcome email can only deliver the editorial promise as well as you have articulated it in the brief — a vague description ("we cover business news") produces a vague welcome; the more specific your input, the more specific and compelling the output
- The skill does not generate full multi-email welcome sequences; it writes the single first-touch email. For a 3- or 5-email onboarding sequence, each email should be requested separately with its place in the sequence specified
- Deliverability instructions (whitelisting, Primary tab tips) are generic across email clients; if your list skews heavily toward a specific client (e.g. corporate Outlook users), specify this for tailored advice
- The "reply with a question" CTA works best for newsletters with fewer than 5,000 subscribers; above that threshold, a different CTA may be more practical to manage

## Related Skills
- [edition-writer](../edition-writer/SKILL.md)
- [re-engagement-email-writer](../re-engagement-email-writer/SKILL.md)
- [niche-positioning-brief](../../strategy/niche-positioning-brief/SKILL.md)
