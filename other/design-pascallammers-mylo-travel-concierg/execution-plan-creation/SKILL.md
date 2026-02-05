---
name: execution-plan-creation
description: Guide execution plan creation using the standard template. Execution plan organizes user stories into waves with agent assignments and verification gates. Use when PM agent drafts or updates an execution plan, or when validating wave structure and dependencies.
owner: project-manager-agent
---

# Execution Plan Creation Skill

**Purpose:** Guide execution plan creation following the standard template
**Trigger:** When PM agent creates or updates an execution plan document
**Output:** Well-structured execution plan with waves, dependencies, and agent assignments

---

## Template Reference

**ALWAYS read before creating:** `templates/execution-plan-template.md`

Contains: frontmatter fields, summary metrics, wave structure, story index, verification gates, agent assignments, risk/rollback sections.

---

## Workflow

1. **Read the template:**
   - Load `templates/execution-plan-template.md`
   - Note all required frontmatter fields and section structure

2. **Gather inputs:**
   - Read approved PRD for project context
   - Read all user stories from `user-stories/` folder
   - Identify story dependencies and complexity scores

3. **Analyze dependencies:**
   - Build dependency graph from story prerequisites
   - Validate DAG structure (detect cycles)
   - Identify critical path through dependencies

4. **Organize into waves:**
   - Wave 1: Stories with no dependencies
   - Subsequent waves: Stories whose dependencies are satisfied
   - Group parallel-executable stories within each wave

5. **Assign agents:**
   - Match story requirements to agent capabilities
   - Use full subagent_type paths (e.g., `core-claude-plugin:generic:coder`)
   - Reference `/skill agent-selection` for assignment guidance

6. **Define verification gates:**
   - Add build/lint/test commands per wave
   - Include integration checks between waves
   - Define rollback triggers

7. **Validate structure:**
   - Run validation checklist (see below)
   - Fix any missing or malformed sections

8. **Save execution plan:**
   - Write to `{projectFolder}/execution-plan.md`
   - Ensure frontmatter is complete

9. **Validation gate:**
   - Spawn reviewer for mandatory plan validation
   - On PASS: Continue to execution phase
   - On FAIL: Loop back with issues for revision

---

## Validation Gate

After execution plan is written, spawn reviewer for mandatory validation.

**Spawn:** `core-claude-plugin:generic:reviewer`
**Input:** Plan path, validation type `execution-plan`
**Output:** `{result: "PASS"|"FAIL", issues: []}`

| Result | Action                                              |
| ------ | --------------------------------------------------- |
| PASS   | Continue to next phase (wave execution)             |
| FAIL   | Return issues to project-manager, retry from step 7 |

**Validation Scope:**

- Frontmatter completeness
- Wave dependency integrity (valid DAG)
- Agent assignment validity
- Verification gates defined per wave

---

## Wave Organization Rules

| Rule                     | Guidance                                          |
| ------------------------ | ------------------------------------------------- |
| Wave 1 = foundation      | Stories with no dependencies, can run in parallel |
| Minimize wave count      | Group stories by dependency satisfaction          |
| Parallel within wave     | Stories in same wave execute concurrently         |
| Sequential between waves | Wave N+1 waits for Wave N verification gate       |
| Critical path awareness  | Identify longest dependency chain                 |

---

## Agent Assignment Guidelines

Reference `/skill agent-selection` for complete agent listing. Common assignments:

| Story Type             | Agent                   | subagent_type                                              |
| ---------------------- | ----------------------- | ---------------------------------------------------------- |
| General implementation | coder                   | `core-claude-plugin:generic:coder`                         |
| Backend/API            | backend-dev             | `core-claude-plugin:generic:backend-dev`                   |
| Database/Prisma        | prisma-database-agent   | `core-claude-plugin:domain:database:prisma-database-agent` |
| React Components       | react-component-agent   | `core-claude-plugin:domain:frontend:react-component-agent` |
| Unit Tests             | unit-test-agent         | `core-claude-plugin:domain:testing:unit-test-agent`        |
| Integration Tests      | integration-test-agent  | `core-claude-plugin:domain:testing:integration-test-agent` |
| Config files           | (specific config agent) | `core-claude-plugin:config:{category}:{agent-name}`        |
| Code review            | reviewer                | `core-claude-plugin:generic:reviewer`                      |
| Agent/Skill creation   | agent-author            | `core-claude-plugin:generic:agent-author`                  |

**Full subagent_type format:** `core-claude-plugin:{category}:{subcategory}:{agent-name}`

---

## Validation Checklist

### Frontmatter (all required)

- [ ] `project_id`, `title`, `status`, `owner` present
- [ ] `total_stories`, `total_complexity`, `total_waves` accurate
- [ ] `created`, `updated` dates (YYYY-MM-DD)

### Structure

- [ ] Summary table with metrics
- [ ] User Stories Index with all stories
- [ ] Wave sections with verification gates
- [ ] Agent Assignments table complete

### Wave Integrity

- [ ] Every story in exactly one wave
- [ ] Wave 1 = no dependencies (parallel)
- [ ] Subsequent waves depend only on prior waves
- [ ] No circular dependencies (valid DAG)

### Agent Assignments

- [ ] Every story has assigned agent
- [ ] Full subagent_type format used
- [ ] Agent matches story type

---

## Example

**Input:** PRD with 6 user stories

**Wave Assignment:**

- Wave 1: msm-auth-001, msm-auth-002 (no deps, parallel)
- Wave 2: msm-auth-003, msm-auth-004 (depend on Wave 1)
- Wave 3: msm-auth-005, msm-auth-006 (depend on Wave 2)

**Output:** `docs/epics/msm007-auth-api/execution-plan.md` with 3 waves, agent assignments, verification gates

---

## Integration

**Called by:** planning-phase, `/architect`, `/build`, `/ms` commands
**Calls:** Read (template, PRD, stories), Write (save plan), Task (reviewer validation gate)
**Spawns:** `core-claude-plugin:generic:reviewer` (mandatory validation gate)
**References:** `/skill agent-selection`, `/skill user-story-template`, `/skill execution-phase`

**Previous:** Story extraction | **Next:** Wave execution (on PASS) | Retry (on FAIL)
