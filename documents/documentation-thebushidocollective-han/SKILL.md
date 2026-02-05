---
name: documentation
description: Documentation creation and modification rules (docs/develop/ design documents, abstraction principles, structure). Use when creating documentation, updating design documents, writing architecture docs, asking about documentation structure, design principles, or working with files in docs/develop/.
---

# Documentation Guide

## Structure

Design documents in `docs/develop/`:

```
docs/develop/
├── architecture/     # Architecture and design principles (conceptual)
├── features/         # Feature specifications
├── database/         # Database design
├── rules/            # Coding rules and development guidelines
└── design/           # Detailed design documents
```

### Directory Roles

#### architecture/
System-wide architecture and design principles

- Clean architecture layer responsibilities
- Dependency injection patterns
- Technology stack composition
- Project structure
- Discord API constraints and guidelines

**Examples**: `rust_optimized_architecture.md`, `dependency_injection.md`

#### features/
Feature requirements and specifications

- Feature overview
- Use cases
- Business flows
- Constraints
- External integrations

**Examples**: `quest_recruitment.md`, `schedule_notification.md`

#### database/
Database design

- Table definitions
- Relations
- Indexes
- Database user design
- Implementation policies (SeaORM, migrations)

**Examples**: `tables/guild/guild_channels.md`, `db_role_usage.md`

#### rules/
Development rules and best practices

- Architecture rules
- Coding style
- Error handling
- Logging
- Security
- Performance
- Testing

**Examples**: `architecture.md`, `error_handling.md`, `logging.md`

#### design/
Detailed design documents

- Implementation-specific design decisions
- Service layer design
- Data conversion logic
- Technical implementation details

**Examples**: `spreadsheet/service_layer.md`, `database/sea_orm_timestamp_automation.md`

## Documentation Principles

### Abstraction Principle (Critical)

**Do not include concrete code implementation**

- Documents describe architecture, responsibilities, and flows **conceptually**
- Avoid dual maintenance of code and documentation
- Leave implementation details to code, documents explain "why" and "what"

```markdown
❌ Bad (too concrete):
## User Creation Process

pub async fn create_user(data: UserData) -> Result<User> {
    let user = User {
        name: data.name,
        email: data.email,
    };
    repository.save(user).await
}

✅ Good (abstract design):
## User Creation Process

### Responsibilities
- Validate user data
- Check for duplicates
- Persist to database

### Flow
1. Validate input data
2. Check email duplication
3. Create user entity
4. Save within transaction
```

### Permanence Principle (Critical)

**Documents are permanent design references, not temporary work trackers**

- Documents should remain valid regardless of implementation timeline
- Avoid including any time-bound or progress-related information
- Focus on stable design decisions and architectural principles

```markdown
❌ Bad (temporal information):
## User Authentication Feature

### TODO
- [ ] Implement password hashing
- [ ] Add JWT token generation
- [ ] Currently working on session management

### Progress
Week 1: Completed user model
Week 2: In progress - authentication logic

✅ Good (permanent design):
## User Authentication Feature

### Responsibilities
- Validate user credentials
- Generate secure session tokens
- Manage user sessions

### Security Constraints
- Passwords must be hashed with bcrypt
- Tokens expire after 24 hours
- Sessions invalidate on logout
```

**Do not include:**
- Implementation plans or roadmaps
- Progress tracking or status updates
- TODO lists or task checklists
- Temporary notes or WIP markers
- Time-sensitive information (e.g., "currently implementing...", "planned for next sprint")
- Developer assignments or timelines

**Documents should be:**
- Permanent design references
- Independent of who implements or when
- Focused on "what" and "why", not "when" or "who"

### Language

- All documentation in **Japanese** (except this skill file)
- Technical terms can remain in English (e.g., Service layer, Repository layer)
- Minimize code samples

### Structure and Readability

```markdown
# Title

## Overview
Explain purpose and big picture in 1-2 paragraphs

## Responsibilities
What this feature/layer handles

## Constraints
Rules to follow and prohibitions

## Flow
Process flow in bullets or diagrams

## Examples
Concrete examples (if needed)
```

## Best Practices

### 1. Clear Purpose

```markdown
✅ Good:
# Recruitment Notification Schedule Feature

## Purpose
Periodically notify recruitment information to increase player participation.
Time-based notifications support players in different timezones.

❌ Bad:
# Recruitment Notification Schedule Feature

A feature that manages schedules.
```

### 2. Specify Layer Responsibilities

```markdown
✅ Good:
## Layer Responsibilities

### Service Layer
- Validate recruitment data
- Determine notification targets
- Call Repository layer for data retrieval

### Repository Layer
- Persist recruitment data
- Execute queries based on search criteria

❌ Bad:
## Processing
Save and retrieve data.
```

### 3. Explicit Constraints

```markdown
✅ Good:
## Constraints

- Transaction management only in Facade layer
- Prohibited: Direct dependency on other Service layers
- Prohibited: Long-held transactions

❌ Bad:
## Notes
Be careful with transactions.
```

### 4. Visualize Flow

```markdown
✅ Good:
## Process Flow

1. Receive user input
2. Validate input data
   - Check required fields
   - Check format
3. Check for duplicates
4. Execute within transaction:
   - Create entity
   - Save to database
   - Update related data
5. Return result

❌ Bad:
## Processing
Save data.
```

## When to Update Documentation

### Update Required

1. **Architecture Changes**
   - Layer responsibility changes
   - New pattern introductions
   - Dependency relationship changes

2. **New Feature Addition**
   - Add feature spec to `features/`
   - Update related `architecture/`

3. **Database Schema Changes**
   - Update `database/tables/`
   - Update relation diagrams

4. **Rule Changes**
   - Update documents in `rules/`
   - Reflect in CLAUDE.md

### Update Not Required

- Minor function name or parameter changes (per abstraction principle)
- Internal implementation optimization
- Bug fixes (not affecting design)

## Document Templates

### Feature Specification (features/)

```markdown
# Feature Name

## Overview
Purpose and big picture of this feature

## Use Cases
- Use case 1: Description
- Use case 2: Description

## Business Flow
1. Step 1
2. Step 2
3. Step 3

## Constraints
- Constraint 1
- Constraint 2

## Related Features
- Reference to related feature 1
- Reference to related feature 2
```

### Architecture Document (architecture/)

```markdown
# Architecture Name

## Purpose
Why adopt this architecture

## Composition
Main components and responsibilities

## Design Decisions
- Decision 1: Reason
- Decision 2: Reason

## Constraints
- Constraint 1
- Constraint 2
```

### Rules Document (rules/)

```markdown
# Rule Name

## Principles
Fundamental concepts

## ✅ Recommended Patterns
Recommended implementation approach (conceptual level)

## ❌ Anti-patterns
Implementation to avoid (conceptual level)

## Exceptions
When this rule doesn't apply
```

## Review Checklist

Check when creating/modifying documents:

- [ ] No concrete code implementation included
- [ ] No temporal information (plans, progress, TODOs) included
- [ ] Responsibilities and flow clearly described
- [ ] Written in Japanese
- [ ] Constraints and prohibitions specified
- [ ] References to related documents included
- [ ] Purpose (why) explained
- [ ] Structured and readable

## Common Mistakes

### ❌ Code Paste

```markdown
❌ Bad:
## Implementation

pub struct UserService {
    repository: Arc<dyn UserRepository>,
}

impl UserService {
    pub async fn create(&self, data: UserData) -> Result<User> {
        self.repository.create(data).await
    }
}
```

### ✅ Conceptual Explanation

```markdown
✅ Good:
## UserService Responsibilities

- Validate user data
- Apply business rules
- Persist data through Repository layer

## Flow
1. Validate input data
2. Apply business rules (e.g., age restrictions)
3. Delegate to Repository layer
```

## Summary

Documents convey **concepts and architecture**.
Leave concrete implementation to code, describe "why designed this way" and "what to follow".
