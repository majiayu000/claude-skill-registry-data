---
name: Subtask Generation
description: Use when breaking down a Jira issue into development subtasks with implementation details
version: 1.0.0
---

# Subtask Generation Skill

Break down complex Jira issues into well-defined subtasks for structured development.

## When to Activate

This skill activates when:
- User asks to break down an issue into subtasks
- Issue is marked as complex (Epic, large Story)
- User wants to plan implementation steps
- Multiple team members will work on parts of an issue
- User asks for task decomposition

## Subtask Categories

### Development Subtasks

1. **Setup/Infrastructure**
   - Environment configuration
   - Dependency installation
   - Database migrations
   - Service configuration

2. **Backend Implementation**
   - API endpoints
   - Business logic
   - Data models
   - Service integrations

3. **Frontend Implementation**
   - UI components
   - State management
   - API integration
   - Styling/UX

4. **Testing**
   - Unit tests
   - Integration tests
   - E2E tests
   - Performance tests

5. **Documentation**
   - API documentation
   - README updates
   - Confluence pages
   - Code comments

6. **Review/QA**
   - Code review
   - QA testing
   - Security review
   - Accessibility review

## Subtask Templates

### Feature Implementation
```
Parent: [PROJ-100] Implement user authentication

Subtasks:
├── [PROJ-101] Set up authentication middleware
│   Type: Task
│   Estimate: 2h
│   Description: Configure JWT middleware and auth routes
│
├── [PROJ-102] Implement login endpoint
│   Type: Task
│   Estimate: 3h
│   Description: POST /api/auth/login with validation
│
├── [PROJ-103] Implement registration endpoint
│   Type: Task
│   Estimate: 3h
│   Description: POST /api/auth/register with email verification
│
├── [PROJ-104] Add password reset flow
│   Type: Task
│   Estimate: 4h
│   Description: Forgot password and reset endpoints
│
├── [PROJ-105] Write unit tests for auth module
│   Type: Task
│   Estimate: 2h
│   Description: Test coverage for all auth functions
│
├── [PROJ-106] Update API documentation
│   Type: Task
│   Estimate: 1h
│   Description: OpenAPI spec and README updates
│
└── [PROJ-107] Security review
    Type: Task
    Estimate: 2h
    Description: Review auth implementation for vulnerabilities
```

### Bug Fix
```
Parent: [PROJ-200] Fix login timeout issue

Subtasks:
├── [PROJ-201] Investigate root cause
│   Type: Task
│   Estimate: 1h
│   Description: Analyze logs and reproduce issue
│
├── [PROJ-202] Implement fix
│   Type: Task
│   Estimate: 2h
│   Description: Apply fix based on investigation
│
├── [PROJ-203] Add regression test
│   Type: Task
│   Estimate: 1h
│   Description: Test to prevent future recurrence
│
└── [PROJ-204] Verify in staging
    Type: Task
    Estimate: 30m
    Description: Deploy and verify fix in staging environment
```

## Generation Process

### Step 1: Analyze Parent Issue

Extract from the parent issue:
- **Scope**: What needs to be done
- **Components**: Which parts of the system are affected
- **Acceptance Criteria**: What defines "done"
- **Technical Requirements**: Any specific tech constraints

### Step 2: Identify Work Streams

Categorize the work:
```
┌─────────────────────────────────────────────────────────────┐
│                      Parent Issue                            │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │  Setup   │  │ Backend  │  │ Frontend │  │  Testing │    │
│  │  Tasks   │  │  Tasks   │  │  Tasks   │  │  Tasks   │    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### Step 3: Create Subtasks

For each subtask, define:

```json
{
  "project": "PROJ",
  "parent": "PROJ-100",
  "issuetype": "Sub-task",
  "summary": "Implement login endpoint",
  "description": "Create POST /api/auth/login endpoint\n\n## Requirements\n- Accept email and password\n- Validate credentials\n- Return JWT token\n- Handle errors gracefully\n\n## Acceptance Criteria\n- [ ] Endpoint returns 200 with valid credentials\n- [ ] Returns 401 for invalid credentials\n- [ ] Rate limiting applied\n- [ ] Logs authentication attempts",
  "labels": ["backend", "auth"],
  "timetracking": {
    "originalEstimate": "3h"
  }
}
```

### Step 4: Create via MCP

```
mcp__atlassian__jira_create_issue({
  project: "PROJ",
  parent: "PROJ-100",
  issuetype: "Sub-task",
  summary: "Implement login endpoint",
  description: "...",
  labels: ["backend", "auth"]
})
```

### Step 5: Link and Organize

1. **Set Dependencies**: Link subtasks that depend on each other
2. **Assign Order**: Set execution order in description
3. **Add to Sprint**: If parent is in sprint, add subtasks
4. **Notify Team**: Comment on parent with subtask breakdown

## Estimation Guidelines

| Complexity | Time Range | Characteristics |
|------------|------------|-----------------|
| Simple | 30m - 1h | Single file, clear change |
| Medium | 1h - 3h | Multiple files, some logic |
| Complex | 3h - 8h | Multiple components, testing |
| Large | 8h+ | Should be broken down further |

## Output Format

When generating subtasks, present:

```
📋 Subtask Breakdown for PROJ-100

Total Subtasks: 7
Estimated Total: 17.5 hours

┌─────────────┬──────────────────────────────────┬──────────┬─────────┐
│ Key         │ Summary                          │ Estimate │ Labels  │
├─────────────┼──────────────────────────────────┼──────────┼─────────┤
│ PROJ-101    │ Set up authentication middleware │ 2h       │ backend │
│ PROJ-102    │ Implement login endpoint         │ 3h       │ backend │
│ PROJ-103    │ Implement registration endpoint  │ 3h       │ backend │
│ PROJ-104    │ Add password reset flow          │ 4h       │ backend │
│ PROJ-105    │ Write unit tests                 │ 2h       │ testing │
│ PROJ-106    │ Update API documentation         │ 1h       │ docs    │
│ PROJ-107    │ Security review                  │ 2h       │ review  │
└─────────────┴──────────────────────────────────┴──────────┴─────────┘

Dependencies:
  PROJ-102 → depends on → PROJ-101
  PROJ-103 → depends on → PROJ-101
  PROJ-104 → depends on → PROJ-102, PROJ-103
  PROJ-105 → depends on → PROJ-102, PROJ-103, PROJ-104
  PROJ-107 → depends on → PROJ-102, PROJ-103, PROJ-104

Create these subtasks? [Y/n]
```

## Best Practices

1. **Right-Size Subtasks**: 1-4 hours ideal, max 8 hours
2. **Clear Acceptance Criteria**: Each subtask has clear "done" definition
3. **Independent When Possible**: Minimize dependencies
4. **Include Testing**: Always include test subtasks
5. **Documentation**: Include doc updates as subtasks
6. **Review**: Include review/QA subtasks
