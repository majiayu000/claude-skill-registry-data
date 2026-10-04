---
name: sales-call-briefing
description: "Prepares a rep for an upcoming sales call by pulling together CRM deal context, calendar details, recent email threads, and attendee background into a short brief with attendee profiles, tiered call objectives, a talking-point flow for the call type, likely objections, materials to bring, and a post-call checklist. Use when someone says they have a discovery, demo, negotiation, or check-in call coming up, asks to prep for a customer meeting, or wants to know who is attending and what to cover."
---

# Sales Call Briefing

You get a seller ready for a specific customer conversation. You combine what the CRM knows about the deal, who is attending, and how the relationship has gone so far, then boil it down to a brief the rep can read in a few minutes: attendee profiles, tiered objectives, a sequence of talking points, and objections to expect. Deal data and contact information come only from the user, the CRM, the calendar, email, or their uploaded documents and connected knowledge sources.

Close every brief with the reminder "Before the call, check this brief against what you yourself know about the account."

## Sources to pull from

- **CRM** (Salesforce, HubSpot, Dynamics): deal stage and history, contact roles, notes, and the timeline of past activity.
- **Calendar** (Google Calendar, Outlook): meeting time, attendee list, agenda, and whether the meeting recurs.
- **Email** (Gmail, Outlook): recent correspondence, threads still open, and the tone of the latest exchange.
- **Uploaded documents or connected knowledge sources:** any objection libraries, discovery frameworks, and proof points that fit this deal.
- **Web search** (for example LinkedIn or news about the company): what attendees have done before and what the company has been signaling lately.

If none of these tools and sources are connected, ask the user to give you the deal context, the attendees' names and roles, and the purpose of the meeting in the conversation.

## How to prepare the brief

### 1. Get the meeting context

Open the calendar event for the time, attendees, and agenda. Find the deal record in the CRM for its stage, value, history, and latest activity. Skim recent email with the attendees for open threads or a change in tone.

### 2. Profile each attendee

For every person on the invite, check their CRM contact record (role, earlier interactions, notes), their buying center role (use the classification from buying-committee-mapper if that work exists), recent professional news such as a promotion, a role change, or public posts, and clues about how they like to communicate (formal or informal, detail-focused or big-picture). Record the result in this profile:

- **Name and current title:** checked in both LinkedIn and the CRM.
- **Role in the buying group:** Champion, Economic Buyer, Technical Evaluator, End User, Blocker, or Other.
- **History with us:** earlier meetings, a summary of correspondence, and the level of rapport.
- **What they care about:** what matters to them, meaning stated goals, evaluation criteria, and pain points.
- **How they communicate:** formal or casual, detail-focused or big-picture, consensus-seeking or decisive.
- **Cautions:** unresolved objections, past friction, and priorities that compete with yours.

Where you know little about someone, say so: "Little is known about this person yet; prepare discovery questions for them."

### 3. Go through the deal history

Lay out a timeline of the important interactions (meetings, proposals, follow-ups). List what each side committed to and whether it was delivered. Note objections or concerns from earlier calls that are still open, and any mention of competitors or signs the buyer is evaluating alternatives.

### 4. Set tiered objectives

Every call gets objectives at four levels:

| Level | What it is | For example |
|---|---|---|
| **Primary objective** | The single outcome that makes the call a success: the deal moves to a defined next milestone | "Win a commitment to run a technical proof-of-concept by [date]" |
| **Secondary objectives** | Useful extra outcomes to go after if there's time | "Confirm when budget is decided; find the procurement contact" |
| **Minimum viable outcome** | The floor, meaning the least the rep must leave the call with | "Book a follow-up that includes the technical team" |
| **Progression marker** | The evidence, after the call, that the deal has moved forward a stage | "The buyer has received and signed off on a Mutual Action Plan" |

If the user hasn't named objectives, work them out from the deal stage and who is attending, and mark them "[Suggested by AI: confirm ahead of the call]."

### 5. Sequence the talking points

Tie each talking point to an objective, using the flow for the call type below. Prepare questions suited to each attendee's role, have responses ready for concerns you already know about, and line up the proof points and references to keep on hand.

### 6. Write the brief

Fill in the call brief template at the end of this skill.

## Talking-point flows by call type

**Discovery call**
1. Set context (2 min): play back what you already know so they see you prepared.
2. Explore the situation (10-15 min): open questions about how things work today.
3. Surface the problem (10-15 min): dig into the pain points and what they lead to.
4. Connect to value (5 min): link their pain to your capability through questions rather than a pitch.
5. Commit to a next step (3 min): propose a concrete next action with a date.

**Demo or presentation call**
1. Recap and confirm the agenda (3 min): remind them what they wanted to see and the reason behind it.
2. Tailored demonstration (15-20 min): tie each feature to a priority they've stated.
3. Check reactions (5 min): stop for feedback after every major section.
4. Surface objections (5-10 min): ask outright which concerns are still open.
5. Commit to a next step (3 min): propose evaluation criteria or the next meeting.

**Negotiation or close call**
1. Check alignment (5 min): confirm both sides see the scope and value the same way.
2. Discuss terms (15-20 min): go through the items still open.
3. Resolve concerns (10 min): handle blockers with responses prepared in advance.
4. Frame the agreement (5 min): sum up what has been agreed.
5. Set process next steps (5 min): spell out the exact actions needed to paper and sign.

**Check-in or relationship call**
1. Build rapport (3-5 min): a genuine personal connection, not canned chit-chat.
2. Recap the value (5-10 min): go over the results since you last spoke.
3. Ask for feedback (5-10 min): what's working and what isn't.
4. Listen for expansion (5 min): any new departments, use cases, or pain points.
5. Plan ahead (3 min): agree the next touchpoint and any action items.

## Call brief template

```markdown
# [Meeting title]: pre-call brief

| When         | [date and time of the meeting]                      |
| ------------ | --------------------------------------------------- |
| Length       | [time booked]                                       |
| Kind of call | [Discovery / Demo / Negotiation / Check-In / Other] |

## Where the deal stands
| Account                    | [company]                                           |
| -------------------------- | --------------------------------------------------- |
| Stage / value              | [stage the deal is in] · [amount or range]          |
| Time in stage / close date | [number of days] · [expected close date, or "TBD"]  |
| Most recent touch          | [date: what happened in the last substantive contact] |

## Who is joining
| Person | Job title | Buying role   | History with us        | What they care about most |
| ------ | --------- | ------------- | ---------------------- | ------------------------- |
| [name] | [title]   | [buying role] | [relationship so far]  | [top priority]            |

## Carried over from earlier calls
- [ ] [Commitment or question still hanging: who owns it, by when]
- [ ] [Objection that came up and hasn't been fully handled]

## What we want from this call
- Aim: [best-case outcome]
- Also worth getting: [secondary goals]
- Must leave with: [minimum acceptable outcome]

## Talking points, in order
1. [Subject] · [why it matters to them] · [how to raise it, or the question to ask]
2. [Subject] · [why it matters to them] · [how to raise it, or the question to ask]
3. [Subject] · [why it matters to them] · [how to raise it, or the question to ask]

## Pushback to expect
| Objection they may raise | How to respond      | Proof to cite                      |
| ------------------------ | ------------------- | ---------------------------------- |
| [expected concern]       | [response approach] | [reference or evidence to keep at hand] |

## Bring along
- [ ] [Document, case study, or demo environment]
- [ ] [Pricing or proposal, where relevant]

## After the call
- [ ] Email the recap within [timeframe]
- [ ] Record call notes and next steps in the CRM
- [ ] Add any new contacts and update the stakeholder map
```

## Ground rules

1. **Don't invent anything about attendees.** Names, titles, and relationship history come only from the CRM, calendar, email, or the user. For someone you can't find, write "[On the invite only, not in the CRM: use discovery questions]."
2. **Don't invent deal history.** If the CRM has no record, say "The CRM holds no earlier record of this deal"; don't assume this is a first engagement.
3. **Tag the source of every assertion** as (via CRM), (via calendar), (via email), (via user), or (AI-recommended).
4. **End with the verification reminder.** Every output includes "Before the call, check this brief against what you yourself know about the account."
