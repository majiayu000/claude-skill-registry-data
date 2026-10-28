---
name: write-gods-tasks
description: >-
  Supplies the accepted task format GODS (Goal, Overview, Definition of Done,
  Solution). Use when the user asks what that format is, or to write up decided
  work in it. NOT for planning before coding — weighing variants belongs to the
  planning skill.
---

## HOW TO WRITE TASKS USING GODS FRAMEWORK

### What is GODS?

The framework helps to formulate tasks in a way that avoids misunderstandings
between the "client" and the "executor":

- Helps to clearly articulate the goal, context, and criteria for task
  completion.
- Makes the task transparent and understandable for executors and clients.
- Suitable for tasks with predictable cycles and measurable results.
- Does not replace flexible processes in research, innovation, or dynamic
  projects.

**Structure:**

- **G — Goal:** Why are we performing the task? What is the business goal?

- **O — Overview:** What is happening now? Why did the task arise? What is
  happening around it?

- **D — Definition of Done:** When do we consider the task completed? By what
  criteria?

- **S — Solution:** How can the task be solved?

---

### TASK FILE TEMPLATE

Moved here from the project instruction template on 2026-08-27. It used to sit
in `AGENTS.md`, which every session mounts, so the model already had the format
and never opened this skill: `write-gods-tasks-trigger-pos-1` scored 0/3 with
13, 16 and 27 tool calls, the agent writing the file itself each time. This
file is now the single source, and `AGENTS.md` points here.

Path: resolve the `tasks` role from the project instructions. The template
default is a date hierarchy — `<YYYY>/<MM>/<slug>.md`, kebab-case slug, max
40 chars — but the project instructions are authoritative.

```markdown
---
implements:
  - FR-XXX
---
# [Task Title]

## Goal

[Why? Business value.]

## Overview

### Context

[Full problematics, pain points, operational environment, constraints, tech debt, external URLs, @-refs to relevant files/docs.]

### Current State

[Technical description of existing system/code relevant to task.]

### Constraints

[Hard limits, anti-patterns, requirements (e.g., "Must use Deno", "No external libs").]

## Definition of Done

Every DoD item MUST pair with (a) an FR-ID and (b) a runnable acceptance reference. Items without this tuple are wishes, not contracts.

- [ ] FR-XXX: <observable behavior>
  - Test: `<path/to/test>::<test_name>` (or `Benchmark: <scenario-id>`)
  - Evidence: `<command that passes iff the item is done>`
- [ ] FR-YYY: <observable behavior>
  - Test: `...`
  - Evidence: `...`

## Solution

[Actionable step-by-step approach. Never left blank — a task file without a
Solution is not written yet. When a planning workflow weighed variants and the
user picked one, this covers that variant only; when no variant selection took
place, it covers the approach you are proposing.]
```

Frontmatter: `date` (YYYY-MM-DD; required), `status: to do | in progress | done |
superseded` (required), `implements: [FR-...]` (optional — present for FR-driven
tasks, omitted for internal/maintenance), optional `tags`, optional
`related_tasks`, optional `migrated_from`, optional `superseded_by` (required
when `status: superseded`). Never edit `status` by hand mid-flight — commit
workflows derive it from the `## Definition of Done` checkbox count.

---

### EXAMPLES OF APPLYING GODS

#### 1. Incidents (Platform team)

- **Goal:** Restore the CI/CD pipeline so that deployment delays do not exceed 1
  hour.
- **Overview:** Updated the Jenkins plugin → 5 builds with errors → version
  incompatible.
- **Definition of Done:** All builds pass without errors within a day, tests
  ≥98% successful, team notified.
- **Solution:** Roll back the plugin, patch, or change the tool after log
  analysis.

---

#### 2. Operational Tasks (Platform team)

- **Goal:** Update the monitoring system to reduce false positives.
- **Overview:** Outdated rules → too many alerts.
- **Definition of Done:** False positives ↓80%, checks passed, documentation
  updated.
- **Solution:** Use a ready-made runbook and scripts.

---

#### 3. Platform Development (Platform team)

- **Goal:** Implement a predictive analytics module to prevent incidents.
- **Overview:** Incident frequency has increased by 25%, no forecasting tools
  available.
- **Definition of Done:** Module integrated, accuracy ≥85%, pilot tested within
  3 months.
- **Solution:** Research ML models, selection after analysis.

---

#### 4. Product Team Requests (Platform team)

- **Goal:** Cut Alpha's deployment time in half and stop updates from breaking,
  so releases no longer block the product team. (Docker is the mechanism and
  belongs in Solution, not here.)
- **Overview:** Currently, Alpha runs on virtual machines, deployment takes a
  long time and causes errors during updates.
- **Definition of Done:**
  - The service runs in Docker.
  - Deployment time reduced by 50%.
  - All tests pass successfully.
  - Documentation updated.
  - Pilot launch confirmed.
- **Solution:** Use Docker Compose, CI/CD integration, and monitoring setup.
