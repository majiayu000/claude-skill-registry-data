---
name: proj-raid-log
version: 1.0.0
description: Maintain a RAID log tracking risks, assumptions, issues, and dependencies with owners and review cadence.
author: matrixx0070
tags: [project-management, raid, risk, issues, tracking]
---

## When to use

Use this to run the living register of everything that could or already does threaten delivery: Risks (might happen), Assumptions (believed true, unverified), Issues (happening now), Dependencies (need from others). Reach for it right after the charter and keep it open for the project's life — it feeds every status update.

**Not for:** deciding what product to build or evaluating feature bets (that is product-management). Not for a company-wide risk framework or compliance register that outlives the project (that is operations). This is a project-scoped delivery log you actively work each week.

## Method

1. Create four sections: Risks, Assumptions, Issues, Dependencies. Classify each entry — the class drives the response. Decision point: is it happening now (Issue) or might it happen (Risk)? An assumption that proves false becomes an Issue.
2. For each Risk: state probability × impact, a mitigation (reduce likelihood), and a contingency (what you do if it fires). Decision point: high×high risks get an owner and an action this week; low×low get logged and reviewed only.
3. For each Assumption: name who can confirm it and by when. Decision point: assumptions on the critical path must be validated early, not left standing.
4. For each Issue: assign an owner, severity, and a target resolution date; track it until closed.
5. For each Dependency: name the providing team, what you need, the needed-by date, and status (link to `proj-dependency-map`).
6. Give every entry a unique id, owner, and next-review date. Never delete — mark Closed with an outcome so history survives.
7. Review on a fixed cadence (weekly); pull the top items into `proj-status-update`.

## Example

R3: "Vendor API rate limit may block launch." P=med, I=high. Mitigation: request quota bump now. Contingency: cache + queue. Owner: you. A2: "We assume the data migration fits in the 4h window" — confirm with DBA by Fri. I1: "Staging DB corrupted" sev-high, owner Sam, due today. D2: "Need auth service from Platform by day 10."

## Pitfalls

- **Risk/issue confusion.** Logging a live problem as a risk delays action. If it is happening, it is an Issue — assign an owner now.
- **Mitigation with no contingency.** Reducing likelihood is not a plan for when it fires anyway. Write both.
- **Orphan entries.** Rows with no owner or review date rot. Every entry needs both.
- **Delete-on-close.** Erasing closed items loses the audit trail. Mark Closed with the outcome instead.

## Output format

```
# RAID: <project>  reviewed <date>
RISKS:    | id | risk | P | I | mitigation | contingency | owner | review |
ASSUMPTIONS: | id | assumption | confirm-by-whom | by-when | status |
ISSUES:   | id | issue | severity | owner | target | status |
DEPENDENCIES: | id | need | from-team | needed-by | status |
(status ∈ open|in-progress|closed; closed rows keep outcome)
```
