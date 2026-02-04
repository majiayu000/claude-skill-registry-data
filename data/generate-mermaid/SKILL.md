---
name: generate-mermaid
description: Automatically invoked when creating visual diagrams (flowcharts, sequence diagrams, ERDs, state machines, user journeys). Ensures proper Mermaid syntax and diagram clarity.
---

# Generate Mermaid Diagrams Skill

This skill activates when you need to create visual documentation using Mermaid diagrams.

## When This Skill Activates

Automatically engage when:
- Creating flowcharts for processes or algorithms
- Documenting API interactions with sequence diagrams
- Designing database schemas with ERDs
- Mapping state transitions with state diagrams
- Illustrating user journeys
- Explaining system architecture

## Diagram Type Selection

### Flowchart
**Use for:** Process flows, decision trees, algorithm logic
**Best when:** Showing sequential steps and decision points

### Sequence Diagram
**Use for:** Component interactions, API calls, time-based processes
**Best when:** Showing how components communicate over time

### ERD (Entity Relationship Diagram)
**Use for:** Database schemas, data models, relationships
**Best when:** Designing or documenting data structure

### State Diagram
**Use for:** State machines, lifecycle flows, status transitions
**Best when:** Tracking object states and transitions

### User Journey
**Use for:** User experience flows, emotional journey, touchpoints
**Best when:** Understanding user perspective through process

## Diagram Creation Workflow

### 1. Choose Appropriate Diagram Type
Match diagram type to information structure

### 2. Identify Key Elements
- What are the main components/nodes?
- What relationships/flows exist?
- What decisions or branches occur?
- What states or transitions matter?

### 3. Organize Layout
- Top-to-bottom or left-to-right
- Group related elements
- Minimize line crossings
- Logical flow direction

### 4. Use Clear Labels
- Descriptive node names
- Action-oriented labels
- Consistent terminology
- Avoid abbreviations unless standard

### 5. Add Context
- Title the diagram
- Provide description
- Explain key elements
- Note important details

## Mermaid Syntax Reference

### Flowchart

#### Basic Structure
```mermaid
flowchart TD
    Start([Start]) --> Process[Process Step]
    Process --> Decision{Decision?}
    Decision -->|Yes| Action1[Action 1]
    Decision -->|No| Action2[Action 2]
    Action1 --> End([End])
    Action2 --> End
```

#### Node Shapes
- `[]` Rectangle (process)
- `()` Rounded rectangle (start/end)
- `{}` Diamond (decision)
- `[()]` Stadium (start/end alt)
- `[[]]` Subroutine
- `[()]` Database

#### Direction
- `TD` or `TB` - Top to bottom
- `LR` - Left to right
- `RL` - Right to left
- `BT` - Bottom to top

### Sequence Diagram

```mermaid
sequenceDiagram
    participant A as Client
    participant B as API
    participant C as Database

    A->>B: POST /users
    activate B
    B->>C: INSERT user
    activate C
    C-->>B: User ID
    deactivate C
    B-->>A: 201 Created
    deactivate B
```

#### Arrow Types
- `->` Solid line
- `-->` Dotted line
- `->>` Solid arrow
- `-->>` Dotted arrow

#### Activation/Deactivation
- `activate Actor` - Show active
- `deactivate Actor` - Show inactive

### ERD

```mermaid
erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ LINE_ITEM : contains
    PRODUCT ||--o{ LINE_ITEM : "ordered in"

    USER {
        int id PK
        string email UK
        string name
        datetime created_at
    }

    ORDER {
        int id PK
        int user_id FK
        decimal total
        string status
    }
```

#### Relationships
- `||--||` One to one
- `||--o{` One to many
- `}o--o{` Many to many
- `||--o|` One to zero or one

#### Attributes
- `PK` - Primary Key
- `FK` - Foreign Key
- `UK` - Unique Key

### State Diagram

```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> Submitted : submit()
    Submitted --> Approved : approve()
    Submitted --> Rejected : reject()
    Approved --> Published : publish()
    Published --> Archived : archive()
    Rejected --> [*]
    Archived --> [*]
```

#### Special States
- `[*]` - Start/End state
- State names use camelCase or PascalCase
- Transitions labeled with actions

### User Journey

```mermaid
journey
    title Online Shopping Experience
    section Browse
      Visit site: 5: Customer
      View products: 4: Customer
      Filter results: 3: Customer
    section Purchase
      Add to cart: 5: Customer
      Enter payment: 2: Customer
      Complete order: 5: Customer
    section Post-Purchase
      Receive email: 4: Customer
      Track shipment: 5: Customer
```

#### Satisfaction Scores
- 1-2: Poor experience
- 3: Neutral
- 4-5: Good experience

## Best Practices

### Clarity

#### Good: Descriptive Labels
```mermaid
flowchart TD
    ValidateInput[Validate User Input] --> CheckAuth{User Authenticated?}
```

#### Avoid: Cryptic Labels
```mermaid
flowchart TD
    A[Validate] --> B{Auth?}
```

### Simplicity

#### Good: Focused Scope
```mermaid
flowchart TD
    Start([User Login]) --> ValidEmail{Valid Email?}
    ValidEmail -->|Yes| CheckPassword{Valid Password?}
    ValidEmail -->|No| ShowError[Show Email Error]
    CheckPassword -->|Yes| Success[Login Success]
    CheckPassword -->|No| ShowError2[Show Password Error]
```

#### Avoid: Too Complex
Don't try to fit an entire system in one diagram - break into multiple focused diagrams

### Layout

#### Good: Logical Flow
```mermaid
flowchart TD
    A --> B
    B --> C
    C --> D
```

#### Avoid: Crossing Lines
Organize nodes to minimize line crossings

### Consistency

- Use same node shape for same type of element
- Use consistent naming conventions
- Keep style uniform across project diagrams

## Diagram Output Format

When creating a diagram, provide:

### 1. Context
```markdown
# [Diagram Title]

[Brief description of what this diagram shows and why it's important]
```

### 2. The Diagram
````markdown
```mermaid
[diagram code]
```
````

### 3. Explanation
```markdown
## Key Elements

- **[Element Name]**: Description of what it represents
- **[Element Name]**: Description

## Flow Description

[Step-by-step walkthrough if needed]

## Notes

- [Important consideration]
- [Edge case or special behavior]
```

## File Organization

Save diagrams to:
- **Architecture diagrams** → `docs/architecture/diagrams/[name].md`
- **Feature flows** → `docs/features/[feature-name]-[type].md`
- **Data models** → `docs/architecture/models/[name].md`

### Naming Convention
`[subject]-[diagram-type].md`

Examples:
- `authentication-flow.md`
- `order-checkout-sequence.md`
- `user-order-erd.md`
- `order-status-state.md`

## Common Patterns

### API Request Flow
```mermaid
sequenceDiagram
    Client->>API: Request
    API->>Validation: Validate
    alt Valid
        API->>Service: Process
        Service->>DB: Query
        DB-->>Service: Data
        Service-->>API: Result
        API-->>Client: 200 OK
    else Invalid
        API-->>Client: 400 Bad Request
    end
```

### Authentication Flow
```mermaid
flowchart TD
    Start([User Login]) --> Submit[Submit Credentials]
    Submit --> Validate{Valid?}
    Validate -->|Yes| CheckMFA{MFA Enabled?}
    Validate -->|No| Error[Show Error]
    CheckMFA -->|Yes| SendCode[Send MFA Code]
    CheckMFA -->|No| Success[Login Success]
    SendCode --> VerifyCode{Code Valid?}
    VerifyCode -->|Yes| Success
    VerifyCode -->|No| Error
    Error --> Start
    Success --> Dashboard[Redirect to Dashboard]
```

### State Transitions
```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Loading : fetch()
    Loading --> Success : data received
    Loading --> Error : fetch failed
    Success --> Idle : reset()
    Error --> Idle : reset()
    Error --> Loading : retry()
```

### Database Schema
```mermaid
erDiagram
    USER ||--o{ POST : writes
    USER ||--o{ COMMENT : writes
    POST ||--o{ COMMENT : has

    USER {
        int id PK
        string email UK
        string username UK
        datetime created_at
    }

    POST {
        int id PK
        int author_id FK
        string title
        text content
        datetime published_at
    }

    COMMENT {
        int id PK
        int post_id FK
        int author_id FK
        text content
        datetime created_at
    }
```

## Diagram Quality Checklist

- [ ] Appropriate diagram type chosen
- [ ] All nodes clearly labeled
- [ ] Logical flow direction
- [ ] Minimal line crossings
- [ ] Consistent naming
- [ ] Context provided
- [ ] Key elements explained
- [ ] Saved to correct location
- [ ] File name follows convention
- [ ] Mermaid syntax valid

## Testing Diagrams

Before finalizing:
1. Copy Mermaid code
2. Test in [Mermaid Live Editor](https://mermaid.live)
3. Verify layout is clear
4. Check labels are readable
5. Ensure no syntax errors

## References

- Mermaid syntax: `.claude/skills/generate-mermaid/references/mermaid-syntax.md`
- Common patterns: `.claude/skills/generate-mermaid/references/common-patterns.md`

## Constraints

- Keep diagrams focused on one aspect
- Break complex systems into multiple diagrams
- Maintain consistency across project diagrams
- Update diagrams when system changes
- Don't diagram everything - only what adds value
