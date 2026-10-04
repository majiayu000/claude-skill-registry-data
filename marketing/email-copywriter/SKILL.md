---
name: email-copywriter
description: Draft newsletter and nurture email copy with brand voice, structured sections, and conversion-focused CTAs
tags: [content, email, newsletter, nurture, copywriting, marketing]
---

# Email Copywriter

Generates newsletter editions and nurture email sequences with brand-aligned copy. Unlike `cold-email-drafter` (which handles outbound sales emails), this skill produces marketing emails: newsletters, drip sequences, onboarding emails, product announcements, and educational content emails. Applies brand voice rules from config, follows email copywriting best practices, and outputs structured email components (subject, preview, body, CTA).

## Prerequisites

- `agency.config.json` at repo root with `agency`, `outreach`, `services`, and `case_studies` sections
- Topic, purpose, or content brief for the email
- Optional: audience segment override
- Optional: existing brand voice document (from `brand-voice` skill)

## Phase 0: Intake

1. Read `agency.config.json` from the project root.
2. Extract:
   - `agency.name` -- for sender identity and sign-off
   - `agency.founder` -- for personal-tone emails
   - `agency.domain` -- for link references
   - `outreach.tone` -- voice and style constraints
   - `outreach.banned_phrases` -- phrases to exclude from all copy
   - `outreach.sign_off` -- default email signature
   - `services[]` -- for contextual mentions where relevant
   - `case_studies[]` -- for social proof blocks
   - `icp.segments[]` -- to tailor language to the target reader
3. Accept parameters:
   - `email_type` -- (required) one of: `newsletter`, `nurture`, `onboarding`, `announcement`, `educational`, `re-engagement`, `event-invite`
   - `topic` -- (required) what the email is about
   - `audience` -- target segment. Default: primary ICP segment
   - `goal` -- primary goal: `educate`, `drive-traffic`, `book-demo`, `announce`, `re-engage`, `nurture`. Default: inferred from email_type
   - `tone_override` -- (optional) override config tone: `casual`, `professional`, `urgent`, `celebratory`
   - `content_inputs` -- (optional) raw notes, data points, or content to incorporate
   - `sequence_position` -- (optional) for nurture/drip: email number in sequence (e.g., "3 of 7")
   - `cta` -- (optional) specific CTA. Default: inferred from goal
   - `word_limit` -- (optional) max body words. Default: varies by type

## Phase 1: Email Architecture

Define the structural blueprint based on email type:

**Newsletter:**
```
Subject line (max 50 chars)
Preview text (max 90 chars, complements subject)
---
Opening hook (2-3 sentences, personal or topical)
---
Section 1: Primary story/insight (100-150 words)
  - Subheading
  - Body with one key takeaway
  - Inline CTA or link
---
Section 2: Secondary content (75-100 words)
  - Quick tip, tool recommendation, or industry news
---
Section 3: Social proof or case study snippet (50-75 words)
  - Data point or result
  - Link to full case study
---
CTA block (primary action, single button)
---
P.S. line (personal note, secondary offer, or teaser for next issue)
---
Sign-off
```

**Nurture email:**
```
Subject line (max 50 chars)
Preview text (max 90 chars)
---
Opening: acknowledge where they are in the journey (2 sentences)
---
Value block: one insight or lesson (100-150 words)
  - Teach something useful, reference pain points from ICP config
---
Bridge: connect the lesson to the agency's service (2-3 sentences)
---
CTA: soft ask appropriate to sequence position
---
Sign-off
```

**Onboarding email:**
```
Subject line
Preview text
---
Welcome + set expectations (what they'll get, how often)
---
Quick win: one immediately actionable tip (50-75 words)
---
What's coming next: tease future value
---
CTA: reply with a question, complete a survey, or book a call
---
Sign-off
```

**Announcement:**
```
Subject line (urgency or excitement, no clickbait)
Preview text
---
The news: lead with the announcement (2-3 sentences)
---
Why it matters to them: frame the announcement from reader's perspective (3-4 sentences)
---
Details: specifics, dates, pricing, features (bullet points)
---
CTA: primary action (sign up, learn more, book)
---
Sign-off
```

**Educational:**
```
Subject line (curiosity or benefit)
Preview text
---
Hook: start with a question or surprising fact
---
Lesson body: teach one concept clearly (150-250 words)
  - Use numbered steps, bullets, or a mini-framework
  - Include one example
---
Application: how the reader can use this today (2-3 sentences)
---
CTA: learn more, read the full guide, or book a consultation
---
Sign-off
```

**Re-engagement:**
```
Subject line (acknowledge absence, no guilt)
Preview text
---
Opening: acknowledge it has been a while, no passive-aggression
---
Value hook: share the single most compelling thing they missed (3-4 sentences)
---
Options: give them a choice (stay subscribed with preferences, or unsubscribe gracefully)
---
CTA: re-engage action or preferences link
---
Sign-off
```

**Event invite:**
```
Subject line (event name + key benefit)
Preview text
---
What: event description (2-3 sentences)
---
Why attend: 3 bullet points of value
---
Details: date, time, format, duration, speakers
---
CTA: register/RSVP button
---
P.S.: share with a colleague who would benefit
---
Sign-off
```

## Phase 2: Subject Line Generation

Generate 5 subject line options using different approaches:

| Approach | Example Pattern |
|----------|----------------|
| Curiosity gap | "The CRO fix nobody talks about" |
| Benefit-first | "3 ways to boost your AOV this week" |
| Number-driven | "We increased conversions 34%. Here is how." |
| Question | "Is your product page costing you sales?" |
| Personal/story | "What I learned auditing 50 Shopify stores" |

**Subject line rules:**
- Max 50 characters (35-45 ideal for mobile)
- No ALL CAPS words
- No excessive punctuation (!!!, ???)
- No spam trigger words: "free", "act now", "limited time", "click here"
- Preview text must complement, never repeat, the subject line
- Test: would YOU open this? If not, rewrite.

Score each subject line:
- Curiosity factor (1-10)
- Clarity (1-10)
- Length appropriateness (1-10)
- Spam risk (low/medium/high)

## Phase 3: Body Copy Generation

Write the email body following the architecture from Phase 1.

**Copywriting rules (non-negotiable):**

1. **First sentence rule**: the opening line must earn the second line. No throat-clearing.
2. **One idea per paragraph**: max 3 sentences per paragraph
3. **Readability**: 6th-8th grade reading level. Short sentences. Simple words.
4. **Scanability**: use subheadings, bold key phrases, bullet points for lists
5. **Voice consistency**: match `outreach.tone` from config throughout
6. **Banned phrase check**: scan against `outreach.banned_phrases` and rewrite any matches
7. **CTA clarity**: one primary CTA per email, stated as a specific action ("Book your audit" not "Learn more")
8. **P.S. line**: always include one for newsletters and nurture emails; it gets disproportionate attention
9. **Social proof**: include at least one data point, testimonial, or case study reference per email
10. **Personalization tokens**: use `{{first_name}}` where appropriate, never more than twice

**Word count targets by type:**

| Email Type | Body Words | Total Words (incl. subject, preview, PS) |
|------------|-----------|------------------------------------------|
| Newsletter | 300-500 | 350-550 |
| Nurture | 150-250 | 200-300 |
| Onboarding | 150-200 | 180-250 |
| Announcement | 150-250 | 200-300 |
| Educational | 250-400 | 300-450 |
| Re-engagement | 100-150 | 130-200 |
| Event invite | 150-250 | 200-300 |

## Phase 4: Sequence Planning (Nurture/Drip Only)

If `email_type` is `nurture` and `sequence_position` is provided, plan the full sequence arc:

**Standard 7-email nurture sequence:**

| Email | Theme | Goal | Tone |
|-------|-------|------|------|
| 1 | Welcome + quick win | Build trust | Warm, helpful |
| 2 | Pain point deep-dive | Create problem awareness | Educational |
| 3 | Framework or method | Position expertise | Authoritative |
| 4 | Case study | Provide social proof | Conversational |
| 5 | Common mistakes | Agitate pain | Direct |
| 6 | Your approach | Bridge to service | Professional |
| 7 | Soft CTA | Drive action | Personal |

Each email must:
- Reference the previous email naturally ("Last time, I shared...")
- Escalate commitment gradually (read -> engage -> click -> book)
- Deliver standalone value even if read in isolation
- Not repeat points from earlier emails

If generating a single email in the sequence, include context notes on what came before and what comes after.

## Phase 5: Quality Checks

Before finalizing, run these checks:

1. **Spam filter test**: scan for spam trigger words, excessive links, image-heavy language
2. **Mobile preview**: subject + preview text combined must make sense in 90 characters
3. **Tone audit**: read aloud; does it sound like the brand?
4. **CTA audit**: is the CTA specific, actionable, and appearing only once as primary?
5. **Link audit**: are all links purposeful? No more than 3 links per email (newsletters: max 5)
6. **Unsubscribe compliance**: include unsubscribe mention in footer context
7. **Banned phrase scan**: final check against `outreach.banned_phrases`
8. **Length check**: within word count targets for the email type

## Phase 6: Output

Return structured JSON:

```json
{
  "email_metadata": {
    "type": "newsletter",
    "topic": "CRO tips for D2C brands",
    "audience": "India D2C",
    "goal": "educate",
    "sequence_position": null,
    "word_count": 420
  },
  "subject_lines": [
    {"text": "The CRO fix nobody talks about", "approach": "curiosity", "curiosity_score": 9, "clarity_score": 7, "length": 30, "spam_risk": "low"},
    {"text": "3 ways to boost your AOV this week", "approach": "benefit", "curiosity_score": 6, "clarity_score": 9, "length": 35, "spam_risk": "low"},
    {"text": "We increased conversions 34%", "approach": "number", "curiosity_score": 8, "clarity_score": 8, "length": 28, "spam_risk": "low"},
    {"text": "Is your product page costing you?", "approach": "question", "curiosity_score": 8, "clarity_score": 8, "length": 33, "spam_risk": "low"},
    {"text": "50 audits later, here is what I found", "approach": "personal", "curiosity_score": 9, "clarity_score": 6, "length": 36, "spam_risk": "low"}
  ],
  "recommended_subject": 0,
  "preview_text": "Most stores miss this on their product pages",
  "email_body": {
    "opening": "Opening hook text...",
    "sections": [
      {"heading": "Section heading", "body": "Section content...", "cta_inline": null},
      {"heading": "Case in point", "body": "Case study reference...", "cta_inline": "See the full audit"}
    ],
    "primary_cta": {"text": "Book your free CRO audit", "url_placeholder": "{{cta_url}}"},
    "ps_line": "P.S. Next week I am breaking down the exact audit checklist we use. Stay tuned.",
    "sign_off": "Ekata | Plasho (plasho.com)"
  },
  "quality_checks": {
    "spam_risk": "low",
    "mobile_preview_ok": true,
    "tone_compliant": true,
    "cta_clear": true,
    "banned_phrases_clear": true,
    "word_count_in_range": true
  },
  "sequence_context": null
}
```

## Phase 7: Review

Present the email to the user:

1. Show the recommended subject line (with alternatives)
2. Show preview text
3. Show the full email body with formatting
4. Highlight the CTA
5. Show quality check results
6. Ask for approval or revision requests

After approval, optionally:
- Create draft in Gmail via `tools.email_sending` if configured
- Log to CRM via `crm-writer` if part of a campaign
- Hand off to `content-repurposer` if the newsletter content should be distributed elsewhere

## Example Usage

Trigger phrases:
- "Write a newsletter about [topic]"
- "Draft a nurture email sequence for new subscribers"
- "Create an onboarding welcome email"
- "Write an announcement email for [news]"
- "Draft email 3 of our nurture sequence"
- "Write a re-engagement email for inactive subscribers"
- "Create an event invite email for [event]"

```
User: Write a newsletter about CRO tips for D2C Shopify brands
Assistant: [reads config, structures newsletter architecture, generates 5 subject lines, writes body with sections and CTA, runs quality checks, returns structured JSON]
```

```
User: Draft a 7-email nurture sequence for new leads who downloaded our CRO guide
Assistant: [reads config, plans full sequence arc, generates each email with escalating commitment, ensures no repetition across emails, returns all 7 as structured JSON]
```
