---
name: sprint-planner
description: Use this skill when planning a new sprint by selecting approved specs from the project board and creating atomic GitHub issues for the development team. Triggers include "plan sprint", "create sprint", "start new sprint", or beginning a development cycle.
---

# Sprint Planner Skill

## Purpose

Plan and initialize a new sprint by selecting approved specifications from the project board, creating a milestone, and generating atomic GitHub issues for each task. This skill bridges the gap between approved specs and executable work items, breaking down high-level features into trackable, atomic tasks for the development team.

## When to Use

Use this skill in the following situations:

- Starting a new sprint or development cycle
- Converting approved specs into actionable GitHub issues
- Creating a milestone and task breakdown for a feature
- Initializing work items from the project board backlog
- Breaking down an epic into atomic implementation tasks

## Prerequisites

- Project board configured with "Approved Backlog" status
- Approved spec files exist in `docs/specs/` directory
- Specs have task lists with `- [ ]` checkbox format
- GitHub repository set up with project board
- `gh` CLI tool installed and authenticated
- `jq` tool installed for JSON parsing
- Epic issues linked to spec files in issue body

## Workflow

### Step 1: Review Project Board

Check the project board for approved specs ready to be planned:

```bash
gh project item-list PROJECT_NUMBER --owner @me --format json
```

Identify epics in the "Approved Backlog" status. These represent specs that have been reviewed, approved, and are ready for implementation.

### Step 2: Discuss Sprint Scope with User

Engage the user to determine:
- Which epic(s) to include in the sprint
- Sprint timeline and duration
- Sprint goals and priorities
- Resource availability

Review the available epics together and select which work to prioritize for this sprint.

### Step 3: Define Sprint Metadata

Work with the user to establish:
- **Sprint name**: e.g., "Sprint 4", "Q1 2025 Sprint 2"
- **Sprint goals**: High-level objectives for this development cycle
- **Timeline**: Start and end dates (if applicable)
- **Success criteria**: How to measure sprint completion

### Step 4: Run the Helper Script

Execute the sprint planning script to automate GitHub issue creation:

```bash
bash scripts/create-sprint-issues.sh
```

### Step 5: Understand What the Script Does

The helper script automates these steps:

1. **Queries project board**:
   - Fetches all items in "Approved Backlog" status
   - Displays available epics with their issue numbers

2. **Prompts for epic selection**:
   - User enters the epic issue number to plan
   - Script retrieves epic details and body

3. **Extracts spec file**:
   - Parses epic body to find associated spec file path
   - Validates the spec file exists

4. **Prompts for milestone name**:
   - User enters sprint milestone name
   - Script creates the GitHub milestone

5. **Parses tasks from spec**:
   - Reads spec file for task list items (`- [ ] **Title**: Description`)
   - Creates a GitHub issue for each task

6. **Creates GitHub issues**:
   - Each task becomes an issue with "TASK: " prefix
   - Issues reference the spec file and parent epic
   - Issues are assigned to the sprint milestone

### Step 6: Verify Issue Creation

After the script completes:

```bash
gh issue list --milestone "Sprint 4"
```

Review that:
- All expected tasks are present
- Issue titles are clear and actionable
- Issues reference correct spec and epic
- Milestone assignment is correct

### Step 7: Review Created Issues with User

Walk through the created issues together:
- Confirm task breakdown is complete
- Verify priorities are set appropriately
- Discuss any missing tasks or adjustments needed
- Assign issues if team members are identified

### Step 8: Update Project Board (Optional)

If using project board automation:
- Move epic from "Approved Backlog" to "In Sprint"
- Verify task issues appear on project board
- Set priorities or labels as needed

### Step 9: Document Sprint Plan (Optional)

Consider creating a sprint planning document:

```markdown
# Sprint 4 Plan

**Timeline**: Nov 1 - Nov 15, 2025
**Epic**: #44 - Claude Code Skill Compliance
**Milestone**: Sprint 4

## Goals
- Restructure all 7 SynthesisFlow skills
- Improve Claude Code compliance
- Validate with skill validation script

## Tasks
- #45 - Restructure doc-indexer skill
- #46 - Restructure project-init skill
...
```

## Error Handling

### jq Not Installed

**Symptom**: Script reports jq command not found

**Solution**:
- Install jq: `sudo apt install jq` (Linux)
- Or: `brew install jq` (Mac)
- Verify: `jq --version`

### No Approved Epics Found

**Symptom**: Script reports no epics in approved backlog

**Solution**:
- Verify project board has "Approved Backlog" status
- Check if epics are in correct status column
- Confirm specs have been approved via spec PR
- Run spec-authoring skill to create and approve specs first

### Epic Body Missing Spec Reference

**Symptom**: Script cannot find spec file in epic body

**Solution**:
- Update epic issue body to include spec file path
- Format: `docs/specs/feature-name/spec.md`
- Ensure spec file actually exists at that path
- Follow spec-authoring workflow to create spec if needed

### Milestone Already Exists

**Symptom**: GitHub API returns error that milestone exists

**Solution**:
- Use a different milestone name
- Or manually delete existing milestone if unused
- Or add tasks to existing milestone via `gh issue create`

### Spec File Missing Task List

**Symptom**: Script creates no issues or very few issues

**Solution**:
- Verify spec file has task list in correct format: `- [ ] **Title**: Description`
- Ensure tasks are in a clear section (e.g., `## Tasks` or `## Implementation`)
- Review spec-delta.md template for proper task formatting
- Update spec file to include detailed task breakdown

### Permission Denied Creating Milestone

**Symptom**: GitHub API returns 403 or permission error

**Solution**:
- Verify `gh` CLI is authenticated: `gh auth status`
- Ensure you have repository write access
- Re-authenticate if needed: `gh auth login`
- Verify repository name is correct in script REPO variable

## Configuration Notes

The script uses these configuration variables (lines 6-11):

```bash
PROJECT_NUMBER="1"
APPROVED_BACKLOG_ID="888736cd"
OWNER="@me"
REPO="bodangren/git-workflow"
```

**To adapt for your project:**
1. Update `PROJECT_NUMBER` to your GitHub project number
2. Find `APPROVED_BACKLOG_ID` by querying project field values
3. Update `REPO` to your repository path (owner/repo)
4. Keep `OWNER="@me"` to use current authenticated user

**Finding your Approved Backlog ID:**
```bash
gh project field-list PROJECT_NUMBER --owner @me
```

## Notes

- **Script automates repetitive work**: Creating dozens of issues manually is tedious and error-prone
- **LLM guides the strategic decisions**: Which specs to plan, sprint scope, timeline
- **Task format matters**: Spec files must use `- [ ] **Title**: Description` format for parsing
- **One epic per sprint run**: Run the script multiple times if planning multiple epics
- **Milestone groups tasks**: All tasks from same epic share a milestone for easy filtering
- **Epic remains parent**: Each task issue references parent epic for traceability
- **Project board integration**: Issues can be automatically added to project board if configured
- **Idempotent considerations**: Running script twice creates duplicate issues - be careful
- **Manual refinement expected**: Review and adjust created issues as needed after script runs
- **Sprint planning is collaborative**: Engage user throughout the process for priorities and scope
