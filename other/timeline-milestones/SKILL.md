---
name: timeline-milestones
description: Builds a credible deal timeline with milestones and a computed critical path, for use when a transaction needs a defensible schedule to the close.
---

# Timeline & Milestones Agent

## When to use
Use this agent when a deal needs a credible schedule that runs all the way to the close. It is built for the point where the team must commit to a timeline in front of a client, a board, or a counterparty and needs the dates to hold up. Reach for it when someone asks "when do we sign, and what has to happen first."

## What it does
It produces a deal timeline with clearly defined milestones and an explicit critical path, showing which activities drive the close date and where the schedule has slack.

## Method
The agent uses a critical-path deal timeline method:

1. List the activities. Enumerate every activity from kickoff to close.
   - Cover preparation, marketing or outreach, diligence, financing, documentation, regulatory approvals, and signing and closing mechanics.
   - A pitfall is omitting third-party consents and closing conditions, which often surface late and delay the close.

2. Estimate durations for each activity in working days, using realistic ranges rather than best-case guesses.
   - Note the driver of each estimate, for example counterparty responsiveness or regulator review windows.

3. Sequence the activities with dependencies.
   - Mark finish-to-start links, for example confirmatory diligence starts only after exclusivity, and mark what can run in parallel.

4. Compute the critical path.
   - Identify the longest chain of dependent activities that determines the earliest close, and mark those activities as zero-float.
   - Any slip on a zero-float activity moves the close date one-for-one.

5. Calculate float for off-path activities.
   - Float is the time a non-critical task can slip before it starts driving the close date; low-float tasks deserve extra monitoring.

6. Set milestones and gates.
   - Define decision gates such as go or no-go after diligence, financing commitment, board approval, sign, and close, each with clear entry criteria.

7. Add buffer to the critical path and to high-risk activities.
   - Regulatory approvals and third-party consents are the usual buffer candidates; state the buffer explicitly rather than hiding it in estimates.

8. Highlight the top schedule risks and the activities most likely to push the close date.
   - Give a recommended mitigation for each, such as starting a consent request earlier or running an approval in parallel.

## Inputs
- The deal type and structure
- The target close or announcement date and any hard deadlines
- Known activities, approvals, and closing conditions
- Third-party or regulatory requirements and their expected review windows
- Resource or advisor constraints that affect durations
- Any prior timeline or key dates already committed
- The gates or approvals the client or board requires

## Output format
- A brief framing note stating the earliest credible close and the main schedule driver.
- A sequenced timeline as an ordered list of activities, each with start and finish in working-day offsets from kickoff, duration, predecessors, and float.
- A clear flag on every critical-path (zero-float) activity.
- A milestones section listing each gate with its target date and entry criteria.
- A risks section naming the activities most likely to slip, the buffer applied, and the assumptions underpinning the schedule, described in prose rather than a rendered table.

## Example
For Meridian Foods, a fictional sell-side process, the critical path runs kickoff, then preparation of marketing materials at fifteen days, then outreach and first-round bids at twenty-five days, then management presentations and confirmatory diligence at thirty days, then documentation and signing at twenty days. Regulatory clearance sits off the critical path with ten days of float because it runs in parallel with documentation. The milestone gate "second-round go or no-go" has entry criteria of at least three qualified bids and a completed data room. A five-day buffer is added ahead of signing to absorb documentation slippage, the most common driver of a missed close date, and the risks section flags that a required antitrust consent could consume its float if the regulator opens a second request.
