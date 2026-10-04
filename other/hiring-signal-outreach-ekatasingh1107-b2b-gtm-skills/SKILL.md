---
name: hiring-signal-outreach
description: Outreach triggered by hiring signals that indicate need for agency services
tags: [hiring, signals, outreach, prospecting, trigger-based]
---

# Hiring Signal Outreach

Monitors job postings and hiring activity from ICP companies for roles that indicate a need for agency services. When a company hires an "ecommerce manager" or "head of digital," they likely need external help during the transition. This skill identifies those signals, researches company context, scores fit, and drafts outreach referencing the hire or open role.

## Prerequisites

- `agency.config.json` in the project root
- WebSearch tool for job board and LinkedIn searches
- Optional: `company-researcher` for deep company analysis
- Optional: `person-researcher` for finding the hiring manager
- Optional: `cold-email-drafter` for polished email generation

## Capabilities Used

1. `company-researcher` -- for researching hiring companies
2. `person-researcher` -- for identifying the hiring manager or new hire
3. `cold-email-drafter` -- for generating polished outreach emails
4. `lead-scorer` -- for scoring the company against ICP
5. `crm-writer` -- for logging qualified leads to CRM

## Phase 0: Read Config

1. Read `agency.config.json` from the project root.
2. Extract ICP definition:
   - `icp.segments[]` -- target segments
   - `icp.geography` -- target geographies
   - `icp.company_size` -- target company sizes
3. Extract `services[]` -- to map job roles to service needs.
4. Extract `outreach.tone` for email drafting.
5. Extract `case_studies[]` for relevant proof points.
6. Define hiring signal roles (if not in config):
   ```
   High-signal roles (directly indicate agency need):
   - Ecommerce Manager / Director
   - Head of Digital / Digital Marketing Manager
   - Shopify Developer (might outsource while hiring)
   - Brand Manager
   - Growth Marketing Manager
   - D2C / DTC Manager
   - VP of E-commerce

   Medium-signal roles (indirectly indicate growth):
   - Marketing Manager
   - CRO Specialist
   - Performance Marketing Manager
   - Product Manager (e-commerce)
   - UX Designer (e-commerce focus)

   Low-signal roles (general growth indicator):
   - CMO / VP Marketing
   - Head of Sales
   - Operations Manager
   ```

## Phase 1: Search for Hiring Signals

Search job boards and LinkedIn for ICP companies with relevant open roles:

**Search queries (via WebSearch):**
```
- "[role_title] job [industry] [geography]"
- "ecommerce manager" OR "head of digital" site:linkedin.com/jobs [geography]
- "Shopify" "ecommerce" job posting [industry] [geography]
- site:lever.co OR site:greenhouse.io "[industry]" "[role_title]"
- "[company_name]" hiring "ecommerce" OR "digital marketing"
- "D2C" OR "DTC" "[role_title]" job [geography] [current_month]
```

**Job boards to search:**
- LinkedIn Jobs
- Wellfound (AngelList)
- Lever / Greenhouse job pages
- Indeed
- Naukri (for India)
- Glassdoor

For each job posting found, extract:
```
Company: [name]
Role: [job title]
Location: [city, country]
Posted: [date]
Job description highlights:
  - [Key responsibility 1]
  - [Key responsibility 2]
  - [Technology mentioned: Shopify, Magento, etc.]
Seniority: [entry/mid/senior/director]
Source: [job board URL]
```

## Phase 2: Analyze the Hiring Signal

For each job posting, determine what it reveals about the company's needs:

**Signal interpretation framework:**

| Role Being Hired | What It Tells Us | Our Opportunity |
|-----------------|------------------|-----------------|
| Ecommerce Manager (new role) | Building e-commerce function from scratch | Need agency to set up and run while they onboard |
| Ecommerce Manager (replacement) | Previous person left, gap in execution | Need agency to fill gap and potentially train new hire |
| Head of Digital | Strategic shift toward digital | Need agency for execution while leader sets strategy |
| Shopify Developer | Technical debt or new build | Might outsource to agency instead of/while hiring |
| Growth Marketing Manager | Scaling phase, need marketing support | Need agency for specialized channels they lack in-house |
| CRO Specialist | Conversion problems, aware of CRO need | Warm to CRO services, might hire agency as alternative |

```
SIGNAL ANALYSIS: [Company Name]
===
Role: Ecommerce Manager
Signal strength: HIGH
Interpretation: Company is building e-commerce capability. The new hire will need
  agency support during first 90 days to execute while they learn the business.

Gap period: 30-90 days (from posting to hire being fully productive)
  This is the window where agency help is most valuable.

Service opportunity:
1. [Service] -- [why they need it based on the role description]
2. [Service] -- [what the job posting mentions that maps to this service]
```

## Phase 3: Research Company Context

For each high-signal company, gather context:

**Research via WebSearch and company-researcher:**
```
COMPANY PROFILE: [Company Name]
===
Website: [URL]
Industry: [sector]
Size: [employees, revenue estimate]
Platform: [Shopify / Magento / Custom -- check their store]
Current store quality: [basic / decent / polished]
Recent activity:
  - [Recent press, launches, campaigns]
  - [Social media presence and activity]
  - [Content marketing efforts]

Existing team:
  - Current team on LinkedIn: [ecommerce/marketing headcount]
  - Other open roles: [what else they're hiring for]
  - Recent hires: [who joined recently -- indicates where they're investing]

Why they're hiring:
  - [Growth signal: expanding team]
  - [Replacement: someone left]
  - [New function: first hire in this area]
```

## Phase 4: Score and Rank

Score each lead:

```
HIRING SIGNAL LEADS
===
Company       | ICP Score | Signal | Role Gap Window | Service Match | Total
--------------|-----------|--------|-----------------|---------------|------
BrandCo       | 90        | HIGH   | 60 days         | 3 services    | 92
StyleUp       | 85        | HIGH   | 45 days         | 2 services    | 84
FitGear       | 75        | MEDIUM | 30 days         | 2 services    | 70
TechStore     | 60        | LOW    | N/A             | 1 service     | 45
```

**Scoring weights:**
- ICP fit: 30%
- Signal strength (role relevance): 25%
- Gap window size (urgency): 20%
- Service match count: 25%

## Phase 5: Draft Personalized Outreach

For each qualified lead, draft outreach referencing the hiring signal:

**Two outreach approaches:**

**Approach 1: Outreach to the hiring manager (before hire is made)**
```
Subject: [Role] hiring -- we can help bridge the gap

"Noticed you're hiring a [role] at [Company]. Smart move as you scale.

Until that person is fully up to speed (usually 60-90 days), you'll still need
[service] running at full capacity.

We helped [similar company] during exactly this transition -- [case study result].

Would it make sense to chat about bridging that gap?"
```

**Approach 2: Outreach to the new hire (after they start)**
```
Subject: Congrats on the new role at [Company]

"Congrats on joining [Company] as [role].

Most [role]s in their first 90 days need to show quick wins while building
the long-term strategy. We specialize in [service] for [industry] brands
and can help you hit the ground running.

We got [similar company] a [specific result] in their first quarter with us.

Worth a quick look?"
```

Generate for each lead:
1. Email to hiring manager (if role is still open)
2. Email to new hire (if someone was recently hired into the role)
3. LinkedIn connection note
4. LinkedIn follow-up message

## Phase 6: Output

Return structured JSON:

```json
{
  "hiring_signal_outreach": {
    "search_date": "2024-03-15",
    "search_criteria": {
      "roles_monitored": ["Ecommerce Manager", "Head of Digital", "Shopify Developer"],
      "industries": ["D2C", "e-commerce", "retail"],
      "geographies": ["India", "US", "UK"],
      "job_boards": ["LinkedIn", "Wellfound", "Indeed"]
    },
    "signals_found": 22,
    "icp_matches": 10,
    "qualified_leads": [
      {
        "company": "BrandCo",
        "website": "https://brandco.com",
        "role_hiring": "Ecommerce Manager",
        "role_posted_date": "2024-03-08",
        "signal_strength": "high",
        "icp_score": 92,
        "gap_window_days": 60,
        "interpretation": "Building ecommerce function, first hire in this area",
        "service_matches": ["Shopify development", "CRO", "catalog management"],
        "current_store": {
          "platform": "Shopify",
          "quality": "basic",
          "issues_spotted": ["default theme", "no reviews", "slow mobile"]
        },
        "contacts": {
          "hiring_manager": {
            "name": "",
            "title": "CMO",
            "linkedin": "",
            "email": ""
          },
          "new_hire": null
        },
        "outreach": {
          "to_hiring_manager": {
            "subject": "",
            "body": ""
          },
          "linkedin_note": "",
          "linkedin_message": ""
        }
      }
    ],
    "summary": {
      "total_qualified": 6,
      "high_signal": 3,
      "medium_signal": 3,
      "top_opportunity": "BrandCo -- hiring Ecommerce Manager, basic Shopify store, 3 service matches"
    }
  }
}
```

Log qualified leads to CRM via `crm-writer` with source tagged as "hiring_signal."

## Example Usage

**Trigger phrases:**
- "Find companies hiring ecommerce roles"
- "Search for hiring signals in D2C brands"
- "Which companies are looking for Shopify developers?"
- "Hiring signal outreach for this week"
- "Find companies that just hired a head of digital"

```
User: Find D2C companies hiring ecommerce managers
Assistant: [searches LinkedIn and job boards for ecommerce manager roles at D2C companies, finds 22 postings, filters to 6 ICP matches, analyzes gap windows and service needs, drafts personalized outreach for hiring managers referencing the specific role and company's current store gaps]
```

```
User: Any companies just hired someone we should reach out to?
Assistant: [searches for recent hire announcements on LinkedIn, identifies 4 new ecommerce/digital hires at ICP companies, drafts "congrats on the new role" outreach with quick-win positioning]
```
