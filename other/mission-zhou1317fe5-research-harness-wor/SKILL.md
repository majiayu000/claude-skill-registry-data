---
name: mission
description: Route explicit Mission requests, supplied Mission specs or task CSVs, and research tasks that require new experiment records.
---

# Mission

Route mission inputs. Do not perform discussion, mapping, execution, or recovery work inside this skill.

Declare: `使用 mission skill，路由到 <子 skill>。`

## Routing

Check in this order; the first match wins.

1. **Existing CSV file or directory**
   - A repository Mission CSV must match the 28-column header in `issues/TEMPLATE.csv`; an explicitly supplied external CSV must match the active project schema or a documented compatibility schema.
   - For a directory, prefer `<dir>/<dir-name>.csv`; if absent, accept its only CSV. Ask only when several candidates remain.
   - Route to `mission-csv-execute`.
2. **Existing canonical spec**
   - Run `mission-spec/scripts/validate_spec.py <path>`.
   - `status: approved` and committed-clean routes to `mission-approved-doc`.
   - `status: draft` routes to `mission-spec`.
   - Invalid metadata hard-stops; do not infer a route from prose or path names.
3. **Existing Markdown without `mission: spec` frontmatter**
   - Treat it as reference material and route to `mission-spec` for canonicalization and approval.
4. **Explicit Mission recovery, including `mission` without arguments**
   - Route to `mission-recovery`. Continue/resume wording or context loss triggers recovery only for an already selected Mission.
5. **Natural-language request passed to `mission`**
   - Route to `mission-spec`.

Ordinary work with a clear goal and acceptance criteria does not need mission. Execute it directly with an ordinary plan when useful. Continue the task selected in the current conversation; an old Mission registry entry cannot take it over.

## Execution stickiness

Once `mission-csv-execute` owns an unfinished CSV, keep routing subsequent progress, explanation, or continue messages to that same execution. Leave only when the CSV reaches a terminal state or the user explicitly pauses, cancels, or changes the task boundary.

Persist that identity in `issues/.missions.json` through `.agents/harness/workflow/mission_state.py`. An explicit pause/cancel is a lifecycle transition with its user source and reason; it does not mark unfinished CSV rows complete or terminate a remote process. A task switch registers the new task with `--replaces <old-task-id>`. Generic recovery never reactivates a cancelled or superseded task. Current applicable user instructions retain priority over research-memory snapshots and pending processing state.

## Sub-skills

| Skill | Owns |
|---|---|
| `mission-spec` | Requirement discussion, canonical draft, explicit approval |
| `mission-approved-doc` | Committed approved spec to `issues/<stem>/` artifacts |
| `mission-csv-execute` | CSV state machine, evidence, review, handoff, commits |
| `mission-recovery` | Locate unfinished CSVs under `issues/` and forward them |

Any valid CSV explicitly supplied by path may execute outside `issues/`. Its artifact root is its parent directory; ignored external artifacts remain local unless already tracked.
