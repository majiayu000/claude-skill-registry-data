---
name: champion-tracker
description: Track key contacts who change jobs and draft warm outreach to movers at ICP companies
tags: [champions, job-changes, relationship, outreach, networking]
---

# Champion Tracker

Monitors a list of champion contacts (past buyers, advocates, warm contacts, conference connections) for job changes. When a champion moves to a new company matching ICP, the skill scores the new company's fit, researches their needs, and drafts warm "congrats on the new role" outreach. The warmest leads in B2B come from past relationships at new companies.

## Prerequisites

- `agency.config.json` in the project root
- Champion list: contacts to monitor (stored in config, CRM, or provided by user)
- WebSearch tool for LinkedIn and career change monitoring
- Optional: `company-researcher` for new-company analysis
- Optional: `cold-email-drafter` for email generation (note: these are warm, not cold)

## Capabilities Used

1. `company-researcher` -- for researching the champion's new company
2. `person-researcher` -- for updated contact details at new company
3. `lead-scorer` -- for scoring the new company against ICP
4. `crm-writer` -- for updating CRM with job change data

## Phase 0: Read Config

1. Read `agency.config.json` from the project root.
2. Extract ICP definition:
   - `icp.segments[]` -- for matching new companies
   - `icp.geography` -- target geographies
   - `icp.company_size` -- target size range
3. Extract `services[]` for mapping to new company needs.
4. Extract `case_studies[]` for proof points (especially the champion's own results if they were a past client).
5. Check for `champions[]` in config:
   ```json
   {
     "champions": [
       {
         "name": "John Smith",
         "linkedin": "https://linkedin.com/in/johnsmith",
         "relationship": "past_buyer",
         "last_company": "Acme Corp",
         "last_title": "Head of E-commerce",
         "notes": "Closed $75K deal, great results, strong advocate",
         "last_checked": "2024-02-15"
       }
     ]
   }
   ```
6. If no champions in config, pull from CRM (look for contacts tagged as champion, advocate, or past buyer).

## Phase 1: Build Champion List

If no champion list exists, help the user build one:

**Champion categories:**
```
CHAMPION TYPES
===
1. Past buyers -- people who purchased your services at a previous company
2. Past evaluators -- people who went through your sales process but didn't buy (friendly no)
3. Advocates -- people who have referred you or spoken positively about your work
4. Conference connections -- people you've met at events with warm rapport
5. Content engagers -- people who regularly engage with your content
6. Industry friends -- people in your network with relevant titles at target companies
```

**For each champion, collect:**
- Full name
- LinkedIn URL
- Current company and title
- Relationship type (past buyer, advocate, etc.)
- History notes (what you did together, results achieved)
- Last interaction date
- Email (if known)

## Phase 2: Search for Job Changes

For each champion on the list, check for recent job changes:

**Search queries (via WebSearch):**
```
- "[Champion Name]" site:linkedin.com
- "[Champion Name]" "new role" OR "excited to announce" OR "joined" [current_year]
- "[Champion Name]" "[Last Known Company]" -- verify still there or moved
- "[Champion Name]" "Head of" OR "Director" OR "VP" [current_year]
```

**Detection methods:**
1. LinkedIn profile check -- compare current title/company to stored data
2. LinkedIn post search -- "excited to announce" or "new chapter" posts
3. News search -- "[name] joins [company]" or "[company] hires [name]"
4. Company page check -- search new employee announcements

For each champion, determine status:
```
STATUS: [Champion Name]
===
Previous: [title] at [company]
Current: [title] at [new company] -- MOVED (detected [date])
  OR
Current: [same title] at [same company] -- NO CHANGE
  OR
Current: UNKNOWN -- could not determine current position
```

## Phase 3: Analyze New Companies

For each champion who has moved, research their new company:

**Company analysis:**
```
NEW COMPANY PROFILE: [Company Name]
===
Website: [URL]
Industry: [sector]
Size: [employees, revenue estimate]
Platform: [Shopify / other -- check their store]
Geography: [HQ location]

ICP match:
- Industry fit: [match/partial/miss]
- Size fit: [match/partial/miss]
- Geography fit: [match/partial/miss]
- ICP score: [0-100]

Current state:
- Website/store quality: [basic/decent/polished]
- Issues visible: [list any obvious problems]
- Recent activity: [new products, campaigns, growth signals]

Champion's likely mandate:
- Role: [their new title]
- Probable priorities: [what someone in this role at this stage company focuses on]
- Budget authority: [likely/possible/unlikely]
- Decision timeline: [first 90 days is the sweet spot]
```

## Phase 4: Score and Prioritize

Score each mover on outreach priority:

```
CHAMPION MOVER SCORING
===
Champion       | Relationship | New Company ICP | Role Level | Timing    | Score
---------------|-------------|-----------------|------------|-----------|------
John Smith     | Past buyer  | 95 (strong)     | Director   | 2 weeks   | 96
Sarah Jones    | Advocate    | 80 (good)       | Manager    | 1 month   | 82
Mike Chen      | Conference  | 70 (fair)       | VP         | 3 months  | 68
Lisa Wang      | Evaluator   | 90 (strong)     | Head of    | 1 week    | 88
```

**Scoring weights:**
- Relationship strength: 30%
  - Past buyer: 100 points
  - Advocate/referrer: 85 points
  - Friendly evaluator: 70 points
  - Conference connection: 60 points
  - Content engager: 50 points
- New company ICP fit: 25%
- Role seniority and budget authority: 20%
- Timing (recency of move, 0-90 days preferred): 25%
  - Under 30 days: 100 points
  - 30-60 days: 80 points
  - 60-90 days: 60 points
  - Over 90 days: 30 points

## Phase 5: Draft Warm Outreach

For each champion mover at an ICP company, draft personalized outreach:

**Tone: warm and congratulatory, not salesy.** These are relationships, not cold prospects.

**Email template structure:**
```
Subject: Congrats on [Company Name]!

"Hey [First Name],

Saw you joined [Company] as [Role] -- congrats! That's a great move.

[Personal reference to shared history: "Loved working with you at [Old Company]"
or "Great catching up at [event]" or "Still impressed by the [result] we got
at [Old Company]."]

[Light observation about new company: "I took a look at [Company]'s store --
there's a lot of potential there" or "[Company] is doing interesting things
in [space]."]

[Soft bridge]: "If you're looking at [service area] as you settle in,
I'd love to share what's been working for similar brands lately."

No pressure at all -- just wanted to say congrats and reconnect.

[Sign-off]"
```

**What NOT to do:**
- Do not pitch in the first message
- Do not list services or pricing
- Do not send a calendar link in message one
- Do not reference their old company's problems
- Do not make it about you

**Generate for each mover:**
1. Personal email (warm, conversational)
2. LinkedIn message (shorter, more casual)
3. Suggested follow-up for 2 weeks later (if no response)

## Phase 6: Output

Return structured JSON:

```json
{
  "champion_tracker": {
    "scan_date": "2024-03-15",
    "champions_monitored": 25,
    "movers_detected": 4,
    "icp_matches": 3,
    "results": [
      {
        "champion": {
          "name": "John Smith",
          "linkedin": "URL",
          "relationship": "past_buyer",
          "history": "Closed $75K deal at Acme Corp, 40% conversion lift"
        },
        "previous": {
          "company": "Acme Corp",
          "title": "Head of E-commerce"
        },
        "current": {
          "company": "NewBrand Co",
          "title": "VP of Digital",
          "start_date": "2024-03-01",
          "days_in_role": 14
        },
        "new_company_analysis": {
          "website": "https://newbrand.co",
          "icp_score": 95,
          "platform": "Shopify",
          "store_quality": "basic",
          "issues": ["default theme", "no CRO optimization", "poor mobile experience"],
          "predicted_needs": ["store revamp", "CRO", "performance marketing"]
        },
        "outreach_priority_score": 96,
        "outreach": {
          "email_subject": "Congrats on NewBrand!",
          "email_body": "",
          "linkedin_message": "",
          "follow_up_email": ""
        }
      }
    ],
    "no_change": 20,
    "unknown_status": 1,
    "summary": {
      "high_priority_movers": 2,
      "top_opportunity": "John Smith moved to NewBrand Co as VP Digital -- past buyer, strong ICP match",
      "next_scan_recommended": "2024-03-29"
    }
  }
}
```

Update CRM via `crm-writer`:
- Update champion's company and title in existing record
- Create new lead entry for the new company
- Tag source as "champion_job_change"
- Note the relationship history for context

## Phase 7: Ongoing Monitoring

Set up recurring scan cadence:
- **Bi-weekly scan**: check all champions for job changes
- **Immediate alerts**: if a past buyer moves to a strong ICP company
- **Quarterly list refresh**: add new champions, remove inactive contacts

After each scan, update `last_checked` date for each champion in config or CRM.

## Example Usage

**Trigger phrases:**
- "Check if any of our champions changed jobs"
- "Run the champion tracker"
- "Did any past clients move to new companies?"
- "Track job changes for our key contacts"
- "Any warm leads from job changes this month?"

```
User: Check if any champions changed jobs
Assistant: [reads champion list from config/CRM, searches LinkedIn for each, finds 4 movers, 3 at ICP companies, drafts warm congratulatory outreach for each with personalized references to shared history, logs new company leads to CRM]
```

```
User: John Smith just moved to NewBrand -- draft outreach
Assistant: [researches NewBrand, checks ICP fit (95 score), reviews history with John ($75K deal, 40% lift), drafts warm email referencing their past work together and a subtle observation about NewBrand's store]
```

```
User: Add these 5 people to the champion list
Assistant: [adds contacts to champions config with relationship type, last known company, notes, and today's date as baseline, runs first scan immediately]
```
