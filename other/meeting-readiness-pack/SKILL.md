---
name: meeting-readiness-pack
description: "Prepares the user for an upcoming meeting by pulling context from calendars, email, chat, notes, CRM, and trackers, then drafting a time-boxed agenda, a one-page pre-read brief, and concrete talking points, with prep depth scaled to the meeting type. Use when the user asks to prepare for a meeting, 1:1, client call, project review, board session, interview, or brainstorm, or wants an agenda, a briefing document, or points to raise."
---

# Meeting Readiness Pack

You get the user ready for a meeting. Collect what is already known about the meeting and the people in it, then produce the pieces they need: an agenda that fits the time slot, a short briefing for attendees where one is warranted, and the specific points the user should bring up. Match your effort to the stakes — a quick 1:1 deserves far less than a board presentation.

## Where the context comes from

Draw on the connected tools and sources available:

| Source | Examples | Useful for |
|---|---|---|
| Calendar | Google Calendar, Outlook Calendar | Title, time, attendee list, location, any attached agenda |
| Email | Gmail, Outlook | Recent exchanges with attendees, documents they shared |
| Chat | Slack, Microsoft Teams | Recent conversations with attendees, what's going on in relevant channels |
| Notes and docs | Notion, Confluence, Google Docs | Notes from earlier meetings, shared documents, project pages |
| CRM | Salesforce, HubSpot | For external meetings: account history, deal status, contact details |
| Work tracking | Jira, Linear, Asana | Open items tied to the meeting topic |
| Uploaded documents or connected knowledge sources | — | Templates for recurring meetings, background documents |

If nothing is connected, ask the user to give you the meeting details, what they know about the attendees, and any notes by hand.

## How to prepare

Run through the following steps for every preparation request, going deeper or lighter depending on how important the meeting is.

### 1. Nail down the basics

Establish:

- **Type of meeting** — for example a 1:1, a team standup or retrospective, a project review, a decision meeting, a brainstorm, an informational session, an interview, a client call, or a board meeting.
- **Who's attending** — names and roles, and whether anyone is external (clients, partners, vendors).
- **Length** — the duration sets the limits of the agenda.
- **Objective** — what should be true once the meeting ends that isn't true now? If the user can't put it into words, work it out with them; a meeting with no objective produces nothing of value. Don't assume the objective yourself — ask before you draft an agenda.
- **One-off or recurring** — for a recurring meeting, retrieve the notes from earlier sessions where available.

### 2. Collect the context

From the connected sources, gather:

- **Earlier meetings with the same people:** the notes from the last one, its action items and decisions; action items still outstanding from past sessions; topics that were postponed or parked.
- **Recent correspondence:** email threads with the attendees over the past 1–2 weeks, messages in relevant chat channels, shared documents edited recently.
- **Where the project or account stands:** open tasks or issues connected to the topic. For external meetings, add account status, deal stage, and recent interactions from the CRM. For project meetings, add milestone status, blockers, and recent changes.
- **Background material:** pre-reads the organizer has already circulated, plus relevant policies, specifications, or reference material from uploaded documents or connected knowledge sources.

With no connected sources, ask the user for whatever context they have. Even two sentences on "what this meeting is for and what happened last time" make a big difference to how good the preparation is.

### 3. Draft the agenda

Lay it out like this:

```
# [Name of the meeting]

| When | Length | Who is coming | Goal: what should be true afterward |
|---|---|---|---|
| [date and time] | [duration] | [attendee list] | [objective] |

## Running order
| # | Item | Minutes | Notes |
|---|---|---|---|
| 1 | Opening / check-in | [X] | [quick framing or warm-up] |
| 2 | [Topic A: most important] | [X] | Background: [one or two sentences] · Decision required? [no / yes, and what must be decided] · Pre-read: [link or reference, if there is one] |
| 3 | [Topic B] | [X] | Background: [...] · Decision required? [...] |
| 4 | [Topic C] | [X] | Background: [...] |
| 5 | Wrap-up: action items and next steps | 5 | Recap what got decided; give every action item an owner and a deadline |

## Still open from the previous meeting
| Item | Owner | Status: done / in progress / not started |
|---|---|---|
| [item] | [name] | [status] |
```

Keep these rules in mind while building it:

- **Give every item a time box.** The allocations together may not exceed the meeting length minus 5 minutes; that buffer absorbs overruns and the wrap-up.
- **Order by importance.** The most important or most time-sensitive topic goes first, so that if the meeting overruns, the critical item has still been covered.
- **Separate decisions from discussions.** Mark each topic that needs a decision; those require the decision-maker in the room and enough background to choose well.
- **Cap the number of topics.** Aim for 3–5 substantive items in a 30-minute meeting and 5–7 in a 60-minute one. Any more and none of them gets proper attention.
- **Carry over last meeting's open items.** People stay accountable only when their commitments are visible.

### 4. Write the pre-read brief (when attendees need background)

Project reviews, client calls, and board meetings usually call for a briefing document. Use this structure:

```
# Pre-read: [Name of the meeting]
Written [date] for the meeting on [date and time]

## The short version
  [2–3 sentences: the reason for meeting, the thing that matters most, and the decision we need]

## Background
  [what attendees must know, one page maximum; link out to detailed sources rather than pasting them in]

## Numbers and facts
  | Fact or metric | Where it came from |
  |---|---|
  | [first]  | [source] |
  | [second] | [source] |
  | [third]  | [source] |

## Questions to settle in the room
  1. [question]
  2. [question]

## How we got here
  - [date]: [the decision, milestone, or change that occurred]
  - [date]: [...]

## Points worth raising
  - [point, plus why it should come up]
  - [point]
  - [point]
```

Writing guidance for the brief:

- **Short wins.** A one-page brief people actually read is worth more than ten pages nobody opens.
- **Cite everything.** Each data point, claim, or reference to past events needs its source, so attendees can follow up if they want more detail.
- **Open with the ask.** When a decision is needed, put the question and the options first and the background second.

### 5. Propose talking points

Using what you found, recommend specific things for the user to raise. Pick from these kinds:

| Kind | Reach for it when | Sample wording |
|---|---|---|
| **Follow-up from the last meeting** | someone took on an action item, or a topic got put off | "We committed to [X] last time. Where does it stand?" |
| **Proactive update** | the user has news or progress the attendees should hear about | "Let everyone know [milestone] is done / [blocker] is cleared." |
| **Question to ask** | the user needs information from someone in the room | "Check with [person] on [topic], since [reason] depends on it." |
| **Risk to flag** | a risk or concern ought to surface early | "Warn that [risk] might hit [timeline/outcome]." |
| **Decision to drive** | a decision is still outstanding and needs attention | "[Topic] needs a decision: do we go with [A] or [B]?" |

## Prep depth by meeting type

Scale the steps above to the kind of meeting:

| Meeting type | How much prep | What to concentrate on |
|---|---|---|
| **1:1 (manager/report)** | Light, about 5–10 min | Open action items, blockers, career and development topics |
| **Team standup** | Minimal, about 2 min | The user's status, blockers, help needed |
| **Project review** | Medium, about 15–20 min | Milestone status, risks, decisions needed, timeline |
| **Client or external call** | Full, about 20–30 min | What the user wants out of the call, the account's history, the state of the relationship, and a pre-read |
| **Board or executive** | Full, 30+ min | The storyline, headline metrics, the decisions being sought, and a full pre-read package |
| **Interview** | Medium, about 15 min | What the role demands, the candidate's background, and a set of questions ready to ask |
| **Brainstorm** | Light, about 10 min | A crisp problem statement, the constraints, a few starter ideas, and creative prompts |

## Ground rules

- Don't invent meeting history or attendee backgrounds. If earlier notes or organizational data aren't available, ask the user.
- Don't make up metrics or data points for a brief. Put `[Input required — ask the user]` in their place.
- Don't assume what the meeting is for. Ask about the objective before drafting the agenda.
- Mark where each piece comes from: `[Via connected tool]` for anything pulled from a connected tool or source, `[Per the user]` for what the user told you, `[My suggestion]` for your own proposals, and `[Input required]` wherever information is still missing.
