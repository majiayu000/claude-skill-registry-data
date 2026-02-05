---
name: writing-user-stories
description: Creates INVEST-compliant user stories with acceptance criteria. Use when capturing requirements, defining backlog items, or breaking down features.
---

# User Story Writing

Create user stories meeting INVEST criteria.

## Execution Requirements

1. Use `templates/user-story.md` template
2. Validate against INVEST criteria before completing
3. Include 2-5 acceptance criteria
4. Replace all `[bracketed placeholders]`
5. Assign Story ID using next sequential number

## Mode Detection

**CREATE**: No existing story path → Copy template, generate next ID, fill sections

**EDIT**: Path provided → Read existing, preserve ID, update as requested

## User Story Format

```
As a [type of user],
I want [goal/desire],
So that [benefit/value].
```

Example:
```
As a registered customer,
I want to save items to a wishlist,
So that I can purchase them later without searching again.
```

## Required Elements

**Title** - Short, descriptive. "Wishlist - Add Items" not "User feature for saving stuff"

**User Story Statement** - Who (role), What (goal), Why (value)

**Acceptance Criteria** - Specific, testable conditions with Given-When-Then or checklist format

## INVEST Criteria

| Criterion | Meaning |
|-----------|---------|
| Independent | Develop in any order |
| Negotiable | Details discussable |
| Valuable | Delivers user/business value |
| Estimable | Team can size it |
| Small | Fits in one sprint |
| Testable | Clear acceptance criteria |

## Acceptance Criteria Formats

Given-When-Then (preferred):
```
- [ ] Given [precondition], When [action], Then [result]
```

Checklist:
```
- [ ] User can [action with measurable outcome]
```

## Writing Guidelines

Be specific about user roles: "premium subscriber" not "user"

Focus on outcomes: "export my data" not "a button"

State the benefit: "analyze in Excel" not "click it"

## Story Splitting

Split large stories by: workflow steps, business rules, data variations, user roles, or CRUD operations.

## Anti-Patterns

Do not write technical stories ("As a developer..."). Do not combine multiple features. Do not describe implementation. Do not omit the value clause. Do not use vague criteria.

## Story vs Task vs Bug

| Type | Purpose |
|------|---------|
| Story | New user-facing capability |
| Task | Technical work, no direct user value |
| Bug | Fix broken behavior |

## Directory Structure

```
stories/
├── US-001-brief-description.md
├── US-002-brief-description.md
└── archive/
```

Create `stories/` if needed. Scan for existing `US-*.md` files, find highest number, increment, pad to 3 digits.

## Template

Use `templates/user-story.md` for all new stories.

## Output

After creating/editing, report: file path, Story ID, acceptance criteria count, any INVEST concerns.
