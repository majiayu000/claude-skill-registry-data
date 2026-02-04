---
name: Issue Orchestration
description: Use when orchestrating a Jira issue through the full development lifecycle to Harness PR with branching, commits, and documentation
version: 1.0.0
---

# Issue Orchestration Skill

Orchestrate the complete development workflow from a Jira issue to a merged Harness pull request.

## When to Activate

This skill activates when:
- User wants to implement a Jira issue
- User asks to create a branch/PR from an issue
- User wants to orchestrate development workflow
- User mentions working on a Jira ticket (e.g., "PROJ-123")
- User asks to automate issue-to-PR pipeline

## Orchestration Pipeline

### Phase 1: Issue Analysis

1. **Fetch Issue Details** via Atlassian MCP:
   ```
   mcp__atlassian__jira_get_issue(issue_key)
   ```

2. **Extract Key Information**:
   - Issue type (Story, Task, Bug, Epic)
   - Summary and description
   - Acceptance criteria
   - Priority and labels
   - Linked issues and dependencies
   - Assignee and reporter

3. **Assess Complexity**:
   - Simple: Single change, clear scope
   - Medium: Multiple files, some complexity
   - Complex: Requires subtasks, multiple components

### Phase 2: Planning

1. **Generate Branch Name**:
   ```
   Pattern: {type}/{issue-key}-{slug}
   Example: feature/PROJ-123-add-user-authentication
   ```

2. **Create Subtasks** (if complex):
   - Break down into implementation steps
   - Create subtasks in Jira via MCP
   - Link subtasks to parent issue

3. **Plan Commits**:
   - Map subtasks to commits
   - Define commit message format:
     ```
     {type}({scope}): {description}

     {body}

     Refs: {issue-key}
     ```

### Phase 3: Branch Creation

1. **Create Branch** via Harness API:
   ```
   POST /repos/{repo}/branches
   {
     "name": "feature/PROJ-123-description",
     "target": "main"
   }
   ```

2. **Update Jira Issue**:
   - Add branch link to issue
   - Transition to "In Progress"
   - Add comment with branch details

### Phase 4: Implementation

1. **For Each Subtask/Change**:
   - Make code changes
   - Create commit with proper message
   - Reference Jira issue in commit

2. **Commit Format**:
   ```
   feat(auth): implement user login endpoint

   - Add POST /api/auth/login endpoint
   - Implement JWT token generation
   - Add password validation

   Refs: PROJ-123
   Subtask: PROJ-124
   ```

3. **Push Changes** to Harness

### Phase 5: Pull Request

1. **Create PR** via Harness API:
   ```
   POST /repos/{repo}/pullreq
   {
     "title": "[PROJ-123] Add user authentication",
     "source_branch": "feature/PROJ-123-add-user-authentication",
     "target_branch": "main",
     "description": "..."
   }
   ```

2. **PR Description Template**:
   ```markdown
   ## Summary
   {issue_summary}

   ## Jira Issue
   [{issue_key}]({jira_url})

   ## Changes
   - {change_1}
   - {change_2}

   ## Testing
   - [ ] Unit tests added
   - [ ] Integration tests pass
   - [ ] Manual testing completed

   ## Documentation
   - [ ] README updated
   - [ ] API docs updated
   - [ ] Confluence page created
   ```

3. **Add Reviewers**:
   - Assign code owners
   - Request reviews via Harness API

### Phase 6: Documentation

1. **Generate Confluence Page** via Atlassian MCP:
   ```
   mcp__atlassian__confluence_create_page(space, title, content)
   ```

2. **Document Template**:
   - Feature overview
   - Technical implementation
   - API changes
   - Testing notes
   - Deployment considerations

3. **Link Documentation**:
   - Add Confluence link to Jira issue
   - Add Confluence link to PR description

### Phase 7: Review & Sync

1. **Trigger Agent Review**:
   - Invoke code-agent for implementation review
   - Invoke review-agent for quality check
   - Invoke doc-agent for documentation review

2. **Post Review Comments**:
   - Add findings to PR
   - Add summary to Jira issue

3. **Sync Status**:
   - Update Jira based on PR state
   - Track review progress

## MCP Tools Required

### Atlassian MCP
- `mcp__atlassian__jira_get_issue` - Fetch issue details
- `mcp__atlassian__jira_create_issue` - Create subtasks
- `mcp__atlassian__jira_update_issue` - Update issue fields
- `mcp__atlassian__jira_add_comment` - Add comments
- `mcp__atlassian__jira_transition` - Change issue status
- `mcp__atlassian__confluence_create_page` - Create docs
- `mcp__atlassian__confluence_update_page` - Update docs

### Harness MCP
- `mcp__harness__create_branch` - Create feature branch
- `mcp__harness__create_commit` - Commit changes
- `mcp__harness__create_pullreq` - Create PR
- `mcp__harness__add_reviewer` - Add PR reviewers
- `mcp__harness__add_comment` - Comment on PR
- `mcp__harness__get_pullreq` - Get PR status

## Status Mapping

| Jira Status | Harness PR State | Action |
|-------------|------------------|--------|
| To Do | - | Create branch |
| In Progress | Open | Active development |
| In Review | Open + Reviewers | Awaiting review |
| Done | Merged | Complete |
| Blocked | Open + Blocked label | Needs attention |

## Example Workflow

**User Input:**
> Implement PROJ-123

**Orchestration Steps:**

1. ✅ Fetched issue: "Add user authentication"
2. ✅ Complexity: Medium (3 components)
3. ✅ Created subtasks: PROJ-124, PROJ-125, PROJ-126
4. ✅ Created branch: feature/PROJ-123-add-user-authentication
5. ✅ Transitioned issue to "In Progress"
6. 🔄 Implementing subtask PROJ-124...
7. ✅ Committed: feat(auth): add login endpoint
8. ✅ Implementing subtask PROJ-125...
9. ✅ Committed: feat(auth): add JWT validation
10. ✅ Created PR #45
11. ✅ Added reviewers: @alice, @bob
12. ✅ Created Confluence page: "User Authentication Feature"
13. ✅ Triggered agent council review
14. ✅ All agents approved

**Result:**
PR #45 ready for human review. Jira issue updated with all links.
