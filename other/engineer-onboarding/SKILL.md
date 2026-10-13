---
name: engineer-onboarding
description: Design and execute an effective engineering onboarding program that gets new hires contributing independently within 30–90 days. Covers pre-day-1 setup, buddy/mentor assignment, first-week milestones, codebase ramp-up strategy, 30/60/90 day plan structure, onboarding health metrics, and differences for remote, new grad, and experienced hire onboarding.
triggers:
  - "onboard a new engineer"
  - "new hire"
  - "onboarding plan"
  - "new team member"
  - "first week"
  - "30 60 90"
  - "someone starting next week"
  - "ramp up a new engineer"
  - "new grad onboarding"
audience:
  - manager
---

# Engineer Onboarding

The first 90 days set the trajectory. An engineer who feels lost, unwelcome, or unproductive in month one often never fully recovers their confidence or engagement. Onboarding is not HR's job — it's the manager's most important lever for getting a new hire to full contribution.

**The goal**: the new engineer should ship something real in their first week, understand the system well enough to contribute independently by day 30, and be operating without a support scaffold by day 90.

> For 1:1 check-ins during onboarding, use the `one-on-one-coaching` skill.  
> For setting the engineer's quarterly goals after onboarding, use the `okr-engineering-alignment` skill.

---

## Why Onboarding Fails

| Failure mode | What it looks like | Root cause |
|---|---|---|
| **Sink or swim** | "Here's the Jira board, figure it out" | No structured plan; manager too busy |
| **Death by documentation** | Engineer reads wikis for 2 weeks | No hands-on work; learning without doing |
| **Isolation** | No buddy, no intro, no social integration | Process focused on tools, not people |
| **No early wins** | First ticket is 6 weeks of work | Wrong first assignment; no confidence boost |
| **Unclear expectations** | Engineer doesn't know if they're doing well | No explicit milestones or check-ins |
| **Context overload** | Every team member dumps context on day 1 | No pacing; no learning structure |

---

## Pre-Day-1 Checklist

Complete these **before** the engineer's first day. Scrambling on day 1 signals disorganisation.

**Access and tooling**
- [ ] Laptop ordered and configured; arrives before day 1
- [ ] GitHub/GitLab access provisioned
- [ ] Slack/Teams added to relevant channels (team, on-call, engineering-wide)
- [ ] Jira / Linear / project tracker access
- [ ] AWS / GCP / Azure access with least-privilege scoping
- [ ] VPN / SSO set up and tested
- [ ] IDE / dotfiles / dev environment setup guide linked
- [ ] Password manager and security keys configured
- [ ] Local dev environment runbook verified to work (test it yourself)

**People and calendar**
- [ ] Buddy assigned (see Buddy Program below) and briefed
- [ ] First 1:1 scheduled for day 1 or 2
- [ ] Intro to team meeting scheduled for week 1
- [ ] Calendar blocked for onboarding ramp-up (protect their time)
- [ ] Engineering-wide team introduced via Slack/email before they arrive

**Context**
- [ ] Welcome message sent the week before (what to expect, where to go, who to find)
- [ ] Onboarding doc / reading list prepared and linked
- [ ] First ticket identified: small, well-scoped, real, end-to-end

---

## The Buddy Program

A buddy is a peer engineer (not the manager) whose job is to be the new hire's first point of contact for questions they don't want to ask the manager.

**Buddy selection criteria:**
- 6–18 months tenure on the team — experienced enough to know the ropes, recent enough to remember the pain
- Patient communicator; proactively inclusive
- Not overloaded with their own work this quarter

**Buddy responsibilities (first 30 days):**
- Daily check-in (async or 5-minute sync) for the first week
- First point of contact for "how do we do X here" questions
- Walk through the codebase together in week 1
- Accompany to at least one cross-team meeting to provide context
- Flag to manager if the new hire seems stuck or disengaged

**What the buddy is not**: a mentor for career growth (that's the manager's job) or a second manager.

---

## First Week: Structure and Milestones

The first week is the highest-anxiety period. Structure it so the engineer ends Friday with a win.

### First Week Schedule Template

```
Monday
  AM: Welcome from manager (1:1); orient to the physical/virtual workspace
      Buddy intro and desk / Slack setup walkthrough
  PM: Dev environment setup with buddy; run the app locally

Tuesday
  AM: Architecture walkthrough — don't explain everything, just the 3 main services
      and the path a request takes through the system
  PM: Pick up first ticket (pre-selected); buddy available for questions

Wednesday
  AM: Team standup; brief team intro from engineer
  PM: Continue first ticket; unblock any environment issues

Thursday
  AM: 30-min "how we work" session: PR process, deploy process, on-call expectations
  PM: Continue first ticket; aim for first PR up for review today

Friday
  AM: First PR merged (or clearly on track for early next week)
  PM: Week 1 retrospective with manager (10 min): what went well, what was confusing?
      Meet the wider engineering team (optional team lunch or virtual coffee)
```

**The milestone that matters most**: a real PR merged in the first 5–7 days. It doesn't need to be large — a bug fix, a small feature, a documentation improvement, a test. The point is end-to-end familiarity with the delivery process and a concrete contribution.

---

## Codebase Ramp-Up Strategy

Don't try to explain everything. Teach them to navigate.

### Week 1: Request path
Walk through the path a single request takes through the system:
- Entry point (API gateway, load balancer)
- Core service(s) handling the request
- Database layer
- Key dependencies (queues, third-party services)
- Response path back out

This gives a map before filling in the details.

### Week 2–3: Working area deep-dive
Focus on the area where they'll be working for the first 60 days.
- Code tour of the relevant service(s)
- How to run tests locally
- How to observe the service in production (logs, metrics, traces)
- Known quirks, tech debt, gotchas

### Week 4–8: Breadth exposure
Gradually introduce adjacent systems as they naturally come up in their work. Don't front-load context — let work pull learning.

### Architecture Decision Records (ADRs)
Point the new hire to your ADRs (if they exist). Reading the last 10–15 ADRs is one of the fastest ways to understand *why* the system is the way it is.

### Recommended learning order
1. Run the app locally
2. Write a test; run the test suite
3. Make a change; deploy to staging
4. Read the last 10 merged PRs in the codebase
5. Pair with a team member on an existing task
6. Pick up an independent ticket

---

## 30/60/90 Day Plan

### Day 30: Learning and Contributing

**Objectives**:
- Comfortable in the development environment
- Has shipped at least 2–3 real contributions (PRs merged)
- Understands the team's delivery process (PR → review → deploy → monitor)
- Has relationships with direct teammates
- Knows where to find help

**Milestones**:
- [ ] Dev environment set up independently
- [ ] First PR merged
- [ ] Can pick up and complete a well-scoped story independently
- [ ] Attended team ceremonies (standup, retro, sprint planning)
- [ ] 30-day check-in completed (see check-in template in `one-on-one-coaching` skill)

**Warning signs at day 30**:
- Has not yet merged a PR → investigate blocker immediately
- Hasn't asked any questions → may be struggling silently
- Buddy relationship isn't working → reassign or add support

---

### Day 60: Independent Contribution

**Objectives**:
- Contributing to the team's sprint velocity without significant support
- Can navigate the codebase across the relevant service area
- Understands team norms around code quality, design, and process
- Beginning to contribute to team discussions (not just listening)

**Milestones**:
- [ ] Taking on stories without needing them pre-broken-down
- [ ] Has raised at least one question/concern in a team forum (retro, design review, etc.)
- [ ] Understands the production monitoring setup; has investigated at least one anomaly
- [ ] No longer needs daily buddy check-ins

**Growth edge to introduce**:
Ask them to improve one part of the onboarding documentation based on their own experience. This is a contribution, a forcing function for reflection, and a gift to the next new hire.

---

### Day 90: Full Team Member

**Objectives**:
- Operating without a support scaffold — they are a full team member
- Has formed a perspective on the codebase: what works, what doesn't
- Beginning to think about the team's work at a slightly higher level
- Career development conversation completed and growth areas identified

**Milestones**:
- [ ] Can independently own a feature from refinement through delivery
- [ ] Has contributed to sprint planning or backlog refinement
- [ ] 90-day retrospective completed: what went well in onboarding, what could be better?
- [ ] First career development conversation completed

---

## Experienced Hire vs. New Graduate Onboarding

| Dimension | Experienced hire | New graduate |
|---|---|---|
| **Technical ramp** | Faster on tools; needs context on *your* system specifically | Needs fundamentals reinforced; may not have production experience |
| **Process ramp** | May have strong opinions from previous job; help them understand *why* you do things your way | Everything is new; be explicit about what's expected |
| **First ticket** | Can take on a larger, slightly ambiguous ticket sooner | Needs a well-scoped, low-ambiguity ticket; pair on it |
| **Buddy role** | Culture and relationship integration | Technical guidance + culture integration |
| **Risk to watch** | Imposing previous patterns before understanding context | Silent struggle; hesitant to ask "basic" questions |
| **Feedback cadence** | Weekly 1:1 check-in is usually enough | More frequent check-ins (2x/week first month) |
| **Time to independence** | Day 30–45 typical | Day 60–75 typical; longer for complex systems |

---

## Remote Onboarding Differences

Remote onboarding requires deliberate over-engineering of social connection — the casual corridor conversations that happen automatically in-person don't happen automatically remotely.

**Additional steps for remote:**
- [ ] Send a physical welcome package before day 1 (notebook, swag, handwritten note)
- [ ] Schedule virtual coffee with each team member in week 1 (15–20 min each)
- [ ] Over-communicate: daily async check-in for first 2 weeks
- [ ] Pair programming sessions at least 2x per week in first month
- [ ] Ensure camera-on for 1:1s and team meetings in first month (discuss this explicitly)
- [ ] Dedicated Slack channel for onboarding questions: low-stakes place to ask anything
- [ ] Virtual "first week retrospective" on Friday of week 1

**Remote-specific risk**: the new hire can become invisible. If they're not visible in stand-ups, Slack, and PRs, other team members won't know them and won't naturally include them.

---

## Onboarding Health Metrics

Measure these to understand whether your onboarding process is working:

| Metric | Target | How to measure |
|---|---|---|
| Time to first merged PR | ≤ 7 days | Git log + start date |
| Time to first independent story | ≤ 30 days | Jira/Linear |
| 30-day onboarding NPS | ≥ 8/10 | Survey (see below) |
| 90-day retention | > 95% | HR data |
| New hire velocity at 90 days vs. team average | ≥ 70% | Sprint metrics |

---

## Onboarding Survey (Send at Day 30 and Day 90)

```
1. How clear were your expectations in the first week? (1–10)
2. How well-supported did you feel technically? (1–10)
3. How well-integrated do you feel with the team socially? (1–10)
4. Was the dev environment setup smooth? What was hardest?
5. What was the most confusing thing about how the team works?
6. What would have made your first 30 days better?
7. Is there anything you needed that you didn't get?
8. Would you recommend this team to a friend as a place to work? (1–10)
```

---

## Output Format

When applying this skill, the agent should:
- Ask: new grad or experienced hire? In-person or remote? Start date?
- Produce a populated 30/60/90 day plan with specific milestones and dates
- Generate the pre-day-1 checklist customized to the team context
- Suggest an appropriate first ticket type (not a specific ticket — characterize what makes a good first ticket for this context)
- Flag any onboarding risks based on the context (remote, very junior, very senior)

---

## References
- Camille Fournier: *The Manager's Path* — Onboarding and the first 90 days
- LeadDev: [How to onboard engineers effectively](https://leaddev.com/team)
- Nicole Forsgren, Jez Humble, Gene Kim: *Accelerate* (DORA) — Developer productivity and time-to-contribution as a metric
- Michael Watkins: *The First 90 Days* — General onboarding framework (adapted for engineering)
- LeadDev: [Remote onboarding: how to set up new hires for success](https://leaddev.com/team)
