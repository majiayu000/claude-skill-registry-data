---
name: work-items
description: Optimize and analyze work items for LLM-assisted development
when_to_use: |
  Use this skill when the user:
  - Pastes a work item, issue, or ticket from any system
  - Asks about work item readiness or completeness
  - Needs to break down a feature into implementation tasks
  - Wants to optimize content for LLM context windows
---

# Work Items Skill

Apply these patterns when working with issues, tickets, or work items from any system (GitHub Issues, Jira, Azure DevOps, Linear, etc.).

## LLM Optimization Patterns

### File Path Compression
Use glob patterns to compress multiple file paths:

| Before | After |
|--------|-------|
| `routes/dev-routes.bicep`, `routes/test-routes.bicep`, `routes/prod-routes.bicep` | `routes/{dev,test,prod}-routes.bicep` |
| `src/components/Button.tsx`, `src/components/Input.tsx` | `src/components/{Button,Input}.tsx` |

### Terse Language Rules
- No articles ("the", "a") unless needed for clarity
- No filler phrases ("In order to", "This will")
- Use arrows for transformations: `external -> internal`, `HTTP -> HTTPS`
- Use equals for settings: `ingress.external = false`

### Output Structure
Optimize work items into this token-efficient format:

```markdown
# {ID}: {title}

## Context
{1-2 sentence summary}

## Files
- {file paths with glob patterns}

## Changes
1. {file}: {action}

## Verify
- {non-obvious verification step}
```

### Acceptance Criteria Filtering
**Remove** obvious/implicit criteria:
- "Deployment succeeds"
- "No downtime"
- "Tests pass"
- "Code reviewed"
- "PR merged"

**Keep** non-obvious verification:
- Specific HTTP status codes
- Portal/UI status checks
- Security constraints
- Integration behaviors

## Task Breakdown Rules

### Granularity
- 1 task = 1 logical change that can be committed independently
- Each task: ~5-30 min of work
- Group related file changes if they must be atomic

### Sequencing
1. Infrastructure/Config first (env vars, config files, dependencies)
2. Core changes second (main logic, modules)
3. Dependent files third (routes, integrations, consumers)
4. Verification last (manual checks, cleanup)

### Task Format
```markdown
## Task {n}: {brief title}

**Files**: {file(s) to modify}

**Do**:
- {specific action}

**Test**:
- {how to verify}
```

## Completeness Criteria

### Title
- Descriptive (> 5 words typically)
- Clearly indicates what feature/change is needed
- Avoids vague terms: "fix bug", "update code", "improvements"

### Description
- Exists and is not empty
- Explains **what** needs to be done
- Explains **why** it's needed (business value/context)
- Provides enough context for a developer to understand scope

### Acceptance Criteria
- Present and populated
- Contains specific, testable conditions
- Uses clear language (Given/When/Then or bullet points)
- Defines what "done" looks like
