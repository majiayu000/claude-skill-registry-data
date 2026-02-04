---
name: domain-knowledge
description: Document domain knowledge including entities, attributes, relationships, processes, and ubiquitous language. Use when documenting domain models, entity relationships, business processes, or building a glossary of domain terms.
---

# Domain Knowledge Documentation

## Overview

This skill helps document domain knowledge systematically. It captures entities, relationships, processes, and terminology to create a shared understanding of the domain.

**Purpose**: Build a comprehensive domain model that serves as the foundation for requirements, implementation, and team communication.

## CRITICAL: NO ASSUMPTIONS POLICY

**This skill MUST trigger dialogue with users, NOT make assumptions about the domain.**

AI has a strong tendency to:
- Invent entity attributes when they're not specified
- Make up relationships between entities
- Fabricate process steps and business logic
- Assume data types and validation rules
- Create plausible but incorrect domain terminology

**NEVER do any of the above.** Instead:
- **ASK questions** about every entity attribute
- **WAIT for answers** before documenting relationships
- **DOCUMENT gaps** with `# TODO:` or `# QUESTION:` if user doesn't know
- **VERIFY understanding** before creating documentation
- **STOP immediately** when uncertain about ANY detail

### What to Always Ask

- "What attributes does this entity have?"
- "What's the data type of each attribute?"
- "How does this entity relate to [other entity]?"
- "What's the cardinality of this relationship?" (1:1, 1:N, N:M)
- "What are the steps in this process?"
- "Are there validation rules or constraints?"
- "Can you provide a real example from your domain?"

## File Location and Organization

### Directory Structure

Domain knowledge is organized in `docs/domains/[domain-name]/[subdomain-name]/` with subdirectories for each type:

```
docs/domains/
└── [domain-name]/
    └── [subdomain-name]/
        ├── entities/
        │   ├── _overview.md          (Master ERD with all entities)
        │   ├── customer.md           (Individual entity file)
        │   └── order.md
        ├── processes/
        │   ├── _overview.md          (Process relationships and flow)
        │   ├── checkout.md           (Individual process file)
        │   └── fulfillment.md
        └── glossary/
            ├── _overview.md          (Alphabetical index of all terms)
            ├── sku.md                (Individual term file)
            └── backorder.md
```

**File organization:**
- **entities/** - One file per entity, plus `_overview.md` with master ERD
- **processes/** - One file per process, plus `_overview.md` showing relationships
- **glossary/** - One file per term/concept, plus `_overview.md` as index

### File Naming

- Use **kebab-case** for filenames: `order-item.md`, `user-registration.md`
- Use `_overview.md` for index/summary files in each subdirectory
- Keep names concise and domain-specific

## Core Capabilities

### 1. Document Entities

Capture domain entities - the core concepts and objects in the domain.

**Entity documentation includes:**
- **Name** - What the entity is called
- **Description** - What it represents in the domain
- **Attributes** - Properties and data the entity holds
- **Constraints** - Business rules and validation
- **Lifecycle** - States and transitions
- **Relationships** - Connections to other entities

**Template:**

```markdown
# [Entity Name]

**Description**: [What this entity represents]

## Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| id | string | Yes | Unique identifier |
| name | string | Yes | ... |

## Relationships

- **has-many** [Other Entity] - Description
- **belongs-to** [Other Entity] - Description

## Lifecycle

- Created when: [trigger/event]
- Status transitions: [state changes]
- Deleted when: [condition]

## Business Rules

- [Rule 1]
- [Rule 2]

## Example

```json
{
  "id": "123",
  "name": "Example"
}
```
```

### 2. Document Relationships

Capture how entities connect and interact.

**Relationship types:**
- **One-to-One** (1:1) - Each A has exactly one B
- **One-to-Many** (1:N) - Each A has many B
- **Many-to-Many** (N:M) - Many A relate to many B
- **Composition** - Part-of relationships (strong ownership)
- **Aggregation** - Has-a relationships (weak ownership)

**Template:**

```markdown
## [Entity A] → [Entity B]

**Type**: one-to-many | many-to-many | one-to-one

**Description**: [What this relationship means]

**Cardinality**:
- [Entity A]: 0..1 | 1 | 0..* | 1..*
- [Entity B]: 0..1 | 1 | 0..* | 1..*

**Constraints**:
- [Business rules for this relationship]
```

### 3. Visualize with Mermaid Diagrams

#### Entity Relationship Diagrams (ERD)

```markdown
## Entity Relationship Diagram

\`\`\`mermaid
erDiagram
    Customer ||--o{ Order : "places"
    Order ||--|{ OrderItem : "contains"
    Product ||--o{ OrderItem : "included in"
    Customer {
        string id PK
        string name
        string email
    }
    Order {
        string id PK
        string customer_id FK
        date order_date
        string status
    }
\`\`\`
```

**Relationship notation:**
- `||--||` : One-to-one
- `||--o{` : One-to-many
- `}o--o{` : Many-to-many

#### Process Flow Diagrams

```markdown
## Process Flow

\`\`\`mermaid
flowchart TD
    Start([Customer initiates checkout])
    Start --> Validate{Cart valid?}
    Validate -->|No| Error[Show error]
    Validate -->|Yes| Payment[Process payment]
    Payment --> Confirm[Send confirmation]
    Confirm --> End([Complete])
\`\`\`
```

#### State Diagrams

```markdown
## Order Lifecycle

\`\`\`mermaid
stateDiagram-v2
    [*] --> Pending : Order placed
    Pending --> Confirmed : Payment received
    Confirmed --> Shipped : Items dispatched
    Shipped --> Delivered : Customer receives
    Delivered --> [*]
    Pending --> Cancelled : Customer cancels
    Cancelled --> [*]
\`\`\`
```

### 4. Document Processes

Capture business workflows and processes.

**Process documentation includes:**
- Process name and goal
- Trigger (what starts it)
- Actors (who participates)
- Steps (what happens)
- Decision points
- Outcomes
- Edge cases

**Template:**

```markdown
# [Process Name]

**Goal**: [What this process achieves]

**Trigger**: [What starts this process]

## Actors

- [Actor 1] - [Their role]
- [Actor 2] - [Their role]

## Steps

1. **[Step name]**
   - Who: [Actor]
   - What: [Action]
   - Input: [Required data/state]
   - Output: [Result/state change]

2. **[Decision point]**
   - If [condition]: Go to step X
   - Else: Go to step Y

## Outcomes

- Success: [What happens]
- Failure: [What happens]

## Business Rules

- [Rule 1]
- [Rule 2]

## Edge Cases

- [Case 1]: [How it's handled]
```

### 5. Document Ubiquitous Language

Capture terms, definitions, and domain vocabulary.

**Glossary documentation includes:**
- Term name
- Definition
- Context/usage
- Synonyms
- Related terms
- Examples

**Template:**

```markdown
# [Term]

**Definition**: [Clear, concise definition]

**Context**: [When/where this term is used]

**Synonyms**: [Alternative terms]

**Related terms**: [Connected concepts]

**Example**:
> [Usage in context]

**Technical mapping**:
- Database: `table_name.column_name`
- Code: `ClassName` or `functionName`
```

## Discovery Workflow

When documenting domain knowledge, follow these steps:

1. **Ask about existing documentation**
   - "Where do you currently document domain knowledge?"
   - "Do you have schema files, type definitions, or API docs?"

2. **Start with entities**
   - "What are the core entities in this domain?"
   - "Which entity should we document first?"
   - Document one entity completely before moving to the next

3. **Map relationships**
   - "How do these entities relate to each other?"
   - "What's the cardinality of this relationship?"

4. **Document processes**
   - "What business processes involve these entities?"
   - "Who are the actors in this process?"

5. **Build glossary**
   - "What terms does your team use?"
   - "Are there any ambiguous terms?"

## Best Practices

1. **Start small, grow organically** - Don't try to document everything at once
2. **Keep it current** - Update when domain understanding changes
3. **Use examples liberally** - Concrete examples make concepts clear
4. **Link everything** - Connect entities to processes to glossary
5. **Document uncertainties** - Use `# TODO:` and `# QUESTION:` markers
