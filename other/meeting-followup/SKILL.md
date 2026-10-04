---
name: meeting-followup
description: >
  Automates post-meeting follow-up after any sales or customer call. Pulls the meeting
  transcript from Fireflies, cross-references HubSpot deal/contact data and Apollo contact
  enrichment, runs a fact-check layer, and produces three deliverables: a plain-text
  follow-up email draft, HubSpot deal notes with stage/amount recommendations, and an
  internal debrief with buying signals, objections, competitor mentions, and next moves.
  Use this skill when the user says "follow up on my meeting with [company]",
  "meeting follow-up", "post-meeting", "write follow-up for [company]",
  "summarize my call with...", "meeting debrief", "what happened on my call with...",
  "draft follow-up email for [company]", "post-call notes", "follow up from today's call",
  "write a recap for [company]", or any variation of wanting follow-up materials after
  a sales or customer conversation.
---

# Meeting Follow-Up

Generate a complete post-meeting follow-up package: email draft, HubSpot notes, and
internal debrief. All grounded in what was actually said on the call, cross-checked
against CRM and enrichment data.

## Core Principle

Every word in the follow-up must trace back to something specific from the call or
the deal history. No filler. No generic "great talking to you" language that could apply
to any meeting. The prospect should read the email and think "this person was actually
paying attention." The internal debrief should be honest, not optimistic.

## The Workflow

Execute these phases in order. Some sub-steps within phases run in parallel.

### Phase 0: Identify the Meeting

Determine which meeting the user wants to follow up on:

1. If the user names a company or person, use that as the search term
2. If the user says "my last meeting" or "today's call", search by recency
3. If ambiguous, search Fireflies for recent calls and present options

Extract from the user's request:
- **Company name** (required — ask if not provided)
- **Person name** (optional, helps narrow search)
- **Date** (optional, defaults to most recent match)

### Phase 1: Data Collection (parallel)

Run all four data pulls simultaneously:

**1A — Fireflies Transcript:**

```
fireflies_search: keyword:"{company_name}" scope:title limit:10
```

If no results by company name, try:
```
fireflies_search: keyword:"{person_name}" scope:title limit:10
```

From the matching meeting(s):
- `fireflies_get_summary` for the meeting — get overview, action items, topics discussed
- `fireflies_get_transcript` for the full transcript — needed for direct quotes and nuance
- Note: meeting ID, title, date, duration, attendees

Also search for any PREVIOUS meetings with this company:
```
fireflies_search: keyword:"{company_name}" scope:title limit:20
```
Pull summaries of prior meetings to track action item progress and conversation continuity.

**1B — HubSpot Deal & Contact Data:**

Search HubSpot for the company and associated contacts:
```
search_crm_objects: objectType:"companies" query:"{company_name}"
search_crm_objects: objectType:"deals" query:"{company_name}"
search_crm_objects: objectType:"contacts" query:"{company_name}"
```

Extract:
- Current deal stage, amount, close date, pipeline
- Contact names, titles, emails, phone numbers
- Deal notes and activity history
- Previous email threads (check contact activity for email subjects/dates)
- Any tasks or upcoming activities scheduled
- Deal owner

**1C — Apollo Contact Enrichment:**

For each attendee from the Fireflies transcript who is NOT from Solum Health:
```
apollo_people_match: email:"{attendee_email}"
```

Or if only name + company:
```
apollo_mixed_people_api_search: person_titles:[] person_locations:[] q_organization_name:"{company}" q_keywords:"{person_name}"
```

Extract:
- Full name, current title, seniority level
- LinkedIn URL
- Company size, industry, funding stage
- Other relevant contacts at the company (decision makers, champions)

**1D — Prior Meeting Cross-Reference:**

If prior meetings exist with this company:
- List action items from prior calls
- Check which ones were completed vs. still open
- Note any pricing, timelines, or commitments previously discussed
- Track how the relationship has progressed over time

### Phase 2: Fact-Check Layer

Before generating any output, run these verification checks:

**Attendee Verification:**
- Compare attendee names from Fireflies against HubSpot contacts and Apollo data
- If a name or title differs, use the most authoritative source (Apollo for titles, HubSpot for contact ownership)
- Flag any attendees on the call who are NOT in HubSpot (suggest adding them)

**Numbers Consistency:**
- Extract any numbers discussed on the call: pricing, volumes, timelines, patient counts, revenue figures
- Compare against numbers from prior meetings and HubSpot deal amount
- Flag inconsistencies (e.g., "They said 500 patients on the last call but 800 on this one")

**Competitor Detection:**
- Scan transcript for mentions of competitors, alternative solutions, or "we're also looking at..."
- Common competitors to watch for: Availity, Waystar, Infinx, Infinitus, Olive AI, Rhyme, Myndshft, manual processes, "doing it in-house", "our current vendor"
- Flag the context of any competitive mention (comparing features, pricing, timeline)

**Commitment Tracking:**
- Identify any commitments made by either side:
  - "We'll send you..." / "I'll follow up with..."
  - "Let's schedule..." / "We can start..."
  - "I'll check with my team about..."
- Cross-reference with prior meeting commitments to see what was delivered
- Flag overdue commitments

**Discrepancy Report:**
- Compile all inconsistencies, missing data, and flags into a fact-check section
- Rate confidence: HIGH (data matches everywhere), MEDIUM (minor gaps), LOW (conflicting information)

### Phase 3: Generate Deliverables

Produce all three outputs. Each must be grounded in specific call content.

---

#### Deliverable A: Follow-Up Email Draft

**Format:** Plain text. No markdown. No bold. No bullets. No asterisks. Ready to paste
into Gmail with Cmd+Shift+V and send without any formatting cleanup.

**Structure:**
1. Opening line referencing something specific from the call (NOT "great meeting today")
2. 1-2 sentences recapping the key topic or problem discussed
3. Specific next steps that were agreed upon, with owners and dates
4. Any documents, materials, or information promised — mention them explicitly
5. Closing that sets up the next interaction naturally
6. Sign-off as JP

**Tone Calibration:**
- If previous email threads exist in HubSpot, match that tone and formality level
- First meeting = slightly more formal but still warm
- Ongoing relationship = casual, direct, skip the pleasantries
- If the call was technical/operational, keep the email operational
- If the call was executive/strategic, keep the email high-level
- Use the prospect's first name naturally
- Keep it under 150 words. Shorter is better.

**What NOT to include:**
- "It was great connecting" or any variation
- Bullet points or numbered lists (this is an email, not a document)
- Links to marketing materials unless specifically discussed
- Product pitches or features not discussed on the call
- "Please don't hesitate to reach out" or any similar filler

**Example calibration (DO NOT copy verbatim — adapt to each call):**

```
Hi Sarah,

Really interesting point you made about the eligibility check volume spiking
during Q1. That tracks with what we're seeing across similar-sized practices.

As discussed, I'm putting together the ROI breakdown based on your 2,400
monthly checks. You mentioned wanting to see the error-rate comparison
against your current Availity workflow, so I'll include that side by side.

I'll have that over to you by Thursday. In the meantime, I've looped in
our implementation lead so we can move quickly if the numbers make sense
on your end.

Talk soon,
JP
```

---

#### Deliverable B: HubSpot Deal Notes

**Format:** Structured text ready to paste into HubSpot deal notes or present as
a recommended CRM update.

**Contents:**

1. **Meeting Summary** (3-5 sentences max)
   - Who was on the call, their roles
   - Primary topic discussed
   - Key decisions or outcomes

2. **Deal Stage Recommendation**
   - Current stage in HubSpot
   - Recommended stage after this meeting (with reasoning)
   - Stage progression options: Appointment Scheduled → Qualified to Buy → Presentation Scheduled → Decision Maker Bought-In → Contract Sent → Closed Won / Closed Lost
   - Only recommend a stage change if the call clearly warrants it

3. **Amount Update** (if pricing was discussed)
   - Current deal amount in HubSpot
   - Recommended amount based on what was discussed
   - Calculation basis (e.g., "500 patients x $2/check = $1,000/mo = $12,000 annual")

4. **Action Items**
   - Each item with: description, owner (Solum or prospect), due date
   - Mark which are blocking the deal from progressing

5. **Next Meeting**
   - Date/time if scheduled
   - Agenda items for next call
   - Who should attend

6. **Contacts to Add/Update**
   - Any new attendees not in HubSpot
   - Title or role updates needed

---

#### Deliverable C: Internal Debrief

**Format:** Structured analysis for internal use. Be honest and direct.

**Contents:**

1. **Call Rating: X/5**
   - 5 = Deal advancing, clear next steps, buying signals strong
   - 4 = Productive call, positive signals, minor gaps
   - 3 = Neutral, no clear movement forward or backward
   - 2 = Concerns raised, objections not handled, momentum stalling
   - 1 = Deal at risk, strong objections, competitive threat, going cold

2. **What Went Well**
   - Specific moments from the call that advanced the deal
   - Direct quotes that show interest, buy-in, or urgency
   - Relationship dynamics that are working

3. **What Concerns Were Raised**
   - Objections stated or implied
   - Questions that suggest hesitation
   - Topics avoided or deflected by the prospect

4. **Buying Signals**
   - Questions about implementation, timeline, onboarding
   - "How would we..." or "When can we start..." language
   - Asking about references, case studies, or similar clients
   - Discussing budget or getting internal approval

5. **Objections & Risks**
   - Price concerns
   - Timing ("not right now", "maybe next quarter")
   - Technical fit questions
   - Internal politics or approval process complexity
   - Status quo bias ("what we have works fine")

6. **Competitive Landscape**
   - Any competitors mentioned, with exact context
   - How Solum was positioned against them
   - Whether the prospect is in an active evaluation

7. **Recommended Next Move**
   - The single most important thing to do before the next call
   - Specific action, not vague ("Send the ROI doc with their numbers by Thursday"
     not "Follow up soon")

8. **Fact-Check Notes**
   - Any discrepancies found during Phase 2
   - Data that needs verification
   - Attendees not in CRM
   - Confidence rating for the overall data quality

### Phase 4: Presentation

Present the three deliverables in this order:

1. **Internal Debrief first** — so JP sees the strategic picture before the tactical outputs
2. **Follow-Up Email Draft** — clearly marked as ready to paste
3. **HubSpot Deal Notes** — with specific fields to update

After presenting, ask:
- "Want me to adjust the email tone or add anything?"
- "Should I update the HubSpot deal with these notes?" (if HubSpot MCP supports writes)
- "Any other attendees I should look up in Apollo?"

## Edge Cases

**No Fireflies transcript found:**
- Tell the user which searches were tried
- Ask if the meeting was recorded on a different platform (Fathom, Zoom, etc.)
- Offer to generate a follow-up based on what the user remembers (manual input mode)

**No HubSpot deal exists:**
- Suggest creating one with recommended stage, amount, and contacts
- Still generate all three deliverables using available data

**Multiple meetings match the search:**
- Present the list with dates, titles, and attendees
- Ask the user to pick the correct one
- Default to the most recent if user says "the latest one"

**Internal meeting (not a prospect call):**
- Skip the follow-up email
- Generate a shorter debrief focused on decisions made and action items
- Skip deal stage recommendations

**Very short call (under 10 minutes):**
- Flag that the call was brief
- Adjust expectations — shorter debrief, simpler email
- Check if the call was cut short or if it was intentionally brief

## Required MCP Tools

This skill requires these MCP integrations to be connected:
- **Fireflies** — for transcripts and summaries
- **HubSpot** — for deal and contact data
- **Apollo.io** — for contact enrichment

If any are missing, tell the user which ones are needed and proceed with what's available.
Generate the deliverables using whatever data sources are connected, and note what's
missing in the output.

## Important Notes

- **Quote the prospect.** The email and debrief should reference specific things they said.
  Generic follow-ups are worthless.
- **Be honest in the debrief.** If the call went badly, say so. If the deal is at risk,
  flag it. JP needs the truth, not optimism.
- **Match email tone to the relationship.** A first meeting email reads differently from
  a fifth meeting email. Check prior threads.
- **Track commitments ruthlessly.** If Solum promised something on a prior call and didn't
  deliver, flag it immediately. If the prospect promised something and didn't deliver,
  note it for the next call.
- **No AI slop in the email.** Zero dashes as punctuation. No "I wanted to follow up on our
  productive conversation." No "leverage", "streamline", "robust", "comprehensive." Write
  like a real person sending a real email.
- **Keep the email SHORT.** Under 150 words. Under 100 is better. Nobody reads long
  follow-up emails.
