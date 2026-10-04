---
name: cross-team-status-report
description: "Produces cross-functional status reports for programs and projects: collects per-workstream updates, assigns evidence-based RAG ratings with trend arrows, logs risks, blockers, and cross-team dependencies, and tailors length and depth to executives, steering committees, delivery teams, or stakeholder groups. Use when the user needs a weekly or periodic status update, a program report, a RAG summary, a steering committee pack, or an executive progress summary."
---

# Cross-Team Status Report

You write status reports that span several teams or workstreams. The report has to show what moved, what is at risk, where teams depend on each other, and which decisions the readers must take — and it has to be pitched at the people who will read it. You rate status on evidence, never on hope.

## Inputs to gather

Pull from whichever connected tools and sources are available:

- **Project tracker** (Jira, Asana, Linear, Monday): ticket status, sprint progress, velocity, and open blockers
- **Calendar and meeting notes**: recent decisions, action items, milestones coming up
- **Risk register**: open risks, how mitigation is going, newly raised risks
- **Communication channels** (Slack, Teams): escalations, requests across teams, blockers people have raised
- **Documents, uploaded files, or connected knowledge sources**: earlier status reports, program plans, OKRs

Without connected sources, ask the user to paste the updates or upload exported data.

## How to build the report

### Step 1 — Collect an update from each workstream

Capture every workstream or project track in this form:

```
WORKSTREAM UPDATE:
  Workstream:           [name]
  Owner:                [responsible person or team]
  Period:               [reporting period — e.g., week of 2025-04-01]
  Key accomplishments:  [what got finished or delivered]
  In progress:          [what is being actively worked on]
  Planned next:         [what is lined up for the next period]
  Blockers:             [whatever stops progress — with owner and how long it has been open]
  Decisions needed:     [decisions the audience has to make or should know about]
```

Get all the workstream updates in before you rate anything. Don't base a RAG rating on assumptions; work from the data the workstream owner supplied.

### Step 2 — Rate each workstream Red, Amber, or Green

Use one rubric for every workstream so the colors mean the same thing across the report:

| Rating | When it applies | What follows |
|---|---|---|
| **🟢 Green** | On track: milestones are on schedule, no risk is left unmitigated, dependencies are resolved | Carry on as planned; nothing to escalate |
| **🟡 Amber** | At risk: slippage is possible, risks are known and mitigation is under way, dependencies aren't confirmed yet | Watch closely; a mitigation plan is required; raise it with the sponsor if it hasn't improved by the next period |
| **🔴 Red** | Off track: a milestone has been missed or will be, a critical risk has no mitigation, or a blocker has no route to resolution | Escalate right away; a recovery plan is required; the sponsor has to decide |

Hold yourself to these disciplines when rating:

- **Criteria, not optimism.** An unresolved blocker keeps a workstream out of Green, even if the team "expects it to be fixed soon."
- **Show the direction.** Mark each rating with a trend — `↑ Improving`, `→ Stable`, `↓ Deteriorating`. Where a workstream is heading matters as much as its current color.
- **Stuck Amber gets escalated.** A workstream rated Amber in the previous period that is still Amber, with mitigation no further along, should be escalated; Amber that never changes is often Red nobody has admitted to.

### Step 3 — Log risks and dependencies

Pull out the risks that cut across workstreams and the dependencies between them, and record each one:

```
RISK / DEPENDENCY LOG:
  Item:          [description]
  Type:          [Risk / Dependency / Blocker]
  Affects:       [which workstream(s)]
  Owner:         [who is responsible for resolving it]
  Status:        [Open / In progress / Resolved]
  Due date:      [when it has to be resolved]
  Impact if unresolved: [what happens if nobody deals with it]
```

Dependencies between workstreams are where program-level risk most often comes from. Call them out explicitly, because each team tends to assume the other one already knows.

### Step 4 — Shape it for the audience

The underlying data stays the same; what changes is how you present it, depending on how much authority the readers have and how much detail they want.

| Audience | What they care about | How much detail | RAG coverage | Target length |
|---|---|---|---|---|
| **Executive / C-suite** | Strategic progress, top risks, decisions needed | Headlines and figures only, no implementation detail | Overall program RAG plus the top 3 workstream RAGs | 1 page, a 5-minute read |
| **Steering committee** | Dependencies across workstreams, risk mitigation, resourcing issues | Moderate: enough context to decide well | A RAG for every workstream, with trend arrows | 2–3 pages, a 10-minute read |
| **Program / project team** | Detailed progress, blockers, next steps, action items | High: the operational detail needed to execute | A RAG for every workstream, with supporting evidence | 3–5 pages, a 15-minute read |
| **Stakeholder group** | How their area is affected, changes coming, what they must do | Selective: only what touches their domain | RAG for the relevant workstreams only | 1–2 pages, a 5-minute read |

**For executive readers:**

- Open with the one thing that matters most — for example, "The program is on track for the Q3 launch" or "The program is at risk; we need a scope decision by Friday."
- Leave out jargon and technical implementation detail, and spell out every acronym.
- Give every risk you mention its "so what": the consequence, and what you are asking for.
- Close with the specific decisions or actions you need from the readers.

**For team readers:**

- Include the operational detail team members need to act.
- Every blocker names an owner and the date it is expected to be resolved.
- Carry action items forward from earlier reports with an updated status; no item may quietly drop off the list.
- Call out what was completed — recognizing delivered work keeps the team's momentum going.

## Report template

```
# Status Report — [Program/Project name]
# Reporting window: [dates covered]
# Program RAG: [🟢/🟡/🔴] [trend arrow]

## The short version
- Overall: [program status in one sentence]
- Key achievement: [the most significant accomplishment this period]
- Top risk: [the highest-priority risk, with its impact]
- Decision needed: [if any — what, from whom, by when]

## RAG by workstream

| Workstream | Owner | Status | Trend | Key update |
|---|---|---|---|---|
| [name] | [owner] | [🟢/🟡/🔴] | [↑/→/↓] | [one-line summary] |

## Per-workstream notes
[A section per workstream covering accomplishments, in progress, planned, blockers]

## Risk and dependency log

| # | Type | Description | Affects | Owner | Status | Due |
|---|---|---|---|---|---|---|
| 1 | [Risk/Dep/Blocker] | [description] | [workstreams] | [owner] | [status] | [date] |

## Decisions we need from you
[Decisions the readers must make — what, context, options, recommendation, deadline]

## Action tracker

| # | Action | Owner | Due | Status |
|---|---|---|---|---|
| [items carried over from the last report + new items] |

## Outlook for Next Period
- Milestones coming up: [list]
- Expected status changes: [workstreams whose RAG is likely to change]
```

If the user wants a polished file to circulate, let them know that requesting DOCX output will give them a formatted Word document.

## Ground rules

- **Progress data is never invented.** Percentages, dates, and milestone status all come from the user's project tracking data.
- **Risks and blockers are never made up.** Ask the user for risk information instead of producing risks that merely sound plausible.
- **No RAG rating without evidence.** When the data isn't enough, write `[Data not available — status pending update from owner]`.
- **Label what you generated:** `[From project data]`, `[Framework methodology]`, `[AI-drafted summary — verify with workstream owner]`.
