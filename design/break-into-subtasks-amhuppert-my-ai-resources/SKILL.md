---
name: break-into-subtasks
description: This skill should be used when breaking down frontend feature requirements into parallelizable work items (API clients, UI components, and integration tasks) with clear dependencies. Particularly useful for creating structured work breakdowns with Mermaid diagrams and organizing tasks for team development.
---

# Break Into Subtasks

## Overview

Guide for analyzing requirements and breaking down frontend work into parallelizable, well-organized tasks.

**Context:** Modern frontend architecture with API clients (Zod schemas + React Query hooks) separate from presentational UI components, connected via integration tasks.

## When to Use This Skill

Use this skill when:

- Analyzing frontend feature requirements
- Breaking down work into parallelizable tasks
- Creating structured work breakdowns with dependency visualization
- Planning team development with clear task assignments
- Organizing features for independent shipping

## Workflow

### 1. Requirements Analysis

**Objective:** Understand the feature completely before planning work.

**Steps:**

1. Read all provided requirements documents thoroughly
2. Identify unclear or ambiguous requirements
3. Ask clarifying questions about:
   - Missing technical details
   - Ambiguous user flows
   - Undefined data contracts
   - Integration points with existing systems
4. Confirm interpretation of requirements with the user before proceeding

**Example Questions:**

- "What exactly is shown when user clicks X?"
- "How is Y determined - frontend or backend?"
- "Should this use existing component Z or build new?"

### 2. Identify High-Level Features

**Objective:** Group related functionality into user-facing features.

**Guidelines:**

- Each feature should represent a complete user workflow or capability
- Features should be independently valuable (can ship separately)
- Group related UI and interactions together
- Typical feature size: 3-8 work items

**Example Features:**

- "Create Location - Drop-a-Pin"
- "Locations Map Layer"
- "Location Details Panel"

### 3. Break Down into Three Work Item Types

For each feature, identify work in three categories:

#### 3.1 API Endpoint Clients

**What:** Zod schemas, data validation/parsing, and React Query hooks for API endpoints.

**Characteristics:**

- Not tied to any specific feature (shared infrastructure)
- Can ALL start immediately with no dependencies
- One work item per unique endpoint
- Reusable across multiple features

**Format:** `{Endpoint Name} - client`

**Examples:**

- "Create Location - client"
- "Get All Locations - client"
- "Address Search - client"

#### 3.2 UI Components

**What:** Presentational components that receive data via props/context.

**Characteristics:**

- Built independently of API implementation
- Can start immediately (parallel with API clients)
- Should be presentational/display-focused
- May include local interaction logic

**Examples:**

- "Location Markers component"
- "Save New Location modal"
- "Address search modal and results dropdown"

#### 3.3 Integration Tasks

**What:** Wire API clients to UI components to create working features.

**Characteristics:**

- Depends on specific API client(s) being complete
- Depends on specific UI component(s) being complete
- Cannot start until dependencies are ready
- Represents completion of feature functionality

**Format:** Descriptive task name with dependencies noted

**Examples:**

- "Wire drop-a-pin flow" (depends on: Create Location - client)
- "Render markers from API data" (depends on: Get All Locations - client)
- "Wire list with all actions" (depends on: Get All Locations - client, Update Location - client, Delete Location - client)

### 4. Create Mermaid Diagram

**Purpose:** Visualize work order, dependencies, and parallelization opportunities.

**Structure:**

```mermaid
flowchart TD
    %% API clients at top level (no grouping)
    API1[{Endpoint Name} - client]
    API2[{Endpoint Name} - client]

    %% Features as subgraphs
    subgraph Feature1["🎯 Feature Name"]
        direction TB
        F1_UI1[UI: Component name]
        F1_INT[Integration: Task name]
        F1_DONE[✅ Feature Complete]

        F1_UI1 --> F1_INT
        F1_INT --> F1_DONE
    end

    %% Dependencies
    API1 --> F1_INT
```

**Requirements:**

1. **Comprehensive inline comments**:
   - Purpose of diagram at top
   - Key rules and critical constraints
   - Purpose of each subgraph
   - Explanation of dependencies
   - Parallelization opportunities

2. **API Endpoint Clients:**
   - Place at top level (not in subgraph)
   - Name format: `{Endpoint Name} - client`
   - No dependencies between them

3. **Feature Subgraphs:**
   - Emoji prefix for visual identification
   - Direction: TB (top to bottom)
   - Contains: UI components → Integration tasks → Feature Complete milestone
   - Internal dependencies with arrows

4. **Dependencies:**
   - API client → Integration task (solid arrows)
   - UI component → Integration task (solid arrows)
   - Feature → Feature (only if truly blocked, avoid if possible)

5. **Avoid:**
   - Dotted lines (unless explicitly needed)
   - Foundation boxes that clutter without adding value
   - Feature dependencies that don't represent real blockers
   - Grouping API clients (keep them top-level)

### 5. Write Work Items in Markdown

**Structure:**

```markdown
## Work Items

### API Endpoint Clients

Build Zod schemas, data parsers, and React Query hooks for each endpoint. These can all be started immediately with no dependencies.

- **{Endpoint Name} - client**
- **{Endpoint Name} - client**

### {Feature Name}

**UI Components:**

- Component name and brief description
- Component name and brief description

**Integration:**

- Integration task name
  - _Depends on: {API Client Name}, {API Client Name}_
- Integration task name
  - _Depends on: {API Client Name}_
```

**Requirements:**

1. **API Endpoint Clients section first** - List all with note about no dependencies
2. **One section per feature** - Matching Mermaid diagram
3. **UI Components subsection** - List all presentational components
4. **Integration subsection** - List integration tasks with italicized dependencies
5. **Dependency format** - `*Depends on: {Client Name}, {Client Name}*`

## Quality Checklist

Before finalizing work breakdown:

- [ ] All API endpoints have corresponding client work items
- [ ] All UI components are listed under their primary feature
- [ ] Every integration task lists its API client dependencies
- [ ] Shared API clients are not duplicated across features
- [ ] Features are independently valuable
- [ ] Parallelization opportunities are maximized
- [ ] Dependencies are necessary (not assumed from user flow)
- [ ] Work items are specific enough to become JIRA tickets

## Common Patterns

### Shared Components

If a UI component is used by multiple features (e.g., "Create location button & dropdown"), extract it from individual features to avoid duplication. List it separately, similar to API clients. Both features' integration tasks will depend on it, but it appears only once in the work breakdown.

### Multi-Step Integrations

Some features have sequential integration steps:

```
Integration 1 (search) → Integration 2 (create from search result)
```

Show this in both Mermaid (arrows between integration nodes) and Markdown (separate integration items).

### CRUD Features

Features with Create/Read/Update/Delete typically need:

- 4 API clients (one per operation)
- Modal/form UI components for each operation
- Integration task that wires all operations together

## Anti-Patterns to Avoid

❌ **Grouping API clients in subgraph** - They're shared infrastructure, keep top-level
❌ **Creating feature dependencies without real blockers** - Maximize parallelization
❌ **Vague integration tasks** - Be specific about what's being wired
❌ **Missing dependency notation** - Always note which API clients are needed
❌ **Insufficient Mermaid comments** - AI agents need context in the diagram itself
❌ **Too granular** - Work items should be JIRA-ticket sized, not hour-by-hour tasks
❌ **Too broad** - "Build entire feature" isn't useful; break into client/UI/integration

## Example Application

Given: "Users can view a list of items and filter by category"

**Analysis:**

- High-level feature: "Items List"
- Needs: API for items, UI for list display, UI for filters, integration

**Breakdown:**

- API: "Get Items - client"
- UI: "Items List Panel", "Category filter component"
- Integration: "Wire items list with filtering" (depends on: Get Items - client)

**Not separate features:** Filtering is part of the list feature, not independent.

---

**Remember:** The goal is maximum parallelization while maintaining clear dependencies. When in doubt, avoid creating blocking relationships between features.
