---
name: managing-ff-pipeline
version: "1.1.1"
description: >
  Manages FlashFusion's prospecting, outreach, and deal pipeline across
  HubSpot (CRM), Apollo.io (prospect research and sequencing), and Clay
  (data enrichment). Covers the full pipeline from identifying prospects
  through closing and handoff to contracts. Activates when the user mentions:
  pipeline, prospect, outreach, follow up, HubSpot, Apollo, Clay, deal stage,
  CRM, sales, FlashFusion clients, lead, contact, sequence, enrichment,
  deal hygiene, pipeline review, who should I reach out to, or any mention
  of finding or progressing FlashFusion consulting opportunities.
---

<!-- ─────────────────────────────────────────────────────────────────────── -->
## DEPENDENCY_DECLARATION

| Tool | MCP Status | Required / Optional | Lane |
|------|------------|---------------------|------|
| HubSpot | ✅ Connected | Required — deal tracking and pipeline state | Personal / Freelance |
| Apollo.io | ✅ Connected | Required — prospecting and sequences | Personal / Freelance |
| Clay | ✅ Connected | Required — enrichment step before outreach | Personal / Freelance |

### Rate Limit Warnings

| Tool | Limit | Risk |
|------|-------|------|
| **Apollo.io** | 10,000 requests/month (standard plan); credits consumed per search and per contact view | Bulk prospecting runs and list exports burn credits silently. Check remaining credit balance before starting any campaign or bulk search. |
| **Clay** | Credit-based per enrichment lookup; no fixed monthly cap but credits deplete per row processed | Bulk enrichment against large company lists can drain credits within a single run with no mid-run warning. Run a small batch (≤10 rows) first; audit balance before any run over 50 rows. |
| **HubSpot** | 100 requests per 10 seconds per private app; additional burst limits on list and bulk import operations | Pipeline sync loops and batch activity logging can hit the 10-sec window. Add retry-with-backoff if any automation layer is built on top of HubSpot API calls. |

<!-- ─────────────────────────────────────────────────────────────────────── -->

# FlashFusion Pipeline Manager

Moves FlashFusion prospects from identified to closed using three connected
tools. Each tool has a specific job — they are not interchangeable.

---

## Evals

**Should trigger:**
1. "I want to find AI-forward IT companies in the Chicago area to reach out to"
2. "Review my HubSpot pipeline — anything stale or missing follow-up?"
3. "I need to enrich this contact before reaching out"

**Should NOT trigger:**
1. "Help me write the SOW for this client" — use managing-ff-contracts
2. "How do I price my services?" — pricing strategy, not pipeline

---

## Tool Roles

| Tool | Job | Do NOT use for |
|---|---|---|
| Apollo.io | Find prospects, research contacts, send sequences | CRM record-keeping |
| Clay | Enrich contact and company data from multiple sources | Outreach |
| HubSpot | Track deals, log activity, manage the pipeline | Prospecting |

**The flow:** Apollo finds → Clay enriches → HubSpot tracks → Apollo sequences.

---

## FlashFusion Ideal Client Profile (ICP)

Target companies and decision-makers most likely to become FlashFusion clients.
Full ICP detail in `references/pipeline-and-icp.md`.

**Quick filter:**
- Company: IT services, MSP, tech-adjacent business, 10–200 employees
- Decision maker: IT lead, operations manager, founder, VP of Operations
- Signal: recently posted about AI adoption, hired for AI roles, using tools
  in FlashFusion's stack (n8n, Make, Zapier, Supabase, Base44)
- Geography: Chicago metro preferred for high-touch; anywhere for
  digital-first consulting

---

## Pipeline Stages

```
1. PROSPECT     Identified, not yet contacted — in Apollo, not yet in HubSpot
2. CONTACTED    Outreach sent — Apollo sequence active
3. RESPONDED    Two-way conversation started — create HubSpot deal
4. QUALIFIED    Need confirmed, scope discussed — deal moves to Qualified
5. PROPOSAL     SOW or NDA sent (managing-ff-contracts) — deal moves to Proposal
6. CLOSED WON   Contract signed, deposit received
7. CLOSED LOST  Reason logged — never leave blank
```

---

## Section 1: Prospecting (Apollo.io)

### Finding prospects

1. Apollo.io → Search → filter by:
   - Industry: IT Services / Managed Services / Business Services
   - Employee count: 10–200
   - Location: Illinois + national if digital-first engagement
   - Technologies used: search for companies using target tools
   - Job titles for decision-makers: IT Director, VP Operations, Founder, CTO

2. Verify intent signals before adding to outreach:
   - Recent LinkedIn activity about AI tools or automation?
   - Job postings for AI/automation roles?
   - Company blog or news about digital transformation?

3. Flag high-intent prospects in Apollo for Clay enrichment before outreach.

### Research before reaching out

Do not send a cold sequence without knowing:
- Their current tool stack (especially where FlashFusion could fit)
- One specific problem FlashFusion could solve for them
- The right person to contact (decision-maker, not gatekeeper)

If this research takes more than 10 minutes per prospect: use Clay enrichment.
If it's a high-value target: use Clay regardless of time.

---

## Section 2: Enrichment (Clay)

Use Clay to pull enriched data on a prospect or company before outreach.

**When to enrich:**
- Any target with deal potential over $2,000
- Any company you're spending more than 10 minutes researching manually
- Any contact where LinkedIn/Apollo data feels thin

**What Clay enrichment adds:**
- LinkedIn activity and recent posts (signals current priorities)
- Company news and funding signals
- Tech stack from multiple sources (not just one database)
- Contact email verification

**Output:** a one-paragraph prospect brief. Paste into HubSpot contact notes
before first touch.

---

## Section 3: Outreach (Apollo.io Sequences)

### Sequence design

Three-touch minimum for cold outreach. More touches for higher-value targets.

```
Touch 1 (Day 1): Specific, relevant opener — reference their situation
Touch 2 (Day 5): Value add — one useful observation or resource
Touch 3 (Day 10): Light close — simple yes/no ask
Touch 4+ (Day 20+): Breakup email — genuine, not performative
```

**Opener format:** Reference something specific. Not "I love what your
company is doing." Specific: "I saw you're hiring for an AI Ops role —
that usually means someone is trying to build the tooling layer around
a stack that's growing faster than the team can manage. That's exactly
what FlashFusion works on."

**Do not:** send generic AI-generated cold emails. Kyle's voice is the asset.
Every sequence should sound like a person who read their LinkedIn, not a
person who found their email address.

### When a prospect responds

Immediately:
1. Pause the Apollo sequence (so they don't get Touch 2 while you're talking)
2. Create a HubSpot deal at stage: CONTACTED → RESPONDED
3. Log the response in HubSpot contact notes

---

## Section 4: Pipeline Management (HubSpot)

### Weekly pipeline hygiene

Every deal should answer three questions:
- What is the next action?
- Who is responsible for it?
- What is the due date?

If a deal can't answer all three, it's stale. Either advance it or close it lost.

**Stale deal threshold:**
- No activity in 14 days at RESPONDED/QUALIFIED stage → follow up or close lost
- No activity in 7 days at PROPOSAL stage → follow up specifically on the SOW
- No activity in 30 days at CONTACTED stage → sequence may have exhausted; move to lost

### Stage transition triggers

| Moving from | To | Trigger |
|---|---|---|
| PROSPECT → CONTACTED | | Apollo sequence sent |
| CONTACTED → RESPONDED | | Any reply (even negative) |
| RESPONDED → QUALIFIED | | Call completed, need confirmed, budget range discussed |
| QUALIFIED → PROPOSAL | | SOW or NDA sent via DocuSeal |
| PROPOSAL → CLOSED WON | | Contract signed, deposit received |
| Any → CLOSED LOST | | Explicit no, no response after 4 touches, or wrong fit confirmed |

### Closed Lost logging

Never leave Closed Lost reason blank. Options:
- No budget right now
- Wrong timing — revisit in [quarter]
- Chose a different solution
- Not the right fit (ICP miss)
- No response after full sequence
- Other (note specifically)

Closed Lost with a reason is a future opportunity. Closed Lost without a reason is a missed asset.

---

## Self-Verification

Weekly pipeline review:
- [ ] All deals have a next action, owner, and due date
- [ ] Stale deals addressed (follow up or close lost)
- [ ] Active Apollo sequences checked for deliverability issues
- [ ] New prospects from this week enriched in Clay before sequence

---

<!-- ─────────────────────────────────────────────────────────────────────── -->
## FAIL_IF CONDITIONS

**HubSpot unavailable:**
- FAIL_IF HubSpot MCP returns auth error, 429, or connection failure: halt all pipeline hygiene reviews and stage transition operations; do not write deal updates, log activity, or create new contacts until connection is confirmed restored.
- DEGRADATION PATH: track pending deal updates in a local scratch note or Notion table tagged "PENDING HUBSPOT SYNC — [date]". No deal state is authoritative until confirmed written to HubSpot. Resume sync in order of pipeline stage (PROPOSAL first, then QUALIFIED, then RESPONDED).

**Apollo.io unavailable:**
- FAIL_IF Apollo.io MCP returns connection error, auth failure, or credit-exhausted response: halt all prospecting searches and sequence send operations; do not initiate contact with new prospects; log any sequences queued but unsent for manual restart; check credit balance before retrying after reconnect.
- DEGRADATION PATH: prospecting can continue at reduced throughput via manual LinkedIn search; Clay enrichment remains available for contacts already identified through other means. Tag any prospect identified during the outage as "Apollo-pending" to queue for sequence enrollment when restored.

**Clay unavailable:**
- FAIL_IF Clay MCP returns error or credit-exhausted response: skip the enrichment step; flag all affected prospects in Apollo with label "needs-enrichment-clay-down"; do not send outreach to any target with deal potential over $2,000 without enrichment — defer those to the Clay-restored queue.
- DEGRADATION PATH: for time-sensitive outreach on lower-value targets (under $2,000 deal potential), proceed with Apollo-only data; note "unenriched — Clay outage [date]" in HubSpot contact record. Enrichment backfill is a required task when Clay is restored before next pipeline review.

<!-- ─────────────────────────────────────────────────────────────────────── -->

## CLAIMS
- Pausing Apollo sequences immediately on first response prevents
  the awkward "second touch after they already replied" — this one
  mistake undermines more outreach than any other
- Closed Lost reason logging turns a dead deal into a dated reminder
  — "no budget, revisit Q4" is a pipeline asset

## COUNTEREXAMPLE
- The 3-touch sequence minimum is for cold outreach; warm referrals
  or inbound responses need zero sequence — respond directly, never
  add a referred prospect to an automated sequence

## CONTRADICTIONS
- "Enrich before reaching out" conflicts with moving fast on a
  time-sensitive opportunity — if someone is actively evaluating
  options, outreach speed beats enrichment depth; skip Clay and go
