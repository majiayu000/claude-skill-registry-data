---
name: mermaid
description: Diagram generation using Mermaid syntax — flowcharts, sequence diagrams, ER diagrams, class diagrams, state machines, and more
layer: utility
category: visualization
triggers:
  - "draw a diagram"
  - "create a flowchart"
  - "sequence diagram"
  - "ER diagram"
  - "class diagram"
  - "state diagram"
  - "visualize this"
  - "mermaid"
inputs:
  - description: Natural language description of what to diagram
  - diagram_type: flowchart | sequence | er | class | state | gantt | pie | git | mindmap
  - entities: List of entities/components to include
  - relationships: Connections between entities
outputs:
  - mermaid_code: Valid Mermaid syntax ready for rendering
  - diagram_explanation: Plain-text explanation of the diagram
  - alternatives: Alternative diagram types that could represent the same information
linksTo:
  - data-modeling
  - api-designer
  - ai-multimodal
linkedFrom:
  - orchestrator
  - planner
  - code-architect
preferredNextSkills:
  - data-modeling
  - api-designer
fallbackSkills:
  - sequential-thinking
riskLevel: low
memoryReadPolicy: selective
memoryWritePolicy: selective
sideEffects: []
---

# Mermaid

## Purpose

This skill generates precise, valid Mermaid diagram syntax from natural language descriptions, code analysis, or structured data. Mermaid diagrams are version-controllable, embeddable in Markdown, and renderable in GitHub, GitLab, Notion, and most documentation platforms.

## Key Concepts

### Diagram Type Selection Guide

| You Want To Show... | Use This Diagram | Mermaid Type |
|---------------------|-----------------|--------------|
| Process flow with decisions | Flowchart | `flowchart TD/LR` |
| Request/response between services | Sequence Diagram | `sequenceDiagram` |
| Database tables and relationships | ER Diagram | `erDiagram` |
| Object-oriented class structure | Class Diagram | `classDiagram` |
| State transitions | State Diagram | `stateDiagram-v2` |
| Project timeline | Gantt Chart | `gantt` |
| Proportional data | Pie Chart | `pie` |
| Git branching | Git Graph | `gitGraph` |
| Hierarchical concepts | Mindmap | `mindmap` |
| User journey steps | User Journey | `journey` |

### Syntax Fundamentals

**Direction**: `TD` (top-down), `LR` (left-right), `BT` (bottom-top), `RL` (right-left)

**Node Shapes**:
```
id[Rectangle]
id(Rounded)
id{Diamond/Decision}
id([Stadium])
id[[Subroutine]]
id[(Database)]
id((Circle))
id>Asymmetric]
id{{Hexagon}}
```

**Edge Types**:
```
A --> B          Solid arrow
A --- B          Solid line (no arrow)
A -.-> B         Dotted arrow
A ==> B          Thick arrow
A -- text --> B   Labeled edge
A -->|text| B    Labeled edge (alternative)
```

## Diagram Templates

### Template 1: System Architecture Flowchart

```mermaid
flowchart TD
    subgraph Client["Client Layer"]
        Browser["Browser/Mobile App"]
    end

    subgraph Edge["Edge Layer"]
        CDN["CDN (CloudFront)"]
        LB["Load Balancer"]
    end

    subgraph App["Application Layer"]
        API["API Server"]
        Worker["Background Worker"]
        Cache["Redis Cache"]
    end

    subgraph Data["Data Layer"]
        DB[(PostgreSQL)]
        S3["Object Storage (S3)"]
        Queue["Message Queue"]
    end

    Browser --> CDN
    CDN --> LB
    LB --> API
    API --> Cache
    API --> DB
    API --> Queue
    Queue --> Worker
    Worker --> DB
    Worker --> S3

    style Client fill:#e1f5fe
    style Edge fill:#f3e5f5
    style App fill:#e8f5e9
    style Data fill:#fff3e0
```

### Template 2: API Request Sequence

```mermaid
sequenceDiagram
    actor User
    participant Client as React App
    participant API as API Server
    participant Auth as Auth Service
    participant DB as Database

    User->>Client: Click "Create Order"
    Client->>API: POST /api/orders
    API->>Auth: Validate JWT
    Auth-->>API: Token valid (user: 123)

    API->>DB: BEGIN TRANSACTION
    API->>DB: INSERT INTO orders
    DB-->>API: order_id: 456

    API->>DB: UPDATE inventory SET qty = qty - 1
    DB-->>API: OK
    API->>DB: COMMIT

    API-->>Client: 201 { id: 456, status: "created" }
    Client-->>User: Show success toast

    Note over API,DB: Transaction ensures atomicity
```

### Template 3: Entity Relationship Diagram

```mermaid
erDiagram
    USER {
        uuid id PK
        string email UK
        string name
        string password_hash
        timestamp created_at
        timestamp updated_at
    }

    ORGANIZATION {
        uuid id PK
        string name
        string slug UK
        timestamp created_at
    }

    MEMBERSHIP {
        uuid id PK
        uuid user_id FK
        uuid org_id FK
        enum role "admin, member, viewer"
        timestamp joined_at
    }

    PROJECT {
        uuid id PK
        uuid org_id FK
        string name
        text description
        enum status "active, archived"
    }

    TASK {
        uuid id PK
        uuid project_id FK
        uuid assignee_id FK
        string title
        text description
        enum priority "low, medium, high, critical"
        enum status "todo, in_progress, review, done"
        timestamp due_date
    }

    USER ||--o{ MEMBERSHIP : "has"
    ORGANIZATION ||--o{ MEMBERSHIP : "has"
    ORGANIZATION ||--o{ PROJECT : "owns"
    PROJECT ||--o{ TASK : "contains"
    USER ||--o{ TASK : "assigned to"
```

### Template 4: State Machine

```mermaid
stateDiagram-v2
    [*] --> Draft: Create

    Draft --> PendingReview: Submit
    Draft --> Deleted: Delete

    PendingReview --> InReview: Reviewer assigned
    PendingReview --> Draft: Withdraw

    InReview --> Approved: Approve
    InReview --> ChangesRequested: Request changes
    InReview --> Rejected: Reject

    ChangesRequested --> Draft: Author revises
    ChangesRequested --> Deleted: Author abandons

    Approved --> Published: Publish
    Approved --> Draft: Unpublish

    Published --> Archived: Archive
    Published --> Draft: Revert to draft

    Rejected --> [*]
    Deleted --> [*]
    Archived --> [*]

    note right of PendingReview
        Auto-assign reviewer
        based on CODEOWNERS
    end note

    note right of Published
        Triggers webhook
        notification
    end note
```

### Template 5: Class Diagram

```mermaid
classDiagram
    class Repository~T~ {
        <<interface>>
        +findById(id: string) T
        +findMany(filter: Filter) T[]
        +create(data: CreateDTO) T
        +update(id: string, data: UpdateDTO) T
        +delete(id: string) void
    }

    class UserRepository {
        -db: Database
        +findById(id: string) User
        +findByEmail(email: string) User
        +findMany(filter: UserFilter) User[]
        +create(data: CreateUserDTO) User
        +update(id: string, data: UpdateUserDTO) User
        +delete(id: string) void
    }

    class UserService {
        -repo: UserRepository
        -auth: AuthService
        -events: EventBus
        +register(data: RegisterDTO) User
        +login(credentials: LoginDTO) Session
        +updateProfile(id: string, data: ProfileDTO) User
    }

    class AuthService {
        -jwt: JWTProvider
        -hash: HashService
        +createToken(user: User) string
        +verifyToken(token: string) TokenPayload
        +hashPassword(plain: string) string
        +verifyPassword(plain: string, hash: string) boolean
    }

    Repository~T~ <|.. UserRepository
    UserService --> UserRepository: uses
    UserService --> AuthService: uses
```

### Template 6: Git Branching Strategy

```mermaid
gitGraph
    commit id: "init"
    branch develop
    checkout develop
    commit id: "setup"

    branch feature/auth
    checkout feature/auth
    commit id: "auth-model"
    commit id: "auth-api"
    commit id: "auth-ui"
    checkout develop
    merge feature/auth

    branch feature/orders
    checkout feature/orders
    commit id: "order-model"
    commit id: "order-api"

    checkout develop
    branch release/1.0
    checkout release/1.0
    commit id: "bump-version"
    commit id: "fix-typo"
    checkout main
    merge release/1.0 tag: "v1.0.0"
    checkout develop
    merge release/1.0

    checkout feature/orders
    commit id: "order-ui"
    checkout develop
    merge feature/orders
```

### Template 7: User Journey

```mermaid
journey
    title User Onboarding Flow
    section Sign Up
        Visit landing page: 5: User
        Click "Get Started": 4: User
        Fill registration form: 3: User
        Verify email: 2: User
    section First Use
        Complete onboarding wizard: 3: User
        Create first project: 4: User
        Invite team member: 3: User
    section Activation
        Complete first task: 5: User
        Receive notification: 4: User, System
        View dashboard: 5: User
```

## Generation Workflow

### From Natural Language

```
INPUT: "Show me how a user request flows through our microservices architecture"

STEP 1: Identify entities
  - User/Client
  - API Gateway
  - Auth Service
  - User Service
  - Order Service
  - Database(s)
  - Message Queue

STEP 2: Identify interactions
  - Client → Gateway: HTTP request
  - Gateway → Auth: validate token
  - Gateway → Service: forward request
  - Service → DB: query/write
  - Service → Queue: publish event

STEP 3: Choose diagram type
  - Temporal interactions between services → Sequence Diagram

STEP 4: Generate Mermaid syntax
  [Produce valid sequenceDiagram code]

STEP 5: Validate
  - All entities referenced in interactions are declared as participants
  - Message labels are clear and concise
  - Activation/deactivation bars are properly nested
  - Notes are used for important details
```

### From Code Analysis

```
INPUT: "Generate an ER diagram from our Prisma schema"

STEP 1: Read the schema file
  → Read prisma/schema.prisma

STEP 2: Extract entities
  - Each `model` becomes an entity
  - Fields become attributes
  - @id → PK, @unique → UK, @relation → FK

STEP 3: Extract relationships
  - One-to-one: model A has field of type B
  - One-to-many: model A has field of type B[]
  - Many-to-many: implicit via relation table or explicit

STEP 4: Generate erDiagram
  [Map Prisma types to Mermaid ER types]
  [Map relationships with correct cardinality]
```

## Styling Guide

### Color Palettes

```
Professional:
  style node fill:#1a73e8,stroke:#1557b0,color:#fff
  style node fill:#34a853,stroke:#2d8e47,color:#fff
  style node fill:#ea4335,stroke:#c5221f,color:#fff
  style node fill:#fbbc04,stroke:#e3a800,color:#000

Pastel (for subgraphs):
  style subgraph fill:#e8f0fe,stroke:#4285f4
  style subgraph fill:#e6f4ea,stroke:#34a853
  style subgraph fill:#fce8e6,stroke:#ea4335
  style subgraph fill:#fef7e0,stroke:#f9ab00
```

### Best Practices

1. **Direction**: Use `LR` for process flows, `TD` for hierarchies
2. **Labels**: Keep edge labels short (2-4 words max)
3. **Grouping**: Use subgraphs to visually cluster related nodes
4. **Consistency**: Use the same node shape for the same type of entity throughout
5. **Simplicity**: If a diagram has more than 15-20 nodes, split into multiple diagrams
6. **IDs**: Use meaningful IDs (`AuthService` not `A1`) for readability

## Anti-Patterns

1. **Overcrowding**: Cramming too many nodes into one diagram. Split into focused sub-diagrams.
2. **Inconsistent notation**: Mixing node shapes randomly. Establish a legend and follow it.
3. **Missing labels**: Edges without labels force the reader to guess the relationship.
4. **Wrong diagram type**: Using a flowchart when a sequence diagram would be clearer (or vice versa).
5. **Invalid syntax**: Not testing the Mermaid code before delivering. Always mentally validate that participants are declared, relationships reference existing entities, and subgraphs are properly closed.

## Integration Notes

- When analyzing database schemas from **data-modeling**, generate ER diagrams.
- When documenting APIs from **api-designer**, generate sequence diagrams for key flows.
- When **ai-multimodal** receives a diagram image, convert it to Mermaid syntax for version control.
- Output Mermaid code blocks in fenced markdown for direct rendering in GitHub/GitLab.
