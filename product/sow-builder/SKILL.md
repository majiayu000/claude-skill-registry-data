---
name: sow-builder
description: >
  Generate scoped Statements of Work (SOWs) with embedded business cases for Solum Health
  prospects. Pulls real data from Fireflies (call transcripts), HubSpot (deal records, emails),
  and Apollo (company enrichment), then cross-references all sources to produce an accurate,
  conservative proposal. Use this skill when the user says "build a SOW", "create a proposal",
  "SOW", "statement of work", "scope of work", "write a proposal", "build a business case",
  "SOW for [company]", "proposal for [company]", or any variation of wanting a scoped proposal
  or statement of work for a prospect or client.
---

# SOW Builder

Generate production-ready Statements of Work with embedded business cases for Solum Health
prospects. Every number is sourced, every claim is cross-referenced, and every assumption
is flagged.

## API Authentication

All data collection uses direct HTTP API calls via the Bash tool with `curl`, piped through `python3` for JSON parsing. API keys are stored in `~/.claude/.api-keys.json`.

| Service | Base URL | Auth Method | Key Path |
|---------|----------|-------------|----------|
| Fireflies | `https://api.fireflies.ai/graphql` | `Authorization: Bearer <KEY>` | `.keys.fireflies.key` |
| HubSpot | `https://api.hubapi.com` | `Authorization: Bearer <KEY>` | `.keys.hubspot.key` |
| Apollo | `https://api.apollo.io` | `X-Api-Key: <KEY>` header | `.keys["apollo.io"].key` |

To load a key at runtime:

```bash
FIREFLIES_KEY=$(python3 -c "import json; print(json.load(open('$HOME/.claude/.api-keys.json'))['keys']['fireflies']['key'])")
HUBSPOT_KEY=$(python3 -c "import json; print(json.load(open('$HOME/.claude/.api-keys.json'))['keys']['hubspot']['key'])")
APOLLO_KEY=$(python3 -c "import json; print(json.load(open('$HOME/.claude/.api-keys.json'))['keys']['apollo.io']['key'])")
```

## Core Principle

A SOW is a commitment document. Overpromise here and you lose trust, margin, or both. Every
number must be conservative. Every scope item must be validated. If data conflicts across
sources, flag it and use the lower number. The internal fact-check section exists so JP can
catch issues before sending.

## The Workflow

### Phase 0: Identify the Company

1. Get the company name from the user. If ambiguous, ask for clarification.
2. Normalize the name for searching across systems (e.g., "Supportive Care" vs "Supportive Care ABA").

### Phase 1: Data Collection

Run ALL of these in parallel where possible. The goal is to pull every data point available
before writing a single word.

#### 1A. Fireflies — Call Transcripts

Fetch all recent transcripts and filter client-side by company name:

```bash
curl -s "https://api.fireflies.ai/graphql" \
  -H "Authorization: Bearer $FIREFLIES_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "query { transcripts(mine: true, limit: 50) { id title date duration participants summary { action_items overview shorthand_bullet } } }"}' \
  | python3 -c "
import json, sys
data = json.load(sys.stdin)
for t in data.get('data', {}).get('transcripts', []):
    if '{company_name}'.lower() in t.get('title', '').lower():
        print(json.dumps(t, indent=2))
"
```

**Note:** The `date` field is Unix milliseconds. The `action_items` field is a string (not an array). Filter transcripts client-side by checking if the company name appears in the title.

Also search for key contacts by name if known.

For each matching transcript, extract:
- **Pain points** — What problems did they describe? Use their exact words.
- **Requirements** — What did they say they need? Features, integrations, workflows.
- **Volume data** — Any numbers: orders/month, claims/month, auth requests, call volumes, employee counts, patient counts, client counts.
- **Pricing discussions** — What pricing was discussed? What was their reaction?
- **Technical constraints** — What EMR do they use? Phone system? Clearinghouse? Any IT restrictions?
- **Integration needs** — What systems need to connect? APIs, SFTP, manual upload?
- **Timeline expectations** — When do they want to go live? Any deadlines?
- **Decision makers** — Who else needs to approve? Who's the champion?
- **Competitive mentions** — Are they evaluating alternatives? Who?
- **Objections raised** — What concerns came up?

#### 1B. HubSpot — Deal & Contact Records

Search for the company and related records:

```bash
# Search companies
curl -s "https://api.hubapi.com/crm/v3/objects/companies/search" \
  -H "Authorization: Bearer $HUBSPOT_KEY" \
  -H "Content-Type: application/json" \
  -d '{"filterGroups":[{"filters":[{"propertyName":"name","operator":"CONTAINS_TOKEN","value":"{company_name}"}]}],"properties":["name","domain","industry","numberofemployees","city","state","website"]}' \
  | python3 -m json.tool

# Search deals
curl -s "https://api.hubapi.com/crm/v3/objects/deals/search" \
  -H "Authorization: Bearer $HUBSPOT_KEY" \
  -H "Content-Type: application/json" \
  -d '{"filterGroups":[{"filters":[{"propertyName":"dealname","operator":"CONTAINS_TOKEN","value":"{company_name}"}]}],"properties":["dealname","dealstage","amount","closedate","pipeline"]}' \
  | python3 -m json.tool

# Search contacts
curl -s "https://api.hubapi.com/crm/v3/objects/contacts/search" \
  -H "Authorization: Bearer $HUBSPOT_KEY" \
  -H "Content-Type: application/json" \
  -d '{"filterGroups":[{"filters":[{"propertyName":"company","operator":"CONTAINS_TOKEN","value":"{company_name}"}]}],"properties":["firstname","lastname","email","jobtitle","phone"]}' \
  | python3 -m json.tool
```

Extract:
- **Deal stage** — Where are they in the pipeline?
- **Deal amount** — What's the expected value?
- **Contacts** — Names, titles, emails of all stakeholders
- **Company properties** — Industry, size, location, website
- **Notes** — Any internal notes from previous interactions
- **Associated activities** — Meetings logged, tasks, follow-ups

#### 1B-2. HubSpot — Email Thread Pull

After finding contacts in 1B, pull the actual email engagement history for each contact.
Email threads often contain requirements, specs, and follow-up questions that never come up
on calls.

**Step 1: Get contact IDs** from the search results above.

**Step 2: Pull email associations for each contact:**

```bash
# Get emails associated with a contact
curl -s "https://api.hubapi.com/crm/v3/objects/contacts/{contact_id}/associations/emails" \
  -H "Authorization: Bearer $HUBSPOT_KEY" \
  | python3 -m json.tool
```

**Step 3: Fetch each email's content:**

```bash
# Get email details (subject, body, direction, timestamp)
curl -s "https://api.hubapi.com/crm/v3/objects/emails/{email_id}?properties=hs_email_subject,hs_email_text,hs_email_html,hs_email_direction,hs_timestamp,hs_email_sender_email,hs_email_to_email" \
  -H "Authorization: Bearer $HUBSPOT_KEY" \
  | python3 -m json.tool
```

**Step 4: For large threads (10+ emails), batch the requests:**

```bash
# Batch read emails
curl -s -X POST "https://api.hubapi.com/crm/v3/objects/emails/batch/read" \
  -H "Authorization: Bearer $HUBSPOT_KEY" \
  -H "Content-Type: application/json" \
  -d '{"inputs":[{"id":"{email_id_1}"},{"id":"{email_id_2}"}],"properties":["hs_email_subject","hs_email_text","hs_email_direction","hs_timestamp"]}' \
  | python3 -m json.tool
```

From the email threads, extract:
- **Requirements shared via email** — specs, feature requests, workflow descriptions
- **Questions asked** — what clarifications did the prospect request?
- **Attachments mentioned** — any docs, spreadsheets, or screenshots referenced
- **Volume data** — numbers shared in writing (these are more reliable than verbal estimates)
- **Pricing follow-ups** — any pricing questions or counter-proposals via email
- **Timeline commitments** — dates or deadlines mentioned in writing
- **Stakeholder signals** — who was CC'd, who forwarded, who responded

**Important:** Email data is often more reliable than call transcript data because it's
written and intentional. When email data conflicts with transcript data, flag both but
give higher weight to the email version in the fact-check.

#### 1C. Apollo — Company Enrichment

Enrich the company profile:

```bash
# Enrich by domain
curl -s "https://api.apollo.io/v1/organizations/enrich?domain={company_domain}" \
  -H "X-Api-Key: $APOLLO_KEY" \
  | python3 -m json.tool
```

If domain unknown, search first:
```bash
# Search by company name
curl -s -X POST "https://api.apollo.io/v1/mixed_companies/search" \
  -H "X-Api-Key: $APOLLO_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q_organization_name":"{company_name}","per_page":5}' \
  | python3 -m json.tool
```

Extract:
- **Company size** — Employee count, headcount growth
- **Revenue** — Annual revenue or revenue range
- **Funding** — Total raised, last round, investors
- **Industry** — Primary industry, sub-industry
- **Technology stack** — What tools they use (may reveal EMR, phone system)
- **Key people** — C-suite, VP-level contacts
- **Locations** — HQ, offices, states they operate in

### Phase 2: Data Synthesis & Fact-Check

Before writing anything, perform the internal fact-check:

#### 2A. Cross-Reference Volume Numbers

Compare volume data across all sources:
- Call transcript #1 vs call transcript #2 vs email vs deal notes
- If numbers differ, document the discrepancy and use the LOWER number for business case
- Flag: "On {date} call, prospect said {X}. On {date} call, prospect said {Y}. Using {lower} for SOW."

#### 2B. Verify Pricing Alignment

Check that pricing discussed matches current Solum pricing tiers:
- Growth: $500/mo (up to ~200 clients)
- Scale: $2,500/mo (200-1,000 clients)
- Enterprise: Custom (1,000+ clients)
- Per-unit pricing: varies by service type
- Flag any pricing that was quoted but doesn't match current structure

#### 2C. Requirements Completeness Check

Build a master requirements list from ALL sources:
- Go through every call transcript and extract each requirement mentioned
- Go through every email and extract each requirement mentioned
- Go through deal notes for any requirements
- Deduplicate but don't drop — if something was mentioned once on call #1 and never again, it still belongs
- Flag requirements that may be technically impossible or need engineering scoping

#### 2D. Technical Feasibility Check

For each integration requirement:
- Is this an EMR Solum already integrates with? (Flag if unknown)
- Is this a standard clearinghouse connection? (Flag if non-standard)
- Does the phone system integration exist? (Flag if new)
- Are there any data format requirements that need validation?

### Phase 3: SOW Generation

Generate the SOW in markdown format. Use Solum Health branding guidelines from the
`solum-health-brand` skill for any PDF generation.

#### Document Structure

```markdown
## Statement of Work: {Company Name} x Solum Health
**Prepared:** {today's date} | **Version:** 1.0
**Prepared by:** JP Montoya, CEO, Solum Health
**Contact:** jp@getsolum.com | (628) 276-2659

---

### 1. Executive Summary

{2-3 paragraphs. Who they are (size, location, specialty). What they need from Solum
and why — use the specific pain points from their own calls/emails. Why now — what's
the trigger driving this decision (growth, staff turnover, compliance, cost pressure).
End with the value proposition: what Solum delivers and the expected impact.}

---

### 2. Current State & Challenges

{Use their own words from transcripts. Each challenge should be a subsection with:}

#### {Challenge 1: e.g., "Manual Prior Authorization Process"}
- **The problem:** {description using prospect's language}
- **Impact:** {quantified where possible — hours/week, error rate, revenue leakage}
- **Source:** {which call/email this came from}

#### {Challenge 2}
...

#### {Challenge N}
...

---

### 3. Why Solum Health

{This section bridges the prospect's pain (Section 2) with the solution (Section 4).
It should feel personal and credible, not like a brochure. 5-6 short paragraphs covering
the pillars below. Adapt language to the prospect's context.}

**Built by operators, for operators.** JP Montoya managed a mental health practice with
80+ providers and 20,000+ patients for four years. Solum's leadership team includes
healthcare operators and industry experts who have lived the problems this product solves.
Every feature exists because someone on the team needed it when running a practice.

**Your EHR stores data. We run the workflows.** Solum doesn't replace your EMR. We sit
on top of it and automate the administrative work your team does manually today: intake,
prior authorizations, benefits verification, referral processing, scheduling, and patient
communication. Your clinical staff stays focused on care.

**Enterprise-grade security.** Solum is built for healthcare from day one. HIPAA-compliant
infrastructure, SOC 2 controls, encrypted data at rest and in transit, role-based access,
and audit trails across every workflow. Your patient data never touches a system that
wasn't designed for it.

**Backed by top healthcare operators and funds.** Solum is backed by Y Combinator (S22)
and investors who operate in healthcare: Wisdom Venture, BAM Capital, Lionheart, Rebel
Fund, Liquid2, and Founders Club. Our investors aren't just writing checks — they bring
operational expertise, payer relationships, and industry access that accelerate the
product and our customers' outcomes.

**Forward-deploy team for successful implementation.** We don't hand you a login and
disappear. Solum deploys a dedicated implementation team that works alongside your staff
to configure workflows, map payer rules, integrate your systems, and train your team.
We stay hands-on through go-live and the first 30 days of production to make sure the
numbers land where they should.

{Add a paragraph specific to this prospect's situation — connect their top 1-2 pain
points from Section 2 to what Solum actually does for practices like theirs. Reference
similar companies by type (not name) if relevant: "We work with ABA groups processing
500+ auths/month" or "Behavioral health practices with 50+ providers use Solum to..."
Keep it concrete and operational, not aspirational.}

{If the prospect mentioned competitors on calls, add a brief differentiation paragraph
here. Do NOT name competitors directly. Instead: "Unlike tools built for hospitals or
general medical practices, Solum is purpose-built for therapy and behavioral health
workflows. Our AI assistant Annie understands the specific payer rules, authorization
requirements, and intake patterns your practice deals with daily."}

---

### 4. Scope of Work

#### Phase 1: {Name — e.g., "Prior Authorization Automation"}
**Timeline:** {weeks/months}

| Deliverable | Description | Inputs Required | Output |
|-------------|-------------|-----------------|--------|
| {item} | {what Solum delivers} | {what we need from them} | {what they get} |

**Integration Requirements:**
- {EMR connection details}
- {Phone system details}
- {Clearinghouse details}

**Explicitly NOT Included:**
- {Scope boundary 1}
- {Scope boundary 2}

#### Phase 2: {Name}
...

#### Phase 3 (if applicable): {Name}
...

---

### 5. Business Case

#### Volume Data (from {company_name})
| Metric | Value | Source |
|--------|-------|--------|
| {e.g., Monthly orders} | {number} | {call date or email date} |
| {e.g., Monthly auth requests} | {number} | {call date or email date} |
| {e.g., Current staff handling this} | {number} | {call date or email date} |

#### Current Cost Estimate
| Cost Component | Calculation | Monthly Cost |
|----------------|-------------|--------------|
| {e.g., Staff labor} | {N staff x $X/hr x Y hrs/week x 4.33} | ${amount} |
| {e.g., Overtime} | {estimate} | ${amount} |
| {e.g., Error/rework cost} | {estimate} | ${amount} |
| **Total Current Cost** | | **${total}** |

#### Projected Cost with Solum
| Component | Calculation | Monthly Cost |
|-----------|-------------|--------------|
| Solum platform fee | {tier or per-unit x volume} | ${amount} |
| Remaining staff cost (if any) | {reduced headcount estimate} | ${amount} |
| **Total with Solum** | | **${total}** |

#### ROI Summary
| Metric | Value |
|--------|-------|
| Monthly savings | ${current - projected} |
| Annual savings | ${monthly x 12} |
| Solum annual cost | ${solum monthly x 12} |
| Net annual savings | ${annual savings - annual cost} |
| ROI | {net savings / solum cost x 100}% |
| Payback period | {months to recoup implementation fee} |

*All calculations use conservative assumptions. See Section 8 for assumptions.*

---

### 6. Implementation Plan

| Phase | Timeline | Milestones | {Company} Responsibilities |
|-------|----------|------------|---------------------------|
| Kickoff & Setup | Week 1-2 | {milestones} | {what they provide} |
| Configuration | Week 3-4 | {milestones} | {what they provide} |
| Testing | Week 5-6 | {milestones} | {what they provide} |
| Go-Live | Week 7-8 | {milestones} | {what they provide} |
| Optimization | Month 3+ | {milestones} | {what they provide} |

**Go/No-Go Checkpoints:**
- After setup: confirm integrations working
- After testing: confirm accuracy meets threshold
- After 30 days: review metrics and adjust

---

### 7. Pricing

| Item | Unit | Rate | Estimated Monthly |
|------|------|------|-------------------|
| {Service line 1} | {per order / per auth / flat} | ${rate} | ${monthly} |
| {Service line 2} | {unit} | ${rate} | ${monthly} |
| **Monthly Total** | | | **${total}** |

**Implementation Fee:** ${amount} (one-time)

**Payment Terms:**
- Monthly invoicing, net 30
- Implementation fee due at kickoff
- {Any special terms discussed}

**Guarantee:** {If discussed — e.g., "30-day money-back guarantee on platform fees"}

---

### 8. Requirements & Assumptions

#### Technical Requirements
- {EMR: name, version, API access needed}
- {Phone system: type, forwarding capability}
- {Clearinghouse: name, connection type}
- {Data formats: HL7, FHIR, CSV, etc.}
- {Network/VPN requirements if any}

#### Assumptions
- {Volume assumption: using {X} orders/month based on {source}}
- {Staffing assumption: current team of {N} handling {function}}
- {Cost assumption: average hourly rate of ${X} for {role}}
- {Timeline assumption: {company} provides access within {X} days of kickoff}
- {Growth assumption: volume flat for Year 1 projections}

#### Dependencies & Risks
| Risk | Mitigation |
|------|------------|
| {e.g., EMR integration delay} | {mitigation approach} |
| {e.g., Data quality issues} | {mitigation approach} |

---

### 9. Fact-Check Notes

> **INTERNAL ONLY — Remove this section before sending to prospect.**

#### Data Discrepancies
- {Any volume numbers that differ across sources}
- {Any pricing that was quoted differently at different times}
- {Any requirements that appeared in one source but not others}

#### Assumptions Needing Validation
- {Assumptions made without direct prospect confirmation}
- {Cost estimates based on industry averages rather than their data}
- {Technical integrations not yet validated by engineering}

#### Open Questions
- {Questions that need answers before finalizing the SOW}
- {Clarifications needed from the prospect}
- {Internal decisions needed (pricing approval, timeline commitment)}

#### Unvalidated Integrations
- {Any integration mentioned that Solum hasn't confirmed it can support}
- {Any EMR/system where connectivity is assumed but not tested}
```

### Phase 4: Output & Delivery

1. **Save the SOW** as markdown to the relevant project folder:
   `~/Documents/Claude/SALES/{company-name}-sow.md`

2. **Generate a PDF** using the `/pdf` skill with Solum Health branding:
   - Font: DM Sans
   - Colors: Navy (#011C40) headers, Solum Blue (#468AF7) accents
   - Logo: Include Solum Health logo at top
   - Footer: "Confidential | Solum Health | getsolum.com"
   - Save to: `~/Documents/Claude/SALES/{company-name}-sow.pdf`

3. **Display a summary** to the user:
   - Company name and deal stage
   - Key pain points identified (top 3)
   - Total scope (number of phases, timeline)
   - Business case headline (monthly savings, ROI)
   - Data quality score (how much was sourced vs assumed)
   - Open questions that need resolving
   - Fact-check flags that need attention

4. **Ask the user:**
   - "Want me to adjust any numbers or scope items?"
   - "Should I remove the Fact-Check section and generate a client-ready version?"
   - "Any pricing changes before I finalize?"

## Rules

### Data Integrity
- NEVER fabricate volume numbers. If no data exists, write "TBD — confirm with prospect" and flag it.
- NEVER round up. If they said "about 350 orders," use 350, not 400.
- ALWAYS cite the source for every number (which call, which email, which date).
- If a number appears in multiple sources with different values, use the LOWER value and flag the discrepancy.

### Business Case Conservative
- Use the lower end of any ranges given by the prospect.
- Assume ZERO growth in Year 1 projections unless the prospect explicitly stated growth plans.
- Use conservative hourly rates for labor cost estimates ($18-25/hr for admin staff, $35-50/hr for clinical staff) unless prospect provided specific numbers.
- Do NOT include "soft" savings (improved morale, better patient experience) in the ROI calculation. Mention them qualitatively only.
- Round savings DOWN to the nearest $100.

### Scope Management
- ALWAYS include a "What's NOT Included" section for every phase.
- If a requirement was mentioned but is vague, list it as "requires scoping" rather than committing to it.
- If a prospect asked for something once in passing, include it in Requirements but note it needs confirmation.
- Custom integrations, custom reporting, and training beyond standard onboarding should be explicitly called out as included or excluded.

### Technical Honesty
- If Solum hasn't integrated with their specific EMR before, say "integration to be validated" not "we support this."
- If a phone system integration is non-standard, flag it as a risk.
- If data format requirements are unclear, list them as open questions.

### Branding
- Use Solum Health brand guidelines from the `solum-health-brand` skill for all visual formatting.
- The SOW should look professional enough to send to a VP or CFO.
- Use clean tables, clear section breaks, and consistent formatting.
- No jargon that the prospect wouldn't understand. If using a technical term, explain it.

### Privacy
- Do NOT include Fireflies transcript IDs or raw transcript text in the client-facing sections.
- The "Source" column in tables should reference "Discovery call ({date})" or "Email ({date})", not internal system references.
- The Fact-Check section (Section 8) is internal only and must be removed before sending.

## Handling Missing Data

If a data source is unavailable or returns no results:

| Source | Fallback |
|--------|----------|
| Fireflies returns no transcripts | Ask user: "I couldn't find call transcripts for {company}. Can you share the key details from your calls?" |
| HubSpot has no deal record | Proceed with available data, note "No HubSpot deal record found" in Fact-Check |
| Apollo returns no enrichment | Use company website and any data from calls. Note "Company enrichment unavailable" in Fact-Check |
| No volume data from any source | Mark all volume fields as "TBD" and flag: "Business case cannot be completed without volume data from prospect" |
| No pricing discussed yet | Use standard Solum pricing tiers based on estimated company size. Note "Pricing not yet discussed with prospect" |

## Quick Reference: Solum Pricing (2026)

Source: `~/Documents/Claude/solum-ops/sow/solum-pricing-2026.pptx` (updated April 2026)

### Authorization & Claim Follow-Up

| Monthly Commitment | Prior Auth (End-to-End) | Claim/PA Follow-Up |
|-------------------|------------------------|-------------------|
| $500 | $16/unit | $4/unit |
| $1,500 | $12/unit | $3.50/unit |
| $5,000 | $10/unit | $3/unit |
| $15,000+ | $8/unit | $2.50/unit |
| Enterprise | Custom | Custom |

Includes: document retrieval & AI classification, pre-submission QA & payer validation,
payer submission (API, portal, fax), follow-up until resolution, OCR extraction,
result posting to EHR/CRM.

### Referral Management & Document Processing

| Volume (docs/month) | Cost per Document | Extra Page (>10 pages) |
|--------------------|-------------------|----------------------|
| 99 – 999 | $1.50 | $0.05 |
| 1K – 5K | $0.80 | $0.045 |
| 5K – 10K | $0.60 | $0.04 |
| 10K – 20K | $0.45 | $0.035 |
| 20,000+ | Enterprise | Custom |

Includes: AI document type identification, data extraction & classification,
structured output delivery, multi-format support (fax, email, portal), error detection,
EHR/CRM posting.

### AI Insurance Verification

| Monthly Commitment | Eligibility Check | Benefit Check | Insurance Monitoring | Eligibility (Self-Serve) |
|-------------------|-------------------|---------------|---------------------|------------------------|
| $500 | $1.50 | $6.00 | $0.75 | $0.35 |
| $1,500 | $0.80 | $5.50 | $0.60 | $0.25 |
| $5,000 | $0.30 | $4.50 | $0.30 | $0.20 |
| $15,000+ | $0.25 | $3.50 | $0.20 | $0.15 |
| Enterprise | Custom | Custom | Custom | Custom |

Self-serve: direct platform access — prospect runs eligibility checks on demand at lower rate.

Includes: real-time payer connectivity, coverage & copay details, deductible & out-of-pocket
info, auth requirement detection, structured response data, audit trail.

### General

- **Implementation fee**: $2,000 one-time (EHR integration, payer mapping, team onboarding)
- **API usage**: not included in per-unit pricing
- **Higher commitment tiers**: unlock lower per-unit rates across all services
- **All commitment tiers**: monthly

## Important Notes

- **Direct API access to Fireflies, HubSpot, and Apollo is required. Keys stored in ~/.claude/.api-keys.json.** If any keys are missing or API calls fail, tell the user which service is unavailable and proceed with available sources.
- **This is a living document.** After generating, the user will likely want to iterate. Support edits, re-pulls, and version bumps.
- **The SOW is not a contract.** It's a scoping document. Do not include legal terms, liability clauses, or binding language. If the prospect needs a contract, that's a separate step.
- **Speed matters.** The user wants this generated quickly after calls, not days later. Optimize for fast data pulls and assembly.
