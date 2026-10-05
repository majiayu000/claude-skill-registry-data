---
name: cold-outreach
description: Research a prospect and generate a personalized cold outreach sequence. First message, two follow-ups, and a break-up message. Based on real signals from their website, not generic templates.
---

# Cold Outreach

Research a prospect company and generate a 4-message outreach sequence personalized to their specific situation. Not templates - actual personalization based on what you find.

## What this does

Three phases:

1. **Prospect Research** - Extract signals from their website, marketing activity, and context
2. **Pain Signal Identification** - Find the specific angle that will resonate
3. **Sequence Generation** - Write 4 messages: opener, follow-up 1, follow-up 2, break-up

## How to use

Pass a company URL or LinkedIn URL:

```
/cold-outreach https://empresa.com
```

Or with context:
```
/cold-outreach https://empresa.com - contacto: Ana Lopez, directora de marketing, LinkedIn: linkedin.com/in/analopez
```

## Phase 1 - Prospect Research

Collect the signals that make outreach feel personal:

**From their website:**
- What they do and who they serve
- What they are clearly investing in (design, content, ads)
- What is clearly missing or underperforming (compared to what you'd expect)
- Any recent changes (new product, rebrand, expansion)
- Tech stack signals (no pixel = cannot run ads; no analytics = flying blind)

**From search:**
- Recent news, press, blog posts
- Job postings (reveals priorities and pain)
- Social media activity (are they active? what topics?)
- Reviews or testimonials (reveals what customers value)

**From LinkedIn (if profile provided):**
- Contact's role and responsibilities
- Recent activity / posts
- Time in current role (new role = often looking to prove impact)
- Shared connections or context

## Phase 2 - Pain Signal Identification

Pick ONE primary pain angle. Not five angles - one.

The best angle is:
- Specific to them (you saw something on their site / LinkedIn)
- Connected to a business outcome they care about (revenue, leads, time)
- Something the agency can actually help with

**Angle selection:**

| Finding | Angle |
|---------|-------|
| No conversion tracking | "You're spending on [channel] with no way to measure return" |
| No Meta Pixel | "Your audience data is building in competitors' accounts, not yours" |
| Inactive social (3+ months) | "Your social presence is sending the wrong signal to new visitors" |
| No case studies | "Prospects who visit your site can't see proof - that's a closing problem" |
| Old website | "Your website is costing you credibility with every new visitor" |
| SEO competitors ranking above them | "X and Y are capturing searches you should be winning" |
| Hiring for marketing | "You're scaling marketing - this is the moment to get the foundation right" |

**What to avoid:**
- "I loved your website" (nobody believes it)
- "I noticed you could improve your SEO" (too generic)
- "We work with companies like yours" (irrelevant)
- "I wanted to reach out because..." (filler)

## Phase 3 - Sequence Generation

Generate 4 messages. Each has a different purpose.

### Message 1 - The Opener

Purpose: Get a reply. One ask. One specific observation.

Format:
```
Subject: [specific, not clickbait - max 7 words]

[Their name],

[One observation from research - something specific to them]

[One sentence connecting it to a business outcome]

[One question or one offer - not both]

[Name]
```

Rules:
- Under 80 words
- No attachment, no portfolio link in first message
- The observation must be specific enough that they think "they actually looked at my site"
- One ask only: either a question OR a link/offer, never both

Example:
```
Subject: Your Meta Pixel isn't firing

Ana,

I was looking at Empresa.com before reaching out - your Meta Pixel is installed but not firing conversion events, which means you're building audiences in Meta without knowing which visits actually convert.

Worth a 15-minute call to show you what that's costing?

Carlos
```

### Message 2 - Follow-up 1 (3-4 days after Message 1)

Purpose: Add value. Give something without asking for anything.

Format:
```
[First name],

[Reference to message 1 - don't apologize for following up]

[One piece of relevant information or insight - specific to their situation]

[Soft ask or no ask at all]

[Name]
```

Rules:
- Under 60 words
- Give value before asking again
- Can include a link to a relevant article or example (not your portfolio)

### Message 3 - Follow-up 2 (5-7 days after Message 2)

Purpose: Create mild urgency or context. Last real attempt.

Format:
```
[First name],

[One line: what you've noticed since your last message - could be something about their industry, a competitor, or a seasonal angle]

[The ask again, slightly reframed]

[Name]
```

Rules:
- Under 50 words
- Do not apologize for following up
- Do not say "I know you're busy"

### Message 4 - Break-up (7-10 days after Message 3)

Purpose: Close the loop, leave the door open. Often gets the highest reply rate.

Format:
```
[First name],

Closing this thread since I haven't heard back. No hard feelings - timing is everything.

[One line: what you'd have helped with]

If things change, you know where to find me.

[Name]
```

Rules:
- Under 40 words after the opening line
- No negativity, no guilt
- The "what you'd have helped with" line should be specific - it is your last pitch

## References

- `references/email-frameworks.md` - PAS, before/after, one-liner formats
- `references/personalization-signals.md` - what to look for per company type

## Output principles

1. One specific observation per message - never generic
2. Under 80 words for Message 1, shorter for each subsequent
3. One ask per message - never a question AND a link
4. No attachments in the sequence (unless asked)
5. Personalization must be verifiable - only include things actually found in research
6. Sequence must feel human, not automated - if it sounds like a mail merge, rewrite it
