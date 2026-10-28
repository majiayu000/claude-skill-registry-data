---
name: gg-plan-intro
description: Lists the planning skills of the project management repo and says which one comes next. Use when the user says "/gg-plan-intro", asks how to plan the project, or asks what comes before the tickets.
---

# The planning skills

Print the list below, in this order — it is the order in which a project
is planned.

- `/gg-plan-requirements` — engineers the goals and requirements together
  with the user, one question at a time
- `/gg-plan-schedule` — cuts the requirements into tickets, estimates them
  and draws the time plan as a Gantt chart, optionally against a target
  date
- `/gg-plan-jira-export` — exports the next tickets of one person, one
  sprint's worth, as a CSV file for Jira
- `/gg-plan-report` — collects what each person needs to hear into their
  quarterly report, as points to tick off

The tickets come after the requirements; the `gg` workflow creates them
(`/gg-ticket`, if the repo has it).

## Say which skill comes next

Read `doc/goals`, `doc/requirements`, `doc/schedule.md`, `doc/team` and
`doc/reports` and name the next step:

- No active goal or no accepted requirement → `/gg-plan-requirements`
- Requirements, but the work at hand is not covered by them →
  `/gg-plan-requirements`
- Requirements, no schedule, and the user wants a time plan or names a
  target date → `/gg-plan-schedule`
- Requirements accepted → plan the tickets
- Planned tickets without a Jira key, and the team works in Jira →
  `/gg-plan-jira-export`
- Changes since the newest report point, or no report for the current
  quarter yet → `/gg-plan-report`

## Important

- Only list the skills, never run one of them unasked.
