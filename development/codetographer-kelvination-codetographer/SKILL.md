---
name: codetographer
description: |
  Generates interactive code flow diagrams (.cgraph files).
  Invoke when users ask: "how does X work", "show me the flow of Y",
  "visualize the architecture", "diagram the data flow",
  "create a graph of the codebase", or similar queries about
  understanding code structure and relationships.
version: "1.0.0"
---

# Codetographer Skill

## Purpose

Generate `.cgraph` files that visualize code architecture and flow.
These files can be viewed in VS Code with the Codetographer extension.

## When to Activate

- User asks how a feature/workflow works
- User wants to understand code relationships
- User requests architecture or flow diagrams
- User wants to visualize dependencies
- User asks to "graph", "diagram", or "map" code

## Output Format

Generate a `.cgraph` JSON file with this structure:

```json
{
  "version": "1.0",
  "metadata": {
    "title": "Feature Name",
    "description": "Brief explanation of what this graph shows",
    "generated": "2025-11-25T14:30:00Z",
    "scope": "src/relevant/path"
  },
  "nodes": [
    {
      "id": "unique-node-id",
      "label": "functionName()",
      "type": "function",
      "description": "What this function does in 1-2 sentences",
      "location": {
        "file": "src/path/to/file.ts",
        "startLine": 42,
        "endLine": 67
      },
      "group": "optional-group-id"
    }
  ],
  "edges": [
    {
      "id": "edge-1",
      "source": "source-node-id",
      "target": "target-node-id",
      "type": "calls"
    }
  ],
  "groups": [
    {
      "id": "group-id",
      "label": "Group Label",
      "description": "What this section represents"
    }
  ],
  "layout": {
    "direction": "TB"
  }
}
```

## Generation Process

### Step 1: Understand Scope

Identify what the user wants to visualize:

- A specific feature (e.g., "authentication flow")
- A subsystem (e.g., "database layer")
- A data flow (e.g., "how orders are processed")
- A dependency tree (e.g., "what depends on UserService")

Ask clarifying questions if the scope is unclear.

### Step 2: Find Relevant Code

Use Glob and Grep to locate:

- Entry points for the feature
- Key functions and classes
- Import/call relationships
- Related files in the scope

**CRITICAL: Keep it focused!** Only include 5-15 nodes maximum. Pick the most important functions/classes that explain the flow. Don't try to show everything.

### Step 3: Extract Locations

For each node, record:

- `file`: Relative path from workspace root (e.g., `src/auth/service.ts`)
- `startLine`: First line of function/class definition
- `endLine`: Last line (recommended)

**IMPORTANT**: Verify line numbers are accurate by reading the actual files.

### Step 4: Map Relationships

Create edges that show the PRIMARY flow. Rules:

- **One edge per relationship** - don't create multiple edges between the same nodes
- **Follow the main path** - show the happy path / primary flow first
- **Keep edges directional** - flow should go in one direction (usually top to bottom)
- **Don't create cycles** unless absolutely necessary for the explanation
- **No edge labels** - the relationship type is enough

### Step 5: Write Clear Descriptions

Every node MUST have a `description` field that explains:

- What this function/class does
- Why it exists in this flow
- **Start with a brief summary** (first sentence shown by default on the node)
- Add more detail after the first sentence if needed (expandable via + button)

**Format tip**: Write descriptions where the first sentence (~60 chars) works as a standalone summary.

Example:
- Good: "Validates user credentials against the database. Returns a JWT token on success or throws AuthError on failure."
- Bad: "This is where we check if the user has entered the correct password and username combination."

### Step 6: Generate File

Create `{feature-name}.cgraph` in project root with properly formatted JSON.

## Node Types

- `function`: Named functions and arrow functions
- `method`: Class methods
- `class`: Class definitions
- `module`: Files treated as logical units
- `file`: File-level grouping

## Edge Types

- `calls`: Direct function/method invocation (most common)
- `imports`: Module import relationship
- `extends`: Class inheritance
- `implements`: Interface implementation
- `uses`: General dependency or data flow

Each edge type is color-coded in the visualization:
- `calls` → Blue (shows active invocations)
- `extends` → Green (inheritance)
- `implements` → Purple (interface implementation)
- `imports`/`uses` → Gray (dependencies)

## Edge Importance

Use the optional `importance` field to control visual weight of edges:

- `primary`: Thick line, full opacity - for the main/critical flow path
- `secondary` (default): Normal line - for standard relationships
- `tertiary`: Thin line, reduced opacity - for minor/optional connections

### Example

```json
{
  "id": "e1",
  "source": "login-route",
  "target": "auth-service",
  "type": "calls",
  "importance": "primary"
}
```

### When to Use Importance

- Mark the **critical path** as `primary` (e.g., the main success flow)
- Leave most edges as `secondary` (default)
- Use `tertiary` for error handlers, logging, or optional dependencies

This helps readers instantly see which paths matter most.

## Custom Edge Colors

You can override the default edge type colors with custom colors:

```json
{
  "id": "e1",
  "source": "api-handler",
  "target": "database",
  "type": "calls",
  "color": "#ff6b6b"
}
```

Use custom colors when:
- You want to show different categories beyond the standard edge types
- You're using a legend to explain custom color meanings
- You want to highlight specific paths with distinct colors

## Legend

Add a legend to explain custom colors or categories in your graph:

```json
"legend": {
  "title": "Data Flow",
  "items": [
    { "color": "#ff6b6b", "label": "Write operations" },
    { "color": "#4ecdc4", "label": "Read operations" },
    { "color": "#ffe66d", "label": "Cache access" }
  ]
}
```

The legend appears in the bottom-left corner of the graph. Use it when:
- You have custom edge colors that need explanation
- You want to categorize edges beyond the standard types
- The graph has semantic meaning tied to colors

### Example with Legend

```json
{
  "version": "1.0",
  "metadata": { "title": "Database Operations" },
  "nodes": [...],
  "edges": [
    { "id": "e1", "source": "api", "target": "db", "type": "calls", "color": "#ff6b6b" },
    { "id": "e2", "source": "cache", "target": "api", "type": "calls", "color": "#4ecdc4" }
  ],
  "legend": {
    "title": "Operation Types",
    "items": [
      { "color": "#ff6b6b", "label": "Database write" },
      { "color": "#4ecdc4", "label": "Cache read" }
    ]
  }
}
```

## Layout Types

The `layout.type` field controls the overall layout algorithm:

- `layered` (default): Hierarchical tree layout, good for call flows and linear processes
- `force`: Compact web-like layout using physics simulation, good for interconnected systems
- `stress`: Balanced even-spacing layout, good for general relationship graphs

### When to Use Each Type

**Use `layered` (default) when:**
- Showing a clear flow from entry point to exit
- Visualizing call hierarchies
- The graph has a natural top-to-bottom or left-to-right direction

**Use `force` when:**
- The graph has many cross-connections (not strictly hierarchical)
- You want a compact view that fits on one screen
- Visualizing interconnected systems or dependency webs

**Use `stress` when:**
- You want evenly-spaced nodes regardless of hierarchy
- The relationships are bidirectional or cyclical
- Displaying general architecture without implied flow

### Example

```json
"layout": {
  "type": "force"
}
```

Or with direction (only applies to `layered`):

```json
"layout": {
  "type": "layered",
  "direction": "LR"
}
```

## Layout Directions (for layered type)

- `TB`: Top to bottom (default - use this for most flows)
- `LR`: Left to right (use for linear pipelines)
- `BT`: Bottom to top (rarely needed)
- `RL`: Right to left (rarely needed)

## Groups (Sections)

Use groups to visually organize related nodes into labeled sections. This is useful when:

- Nodes belong to distinct logical layers (e.g., "API Layer", "Service Layer", "Data Layer")
- You want to show component boundaries (e.g., "Frontend", "Backend")
- The flow crosses different modules or domains

### Group Definition

```json
"groups": [
  {
    "id": "api-layer",
    "label": "API Layer",
    "description": "HTTP request handlers"
  },
  {
    "id": "service-layer",
    "label": "Service Layer",
    "description": "Business logic"
  }
]
```

### Assigning Nodes to Groups

Add a `group` field to each node that should be in a group:

```json
{
  "id": "login-handler",
  "label": "handleLogin()",
  "type": "function",
  "group": "api-layer",
  ...
}
```

### When to Use Groups

- **Use groups** when you have 8+ nodes that naturally cluster into 2-4 logical sections
- **Don't use groups** for small graphs (under 6 nodes) - they add unnecessary visual complexity
- **Limit to 2-4 groups** - too many groups defeats the purpose of organization

## Best Practices

1. **LESS IS MORE**: 5-15 nodes maximum. If you need more, split into multiple graphs.
2. **One node per concept**: Don't create separate "descriptor" nodes - put the description IN the node's description field.
3. **Clear labels**: Use full function names like `handleLogin()` or `UserService.authenticate()`
4. **Always include descriptions**: Every node should explain what it does.
5. **Verify locations**: Double-check file paths and line numbers are accurate.
6. **Use relative paths**: From workspace root, not absolute paths.
7. **Use TB layout**: Top-to-bottom is easiest to follow for most flows.
8. **No edge labels**: The edge `type` is sufficient context.
9. **Use groups sparingly**: Only add groups for larger graphs with clear logical divisions.

## Anti-Patterns to Avoid

❌ **Don't do this:**
- Creating 30+ nodes (too complex)
- Adding "label" nodes that just describe a relationship
- Using edge labels (they clutter the visualization)
- Creating cycles that make the flow hard to follow
- Omitting descriptions from nodes
- Using LR layout for hierarchical call graphs

✅ **Do this instead:**
- Keep graphs focused and small
- Put all information IN the node (label, description, location)
- Let the edge type convey the relationship
- Create a clear top-to-bottom flow
- Always include meaningful descriptions
- Use TB layout for call hierarchies

## Example Output

For a request like "Show me how user authentication works":

```json
{
  "version": "1.0",
  "metadata": {
    "title": "User Authentication Flow",
    "description": "How login, token generation, and session management work",
    "generated": "2025-11-25T14:30:00Z",
    "scope": "src/auth"
  },
  "nodes": [
    {
      "id": "login-route",
      "label": "POST /api/login",
      "type": "function",
      "description": "API endpoint that receives login credentials from the client. Validates input format before delegating to the auth service.",
      "location": {
        "file": "src/routes/auth.ts",
        "startLine": 15,
        "endLine": 35
      }
    },
    {
      "id": "auth-service-login",
      "label": "AuthService.login()",
      "type": "method",
      "description": "Core authentication logic. Looks up the user, verifies password hash, and generates a JWT token on success.",
      "location": {
        "file": "src/services/auth.ts",
        "startLine": 42,
        "endLine": 78
      }
    },
    {
      "id": "user-repo-find",
      "label": "UserRepository.findByEmail()",
      "type": "method",
      "description": "Queries the database for a user record matching the provided email address.",
      "location": {
        "file": "src/repositories/user.ts",
        "startLine": 23,
        "endLine": 31
      }
    },
    {
      "id": "token-generate",
      "label": "generateToken()",
      "type": "function",
      "description": "Creates a signed JWT containing user ID and roles. Token expires in 24 hours by default.",
      "location": {
        "file": "src/utils/jwt.ts",
        "startLine": 8,
        "endLine": 22
      }
    }
  ],
  "edges": [
    {
      "id": "e1",
      "source": "login-route",
      "target": "auth-service-login",
      "type": "calls"
    },
    {
      "id": "e2",
      "source": "auth-service-login",
      "target": "user-repo-find",
      "type": "calls"
    },
    {
      "id": "e3",
      "source": "auth-service-login",
      "target": "token-generate",
      "type": "calls"
    }
  ],
  "layout": {
    "direction": "TB"
  }
}
```

## After Generation

Tell the user:

1. The file was created at `{filename}.cgraph`
2. Open it in VS Code (requires Codetographer extension)
3. Click a node to highlight its connections
4. Click the `+` button on a node to expand its description
5. Cmd+Click (or Ctrl+Click) a node to jump to that code location
