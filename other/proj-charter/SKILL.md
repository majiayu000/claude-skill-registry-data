---
name: proj-charter
version: 1.0.0
description: Write a project charter that pins down goal, scope, success criteria, and stakeholders before work starts.
author: matrixx0070
tags: [project-management, charter, scope, stakeholders, kickoff]
---

## When to use

Use this at project kickoff to get one authoritative page that says what this project is, why it exists, what is in and out, and who decides. Reach for it when work is about to start but nobody can state the goal in one sentence, or when stakeholders disagree on scope.

**Not for:** deciding *which* product or feature to build or its market rationale (that is product-management — the charter takes the "what" as an input). Not for documenting a repeatable process or a standard operating procedure (that is operations). The charter is a one-time, delivery-framing artifact for a specific initiative.

## Method

1. Write the goal as one sentence: the outcome that exists when the project is done, not the activity. Decision point: if you cannot fit it in one sentence, the project is two projects — split it.
2. List success criteria as 3-5 measurable checks (a number, a date, a shipped artifact). Each must be verifiable by someone other than you.
3. Define scope in two columns: In and Out. Decision point: any item nobody will explicitly place in "In" goes in "Out" — silence is not commitment.
4. Identify stakeholders and assign one role each: Sponsor (funds/unblocks), Owner (drives daily), Contributors, Informed. Decision point: exactly one Sponsor and one Owner — if there are two of either, escalate to name one before proceeding.
5. State constraints and known assumptions (budget ceiling, deadline, fixed team, dependencies).
6. Capture the top 3 risks in one line each (full tracking goes to `proj-raid-log`).
7. Get the Sponsor's explicit sign-off. Decision point: no sign-off means no charter — do not start execution.

## Example

Goal: "New customers can self-serve signup without a sales call by Q3." Success: (1) signup-to-active < 10 min, (2) zero manual steps, (3) live by Sep 30, (4) < 2% support tickets on signup. In: web signup, billing hookup. Out: mobile app, SSO. Sponsor: VP Growth. Owner: you. Sign-off captured in kickoff thread.

## Pitfalls

- **Goal as activity.** "Build a signup flow" is a task, not an outcome. State the result the business gets.
- **Unmeasurable success.** "Improve onboarding" cannot be checked off. Force a number and a date.
- **Empty Out column.** Undefined exclusions become scope creep. List what you are deliberately not doing.
- **Two sponsors, no decider.** Ambiguous authority stalls every decision. Name one accountable Sponsor.

## Output format

```
# Charter: <project>
GOAL: <one-sentence outcome>
SUCCESS CRITERIA:
- [ ] <measurable check + date/number>
SCOPE — IN: <items>   OUT: <items>
STAKEHOLDERS: Sponsor=<name> | Owner=<name> | Contributors=<> | Informed=<>
CONSTRAINTS: budget=<> deadline=<> team=<>
ASSUMPTIONS: <list>
TOP RISKS: <3 one-liners>
SIGN-OFF: <sponsor> on <date>
```
