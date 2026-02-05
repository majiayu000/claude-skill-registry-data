---
name: mermaid-expert
description: Expert guidance for Mermaid.js diagramming library. Create flowcharts, sequence diagrams, class diagrams, state diagrams, Gantt charts, git graphs, and block diagrams. Use when working with Mermaid syntax, creating diagrams, or visualizing complex concepts and workflows.
---

# Mermaid Expert

Expert guidance for Mermaid.js, the powerful JavaScript library for creating diagrams and visualizations using text-based syntax. Mermaid transforms simple text descriptions into professional-looking diagrams that can be embedded in documentation, presentations, and web applications.

## Additional Resources

For comprehensive documentation and advanced features, see the [Mermaid Source Documentation](docs/snapshot/v11.12.1/) which includes:
- [Flow Charts Guide](docs/snapshot/v11.12.1/flow_charts.md) - Complete flowchart syntax and examples

For integration details and configuration options, refer to the main documentation at [docs/snapshot/v11.12.1/](docs/snapshot/v11.12.1/).

## Core Concepts

**Mermaid is a text-to-diagram tool that allows you to create:**
- Flowcharts for processes and decision trees
- Sequence diagrams for interactions and timelines
- Class diagrams for software architecture
- State diagrams for finite state machines
- Gantt charts for project management
- Git graphs for version control visualization
- Block diagrams for system layouts

### Getting Started

**Basic Mermaid syntax structure:**
```mermaid
diagramType
    [diagram content]
```

**Simple flowchart example:**
```mermaid
flowchart TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Process 1]
    B -->|No| D[Process 2]
    C --> E[End]
    D --> E
```

### Installation and Setup

**In HTML:**
```html
<script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
```

**In Markdown/Documentation:**
Most modern platforms (GitHub, GitLab, Notion) support Mermaid natively using code blocks with `mermaid` language identifier.

**Node.js/npm:**
```bash
npm install mermaid
```

### Command Line Interface (mermaid-cli)

For detailed installation instructions and usage, see the official [mermaid-cli repository](https://github.com/mermaid-js/mermaid-cli).

**Basic usage examples (after installation):**
```bash
# Convert Mermaid file to SVG
mmdc -i input.mmd -o output.svg

# Convert to PNG with dark theme and transparent background
mmdc -i input.mmd -o output.png -t dark -b transparent

# Generate diagrams in markdown files (automatically finds and replaces mermaid blocks)
mmdc -i readme.template.md -o readme.md
```

**Piping input from stdin:**
```bash
cat << EOF | mmdc --input -
flowchart TD
    A[Start] --> B[Process]
    B --> C[End]
EOF
```

**Docker usage:**
```bash
docker pull minlag/mermaid-cli
docker run --rm -u $(id -u):$(id -g) -v /path/to/diagrams:/data minlag/mermaid-cli -i diagram.mmd
```

**Syntax validation with mermaid-cli:**
If mermaid-cli is installed, you can validate Mermaid syntax using:
```bash
# Test syntax by piping input
echo "flowchart TD; A-->B" | mmdc --input -
# If no errors occur, the syntax is valid
```

*If mermaid-cli is not installed, please refer to the [official installation guide](https://github.com/mermaid-js/mermaid-cli) for setup instructions.*

**Configuration:**
```javascript
mermaid.initialize({
    startOnLoad: true,
    theme: 'default',
    themeVariables: {
        primaryColor: '#ffcc00',
        primaryTextColor: '#000',
        lineColor: '#ffcc00'
    }
});
```

## Flow Charts

### Basic Flowchart Syntax

**Node types:**
```mermaid
flowchart LR
    A[Square with text] --> B(Rounded rectangle)
    B --> C{Diamond for decision}
    C --> D((Circle))
    C --> E>Flag shape]
    D --> F[/Parallelogram/]
    E --> G[\Hexagon\]
```

**Directions:**
- `TD` or `TB` - Top to Bottom (default)
- `BT` - Bottom to Top
- `LR` - Left to Right
- `RL` - Right to Left

**Complex example with styling:**
```mermaid
flowchart TD
    A[Start Process] --> B{Data Available?}
    B -->|Yes| C[Load Data]
    B -->|No| D[Generate Mock Data]
    C --> E[Process Data]
    D --> E
    E --> F{Validation Passed?}
    F -->|Yes| G[Save Results]
    F -->|No| H[Log Error]
    G --> I[End]
    H --> I

    style A fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    style G fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px
    style H fill:#ffebee,stroke:#c62828,stroke-width:2px
```

### Advanced Flowchart Features

**Subgraphs:**
```mermaid
flowchart TB
    subgraph "User Authentication"
        A[Login Form] --> B{Credentials Valid?}
        B -->|Yes| C[Grant Access]
        B -->|No| D[Show Error]
    end

    subgraph "Main Application"
        C --> E[Load Dashboard]
        E --> F[User Actions]
    end
```

**Links and actions:**
```mermaid
flowchart LR
    A[Click Here] --> B(https://example.com)
    C[Callback] --> D{javascript:alert('Hello')}
```

## Sequence Diagrams

### Basic Sequence Diagram

**Participants and interactions:**
```mermaid
sequenceDiagram
    participant Alice
    participant Bob
    participant Server

    Alice->>Bob: Hello Bob!
    Bob->>Alice: Hi Alice!
    Alice->>Server: Request data
    Server-->>Alice: Response data
    Bob->>Server: Request different data
    Server--xBob: Error response
```

**Advanced features:**
```mermaid
sequenceDiagram
    participant User as UI User
    participant Frontend as Web App
    participant Backend as API Server
    participant Database as DB

    User->>Frontend: Submit form
    Frontend->>Backend: POST /api/data
    activate Backend
    Backend->>Database: Query data
    Database-->>Backend: Return results
    Backend-->>Frontend: JSON response
    deactivate Backend
    Frontend->>User: Display results

    Note over User,Database: Complete workflow
    Note right of Backend: Processing request
    Note left of Frontend: Rendering UI
```

### Loops and Conditionals

```mermaid
sequenceDiagram
    participant Client
    participant Server

    loop Retry mechanism
        Client->>Server: Send request
        alt Success
            Server-->>Client: Success response
            break Stop retrying
        else Server error
            Server--xClient: Error response
            Client->>Client: Wait and retry
        end
    end
```

## Class Diagrams

### UML Class Structure

**Basic class definition:**
```mermaid
classDiagram
    class Animal {
        +String name
        +int age
        +String species
        +makeSound()
        +eat()
        +sleep()
    }

    class Dog {
        +String breed
        +bark()
        +wagTail()
    }

    Animal <|-- Dog : inherits
```

**Complex class relationships:**
```mermaid
classDiagram
    class Vehicle {
        +String id
        +String brand
        +int year
        +start()
        +stop()
    }

    class Car {
        +int numDoors
        +String fuelType
        +openTrunk()
    }

    class Motorcycle {
        +String engineType
        +doWheelie()
    }

    class Engine {
        +int horsepower
        +String type
        +startEngine()
    }

    Vehicle <|-- Car
    Vehicle <|-- Motorcycle
    Car "1" *-- "1" Engine : has
    Motorcycle "1" *-- "1" Engine : has
```

### Class Relationships

```mermaid
classDiagram
    class User {
        +String username
        +String email
        +login()
        +logout()
    }

    class Order {
        +String orderId
        +Date orderDate
        +float total
        +addItem()
        +removeItem()
    }

    class Product {
        +String productId
        +String name
        +float price
        +getDetails()
    }

    User "1" --> "*" Order : places
    Order "*" --> "*" Product : contains
    User "1" --> "*" Product : reviews
```

## State Diagrams

### State Machine Visualization

**Basic state diagram:**
```mermaid
stateDiagram-v2
    [*] --> Still
    Still --> [*] : Stop
    Still --> Moving : Start
    Moving --> Still : Stop
    Moving --> Crashed : Crash
    Crashed --> [*] : Repair
```

**Complex state machine:**
```mermaid
stateDiagram-v2
    [*] --> Idle

    state "Processing Order" as OrderProcessing {
        [*] --> Received
        Received --> Validating : validate
        Validating --> Processing : valid
        Validating --> Rejected : invalid
        Processing --> Completed : done
        Processing --> Failed : error
        Completed --> [*]
        Failed --> [*]
        Rejected --> [*]
    }

    Idle --> OrderProcessing : new_order
    OrderProcessing --> Idle : finished
```

### Concurrent States

```mermaid
stateDiagram-v2
    [*] --> Active

    state Active {
        [*] --> Reading
        state Writing {
            [*] --> Draft
            Draft --> Reviewing
            Reviewing --> Published
            Reviewing --> Draft
        }
        Reading --> Writing : start_writing
        Writing --> Reading : finish_writing
    }

    Active --> [*] : logout
```

## Gantt Charts

### Project Timeline Visualization

**Basic Gantt chart:**
```mermaid
gantt
    title Website Development
    dateFormat  YYYY-MM-DD
    section Design
    Wireframes     :a1, 2024-01-01, 5d
    Mockups        :a2, after a1, 7d
    section Development
    Frontend       :a3, after a2, 14d
    Backend        :a4, after a1, 21d
    section Testing
    QA Testing     :a5, after a3, 10d
    section Deployment
    Launch         :a6, after a5, 2d
```

**Advanced Gantt chart with milestones:**
```mermaid
gantt
    title Mobile App Development
    dateFormat  YYYY-MM-DD
    axisFormat %m/%d

    section Planning
    Requirements     :done,    p1, 2024-01-01, 3d
    Architecture     :done,    p2, after p1, 2d
    Milestone 1      :milestone, m1, 2024-01-06, 0d

    section Development
    UI Design        :active,  d1, 2024-01-07, 10d
    Backend API      :         d2, 2024-01-08, 15d
    Database         :         d3, 2024-01-10, 8d
    Milestone 2      :milestone, m2, 2024-01-25, 0d

    section Testing
    Unit Tests       :         t1, after d2, 7d
    Integration      :         t2, after d3, 10d
    UAT              :         t3, after t2, 5d

    section Deployment
    App Store Release:         dep, after t3, 3d
```

## Git Graphs

### Version Control Visualization

**Basic git graph:**
```mermaid
gitGraph
    commit
    commit
    branch develop
    checkout develop
    commit
    commit
    checkout main
    merge develop
    commit
    branch feature
    checkout feature
    commit
    commit
    checkout main
    merge feature
    commit
```

**Advanced git workflow:**
```mermaid
gitGraph
    commit id: "Initial commit"
    branch develop
    checkout develop
    commit id: "Setup dev environment"

    branch feature-auth
    checkout feature-auth
    commit id: "Add user model"
    commit id: "Implement authentication"
    checkout develop
    merge feature-auth tag: "v0.1.0"

    branch feature-ui
    checkout feature-ui
    commit id: "Create layout components"
    commit id: "Add styling"
    checkout develop
    merge feature-ui

    checkout main
    merge develop tag: "v1.0.0"
    commit id: "Production release"
```

## Block Diagrams

### System Architecture Visualization

**Basic block diagram:**
```mermaid
block-beta
    columns 4
    db[(Database)] block:Server[Server]  rest[API] ui[UI]
    db --> block --> rest --> ui
```

**Complex system architecture:**
```mermaid
block-beta
    columns 4

    block:Users["User Layer"]
        service:Web[Web Client]
        service:Mobile[Mobile App]
        service:Desktop[Desktop App]
    end

    block:Gateway["API Gateway"]
        service:LoadBalancer[Load Balancer]
        service:Auth[Auth Service]
    end

    block:Services["Microservices"]
        service:UserService[User Service]
        service:OrderService[Order Service]
        service:PaymentService[Payment Service]
    end

    block:Data["Data Layer"]
        db[(User DB)]
        db[(Order DB)]
        db[(Payment DB)]
        cache[(Redis Cache)]
    end

    Users --> Gateway
    Gateway --> Services
    Services --> Data
```

## Integration and Usage

### In Markdown Files

**GitHub/GitLab integration:**
```markdown
# Process Flow

Here's our user authentication flow:

```mermaid
flowchart TD
    A[User Login] --> B{Valid Credentials?}
    B -->|Yes| C[Access Granted]
    B -->|No| D[Show Error]
    C --> E[Dashboard]
    D --> A
```
```

### Web Integration

**HTML example:**
```html
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
</head>
<body>
    <div class="mermaid">
        flowchart LR
            A[Start] --> B[Process]
            B --> C[End]
    </div>

    <script>
        mermaid.initialize({startOnLoad: true});
    </script>
</body>
</html>
```

### React/Vue Integration

**React component:**
```jsx
import React, { useEffect } from 'react';
import mermaid from 'mermaid';

const MermaidDiagram = ({ chart, id }) => {
  useEffect(() => {
    mermaid.initialize({ startOnLoad: true });
    mermaid.contentLoaded();
  }, []);

  return <div id={`mermaid-${id}`} className="mermaid">{chart}</div>;
};

// Usage
const MyFlow = () => {
  const flowChart = `
    flowchart TD
        A[React Component] --> B[State Management]
        B --> C[UI Rendering]
        C --> D[User Interaction]
  `;

  return <MermaidDiagram chart={flowChart} id="app-flow" />;
};
```

## Best Practices

### Diagram Design Principles

**Keep diagrams simple:**
- Limit to 15-20 nodes per diagram for readability
- Use clear, concise labels
- Group related elements together
- Use consistent styling

**Effective flowcharts:**
- Follow top-to-bottom or left-to-right flow
- Use decision points sparingly
- Color-code different types of actions
- Add meaningful annotations

**Sequence diagram tips:**
- Show clear message flow
- Use appropriate message types (sync, async, reply)
- Group related interactions
- Highlight important state changes

### Performance Optimization

**For web applications:**
```javascript
// Initialize Mermaid once
mermaid.initialize({
    startOnLoad: false,
    theme: 'default',
    themeVariables: {
        primaryColor: '#0066cc',
        primaryTextColor: '#333'
    }
});

// Render diagrams on demand
const renderDiagram = async (element, definition) => {
    const { svg } = await mermaid.render('mermaid-diagram', definition);
    element.innerHTML = svg;
};
```

### Accessibility Considerations

**Accessible Mermaid diagrams:**
- Provide alt text descriptions
- Use high-contrast colors
- Ensure keyboard navigation
- Include ARIA labels

```html
<div class="mermaid" aria-label="User authentication flowchart" role="img">
    flowchart TD
        A[Login] --> B{Valid?}
        B -->|Yes| C[Dashboard]
        B -->|No| D[Error]
</div>
```

## Troubleshooting

### Common Issues

**Diagrams not rendering:**
- Check JavaScript loading order
- Verify correct language identifier (`mermaid`)
- Ensure proper HTML escaping

**Syntax errors:**
- Validate indentation (spaces only, no tabs)
- Check for missing semicolons or brackets
- Verify node and edge syntax

**Using mermaid-cli for validation:**
If you have mermaid-cli installed, you can validate syntax:
```bash
# Test syntax by attempting to render
echo "flowchart TD; A-->B" | mmdc --input -
# If successful, syntax is valid
# If errors appear, check the console output for specific issues
```

For installation instructions, see the [official mermaid-cli repository](https://github.com/mermaid-js/mermaid-cli).

**Performance issues:**
- Large diagrams may slow page loading
- Consider lazy loading for complex diagrams
- Use appropriate SVG optimization

### Debug Tools

**Browser console:**
```javascript
// Enable debug mode
mermaid.initialize({
    logLevel: 'debug'
});

// Check diagram parsing
mermaid.parse('flowchart TD\nA-->B');
```

## Advanced Features

### Custom Themes

**Define custom theme variables:**
```javascript
mermaid.initialize({
    theme: 'base',
    themeVariables: {
        primaryColor: '#ffcc00',
        primaryTextColor: '#333333',
        primaryBorderColor: '#333333',
        lineColor: '#333333',
        secondaryColor: '#fff',
        tertiaryColor: '#fff'
    }
});
```

### Interactive Features

**Click handlers:**
```javascript
// Add click actions to nodes
const definition = `
flowchart LR
    A[Click Me] --> B{Action}

    click A "https://example.com"
    click B "alert('Decision point')"
`;
```

## Resources

- Official documentation: https://mermaid.js.org/
- Live editor: https://mermaid.live/
- GitHub repository: https://github.com/mermaid-js/mermaid
- Integration guides: https://mermaid.js.org/ecosystem/integration/
- Community Discord: https://discord.gg/mERmu2FpGJ
