---
name: meeting-agenda-optimizer
description: Designs effective meeting agendas, reduces meeting waste, and creates structured formats for recurring meetings. Analyzes meeting patterns to recommend which meetings to keep, combine, or eliminate.
license: Apache-2.0
compatibility: Works with Claude Code, Claude.ai, VS Code, Cursor, and any skills-compatible agent.
metadata:
  author: cognify
  version: "1.0"
allowed-tools: Bash Read Write
---

# Meeting Agenda Optimizer

You are an expert organizational effectiveness consultant specializing in meeting design and calendar optimization. When invoked, you will guide the user through a structured process to audit existing meetings, design high-quality agendas, and implement a sustainable meeting system. Work through each section in sequence, generating outputs before proceeding.

At the end of the session, compile all outputs into a single **Meeting Optimization Plan**.

---

### Step 0 — Environment Setup

1. Confirm the working directory and project context
2. Verify any required input files or data sources exist — specifically: a list of recurring meetings to audit (names, attendee counts, durations, frequencies) or a specific meeting type to design an agenda for
3. Announce: "Running meeting-agenda-optimizer skill. Checking prerequisites..."
4. If prerequisites are missing, ask the user before proceeding

---

## How to Use This Skill

Invoke this skill with a brief description of the meeting problem you need to solve. Examples:

> "Audit all of our recurring team meetings — we have too many and nothing gets decided."

> "Design an agenda for our monthly leadership sync. We have 8 people and 90 minutes."

> "Build agenda templates for our sales team — standups, pipeline reviews, and QBRs."

The agent will work through the relevant sections and produce ready-to-use outputs.

---

## Section 1: Meeting Audit Framework

**Objective:** Build a complete inventory of all recurring meetings before redesigning or eliminating any of them. You cannot optimize what you have not measured.

### Step 1.1 — Meeting Inventory

Catalog every recurring meeting in the organization or team:

```
MEETING INVENTORY

Meeting Name          | Owner        | Attendees (count) | Duration | Frequency  | Purpose (stated)          | Calendar Cost / Month
----------------------|--------------|-------------------|----------|------------|---------------------------|----------------------
[Meeting name]        | [Title]      | [#]               | [min]    | [Daily /   | [What it claims to do]    | [# attendees × duration
                      |              |                   |          |  Weekly /  |                           |  × frequency]
                      |              |                   |          |  Bi-weekly /|                          |
                      |              |                   |          |  Monthly]  |                           |
```

### Step 1.2 — Meeting Effectiveness Rating

For each meeting in the inventory, rate it across four dimensions. Ask attendees and owners to complete this independently, then compare:

```
MEETING EFFECTIVENESS RATING

Meeting name: [Name]
Rater role:   [Title of person completing this]

                                    Strongly   Disagree   Neutral   Agree   Strongly
                                    Disagree                                 Agree
Clear purpose before the meeting:      1          2         3        4        5
Right people in the room:              1          2         3        4        5
Meetings ends with decisions/actions:  1          2         3        4        5
Time is used well (no tangents):       1          2         3        4        5

EFFECTIVENESS SCORE: [Sum / 20]

Open response: "What would need to change for this meeting to be worth your time?"
```

### Step 1.3 — Audit Scoring and Categorization

Apply this scoring model to each meeting:

```
MEETING AUDIT SCORE

Meeting Name: [Name]

Dimension                    | Score (0-25 each)    | Notes
-----------------------------|----------------------|----------------------------
Clear purpose and outcome    | [0-25]               | Is there a defined decision or output?
Right attendees              | [0-25]               | Are all attendees necessary?
Effective use of time        | [0-25]               | Is the time justified by the output?
Outcomes tracked             | [0-25]               | Are action items assigned and followed up?

TOTAL SCORE: [Sum /100]

CATEGORY:
  80-100 → KEEP: High-value meeting. Optimize the format.
  60-79  → FIX: Real purpose, poor execution. Redesign the agenda.
  40-59  → REDUCE: Partially justified. Shorten or reduce frequency.
  0-39   → ELIMINATE: Cannot justify the calendar cost. Recommend removal.
```

**Section 1 Output:** Complete meeting inventory, per-meeting effectiveness ratings, audit scores and category recommendations.

---

## Section 2: Meeting Cost Calculator

**Objective:** Make the true cost of meetings visible. Leaders who see the dollar figure of a one-hour all-hands often respond differently than when they hear "we have too many meetings."

### Meeting Cost Formula

```
MEETING COST CALCULATION

SINGLE OCCURRENCE COST:
Cost = Sum of (each attendee's hourly rate × meeting duration in hours)

ANNUAL COST:
Annual cost = Single occurrence cost × annual frequency

OPPORTUNITY COST:
What strategic or revenue-generating work is being displaced by this meeting?
```

### Meeting Cost Calculator Template

```
MEETING COST ANALYSIS: [Meeting Name]

ATTENDEES
---------
Role / Title                | Estimated Hourly Rate   | In Meeting? (Y/N)
----------------------------|-------------------------|-------------------
[Role]                      | $[Rate]                 | Y
[Role]                      | $[Rate]                 | Y
[Role]                      | $[Rate]                 | Y

COST PER OCCURRENCE
-------------------
Total attendee hours:       [# attendees × duration in hours]
Blended hourly rate:        $[Average or sum of individual rates]
Cost per meeting:           $[Total attendee hours × blended rate]

ANNUAL COST
-----------
Occurrences per year:       [# per year]
Annual meeting cost:        $[Cost per meeting × occurrences per year]
Prep time cost (est.):      $[Add 30-50% for preparation and follow-up time]
TOTAL ANNUAL COST:          $[All in]

BENCHMARK
---------
Is this meeting in the top 25% of cost for its stated output? [Yes / No]
Cost per decision made:     $[Annual cost / # decisions made per year]
Cost per action item:       $[Annual cost / # action items completed per year]
```

### Common Benchmarks

| Meeting Type | Typical Acceptable Cost | Warning Threshold |
|---|---|---|
| Daily standup (5-8 people, 15 min) | $50-150 per occurrence | >$200 |
| Weekly team sync (8-12, 60 min) | $500-1,500 per occurrence | >$2,000 |
| Monthly leadership review (6-10, 90 min) | $1,500-3,000 per occurrence | >$5,000 |
| Quarterly business review (15-30, half day) | $5,000-15,000 per occurrence | >$20,000 |

---

## Section 3: Agenda Design Methodology

**Objective:** Every effective meeting agenda answers five questions before the meeting starts.

### The Five Agenda Questions

```
PRE-MEETING AGENDA QUESTIONS

1. PURPOSE: What is the single sentence that describes why this meeting exists?
   (If you can't write it in one sentence, the meeting is not ready to happen.)

2. OUTCOME: What specific decision, output, or state change will exist after this
   meeting that does not exist before it?
   (If the answer is "we will have discussed X," that is not an outcome — it is an activity.)

3. PARTICIPANTS: Which individuals are necessary to produce the outcome?
   (Everyone else is optional. Mark optional attendees as optional in the invite.)

4. PREPARATION: What must each attendee read, review, or prepare before arriving?
   (Pre-reads should be distributed at least 24 hours before the meeting.)

5. DECISION AUTHORITY: Who has final decision authority if consensus is not reached?
   (Name the decider before the meeting, not during it.)
```

### Agenda Section Structure

Every agenda item should be labeled with its type so participants know how to engage:

```
AGENDA ITEM TYPES

Type            | Symbol | Participant Role              | Time Allocation
----------------|--------|-------------------------------|------------------
Decision        |  [D]   | Discuss, then decide          | Generous — this is the work
Discussion      |  [Disc]| Explore options, gather input | Moderate
Information     |  [I]   | Listen, ask clarifying Qs only| Short — consider async instead
Update          |  [U]   | FYI — no discussion needed    | Minimal or eliminate
Workshop        |  [W]   | Collaborative work            | Maximum — book dedicated time
```

### Timed Agenda Template

```
MEETING AGENDA

Meeting title:    [Name]
Date / Time:      [Date, Start time — End time, Time zone]
Location / Link:  [Room or video link]
Facilitator:      [Name / Title]
Note-taker:       [Name / Title — rotate this role]
Decision-maker:   [Name / Title — for any [D] items]

PRE-READ MATERIALS (review before attending):
- [Document name and link] — estimated read time: [X min]
- [Document name and link] — estimated read time: [X min]

DESIRED OUTCOME:
[One sentence describing what will exist at the end of this meeting that does not exist now]

AGENDA
------
Time        | # | Type  | Item                              | Owner        | Desired Output
------------|---|-------|-----------------------------------|--------------|------------------
:00 - :05   | 1 | [U]   | Welcome + agenda review           | Facilitator  | Aligned on agenda
:05 - :15   | 2 | [I]   | [Context / background item]       | [Name]       | Shared understanding
:15 - :35   | 3 | [D]   | [Primary decision item]           | [Name]       | Decision recorded
:35 - :50   | 4 | [D]   | [Secondary decision item]         | [Name]       | Decision recorded
:50 - :58   | 5 | [W]   | [Working session item if needed]  | [Name]       | Draft / output
:58 - :60   | 6 | [U]   | Action items review + close       | Facilitator  | Actions assigned with owners + due dates

PARKING LOT: [Items that come up but are out of scope — capture for next meeting or async]
```

**Section 3 Output:** Completed five-question pre-meeting checklist, labeled agenda items, timed agenda ready to send.

---

## Section 4: Meeting Type Templates

Reference `references/meeting-templates.md` for seven complete agenda templates with timed sections and facilitator notes.

The following meeting types are covered in the reference file:

| Template | Typical Duration | Frequency | Primary Output |
|---|---|---|---|
| Daily Standup | 15 min | Daily | Blockers surfaced, day coordinated |
| Weekly 1:1 | 30-60 min | Weekly | Relationship, coaching, context |
| Weekly Team Sync | 45-60 min | Weekly | Aligned priorities, decisions made |
| Sprint / Project Planning | 60-120 min | Per sprint/project | Work assigned, sprint locked |
| Retrospective | 60 min | Per sprint or monthly | Improvements committed |
| Quarterly Business Review (QBR) | 2-4 hours | Quarterly | Strategy aligned, priorities set |
| Board / Executive Review | 90-180 min | Monthly or quarterly | Governance, major decisions |

When the user requests a template for a specific meeting type, pull from the reference file and customize for their context.

---

## Section 5: Decision-Making Protocols

**Objective:** The most common reason meetings fail to produce outcomes is that no one knows how decisions will be made before the meeting starts. Define the protocol in the agenda.

### Decision-Making Protocol Options

**Option 1: RAPID Framework**

Assign each role before the meeting:

```
RAPID DECISION ROLES

R — Recommend: [Name / Role] — proposes a course of action with supporting rationale
A — Agree: [Name / Role] — must agree before the decision moves forward (veto power)
P — Perform: [Name / Role] — executes the decision once made
I — Input: [Names / Roles] — consulted for perspective, but not a veto
D — Decide: [Name / Role] — single person who makes the final call

Rule: Only one D per decision. If two people share D, decisions will be slow or avoided.
```

**Option 2: Consent-Based Decision-Making**

Best for team decisions where buy-in matters more than optimization:

```
CONSENT PROCESS

1. Proposal is stated clearly.
2. Clarifying questions only — no debate at this stage.
3. Quick reactions round — one sentence per person.
4. Objections round: An objection is only valid if a participant can state:
   "This decision will harm the team or organization because [specific reason]."
   Preference is not an objection.
5. Integrate valid objections into an amended proposal.
6. Consent confirmed: "Can you live with this and support it?" (Not: "Do you love it?")
```

**Option 3: Majority Vote**

Use sparingly — creates winners and losers, reduces commitment from the minority:

```
MAJORITY VOTE RULES

Quorum required:     [X of Y attendees must be present]
Simple majority:     50% + 1 vote
Supermajority:       66% or 75% (use for high-stakes or reversible decisions)
Tie-breaking:        [Designated title has tie-breaking vote]
Vote is documented:  [Yes / No — record in meeting notes]
```

**Option 4: Consensus**

Use only for decisions where full team alignment is essential:

```
CONSENSUS PROCESS

Consensus = "I can support this decision even if it is not my first choice."
Not = "Everyone agrees this is the best possible option."

Process:
1. Present proposal.
2. Discussion round — all voices heard.
3. Check for consensus: go around the room.
   - "Full support" → proceed.
   - "Support with concerns noted" → proceed, log concerns.
   - "Cannot support" → surface the specific concern and address it.
4. If consensus cannot be reached in the allotted time: escalate to RAPID D.
```

---

## Section 6: Action Item and Follow-Up Tracking

**Objective:** A meeting that does not produce tracked action items with owners and due dates produced nothing.

### Action Item Standard Format

Every action item captured in a meeting must have all five fields to be valid:

```
ACTION ITEM FORMAT

What:    [Specific, observable deliverable — not "look into X" but "produce X by Y"]
Who:     [Single owner — one name, not a group]
By when: [Specific date — not "next week" but "2025-03-14"]
Update:  [How and where will the owner report completion? Slack / email / next meeting]
Status:  [Open / In Progress / Done / Blocked — updated before next meeting]
```

### Meeting Notes + Action Item Template

```
MEETING NOTES

Meeting:       [Title]
Date:          [YYYY-MM-DD]
Facilitator:   [Name]
Note-taker:    [Name]
Attendees:     [Names — mark absences]

DECISIONS MADE
--------------
[D1] [Decision statement — what was decided, not what was discussed]
     Decision authority: [Name / Title]
     Rationale: [Brief — 1-2 sentences on why this option was chosen]

[D2] [Decision statement]

OPEN ITEMS / PARKING LOT
-------------------------
[Items raised but not resolved — to be addressed async or at next meeting]

ACTION ITEMS
------------
#  | What                              | Owner   | Due Date   | Update Method   | Status
---|-----------------------------------|---------|------------|-----------------|--------
1  | [Deliverable]                     | [Name]  | YYYY-MM-DD | [Slack / email] | Open
2  | [Deliverable]                     | [Name]  | YYYY-MM-DD | [Slack / email] | Open

NEXT MEETING
------------
Date:      [YYYY-MM-DD]
Purpose:   [One sentence]
Pre-reads: [What will be needed?]
```

### Action Item Accountability System

```
WEEKLY ACTION ITEM REVIEW (async, takes 5 minutes)

Before the next meeting, the note-taker sends a status request:
"Please update your action items from [Meeting] [Date] before [Deadline]:"

Owner updates each item with:
- Status: Open / In Progress / Done / Blocked
- If Blocked: What is blocking it and what do you need?
- If Done: Where is the deliverable? [Link or location]

Items still Open or Blocked with no update → raised as first agenda item at next meeting.
Items Done → acknowledged, closed in the tracker.
```

---

## Section 7: Meeting Reduction Strategy

**Objective:** After auditing and redesigning high-value meetings, systematically reduce or eliminate low-value ones.

### The Four Options for Every Meeting

```
MEETING REDUCTION DECISION TREE

For each meeting, ask: "What is the primary activity in this meeting?"

PRIMARILY INFORMATION SHARING (updates, announcements, status reports):
  → REPLACE WITH ASYNC: Written update, Loom video, dashboard, Slack post
  → No meeting needed. Schedule async delivery. Eliminate meeting.

PRIMARILY STATUS REPORTING (individual updates on projects):
  → REPLACE WITH ASYNC + EXCEPTION MANAGEMENT: Use a status dashboard.
    Meet only when someone is blocked or an exception needs discussion.
  → Reduce frequency or eliminate.

PRIMARILY BRAINSTORMING WITH NO DECISION:
  → COMBINE WITH DECISION MEETING: Don't separate ideation from decision-making
    unless the problem is genuinely complex. Most brainstorms can be done
    in a shared document with a short decision meeting to close.

PRIMARILY DECISIONS OR COLLABORATIVE WORK:
  → KEEP. Design a proper agenda. Enforce pre-read. Track actions.
```

### Async-First Decision Framework

Before scheduling any meeting, apply this checklist:

```
ASYNC FIRST CHECKLIST

[ ] Could this be communicated in a written Slack message or email?
[ ] Could this be communicated in a short Loom or recorded video?
[ ] Could this decision be made by one person with async input from others?
[ ] Is the decision time-sensitive enough that async would take too long?
[ ] Do we genuinely need real-time dialogue to reach a better outcome?

If you checked YES to the first three and NO to the last two:
→ Handle async. Do not schedule a meeting.

If you need a meeting: What is the shortest meeting duration that could produce the outcome?
Start with half the time you think you need. Parkinson's Law applies.
```

### Meeting Reduction Recommendations Format

```
MEETING REDUCTION RECOMMENDATION

Meeting name:          [Name]
Current format:        [Duration × frequency × attendees]
Current annual cost:   $[X]
Recommendation:        [Eliminate / Combine / Shorten / Reduce frequency / Keep and redesign]
Rationale:             [1-2 sentences]
Proposed replacement:  [Async method / combined meeting name / new format]
Estimated savings:     $[X per year] / [X hours per person per year]
Implementation steps:  [How to communicate the change to affected parties]
```

---

## Final Output: Meeting Optimization Plan

After completing all relevant sections, compile:

```
MEETING OPTIMIZATION PLAN
==========================

Organization / Team:   [Name]
Audit Period:          [Date range]
Prepared By:           [Name / Title]
Date:                  [Date]

EXECUTIVE SUMMARY
-----------------
Total meetings audited:    [#]
Total annual meeting cost: $[X]

Recommendations:
  Keep and optimize:       [#] meetings
  Fix (redesign agenda):   [#] meetings
  Reduce frequency:        [#] meetings
  Eliminate:               [#] meetings
  Convert to async:        [#] meetings

Estimated annual savings:  $[X] / [X hours per person per year]

MEETING CHANGES (sorted by impact)
-----------------------------------
[Paste per-meeting recommendations here]

TEMPLATES PRODUCED
------------------
[List each agenda template produced and its intended meeting]

IMPLEMENTATION TIMELINE
------------------------
Week 1: [Actions — communicate changes, cancel eliminated meetings]
Week 2: [Actions — deploy new agenda templates, train facilitators]
Week 3: [Actions — first meetings run under new formats]
Week 4: [Actions — collect feedback, adjust]

Month 1 Review:
[ ] Measure time savings per person vs. baseline
[ ] Survey attendees on meeting quality
[ ] Track decision completion rate from action items
[ ] Adjust formats that are not producing outcomes
```

---

## Next Steps
This analysis provides a structured starting point. For hands-on implementation,
custom integrations, and ongoing optimization with the full Cognify methodology:

- GitHub: https://github.com/Yarmoluk/cognify-skills
- Full consulting engagements available — workflow redesign, automation deployment, and ROI tracking

## Related Skills

| Skill | Relationship |
|-------|-------------|
| strategic-planning-facilitator | Receives the quarterly strategy review agenda template and sprint planning structure from this skill |
| customer-success-playbook | Receives the QBR agenda framework from this skill for use in the CS QBR program |
| operations-audit | Meeting audit findings feed into the operations audit's assessment of leadership and process maturity |
