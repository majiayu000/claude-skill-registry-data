---
name: domain-extractor
description: >
  Extract technology-free domain model from codebase. Produces a pure business-language
  specification that any stakeholder can understand. Use for: understand legacy code,
  document business logic, domain modeling, business requirements extraction,
  what does this code do, explain codebase to non-technical stakeholders.
---

# Domain Extractor

Extract pure business domain from code. Output contains ZERO technology terms.

## Purpose

Transform code into a business specification that:
- A CEO can understand
- Survives technology changes
- Captures what the system DOES, not HOW

## Activation

- "What does this codebase do?"
- "Extract the business logic"
- "Document this for stakeholders"
- "I need to understand this legacy system"

## Process

### Step 1: Analyze Code (10-15 min)

Read the codebase looking for:
- Models/Entities → Domain concepts
- Validation → Business rules
- Controllers/Handlers → Workflows
- Error messages → User expectations

### Step 2: Translate to Business Language

**Forbidden terms** (if you write these, rewrite):

```
API, REST, GraphQL, HTTP, endpoint, request, response,
database, SQL, query, schema, table, cache, session, token,
component, frontend, backend, server, client, service,
function, class, method, controller, middleware
```

**Translation examples**:

| Code | Business Language |
|------|-------------------|
| `POST /api/orders` | Customer places order |
| `SELECT * FROM users` | Look up customer |
| `validateCart()` | Verify order is valid |
| `sendEmail()` | Notify customer |
| `redis.cache()` | Remember for quick access |

### Step 3: Produce Output

Generate this exact format:

```markdown
# Domain Specification: [System Name]

## Purpose
[One paragraph: What business problem this solves]

## Actors
- **[Actor 1]**: [Role description]
- **[Actor 2]**: [Role description]

## Core Concepts
| Concept | Definition |
|---------|------------|
| [Name] | [Business meaning] |

## Workflows

### [Workflow 1 Name]
1. [Actor] [action] [object]
2. System [verifies/records/notifies] [what]
3. [Result]

### [Workflow 2 Name]
...

## Business Rules
- [Rule 1]
- [Rule 2]

## Constraints
- [Constraint 1]
- [Constraint 2]
```

## Validation

Before delivering, verify:
1. Read aloud - would a non-technical person understand every word?
2. Search for forbidden terms - zero should appear
3. Check completeness - all major code paths represented?

## Example

See `references/example.md` for complete input/output example.

## Output

Single markdown document: **Domain Specification**

No tech stack recommendations. No architecture proposals. Just pure domain.
