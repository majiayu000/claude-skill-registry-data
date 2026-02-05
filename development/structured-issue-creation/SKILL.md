---
name: Structured Issue Creation
description: Create well-structured Jira issues from code changes, conversations, or requirements. Use when creating issues, bugs, stories, tasks, or when the user wants to track work in Jira. Analyzes context to generate clear titles, descriptions, and appropriate fields.
allowed-tools: Read, Grep, Bash
---

# Structured Issue Creation

Expert assistance for creating well-structured, comprehensive Jira issues from any context.

## When to Use This Skill

- User wants to create a Jira issue
- User mentions tracking work, bugs, features, or tasks
- After implementing code that should be tracked
- When discussing a problem that should be documented
- User asks to "open a ticket" or "create an issue"

## Issue Types and When to Use Them

### 🐛 Bug
**When to use**: Something is broken or not working as expected

**Required information**:
- What's broken?
- How to reproduce?
- Expected vs actual behavior
- Environment details

### 📖 Story
**When to use**: User-facing feature or capability

**Required information**:
- User persona
- What they want to do
- Why they want it (business value)
- Acceptance criteria

### ✓ Task
**When to use**: Work that doesn't fit other types (refactoring, documentation, DevOps)

**Required information**:
- What needs to be done?
- Why it's needed
- Definition of done

### 🎯 Epic
**When to use**: Large body of work that contains multiple stories

**Required information**:
- High-level goal
- Scope boundaries
- Success metrics

## Issue Structure Template

### Title (Summary)
- **Format**: `[Type] Brief, clear description`
- **Length**: < 60 characters
- **Examples**:
  - `User login fails with special characters`
  - `Add dark mode toggle to settings`
  - `Refactor authentication module for testability`

### Description

#### For Bugs
```markdown
## Problem
Brief description of what's broken.

## Steps to Reproduce
1. Go to login page
2. Enter email with + character
3. Click submit

## Expected Behavior
User should be able to login with any valid email.

## Actual Behavior
Error: "Invalid email format"

## Environment
- Browser: Chrome 120
- OS: macOS 14
- Version: v2.3.1

## Screenshots/Logs
[Attach if available]

## Impact
Who is affected and how severely?

## Suggested Fix
[Optional] Potential solution or workaround
```

#### For Stories
```markdown
## User Story
As a [user type]
I want [goal]
So that [benefit]

## Background/Context
Why we're building this feature.

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Design/Mockups
[Link to designs if available]

## Technical Notes
- API changes needed
- Database changes
- Third-party integrations

## Out of Scope
What we're NOT doing in this story.
```

#### For Tasks
```markdown
## Objective
What needs to be accomplished.

## Context
Why this work is needed.

## Implementation Details
- Step 1
- Step 2
- Step 3

## Definition of Done
- [ ] Code complete
- [ ] Tests added
- [ ] Documentation updated
- [ ] Reviewed and merged
```

## Priority Guidelines

### 🔴 Highest (P1)
- Production outages
- Security vulnerabilities
- Data loss scenarios
- Blocking other work

### 🟠 High (P2)
- Significant bugs affecting many users
- Important features with deadlines
- Performance issues

### 🟡 Medium (P3)
- Minor bugs
- Feature enhancements
- Technical debt

### 🟢 Low (P4)
- Nice-to-have features
- Minor improvements
- Cosmetic issues

## Labels Best Practices

### Functional Labels
- `frontend`, `backend`, `api`, `database`
- `mobile`, `web`, `desktop`

### Technical Labels
- `performance`, `security`, `accessibility`
- `technical-debt`, `refactoring`

### Process Labels
- `needs-design`, `needs-review`, `blocked`
- `good-first-issue`, `help-wanted`

### Business Labels
- `customer-request`, `urgent`, `quick-win`

## Creating Issues from Code Context

When creating an issue based on code I've written or changes I've detected:

1. **Analyze the change**:
   - What was added/modified?
   - What problem does it solve?
   - What testing is needed?

2. **Determine issue type**:
   - Bug fix? → Bug
   - New feature? → Story or Task
   - Refactoring? → Task

3. **Extract details**:
   - Use file names for context
   - Include code snippets in description
   - Link to related files

4. **Generate structured content**:
   - Clear, descriptive title
   - Complete description with context
   - Appropriate labels and priority

## Example: Creating Issue from Code

**Context**: I just helped implement user authentication

**Analysis**:
- New feature added: OAuth integration
- Files modified: auth.js, login.js, config.js
- Tests added: auth.test.js

**Generated Issue**:

**Title**: `Implement OAuth 2.0 authentication for user login`

**Type**: Story

**Description**:
```markdown
## User Story
As a user
I want to login using OAuth providers (Google, GitHub)
So that I don't need to create another password

## Implementation Details
Added OAuth 2.0 authentication with the following changes:

**Modified Files**:
- `src/auth/auth.js` - OAuth client integration
- `src/components/login.js` - OAuth login buttons
- `src/config/config.js` - OAuth app credentials

**Tests**:
- `tests/auth.test.js` - OAuth flow tests

## Acceptance Criteria
- [x] Google OAuth integration working
- [x] GitHub OAuth integration working
- [x] Error handling for failed OAuth
- [x] Tests added and passing
- [ ] Documentation updated
- [ ] Security review completed

## Security Considerations
- OAuth credentials stored in environment variables
- PKCE flow used for enhanced security
- Token refresh logic implemented

## Next Steps
- Update user documentation
- Security team review
- Deploy to staging for testing
```

**Labels**: `backend`, `authentication`, `security`, `needs-review`

**Priority**: High

## Creating Issues from Conversations

When creating an issue from a discussion:

1. **Identify the core request**: What does the user actually want?
2. **Ask clarifying questions** if needed:
   - "Is this a bug or a new feature?"
   - "How urgent is this?"
   - "Who is affected?"
   - "Any specific requirements?"

3. **Structure the information**: Use appropriate template
4. **Confirm with user**: Show them the issue before creating

## Linking Related Work

When creating issues, consider:

### Parent/Child Relationships
- Epic → contains → Stories
- Story → contains → Subtasks

### Issue Links
- **Blocks**: This issue prevents progress on another
- **Is blocked by**: Cannot proceed until another is done
- **Relates to**: General relationship
- **Duplicates**: Same as another issue
- **Causes**: This issue causes another problem

### Example
```
Epic: User Authentication System
├─ Story: Implement OAuth login
│  ├─ Task: Add Google OAuth
│  ├─ Task: Add GitHub OAuth
│  └─ Task: Update login UI
├─ Story: Add password reset flow
└─ Story: Implement 2FA
```

## Quality Checklist

Before creating an issue, verify:

- [ ] **Title is clear**: Someone unfamiliar with context understands
- [ ] **Description is complete**: All necessary information included
- [ ] **Type is correct**: Bug/Story/Task/Epic appropriate
- [ ] **Priority is set**: Based on impact and urgency
- [ ] **Labels added**: For filtering and organization
- [ ] **Assignee considered**: Should someone be assigned now?
- [ ] **Linked issues**: Related work connected
- [ ] **Acceptance criteria**: Clear definition of done

## Common Mistakes to Avoid

### ❌ Vague Titles
"Fix login" → "User login fails with OAuth when email contains + character"

### ❌ Missing Context
"Implement feature" → Include user story, requirements, acceptance criteria

### ❌ No Acceptance Criteria
Add clear, testable conditions for completion

### ❌ Wrong Issue Type
Refactoring as Bug → Should be Task

### ❌ Missing Priority
Always set priority based on impact

### ❌ Kitchen Sink Issues
One issue = one logical unit of work. Split large work into multiple issues.

## Workflow Integration

### After Writing Code
```
Me: "I've implemented the user profile feature. Should I create a Jira issue to track this?"

You: "Yes, create a story"

Me: [Analyzes code] "I'll create a story with:
- Title: 'Implement user profile with avatar upload'
- Description includes implementation details from the code
- Acceptance criteria based on what was built
- Labels: frontend, backend, user-management
- Priority: Medium

Create this issue?"
```

### From Bug Reports
```
You: "Users report that the app crashes when uploading large files"

Me: "I'll create a bug issue:

## Title
App crashes when uploading files > 10MB

## Description
[Structured bug template with all details]

Should I also search for similar issues first to avoid duplicates?"
```

## Advanced Features

### Issue Templates
If your Jira project has custom templates, I can:
- Use project-specific fields
- Follow your team's conventions
- Match your existing issue style

### Bulk Creation
Create multiple related issues at once:
```
You: "Create issues for the payment integration epic"

Me: "I'll create:
1. Epic: Payment Integration
2. Story: Stripe API integration
3. Story: Payment form UI
4. Story: Transaction history
5. Task: Payment testing in sandbox

Proceed with all 5 issues?"
```

## How I'll Help

When you need to create an issue, I will:

1. **Gather context**: Understand what you want to track
2. **Determine type**: Bug, Story, Task, or Epic?
3. **Structure content**: Use appropriate template
4. **Add metadata**: Priority, labels, relationships
5. **Show preview**: Let you review before creating
6. **Create issue**: Use `/jira-create` command
7. **Follow up**: Suggest next actions (assign, link, transition)

## Example Interaction

**You**: "The authentication module I just wrote should be tracked"

**Me**: "I'll create a story for this. Let me analyze what you built...

**Proposed Issue:**

**Title**: Implement OAuth 2.0 authentication system

**Type**: Story

**Priority**: High

**Description**:
[Complete structured description with code context]

**Labels**: backend, authentication, security

Does this look good? Should I create it?"

**You**: "Yes"

**Me**: [Uses `/jira-create`] "Created PROJ-456: Implement OAuth 2.0 authentication system. Would you like me to add it to your current sprint?"
