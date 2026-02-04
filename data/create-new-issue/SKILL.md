---
name: create-new-issue
description: For use when a new issue/task has been identified and needs to be formally captured using the Wrangler MCP issue management system. Use this skill to create new issues via the issues_create MCP tool with appropriate metadata and structured content.
---

You are a specialist at taking details about a newly identified issue or outstanding task and converting that information into a well-structured issue using the Wrangler MCP issue management tools.

## Core Responsibilities

## Skill Usage Announcement

**MANDATORY**: When using this skill, announce it at the start with:

```
🔧 Using Skill: create-new-issue | [brief purpose based on context]
```

**Example:**
```
🔧 Using Skill: create-new-issue | [Provide context-specific example of what you're doing]
```

This creates an audit trail showing which skills were applied during the session.



- Analyze the provided issue details to identify key information
- Use the **issues_create** MCP tool to create the issue with proper metadata
- Structure the description field according to issue type (bug vs task)
- Populate all relevant fields: title, description, type, status, priority, labels, assignee, project, wranglerContext
- Verify the issue was created successfully

## Issue Creation Process

### 1. Determine Issue Type

**For bugs:**
- Set `type: "issue"`
- Set `labels: ["bug"]` (plus any other relevant labels)
- Structure description with: Summary (what's broken, impact, current vs. expected behavior), Reproduction Steps, Environment, Root Cause Analysis, Solutions Attempted, Diagnostics, References
- See template: [BUG_ISSUE_TEMPLATE.md](templates/BUG_ISSUE_TEMPLATE.md)

**For tasks:**
- Set `type: "issue"`
- Set `labels: ["task"]` (plus any other relevant labels)
- Structure description with: Description, Objective (goal, value, scope), Requirements (functional, non-functional, dependencies), Tasks (implementation checklist), Testing Requirements, Acceptance Criteria, Implementation Notes, References
- See template: [TASK_ISSUE_TEMPLATE.md](templates/TASK_ISSUE_TEMPLATE.md)

**For feature requests:**
- Set `type: "issue"`
- Set `labels: ["feature", "enhancement"]` (plus any other relevant labels)
- Structure description with: Feature Description (what, why, who), User Story, Current vs. Proposed Behavior, User Experience, Requirements (must/should/nice-to-have), Success Metrics, Design Considerations, Open Questions, References
- See template: [FEATURE_REQUEST_TEMPLATE.md](templates/FEATURE_REQUEST_TEMPLATE.md)

**For specifications:**
- Set `type: "specification"`
- Structure description with: Executive Summary, Goals and Non-Goals, Background & Context, Requirements, Architecture, Implementation Details, Security, Error Handling, Observability, Testing Strategy, Deployment, Performance, Risks, Success Criteria, Timeline, References
- See template: [SPECIFICATION_TEMPLATE.md](../writing-specifications/templates/SPECIFICATION_TEMPLATE.md)
- **Note:** For complex specifications, use the dedicated [writing-specifications](../writing-specifications/SKILL.md) skill which provides comprehensive guidance and process

### 2. Use the issues_create Tool

Call the `issues_create` MCP tool with all relevant parameters:

```javascript
issues_create({
  title: "Clear, concise title",
  description: "Detailed description with appropriate sections based on type",
  type: "issue" | "specification",
  status: "open" | "in_progress" | "closed" | "cancelled",
  priority: "low" | "medium" | "high" | "critical",
  labels: ["bug", "backend", ...],
  assignee: "username",
  project: "project-name",
  wranglerContext: {
    agentId: "agent-identifier",
    parentTaskId: "parent-issue-id",
    estimatedEffort: "2 days"
  }
})
```

### 3. Required vs Optional Fields

**Required:**
- `title` - Clear, concise issue title (max 200 chars)
- `description` - Detailed description with structured sections

**Optional but recommended:**
- `type` - Defaults to "issue"
- `status` - Defaults to "open"
- `priority` - Defaults to "medium"
- `labels` - Array of tags for categorization
- `assignee` - Who's responsible
- `project` - Project/epic association
- `wranglerContext` - Workflow metadata (agentId, parentTaskId, estimatedEffort)

## Template Reference

You can reference the template files for structure guidance:
- **Bug issues**: [BUG_ISSUE_TEMPLATE.md](templates/BUG_ISSUE_TEMPLATE.md) - Comprehensive bug reporting with RCA, environment, diagnostics
- **Task issues**: [TASK_ISSUE_TEMPLATE.md](templates/TASK_ISSUE_TEMPLATE.md) - Implementation tasks with requirements, checklist, acceptance criteria
- **Feature requests**: [FEATURE_REQUEST_TEMPLATE.md](templates/FEATURE_REQUEST_TEMPLATE.md) - User-facing features with user stories, UX details, success metrics

**Important:** These templates show the frontmatter structure and content sections. Use them as a guide for formatting the `description` field when calling `issues_create`, but always use the MCP tool rather than manually creating files.

**For specifications**, use the dedicated [writing-specifications](../writing-specifications/SKILL.md) skill which has its own template and comprehensive process guidance.

## Example Usage

### Creating a Bug Issue

```javascript
issues_create({
  title: "API returns 500 error on user login",
  description: `## Summary

Authentication endpoint fails with 500 error when username contains special characters.

## Issue Reproduction Steps

1. Navigate to /api/auth/login
2. POST with username containing '@' symbol
3. Observe 500 error response

## Solutions Attempted

- Validated input sanitization (not the issue)
- Checked database constraints (no violations)

## Available Diagnostics

Error logs show: "Invalid character in username field"
Stack trace available in logs/api-2025-11-17.log

## References

### Key Files
- src/api/auth/login.ts
- src/validators/username.ts`,
  type: "issue",
  status: "open",
  priority: "high",
  labels: ["bug", "api", "auth"],
  project: "v1.2"
})
```

### Creating a Task Issue

```javascript
issues_create({
  title: "Implement password reset flow",
  description: `## Objective

Add password reset functionality for users who forget their credentials.

## Requirements

- Email-based reset link with expiration
- Secure token generation
- Password strength validation
- Rate limiting to prevent abuse

## Implementation Steps

1. Create password reset API endpoint
2. Implement email service integration
3. Add reset token storage and validation
4. Build password reset UI
5. Add rate limiting middleware

## Testing Requirements

- Unit tests for token generation/validation
- Integration tests for email flow
- E2E tests for complete user journey

## Acceptance Criteria

- [ ] User can request reset via email
- [ ] Reset link expires after 1 hour
- [ ] New password meets strength requirements
- [ ] Rate limiting prevents abuse (max 3 requests/hour)`,
  type: "issue",
  status: "open",
  priority: "medium",
  labels: ["task", "feature", "auth"],
  assignee: "backend-team",
  project: "v1.2",
  wranglerContext: {
    agentId: "implementation-agent",
    estimatedEffort: "3 days"
  }
})
```

## Important Notes

- **Always use the MCP tool** - Don't manually create markdown files; use `issues_create`
- **Auto-generated IDs** - The system assigns sequential IDs (000001, 000002, etc.)
- **Timestamps are automatic** - createdAt and updatedAt are set automatically
- **Files stored at project root** - Issues saved to `issues/`, specs to `specifications/`
- **Markdown format** - Files are stored as markdown with YAML frontmatter for git-friendliness
