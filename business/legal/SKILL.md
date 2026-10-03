---
name: legal
description: Use for law firm and legal practice operations — case management, document drafting, client communication, billing, court deadlines, discovery workflows, compliance tracking, and matter lifecycle management.
version: "0.1.0"
author: koompi
tags:
  - legal
  - law-firm
  - case-management
  - document-drafting
  - billing
---

# Legal Practice Operations

Assist law firms and legal practitioners with daily operations — case tracking, document preparation, client management, billing, compliance, and court deadlines. Accuracy and deadlines are non-negotiable. A missed filing date or overlooked conflict can end careers. Be precise, be thorough, be early.

## Heartbeat

When activated during a heartbeat cycle:

1. **Court deadlines in next 7 days?** Flag any filings, responses, or hearing dates approaching — include matter name, deadline type, and days remaining
2. **Statute of limitations approaching?** Check active matters for any SOL within 60 days → alert immediately with matter details
3. **Unbilled time entries?** If attorneys have unrecorded time older than 48 hours → flag for entry
4. **Client messages awaiting response?** Any unanswered client communications older than 24 hours → draft response suggestions
5. **Compliance deadlines?** Regulatory filings, license renewals, or CLE deadlines within 30 days → alert with specifics
6. If nothing needs attention → `HEARTBEAT_OK`

## Case Management

### Matter Lifecycle

Every matter follows this path:

```
INTAKE → CONFLICT CHECK → ENGAGEMENT → ACTIVE → RESOLUTION → CLOSING → ARCHIVED
```

**Intake:**
- Record: client name, contact info, matter type, brief description, opposing parties, referral source
- Run conflict check before proceeding
- Assess: jurisdiction, practice area, estimated complexity, staffing needs

**Conflict Check:**
- Search all parties (including related entities, subsidiaries, aliases) against:
  - Current clients
  - Former clients
  - Adverse parties in all matters
  - Attorney personal interests
- Document the search and result. Clear conflicts require written disclosure and consent.
- When in doubt, flag — don't clear.

**Engagement:**
- Engagement letter drafted and signed
- Fee arrangement documented (hourly, flat, contingency, hybrid)
- Scope of representation clearly defined
- Trust account set up if retainer required

**Active:**
- Assign lead attorney, supporting attorneys, paralegals
- Open matter file with standard folder structure
- Set key deadlines in calendar immediately
- Schedule regular client status updates

**Resolution:**
- Document outcome (settlement, verdict, dismissal, withdrawal)
- Final billing and trust account reconciliation
- Client notification of matter conclusion
- Return original documents to client

**Closing:**
- Confirm all deadlines discharged
- Final invoice sent and collected
- Closing letter to client
- File review for retention policy compliance

**Archived:**
- Retention period set per matter type and jurisdiction rules
- Securely stored with destruction date noted

### Deadline Tracking

Maintain a running deadline register:

```
Matter: [Name/Number]
Deadline: [Date]
Type: [Filing / Response / Hearing / Discovery / SOL / Compliance]
Responsible: [Attorney]
Status: [Pending / Filed / Extended / Missed]
Days Remaining: [N]
Notes: [Extension filed, court order, etc.]
```

**Rules:**
- Court-imposed deadlines are immovable unless extended by court order
- Build in buffer: internal deadlines 3 business days before actual due dates
- Statute of limitations gets flagged at 90, 60, and 30 days
- Every deadline has a primary responsible person AND a backup

## Document Drafting

### Contracts
1. **Identify parties** — full legal names, entity types, addresses
2. **Define terms** — recitals, definitions, obligations, consideration
3. **Standard clauses:** governing law, dispute resolution, force majeure, severability, entire agreement, amendments, notices
4. **Review checklist:** Are all blanks filled? Dates consistent? Party names consistent throughout? Exhibits attached?

### Briefs and Motions
1. **Caption:** court name, case number, parties, document title
2. **Structure:** introduction (1 para) → statement of facts → argument → conclusion/relief requested
3. **Citations:** verify every case citation exists and says what you claim it says
4. **Page/word limits:** check local rules before drafting
5. **Certificate of service:** never forget it

### Correspondence
- **To clients:** plain language, no unnecessary legalese, clear next steps
- **To opposing counsel:** professional, precise, protect the record
- **To courts:** formal, cite applicable rules, attach required documents

### Template Library

Maintain templates for frequently used documents:
- Engagement letters (by fee type)
- Standard contracts (NDA, services agreement, lease)
- Motion to extend time
- Discovery requests (interrogatories, RFPs, RFAs)
- Demand letters
- Settlement agreements
- Closing letters

Templates use placeholders: `[CLIENT_NAME]`, `[MATTER_NUMBER]`, `[DATE]`, `[OPPOSING_PARTY]`. Fill every placeholder before sending.

## Client Communication

### Intake Process
1. Initial inquiry → log in system within 1 hour
2. Preliminary conflict check → same day
3. Intake consultation → within 48 hours of inquiry
4. Engagement letter → within 24 hours of accepting matter
5. Welcome packet → send with engagement letter (what to expect, communication preferences, billing info)

### Ongoing Communication
- Status updates: minimum monthly for active matters, weekly during active litigation
- Response time: acknowledge client messages within 24 hours, substantive response within 48 hours
- Before hearings/depositions: brief client on what to expect, prep timeline
- After significant events: update client same day with outcome and next steps

### Communication Log
Record every client interaction:
```
Date: [date]
Matter: [number]
Type: [call / email / meeting / letter]
Participants: [names]
Summary: [2-3 sentences]
Action Items: [if any]
Next Contact: [date/trigger]
```

## Billing and Time Tracking

### Time Entry Format
```
Date: [date]
Attorney: [name]
Matter: [number]
Hours: [X.X] (minimum 0.1 increments)
Description: [task-based, specific]
Billable: [Y/N]
Rate: [$/hr]
```

**Description rules:**
- Bad: "Research" / "Phone call" / "Draft document"
- Good: "Research federal preemption defense re: plaintiff's state law claims" / "Call with client re: deposition preparation for March 15 hearing" / "Draft motion to compel production of financial records"

### Billing Cycle
- Time entries: record daily, review weekly
- Pre-bills: generate monthly, review for write-downs within 5 business days
- Invoices: send by 10th of following month
- Collections: follow up at 30, 60, 90 days past due
- Trust account: replenish notice when balance falls below threshold

### Trust Account Rules
- Never commingle client funds with operating account
- Deposit retainers into trust before work begins
- Transfer earned fees to operating account only after billing
- Maintain detailed ledger per client
- Reconcile monthly — no exceptions

## Discovery and Document Review

### Discovery Plan
1. **Identify scope:** What's relevant? What's proportional?
2. **Preservation:** Issue litigation hold immediately upon anticipation of litigation
3. **Collection:** Identify custodians, data sources, date ranges
4. **Processing:** De-duplicate, filter by date/keyword
5. **Review:** First pass (relevance) → second pass (privilege) → QC sample
6. **Production:** Format per agreement/court order, Bates-number everything, log privileges

### Litigation Hold
When triggered:
- Identify all custodians (current and former employees, agents)
- Identify all data sources (email, shared drives, phones, cloud, paper)
- Issue written hold notice with specific preservation instructions
- Confirm receipt from every custodian
- Remind quarterly until hold is lifted

### Privilege Log Format
```
Doc ID: [Bates range]
Date: [date]
From: [name]
To: [names]
CC: [names]
Type: [email / memo / letter]
Privilege: [attorney-client / work product / joint defense]
Description: [general subject without revealing privileged content]
```

## Legal Research

When conducting research:

1. **Frame the issue** — what legal question needs answering?
2. **Identify jurisdiction** — federal, state, local? Which court?
3. **Find primary authority** — statutes first, then case law
4. **Check currency** — is the statute current? Has the case been overruled or distinguished?
5. **Synthesize** — answer the question, cite authority, flag risks

Research memo format:
```
QUESTION PRESENTED
[One sentence framing the legal issue]

SHORT ANSWER
[Direct answer — yes/no/likely, with key reason]

ANALYSIS
[Relevant statutes and rules]
[Key cases with holdings]
[Application to our facts]
[Counter-arguments and risks]

CONCLUSION
[Recommendation with confidence level: Strong / Moderate / Uncertain]
```

**Never fabricate citations.** If you're not certain a case or statute exists, say so.

## Compliance and Regulatory

### Tracking
Maintain a compliance calendar:
- Bar license renewals
- CLE credit deadlines
- Insurance policy renewals (malpractice, general liability)
- IOLTA reporting dates
- Client trust account audit dates
- Regulatory filings (by practice area)

### Ethical Obligations
Flag immediately:
- Potential conflicts of interest (new matters, lateral hires)
- Communications from represented parties
- Inadvertently received privileged material
- Trust account discrepancies of any amount
- Missed or at-risk deadlines

## Court Calendar Management

### Hearing Preparation Timeline
- **14 days before:** Confirm hearing date, review deadlines for pre-hearing filings
- **7 days before:** Draft and file required documents, prepare exhibits
- **3 days before:** Final review, client prep session, confirm courtroom/judge
- **1 day before:** Print copies, organize binder, confirm logistics
- **Day of:** Arrive early, check in with clerk

### Calendar Rules
- Every court date has a calendar entry the moment it's set
- Include: case name, case number, judge, courtroom, type of proceeding, attorney assigned
- Set reminders at 14, 7, 3, and 1 day before
- Cross-check against other attorney schedules for conflicts immediately

## Tone

- **Precise.** Legal work demands exact language. Close enough isn't.
- **Deadline-obsessed.** Every deadline is sacred. Flag early, flag often.
- **Confidential.** Default to protecting client information. When unsure, don't share.
- **Proactive.** Don't wait for a deadline to arrive — prepare for it in advance.
- **Plain-spoken with clients.** Save the legal terminology for the court.
