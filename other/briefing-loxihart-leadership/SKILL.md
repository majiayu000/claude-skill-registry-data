---
name: briefing-loxihart-leadership
version: "1.0.1"
description: >
  Prepares and structures leadership communications for Kyle Rosebrook's AI SME
  role at Loxihart — monthly progress updates, initiative proposals, adoption
  milestone announcements, and domain unlock requests. Tailored to three
  named stakeholders: [PERSON] (direct manager), [PERSON], and [PERSON]
  Miles. Activates when preparing a status update for [PERSON], drafting a
  proposal for leadership, presenting AI adoption survey results, announcing an
  AI win, requesting a domain unlock, writing an initiative brief, summarizing
  AI program progress, communicating a blocker, or documenting SME activity.
  Also triggers on: [PERSON] update, leadership brief, Loxihart AI update, adoption
  report, SME progress, brief [PERSON], brief [PERSON], Loxihart AI proposal, domain
  unlock request, stakeholder communication, management update, monthly AI
  summary.
---

# Loxihart Leadership Briefing

Produces the right communication for the right Loxihart stakeholder at the right
time. Proactive, metric-backed, team-attributed. Never reactive, never
technical-for-its-own-sake, never a personal highlight reel.

---

## Evals

**Should trigger:**
1. "I need to update [PERSON] on what I've been doing with AI this month"
2. "Help me put together a proposal for [PERSON] about expanding
   Claude to the helpdesk team"
3. "How should I present the AI adoption survey results to leadership?"

**Should NOT trigger:**
1. "Write a general leadership presentation about AI trends" — generic
2. "How do I get better at public speaking?" — personal development

---

## Decision Tree

```
What are you communicating?
  ├─ Regular update on AI program activity
  │    └─ Audience: [PERSON] only → Monthly Update (Section 2)
  ├─ Proposing a new initiative or domain unlock
  │    └─ Audience: [PERSON] + [PERSON]/[PERSON] → Initiative Proposal (Section 3)
  ├─ Announcing a win or adoption milestone
  │    └─ Audience: varies → Win Announcement (Section 4)
  └─ Escalating a blocker or requesting a decision
       └─ Audience: [PERSON] first → Escalation (Section 5)
```

---

## Section 1: Framing Principles

Full stakeholder profiles in `references/stakeholder-profiles.md`.
Full framing patterns in `references/framing-patterns.md`.

**Business outcomes, not technical details.**
[PERSON], [PERSON], and [PERSON] do not need to know how the MCP server works.
They need: adoption rate, time saved, tickets resolved faster, risk reduced.

**Team wins, not personal wins.**
Every metric should read as "the team is adopting AI" not "Kyle did AI."
Your influence compounds when others take credit for wins you enabled.

**Proactive over reactive.**
Send the monthly update before [PERSON] asks. Being asked means you drifted.

**One ask per communication.**
Every proposal has exactly one ask. Not three. One.

---

## Section 2: Monthly [PERSON] Update

**Format:** Slack message or short email. Not a document.
**Length:** 150–250 words. Scannable.
**Cadence:** First week of every month. Set a recurring reminder.

```
Subject / thread: AI SME — [Month] Update

Hey [PERSON],

Quick monthly update on the AI program:

ACTIVITY THIS MONTH
- [Domains or teams engaged]
- [Training sessions, 1-on-1s, enablement work]
- [Tools or capabilities introduced]

NUMBERS (if available)
- [Adoption metric from most recent pulse check]
- [Time savings estimate if collected]

COMING UP
- [Next initiative or focus area]
- [Single ask or dependency, if any]

Anything you want me to reprioritize or flag?
— Kyle
```

Do not include: technical implementation details, tool comparison rationale,
anything that requires [PERSON]/[PERSON] approval in a [PERSON]-only update.

---

## Section 3: Initiative Proposal ([PERSON] / [PERSON])

**Format:** One-pager. Two pages maximum.
**Length:** 400–600 words.
**Routing:** Draft → [PERSON] reviews and sponsors → [PERSON] carries it up,
or Kyle presents with [PERSON] present. Never cold-pitch [PERSON] or [PERSON].

**Structure:**

```
[TITLE]: AI Enablement Initiative — [Initiative Name]

SITUATION
Current state, the gap or opportunity. No technical detail. One metric.

RECOMMENDATION
One sentence: what specifically are you proposing?

EXPECTED OUTCOMES
- [Time savings / efficiency metric]
- [Risk reduced / capability added]
- [Team or business outcome]

INVESTMENT REQUIRED
Time, licensing, training, coordination. Be specific.
If no budget ask, say so explicitly.

RISKS / DEPENDENCIES
What could go wrong. One or two sentences.

ASK
One sentence: what decision is needed?
"Approve a 30-day pilot with the helpdesk team."
"Authorize the $X/month license for the support domain."
```

---

## Section 4: Win Announcement

**Format:** Slack message to the relevant channel or thread.
**Length:** 3–5 sentences. No fanfare. The metric speaks.

```
The [team/domain] has been using [tool] for [timeframe]. Early results:
[metric]. [One sentence on what drove adoption — credit the team].
[Optional: one sentence on what's next.]
```

Do not use: "amazing," "excited," "proud of." Let the numbers carry it.

---

## Section 5: Escalation / Decision Request

**Format:** Slack DM or short email to [PERSON] first.

```
SITUATION: [One sentence — what is blocked and why]
IMPACT: [What happens if unresolved — specific]
OPTIONS: [Two max — your recommendation labeled clearly]
ASK: [What decision, from whom, by when]
```

If this runs longer than half a page, use the Initiative Proposal format.

---

## Self-Verification

- [ ] Business outcomes framed, not technical details
- [ ] Wins attributed to team, not personally to Kyle
- [ ] Exactly one ask, or none if update-only
- [ ] [PERSON] has reviewed before anything reaches [PERSON]/[PERSON]
- [ ] All metrics are verified, not extrapolated
- [ ] Length matches format spec

---

## CLAIMS
- Proactive monthly updates keep [PERSON] as an active ally; reactive updates
  position Kyle as someone who needs managing
- Team-attributed wins build organizational capital that supports future
  initiatives; personal-attributed wins generate resentment
- One ask per communication outperforms multiple asks for approval rate

## COUNTEREXAMPLE
- Metric-backed communications backfire when metrics are cherry-picked —
  a skeptical stakeholder will notice selective reporting faster than they
  would notice no metrics at all

## CONTRADICTIONS
- "No technical detail for leadership" conflicts with proposals where
  the ask itself is technical — include just enough to make the ask legible
