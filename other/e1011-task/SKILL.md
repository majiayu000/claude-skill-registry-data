---
name: e1011-task
description: "Use when define task characteristics to feed human-centred design (HCD) analysis per ECSS-E-ST-10-11C §4.2.1.4: identify each operator task by name and mission phase, assign a frequency category (rare, occasional, routine), determine the criticality level (safety-critical, mission-critical, non-critical), score four workload dimensions (physical demand, cognitive demand, time pressure, consequence of error) on a three-point scale, and flag high-risk pairings where elevated criticality coincides with high workload for priority HCD attention. The resulting task inventory and characteristics drive display design, automation boundary decisions, training scope, and workload mitigation strategies. Trigger: ecss, e-st-10-system-scope, hcd, human-factors, task-analysis, workload, criticality, operator-task."
license: Apache-2.0
compliance: STANDARDS-REF
standards:
  - id: ecss
    reference-only: true
gated: false
domain: space-systems
pack: space-systems
compatibility: "agentskills.io SKILL.md; any SKILL.md host (Claude Code, Hermes, OpenClaw)"
metadata:
  domain: space-systems
  subdomain: ecss
  tags: [ecss, e-st-10-system-scope, hcd, human-factors, task-analysis, workload, criticality, operator-task]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Human Factors Engineering — Task Characterization for HCD (space-systems/ecss/e1011-task)

Use when the task is to define operator tasks and their key characteristics
(frequency, criticality, workload) per ECSS-E-ST-10-11C §4.2.1.4 so that
the human-centred design process has a quantified task inventory to drive
display design, automation boundaries, training scope, and workload
mitigation decisions.

## Domain quick reference

- §4.2.1.4 requires the engineering team to produce a task inventory for
  every operator interaction with the system. Each entry covers three
  mandatory characteristics: frequency, criticality, and workload.
- **Frequency** captures how often the task is performed in a reference
  mission: rare (once or a few times per mission), occasional (weekly or
  less), or routine (daily or more). Frequency drives training repetition
  requirements and procedure refresh intervals.
- **Criticality** captures the consequence if the task is performed
  incorrectly or not at all: safety-critical (risk of crew injury, loss of
  life, or loss of vehicle), mission-critical (risk of mission abort or
  loss of primary mission objective), or non-critical (minor impact,
  recoverable). Criticality drives the depth of error-tolerance design and
  the level of independent verification required in the procedure.
- **Workload** is assessed across four dimensions — physical demand,
  cognitive demand, time pressure, and consequence of error — each rated
  low, medium, or high. The four ratings are summed (1/2/3 per level) into
  a score of 4–12. Scores 10–12 map to a high workload band, 7–9 to
  medium, 4–6 to low.
- A task is flagged **high-risk** when its criticality is safety-critical
  or mission-critical AND its workload band is high. High-risk tasks
  require prioritized HCD attention: automation assistance, display
  cueing, workload reduction, or procedure simplification.

## Workflow

1. Enumerate every operator interaction with the system for each mission
   phase. Name each task concisely (verb + object, e.g. "Verify docking
   latch engagement") and record its mission phase. Reject any entry with
   an empty name or phase.
2. Assign a frequency category (rare / occasional / routine) to each task
   based on the mission timeline. Use the reference mission duration as the
   denominator; if a task spans multiple phases, assign the category for
   the highest-frequency occurrence.
3. Assign a criticality level (safety-critical / mission-critical /
   non-critical) based on the worst credible consequence of the task being
   omitted or executed incorrectly. Use the system's hazard log as the
   authority for safety-critical assignments.
4. Rate each of the four workload dimensions (physical demand, cognitive
   demand, time pressure, consequence of error) as low, medium, or high,
   then compute the total workload score. Derive the workload band from the
   score: 10–12 = high, 7–9 = medium, 4–6 = low.
5. Flag every task whose criticality is safety-critical or mission-critical
   AND whose workload band is high. Record these as high-risk tasks
   requiring dedicated HCD mitigation.
6. Compile the full task inventory table (name, phase, frequency,
   criticality, workload score, workload band, high-risk flag) and deliver
   it as an input to the HCD planning activity. Confirm that every task
   entry has passed validation before inclusion.

## Pitfalls

- Omitting the workload assessment for non-critical tasks: even non-critical
  tasks with high workload can interfere with adjacent critical tasks through
  operator saturation, so the workload score must be recorded for all tasks.
- Conflating criticality with complexity: a highly complex task (high
  cognitive demand) is not automatically safety-critical; criticality is
  determined by consequence, not by difficulty.
- Treating the workload band as an absolute ceiling: the four-dimension
  score is a planning heuristic, not a certified human-factors rating; any
  task approaching the high band boundary (score 9–10) should be reviewed
  by the human-factors lead before its band is finalized.
- Leaving a task's criticality as safety-critical without a corresponding
  hazard-log reference: the assignment must be traceable to a specific
  hazard entry, not an informal judgment.
- Applying the same workload score across all mission phases for a task
  that changes character (e.g. an EVA procedure performed under nominal
  versus contingency conditions); use separate task entries for
  significantly different operational contexts.

## Behavior contract (gate 3)

The task-validation, workload-scoring, band-mapping, high-risk-flagging,
and inventory-analysis logic is exercised by the gate 3 contract test:
scripts/test_e1011_task.py against scripts/e1011_task_logic.py (stdlib
unittest, offline). Run:
python3 scripts/test_e1011_task.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
