---
name: "Requirements Engineering"
description: "Translate user prompts into structured requirements, user stories, and beads tasks. Use when: (1) Parsing user feature requests, (2) Creating acceptance criteria, (3) Breaking down epics into tasks, (4) Auto-generating beads issues. Trigger keywords: requirements, user story, acceptance criteria, as a, i want, so that, given when then, task breakdown, epic creation"
version: 1.1.0
---

# Requirements Engineering

Translate natural language prompts into structured requirements and tasks.

## Requirements Format Decision Tree

```
What format is the user using?
│
├─ "As a... I want... So that..."
│   └─ User Story format → Extract actor, feature, benefit
│
├─ "Given... When... Then..."
│   └─ BDD format → Extract precondition, action, outcome
│
├─ "Add/Implement/Build X with Y"
│   └─ Feature request → Extract action, components, technology
│
├─ "Fix/Debug X"
│   └─ Bug report → Route to debug workflow
│
└─ "Refactor/Optimize X"
    └─ Refactoring → Route to refactor workflow
```

---

## NEVER Do This

**NEVER** accept vague requirements:
```
# BAD - Too vague, can't test
"Add payment saving"
"Make authentication work"

# GOOD - Specific, testable
"User can save credit card with last 4 digits displayed"
"User receives JWT token on successful email/password login"
```

**NEVER** create broad acceptance criteria:
```
# BAD - Not testable
- [ ] Payment should work
- [ ] Authentication is secure

# GOOD - Specific and verifiable
- [ ] Card is validated before saving
- [ ] Card number shows only last 4 digits in UI
- [ ] Access token expires in 15 minutes
```

**NEVER** skip task dependencies:
```
# BAD - Missing dependencies
PAY-005: Payment service (no deps listed)

# GOOD - Explicit dependencies
PAY-005: Payment service
└─ Dependencies: PAY-002 (payments table), PAY-004 (Payment model)
```

---

## User Story Template

```
As a [actor/role]
I want [feature/capability]
So that [business benefit/value]
```

**Example**:
```markdown
## User Story

**As a** customer
**I want** to save my payment method
**So that** I can checkout faster on future purchases

## Acceptance Criteria

- [ ] User can add credit card
- [ ] Card is validated before saving
- [ ] Card number masked (only last 4 digits)
- [ ] Saved cards appear in checkout dropdown
```

---

## BDD Acceptance Criteria

```
Given [initial context/precondition]
When [action/event occurs]
Then [expected outcome/result]
```

**Example**:
```markdown
**Given** a registered user
**When** they enter valid credentials
**Then** they receive a JWT access token
**And** the access token expires in 15 minutes
```

---

## Task Breakdown Template

Break features into Rails technical layers:

| Layer | Example Tasks |
|-------|---------------|
| Database | Migrations, schema changes |
| Model | ActiveRecord, validations, associations |
| Service | Business logic, external APIs |
| Controller | HTTP endpoints, routing |
| View/Component | UI, Hotwire, ViewComponents |
| Testing | RSpec tests for each layer |

### Dependency Flow

```
Database → Models → Services → Controllers → Views → Tests
```

---

## Action Verb → Intent Mapping

| Verb | Intent | Workflow |
|------|--------|----------|
| Implement/Build/Create | New Feature | `/reactree-dev` |
| Add/Include | Enhancement | `/reactree-feature` |
| Fix/Debug | Bug Fix | `/reactree-debug` |
| Refactor/Cleanup | Refactoring | `/reactree-refactor` |
| Optimize/Improve | Performance | `/reactree-dev --refactor` |

---

## Quick Extraction Patterns

```bash
# Actor: "As a/an X"
ACTOR=$(echo "$prompt" | grep -ioE "as an? [a-z ]+" | sed 's/as an? //')

# Feature: "I want X"
FEATURE=$(echo "$prompt" | grep -ioE "i want [^.]*" | sed 's/i want //')

# Benefit: "So that X"
BENEFIT=$(echo "$prompt" | grep -ioE "so that [^.]*" | sed 's/so that //')

# Components: "with X and Y"
COMPONENTS=$(echo "$prompt" | grep -ioE "with [a-z, and]+" | sed 's/with //')

# Technology: "using Z"
TECH=$(echo "$prompt" | grep -ioE "using [a-z ]+" | sed 's/using //')
```

---

## Complexity Scoring

| Word Count | Complexity | Components | Action |
|------------|------------|------------|--------|
| < 10 | Low | 1-2 | Simple task, no epic |
| 10-20 | Medium | 2-3 | Feature, create tasks |
| > 20 | High | 4+ | Epic with subtasks |

---

## Beads Task Creation

For complex features, auto-create beads structure:

```bash
# Create epic
EPIC_ID=$(bd create --type epic --title "$FEATURE_TITLE")

# Create subtasks with dependencies
bd create --type task --title "Add schema" --deps "$EPIC_ID"
bd create --type task --title "Add models" --deps "$EPIC_ID,$SCHEMA_TASK"
bd create --type task --title "Add services" --deps "$MODEL_TASK"
```

---

## Output Checklist

Before implementation, verify:

- [ ] User story has actor, feature, benefit (if applicable)
- [ ] Acceptance criteria are specific and testable
- [ ] Technical components identified
- [ ] Task breakdown follows layer strategy
- [ ] Dependencies explicitly stated
- [ ] Beads epic created (for complex features)

---

## References

Detailed patterns and scripts in `references/`:
- `formats-and-patterns.md` - Extraction logic, intent classification
- `task-breakdown.md` - Layer strategy, dependency detection, examples
- `beads-integration.md` - Auto task creation, workflow routing
