---
name: project-scoring
description: How the Score page of the Agent Console measures a project against its own plan, release by release. Read it when a task must be classified under a scoring criterion, when the Score page shows unclassified tasks, when a criterion looks wrong, or when someone proposes a new criterion or weight.
last_reviewed: 2026-10-23
sources: [original]
---

# Project scoring (Score page)

The page is computed live by `Claude/hooks/score.py` from the project's own documents. Nobody types numbers.

## What is measured
Per criterion and release, on a 0-5 scale: **plan** (what the roadmap expects), **built** (Done plus half of In progress) and **proven** (Done, minus open bugs linked to the task). Totals are out of 100: the primary criteria (the contest's own quality criteria) share 70 points, the additional criteria (ours) carry their weights (30 points), a bonus track is shown but is not in the 100. A traffic light per criterion says where to act: red = act now, yellow = watch, green = fine; the later the release, the smaller the accepted gap.

## Where the evidence comes from
- ROADMAP tasks (release codes `P<phase>-R<n>`; `Later` and `Out of scope` are ignored).
- BUGS open bugs: blocking 1.0, major 0.6, medium 0.3, minor 0.1 off the proven value; a bug that names a task id (T-012) hits that task's criteria, any other open bug lowers Feasibility.
- RELEASE-READINESS verdict for Publishing readiness (READY 5, with reservations 3.5, NOT READY 1.5, none 0).
- Docs format check and STATUS freshness for Documentation; the number of planned tasks when first measured for Scope.

## Classifying tasks
A task is linked to a criterion by keywords in `Claude/reference/score-criteria.json`. When a task is not linked (the page lists them), add it to `Claude/docs/score-map.json`: `{"T-012": ["audio", "fun"]}`. planner-docs does this for every task it creates. An explicit entry replaces the keyword match.

## Judgement calls (agents)
Only `Claude/docs/score-notes.json` takes subjective input: `{"fun": {"adj": -0.5, "why": "stranger playtest: unclear goal"}}`. `adj` is capped at +-1, needs a reason based on a log, playtest or check, and is shown on the page as evidence. Never raise a value without evidence; never edit the code to move a score.

## New criteria or weights
Never edit the shipped criteria. Propose the change through the Skills page (skill-reflector, `skills_lib.py propose`): the owner approves, then the criterion is saved in `Claude/docs/score-criteria-extra.json` (fields: id, n, g = primary|additional|bonus, w, depth, keywords, tip). Use it when the contest rules or the genre change what matters (for example a criterion the owner never uses is dropped from the plan, not from the list).

## Snapshots
When a release closes (all its tasks Done) a row is appended to `Claude/logs/score-history.jsonl`, so later releases can be compared with it. The hook runs after ROADMAP/BUGS edits; `python3 Claude/hooks/score.py --snapshot` runs it by hand.
