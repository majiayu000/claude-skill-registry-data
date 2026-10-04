---
name: agency-setup
description: >
  Interactive onboarding wizard that generates agency.config.json for any B2B
  agency. Asks structured questions about the agency, services, ICP, tools,
  outreach preferences, and CRM setup. Outputs a complete config file.
tags: [onboarding, setup]
---

# Agency Setup

Interactive onboarding wizard that generates your `agency.config.json`. This is the first skill you run -- every other skill reads from this config.

## Prerequisites

None. This is the starting point.

## Phase 0: Welcome

Explain to the user:
"I'm going to ask you a series of questions to configure your B2B GTM skills. This generates an `agency.config.json` file that every other skill reads from. Takes about 5 minutes."

## Phase 1: Agency Basics

Ask these questions:

1. **Agency name** -- "What's your agency/company name?"
2. **Domain** -- "What's your website domain?" (e.g., plasho.com)
3. **Founder name** -- "Who should outreach be signed by?"
4. **Tagline** -- "One-liner describing what you do?" (e.g., "Shopify agency for D2C brands")
5. **Location** -- "Where is your agency based?"

## Phase 2: Services

Ask:
6. **Services** -- "List your core services (e.g., Shopify development, CRO, performance marketing). I'll help you define search keywords for each."

For each service mentioned, generate relevant search keywords automatically. Present them for approval:
- Primary keywords (exact match for your service)
- Secondary keywords (broader category)

## Phase 3: Ideal Customer Profile (ICP)

Ask:
7. **Target markets** -- "Which geographic markets do you sell to?" (e.g., India, US, UK)
8. **Company sizes** -- "What size companies are your best clients?" (e.g., 10-50 employees, 50-200)
9. **Industries** -- "What industries do your best clients come from?" (e.g., D2C, SaaS, Retail)
10. **Decision maker titles** -- "Who do you typically sell to? Job titles?" (e.g., Founder, Head of Ecommerce, VP Marketing)
11. **ICP description** -- "In one sentence, describe your ideal client" (e.g., "Post-PMF D2C brands looking to scale their Shopify store")

Auto-generate intent keywords and negative keywords based on their services. Present for approval.

## Phase 4: Case Studies

Ask:
12. **Case studies** -- "Do you have any client case studies or proof points? For each, tell me: client name (or anonymized), industry, what you did, and the result."

For each case study, also ask: "When should outreach reference this case study?" (e.g., "when talking to sports brands" or "for CRO discussions")

If they have no case studies yet, note that and skip. Skills will adapt by focusing on expertise and value props instead.

## Phase 5: Tool Stack

Ask about each tool category. For each, determine: which tool, what plan, API or browser access, daily limits.

13. **Lead enrichment** -- "What do you use for finding contact info? (Apollo.io free/paid, ZoomInfo, Clearbit, none)"
   - If Apollo free: set access to "browser", note Chrome automation needed
   - If Apollo paid: ask for API key env var name, set access to "api"

14. **Email validation** -- "What do you use for email validation? (ZeroBounce, NeverBounce, none)"
   - Ask about credits remaining and preferred access method

15. **Email sending** -- "What do you use for sending emails? (Gmail, Superhuman, Smartlead, Instantly, Lemlist)"
   - Ask about sending domains and warmup status
   - Ask daily sending limit

16. **LinkedIn automation** -- "What do you use for LinkedIn outreach? (Dripify, Expandi, PhantomBuster, manual)"
   - Ask daily limit

17. **CRM** -- "What CRM do you use? (Google Sheets, HubSpot, Salesforce, Pipedrive)"
   - If Google Sheets: ask for sheet ID (or offer to create new)
   - If other: ask for API key env var

18. **Browser automation** -- "Do you have Claude-in-Chrome or another browser automation tool? (Yes/No)"

## Phase 6: Outreach Preferences

Ask:
19. **Tone** -- "How should your outreach sound? (e.g., Direct and helpful, Professional and warm, Casual and friendly)"
20. **Banned phrases** -- "Any phrases to never use in outreach?" (Suggest defaults: "I hope this finds you well", "I came across", "Just checking in")
21. **Cadence** -- "How aggressive should your outreach cadence be?"
   - Suggest default 11-day cadence. Let them modify.
   - Ask about daily caps per channel.

## Phase 7: Scoring Preferences

Ask:
22. **Platform priorities** -- "Which lead sources matter most to you?" (Show list: Freelancer, Upwork, Reddit, LinkedIn, Funding News, etc.)
   - Auto-assign weights based on their ranking

23. **What makes a lead HOT?** -- "What score threshold should trigger immediate action?" (Suggest 60)
24. **Budget matters?** -- "Do budget signals matter for scoring?" (If yes, ask for tiers)

## Phase 8: Generate Config

1. Compile all answers into `agency.config.json` format
2. Present the complete config for review
3. After user approves, write to `agency.config.json` at repo root
4. Also save a copy to `skills/capabilities/agency-setup/configs/{agency-name}.json`

## Phase 9: Next Steps

Tell the user:
"Your config is ready. Here's what to do next:
1. Run `/crm-setup` to initialize your CRM with the right tabs and headers
2. Run `/signal-scanner` to find your first leads
3. Run `/lead-enrichment-pipeline` to research and enrich those leads
4. Run `/outreach-draft-pipeline` to generate personalized outreach"

## Example Configs

See `configs/plasho.json` for a complete reference config from a Shopify agency.
