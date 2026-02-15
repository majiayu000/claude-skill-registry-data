---
name: documenting-business-processes
description: Document business processes and workflows that a system implements. Describes end-to-end flows like user registration, order fulfillment, or payment processing — how domain entities move through the system. Use when (1) business workflows are undocumented, (2) a flow spans multiple components and no single component's docs tell the full story, (3) agents need to understand end-to-end behavior to implement changes, or (4) stakeholders need visibility into how the system handles a business process. NOT for development processes — those belong in skills and contribution guidelines.
---

# Documenting Business Processes

Document the business processes and workflows a system implements: how domain entities move through the system, what triggers each step, what the outcomes are, and what can go wrong. Business process docs tell the **end-to-end story** that no single component's documentation can tell on its own.

## Core Principles

1. **End-to-End Perspective**: Process docs describe a complete flow from trigger to outcome. They cross component boundaries — that's their purpose.
2. **Business Language**: Describe processes in business terms, referencing domain concepts. "User submits registration form" not "POST /api/v1/users handler validates input."
3. **NOT Development Processes**: This skill documents business workflows the system implements (user registration, order fulfillment). Development processes (how to test, deploy, contribute) belong in skills and contribution guidelines — not here.
4. **No Duplication Across Levels**: Reference domain docs for entity definitions and architecture docs for system structure. Process docs describe the FLOW — how entities traverse the architecture. Don't redefine domain terms or re-explain architectural patterns.
5. **Include Failure Paths**: Happy paths are easy. Document what happens when things go wrong — failed payments, validation errors, timeouts, partial completions.

## Documentation Hierarchy

```
Domain              ← Defines the entities involved in processes
  ↓
Architecture        ← Defines the system structure processes traverse
  ↓
Business Processes  ← You are here (end-to-end flows across the system)
  ↓
Components          ← Implements individual steps of processes
```

## Workflow

### Step 1: Discover Existing Documentation

Before writing anything:

1. Check for existing process docs, flow diagrams, or sequence diagrams
2. Read AGENTS.md for pointers to existing documentation
3. Check domain and architecture docs for references to processes
4. **If process docs already exist**: Understand their structure and extend them

### Step 2: Trace the Process

Follow the targeted process through the codebase:

1. Identify the trigger — what initiates this process (user action, scheduled job, external event)
2. Trace the happy path step by step across component boundaries
3. Identify decision points — where the flow branches based on conditions
4. Map failure modes — what can go wrong at each step and how the system handles it
5. Identify the outcomes — what state changes when the process completes (or fails)
6. Note any asynchronous steps, retries, or eventual consistency patterns

**Stay within the requested scope.** Document one process at a time.

### Step 3: Write Process Documentation

Follow the project's existing doc style. If none exists, use this structure:

```markdown
# <Process Name>

## Overview
<What this process accomplishes from a business perspective — 2-3 sentences>

## Trigger
<What initiates this process — user action, system event, schedule, external call>

## Actors
<Who or what is involved — users, services, external systems>
- <Actor>: <role in this process>

## Diagram
<Mermaid diagram visualizing the process flow — see diagram guidance below>

## Flow

### Happy Path
1. <Step 1> — <what happens, which component handles it>
2. <Step 2> — <what happens, which component handles it>
3. ...
<Result: what state changes when the process completes successfully>

### Failure Scenarios

#### <Failure Scenario 1>
- **Trigger**: <What causes this failure>
- **At step**: <Where in the flow it occurs>
- **Handling**: <How the system responds — rollback, retry, partial completion, error state>
- **User impact**: <What the user experiences>

#### <Failure Scenario 2>
...

## State Changes
<What entities are created, modified, or deleted when this process completes>
- <Entity>: <from state> → <to state>

## Dependencies
<External systems, services, or conditions this process relies on>
```

#### Mermaid Diagrams

Every process doc should include a mermaid diagram placed **before** the textual flow description. The diagram gives humans an instant visual overview; the text provides the detail.

Choose the diagram type based on the process shape:

- **Flowchart** (`flowchart TD`): Best for most processes — decision branches, parallel paths, error terminals. Use subgraphs to group related phases.
- **Sequence diagram** (`sequenceDiagram`): Best when the process is a back-and-forth between distinct actors or systems (e.g., sourcing chain, API handshakes).

Guidelines:
- Keep diagrams focused — show the main flow and key decision points, not every edge case
- Use descriptive node labels in business language, not function names
- Mark error terminals distinctly (e.g., red styling or stop symbols)
- Use subgraphs to separate phases when a process has distinct stages

### Step 4: Update AGENTS.md Pointers

If new documentation files were created, propose adding a pointer in AGENTS.md:

```markdown
## Business Processes
See `docs/processes/<process>.md` for <brief description>.
```

**Never put process details into AGENTS.md itself** — only add a pointer.

## Integration with Other Skills

- **documenting-domain**: Process docs reference domain entities (e.g., "creates a new User — see domain/users.md for the User entity definition"). Never redefine domain terms here.
- **documenting-architecture**: Process docs reference architectural patterns when relevant (e.g., "this step publishes an event via the event bus — see architecture/event-bus.md"). Never re-explain the architecture here.
- **documenting-components**: Component docs describe how individual steps are implemented; process docs describe the end-to-end flow across components.
- **project-feature-planning**: Process docs help agents understand the full impact of changes — modifying one step of a process affects the entire flow.

## Rules

- **Never document development processes** — testing, deployment, and CI/CD belong in skills and contribution guidelines
- **Never document all processes at once** — only the targeted process
- **Never redefine domain concepts or architectural patterns** — reference the appropriate docs
- **Always include failure paths** — happy-path-only docs are incomplete and misleading
- **Business language first** — describe what happens from the business perspective, then note which components are involved
- **Use reference-style links** — when linking to other docs or source files, use reference links (`[text][ref]` with `[ref]: path` at the bottom of the file) rather than inline links. They read better in source and are easier to maintain.
- **Propose structure first** — if no process docs exist yet, propose a directory structure and format before creating files
