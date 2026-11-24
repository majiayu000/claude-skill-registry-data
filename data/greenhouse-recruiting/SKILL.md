---
name: "greenhouse-ats-api"
description: "Manage candidates, jobs, and pipelines in Greenhouse Recruiting. Use when creating or updating candidate records, moving stages, logging notes, building scorecards, running reports, managing structured hiring, or interacting with the Greenhouse Harvest API (v1/v2 legacy or v3 OAuth), Ingestion API, or Job Board API."
---

# Greenhouse ATS & API Skill

You are an expert Greenhouse ATS operator and API integrator. Apply these workflows whenever the user is working inside Greenhouse Recruiting or building/running Greenhouse API calls.

> **API Version Status:** We currently operate on **Harvest API v1/v2 (legacy)**. Harvest v1 and v2 are deprecated and will be unavailable after **August 31, 2026**. All new integrations should be built on v3. Existing v1/v2 integrations must be migrated before that date. Both versions are fully documented below.

---

## Greenhouse Recruiting — Core Objects

| Object | What it is |
|---|---|
| **Job** | An open role with a defined interview pipeline and scorecard |
| **Job Post** | The public-facing listing attached to a Job (can be multiple per job) |
| **Candidate** | A person in your system, potentially across multiple applications |
| **Application** | A candidate's record tied to a specific Job |
| **Prospect** | A sourced candidate not yet applied to a specific job |
| **Stage** | A step in the pipeline (Application Review, Phone Screen, Onsite, Offer) |
| **Scorecard** | Structured evaluation for a candidate at a given stage |
| **Interview Kit** | The scorecard + interview questions assigned to a specific interviewer |
| **Activity Feed** | Audit log on every Application — all notes, emails, stage changes |
| **Rejection Reason** | Required code when closing an application — powers pipeline analytics |

---

## Structured Hiring in Greenhouse — Best Practices

Greenhouse is built around **structured hiring**. Follow this philosophy:

### Job Kickoff Meeting
Before opening a role, run a kickoff meeting using the Job Setup tab. Capture:
- Role-specific competencies (what does "great" look like in this role?)
- Must-have vs. nice-to-have skills
- Deal-breaker criteria
- Interview stage design (who interviews, in what order, on what attributes)
- Target diversity sourcing channels

### Scorecard Design
- Create a scorecard for every role before sourcing begins
- Organise scorecard into **Categories** (e.g., Technical Skills, Communication, Leadership)
- Assign **focus attributes** to each interview stage so each interviewer assesses different things — never let multiple interviewers assess the same attribute
- Use the Greenhouse science-based rating system: Strong Yes / Yes / No / Strong No
- Link specific behavioural questions to each attribute within the interview kit
- Greenhouse sends automatic scorecard reminders 1 hour after each interview ends — set additional manual reminders for accountability

### Candidate Roundup Meeting
After all scorecards are submitted, run a roundup meeting (30–60 min):
- Review scorecard data attribute by attribute — not gut feelings
- Challenge vague assessments: "Can you give a behavioural example?"
- Come out with a clear go/no-go decision
- Document the decision rationale in the activity feed

### Offer Management
- Complete offer details in Greenhouse before extending verbally
- Mark candidate as Hired immediately upon acceptance — this closes the job and locks time-to-hire data

---

## Candidate Record Best Practices

- **Source tagging is mandatory** — always set source (LinkedIn, Referral, GitHub, Job Board, etc.)
- **Recruiter and Coordinator fields** — never leave blank
- **Notes must be behavioural** — what the candidate said or did, not what you felt
- **Reject with a reason code** — every rejection needs a reason; this powers funnel analytics
- **Unreject** is possible via API or UI if a candidate was mistakenly rejected
- **Custom fields** — use for role-specific data like visa status, salary expectations, relocation preference; never put these in free-text notes

---

## Greenhouse KPIs to Track

| KPI | Definition | Why it matters |
|---|---|---|
| **Qualified candidates per opening** | Candidates who reach first phone screen | Healthy pipeline volume |
| **Days to offer** | Days from application to offer acceptance | Speed metric; predicts when hires join |
| **Offer acceptance rate** | % of offers accepted | Competitiveness of comp + candidate experience |
| **Candidate survey results** | % responding "positive experience" post-onsite | Candidate experience signal |
| **Hires to goal** | % of headcount targets met; aim for ≥90% per quarter | Business partnership quality |
| **Source-to-close** | Speed of candidates by source through the pipeline | Source quality signal |
| **Stage conversion rates** | % advancing from each stage to the next | Identifies bottlenecks |
| **Time-in-stage** | Avg days a candidate sits in each stage | Flag anything >7 days |
| **Pipeline demographic representation** | DE&I funnel tracking | Equitable process health |

---

## Harvest API v1/v2 — Current (Legacy)

**Base URL:** `https://harvest.greenhouse.io/v1/`
**Authentication:** HTTP Basic Auth — API key as username, password blank (note the trailing colon)
```bash
curl https://harvest.greenhouse.io/v1/candidates/ -u YOUR_API_KEY:
# Or via header:
Authorization: Basic <base64(YOUR_API_KEY:)>
```
**Required header for all write operations:** `On-Behalf-Of: {greenhouse_user_id}`
**Rate limits:** 50 requests per 10-second window; HTTP 429 on breach; check `X-RateLimit-Remaining` header
**Pagination:** RFC-5988 `Link` header; max 500 records per page (`per_page=500`)
**Key trait:** Child resources (e.g., applications) are **embedded inside** parent responses (e.g., GET /candidates returns applications inline)

```bash
# --- CANDIDATES ---
GET  /v1/candidates?per_page=100&page=1        # List all candidates
GET  /v1/candidates/{id}                        # Get candidate (includes applications inline)
POST /v1/candidates                             # Create candidate
Body: {
  "first_name": "Jane", "last_name": "Doe",
  "email_addresses": [{"value": "jane@example.com", "type": "personal"}],
  "social_media_addresses": [{"value": "linkedin.com/in/janedoe"}],
  "applications": [{"job_id": 12345}],
  "recruiter": {"email": "recruiter@company.com"},
  "tags": ["sourced", "linkedin"]
}
POST /v1/candidates/{id}/attachments            # Add resume/attachment
Body: {"filename": "resume.pdf", "type": "resume",
       "content": "<base64>", "content_type": "application/pdf"}
POST /v1/candidates/{id}/educations             # Add education record
POST /v1/candidates/{id}/employments            # Add employment record
GET  /v1/candidates/{id}/tags                   # Get candidate tags
GET  /v1/candidates/{id}/activity_feed          # Full audit log

# --- APPLICATIONS ---
GET  /v1/applications?job_id=12345&status=active   # List applications
GET  /v1/applications/{id}                          # Get application
POST /v1/applications/{id}/move                     # Advance stage
Body: {"from_stage_id": 123, "to_stage_id": 456}
POST /v1/applications/{id}/hire                     # Mark as hired
PATCH /v1/applications/{id}/reject                  # Reject (note: PATCH not POST)
Body: {"rejection_reason_id": 789, "rejection_email": {"send_email_at": "now"}}
PATCH /v1/applications/{id}/reject                  # Update rejection reason on already-rejected app
POST /v1/applications/{id}/unreject                 # Unreject
POST /v1/applications/{id}/transfer_to_job          # Move to different job
Body: {"job_id": 99999}
PATCH /v1/applications/{id}/convert_prospect        # Convert prospect to candidate
POST /v1/applications/{id}/activity_feed            # Add note
Body: {"user_id": 123, "body": "Note text", "visibility": "private"}
GET  /v1/applications/{id}/scorecards               # List submitted scorecards
GET  /v1/applications/{id}/scheduled_interviews     # Get interviews
GET  /v1/applications/{id}/eeoc                     # EEOC data
GET  /v1/applications/{id}/demographics/answers     # Demographic answers
DELETE /v1/applications/{id}                        # Delete (candidate apps only, not prospects)

# --- OFFERS ---
GET   /v1/applications/{id}/offers                  # List offers
GET   /v1/applications/{id}/offers/current_offer    # Current offer
PATCH /v1/applications/{id}/offers/current_offer    # Update offer

# --- JOBS ---
GET /v1/jobs?status=open                            # List open jobs
GET /v1/jobs/{id}                                   # Get job
GET /v1/jobs/{job_id}/stages                        # List pipeline stages

# --- APPROVALS ---
GET  /v1/approval_flows/{id}                                          # Get approval flow
POST /v1/approval_flows/{id}/request_approvals                        # Trigger approval
PUT  /v1/approver_groups/{approver_group_id}/replace_approvers        # Swap approvers

# --- USERS & CONFIG ---
GET  /v1/users                                      # List users (find On-Behalf-Of IDs)
GET  /v1/custom_fields/{field_type}                 # Get custom fields
POST /v1/custom_fields                              # Create custom field
GET  /v1/close_reasons                              # List rejection reason IDs
```

> **v1 endpoints with known v2 upgrades (use v2 where available):**
> - User management: `PATCH /v2/users/{id}`, `/v2/users/{id}/disable`, `/v2/users/{id}/enable`
> - Job post updates: `PATCH /v2/job_posts/{id}` and `PATCH /v2/job_posts/{id}/status` (split in v2)
> - Scheduled interviews: `POST /v2/scheduled_interviews`, `PATCH /v2/scheduled_interviews/{id}`
> - Destroy openings: `DELETE /v2/jobs/{id}/openings/{opening_id}`

---

## Harvest API v3 — Future / New Integrations

**Use v3 for all new integrations. Migrate existing v1/v2 by August 31, 2026.**

### Authentication — the biggest change from v1/v2

v3 drops Basic Auth entirely. It uses **OAuth 2.0 with JWT Bearer tokens**.

**Two flows depending on integration type:**

| Type | Flow | Use when |
|---|---|---|
| Custom internal integration | Client Credentials | Your team built it, no external users |
| Partner / third-party tool | Authorization Code Grant | External users authorise access |

**Custom integration (Client Credentials) — step by step:**
```
1. In Greenhouse: Configure > Dev Center > API Credential Management
   → Create new API credentials → select "Harvest V3 (OAuth)"
   → Note: client_secret is shown ONLY ONCE. Store it immediately.
   → Assign scopes (only what you need)

2. Generate a token:
POST https://auth.greenhouse.io/oauth/token
Body: {
  "grant_type": "client_credentials",
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET",
  "sub": "GREENHOUSE_USER_ID"   ← identifies the acting user (replaces On-Behalf-Of)
}
Response: { "access_token": "eyJ...", "expires_in": 3600 }

3. Use the token on every request:
Authorization: Bearer eyJ...
```

**Partner integration (Authorization Code Grant):**
```
1. Build auth URL:
https://auth.greenhouse.io/authorize
  ?response_type=code
  &client_id=YOUR_CLIENT_ID
  &redirect_uri=YOUR_CALLBACK_URL
  &scope=harvest:candidates:list harvest:job_posts:list
  &state=RANDOM_CSRF_TOKEN

2. Exchange code for token:
POST https://auth.greenhouse.io/oauth/token
Body: { "grant_type": "authorization_code", "code": "...", "redirect_uri": "..." }

3. Refresh when expired (tokens expire; use refresh_token grant to renew)
```

### Key Structural Change in v3

> In v1/v2, child resources were **embedded inside parent responses**.
> In v3, child resources are **separate** — you must query them independently.

```bash
# v1/v2: GET /candidates/{id} returns candidate WITH all applications embedded
# v3:    GET /v3/candidates/{id} returns candidate WITHOUT applications
#        To get applications: GET /v3/applications?candidate_id={id}
```

This affects any code that parses nested objects from parent responses. Audit all response parsers during migration.

### v3 Endpoints

**Base URL:** `https://harvest.greenhouse.io/v3/`
**Header:** `Authorization: Bearer {access_token}`

```bash
# Common scope examples
harvest:candidates:list        # GET /v3/candidates
harvest:candidates:write       # POST/PATCH /v3/candidates
harvest:job_posts:list         # GET /v3/job_posts
harvest:applications:list      # GET /v3/applications
harvest:applications:write     # Move, hire, reject, etc.
harvest:offers:list
harvest:users:list

# Endpoint paths follow the same naming as v1 but under /v3/
GET  /v3/candidates
GET  /v3/candidates/{id}
GET  /v3/applications?candidate_id={id}    # child resources queried separately
GET  /v3/job_posts
POST /v3/candidates
```

---

## Migration Checklist — v1/v2 → v3

Work through this before the August 31, 2026 deadline:

- [ ] Audit all integrations using v1/v2 — list every script, tool, and third-party connector
- [ ] Create v3 OAuth credentials in Configure > Dev Center for each integration
- [ ] Replace Basic Auth with OAuth 2.0 token generation and Bearer header
- [ ] Update response parsers — remove code that reads child objects embedded in parent responses
- [ ] Update user identity — replace `On-Behalf-Of` headers with `sub` in token request body
- [ ] Update scope permissions — v3 uses named scopes; map current endpoint permissions to scope equivalents
- [ ] Test in staging before cutting over production
- [ ] Update third-party connectors (check vendor v3 support timelines)
- [ ] Rotate old credentials once migration is confirmed working

---

## Ingestion API — Pushing Sourced Prospects In

Use the Ingestion API to push candidates from LinkedIn sourcing, external tools, or scripts into Greenhouse.

**Authentication:** Basic Auth (API key:blank) OR OAuth 2.0
**Required header:** `On-Behalf-Of: {greenhouse_user_id}`

```bash
POST https://harvest.greenhouse.io/v1/candidates
Headers:
  Authorization: Basic <base64(api_key:)>
  Content-Type: application/json
  On-Behalf-Of: <user_id>

Body: {
  "prospect": true,
  "first_name": "Jane",
  "last_name": "Doe",
  "email_addresses": [{"value": "jane@example.com", "type": "personal"}],
  "social_media_addresses": [{"value": "linkedin.com/in/janedoe"}],
  "applications": [{"job_id": 12345}],
  "recruiter": {"email": "recruiter@company.com"},
  "tags": ["sourced-linkedin", "q2-pipeline"]
}
```

---

## Job Board API — Custom Career Site

Use when building a custom career page or application intake outside Greenhouse's hosted board.

- `GET /jobs` — list public job posts
- `POST /applications` — submit an application (requires auth)
- Advantage over Harvest: publicly accessible, heavily cached, no hard rate limits

---

## Greenhouse Webhooks

Set up webhooks in Configure > Dev Center > Web Hooks for event-driven integrations:

| Event | Use case |
|---|---|
| `application_created` | Trigger sourcing CRM update |
| `application_stage_changed` | Notify hiring manager or kick off scheduling |
| `candidate_hired` | Push to HRIS / onboarding system |
| `offer_extended` | Trigger background check or comp benchmarking |
| `scorecard_submitted` | Alert recruiter to review and advance or reject |

---

## Automation Rules to Configure on New Jobs

Suggest these Greenhouse rules for every new job setup:
- Auto-reject applications missing resume after 5 days
- Auto-send application confirmation email upon receipt
- Notify hiring manager when candidate moves to Onsite stage
- Flag applications with missing scorecard 48+ hours after interview
- Auto-advance "Strong Yes" phone screens after recruiter review (optional)

---

## API Security Best Practices

- Treat Harvest API keys as Site Admin level access — never share or embed in client-side code
- Use granular permissions in Configure > Dev Center > API Credential Management
- Create a dedicated **Integration System User (ISU)** for all API operations
- Optionally restrict API key access by IP address in the Dev Center
- Rotate API keys periodically and immediately if compromised
- Use OAuth 2.0 for Ingestion API partner integrations where possible
