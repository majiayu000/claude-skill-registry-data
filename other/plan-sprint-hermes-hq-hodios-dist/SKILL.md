---
name: plan-sprint
description: Builds a sprint plan from a backlog and real capacity, with a sprint goal, committed and stretch items, dependencies, risks and what it deliberately leaves out. Use before sprint planning.
license: CC0-1.0
metadata:
  version: 1.1.1
  kind: prompt
  category: planning
  source: https://hermes-ide.com/prompts/plan-sprint
  catalog: 2026.1014.1
---

# Plan a sprint

## Inputs

- [BACKLOG] (required): The prioritised backlog items under consideration, with estimates, owners or skills needed, and dependencies if known.
- [CAPACITY] (required): Who is available and for how many days, known absences, on-call or support rotations, meetings, and recent velocity or throughput if you track it.
- [SPRINT_LENGTH] (optional; default: 2 weeks): Length of the sprint.
- [CARRY_OVER] (optional): Unfinished work from the last sprint and how much of it remains.

Take each value from the invocation or the user’s message. If a required value is missing, ask for it once.

<context>
Sprints fail in planning more often than in execution: the team commits to the sum of everyone's nominal hours, forgets on-call and holidays, ignores carry-over, picks unrelated items with no goal tying them together, and discovers on day six that an item depended on another team. A good plan starts from realistic capacity, picks a single goal worth achieving, commits to less than the maximum, and says out loud what it is not doing.
</context>

<task>
Draft a [SPRINT_LENGTH] sprint plan from the backlog and capacity below, ready for the team to challenge in planning.

<backlog>
[BACKLOG]
</backlog>

<capacity>
[CAPACITY]
</capacity>

Only if [CARRY_OVER] was provided: 
<carry_over>
[CARRY_OVER]
</carry_over>

1. Compute realistic capacity, in the backlog's own unit, and show the arithmetic:
   - **Available person-days:** people × working days, minus absences, on-call or support time and fixed ceremonies. Compare it with a normal sprint for this team.
   - **With history in points or item counts:** capacity = the average of the last three sprints × (available person-days ÷ normal person-days). Do not apply a focus factor on top: history already includes meetings, interruptions and reviews. If the history is volatile, plan to the lower end of the range and say so.
   - **Without history:** apply a focus factor of 60 to 70% to available person-days, say it is an assumption, and only then compare with the items' estimates. If items are sized in T-shirt sizes or not at all, say they cannot be summed reliably, state the day range you assume per size (or ask for it), and treat the result as a rough fit, not a total.
2. Account for carry-over first: re-estimate what remains, and decide with a reason whether each item continues, is split or goes back to the backlog.
3. Propose one sprint goal: a single outcome, written as what users or the business will have by the end, that most committed items serve. If the backlog has no coherent goal, say so and propose the best candidate.
4. Select committed items in priority order up to realistic capacity, leaving roughly 10 to 20% unplanned only if the history is volatile or the team has unplanned support work not reflected in it. Never commit beyond capacity because someone asked; put the excess in stretch or Not this sprint and say what the trade-off is. Prefer finishing over starting, and items that serve the goal. Flag items that are not ready (no acceptance criteria, unresolved questions, missing designs, estimates too large for one sprint) and either propose a split or move them out.
5. Pick stretch items that fill the remaining capacity, labelled clearly as not committed.
6. Check the plan against people, not only points: no one is overloaded, specialist skills are not a bottleneck, and work that needs reviews, QA or another team has time for it.
7. List dependencies (other teams, vendors, environments, decisions) with what is needed and by which day, and the main risks with a mitigation each.
8. List what is deliberately left out and why, so stakeholders hear it before the sprint, not after.
</task>

<constraints>
- Use the backlog's own estimates and units. Do not re-estimate items unless asked, but flag estimates that look inconsistent.
- Do not change the backlog's priority order silently. If the plan skips a higher-priority item, give the reason.
- Do not invent team members, dates, velocities or dependencies. Mark assumptions.
- The plan is a proposal for the team to decide on, not a commitment made for them.
- Separate what you verified from what you inferred. Mark inferences as such.
- When you do not know, say "I don't know" once and state what would settle it.
</constraints>

<output_format>
## Sprint goal
One sentence, then one line on why this goal.
## Capacity
Table: person or role, days available, deductions, available days. Then the conversion to the backlog's unit (history scaling or focus factor, never both) and the resulting capacity.
## Committed
Table: item, estimate, owner or skill, serves goal (yes or no), ready (yes or what is missing). Total against capacity, in the same unit.
## Stretch
Same table, labelled as not committed.
## Not this sprint
Bullets: item and reason.
## Dependencies and risks
Table: dependency or risk, needed by, owner, mitigation.
## Questions for planning
Numbered questions the team must answer in the planning meeting.
</output_format>
