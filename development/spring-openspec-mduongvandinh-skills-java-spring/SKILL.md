---
name: spring-openspec
version: 1.0.0
description: |
  Spec-First Development with OpenSpec for Spring Boot.
  Align on specifications before implementation begins.

triggers:
  - "new feature"
  - "spec first"
  - "openspec"
  - "specification"
  - "proposal"
---

# OpenSpec - Spec-Driven Development

## Workflow

```
┌──────────────────────────────────────────────────────────────┐
│                    OPENSPEC WORKFLOW                          │
│                                                               │
│  ┌──────────┐    ┌──────────┐    ┌───────────┐    ┌────────┐│
│  │ PROPOSAL │───→│  REVIEW  │───→│ IMPLEMENT │───→│ARCHIVE ││
│  │          │    │          │    │           │    │        ││
│  │ Draft    │    │ Align    │    │ Code      │    │ Merge  ││
│  │ Specs    │    │ Together │    │ Tasks     │    │ Specs  ││
│  └──────────┘    └──────────┘    └───────────┘    └────────┘│
└──────────────────────────────────────────────────────────────┘
```

## Directory Structure

```
openspec/
├── AGENTS.md           # Instructions for AI assistants
├── specs/              # Authoritative specifications
│   ├── auth/
│   ├── user/
│   └── order/
└── changes/            # Proposed modifications
    └── feature-xxx/
        ├── proposal.md
        ├── tasks.md
        └── spec-delta.md
```

## Commands

| Command | Description |
|---------|-------------|
| `/openspec-proposal <name>` | Create new proposal |
| `/openspec-review` | Review and align |
| `/openspec-implement <name>` | Implement from spec |
| `/openspec-archive <name>` | Archive completed feature |

## Proposal Template

```markdown
# Proposal: Feature Name

## Objective
What we want to achieve.

## Scope
- Item 1
- Item 2

## Out of Scope
- Not included

## Success Criteria
- Criterion 1
- Criterion 2

## Dependencies
- Dependency 1
```

## Spec Template

```markdown
# Feature Specification

## API Endpoint
POST /api/v1/resource
...

## Business Rules
1. Rule 1
2. Rule 2

## Data Model
@Entity...

## Sequence Diagram
Client -> Controller -> Service -> Repository
```

## Reference in Code

```java
/**
 * Service description.
 *
 * @spec openspec/specs/feature/spec-name.md
 */
@Service
public class MyService {
    // Implementation
}
```
