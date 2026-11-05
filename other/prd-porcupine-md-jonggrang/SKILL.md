---
name: prd
description: Generate Product Requirements Document from feature intent/description
type: generate
project_types: [web-app, api, library, cli, tui]
trigger: "create PRD, generate requirements, write specification"
inputs:
  - name: feature
    description: Feature description or intent to be built
    required: true
  - name: audience
    description: Target user/audience for this feature
    required: false
    default: "end users"
---

## Context

You are a product analyst creating a PRD for project {{project_name}} ({{project_type}}).
Stack used: {{stack}}.

This PRD will be used as input for the Jonggrang development workflow, where each user story will become one atomic task handled by an AI agent in a single iteration.

## Instructions

1. Analyze the given feature intent/description: "{{input.feature}}"

2. Create a PRD with the following structure:
   - **Overview**: Feature summary in 2-3 sentences
   - **Problem Statement**: What problem this solves
   - **User Stories**: List of user stories in the format "As a [role], I want [action], so that [benefit]"
   - **Acceptance Criteria**: Per user story, what must be true for it to be considered complete
   - **Technical Notes**: Technical considerations, dependencies, constraints
   - **Out of Scope**: What is NOT included in this feature

3. Ensure each user story:
   - Is small enough to be completed in 1 context window (~30 minutes of agent work)
   - Has testable acceptance criteria
   - Does not overlap file ownership with other stories (if possible)
   - Has a clear priority (1 = highest)

4. Save the PRD to `tasks/prd-{{input.feature | slugify}}.md`

5. Ask the user whether the PRD is acceptable or needs revision

6. After approval, convert to `.jonggrang/jonggrang-tasks.json` format:

## Script

```bash
#!/bin/bash
# Create tasks directory if not exists
mkdir -p tasks
```

## Validation

- [ ] PRD file saved in `tasks/prd-*.md`
- [ ] Each user story has acceptance criteria
- [ ] Each story is sufficiently atomic (completable in 1 iteration)
- [ ] Priorities assigned to all stories
- [ ] .jonggrang/jonggrang-tasks.json updated with new tasks

## Examples

### Input
```
feature: "User authentication with email and social login"
```

### Output PRD (excerpt)
```markdown
# PRD: User Authentication

## Overview
Implement user authentication system supporting email/password
and social login (Google, GitHub) with session management.

## User Stories

### Story 1: Email Registration (Priority: 1)
As a new user, I want to register with my email and password,
so that I can create an account.

Acceptance Criteria:
- POST /api/auth/register accepts email + password
- Email validated (format + uniqueness)
- Password hashed with bcrypt (min 8 chars)
- Returns JWT token on success
- Returns 422 on validation error
- Tests: happy path, duplicate email, weak password

Files: src/routes/auth.ts, src/services/auth.ts, tests/auth.test.ts
```
