---
name: requirements-engineering
description: Transform ideas into actionable specifications through structured requirements capture, user story creation, and scope definition. Use for product ideation sessions, writing user stories with acceptance criteria, defining MVP scope, prioritizing features (MoSCoW/RICE), creating PRDs, and turning vague concepts into implementable specifications.
---

# Requirements Engineering

Capture, structure, and refine product ideas into implementable specifications.

## Idea Capture Process

### 1. Problem Statement
Start every feature with the problem, not the solution:
```
PROBLEM: [What pain point exists?]
WHO: [Who experiences this?]
IMPACT: [What happens if unsolved?]
```

### 2. Solution Exploration
```
PROPOSED SOLUTION: [High-level approach]
ALTERNATIVES CONSIDERED: [Other options]
WHY THIS APPROACH: [Decision rationale]
```

### 3. Success Criteria
Define measurable outcomes before building:
- What does "done" look like?
- How will we know it's working?
- What metrics indicate success?

## User Story Format

### Standard Template
```
AS A [user type]
I WANT TO [action/goal]
SO THAT [benefit/value]

ACCEPTANCE CRITERIA:
- GIVEN [context] WHEN [action] THEN [outcome]
- GIVEN [context] WHEN [action] THEN [outcome]
```

### Example
```
AS A registered user
I WANT TO reset my password via email
SO THAT I can regain access when I forget my credentials

ACCEPTANCE CRITERIA:
- GIVEN a valid email, WHEN I request reset, THEN I receive a link within 2 minutes
- GIVEN a reset link, WHEN I click it after 24 hours, THEN it shows expired
- GIVEN a valid reset link, WHEN I submit a new password, THEN I can log in immediately
```

### Story Quality Checklist
- [ ] Independent (can be built separately)
- [ ] Negotiable (not overly prescriptive)
- [ ] Valuable (delivers user/business value)
- [ ] Estimable (can assess complexity)
- [ ] Small (fits in one iteration)
- [ ] Testable (clear pass/fail criteria)

## Prioritization Frameworks

### MoSCoW Method
| Category | Definition | Rule |
|----------|------------|------|
| **Must** | Critical for launch, non-negotiable | ~60% of effort |
| **Should** | Important but not critical | ~20% of effort |
| **Could** | Nice-to-have enhancements | ~20% of effort |
| **Won't** | Explicitly out of scope (this time) | Document for later |

### RICE Scoring
```
RICE Score = (Reach × Impact × Confidence) / Effort

Reach: Users affected per quarter (number)
Impact: 3=massive, 2=high, 1=medium, 0.5=low, 0.25=minimal
Confidence: 100%=high, 80%=medium, 50%=low
Effort: Person-weeks (or points)
```

### Priority Matrix (Quick)
```
         High Impact    Low Impact
Low      ┌─────────────┬───────────┐
Effort   │  DO FIRST   │  FILL-IN  │
         ├─────────────┼───────────┤
High     │  SCHEDULE   │   DROP    │
Effort   └─────────────┴───────────┘
```

## MVP Scoping

### MVP Definition Questions
1. What is the smallest thing that proves/disproves our hypothesis?
2. What's the core value proposition?
3. What can users NOT do without?
4. What would we be embarrassed to ship without?

### Scope Reduction Techniques
- **Time-box**: "What can we ship in 2 weeks?"
- **User-limit**: "What do our first 10 users need?"
- **Feature-limit**: "If we could only ship 3 features..."
- **Manual-first**: "What can we do manually before automating?"

### MVP vs V1 Distinction
```
MVP: Validates the core assumption
- Minimum features to test hypothesis
- May use manual processes
- Focused on learning

V1: First real product
- Complete core workflows
- Production-ready quality
- Focused on delivering value
```

## Requirements Document Template

```markdown
# [Feature/Product Name]

## Overview
One paragraph explaining what this is and why it matters.

## Problem Statement
- Who has this problem?
- What is the current pain?
- What's the cost of not solving it?

## Proposed Solution
High-level description of the approach.

## User Stories
[List stories with acceptance criteria]

## Scope

### In Scope (MVP)
- [Must-have 1]
- [Must-have 2]

### In Scope (V1)
- [Should-have 1]
- [Could-have 1]

### Out of Scope
- [Won't-have with rationale]

## Open Questions
- [Unresolved decision 1]
- [Unresolved decision 2]

## Dependencies
- [External dependency or blocker]

## Success Metrics
- [Measurable outcome 1]
- [Measurable outcome 2]
```

## Refinement Checklist

Before considering requirements "ready":
- [ ] Problem clearly articulated
- [ ] Target user identified
- [ ] Acceptance criteria defined
- [ ] Edge cases considered
- [ ] Scope boundaries explicit
- [ ] Dependencies identified
- [ ] Success metrics defined
- [ ] Technical feasibility validated
