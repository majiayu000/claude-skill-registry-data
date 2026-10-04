---
name: message-generator
description: Multi-channel personalized message generation with 3 tiers of personalization
tags: [messaging, outreach, personalization, email, linkedin, instagram]
---

# Message Generator

Generates personalized outreach messages across all channels. Supports 3 tiers of personalization, from basic merge fields to fully individualized messages referencing specific signals and research. All tone, rules, and constraints are read from `agency.config.json`.

## Prerequisites

- `agency.config.json` at repo root with `outreach`, `services`, `case_studies`, and `agency` sections
- Lead data with at minimum: name, company
- For Tier 2+: ICP segment data (industry, company size)
- For Tier 3: Output from `company-researcher`, `person-researcher`, `cro-auditor`, or `signal-scanner`

## Phase 0: Intake

1. Read `agency.config.json` from the project root.
2. Extract:
   - `agency.name` -- the agency name for sign-offs and references
   - `agency.domain` -- for email domain
   - `agency.founder` -- for personal sign-offs
   - `outreach.tone` -- voice/style guide for all messages
   - `outreach.banned_phrases` -- phrases that must NEVER appear in any message
   - `outreach.sign_off` -- default sign-off line
   - `outreach.cadence` -- which message types to send on which day
   - `outreach.daily_caps` -- per-channel daily limits
   - `services[]` -- agency's service offerings for value prop
   - `case_studies[]` -- proof points to reference
3. Accept parameters:
   - `message_type` -- one of: `cold-email`, `gig-proposal`, `community-reply`, `linkedin-note`, `instagram-dm`, `call-script`, `follow-up-email`, `breakup-email`
   - `personalization_tier` -- 1, 2, or 3
   - `lead` -- the lead data object
   - `research` -- (Tier 3 only) output from researcher skills
   - `framework` -- (optional) override: `PAS`, `BAB`, `AIDA`, `Signal-Proof-Ask`
   - `cadence_day` -- (optional) which day in the cadence sequence

## Phase 1: Framework Selection

If no framework is specified, auto-select based on message type and tier:

| Message Type | Default Framework | Notes |
|---|---|---|
| cold-email | Signal-Proof-Ask (Tier 3), PAS (Tier 2), BAB (Tier 1) | Lead with signal reference when available |
| gig-proposal | Signal-Proof-Ask | Always lead with their specific need |
| community-reply | None (conversational) | Help first, pitch subtly |
| linkedin-note | BAB | Short, personal |
| instagram-dm | None (casual) | Ultra-short, visual reference |
| call-script | AIDA | Structured for verbal delivery |
| follow-up-email | PAS | Reference previous touchpoint |
| breakup-email | BAB | Create urgency without pressure |

### Framework definitions:

**PAS (Problem-Agitate-Solve):**
1. Name the problem the lead is facing
2. Amplify the cost of not solving it
3. Present the agency's service as the solution

**BAB (Before-After-Bridge):**
1. Describe their current state
2. Paint the better future state
3. Bridge: how the agency gets them there

**AIDA (Attention-Interest-Desire-Action):**
1. Hook with a bold statement or stat
2. Build interest with relevance
3. Create desire with proof/results
4. Clear CTA

**Signal-Proof-Ask:**
1. Reference the specific signal (their post, job listing, funding, etc.)
2. Prove credibility with a relevant case study result
3. Ask one clear question or propose one action

## Phase 2: Personalization

### Tier 1: Merge Fields Only
For bulk outreach. Replace placeholders with lead data:
- `{{first_name}}` -- lead's first name
- `{{company}}` -- company name
- `{{agency.name}}` -- agency name
- `{{agency.founder}}` -- founder name
- `{{sign_off}}` -- from config
- `{{case_study.name}}` -- case study client name
- `{{case_study.result}}` -- case study result line

The message body uses generic industry angles. No lead-specific research.

### Tier 2: Segment-Based
Group leads by ICP segment and customize messaging:
- **Industry angle**: Reference industry-specific pain points
  - D2C fashion: "Product pages with size guides and lifestyle imagery convert 2x better"
  - Sports/fitness: "Sports brands need trust signals, athlete endorsements front and center"
  - Beauty/skincare: "Skincare brands live or die by before/after proof and ingredient transparency"
- **Company size angle**:
  - Early stage (<50): "You're growing fast, your store needs to keep up"
  - Mid-market (50-200): "Your team is stretched thin, outsourcing Shopify work frees your ecomm lead to focus on strategy"
- **Market angle**:
  - India: Reference local market dynamics, pricing in INR
  - US/UK/AU: Reference remote team benefits, timezone overlap, cost advantage

### Tier 3: Per-Lead (Hyper-Personalized)
Requires research data from `company-researcher`, `person-researcher`, `cro-auditor`, or `signal-scanner`.

Personalization sources (use all that are available):
- **Signal reference**: "I saw your post on Reddit looking for a Shopify developer..."
- **CRO finding**: "I checked {{company}}'s product pages, noticed {{specific_issue}}..."
- **Personal interest**: "Your recent LinkedIn post about {{topic}} resonated..."
- **Company news**: "Congrats on the Series A, perfect time to invest in your storefront..."
- **Tech stack note**: "I see you're on {{theme}}, we've migrated several stores from that to..."

Build the opening line from the strongest personalization hook available.

## Phase 3: Message Generation

### Channel-specific rules:

**cold-email:**
- Subject line: max 50 characters, no spam trigger words, personalized when possible
- Body: max 150 words for Tier 1-2, max 200 words for Tier 3
- One CTA only (book a call, reply, or view case study)
- No attachments or links in first email (deliverability)
- P.S. line optional for Tier 3 (add a personal touch)

**gig-proposal:**
- Open with their specific requirement (mirror their language)
- Show relevant experience in 2-3 bullet points
- Include timeline and availability
- Max 250 words
- End with a question that invites dialogue

**community-reply:**
- Help first: answer their question genuinely
- Subtly mention experience: "We did something similar for a sports brand..."
- No hard pitch, no links in first reply
- Match the community's tone (casual for Reddit, professional for Shopify Community)
- Max 150 words

**linkedin-note:**
- Max 300 characters (LinkedIn connection note limit)
- One personalization point
- One reason to connect
- No pitch in the connect note

**instagram-dm:**
- Max 100 words
- Reference something specific from their feed (a product, a post, their aesthetic)
- Casual, conversational tone
- No links in first DM

**call-script:**
- Opening hook (15 seconds)
- Qualification questions (3 max)
- Value prop with case study reference
- Objection handling notes
- Close with meeting ask
- Total talk track: 2-3 minutes

**follow-up-email:**
- Reference the previous touchpoint (email, call, LinkedIn)
- Add new value (a relevant insight, article, or finding)
- Max 100 words
- Different CTA than the first email

**breakup-email:**
- Acknowledge they're busy
- Summarize value in one line
- "If timing isn't right, no worries"
- Leave the door open
- Max 75 words

## Phase 4: Quality Check

Before returning, verify every generated message:

1. **Banned phrase scan**: Check against `outreach.banned_phrases`. If any match, rewrite the offending sentence.
2. **Word count**: Verify within channel limits.
3. **CTA count**: Exactly one CTA per message (except call scripts).
4. **Tone check**: Re-read against `outreach.tone` description. Rewrite if it sounds generic, desperate, or salesy.
5. **Spam word check**: No "free", "guaranteed", "act now", "limited time", "click here" in emails.

## Phase 5: Output

Return structured JSON:

```json
{
  "message_type": "cold-email",
  "personalization_tier": 3,
  "framework": "Signal-Proof-Ask",
  "subject_line": "Your product pages are leaving money on the table",
  "body": "The full message text...",
  "personalization_points": [
    "Referenced their Reddit post about needing Shopify help",
    "Mentioned their missing product reviews (from CRO audit)",
    "Used Kibi Sports case study (same industry)"
  ],
  "cta": "Reply to grab 15 min this week?",
  "word_count": 142,
  "channel_rules_met": true,
  "banned_phrases_clear": true,
  "sign_off": "Ekata | Plasho (plasho.com)",
  "cadence_day": 1,
  "cadence_next": "Day 2: LinkedIn connect"
}
```

For batch generation, return an array of message objects.

## Phase 6: Log

If writing to CRM, use `crm-writer` to log: lead name, company, channel, message type, tier, subject line, cadence day, generated_at timestamp.

## Example Usage

Trigger phrases:
- "Draft a cold email for this lead"
- "Write a LinkedIn note for [name]"
- "Generate outreach messages for these leads"
- "Write a gig proposal for this Freelancer post"
- "Create a follow-up email for [company]"
- "Generate Tier 3 messages using this research"

```
User: Write a cold email for the founder of BrandX, they just raised a seed round
Assistant: [reads config, selects Signal-Proof-Ask framework, generates Tier 3 email referencing funding news, includes case study, returns structured JSON]
```

```
User: Generate Tier 1 cold emails for these 10 leads
Assistant: [reads config, uses BAB framework, applies merge fields only, returns 10 message objects]
```
