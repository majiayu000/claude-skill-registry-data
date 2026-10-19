---
name: generate-diagram
description: >
  Generate visual diagrams for Löwy's Method architectures: call chain diagrams, sequence
  diagrams, swim lane activity diagrams, and layered architecture overviews. Use when the user
  asks to visualize an architecture, draw a call chain, produce a sequence diagram, create a
  swim lane diagram, or render the layered structure. Trigger on: "draw the call chain",
  "sequence diagram", "swim lane", "visualize the architecture", "diagram the flow",
  "show me the layers", "architecture diagram", or any request to produce a visual
  representation of a Löwy-style layered architecture or its call chains.
---

# Architecture Diagram Generation

**Read** `${CLAUDE_PLUGIN_ROOT}/references/composition.md` §5 (Call Chain Notation) and `${CLAUDE_PLUGIN_ROOT}/references/structure.md` §1
(The Four Layers) before generating diagrams.

You are producing visual representations of Löwy-style layered architectures.

## Diagram Types

### 1. Layered Architecture Overview
Shows all services organized by layer with the Utilities bar.

**Format:** Mermaid block diagram or ASCII.
**Layer colors (when supported):**
- Client layer: green
- Manager/Engine (Business Logic): yellow/amber
- ResourceAccess: gray
- Resource: blue
- Utility: purple

### 2. Call Chain Diagram
A simplified dependency graph superimposed on the layered architecture for a single use case.

**Notation:**
- `→` Solid arrow = synchronous request/response
- `⇢` or `-.->` Dashed arrow = queued/asynchronous call (through queue or message bus)
- Components colored by layer

**Mermaid template:**
```mermaid
graph TD
    subgraph Clients
        C1[ClientName]
    end
    subgraph Business Logic
        M1[ManagerName]
        E1[EngineName]
    end
    subgraph Resource Access
        RA1[AccessName]
    end
    subgraph Resources
        R1[ResourceName]
    end
    subgraph Utilities
        U1[UtilityName]
    end

    C1 --> M1
    M1 --> E1
    M1 --> RA1
    E1 --> RA1
    RA1 --> R1
    M1 -.-> U1
```

### 3. Sequence Diagram
UML-style with layer-colored lifelines. Use when:
- Call ordering matters
- Multiple interactions with the same component type
- Complex use cases
- Technical audience

**Mermaid template:**
```mermaid
sequenceDiagram
    participant C as Client
    participant M as Manager
    participant E as Engine
    participant RA as ResourceAccess
    participant R as Resource

    C->>M: initiateUseCase()
    M->>E: performActivity()
    E->>RA: atomicVerb()
    RA->>R: query/command
    R-->>RA: result
    RA-->>E: result
    E-->>M: result
    M-->>C: response
```

### 4. Swim Lane Activity Diagram
Use BEFORE drawing call chains to identify which services participate and how workflow
distributes across areas of interest. Each swim lane = one subsystem or area of concern.

## Workflow

### Step 1: Determine Diagram Type
Ask the user (or infer from context):
- Overview of the full architecture → Layered Architecture Overview
- How a specific use case flows → Call Chain or Sequence Diagram
- Pre-analysis of workflow distribution → Swim Lane

### Step 2: Gather Inputs
- The list of services and their layer assignments
- The use case(s) to diagram (for call chains / sequences)
- Any known communication patterns (sync, queued, pub/sub)

### Step 3: Generate the Diagram
- Use Mermaid syntax for portability
- Enforce layer ordering top-to-bottom: Client → Manager → Engine → RA → Resource
- Utilities in a separate group (accessible from any layer)
- Validate every arrow against closed-architecture rules before rendering

### Step 4: Annotate
Add notes for:
- Which relaxed rules are in play (e.g., Manager→RA skip)
- Any queued/async boundaries
- Event publications (dashed lines with «event» label)

## Validation Before Output
Before presenting any diagram, verify:
- [ ] No upward arrows (no calling up)
- [ ] No sideways arrows within a layer (except permitted relaxations)
- [ ] Manager is the orchestrator, not the Client
- [ ] Events published only by Managers (a Client may only post a use-case request to one Manager)
- [ ] Queued calls shown as dashed arrows
