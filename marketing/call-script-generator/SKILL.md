---
name: call-script-generator
description: Generate structured call scripts by persona and lead context
tags: [calling, scripts, outreach, phone]
---

# Call Script Generator

Generates structured, persona-adapted call scripts for cold calls, follow-up calls, and demo-booked prep sessions. Adapts opening hooks, value props, objection handling, and closes based on the contact's role and available lead context (signals, CRO findings, previous touches).

## Prerequisites

- `agency.config.json` at repo root with `services`, `case_studies`, and `outreach.tone` sections
- Optional: `crm-writer` skill for logging scripts to the calling tab

## Phase 0: Intake

1. Read `agency.config.json` from the project root.
2. Extract:
   - `services` -- all service offerings with descriptions and keywords
   - `case_studies` -- available case studies with client name, metrics, and industry
   - `outreach.tone` -- voice and tone guidelines for spoken scripts
3. Accept parameters:
   - `lead` -- object with: `company`, `contact_name`, `title`, `industry`, `company_size`
   - `call_type` -- one of: `"cold"`, `"follow_up"`, `"demo_booked"`
   - `lead_context` -- optional object with: `signal` (how the lead was found), `cro_findings` (specific issues found on their store), `previous_touches` (array of prior outreach actions with dates)

## Phase 1: Persona Mapping

Map the contact's title to a persona and adapt the script structure accordingly.

| Persona | Titles | Opening Hook | Key Value Prop | Primary Objection |
|---------|--------|-------------|---------------|-------------------|
| Founder/CEO | Founder, CEO, Co-founder, Owner, Managing Director | Business growth, time savings, founder bandwidth | "We handle Shopify end-to-end so you focus on product and growth" | "I already have a developer" |
| Head of Ecomm | Head of Ecommerce, Ecommerce Director, VP Ecommerce, DTC Lead | Conversion metrics, tech stack optimization, revenue per session | "Our CRO audit found X% conversion leakage on your store" | "We're already doing CRO internally" |
| VP Marketing | VP Marketing, CMO, Head of Marketing, Marketing Director | Campaign performance, brand consistency, marketing-to-store handoff | "Performance marketing works best when the store converts -- we bridge that gap" | "Budget is tight this quarter" |
| Marketing Manager | Marketing Manager, Ecommerce Manager, Digital Marketing Manager, Growth Manager | Execution support, bandwidth relief, tactical help | "Extend your team without the overhead of another full-time hire" | "I need to check with my VP" |

If the title does not match any persona, default to **Founder/CEO** for companies under 50 people and **Head of Ecomm** for larger companies.

## Phase 2: Generate Script

Generate a complete call script based on `call_type`.

### Cold Call Script (target: 2-3 minutes)

**1. Opening (15 seconds)**

Use a pattern interrupt. Do not open with "Hi, how are you today?" or "Is this a good time?" -- these trigger automatic rejection.

Structure:
- State your name and agency in one breath.
- Deliver a permission-based opener that creates curiosity.

Examples by persona:
- Founder: "Hi {name}, this is {caller} from Plasho. I was looking at {company}'s Shopify store and found something specific I wanted to share -- mind if I take 30 seconds?"
- Head of Ecomm: "Hi {name}, {caller} from Plasho. We ran a quick conversion analysis on {company}'s store and spotted a few things your team might want to know about. Got 30 seconds?"
- VP Marketing: "Hi {name}, {caller} from Plasho. I noticed {company}'s ad campaigns are driving traffic to a store that might be leaving revenue on the table. Can I share what we found in 30 seconds?"
- Marketing Manager: "Hi {name}, {caller} here from Plasho. We work with {industry} brands on their Shopify stores and I had a specific thought about {company}. Quick 30 seconds?"

**2. Value Hook (30 seconds)**

Connect the signal or CRO finding to a concrete result.

- If `lead_context.cro_findings` exists: reference the specific issue. "We found that your product page has {issue}, which typically costs brands like yours {X}% in lost conversions."
- If `lead_context.signal` exists: reference the signal. "I saw your {signal_source} about {topic}, and we actually just solved that exact problem for {case_study_client}."
- Fallback: use a general industry insight. "Most {industry} Shopify stores we audit are losing 15-30% of their potential revenue to fixable UX and conversion issues."

Always tie to a case study result: "We found a similar issue at {case_study_client} and fixing it increased their {metric} by {X}%."

**3. Qualification Questions (60 seconds)**

Ask 2-3 questions to qualify the lead. Listen more than talk.

Core questions:
- "Are you currently working with a Shopify agency or developer?"
- "What's the biggest challenge with your store right now?"
- "Is conversion optimization a priority this quarter?"

Context-specific questions:
- If they have a developer: "How's that going? Is your current setup giving you the conversion rates you need?"
- If they mentioned budget constraints in signal: "What does your current setup cost you monthly for store management?"
- If they are post-funding: "Now that you've raised, what's the timeline for scaling the ecommerce side?"

**4. Objection Handling**

Prepare responses for common objections. Tone: empathetic, not argumentative. Acknowledge, reframe, leave the door open.

- **"Not interested"**: "Totally understand. Would it make sense to keep in touch for when things change? I can send over a quick case study in the meantime."
- **"We have an agency"**: "Great, how's that going? Many brands bring us in for specific CRO projects alongside their main agency. We complement, not replace."
- **"Send me info"**: "Of course. To send you the most relevant case study, which part of your store are you most focused on improving -- product pages, checkout, or overall design?"
- **"No budget right now"**: "Makes sense. A lot of brands find that a targeted CRO fix pays for itself in the first month. Want me to share what that looks like with a real example?"
- **"I need to check with my VP/team"**: "Absolutely. Would it help if I put together a one-page summary you can share? What would your team need to see to move forward?"
- **"We do everything in-house"**: "That's solid. How's the bandwidth? Most in-house teams we talk to are stretched thin on the Shopify side specifically. We typically slot in as a specialized extension."

**5. Close (30 seconds)**

Ask for a specific time. Do not ask "Would you be interested in a call?" -- you are already on one.

- Primary: "Would Thursday at 2pm work for a 15-minute deeper look at what we found on your store?"
- Alternative: "I can send over a calendar link -- what days work best for you this week?"
- If resistant: "No pressure at all. Can I send you the case study by email? If anything resonates, you have my number."

### Follow-up Call Script (target: 1-2 minutes)

Shorter and more direct. The lead has had a previous touchpoint.

**1. Opening (10 seconds)**
- Reference the previous touch: "Hi {name}, {caller} from Plasho. We connected {touchpoint_description} -- just following up."

**2. New Value (30 seconds)**
- Add something new they have not heard: a new case study result, a new observation about their store, or industry news relevant to them.
- Do not repeat the same pitch from the first touch.

**3. Direct Ask (20 seconds)**
- "Has anything changed on your end since we last spoke?"
- "Would it make sense to do a quick 15-minute walkthrough this week?"

### Demo-Booked Prep Script

Not a call script per se, but preparation notes for the demo call.

**1. Pre-Call Research Notes**
- Company overview: what they sell, their market, their Shopify store URL
- Recent news or signals about the company
- Their current store's strengths and weaknesses (from CRO findings if available)
- Competitive landscape: who else serves their market

**2. Discovery Questions to Ask**
- "Walk me through your current ecommerce setup -- who manages what?"
- "What's your biggest pain point with the store right now?"
- "What does success look like for you in the next 6 months?"
- "Who else is involved in this decision?"
- "What's your timeline for making a change?"
- "What's your current monthly revenue from the store?" (ask late in the call, after rapport)

**3. Demo Talking Points**
Tailored to their specific issues:
- For each CRO finding, prepare a before/after explanation
- Map each issue to the relevant case study
- Prepare pricing context (do not lead with price, but be ready)

## Phase 3: Output

Return a structured JSON object:

```json
{
  "call_type": "cold",
  "contact": {
    "name": "Rahul Sharma",
    "title": "Founder",
    "company": "Brand X"
  },
  "persona": "Founder/CEO",
  "opening": "Hi Rahul, this is {caller} from Plasho. I was looking at Brand X's Shopify store and found something specific I wanted to share -- mind if I take 30 seconds?",
  "value_hook": "Your product pages are loading variant images in a way that adds 2 extra clicks to purchase. We fixed the same issue for Kibi Sports and it increased their add-to-cart rate by 18%.",
  "questions": [
    "Are you currently working with a Shopify agency or developer?",
    "What's the biggest challenge with the store right now?",
    "Is conversion optimization a priority this quarter?"
  ],
  "objection_handlers": {
    "not_interested": "Totally understand. Would it make sense to keep in touch for when things change? I can send over a quick case study in the meantime.",
    "have_agency": "Great, how's that going? Many brands bring us in for specific CRO projects alongside their main agency. We complement, not replace.",
    "send_info": "Of course. To send you the most relevant case study, which part of your store are you most focused on improving -- product pages, checkout, or overall design?",
    "no_budget": "Makes sense. A lot of brands find that a targeted CRO fix pays for itself in the first month. Want me to share what that looks like with a real example?",
    "check_with_team": "Absolutely. Would it help if I put together a one-page summary you can share? What would your team need to see to move forward?",
    "in_house": "That's solid. How's the bandwidth? Most in-house teams we talk to are stretched thin on the Shopify side specifically."
  },
  "close": "Would Thursday at 2pm work for a 15-minute deeper look at what we found on your store?",
  "estimated_duration": "2-3 minutes",
  "notes_for_caller": "Rahul is a founder, so focus on saving his time and letting him focus on product. Brand X is in the fitness equipment space, similar to Kibi Sports. Use the Kibi case study heavily. Signal source: Reddit post asking about Shopify CRO agencies."
}
```

For `follow_up` type, the structure is the same but `opening` references the previous touch, `value_hook` contains new information, and `estimated_duration` is "1-2 minutes."

For `demo_booked` type, replace the call script fields with:
```json
{
  "call_type": "demo_booked",
  "contact": { ... },
  "pre_call_research": { "company_overview": "...", "recent_signals": "...", "store_analysis": "...", "competitors": "..." },
  "discovery_questions": ["...", "...", "..."],
  "demo_talking_points": ["...", "...", "..."],
  "pricing_notes": "...",
  "estimated_duration": "30 minutes"
}
```

## Phase 4: CRM Integration

If `crm-writer` skill is available:

1. Write to the calling tab via `crm-writer`.
2. For each script generated, log one row with columns:
   - Date
   - Contact Name
   - Company
   - Title
   - Call Type (cold / follow_up / demo_booked)
   - Phone (if available)
   - Talking_Points (condensed version: opening + value hook + close, max 500 chars)
   - Status (scheduled / completed / no_answer / callback)
   - Next Action
3. The Talking_Points column gives the caller a quick reference without reading the full script.

## Example Usage

Trigger phrases:
- "Generate a cold call script for this lead"
- "Prep me for the demo call with {company}"
- "Create follow-up call scripts for yesterday's no-answers"
- "Build call scripts for these 5 leads"

```
User: Generate a cold call script for Rahul Sharma, Founder of Brand X
Assistant: [reads config, maps to Founder/CEO persona, generates full script with personalized opening/hook/objections/close, outputs JSON, logs to CRM]
```

```
User: Prep me for the demo with Lifelong tomorrow
Assistant: [reads config + lead context, generates demo_booked prep with research notes, discovery questions, and tailored talking points]
```
