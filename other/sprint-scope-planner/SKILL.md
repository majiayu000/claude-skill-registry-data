---
name: sprint-scope-planner
description: "Plans fixed-length sprints: calculates raw, adjusted, and effective capacity with a team-derived focus factor, converts it to points via historical velocity, writes an outcome-based sprint goal, maps and de-risks dependencies, splits work into commitment and ordered stretch, and produces a complete sprint plan. Also guides mid-sprint rebalancing. Use when a team asks to plan or scope a sprint, work out capacity or velocity, set a sprint goal, decide what to commit to, or rebalance a sprint that is slipping."
---

# Sprint Scope Planner

You help teams plan fixed-length iterations. That means sizing the work to the capacity the team really has, framing the sprint around an outcome, getting dependencies under control, and drawing a clear line between what the team commits to and what it will pull only if time allows.

## Running the planning session

Structure the work in two parts: preparation beforehand, and the planning meeting itself.

### Preparation

1. **Groom the backlog.** The top candidates need clear descriptions, acceptance criteria, and estimates. Anything ungroomed stays out of the sprint.
2. **Work out capacity.** Run all four capacity steps below with this sprint's data.
3. **Find the dependencies.** For every candidate story, surface what it needs from other teams or from outside parties.
4. **Look back at the last sprint.** What carried over, and what did the team learn? Carry-over items deserve priority consideration, but they don't get in automatically — reassess their priority.

### In the meeting

1. **Present the sprint goal** drafted using *Framing the sprint goal*.
2. **Go through the candidate stories.** For each, confirm its scope, estimate, dependencies, and acceptance criteria.
3. **Fill the commitment.** Keep adding stories to the commitment until effective capacity is used up.
4. **Order for dependencies.** Sequence the committed stories so that nothing starts before its prerequisites.
5. **Add stretch items** in priority order.
6. **Confirm with the team.** Each person confirms they know what they are working on and think the commitment is achievable.

Then write it all down using the sprint plan format further below.

## Working out capacity

### Step 1 — Raw capacity

This is the theoretical ceiling before any deductions:

```
RAW CAPACITY = Team members × Sprint length (days) × Hours per day
```

Base the hours on the team's normal working day, and do not assume a day holds 8 productive engineering hours. After meetings, context switching, and overhead, most teams get 5–6 productive hours a day.

### Step 2 — Adjust for availability

Take out the time you already know is unavailable:

- **PTO / holidays** — subtract whole days for each person affected.
- **On-call rotation** — cut that person's capacity by 30–50%, depending on the historical interrupt rate.
- **Recurring meetings** — subtract each person's total meeting hours over the sprint.
- **Onboarding / ramp-up** — anyone new to the team counts at 25–50% capacity during their first 2–4 sprints.
- **Support rotation** — deduct however much support work the team has historically absorbed on average.

```
ADJUSTED CAPACITY = RAW CAPACITY − (PTO hours + on-call reduction + meetings + support)
```

### Step 3 — Focus factor

The focus factor absorbs unplanned work, bug fixes, code review, and any other overhead the adjustments above didn't catch. Calculate it from this team's past sprints:

```
FOCUS FACTOR = (Actual story points completed) / (Adjusted capacity in hours) — averaged over last 3-5 sprints
```

With no history to go on, begin at 0.7 (70%) and recalibrate after 2–3 sprints. Never hand out a one-size-fits-all focus factor: it depends on how mature the team is, how healthy the codebase is, and how often the team gets interrupted.

```
EFFECTIVE CAPACITY = ADJUSTED CAPACITY × FOCUS FACTOR
```

Effective capacity is the number you plan against.

### Step 4 — Convert to the team's unit

Express effective capacity in whatever unit the team estimates in. For story points, translate it through the velocity the team has actually delivered:

```
SPRINT CAPACITY (points) = Average velocity over last 3-5 sprints, adjusted for capacity differences
```

So if this sprint has 80% of the usual capacity, plan for about 80% of average velocity. Velocity describes what happened; it is not a target, so never inflate it or treat it as something to "stretch."

## Framing the sprint goal

A sprint goal describes an outcome, not a pile of tickets. It answers the question: "If this sprint goes well, what will be true afterward that isn't true today?"

### How to set it

1. **Check product priorities.** Find the highest-impact work in the backlog, using the roadmap and the current OKRs as reference.
2. **Draft one or two candidate goals,** each phrased as an outcome rather than a task list.
3. **Check the scope.** Can the team realistically hit this goal within effective capacity? If not, shrink the goal — never the quality.
4. **Get the team behind it.** The team has to understand the goal and commit to it. A goal handed down without buy-in gets compliance, not commitment.

### How to tell if it's a good goal

- **Outcome-oriented** — *good:* "Users can check out without a page refresh." *Bad:* "Close PAY-301, PAY-302 and PAY-303."
- **Singular focus** — *good:* one coherent theme or objective. *Bad:* several unrelated objectives bundled together.
- **Testable** — *good:* a demo or a metric can prove it was reached. *Bad:* no way to tell whether it was met.
- **Achievable** — *good:* fits within sprint capacity once estimated. *Bad:* only works under optimistic assumptions about capacity.
- **Stakeholder-meaningful** — *good:* people outside engineering can see the value. *Bad:* written entirely in technical jargon.

## Getting dependencies under control

Classify each dependency and apply the matching mitigation:

| Type | What it is | How to mitigate it |
|---|---|---|
| **Internal team** | A story that relies on another story in the same sprint | Sequence the stories; assign them to a pair where possible |
| **Cross-team** | Work waiting on another team's deliverable | Confirm their delivery date before committing; build in buffer |
| **External** | A third-party API, a vendor deliverable, a customer approval | Don't commit the dependent work until the timeline is confirmed |
| **Technical** | Shared infrastructure, a database migration, the deployment pipeline | Identify it and schedule it early in the sprint |

Then take every dependency through five steps:

1. **Classify** it using the types above.
2. **Confirm its status** — resolved, in progress, or not started?
3. **Weigh the risk** — what happens if it arrives late, and is there other work the team could pull instead?
4. **Name an owner** — one person on the team tracks each external dependency.
5. **Schedule a check-in** — decide when you'll confirm it's on track, and make it earlier than the sprint's final day.

**Hard rule:** a story with an unresolved external dependency and no confirmed delivery date belongs in stretch. It never goes into the commitment.

## Commitment versus stretch

Divide the sprint backlog into two explicitly separate groups.

**Commitment** is work the team is confident of finishing inside the sprint — they put the odds of completion at 80–90% or better, given effective capacity. Every committed item must:

- fit within effective capacity;
- have its dependencies resolved, or have confirmed delivery dates for them;
- have clear acceptance criteria — if the team can't say what "done" looks like, the item isn't ready to commit.

**Stretch** is work the team pulls in only if committed items finish early. Every stretch item must be:

- fully groomed and ready to start, with no blocking questions;
- free of unresolved dependencies;
- independent, so pulling it in doesn't destabilize committed work;
- ranked by priority, so the team knows which to pull first.

**How to split capacity:** commit 80–90% of effective capacity and fill the remaining 10–20% with ranked stretch items. Tune the exact ratio to the team's track record — teams that consistently under-commit can tighten it, and teams that over-commit should loosen it.

## The sprint plan

Fill in this layout. Where the user hasn't supplied a value, leave the bracket empty rather than inventing one.

```
Sprint [name or number]  ·  runs [first day] to [last day]
Sprint goal: [the outcome that will be true when the sprint ends]

Capacity
| Input              | Value                                   |
|--------------------|-----------------------------------------|
| Headcount          | [number of people]                      |
| Raw capacity       | [hours or points]                       |
| Deductions         | [PTO, on-call, meetings, support, ...]  |
| Effective capacity | [figure you plan against]               |
| Velocity baseline  | [mean of the 3-5 most recent sprints]   |

Committed work — [sum in points/hours], i.e. [X]% of effective capacity
| # | Item          | Size       | Assignee | Depends on     | State |
|---|---------------|------------|----------|----------------|-------|
| 1 | [story title] | [estimate] | [person] | [dependencies] | Ready |

Stretch work — [sum in points/hours]
| # | Item          | Size       | Pull order          | Depends on     |
|---|---------------|------------|---------------------|----------------|
| 1 | [story title] | [estimate] | 1 (first to pull)   | [dependencies] |

Dependency tracker
| What we're waiting on | Kind | Tracked by | Resolution expected | Check on |
|-----------------------|------|------------|---------------------|----------|

Threats to the goal
  [biggest risks to hitting the sprint goal, drawn from the dependency and capacity review]

Carried in from last sprint
  [each item, why it slipped, and its reassessed priority]
```

## When a sprint starts slipping

If the sprint gets into trouble — items become blocked, scope shifts, people are unexpectedly out — triage in this order:

1. **Recalculate capacity** for the days left in the sprint.
2. **Recheck the commitment** — sort the committed items into those in trouble and those still on schedule.
3. **Guard the goal** — when a subset of the committed work still achieves it, move the items that don't serve the goal to stretch.
4. **Escalate blockers** — an unresolved dependency that threatens the sprint goal gets escalated right away rather than waiting for the next stand-up.
5. **Keep stakeholders informed** — whenever the commitment changes, send them an update using `product-update-communicator`.

## Ground rules

- **Never invent velocity data, estimates, or capacity numbers.** Every team metric must come from the user, their project tracker, or their uploaded documents or connected knowledge sources.
- **Never prescribe a universal focus factor, velocity target, or capacity ratio.** Teach the calculation and let the team derive its own numbers.
- **Never fill a sprint plan with made-up stories or estimates.** If no data has been provided, produce blank templates.
- **Tag where every element comes from**, using one of three labels:
  - `[Team or tracker data]` — figures and items the user or their tracker supplied;
  - `[Planning method]` — content taken from the sprint-planning approach described here;
  - `[AI proposal — team to confirm]` — anything you suggested that the team still has to validate.
