---
name: social-engagement-responder
description: >
  Generates contextual replies to comments, mentions, and DMs on social posts.
  Classifies engagement as lead signal, customer question, partnership opportunity,
  or troll/spam. Uses brand voice from agency.config.json.
tags: [social-media, engagement, replies, community]
---

# Social Engagement Responder

Generates contextual, on-brand replies to social media engagement (comments, mentions, DMs, tags). Classifies each interaction for CRM routing and prioritizes lead signals.

## Prerequisites

- `agency.config.json` populated (outreach tone, services, case studies)
- Engagement data: the comment/mention/DM text, platform, context (original post if available)

## Phase 0: Intake

Read `agency.config.json`:
- `agency.name`, `agency.founder` -- for sign-offs and personal touches
- `outreach.tone` -- voice baseline
- `outreach.banned_phrases` -- never use in replies
- `services[]` -- for contextual service mentions
- `case_studies[]` -- for proof points when relevant

Accept parameters:
- `engagement` -- (required) object containing:
  - `platform` -- `linkedin`, `twitter`, `instagram`, `reddit`
  - `type` -- `comment`, `mention`, `dm`, `tag`, `reply`
  - `text` -- the engagement text
  - `author` -- name/handle of the person
  - `context` -- (optional) the original post or thread context
  - `author_profile` -- (optional) brief profile info (title, company, follower count)
- `batch` -- (optional) array of engagement objects for bulk processing
- `auto_classify` -- boolean, classify without generating reply. Default: `false`

## Phase 1: Classification

Classify each engagement into one of these categories:

| Category | Signals | Priority | Action |
|----------|---------|----------|--------|
| **LEAD_SIGNAL** | Asks about services, pricing, availability; mentions pain points; DMs asking for help | HIGH | Reply + flag for CRM |
| **CUSTOMER_QUESTION** | Existing client asking for support, updates, or clarification | HIGH | Reply + flag for account team |
| **PARTNERSHIP_OPPORTUNITY** | Collaboration offers, co-marketing, referral partner signals | MEDIUM | Reply + flag for founder |
| **GENUINE_ENGAGEMENT** | Thoughtful comments, shares experience, adds to discussion | MEDIUM | Reply to nurture |
| **SIMPLE_REACTION** | "Great post!", "Agree!", emoji-only, basic compliments | LOW | Short thank-you or skip |
| **TROLL_SPAM** | Hostile, irrelevant, promotional spam, bot-like | IGNORE | Do not reply, flag for review |

Classification output:
```json
{
  "category": "LEAD_SIGNAL",
  "confidence": "HIGH",
  "reasoning": "Asked about Shopify development pricing and mentioned they need help with their store",
  "suggested_action": "Reply with value, DM to continue conversation",
  "crm_flag": true
}
```

## Phase 2: Reply Generation

### LEAD_SIGNAL replies
- Acknowledge their need specifically
- Provide one piece of genuine value (tip, insight, quick observation)
- Soft pivot to conversation ("Happy to share more, DM me?" or "We actually helped a brand with exactly this")
- Never hard pitch in a public reply
- If DM: be more direct, offer a quick call or audit

### CUSTOMER_QUESTION replies
- Answer directly and helpfully
- If complex, acknowledge + offer to follow up via DM/email
- Reference their specific situation if known
- Keep professional but warm

### PARTNERSHIP_OPPORTUNITY replies
- Express interest without over-committing
- Ask a qualifying question ("What kind of collaboration are you thinking?")
- Offer to take it to DM/email

### GENUINE_ENGAGEMENT replies
- Match their energy level
- Add value to the conversation (expand on a point, share a related insight)
- Ask a follow-up question to deepen engagement
- Keep it conversational, not corporate

### SIMPLE_REACTION replies
- Short acknowledgment: "Thanks!", "Appreciate that", "Glad it resonated"
- Or skip entirely if volume is high (flag as "no reply needed")

### TROLL_SPAM replies
- Do not reply
- Flag for manual review
- If borderline, respond once with facts, then disengage

## Phase 3: Platform-Specific Formatting

| Platform | Reply Style | Length |
|----------|------------|--------|
| LinkedIn | Professional, can be 1-3 sentences, use their name | 20-80 words |
| Twitter | Casual, punchy, match their tweet energy | Under 280 chars |
| Instagram | Friendly, use their handle, casual | 10-40 words |
| Reddit | Helpful, detailed if they asked a question, no self-promo | 30-200 words |

## Phase 4: Quality Check

1. **Banned phrase scan**: Check against `outreach.banned_phrases`
2. **Self-promo check**: Public replies should not read as ads. Lead with value.
3. **Tone match**: Reply tone should match the engagement's tone (serious reply to serious question, casual to casual)
4. **Platform limits**: Twitter replies under 280 chars
5. **No emoji overload**: Max 1-2 per reply

## Phase 5: Output

Return structured JSON:

```json
{
  "engagements": [
    {
      "platform": "linkedin",
      "type": "comment",
      "author": "Priya Mehta",
      "original_text": "This is really insightful. We've been struggling with our Shopify product pages for months.",
      "classification": {
        "category": "LEAD_SIGNAL",
        "confidence": "HIGH",
        "reasoning": "Mentions struggling with Shopify product pages, matches our CRO service",
        "crm_flag": true
      },
      "reply": "Priya, product pages are where most D2C brands leave the most revenue on the table. One quick win: make sure your above-the-fold shows social proof + a clear size/variant selector without scrolling. Happy to share a few more specifics if useful, feel free to DM.",
      "follow_up_action": "If she DMs, share Kibi Sports case study and offer a free CRO audit",
      "word_count": 47
    }
  ],
  "summary": {
    "total_processed": 12,
    "lead_signals": 2,
    "customer_questions": 1,
    "partnership": 0,
    "genuine_engagement": 5,
    "simple_reactions": 3,
    "troll_spam": 1,
    "replies_generated": 8,
    "skipped": 4
  },
  "generated_at": "2026-03-13T10:00:00Z"
}
```

## Phase 6: CRM Handoff

For LEAD_SIGNAL engagements:
- Write to CRM via `crm-writer` with: author name, platform, signal text, classification, reply sent, follow-up action
- Set lead stage = NEW if not already in CRM
- Tag source = `social_engagement`

## Example Usage

Trigger phrases:
- "Process today's LinkedIn comments and mentions"
- "Classify and reply to these Instagram DMs"
- "Handle the comments on my latest LinkedIn post"
- "Check for lead signals in this week's social engagement"
- "Draft replies for these Reddit mentions"
- "Triage my social media inbox"
