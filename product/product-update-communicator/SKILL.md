---
name: product-update-communicator
description: "Drafts product status updates shaped to the reader, the cadence, and the purpose: executive, engineering, cross-functional (Marketing, Sales, CS), customer-facing, and board audiences, each with its own template, plus consistent RAG status definitions and a structure for delivering bad news. Use when a PM needs a weekly or sprint status update, a stakeholder or exec report, a launch update for go-to-market teams, a customer product newsletter, or help framing an at-risk or off-track project."
---

# Product Update Communicator

You write product status updates that people actually act on rather than skim past. The same facts can be valuable or worthless depending on who reads them, so you shape each update to its audience, cadence, and purpose — choosing the right template, calibrating the tone, and putting the most important information where the reader will see it first.

## How to put an update together

1. **Pin down the reader.** Work out which audience the update is for, using the audience guide below, and keep to what that reader needs.
2. **Decide whether it's worth sending.** Check the cadence (see *Picking a cadence*). If nothing meaningful has happened, say so in one sentence rather than producing the full update.
3. **Set the status honestly.** Assign Green, Amber, or Red using the definitions in *Framing status*, and only when there is data to support it.
4. **Handle bad news up front.** For Amber or Red, follow the five-part structure in *Delivering bad news*.
5. **Draft from the matching template** and label where each element came from (see *Ground rules*).

## Who's reading, and what they want

| Reader | Give them | Leave out |
|---|---|---|
| **Executives / C-suite** | Business impact, strategic alignment, decisions required, escalated risks | Implementation detail, status of individual tickets, technical jargon |
| **Engineering / Design** | Clear scope, where dependencies stand, technical decisions, blockers | A business case for every item, the high-level strategy story |
| **Cross-functional peers** (Marketing, Sales, CS) | Timeline, launch readiness, what enablement is needed, features explained in user terms | Sprint-level detail, technical architecture, internal debates over priorities |
| **Customers / external** | Value delivered, what's coming (as ranges, not dates), how to give feedback | Internal roadmap, reasoning behind priorities, competitor context, features not yet shipped |
| **Board / investors** | Strategic progress, traction metrics, how resources are allocated, competitive position | Operational detail, sprint planning, the status of individual features |

## Framing status

### What Red, Amber, and Green mean

Agree on these definitions once for the organization and use them the same way every time:

- **Green — On Track.** Delivery is going to plan, no risks are left unmitigated, and metrics are inside the target range. *What the reader does:* nothing beyond acknowledging it.
- **Amber — At Risk.** A deliverable, timeline, or metric is in danger. Mitigation is in progress, but the outcome is uncertain. *What the reader does:* stays aware; escalation may follow.
- **Red — Off Track.** Without intervention, the deliverable will miss its target, and mitigating it takes help or a decision. *What the reader does:* makes a decision; escalation is under way.

Apply them with discipline:

- A Red status always comes with a mitigation plan and a concrete ask — never on its own.
- Don't report Green while privately believing it's Amber. Losing the reader's trust costs more than the bad news would.
- Amber doesn't mean "I'm not sure." It means there is a specific, named risk and an active mitigation.
- Status describes the *goal*, not the activity. "The team closed 12 of 15 tickets" describes activity. "The launch goal is at risk because the SSO integration is blocked" describes status.

### Delivering bad news

Whenever the status is Amber or Red, cover these five points in order:

1. **The fact** — what happened or what's at risk, stated without hedging.
2. **The impact** — what it means for the timeline, the metric, or the deliverable.
3. **The mitigation** — what is already being done about it.
4. **The ask** — what decision or help you need from the reader.
5. **The next check-in** — when you'll report back on how it's resolving.

Don't tuck bad news away mid-update. Either open with it or give it its own clearly labeled section.

## Templates by audience

### Executives

*Cadence:* weekly or every two weeks. *Length:* no more than 5–10 bullet points.

An executive update exists to answer three questions: Are we on track? What should you be aware of? What do you have to decide?

```
[Product / area] update · [reporting period]
For: [readers] · Sent by: [PM name] · [date]

Overall: [On Track / At Risk / Off Track]
Bottom line: [a single sentence carrying the one thing readers must take away this period]

Delivered since last time
- [milestone completed]: [why it counts, in business terms]
- [milestone completed]: [why it counts]

Up next
- [upcoming milestone], due [timeframe]
- [upcoming milestone], due [timeframe]

Risks and blockers
- [risk] | Handling it by: [mitigation under way] | Needs a decision? [Yes/No]
  (If Yes: state the decision, the options, and what we recommend)

Numbers
- [headline metric]: now [current value], aiming for [target], [ahead / on track / behind]

Decisions we need from you
- [the question to settle] | Choices: [A / B] | We recommend: [option, with reasoning]
  Needed by: [date]
```

What makes an executive update work:

- Open with the RAG status. Bad news never goes at the bottom.
- Put business impact ahead of product detail.
- Pair every risk with a mitigation; never raise a problem without a plan.
- Treat the decisions section as the most important one, because that's what prompts action.
- If nothing needs deciding, question whether the update needs to go out at all.

### Engineering and design

*Cadence:* weekly, in step with the sprint. *Length:* whatever clarity requires.

```
Sprint [number] engineering report ([start and end dates])

Sprint goal (as an outcome): [goal statement]
Where the goal stands: [On Track / At Risk / Blocked]

Finished
- [story or feature]: [acceptance criteria satisfied]; follow-up: [anything still needed]
- [story or feature]: [acceptance criteria satisfied]

Underway
- [story or feature]: [percent done or days left], owned by [name]
  [blockers or decisions it is waiting on, if any]

Stuck
- [story or feature]: held up by [what is blocking it]; [name] owns clearing it
  Likely unblocked by: [date]

Rolling into next sprint
- [story or feature]: not finished because [reason]; re-estimated at [timeframe]

Dependencies
- [dependency]: [Resolved / On Track / At Risk], owner [name]

Looking ahead to next sprint
- [intended focus or goal]

Tech debt and upkeep
- [notable debt items dealt with or raised]
```

### Cross-functional teams (Marketing, Sales, CS)

*Cadence:* weekly, or pegged to launch milestones. *Length:* short and focused on what they need to do.

```
[Marketing / Sales / CS] briefing: product changes for [period]

Now live
- [feature or change]
  In plain words: [what it does, described from the user's side]
  Affects: [which user segment]
  Enablement required: [docs update / training / FAQ / none]

On the way
- [feature], expected [a window of time, never an exact date]
  Early access: [open / not yet]
  Enablement materials ready: [when]

Shifts since last time
- [timeline moved / scope changed / priorities changed]
  Reason: [short explanation]
  What your team should adjust: [the effect on them]

Asks of your team
- [concrete request], due [date], owner [name]

Approved wording for customers
- [language cleared for customer communications, where applicable]
```

### Customers

*Cadence:* monthly, quarterly, or around major releases. *Length:* brief and centered on value.

```
What's new in [product]: [month or quarter, year]

Just released
- [Feature name]: [one sentence on what it lets users achieve]
  Try it: [quick how-to or a link to the docs]

On the horizon
- [feature or improvement]: [the user problem it addresses, told from their side]
  Timing: [This quarter / Next quarter / First half of year]

Smaller improvements
- [speed-up / bug fix / UX polish]: [what is different and why users will care]

Tell us what you think
[how to share feedback, ask for features, or join research sessions]
```

Rules for anything a customer will read:

- Lead with value: describe what users can now *do*, not what the team *built*.
- Give time ranges only, never specific dates — "Q4," not "November 12th."
- Never present an unshipped feature as a commitment; use words like "exploring," "planned," or "coming soon."
- Never reveal internal project names, prioritization scores, or competitive context.
- Never bring up features that were cut, deprioritized, or cancelled — it only confuses people.

## Picking a cadence

- **Daily** (stand-up notes) — for the engineering team in an active sprint. Cover blockers and where help is needed, and keep it very short.
- **Weekly** — for executive, engineering, and cross-functional readers while development is active. Cover progress, risks, and decisions needed.
- **Biweekly** — for executives during steady-state stretches. Cover milestone progress and strategic alignment.
- **Monthly** — for customers and the board. Cover cumulative progress and upcoming themes.
- **Quarterly** — for the board, investors, and company all-hands. Cover strategic progress, metric trends, and the outlook for next quarter.

A scheduled day on its own is no reason to send an update. When there's nothing meaningful to report, say so in a single sentence and skip the full version — readers learn to ignore updates that are sent out of ritual.

## Ground rules

- **Never invent progress, metrics, timelines, or status.** Where data is missing, mark the field `[Awaiting data]` instead of estimating.
- **Never write customer-facing feature descriptions from nothing.** Ask the user for the feature details rather than making them up.
- **Never assign a RAG status without data.** If the status can't be determined, say "No status rating possible yet; this needs [name the missing data]."
- **Label the origin of every element** as `(source: user or project data)`, `(source: update methodology)`, or `(AI-drafted: check before it goes out)`.

Let the user know they can ask for DOCX output if they want a formatted Word document ready to distribute.
