---
name: speckit-phasestoissues
description: Convert development phases into individual GitHub issues for better tracking
  and collaboration.
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: workflows:commands/phasestoissues.md
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

### 1. Load Feature Context

Run the prerequisite check script from repo root and parse the output:

```bash
cd "$(git rev-parse --show-toplevel)" && \
source .specify/scripts/bash/common.sh && \
get_feature_paths
```

This provides:
- `FEATURE_DIR` - Feature directory path
- `FEATURE_SPEC` - Specification file (spec.md)
- `IMPL_PLAN` - Implementation plan (plan.md)
- `TASKS` - Task list (tasks.md)

All paths are absolute.

### 2. Verify GitHub Repository

Get the Git remote URL:

```bash
git config --get remote.origin.url
```

> [!CAUTION]
> ONLY PROCEED TO NEXT STEPS IF THE REMOTE IS A GITHUB URL

**Stop immediately** if:
- Remote is not a GitHub URL
- Remote URL cannot be determined
- Repository does not match expected pattern

### 3. Extract Phase Information

Load and parse the specification file (`$FEATURE_SPEC` / spec.md):

**Extract:**
- **Phase Title**: First H1 heading or feature name from directory
- **Phase Description**: Content under "Story" or "Overview" section
- **Acceptance Criteria**: Content under "Acceptance Criteria" section
- **Context/Background**: Any additional context sections

**Parse Tasks** from `$TASKS` (tasks.md):
- Extract all task lines in format: `- [ ] T001: Task description`
- Preserve task IDs and descriptions
- Note task status (pending vs completed)

**Parse Plan** (if exists) from `$IMPL_PLAN` (plan.md):
- Extract implementation approach
- Note technical decisions
- Identify dependencies

### 4. Build Phase Issue Body

Construct a comprehensive GitHub issue for each phase with this structure:

```markdown
## Description

[Phase description from spec.md]

## Acceptance Criteria

[Acceptance criteria from spec.md]

## Implementation Plan

[High-level approach from plan.md, if available]

### Key Technical Decisions
- [Decision 1]
- [Decision 2]

### Dependencies
- [Dependency 1]
- [Dependency 2]

## Tasks

See sub-issues for individual task tracking.

## Context

**Branch**: `[branch-name]`
**Feature Directory**: `[feature-dir]`
**Phase**: [phase-number]/[total-phases]
**Created from spec-kit workflow**

---

**Note**: Sub-issues will be created for each task. Use `/speckit.workflows.review` to validate implementation against acceptance criteria.
```

### 5. Determine Issue Labels

Automatically assign labels based on:

**Workflow Type** (from branch pattern):
- `bugfix/*` -> `bug`, `bugfix`
- `refactor/*` -> `refactor`, `technical-debt`
- `hotfix/*` -> `hotfix`, `urgent`
- `modify/*` -> `enhancement`, `modification`
- `deprecate/*` -> `deprecation`, `breaking-change`
- Standard feature -> `feature`, `enhancement`

**Priority** (from spec.md if available):
- Critical/High -> `priority: high`
- Medium -> `priority: medium`
- Low -> `priority: low`

**Status**:
- `status: planning` (if tasks exist but none completed)
- `status: in-progress` (if some tasks completed)

### 6. Create Phase Issues

For each phase, use the GitHub MCP server tool to create the parent issue:

**Required:**
- `owner`: Extract from Git remote URL
- `repo`: Extract from Git remote URL
- `title`: "Phase N: [Phase title]" from spec.md
- `body`: Formatted issue body from step 4
- `labels`: Labels from step 5

**Capture the issue number** for sub-issue creation.

### 7. Create Sub-Issues for Tasks

For each task within a phase:

1. **Create task issue** using GitHub MCP:
   - `title`: "T001: [Task description]" (preserve task ID)
   - `body`:
     ```markdown
     ## Task Details

     [Task description from tasks.md]

     ## Context

     **Parent Phase**: #[phase-issue-number]
     **Branch**: [branch-name]
     **Feature Directory**: [feature-dir]

     ---

     Part of larger feature spec-kit workflow.
     ```
   - `labels`: Same labels as parent phase issue

2. **Link as sub-issue** using `mcp_github_github_sub_issue_write`:
   - `method`: "add"
   - `owner`: From Git remote URL
   - `repo`: From Git remote URL
   - `issue_number`: Parent phase issue number
   - `sub_issue_id`: Task issue ID (not issue number - get from created issue)

**Important**: GitHub sub-issues require issue IDs, not issue numbers. Extract the `id` field from the created task issue.

### 8. Set Sub-Issue Priority

If tasks have natural ordering, use `mcp_github_github_sub_issue_write` with method "reprioritize" to set task order within the phase
- `labels`: Labels from step 5

> [!CAUTION]
> UNDER NO CIRCUMSTANCES EVER CREATE ISSUES IN REPOSITORIES THAT DO NOT MATCH THE REMOTE URL

**Example:**
```
Repository: github.com/user/repo
Title: Phase 1: User Authentication
Labels: feature, status: planning
Body: [Full formatted content]
```

### 9. Link Issue to Branch

After creating the issue, provide instructions to link it:

```bash
# Update spec.md with issue link
echo -e "\n## GitHub Issue\n\n#[issue-number]" >> "$FEATURE_SPEC"

# Or add issue number to commit messages
git commit --amend -m "feat: [phase title] (#[issue-number])"
```

### 10. Output Summary

Display result to user:

```
GitHub Issue Created

Issue: #[number]
Title: [phase title]
URL: https://github.com/[owner]/[repo]/issues/[number]

Tasks Included: [N tasks]
Labels: [label1, label2, ...]

Next Steps:
1. Review issue on GitHub
2. Assign to team members
3. Add to project board/milestone
4. Track progress by checking off tasks
5. Use /speckit.workflows.review when ready for validation
```

## Important Notes

1. **One Issue Per Phase**: Creates a single issue representing the development phase
2. **Tasks as Checkboxes**: All tasks become checkboxes in the issue body
3. **Comprehensive Context**: Issue includes spec, acceptance criteria, and plan
4. **Safe by Default**: Validates GitHub remote before creating issues
5. **Workflow Aware**: Labels reflect the workflow type (bugfix, refactor, etc.)
6. **Trackable**: Issue provides full context for team discussion and tracking

## Edge Cases

**No tasks.md exists**:
- Create issue with story and acceptance criteria only
- Note in issue body that task breakdown is needed
- Recommend running `/speckit.tasks` first

**No spec.md exists**:
- Cannot create issue without phase context
- Recommend running `/speckit.plan` or creating spec first
- Display error message with guidance

**Multiple features in repo**:
- Uses current feature based on branch/directory context
- Issue title and content scoped to current feature only

**Issue already exists**:
- Check if issue with same title exists (optional)
- Warn user before creating duplicate
- Offer to update existing issue instead

**No GitHub remote**:
- Stop with clear error message
- Cannot create issues without GitHub repository
- Suggest adding GitHub remote or creating issues manually

## Context Information

User input: $ARGUMENTS

Create a comprehensive, well-structured GitHub issue that represents the development phase with tasks as actionable checkboxes.