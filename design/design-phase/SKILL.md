---
name: design-phase
description: Design phase with validation gates. Annotates PRD, creates story outlines, builds execution plan (via execution-plan-creation skill), validates artifacts via reviewer. NO HITL in this phase - single HITL happens after all docs complete.
---

# Design Phase Skill

> **ROOT AGENT ONLY** - Spawns agents, runs only from root Claude Code agent.

**Purpose:** Annotate PRD, create stories, build execution plan with validation gates (NO HITL)
**Trigger:** After requirements-phase passes (PRD created)
**Input:** `prdPath` (string), `projectFolder` (string), `complexity` (int), `tools` (string[]), `scope` (string[])
**Output:** `{storiesFolder, storyFiles, executionPlan, allValidated}`

**Flow:** Architect annotates PRD -> BA creates outlines -> PM builds plan -> Reviewer validates -> BA fills details -> Architect adds architecture -> Reviewer validates -> Continue to HITL

---

## Workflow Steps

### Step 1: Architect Annotates PRD

**Spawn:** `core-claude-plugin:generic:architect`

- Read approved PRD from `prdPath`
- Add inline architecture notes (API endpoints, key files, patterns)
- Keep annotations concise (50-100 lines max)
- Complexity >= 30 triggers deeper analysis mode

### Step 2: BA Creates Story Outlines

**Spawn:** `core-claude-plugin:generic:business-analyst`

- Read annotated PRD
- Create `user-stories/` folder in project folder
- Extract story outlines (title, brief description, dependencies)
- Follow Story Granularity Guidelines (see `reference.md`)
- Create files: `{PROJ}-{EPIC}-{NNN}-{slug}.md`
- Return paths to all story files

### Step 3: PM Creates Execution Plan

**Spawn:** `core-claude-plugin:generic:project-manager`
**Invokes:** `/skill execution-plan-creation`

- Read story outlines, analyze dependencies, build dependency graph
- Organize into parallel waves (max 10 agents/wave)
- Assign agents to each story
- Output to `execution-plan.md` in project folder

### Step 4: Validate Execution Plan

**Spawn:** `core-claude-plugin:generic:reviewer`
**Invokes:** `/skill document-validation` (type: execution-plan)

- Validate frontmatter fields and required sections
- Check wave integrity (all stories assigned, valid DAG)
- **If invalid:** Return issues to PM, loop back to Step 3

### Step 5: BA Fills Story Details

**Spawn:** `core-claude-plugin:generic:business-analyst`
**Invokes:** `/skill user-story-creation`

- Read each story outline
- Fill in complete story format (As a / I want / So that)
- Add acceptance criteria (minimum 3 testable criteria)
- Add technical details (files to create/modify)

### Step 6: Architect Adds Architecture Section

**Spawn:** `core-claude-plugin:generic:architect`

For each story file:

- Add "Architecture" section (if not exists)
- Fill in: API endpoints, key files, database models, component names, patterns

### Step 7: Validate Stories

**Spawn:** `core-claude-plugin:generic:reviewer`
**Invokes:** `/skill document-validation` (type: user-story)

For each story:

- Validate frontmatter fields and required sections
- Check acceptance criteria completeness
- **If invalid:** Return issues to BA, loop back to Step 5

### Step 8: Continue to HITL Approval Phase

**NO HITL in this phase.** Continue to single HITL gate.

The calling command (/build) handles the single HITL approval for all docs (PRD + execution plan + stories).

**Output:**

```json
{
  "storiesFolder": "docs/epics/msm008-feature/user-stories/",
  "storyFiles": ["MSM-008-001-story.md", "MSM-008-002-story.md"],
  "executionPlan": "docs/epics/msm008-feature/execution-plan.md",
  "allValidated": true
}
```

---

## Story Granularity

Create stories by **functional capability**, not by package/layer. See `reference.md` for detailed guidelines.

| Rule             | Description                             |
| ---------------- | --------------------------------------- |
| Testable Units   | Each story independently testable       |
| Max 15-20 min    | Break down larger stories               |
| Parallel default | Stories in same wave run concurrently   |
| Dependency-aware | Use `dependencies` field in frontmatter |

---

## Integration

| Type          | Items                                                                           |
| ------------- | ------------------------------------------------------------------------------- |
| **Called by** | `/build` (after requirements-phase), `/ms` (complexity >= 15)                   |
| **Spawns**    | architect (1,6), business-analyst (2,5), project-manager (3), reviewer (4,7)    |
| **Invokes**   | execution-plan-creation (3), user-story-creation (5), document-validation (4,7) |
| **Next**      | HITL Approval (single gate), then execution-phase                               |
