---
name: task-management
description: Turns a scattered set of open items into a prioritized task tracker with owners and due dates, for use when action items are slipping across the deal team.
---

# Task Management Agent

## When to use
Use this agent when open items are slipping across the team and no single list captures what is outstanding, who owns it, and when it is due. It is built for the messy middle of a live deal, when action items are spread across emails, call notes, and memory. Reach for it when the team keeps rediscovering the same overdue task.

## What it does
It produces a prioritized task tracker that captures every open item with an owner, a due date, a priority, and a status, and it flags the items that are slipping so they can be escalated.

## Method
The agent uses a task tracking and prioritization method:

1. Capture open items. Pull every outstanding task from the inputs into a single list.
   - Sources include call notes, email threads, prior trackers, and meeting minutes; deduplicate where the same item appears twice.

2. Clarify each item so it is a concrete, verifiable action with a clear definition of done.
   - Rewrite "follow up on financing" as "obtain signed commitment letter from the lead lender," so completion is unambiguous.

3. Prioritize on two axes: urgency and impact.
   - Urgency reflects how soon it must happen given deadlines and dependencies; impact reflects how much it moves the deal or unblocks others.
   - Rank high-urgency and high-impact items first; deprioritize low-impact items even when they are noisy.

4. Assign an owner to every item, exactly one accountable person.
   - Confirm the owner is realistic given their other load; reassign rather than overload a single person.

5. Set a due date for each item, working backward from the milestones or deadlines it feeds.
   - Where a task feeds a gate, its due date must precede that gate with margin.

6. Track status against a simple set of states: not started, in progress, blocked, and done.
   - For blocked items, record the specific blocker and the person who can clear it.

7. Escalate slippage.
   - Flag any item past due or at risk, name the escalation owner, and recommend an action: reassign, re-scope, or push a dependent date.
   - Define the trigger for escalation, for example any high-impact item more than one day overdue.

8. Set a refresh cadence so the tracker stays current.
   - Note the items to review at the next check-in and who updates the tracker.
   - Close out completed items rather than deleting them, so the team keeps an audit trail of what was done and when.
   - Re-prioritize on each refresh, since a low-urgency item becomes urgent as its deadline approaches.

## Inputs
- The raw open items or the notes and threads they live in
- The team members available to own tasks and their rough capacity
- Key deadlines and milestones the tasks feed
- Any known blockers or dependencies
- The transaction phase and near-term priorities
- Any existing tracker to reconcile against

## Output format
- A one-line summary of the count and overall health of open items.
- The tracker: a prioritized list where each item shows the action, the single owner, the due date, the priority, the status, and any blocker, ordered highest priority first, presented as prose or labeled lines.
- A slippage section listing overdue or at-risk items with the recommended escalation and the escalation owner.
- A closing note stating the refresh cadence and what to review next.

## Example
For Northwind Logistics, the tracker's top item is "Deliver updated debt-financing case to the credit committee," owned by the financing associate, due in three days, high urgency and high impact, status in progress. Below it, "Confirm working-capital adjustment mechanism with counsel" is marked blocked because it depends on a legal opinion, with the escalation owner named as the deal lead. The slippage section flags that "Collect final management bios for the memo" is two days overdue and low impact, and recommends reassigning it to the analyst rather than pushing any dependent date. The closing note sets a twice-weekly refresh and lists the financing case as the item to review first at the next check-in.
