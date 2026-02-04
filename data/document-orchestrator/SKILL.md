---
name: document-orchestrator
description: Generate structured markdown documents (PRDs, tasks, investigation plans) from templates based on workflow type. Creates directory structure and manages document lifecycle for feature, bug, and plan workflows.
---

# Document Orchestrator

This skill handles creation of all structured documentation for workflow, bugfix, and plan commands.

## When to Use

Use this skill when:
- After selecting a Linear task with linear-task-selector
- Need to generate PRD, tasks, investigation plans, or decomposition docs
- Creating directory structure for feature/bug/plan workflows

## Instructions

### Step 1: Load Task Context
Read the selected task from the appropriate directory (created by linear-task-selector):
- For features: `features/<feature-name>/selected-task.json`
- For bugs: `bugs/<bug-name>/selected-task.json`
- For epics: `epics/<epic-name>/selected-task.json`

The `featureName` field in the JSON tells you which directory to use.

Extract:
- `workflowType`: "feature", "bugfix", or "plan"
- `featureName`: Directory name for locating/storing files
- `title`: Task title
- `description`: Full task description
- `taskId`: Linear issue ID

### Step 2: Verify Directory Structure

The directory should already exist (created by linear-task-selector).

**For feature workflows:**
Use existing `features/<feature-name>/` directory

**For bugfix workflows:**
Use existing `bugs/<bug-name>/` directory

**For plan workflows:**
Use existing `epics/<epic-name>/` directory

If directory doesn't exist, create it using the `featureName` from selected-task.json.

### Step 3: Generate Documents

#### For Feature Workflow

**3a. Generate PRD**
Use the PRD template from `~/.claude/tools/prompts/prd-prompt-template.md`:

Role: Senior product manager for Hokusai
Task: Generate PRD that a junior team member can follow
Input: Replace `{{PROJECT_SUMMARY}}` with task title + description
Output: `features/<feature-name>/prd.md`

Required sections:
- Objectives
- Personas (if applicable)
- Success criteria
- Clearly delineated tasks
- Straightforward language
- No dates, versions, icons, or emojis

Reference: Review project README.md and https://docs.hokus.ai/

**3b. Generate Tasks**
Use the tasks template from `~/.claude/tools/prompts/tasks-prompt-template.md`:

Role: Product manager working with junior developer
Task: Create detailed, prioritized task list from PRD
Input: Read `features/<feature-name>/prd.md`
Output: `features/<feature-name>/tasks.md`

Required format:
```markdown
## Section Name
1. [ ] Task description
   a. [ ] Subtask description
   b. [ ] Subtask description

## Testing
7. [ ] Write and implement tests
   a. [ ] Database schema tests
   b. [ ] API endpoint tests
   c. [ ] Integration tests
```

Required components:
1. Automated testing (consistent with existing test suite)
2. Documentation (technical changes in README.md)
3. Dependencies (noted in section headers)

#### For Bugfix Workflow

**3a. Generate Investigation Plan**
Use template from `~/.claude/tools/prompts/bug-investigation-template.md`:

Role: Senior software engineer and debugging specialist
Task: Create comprehensive investigation plan
Input: Replace `{{BUG_SUMMARY}}` with task title + description
Output: `bugs/<bug-name>/investigation.md`

Required sections:
1. Bug Summary (description, when/who affected, impact, severity)
2. Reproduction Steps (verified steps, environment, success rate)
3. Affected Components (services, tables, endpoints, dependencies)
4. Initial Observations (errors, logs, metrics, recent changes)
5. Data Analysis Required (logs, queries, metrics, reports)
6. Investigation Strategy (priority, tools, questions, success criteria)
7. Risk Assessment (impact, escalation, security, data integrity)
8. Timeline (first appeared, deployments, frequency, patterns)

**3b. Generate Hypotheses Document**
Use template from `~/.claude/tools/prompts/bug-hypothesis-template.md`:

Output: `bugs/<bug-name>/hypotheses.md`

Format for each hypothesis:
```markdown
## Hypothesis N: [Brief description]

**Proposed Root Cause:**
[What you think is causing the bug]

**Why This Could Cause Observed Behavior:**
[Technical explanation]

**How to Test:**
[Specific steps to validate/invalidate]

**Expected Outcome if Correct:**
[What you'll observe if this is the root cause]

**Priority:** [High/Medium/Low]
**Likelihood:** [High/Medium/Low]
**Status:** [Untested/Testing/Confirmed/Rejected]
```

**3c. Generate Fix Tasks Document**
Use template from `~/.claude/tools/prompts/bug-tasks-template.md`:

Output: `bugs/<bug-name>/fix-tasks.md`

Required sections:
1. Root cause fix implementation
2. Tests to prevent regression
3. Documentation updates
4. Monitoring/alerting improvements

#### For Plan Workflow

**3a. Generate Decomposition Request**
Output: `epics/<epic-name>/decomposition-request.json`

```json
{
  "issueNumber": 10,
  "title": "Epic Title",
  "projectName": "Project Name",
  "description": "Epic description summary"
}
```

**3b. Research Existing Implementation**
Use Read, Grep, Glob tools to:
- Understand what already exists
- Identify what's missing
- Find relevant files and patterns

Output: `epics/<epic-name>/research.md`

**3c. Generate Decomposition Plan**
Output: `epics/<epic-name>/decomposition-plan.json`

```json
{
  "masterDocumentPath": "path/to/main/doc.md",
  "relevantFiles": ["file1.ts", "file2.tsx"],
  "subIssues": [
    {
      "title": "Task title (action verb + specific noun)",
      "description": "Detailed description with context, requirements, acceptance criteria, references, edge cases",
      "dependencies": [0, 1],
      "estimate": 5,
      "priority": 1
    }
  ]
}
```

Guidelines:
- 3-10 sub-issues per epic
- Each completable in single PR
- Include tests and docs in each task
- Clear dependencies using array indices
- Estimates: 1-2 simple, 3-5 moderate, 5-8 complex
- Priority: 1 urgent, 2 high, 3 normal, 4 low

### Step 4: Validate Documents

Check that:
- All required sections are present
- Content is specific and actionable
- No placeholder text remains (e.g., {{PROJECT_SUMMARY}})
- File paths are correct
- Markdown formatting is valid

### Step 5: Return Summary

Provide user with:
```
✓ Documents generated:
  - features/add-user-auth/prd.md
  - features/add-user-auth/tasks.md

Next step: Review PRD and tasks, then begin implementation
```

## Examples

### Example 1: Feature Documentation
```
Input: features/add-user-auth/selected-task.json with workflowType: "feature"
Process:
1. Use existing features/add-user-auth/
2. Generate prd.md from template + task description
3. Generate tasks.md from PRD
4. Return: "✓ PRD and tasks created"
```

### Example 2: Bug Documentation
```
Input: bugs/contact-discovery-timeout/selected-task.json with workflowType: "bugfix"
Process:
1. Use existing bugs/contact-discovery-timeout/
2. Generate investigation.md from template + bug description
3. Generate hypotheses.md with 3-5 initial hypotheses
4. Generate fix-tasks.md template
5. Return: "✓ Investigation plan created"
```

### Example 3: Plan Documentation
```
Input: epics/user-management-system/selected-task.json with workflowType: "plan"
Process:
1. Use existing epics/user-management-system/
2. Generate decomposition-request.json
3. Research existing codebase → research.md
4. Generate decomposition-plan.json with 5 sub-issues
5. Return: "✓ Decomposition plan created"
```

## Error Handling

### Missing Task Context
If no selected-task.json exists in the expected directory:
1. Error: "No task selected. Run linear-task-selector first."
2. Exit gracefully

### Directory Already Exists
If feature/bug directory exists:
1. Warn user: "Directory already exists: features/X"
2. Ask: "Overwrite? (y/n)"
3. If no, suggest alternative name

### Template Errors
If template generation fails:
1. Show specific error (missing info, API failure, etc.)
2. Ask user for missing information
3. Retry generation

## Output

This skill outputs:
- Feature workflow: `features/<name>/prd.md`, `features/<name>/tasks.md`
- Bugfix workflow: `bugs/<name>/investigation.md`, `bugs/<name>/hypotheses.md`, `bugs/<name>/fix-tasks.md`
- Plan workflow: `epics/<name>/decomposition-request.json`, `epics/<name>/decomposition-plan.json`, `epics/<name>/research.md`
- Console: Summary of created documents

Note: All files are stored in workflow-specific directories to prevent conflicts when multiple Claude sessions run concurrently.

## Integration

This skill integrates with:
- **Input from**: linear-task-selector (task context)
- **Output to**: git-workflow-manager (branch creation, commits)
- **Used by**: workflow, bugfix, plan commands
