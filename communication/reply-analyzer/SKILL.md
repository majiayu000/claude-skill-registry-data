---
name: reply-analyzer
description: Classify reply sentiment and determine next action
tags: [replies, analysis, sentiment, pipeline]
---

# Reply Analyzer

Classifies the sentiment and intent of replies to outreach messages. Determines the recommended next action, generates draft responses for positive and neutral cases, and outputs CRM stage updates. Used by the `evening-scan` playbook after `inbox-scanner` returns responses.

## Prerequisites

- `agency.config.json` at repo root with `outreach`, `services`, `case_studies`
- Reply data from `inbox-scanner` or manually provided

## Phase 0: Intake

1. Read `agency.config.json` from the project root.
2. Extract:
   - `services` -- list of services offered (for matching interest areas)
   - `case_studies` -- available case studies (for draft responses)
   - `outreach.tone` -- voice guidelines for draft responses
   - `outreach.banned_phrases` -- phrases to avoid in draft responses
   - `outreach.sign_off` -- signature line for draft responses
3. Accept parameters:
   - `reply_text` -- the full text of the reply (required)
   - `from_name` -- name of the person who replied
   - `from_email` -- their email address (if available)
   - `company` -- their company name (if known)
   - `channel` -- where the reply came from (`email`, `linkedin`, `instagram`)
   - `lead_context` -- object with cadence day, previous touches, lead score, tier

## Phase 1: Sentiment Classification

Analyze the reply text and classify it into exactly one of these categories:

| Category | Signals | Examples |
|----------|---------|---------|
| `POSITIVE_DEMO` | Explicitly requests a meeting, call, or demo | "Let's set up a call", "Can we chat this week?", "Send me a calendar link", "Free Thursday?" |
| `POSITIVE_INTERESTED` | Questions about services, pricing, timeline, availability; general interest | "Sounds interesting, tell me more", "What are your rates?", "How long does a CRO audit take?", "Can you send some examples?" |
| `NEUTRAL_QUESTION` | Asks for info but no clear buying intent | "Who is this?", "How did you find me?", "What does Plasho do?", "Where are you based?" |
| `NEUTRAL_OOO` | Out of office or auto-reply | "I'm out of office until...", "On PTO, back on...", "Auto-reply: I'm currently unavailable" |
| `NEGATIVE_NOT_NOW` | Polite decline with timing indication; not a permanent no | "Not the right time", "Maybe next quarter", "We just signed with someone", "Check back in 3 months" |
| `NEGATIVE_NOT_INTERESTED` | Clear rejection without timing indicator | "Not interested", "We're good, thanks", "Not looking for this", "Please don't contact me" |
| `NEGATIVE_UNSUBSCRIBE` | Wants to be removed from all communication | "Unsubscribe", "Remove me from your list", "Stop emailing me", "Do not contact me again", "This is spam" |
| `REFERRAL` | Redirects to another person inside or outside their company | "You should talk to [name]", "CC'ing my colleague who handles this", "Try reaching out to our head of ecomm" |

### Classification rules:

- If multiple signals are present, choose the **strongest positive** category. A reply that asks a question AND requests a call is `POSITIVE_DEMO`, not `NEUTRAL_QUESTION`.
- Short replies ("Thanks", "Got it", "OK") without additional context: classify as `NEUTRAL_QUESTION` with LOW confidence.
- Replies that are clearly automated (vacation responders, ticket confirmations): classify as `NEUTRAL_OOO`.
- Any mention of "unsubscribe", "remove", "stop", or "spam" overrides all other signals and forces `NEGATIVE_UNSUBSCRIBE`.

## Phase 2: Intent Extraction

Beyond the top-level sentiment, extract these structured details from the reply:

### Questions asked
List every question the person asked, verbatim or paraphrased:
- "What are your rates?"
- "How long does a CRO audit take?"
- "Do you work with brands outside India?"

### Objections raised
Identify any objections or hesitations:
- **Price**: "Too expensive", "What's the budget?", "We don't have budget right now"
- **Timing**: "Not the right time", "Maybe next quarter", "After our funding round"
- **Existing vendor**: "We already work with an agency", "We just signed with someone"
- **Platform**: "We're not on Shopify", "We use WooCommerce", "Thinking of migrating to Shopify"
- **Trust**: "Never heard of you", "Can you share references?", "How many stores have you done?"
- **Scope**: "We only need X, not Y", "This is too comprehensive"

### People mentioned
Extract any person references that could be referrals:
- Name (if mentioned)
- Title/role (if mentioned)
- Company (if different from the replier's company)
- Contact info (if shared)

### Timeline indicators
Extract any timing references:
- Specific dates: "after March", "in Q2", "next month"
- Relative: "in 2 weeks", "next quarter", "after funding"
- Vague: "sometime later", "eventually"
- Urgent: "ASAP", "this week", "immediately"

### Interest areas
Map the reply to specific services from `agency.config.json`:
- Which service(s) they seem interested in
- Any specific problems they mentioned (e.g., "our conversion rate is low" maps to CRO)

## Phase 3: Recommended Action

Based on the classification, recommend a specific next action and CRM stage update:

| Classification | Recommended Action | CRM Stage Update | Pause Cadence? |
|---------------|-------------------|-----------------|----------------|
| `POSITIVE_DEMO` | Send calendar link immediately. Suggest 2-3 time slots. Keep it short. | `DEMO_BOOKED` | Yes |
| `POSITIVE_INTERESTED` | Reply with relevant info addressing their questions. Include the most relevant case study. Ask if they want to jump on a 15-min call. | `REPLIED` | Yes |
| `NEUTRAL_QUESTION` | Answer their question directly and concisely. Re-pitch value in 1-2 sentences. Include a soft CTA for a call. | `REPLIED` | Yes |
| `NEUTRAL_OOO` | Do nothing now. Note their return date. Reschedule next cadence touch for return date + 1 day. | `CONTACTED` (keep current) | Adjust timing only |
| `NEGATIVE_NOT_NOW` | Send polite acknowledgment. If they gave a timeline, set a reminder for that date. If no timeline, set reminder for 90 days. | `REPLIED` | Yes, with reactivation date |
| `NEGATIVE_NOT_INTERESTED` | Send a short, gracious close: "Understood, thanks for letting me know. If things change, we're here." Mark lead as done. | `NOT_INTERESTED` | Yes, end cadence |
| `NEGATIVE_UNSUBSCRIBE` | Send acknowledgment: "Done, you won't hear from us again." Remove from ALL sequences and lists immediately. | `DO_NOT_CONTACT` | Yes, permanent |
| `REFERRAL` | Thank the original contact. Add the referred person as a new lead with source = "referral from [original contact]". Begin research on the referred person. | `REPLIED` (original) + create new lead | Yes (original) |

### Draft response generation

Generate a draft response for `POSITIVE_DEMO`, `POSITIVE_INTERESTED`, `NEUTRAL_QUESTION`, `NEGATIVE_NOT_NOW`, `NEGATIVE_NOT_INTERESTED`, and `NEGATIVE_UNSUBSCRIBE` categories.

Draft response rules:
- Follow the `outreach.tone` from config: direct, helpful, zero fluff
- Never use any phrase from `outreach.banned_phrases`
- Keep it under 100 words for email, under 50 words for LinkedIn/Instagram
- Use the replier's first name
- For positive replies: reference the most relevant `case_studies` entry based on their industry/interest
- For demo requests: include a calendar link placeholder `[CAL_LINK]`
- Sign off with `outreach.sign_off`
- Match the channel tone: email can be slightly longer, LinkedIn/Instagram should be conversational and brief

## Phase 4: Output

Return structured JSON:

```json
{
  "classification": "POSITIVE_INTERESTED",
  "sentiment": "positive",
  "confidence": "HIGH",
  "summary": "Interested in CRO audit services, asked about pricing and timeline",
  "questions_asked": [
    "What are your rates?",
    "How long does a CRO audit take?"
  ],
  "objections": [],
  "referrals": [],
  "timeline_mentioned": null,
  "interest_area": "Conversion Rate Optimization",
  "recommended_action": "Reply with CRO audit pricing and Kibi Sports case study. Suggest 15-min call.",
  "crm_stage_update": "REPLIED",
  "pause_cadence": true,
  "reactivation_date": null,
  "draft_response": "Hey Sarah, glad this caught your eye. For CRO, we typically start with a full audit (takes about a week) -- for reference, our Kibi Sports audit uncovered issues causing 15-25% revenue loss, and the redesign drove measurable uplift in conversions.\n\nHappy to walk through what a quick audit of your store would look like. Got 15 min this week?\n\nEkata | Plasho (plasho.com)",
  "new_leads_to_create": []
}
```

For `REFERRAL` classification, the `new_leads_to_create` array is populated:

```json
{
  "classification": "REFERRAL",
  "sentiment": "neutral",
  "confidence": "MEDIUM",
  "summary": "Redirected to their Head of Ecommerce, Priya Sharma",
  "questions_asked": [],
  "objections": [],
  "referrals": [
    {
      "name": "Priya Sharma",
      "title": "Head of Ecommerce",
      "company": "Brand X",
      "email": null,
      "source": "Referral from Sarah Chen"
    }
  ],
  "timeline_mentioned": null,
  "interest_area": null,
  "recommended_action": "Thank Sarah for the referral. Research Priya Sharma at Brand X. Add as new lead with referral source.",
  "crm_stage_update": "REPLIED",
  "pause_cadence": true,
  "reactivation_date": null,
  "draft_response": "Thanks Sarah, really appreciate the pointer. Will reach out to Priya.\n\nEkata | Plasho (plasho.com)",
  "new_leads_to_create": [
    {
      "name": "Priya Sharma",
      "title": "Head of Ecommerce",
      "company": "Brand X",
      "email": null,
      "source": "Referral from Sarah Chen",
      "priority": "HIGH"
    }
  ]
}
```

Confidence levels:
- **HIGH**: Reply is unambiguous, classification is clear from the text
- **MEDIUM**: Reply has mixed signals or is short/ambiguous, classification is best guess
- **LOW**: Reply is very short (1-3 words), automated, or context-dependent

## Example Usage

Trigger phrases:
- "Analyze this reply"
- "Classify this response"
- "What should I do with this reply?"
- "Run reply analyzer on these responses"

```
User: Analyze this reply: "Hey, interesting work on Kibi Sports. We're actually looking at overhauling our Shopify store. What would something like that cost for a mid-size D2C brand? Could do a call next week."
Assistant: [classifies as POSITIVE_DEMO, extracts pricing question + timeline "next week", recommends sending calendar link with 2-3 slots, generates draft response referencing Kibi Sports case study]
```

```
User: What do I do with this: "Thanks but we just hired an agency last month."
Assistant: [classifies as NEGATIVE_NOT_NOW, extracts objection "existing vendor", recommends polite acknowledgment with 90-day reminder, generates short gracious reply]
```
