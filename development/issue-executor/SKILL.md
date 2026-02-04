---
name: issue-executor
description: Use this skill to start work on an assigned GitHub issue. This is the core implementation loop of the SynthesisFlow methodology. Guides the AI to load full context (specs, plans, retrospective), create a feature branch, and begin implementation. Triggers include "start work on issue", "implement issue #X", or beginning development work.
---

# Issue Executor

## Purpose

Execute the core development workflow for a single, atomic GitHub issue within the SynthesisFlow methodology. This skill ensures all necessary context is loaded before any code is written, work is isolated on a dedicated feature branch, and the implementation follows the spec-driven approach.

## When to Use

Use this skill in the following situations:

- Starting work on a planned GitHub issue from the current sprint
- Beginning a work session and ready to implement a specific task
- Need to load full context for an issue before coding
- Want to follow the complete SynthesisFlow development workflow

## Prerequisites

- GitHub repository with issues created (via sprint-planner skill)
- Git working directory is clean (no uncommitted changes)
- Currently on main branch
- `gh` CLI tool installed and authenticated
- `jq` tool installed for JSON parsing
- Project has docs/ structure with specs and retrospective

## Core Principles

### Context is King

Load all relevant context before writing any code:
- **Issue details**: Requirements and acceptance criteria
- **Spec files**: Related specifications from docs/specs or docs/changes
- **Retrospective**: Learnings from past issues to avoid repeating mistakes
- **Doc index**: Map of all available documentation

### Isolation

All work happens on a dedicated feature branch to:
- Protect main branch from work-in-progress
- Enable clean PR workflow
- Allow abandoning work without impact

### Atomic Work

Each issue represents a single, well-defined task that can be:
- Completed independently
- Reviewed as a unit
- Merged without dependencies

## Workflow

### Step 1: Identify the Issue

Determine which issue to work on. The user specifies the issue number (e.g., #45).

Check open issues if needed:
```bash
gh issue list --assignee @me --state open
```

### Step 2: Run the Helper Script

Execute the work-on-issue script with the issue number:

```bash
bash scripts/work-on-issue.sh ISSUE_NUMBER
```

For example:
```bash
bash scripts/work-on-issue.sh 45
```

### Step 3: Understand What the Script Does

The helper script automates these steps:

1. **Validates prerequisites**:
   - Checks jq is installed
   - Verifies git working directory is clean
   - Ensures no uncommitted changes exist

2. **Loads issue context**:
   - Fetches issue title and body from GitHub
   - Extracts associated spec file references
   - Reads spec files if they exist

3. **Loads project context**:
   - Reads RETROSPECTIVE.md for lessons learned
   - Runs doc-indexer to get documentation map

4. **Creates feature branch**:
   - Generates branch name from issue (e.g., `feat/45-restructure-doc-indexer`)
   - Checks out new branch

5. **Confirms readiness**:
   - Displays success message
   - Confirms branch created and context loaded

### Step 4: Review Loaded Context

After the script completes, review the context it loaded:

- **Issue details**: Understand requirements and acceptance criteria
- **Spec files**: Review specifications for what needs to be built
- **Retrospective**: Note any relevant lessons from past work
- **Doc index**: Identify other relevant documentation to read

### Step 5: Begin Implementation

With full context loaded and feature branch created:

1. Plan the implementation approach
2. Write code following the acceptance criteria
3. Test the changes
4. Commit work incrementally
5. Push to remote when ready for PR

### Step 6: When to Use Script vs Manual Steps

**Use the helper script when**:
- Starting fresh work on a new issue
- Need to load all context automatically
- Want the standard workflow enforced

**Use manual steps when**:
- Already familiar with the issue context
- Continuing work on an existing branch
- Need to customize the workflow for special cases

## Error Handling

### Working Directory Not Clean

**Symptom**: Script reports uncommitted changes

**Solution**:
- Commit current work: `git add . && git commit -m "..."`
- Or stash changes: `git stash`
- Or discard changes: `git restore .` (careful!)
- Then run script again

### Not on Main Branch

**Symptom**: Currently on a feature branch

**Solution**:
- Finish current work and create PR
- Or switch to main: `git switch main`
- Then run script again

### Missing jq Tool

**Symptom**: Script reports jq not installed

**Solution**:
- Install jq: `sudo apt install jq` (Linux)
- Or: `brew install jq` (Mac)
- Or manually parse JSON without script

### Spec File Not Found

**Symptom**: Script reports spec file doesn't exist

**Solution**:
- Verify the spec file path in the issue body
- Check if spec is in docs/changes/ (proposed) vs docs/specs/ (approved)
- Read the spec from docs/changes/ if it's a new feature
- Proceed without spec if issue doesn't require one

### Branch Already Exists

**Symptom**: Git reports branch name already exists

**Solution**:
- Check if you're resuming work: `git switch feat/45-...`
- Or delete old branch: `git branch -D feat/45-...`
- Then run script again

## Notes

- The script loads context but doesn't write code - that's the AI's job with full understanding
- Branch naming follows convention: `feat/ISSUE_NUMBER-kebab-case-title`
- Issue body should reference spec files as: `docs/specs/...` or `docs/changes/...`
- Retrospective provides valuable lessons - pay attention to recent learnings
- Doc indexer shows what documentation exists without loading full content
- For detailed workflow steps, see `references/work-on-issue.md`
- The script is a helper to reduce repetitive context loading - Claude still executes the development workflow
