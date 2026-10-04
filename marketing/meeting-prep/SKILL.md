---
name: meeting-prep
description: >
  Pre-meeting research and talking points generator. Researches the person
  and company, pulls CRM history, and generates a structured briefing with
  agenda, talking points, objection handlers, and recommended asks.
tags: [sales, meetings, research, preparation]
---

# Meeting Prep

Generates a comprehensive meeting briefing before any prospect or client call. Combines live company and person research with CRM history to produce an agenda, tailored talking points, anticipated objections with handlers, and a clear ask for the meeting outcome.

## Prerequisites

- `agency.config.json` populated (services, ICP, case studies, CRM config)
- WebSearch tool available for live research
- CRM data accessible (optional but improves quality significantly)
- Meeting details: who, when, what type of meeting

## Capabilities Used

1. `person-researcher` -- deep dive on the contact (background, role, LinkedIn, content they've published)
2. `company-researcher` -- company intel (size, revenue, tech stack, recent news, hiring)
3. `crm-writer` -- pull CRM history for existing leads/clients
4. `linkedin-researcher` -- LinkedIn profile and activity analysis
5. `decision-maker-finder` -- identify other stakeholders who may be in the meeting

## Phase 0: Intake

Read `agency.config.json`:
- `services[]` -- available services to recommend
- `case_studies[]` -- proof points to reference
- `icp.segments[]` -- check if the prospect fits ICP
- `crm.tabs` -- locate lead/client records
- `agency.name`, `agency.domain` -- for context
- `tools.crm` -- determine CRM path (Google Sheets, etc.)

Accept parameters:
- `contact_name` -- (required) name of the person you're meeting
- `company_name` -- (required) their company
- `meeting_type` -- `discovery` | `follow_up` | `proposal` | `qbr` | `onboarding` | `general`. Default: `discovery`
- `meeting_date` -- scheduled date/time
- `meeting_context` -- any additional context (e.g., "They reached out after seeing our case study")
- `attendees` -- list of other attendees if known
- `research_depth` -- `quick` | `deep`. Default: `deep`

## Phase 1: Person Research

Run `person-researcher` for the primary contact:

### LinkedIn Profile
- Current title and tenure
- Previous roles (especially ecommerce, marketing, or agency experience)
- Education and certifications
- Recent posts and engagement topics
- Mutual connections
- Groups and interests

### Professional Background
- WebSearch: `"{{contact_name}}" "{{company_name}}"`
- WebSearch: `"{{contact_name}}" interview OR podcast OR conference`
- WebSearch: `"{{contact_name}}" linkedin`
- Look for: speaking appearances, published articles, quotes in press

### Communication Style Indicators
- Formal vs casual (based on LinkedIn content tone)
- Data-driven vs narrative (based on content they share)
- Technical vs strategic (based on role and background)

Compile:
```
CONTACT PROFILE
---
Name: [full name]
Title: [current title]
Tenure: [time in current role]
Background: [2-3 sentences on career arc]
LinkedIn: [URL]
Recent activity: [what they've been posting/engaging with]
Communication style: [formal/casual, data/narrative, technical/strategic]
Mutual connections: [if any]
Personal hooks: [shared interests, mutual connections, alma mater, hobbies]
```

If `attendees` were provided, run a lighter version of person research for each additional attendee.

## Phase 2: Company Research

Run `company-researcher` for the company:

### Company Fundamentals
- Industry and vertical
- Company size (employees, revenue if available)
- Founded date
- Headquarters location
- Funding status and recent rounds

### Digital Presence
- WebSearch: `site:{{company_domain}}`
- Current website platform (Shopify, WooCommerce, custom)
- Website quality assessment (quick visual scan via WebSearch results)
- Social media presence and activity levels
- App store / review presence

### Recent Activity
- WebSearch: `"{{company_name}}" {{current_year}}`
- New product launches
- Press mentions or media coverage
- Hiring activity (roles, departments expanding)
- Partnerships or collaborations announced
- Awards or recognition

### Ecommerce Signals (if applicable)
- WebSearch: `"{{company_name}}" shopify OR ecommerce OR "online store"`
- Store traffic estimates (if tools available)
- Product catalog size and complexity
- Pricing tier (premium, mid-market, budget)
- Competitor landscape in their market

### ICP Fit Assessment
Compare against `icp.segments[]`:
- Segment match: [which ICP segment, if any]
- Fit score: HIGH / MEDIUM / LOW / NO FIT
- Fit rationale: [why they do or don't match]

Compile:
```
COMPANY PROFILE
---
Company: [name]
Industry: [vertical]
Size: [employees] / Revenue: [estimate]
Platform: [current ecommerce platform]
Website: [URL]
ICP fit: [HIGH/MEDIUM/LOW] -- [rationale]
Recent news: [top 3 headlines]
Growth signals: [hiring, funding, product launches]
Pain indicators: [website issues, competitor pressure, scaling challenges]
```

## Phase 3: CRM History Pull

Check CRM for existing records:

### If Lead Exists
- Lead source (inbound, outbound, referral)
- Lead score (if `lead-scorer` has run)
- Outreach history (emails sent, responses, calls)
- Previous meeting notes
- Stage in pipeline
- Assigned rep

### If Client Exists
- Contract start date and current value
- Active services
- Account health (from `churn-detector` if available)
- Recent deliverables and results
- Open issues or concerns
- Last QBR date and outcomes

### If No Record
- Note: "New contact, no CRM history"
- Flag for CRM entry after meeting

Compile:
```
CRM HISTORY
---
Status: [Lead / Client / New Contact]
Pipeline stage: [if lead]
Previous interactions: [summary]
Key notes: [anything flagged by previous reps]
Open items: [unresolved issues or pending proposals]
```

## Phase 4: Agenda Construction

Build a meeting agenda tailored to `meeting_type`:

### Discovery Call Agenda (15-30 min)
```
1. Rapport (2-3 min)
   - [Personal hook from Phase 1]
   - [Recent company news to reference]

2. Context Setting (2 min)
   - How they found us / why we reached out
   - Quick agency intro (30 seconds, not a pitch)

3. Discovery Questions (10-15 min)
   - Current state: "Walk me through your current ecommerce setup"
   - Pain points: "What's the biggest challenge with [specific area]?"
   - Goals: "Where do you want to be in 6 months?"
   - Decision process: "How do you typically evaluate partners?"
   - Timeline: "Is there a timeline driving this?"
   - Budget: "Do you have a budget range in mind for this type of work?"

4. Value Bridge (5 min)
   - Map their pain to a specific service
   - Reference relevant case study
   - Share one actionable insight they can use immediately

5. Next Steps (2 min)
   - Propose specific next action
   - Confirm decision-makers for next meeting
   - Set timeline
```

### Follow-Up Call Agenda
```
1. Recap (2 min)
   - Reference key points from last conversation
   - Confirm understanding of their needs

2. Address Open Items (5-10 min)
   - [Items from CRM history or previous meeting]

3. Proposal Preview or Deep Dive (10-15 min)
   - Service recommendation with specifics
   - Pricing discussion (if appropriate)
   - Timeline and deliverables

4. Objection Handling (5 min)
   - [Pre-prepared based on Phase 5]

5. Close / Next Steps (3 min)
   - Decision timeline
   - Required approvals
   - Proposal delivery date
```

### Proposal Presentation Agenda
```
1. Recap Needs (3 min)
2. Proposed Solution (10 min)
3. Case Study / Proof (5 min)
4. Investment and Timeline (5 min)
5. Q&A and Objections (5 min)
6. Decision Process and Next Steps (2 min)
```

### QBR Agenda
Defer to `qbr-builder` skill for structure.

### Onboarding Agenda
```
1. Welcome and Team Intros (5 min)
2. Project Scope Confirmation (10 min)
3. Communication Preferences (5 min)
4. Access and Tool Setup (10 min)
5. Timeline and Milestones Review (10 min)
6. Questions and Parking Lot (5 min)
7. Immediate Next Steps (5 min)
```

## Phase 5: Talking Points and Objection Handlers

### Tailored Talking Points
Based on research, generate 5-7 specific talking points:

```
TALKING POINTS
---
1. [Company news hook]: "I saw [specific thing]. How is that impacting [area]?"
2. [Pain point probe]: Based on [signal], ask about [specific challenge]
3. [Service bridge]: Their [situation] maps to our [service] -- here's how
4. [Case study reference]: "[Client] had a similar situation. We [action], result was [metric]"
5. [Industry insight]: "[Trend] is affecting [their vertical]. We're seeing [observation]"
6. [Differentiator]: What makes our approach different for their specific situation
7. [Urgency builder]: Time-sensitive factor (seasonal, competitive, platform update)
```

### Objection Handlers
Anticipate likely objections based on meeting type and research:

```
OBJECTION HANDLERS
---
"Too expensive":
  -> "Understood. Let me walk through the ROI math. With [client], the [service] paid for itself in [timeframe] through [metric improvement]."

"We're handling it in-house":
  -> "That makes sense for [area]. Where we typically help teams like yours is [specific gap]. [Client] had an in-house team too, and they brought us in specifically for [niche]."

"We need to think about it":
  -> "Of course. To help your decision, what specific questions would you want answered? I can send over [specific resource] that addresses [concern]."

"We're talking to other agencies":
  -> "Good, you should. The key differentiator to evaluate is [specific strength]. Happy to do a mini-audit so you can compare approaches side by side."

"Bad timing":
  -> "When would be better? [If seasonal]: Actually, starting now means you're ready for [upcoming event/season]."

"We tried an agency before and it didn't work":
  -> "What went wrong? [Listen]. Our approach to avoiding that is [specific process]. We also [accountability mechanism]."
```

### Red Flags to Watch For
- Vague answers about budget or timeline (low intent)
- "Just exploring" with no urgency driver
- Decision-maker not in the meeting and no path to them
- Comparing on price alone
- Unrealistic expectations for budget

### Green Flags to Celebrate
- Specific pain points with urgency
- Decision-maker present or scheduled for next call
- Budget range aligned with services
- Asking detailed questions about process and team
- Referencing competitors or previous agency experience (knows the market)

## Phase 6: Output

Return structured JSON:

```json
{
  "meeting_date": "2026-03-10T14:00:00+05:30",
  "meeting_type": "discovery",
  "contact": {
    "name": "Rahul Sharma",
    "title": "Head of Ecommerce",
    "company": "BrandX",
    "linkedin": "https://linkedin.com/in/rahulsharma",
    "communication_style": "data-driven, semi-formal",
    "personal_hooks": ["IIM Bangalore alum", "posted about D2C growth last week"]
  },
  "company": {
    "name": "BrandX",
    "industry": "Sports Equipment D2C",
    "size": "50-100 employees",
    "platform": "Shopify Plus",
    "icp_fit": "HIGH",
    "icp_segment": "Midmarket D2C India",
    "recent_news": ["Launched new product line in Feb", "Series A in Dec 2025"],
    "pain_indicators": ["Basic product pages", "No CRO visible", "Slow mobile load"]
  },
  "crm_status": "Lead",
  "pipeline_stage": "Discovery",
  "previous_interactions": "2 emails exchanged, opened case study PDF",
  "agenda": {
    "duration_minutes": 30,
    "sections": [
      {"title": "Rapport", "duration": 3, "notes": "Reference their new product launch"},
      {"title": "Discovery Questions", "duration": 15, "key_questions": ["Current CRO setup?", "Biggest conversion challenge?", "Q2 goals?"]},
      {"title": "Value Bridge", "duration": 7, "case_study": "Kibi Sports CRO"},
      {"title": "Next Steps", "duration": 5, "goal": "Book proposal call with founder"}
    ]
  },
  "talking_points": [
    "Reference Series A -- growth mode, store needs to match ambition",
    "New product line = opportunity for catalog optimization",
    "Kibi Sports parallel -- similar stage, 18% conversion lift"
  ],
  "objection_handlers": {
    "price": "ROI math with Kibi Sports numbers",
    "timing": "Pre-season prep argument",
    "in_house": "Complement their team on CRO specifically"
  },
  "recommended_ask": "Book 45-min proposal presentation with founder and Head of Ecommerce",
  "risk_factors": ["No founder in first call", "Early-stage may have tight budget"],
  "generated_at": "2026-03-10T09:00:00Z"
}
```

Also output a human-readable briefing:

```
MEETING BRIEFING
[Contact] at [Company] -- [Meeting Type]
[Date/Time]
===

QUICK FACTS:
- [3-4 bullet points: role, company, ICP fit, key signal]

AGENDA:
[Structured agenda with timing]

TOP 5 TALKING POINTS:
1. [point]
2. [point]
3. [point]
4. [point]
5. [point]

LIKELY OBJECTIONS:
- [objection]: [handler summary]

YOUR ASK:
[What you want to walk away with]

WATCH FOR:
- Red flags: [list]
- Green flags: [list]
```

## Phase 7: Review

Present the briefing for user review.

**APPROVAL GATE**: "Meeting briefing ready. Anything to adjust before your call?"

After the meeting, prompt:
- "How did the meeting go? I'll update the CRM with notes and next steps."
- Update CRM via `crm-writer` with meeting outcome, notes, and next action.

## Example Usage

Trigger phrases:
- "Prep me for my call with Rahul at BrandX"
- "Meeting prep for tomorrow's discovery call"
- "Research [person] at [company] before our meeting"
- "I have a call with [prospect] in an hour, brief me"
- "Generate talking points for my meeting with [client]"
- "Prep the QBR meeting with [client]"
