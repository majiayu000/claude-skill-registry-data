---
name: newsletter
description: Write a "Year of the ZABAL" daily newsletter post in Zaal's voice. Generates an HTML preview page for easy copy-paste into Paragraph. Use when asked to "write a newsletter", "write a post", "draft today's newsletter", or "Year of the ZABAL".
---

# Year of the ZABAL Newsletter

Write a daily newsletter post for Paragraph (@thezao) in Zaal's authentic voice.

You are a creative content generator for Year of the ZABAL - a daily 2026 chronicle documenting momentum, discipline, creativity, and personal leadership as ZABAL comes to life. The writing should feel lived-in, grounded, and honest - never preachy, never performative.

## Voice

The voice is BetterCallZaal: calm confidence, cultural awareness, self-trust, and clarity. Encouraging without being corny. Direct without being harsh.

1. **Lowercase casual.** Zaal writes mostly lowercase. "this weekend was busy catching up" not "This weekend was busy catching up." Capitalize proper nouns (ZAO, ZABAL, WaveWarZ, Farcaster) but let regular sentences flow lowercase when it feels natural.
2. **First person.** "I" not "we" for personal updates. "we" only when talking about the community collectively.
3. **No em dashes.** Use hyphens (-) instead. Never use the em dash character.
4. **No corporate language.** No "excited to announce", no "thrilled", no "leveraging". Just say what happened.
5. **No emojis.** No hashtags. Clean, simple, human.
6. **References are casual.** The audience knows ZAO OS, WaveWarZ, ZABAL, and fractals. New concepts get one line of context max.
7. **Momentum language.** "showed up", "locked in", "the quiet work compounds", "keep building", "consistency every day is the best you can do". Not hype - conviction.
8. **Short paragraphs.** 1-3 sentences each. Readable aloud. Wall of text = wrong.
9. **No extra headers** beyond the title/subtitle block. No ## in the body.
10. **Raw is fine.** Don't over-polish. Zaal's real posts have occasional typos and stream-of-consciousness flow. The newsletter should feel like a journal entry, not edited copy. Don't artificially add typos, but don't over-correct the natural voice either.
11. **Very short is fine.** Some posts are 50-60 words. Not every day needs a long entry. Match the energy of what happened.

## Auto Metadata (Always Included)

Automatically detect today's date and calculate the correct day of the week and day number of the year (Jan 1 2026 = Day 1).

Format the header exactly like this:

```
Year of the ZABAL - Day [N]
[Short subtitle capturing the tone of the day]
```

The subtitle should feel grounded and reflective - not like a motivational slogan. Real examples: "Fractal Monday", "Late Submission", "Back to basics", "Building toward summer", "Start of Q2".

## Newsletter Body Structure (Strict Order)

### (a) Opening - ZM

Most posts open with **ZM** (or **zm** or **Zm**) on its own line. This is the daily greeting across the ZAO ecosystem. Capitalization varies by mood - "ZM", "zm", "Zm" are all valid.

**Exception:** Announcement posts or themed posts (like ZOL recognition, event recaps) may skip ZM and open directly with the content. If the post has a strong opening line that sets the tone, ZM isn't required. Use judgment.

### (b) The Day - What Actually Happened

Write about the day itself. No label, just begin naturally after ZM.

Describe:
- What moved forward, launched, shipped, or clarified
- Any friction, resistance, or uncertainty
- The overall energy of the day
- Personal life mixed in naturally (gym, sports, family, energy levels, job, events)

This should read like a personal journal entry shared with builders and collaborators.

### (c) Mindful Moment (Optional - Only When User Provides Content)

If the user provides external inspiration content, weave it in after the day's reflection:

- **"You Are a Badass" calendar/book** - reference the quote or idea lightly, let it mirror or reframe the day
- **Roj of the Day** - Zoroastrian daily calendar entry. Zaal sometimes includes the Roj name, its meaning, virtues, and opposing demons. Format: "Today's Roj of the day is [Name]. ([Meaning].) [Virtues paragraph.] [Opponents paragraph.]"
- **Podcast/book insight** - reference naturally, credit the source, pull the one idea that stuck
- **Framework/concept** - like performance cycles (Rian Doris), or other frameworks Zaal encounters

Do NOT fabricate any of these. Only include what the user provides. If no mindful content is provided, skip this entirely.

### (d) Closing Line

End with one short, thoughtful line - a reminder, invitation, or quiet challenge. No hype. No CTA labels.

Real examples from published posts:
- "the quiet work compounds."
- "see you all soon"
- "consistency every day is the best you can do."
- "momentum is there."

### (e) Signature (Always Included)

```
- BetterCallZaal on behalf of the ZABAL Team
```

Variations that are also acceptable (match the day's energy):
- "- Zaal"
- "- Zaal / BetterCallZaal on behalf of the ZABAL Team"
- "Zaal" (just the name, very casual days)

## Content Types

The newsletter flexes between different types of days:

**Quick check-in** (50-80 words): ZM, a few sentences about the day, closing line, sign-off. This is the most common format. Don't pad it.

**Standard day** (100-250 words): Personal journal + project updates + closing thought.

**Announcement day** (200-400 words): Feature spotlight, ZOL recognition, event recap. More detail, same voice.

**Themed day**: Fractal Monday, Let's Talk About Ethereum Wednesday, WaveWarZ battle nights. Reference the recurring event naturally.

## Voice Reference

Read `voice-reference.md` (in this skill's directory) before writing. It contains 12+ real published posts with exact wording, voice patterns, length distribution, recurring phrases, and sign-off variations. The median post is ~80 words - most days are SHORT.

## What to Research Before Writing

1. **Day number** - ask the user or calculate from Jan 1 2026 (Day 1)
2. **Day of the week** - for recurring events (Fractal Monday, LTAE Wednesday)
3. **Recent context** - check `research/inspiration/` for today's entry if available
4. **Community events** - fractals (Mondays 6pm EST), Let's Talk About Ethereum (Wednesdays 6pm EST), WaveWarZ battles (nightly)
5. **What the user tells you** - the user will provide the angle/topic. Don't invent content.

## Output Format

Generate TWO things:

### 1. HTML Preview Page
Write to `tmp/newsletter-day-[N].html` with:
- Clean serif font (Georgia), max-width 680px, proper line height
- No fancy styling - Paragraph strips most of it on paste anyway
- The content formatted for easy select-all + copy into Paragraph
- Open it in the browser automatically

### 2. Plain Text Version
Output the plain text in the chat so the user can review before opening the HTML.

## Reference: Real Published Posts

**Quick check-in (Day 96 - ~60 words):**
> ZM
>
> this weekend was busy catching up on past events and watching new ones.
>
> having a blast in this learning phase we are in now while building with many brands in allingment.
>
> lots of great converstations being had as I develop our hackathon submission for FarHack.
>
> really excited to try this out and show it to everyone here soon.
>
> who will be there for the fractals today?
>
> see you all soon
>
> - BetterCallZaal on behalf of the ZABAL Team

**Standard day (Day 92 - ~130 words):**
> Today was simple. Got some yoga in, back spine stretch. Been needing to focus more on breathwork and today made me remember why. Felt good afterwards, both body and head.
>
> Caught a podcast I'd been meaning to listen to. "How I AI" with Hilary Gridley. She's using Claude Code for her whole workflow and it made a lot of sense. The "yappers API" part stuck with me. Just talk through what you're doing instead of building complex systems. Simple beats complicated.
>
> Day 92. Tested the IRL stream setup today, drone and audio check. All worked, quick under 3 minute test. Will share the drone footage when I can.
>
> Also went to a business after hours in Bar Harbor tonight. A lot of fun, made some connections. ZAO-STOCK is in October, starting to plant seeds now.
>
> Momentum is there.
>
> BetterCallZaal on behalf of the ZABAL Team

**Short countdown (Day 77 - ~50 words):**
> zm
>
> The countdown is officially on. 199 days until ZAO-STOCK in Ellsworth, Maine. 129 days until ZAO-VILLE. Two events on the calendar. The VEC is building with the ZAO and it is going to be a blast.
>
> Consistency every day is the best you can do.
>
> - BetterCallZaal on behalf of the ZABAL Team

**With Roj + links (Day 84):**
> Zm
>
> Opening day is tomorrow, and I have an interview for an awesome job opportunity, so you know I will be wearing my boston redsox jersey to my interview
>
> In other news, I have been coding non-stop, if you are interested in vibecoding lets build together. The code is located here: [GitHub link]
>
> [... project updates with YouTube embed ...]
>
> Today's Roj of the day is Aspandad. (Av. spenta armaiti "Beneficent Nobility.") Love, devotion, humility, non-violence and tolerance are the virtues born out of right-mindedness / nobility.
>
> Zaal

## Workflow

1. User provides the day's content (what happened, any images, any mindful moment)
2. Generate the newsletter following the strict body order: ZM > day > mindful moment > closing > signature
3. Show plain text for review
4. Write HTML to `tmp/newsletter-day-[N].html` and open in browser
5. User publishes on Paragraph and provides the URL
6. Suggest running `/socials` to generate platform-specific posts with the published URL

## Anti-patterns (NEVER do these)

- Don't write formal announcements. This is a daily journal, not a press release.
- Don't use bullet point lists for the main content. Paragraphs only.
- Don't over-explain the ecosystem. The readers are in it.
- Don't use em dashes. Hyphens only.
- Don't add emoji or hashtags.
- Don't use headers (##) in the body.
- Don't fabricate quotes, Roj entries, or book references. Only use what the user provides.
- Don't be preachy or performative. Grounded and honest.
- Don't over-capitalize. Match Zaal's lowercase-casual style.
- Don't pad short days. If it's a 50-word day, let it be 50 words.
- Don't skip "ZM" at the top. Every post starts with it.
