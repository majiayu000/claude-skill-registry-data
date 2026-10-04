---
name: post-conference-fup
description: >
  Post-conference follow-up engine. After a conference ends, segments all contacts by engagement
  level (met + hot, replied but didn't meet, no response, badge scans only) and builds tailored
  Apollo sequences for each segment. Tracks which leads converted to meetings, deals, and pipeline.
  Use this skill when the user says "conference follow up", "post conference sequences", "follow up
  from [event]", "conference FUP", "who did I meet at [conference]", "conference leads follow up",
  "segment conference contacts", "post event outreach", "conference pipeline", or any variation of
  wanting to execute follow-up after attending a conference.
---

# Post-Conference Follow-Up Engine

The conference is over. Now the real work starts. This skill takes every contact from the
event, segments them by how warm they are, and builds targeted sequences so nobody falls
through the cracks.

## Core Principle

A conference generates 4 types of contacts. Each needs a completely different follow-up
cadence, tone, and urgency. Sending the same "great meeting you at [event]" email to
someone you had a 30-minute deep dive with AND someone whose badge you scanned walking
by is how you waste a conference investment.

## The Four Segments

| Segment | Definition | Temperature | Follow-up Window | Sequence Type |
|---------|-----------|-------------|-----------------|---------------|
| **HOT — Met & Engaged** | Had a real conversation (5+ min), exchanged context, discussed pain points or product. May have scheduled a follow-up already. | Hot | 24-48 hours | Personalized 1:1 |
| **WARM — Replied / Brief Contact** | Replied to pre-conference outreach, had a quick intro at the event, or exchanged cards but no deep conversation. | Warm | 48-72 hours | Semi-personalized sequence |
| **COOL — No Response / Didn't Meet** | Were on the attendee list, got pre-conference outreach, but never replied and you didn't connect at the event. | Cool | 3-5 days post-event | Conference-themed cold sequence |
| **COLD — Badge Scan / List Only** | Badge scan, sponsor list, or attendee directory only. No prior outreach, no interaction. | Cold | 5-7 days post-event | Value-first cold sequence |

## The Workflow

### Phase 0: Gather All Conference Contacts

Collect contacts from every source:

**From Conference Prep skill outputs (if used):**
- Check for `~/[ConferenceName]_[Year]_ICP_Attendees.csv`
- Check for `~/[ConferenceName]_[Year]_ICP_Companies.csv`

**From the user:**
- Ask: "Do you have any of these from [conference]?"
  1. Badge scan export (CSV/Excel from event app)
  2. Business cards collected (names to look up)
  3. Notes from meetings (who you talked to, what about)
  4. Calendar invites scheduled during/after the event
  5. LinkedIn connection requests sent/received
  6. Pre-conference outreach list (from conference-prep)

**From Fireflies (meetings that already happened):**
```
fireflies_get_transcripts: mine=true, fromDate={conferenceStartDate}, toDate={today}, limit=50
```

Filter for calls with people you met at the conference. Match by:
- Company names from the attendee list
- Meeting titles mentioning the conference name
- Meetings with new contacts (not existing clients)

For each match, get the summary:
```
fireflies_get_summary: transcriptId={id}
```

**From HubSpot (any contacts already logged):**
```
search_crm_objects: objectType="contacts"
  filterGroups: [{ filters: [
    { propertyName: "createdate", operator: "GTE", value: "{conferenceStartDate}" }
  ]}]
  properties: ["firstname", "lastname", "email", "company", "jobtitle",
               "hs_lead_status", "notes_last_updated", "hs_analytics_source"]
  limit: 100
```

**From Apollo (pre-conference sequences):**
```
apollo_emailer_campaigns_search: q_name="{conferenceName}"
```

Check reply status for each contact in the conference sequence.

### Phase 1: Segment Every Contact

Build a master list. For each contact, determine their segment:

**HOT — Met & Engaged** (check these signals):
- [ ] You have a Fireflies transcript with this person
- [ ] User confirms they had a meaningful conversation
- [ ] A follow-up meeting is already scheduled
- [ ] They asked about pricing or next steps at the event
- [ ] User has meeting notes about this person
- [ ] They visited your booth and spent 5+ minutes

**WARM — Replied / Brief Contact** (check these signals):
- [ ] They replied to pre-conference outreach (Apollo reply data)
- [ ] You exchanged cards but didn't have a deep conversation
- [ ] Brief intro at a session, reception, or booth
- [ ] They connected with you on LinkedIn during the event
- [ ] They attended your presentation/panel

**COOL — No Response / Didn't Meet** (check these signals):
- [ ] They were on your pre-conference outreach list
- [ ] They received emails but never replied
- [ ] They were at the conference but you didn't connect
- [ ] They were on the attendee list and are ICP

**COLD — Badge Scan / List Only** (everything else):
- [ ] Badge scan only, no prior interaction
- [ ] Found on exhibitor/sponsor list but no contact made
- [ ] Attendee directory entry, no outreach sent

Present the segmentation to the user for review:

```
CONFERENCE FOLLOW-UP SEGMENTATION: [Conference Name]
====================================================

HOT — Met & Engaged (X contacts)
  1. [Name] — [Title] at [Company]
     Context: [what you discussed, pain points mentioned]
     Next step: [meeting scheduled? proposal needed?]
  2. ...

WARM — Replied / Brief Contact (X contacts)
  1. [Name] — [Title] at [Company]
     Context: [replied to email / quick intro at reception]
  2. ...

COOL — No Response / Didn't Meet (X contacts)
  1. [Name] — [Title] at [Company]
     Pre-conference: [3 emails sent, no reply]
  2. ...

COLD — Badge Scan / List Only (X contacts)
  1. [Name] — [Title] at [Company]
     Source: [badge scan / attendee directory]
  2. ...

Does this segmentation look right? Move anyone between segments before I build sequences.
```

Wait for user confirmation before proceeding.

### Phase 2: Enrich Missing Data

For contacts without full info, run Apollo enrichment:

```
apollo_people_match: name={name}, domain={companyDomain}
apollo_people_bulk_match: (for batches of 10+)
```

Ensure every contact has:
- Verified email
- Current title
- Company name and size
- LinkedIn URL
- Phone (if available)

### Phase 3: Build Sequences by Segment

#### HOT Sequence — "Continue the Conversation"

**Do NOT put these in a mass sequence.** These get personalized 1:1 emails.

For each HOT contact, draft a personal follow-up email:

```
Subject: [specific reference to your conversation]

[Name],

[Reference specific thing you discussed — their pain point, something they said,
a question they asked. Show you were listening.]

[One concrete next step: share a relevant case study, schedule the demo you
discussed, send the pricing they asked about, connect them with a reference.]

[If meeting already scheduled: "Looking forward to [day]. In the meantime,
here's [relevant resource]."]

[Sign-off with direct calendar link]
```

**Rules for HOT emails:**
- Must reference something specific from your conversation (not generic "great meeting you")
- Must include one piece of value (case study, data point, article, intro)
- Must have a clear next step with a specific date/time suggestion
- Send within 24-48 hours while memory is fresh
- CC or BCC into HubSpot for tracking

**Create HubSpot deal for each HOT contact:**
```
manage_crm_objects: objectType="deals", operation="create"
  properties: {
    dealname: "[Company] — [Conference Name]",
    dealstage: "qualifiedtobuy",
    amount: "[estimated based on company size]",
    pipeline: "default",
    closedate: "[30 days from now]"
  }
```

#### WARM Sequence — "We Almost Connected"

Build an Apollo sequence (3-4 touches over 10 days):

**Email 1 (Day 1-2): Conference Connection**
```
Subject: [Conference Name] — quick follow-up

[Name],

We briefly connected at [Conference Name] [specific context: at the reception /
after the [session name] panel / at the exhibit hall].

[One sentence about a key takeaway from the conference relevant to their role]

[Offer: "I put together a quick recap of the sessions most relevant to
[their specialty] — happy to share if useful."]

— JP
```

**Email 2 (Day 4): Value Drop**
```
Subject: Re: [Conference Name] — quick follow-up

[Name],

One thing that kept coming up at [Conference Name]: [relevant industry pain point].

[Share the post-conference insights one-pager if available, or a relevant stat/insight]

[Soft CTA: "Would love to hear how your team is handling [specific pain point]."]
```

**Email 3 (Day 7): Direct Ask**
```
Subject: 15 min this week?

[Name],

Quick question: is [specific pain point discussed at conference] something your
team deals with?

We're helping [similar company type] [specific result with number].

Worth a 15-minute call? [Calendar link]
```

**Email 4 (Day 10): Break-up**
```
Subject: closing the loop

[Name],

I know post-conference inbox is brutal, so I'll keep this short.

If [pain point] is on your radar, I'd love to chat. If not, no worries at all.

[Calendar link] if timing works.
```

#### COOL Sequence — "We Were Both There"

Build an Apollo sequence (4-5 touches over 14 days). These people got pre-conference
outreach but didn't engage. The conference gives you a new angle.

**Email 1 (Day 3-5): Fresh Angle**
```
Subject: [Conference Name] takeaway for [Company]

[Name],

Just got back from [Conference Name]. One session hit close to home for
[their company type]: [specific session topic or insight].

[Key stat or insight from the conference relevant to them]

Thought of [Company] because [specific reason tied to their ICP profile].

Worth comparing notes? [Calendar link]
```

**Email 2 (Day 7): Social Proof**
```
Subject: what [similar company] is doing differently

[Name],

At [Conference Name], I talked to several [their company type] leaders about
[pain point]. The ones making progress had one thing in common: [insight].

[Brief case study or result: "One group cut [metric] from X to Y."]

Is this something [Company] is working on?
```

**Email 3 (Day 10): Value Asset**
```
Subject: [Conference] recap — the 4 stats that matter

[Attach or link the post-conference insights PDF if available]

[Name],

Put together a quick recap of the data points from [Conference Name] that
matter most for [their company type]. Attached.

No pitch, just the numbers. Let me know if any of them surprise you.
```

**Email 4 (Day 14): Last Touch**
```
Subject: one more thing from [Conference]

[Name],

Last follow-up on this. If [pain point] isn't a priority right now, totally
understand.

If it is — we should talk. We're seeing [specific result] with [company type]
like yours.

[Calendar link]
```

#### COLD Sequence — "Industry Value First"

Build an Apollo sequence (3 touches over 14 days). No conference reference since
you didn't interact. Lead with pure value.

**Email 1 (Day 5-7): Industry Insight**
```
Subject: [their company type] + [pain point] data

[Name],

[Specific industry stat relevant to their role and company type]

We've been working with [X number] [company types] on this. The ones seeing
results are [doing specific thing].

Curious if this is on [Company]'s radar?
```

**Email 2 (Day 10): Case Study**
```
Subject: how [similar company type] cut [metric] by [%]

[Name],

Quick case study: [brief result story, 2 sentences max].

Would this kind of result matter for [Company]?

[Calendar link] if worth a 15-min look.
```

**Email 3 (Day 14): Direct + Short**
```
Subject: quick question

[Name],

Does [Company] handle [pain point] manually today?

If yes, worth a quick call. If no, I'll stop bugging you.

— JP
```

### Phase 4: Deploy Sequences

**For HOT contacts:**
1. Draft each personalized email and present to the user for review
2. After approval, send via HubSpot or user's email client
3. Create deals in HubSpot
4. Log the activity

**For WARM / COOL / COLD:**
1. Create Apollo sequences with the email copy:
```
apollo_emailer_campaigns_create (if available) or present the sequence
copy for manual creation in Apollo
```

2. Add contacts to their respective sequences:
```
apollo_emailer_campaigns_add_contact_ids:
  id: {sequence_id}
  contact_ids: [{contact_ids}]
```

3. Assign the correct email account:
```
apollo_email_accounts_index (to find available sending accounts)
```

### Phase 5: Pipeline Dashboard

After all sequences are deployed, present a summary:

```
POST-CONFERENCE PIPELINE: [Conference Name]
============================================

Total contacts processed: XX

HOT (personal follow-up):     XX contacts → XX deals created ($XX pipeline)
WARM (3-touch sequence):      XX contacts → Sequence "[name]" active
COOL (4-touch sequence):      XX contacts → Sequence "[name]" active
COLD (3-touch value sequence): XX contacts → Sequence "[name]" active

Expected timeline:
  Week 1: HOT meetings happening, WARM first touches landing
  Week 2: WARM follow-ups, COOL first touches landing
  Week 3: All sequences completing, pipeline qualifying
  Week 4: Evaluate conversion, pause or extend sequences

Deals to watch:
  1. [Company] — $[amount] — [next step by date]
  2. [Company] — $[amount] — [next step by date]

Conference ROI tracking:
  Investment: $[ticket + travel + hotel + time]
  Pipeline generated: $[total deal value]
  Target close rate: [X]% → Expected revenue: $[amount]
```

### Phase 6: Weekly Check-In

Set a reminder to run a check-in 7 and 14 days post-conference:

**7-day check:**
- Which HOT contacts have meetings scheduled?
- Which WARM contacts replied?
- Any sequence bounces or unsubscribes?
- Deals created and stage progression

**14-day check:**
- Conversion from each segment (replied / meeting booked / deal created)
- Which sequence messaging performed best?
- Contacts to move between segments (COOL → WARM if they replied)
- Contacts to remove (bounced, wrong person, not ICP after research)

## Sequence Performance Benchmarks

Track these against your baselines:

| Metric | HOT | WARM | COOL | COLD |
|--------|-----|------|------|------|
| Open rate target | 80%+ | 50%+ | 30%+ | 20%+ |
| Reply rate target | 50%+ | 20%+ | 8%+ | 3%+ |
| Meeting rate target | 40%+ | 10%+ | 3%+ | 1%+ |

If WARM is outperforming COOL by 3x+ on reply rate, your segmentation is working.
If they're similar, you're not personalizing enough for WARM.

## Important Rules

- **HOT contacts NEVER go in a mass sequence.** Personal emails only. These are your highest-value leads.
- **Segment before you send.** Spending 30 minutes segmenting saves you from burning warm leads with cold messaging.
- **Conference reference has a shelf life.** After 7 days, "great meeting you at [event]" sounds stale. COOL and COLD sequences should lead with value, not the event.
- **Attach the insights one-pager.** If you ran `/post-conference-insights`, use that PDF as a value drop in WARM and COOL sequences.
- **Track everything in HubSpot.** Every deal, every note, every activity. Conference ROI is impossible to measure without clean data.
- **Don't spray badge scans.** COLD contacts get a value-first approach with no conference reference. Treat them like any other cold prospect.
- **Move contacts between segments.** A COOL contact who replies to email 1 becomes WARM. A WARM contact who books a meeting becomes HOT. Update accordingly.

## File Dependencies

- **Conference Prep outputs** (optional): ICP Attendees CSV, ICP Companies CSV
- **Post-Conference Insights PDF** (optional): Use as value drop in sequences
- **Apollo MCP**: For sequence creation and contact management
- **HubSpot MCP**: For deal creation and pipeline tracking
- **Fireflies MCP**: For finding meetings that already happened with conference contacts

## Output

- Segmented contact list with context notes
- Personalized HOT emails ready to send
- WARM/COOL/COLD Apollo sequences with email copy
- HubSpot deals for HOT contacts
- Pipeline dashboard with ROI tracking
- 7-day and 14-day check-in prompts
