---
name: icp-customer-interviews
description: Your customer-interview target finder. Connect Salesforce (CSM-managed customer book) and a canonical ICP doc — turns "who should I interview to validate the ICP, test the positioning, learn how they found us?" into a ranked slate of ~20 customers, each with a verdict, three-bullet why, and one named buying-committee recipient ready for a CSM-mediated intro. Use when a founder, GTM leader, or PMM is starting an ICP-validation round, testing new positioning, building a win-story program, or scouting reference customers. Trigger on "find customers to interview", "ICP validation interviews", "test our positioning with customers", "customer interview targets", "who in my book matches the ICP", "build a customer research slate", "find reference customers", "who should we talk to about how they found us", "validate the ICP with real customers", or any request to convert a CSM or AE book into a prioritized interview slate. Also fires when a new ICP doc ships and needs socializing with the customers who define it.
---

# ICP Customer Interviews — your customer-interview target finder

**Required connectors:** Salesforce (the source of truth for who's on the CSM book and who's paying) + a canonical ICP doc (URL or local path to your "Master ICP Profile" or equivalent).

**Optional connectors:** Amplitude (Product Engagement Score for "are they actually using it?") · Mixmax (meeting history for "have we already talked recently?") · GitHub Pages (to publish the deliverable to your reports site) · Octave (to draft the outreach after the slate is built).

## What this skill answers

In plain English, the ICP Customer Interviews skill answers questions like:

- "Who in my CSM book matches the new ICP doc?" → A ranked list of paying customers scored against your canonical ICP, top to bottom
- "Find me 20 customers to interview about how they found us" → A 20-account slate with named buying-committee recipients, ready for CSM-introduced outreach
- "We just shipped a new positioning doc — who should we test it with?" → The accounts that define the ICP, prioritized by their ability to speak to evaluation, outcomes, and competitive alternatives
- "Who can I ask to test the v8 positioning?" → Customers segmented by tenure and product engagement so you know which voices are fresh, which are seasoned
- "I need 6 priority interviews booked this month, plus 14 backups" → A two-tier output: Priority (book first) and If Capacity (workable backups)
- "Build me a reference-customer pipeline" → Pre-filtered for power users on the right stack, with a named recipient already in the buying committee

## What it owns internally

The ICP Customer Interviews skill is the product layer over these atomic skills:

- **`icp-analyst`** — for the multi-source ICP scoring (Aero + Octave + Common Room + signals)
- **`salesforce-analyst`** — for the CSM-book pull and contact graph
- **`amplitude-analyst`** — for Product Engagement Score per account (optional but recommended)
- **`customer-strategy-brief`** — for the per-account brief methodology (Verdict, three-bullet Why, named Next Move)
- **`conversation-analyst`** — for last-touch and meeting-history context (prevents reaching out to someone you just talked to)
- **`comms-analyst`** — to ship the deliverable (draft Octave intros, post to Slack, publish to GitHub Pages)

## The quality gates this skill guarantees

**No score without a recipient.** Every account on the final slate has a named buying-committee contact (VP Sales, CRO, RevOps, Founder, or comparable) pulled from the live Salesforce contact graph. If the contact graph is empty for a high-scoring account, surface that as a CRM hygiene flag rather than silently dropping the account.

**ICP doc grounding — not generic.** The skill MUST read the canonical ICP doc the user points it at and extract the actual size band, geo, tech stack, and industry weights from that doc. No baked-in scoring rubrics. If the ICP doc cannot be resolved, stop and ask for it.

**Two-tier output — priority and backup.** The slate ships as 5–7 Priority interviews (the definitional ICP customers — book these first) plus 13–15 workable backups. This matches how booking actually goes: you do not need 25 perfect calls, you need 10–20 booked, and the priority tier is the high-conviction set.

**Explicit watchlist.** The skill explicitly names accounts it considered but dropped — Consumer & Retail when the ICP doc flags it as anti-pattern, off-stack CRMs, marquee logos above the size ceiling, sub-band employee counts. This is the audit trail for "why isn't Acme on the list."

**Brief methodology — not just a table.** Each Priority account renders a full `customer-strategy-brief`-style card: Verdict, three-bullet Why grounded in actual data (size, ARR, fit, engagement, tenure), Next Move with a named recipient, and Caveats when relevant. Backups go in a compact table.

## Composite interview-fit score breakdown

```
Interview Fit Score 0-100 (the headline number)
  = 35% × Size match              (per the ICP doc's sweet-spot band)
  + 15% × Geography match         (per the ICP doc's primary region)
  + 15% × Email provider match    (per the ICP doc's primary stack — usually Gmail)
  + 10% × CRM match               (per the ICP doc's primary CRM — usually Salesforce)
  + 15% × Industry match          (per the ICP doc's primary vertical set)
  + 10% × Aero / scoring-vendor fit  (High / Med / Low)

Modifiers (applied after the score):
  + Tenure bucket signal — 2–5yr ⭐ (freshest buyer memory)
  + Product Engagement Score (PES) — High = "they can speak to outcomes"
  - Below the size floor or above the ceiling — flagged but not dropped
  - Consumer & Retail (if ICP doc flags as anti-pattern) — drop from slate, surface on watchlist
  - Off-stack CRM (if not in the ICP doc's primary CRM set) — flagged
  - No senior buying-committee contact in SFDC — flagged as CRM hygiene gap
```

The threshold for "ICP-match" is **78+ on the composite** by default, but the skill reads any explicit threshold from the ICP doc if one is named.

## Verdict taxonomy

Adapted from `customer-strategy-brief` for the interview-target use case:

- 🟢 **Interview — Priority** — Definitional ICP, named recipient confirmed, can speak to all five interview questions. Book first.
- 🟢 **Interview** — Strong ICP match, named recipient confirmed. Workable backup.
- 🟡 **Interview If Capacity** — Workable with a caveat (mid-PES so adoption-gap story; size edge case; Aero false-negative). Book only if priority calls don't fill.
- ⚪ **Skip This Round** — Scored well but anti-pattern, off-stack, or out-of-band. Surface on watchlist with reason.

## The five interview questions the slate must support

Every account on the slate MUST be able to answer:

1. **How did you find Mixmax?** (Channel-of-acquisition validation — Inbound / Outbound / Product / Word-of-mouth)
2. **What did you almost pick instead?** (Competitive alternative set — what we're really winning against)
3. **[Test the current positioning]** — The skill ingests the current positioning sentence from the ICP doc and asks the customer to react to it
4. **What outcome are you getting that you couldn't get elsewhere?** (The "why we stay" story — the differentiated value)
5. **Would you recommend us? To whom?** (Reference-customer eligibility + ICP self-replication signal)

If an account is too new (< 6 mo tenure) to answer #2 or #4 reliably, the skill demotes it to Backup or Skip.

## Procedure

### Step 1 — Resolve the ICP doc

Take a URL, local path, or "use the latest" instruction. Read the doc. Extract:
- Size sweet-spot band (e.g., 50–200) and outer ceiling (e.g., 500)
- Primary geography (e.g., NA — US + Canada)
- Primary email provider (e.g., Gmail; weight Outlook lower)
- Primary CRM (e.g., Salesforce + HubSpot)
- Industry vertical set (the "preferred 8") and any explicit anti-pattern verticals (e.g., Consumer & Retail)
- Aero / scoring-vendor tier requirements (if specified)
- The current positioning sentence — verbatim, for use in interview question #3

If the doc cannot be resolved or is missing one of these dimensions, stop and ask.

### Step 2 — Pull the CSM-managed customer book

Salesforce query: every Account where `CSM__c != null` AND `Type = 'Customer'` AND `DWH_DS_Customer_ARR__c > 0`. Pull the universe fields the scoring needs: Name, Website, CSM, Owner (AE), Industry, CR_Industry__c, NumberOfEmployees, CR_Number_of_Employees__c, BillingCountry, ARR, Email_Provider__c, CRM__c, Aero_Account_Fit_Score_Tier__c, Aero_Product_Engagement_Score__c, CreatedDate, RP_Renewal_Period_End__c, Past_Renewals__c.

### Step 3 — Score every account against the ICP

Apply the composite formula above using the bands extracted in Step 1. Compute tenure bucket from CreatedDate. Flag anti-pattern industry hits (drop from slate, hold on watchlist).

### Step 4 — Pull buying-committee contacts for the top 25

For each of the top 25 (post-anti-pattern-drop), query Salesforce Contacts with senior titles (VP, Chief, Head, Director, RevOps, Sales Ops, Founder, CEO, President), ordered by LastActivityDate. Pick the seniormost still-active contact per account.

Surface "no senior contact" as a CRM hygiene flag — do not drop the account.

### Step 5 — Apply the customer-strategy-brief methodology to the Priority tier

The top 5–7 (or whatever ranks 100–80) render as full `customer-strategy-brief`-style cards:
- **Verdict** with color
- **Three bullets of Why** — grounded in size + ARR + fit + engagement + tenure
- **Next Move** — CSM-mediated intro to the named recipient, framed for interview question #1/#2/#3
- **Caveats** — tenure mental-model risk, CRM hygiene, industry mis-tag

Backups (ranks ~80–60) render as a compact table.

### Step 6 — Build the watchlist

Explicitly name and reason for every account that scored 78+ but didn't make the slate: anti-pattern industry, off-stack CRM, sub-band employee count, marquee logo above ceiling.

### Step 7 — Render the HTML artifact

Single-file HTML, dual-theme (per the org's brand guidelines), with this structure:
1. Header + theme toggle
2. Metric strip (book size, ICP-match count, slate size, priority count, median ARR, median employees)
3. Methodology — three cards: ICP gates / brief methodology / the five interview questions
4. Priority shortlist — full brief cards
5. Full 20 slate — compact table with named recipients
6. Watchlist — skipped accounts with reasons
7. How to book — operational steps (forward to the CSMs, sequence priority first, Octave drafts, cadence)
8. Data-quality notes — anything that surfaced (CRM blanks, Aero false-negatives, dated contact graphs)

### Step 8 — Ship it

If `comms-analyst` is connected and the user requested publish:
- Save HTML to the workspace folder
- Publish to GitHub Pages (operational/ root by default, or wherever the org's `reports.json` puts strategy docs)
- Register in `reports.json` under category "Strategy", roles `["sales", "marketing", "leadership"]`
- Optionally draft Octave intros for the priority tier and DM the CSMs

## Output format example

For "find me 20 customers from my CSM book to interview about how they found us":

```
🎯 Customer Interview Targets — ICP Validation Round
   49 CSM-managed customers · 24 ICP-match · 20 recommended slate · 6 priority

PRIORITY SHORTLIST (book these first)

🟢 1 · Right Side Up — ICP 100 · Priority
   200 emp · US · Professional Services · Gmail+Salesforce · $14.6K ARR · 5yr+
   WHY
   • Sweet-spot 200 emp, Pro Services (#1 converting industry in May audit),
     full Gmail+Salesforce — exact firmographic shape we use to define the ICP
   • 5+ year customer with 5 past renewals — long enough memory to compare
     current positioning to what they originally bought
   • Aero PES 99 + High fit — product is being used; they can speak to
     actual outcomes, not just intent
   NEXT MOVE
   Diana (CSM) intros Tyler Elliston, Founder · tyler@rightsideup.co
   Frame: Heath-to-founder ICP conversation — "we're rewriting how we
   describe who we sell to, and you're the case study." Buying committee.
   CAVEATS
   5yr+ tenure means buying mental model may be dated — lean into
   "if you were buying us today, what would the pitch need to be?"

🟢 2 · Whip Around — ICP 98 · Priority
   [... same brief shape ...]

[... priority tier continues for ranks 1-6 ...]

THE FULL 20 — backup slate (compact table)
[Rank | Account | ICP | Emp | Industry | ARR | Aero | PES | CSM | Verdict |
 Recipient | One-line angle]

WATCHLIST — scored well but skipping this round
• Three Day Rule (ICP 82) — Consumer matchmaking. Anti-pattern per audit.
• AuditBoard (ICP 78) — 928 emp. Above ceiling. Different conversation.
• Zensurance (ICP 69) — Off-stack on SugarCRM.
• Marquee logos (Airbnb, Datadog, DoorDash) — 10K+ emp.

HOW TO BOOK
1. Forward this brief to the two CSMs who own the slate.
2. Sequence the 6 priority first — book 2/week.
3. Draft Octave intros using the named recipients.
4. Target 30-min interviews; the 5 questions are the spine of every call.

DATA QUALITY FLAGS
• 20/49 customers have blank CRM field in Salesforce.
• 4 accounts show Aero false-negative pattern (Low fit + High PES).
• Leap Tools has $49K ARR + 7 renewals but no current senior contact in SFDC.
```

## When NOT to use this skill

- **Prospect/cold targeting** — use `icp-analyst` + `enrichment-analyst` on a TAM list, not your CSM book
- **Win/loss interview list** — use a Closed Won / Closed Lost report; this skill is for active paying customers
- **NPS or generic VoC surveys** — this is a curated qualitative-interview slate, not a survey distribution list
- **Per-account QBR prep** — use `customer-strategy-brief` or `customer-strategy-deep-dive`
- **Pipeline / forecast review** — use `salesforce-analyst` or `deal-intelligence`

## Cross-links

- **Upstream:** the canonical ICP doc (the org's "Master ICP Profile" or equivalent)
- **Sibling:** `icp-analyst` (single-account ICP qualifier), `customer-strategy-brief` (single-account 60-second brief), `conversation-analyst` (relationship state)
- **Downstream:** `comms-analyst` (publish + draft Octave outreach), `customer-battle-plan` (build the multi-touch save/expansion play if an interview surfaces risk)

## Lock-in notes

- Reads the ICP doc as source of truth — does not bake in any specific size band, vertical, or stack
- Two-tier output (Priority + Backup) is non-negotiable — matches how booking actually plays out
- Every Priority account names a recipient; no recipient = CRM hygiene flag, not silent drop
- Watchlist is required, not optional — it's the audit trail
- Customer-strategy-brief methodology is the per-account standard — Verdict, three bullets, named Next Move
