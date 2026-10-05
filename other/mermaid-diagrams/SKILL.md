---
allowed-tools: Read, Write, Edit
description: 'Create clear, well-structured diagrams using Mermaid syntax.

  Use when visualizing architecture, workflows, data models, or processes.

  Helps choose the right diagram type and follows best practices for readability.'
name: mermaid-diagrams
---

# Mermaid Diagrams

Create clear, well-structured diagrams using Mermaid syntax for documentation, architecture, and process visualization.

## Choosing the Right Diagram

| What You're Showing | Diagram Type | Best For |
|---------------------|--------------|----------|
| Process flow, decisions | Flowchart | Algorithms, user flows, decision trees |
| Component interactions over time | Sequence | API calls, authentication flows, message passing |
| System components and connections | Architecture (flowchart) | Service architecture, deployment topology |
| Database tables and relationships | ER Diagram | Data models, schema documentation |
| Object structure and inheritance | Class Diagram | OOP design, type hierarchies |
| Lifecycle transitions | State Diagram | Order status, user states, workflows |
| Project timeline | Gantt | Sprints, milestones, dependencies |
| Proportions | Pie Chart | Distribution, percentages |
| Hierarchical concepts | Mindmap | Feature breakdown, brainstorming |
| Version control history | Git Graph | Branch strategy, release flow |

## Diagram Best Practices

### Keep It Readable

- **Limit nodes**: 7-15 nodes per diagram; split if larger
- **Use clear labels**: Full words, not abbreviations
- **Direction matters**: Top-to-bottom (TD) for hierarchies, left-to-right (LR) for timelines
- **Group related items**: Use subgraphs to cluster related components

### Consistent Styling

- Use consistent shapes for similar node types
- Color sparingly—for emphasis, not decoration
- Keep line styles uniform unless showing different relationship types

## Flowchart

For processes, decisions, and workflows.

```mermaid
flowchart TD
    A[Start] --> B{Valid Input?}
    B -->|Yes| C[Process Data]
    B -->|No| D[Show Error]
    C --> E[Save Result]
    D --> A
    E --> F[End]
```

### Node Shapes

| Shape | Syntax | Use For |
|-------|--------|---------|
| Rectangle | `[text]` | Process, action |
| Rounded | `(text)` | Start/end points |
| Diamond | `{text}` | Decision |
| Parallelogram | `[/text/]` | Input/output |
| Circle | `((text))` | Connector |
| Database | `[(text)]` | Data store |

### Subgraphs for Grouping

```mermaid
flowchart LR
    subgraph Frontend
        A[React App] --> B[API Client]
    end
    subgraph Backend
        C[API Gateway] --> D[Service]
        D --> E[(Database)]
    end
    B --> C
```

## Sequence Diagram

For interactions between components over time.

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant A as API
    participant D as Database

    U->>F: Click Login
    F->>A: POST /auth/login
    A->>D: Query user
    D-->>A: User record
    A-->>F: JWT token
    F-->>U: Redirect to dashboard
```

### Message Types

| Arrow | Meaning |
|-------|---------|
| `->>` | Synchronous request |
| `-->>` | Synchronous response |
| `--)` | Asynchronous message |
| `--x` | Failed/rejected |

### Grouping with Boxes

```mermaid
sequenceDiagram
    box Client
        participant Browser
        participant Worker
    end
    box Server
        participant API
        participant Queue
    end
    Browser->>API: Request
    API--)Queue: Enqueue job
    Queue--)Worker: Process
```

## Entity Relationship Diagram

For database schemas and data models.

```mermaid
erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ ORDER_LINE : contains
    PRODUCT ||--o{ ORDER_LINE : "ordered in"

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

    PRODUCT {
        int id PK
        string name
        decimal price
    }
```

### Relationship Notation

| Symbol | Meaning |
|--------|---------|
| `\|\|` | Exactly one |
| `o\|` | Zero or one |
| `}o` | Zero or many |
| `}\|` | One or many |

## Class Diagram

For object-oriented design and type hierarchies.

```mermaid
classDiagram
    class User {
        +int id
        +string email
        +login() bool
        +logout() void
    }

    class Admin {
        +list~string~ permissions
        +grantAccess(User) void
    }

    class Guest {
        +register() User
    }

    User <|-- Admin : extends
    User <|-- Guest : extends
    User "1" --> "*" Order : places
```

### Visibility Modifiers

| Symbol | Visibility |
|--------|------------|
| `+` | Public |
| `-` | Private |
| `#` | Protected |
| `~` | Package |

## State Diagram

For lifecycle and state transitions.

```mermaid
stateDiagram-v2
    [*] --> Draft

    Draft --> Pending: Submit
    Pending --> Approved: Approve
    Pending --> Rejected: Reject
    Rejected --> Draft: Revise

    Approved --> [*]

    state Pending {
        [*] --> UnderReview
        UnderReview --> NeedsInfo: Request Info
        NeedsInfo --> UnderReview: Info Provided
    }
```

## Gantt Chart

For project timelines and schedules.

```mermaid
gantt
    title Project Timeline
    dateFormat YYYY-MM-DD

    section Planning
        Requirements    :done, req, 2024-01-01, 7d
        Design         :done, des, after req, 5d

    section Development
        Backend API    :active, api, after des, 14d
        Frontend       :fe, after des, 14d
        Integration    :int, after api, 7d

    section Release
        Testing        :test, after int, 5d
        Deployment     :deploy, after test, 2d
```

## Architecture Diagrams

Use flowcharts with subgraphs for system architecture.

```mermaid
flowchart TB
    subgraph Client
        Web[Web App]
        Mobile[Mobile App]
    end

    subgraph "API Layer"
        Gateway[API Gateway]
        Auth[Auth Service]
    end

    subgraph Services
        UserSvc[User Service]
        OrderSvc[Order Service]
        NotifySvc[Notification Service]
    end

    subgraph Data
        DB[(PostgreSQL)]
        Cache[(Redis)]
        Queue[Message Queue]
    end

    Web & Mobile --> Gateway
    Gateway --> Auth
    Gateway --> UserSvc & OrderSvc
    OrderSvc --> Queue
    Queue --> NotifySvc
    UserSvc & OrderSvc --> DB
    UserSvc --> Cache
```

## Styling

Apply styles sparingly for emphasis.

```mermaid
flowchart LR
    A[Normal] --> B[Warning]
    B --> C[Error]
    C --> D[Success]

    style B fill:#fff3cd,stroke:#ffc107
    style C fill:#f8d7da,stroke:#dc3545
    style D fill:#d4edda,stroke:#28a745
```

### Class-Based Styling

```mermaid
flowchart TD
    A[Service A]:::healthy --> B[Service B]:::degraded
    B --> C[Service C]:::down

    classDef healthy fill:#d4edda,stroke:#28a745
    classDef degraded fill:#fff3cd,stroke:#ffc107
    classDef down fill:#f8d7da,stroke:#dc3545
```

## Common Pitfalls

| Problem | Cause | Solution |
|---------|-------|----------|
| Diagram won't render | Special characters in labels | Wrap labels in quotes: `A["Label: with colon"]` |
| Arrows going wrong way | Direction mismatch | Check `TD` vs `LR` orientation |
| Cluttered diagram | Too many nodes | Split into multiple diagrams or use subgraphs |
| Text cut off | Long labels | Use abbreviations or multi-line: `A["Line 1<br/>Line 2"]` |
| Inconsistent spacing | Manual positioning | Let Mermaid auto-layout; avoid fighting it |

## Escaping Special Characters

```mermaid
flowchart LR
    A["Label with (parentheses)"]
    B["Contains 'quotes'"]
    C["Has #hash and @at"]
```

## Where Mermaid Works

- GitHub/GitLab markdown (native support)
- Notion, Obsidian, many note apps
- Docusaurus, MkDocs, VitePress
- VS Code with preview extensions
- Export to PNG/SVG via Mermaid CLI or online editors
