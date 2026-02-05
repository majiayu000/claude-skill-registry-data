---
name: c4-diagrams
description: Creates and manages C4 architecture diagrams using PlantUML. Use when the user wants to visualize software architecture, create context/container/component/sequence diagrams, document system design with the C4 model, or mentions architecture diagrams, system design, or PlantUML. Supports iterative diagram building through conversational workflow.
license: Complete terms in LICENSE.txt
---

# C4 Architecture Diagrams

This skill helps you create and manage C4 architecture diagrams using the PlantUML format. C4 diagrams provide a hierarchical way to visualize software architecture at different levels of detail, from high-level system context down to low-level components.

The C4 model uses four diagram types:
- **Context**: Shows the system in its environment with external actors and systems
- **Container**: Zooms into the system to show high-level technical building blocks
- **Component**: Zooms into a container to show its internal structure
- **Sequence**: Shows how elements interact with each other over time

All diagrams are stored as `.puml` files in `doc/diagrams/` and rendered to PNG images using the public PlantUML server.

## Requirements

Before using this skill, ensure you have:
- **Bash** - For directory setup (available on Linux, macOS, WSL)
- **Python 3.6+** - For diagram rendering (uses standard library only, no pip install needed)
- **Internet access** - To reach the public PlantUML server (https://www.plantuml.com/plantuml/)
- **File system write permissions** - In your project's working directory

**Note:** This skill uses only standard library dependencies. No package managers or external installations required beyond Python itself.

## 🚀 High-Level Workflow

Creating C4 diagrams follows a five-phase workflow:

1. **Initialize Directory Structure** - Set up `doc/diagrams/` with subdirectories for each diagram type
2. **Choose Diagram Type & Create File** - Select appropriate diagram type and initialize from template
3. **Add Elements** - Define the entities in your diagram (people, systems, containers, components)
4. **Define Relationships** - Connect elements with labeled relationships
5. **Render Diagram** - Generate PNG image from PlantUML source

Each phase includes validation steps to ensure correctness before proceeding to the next phase.

---

## Phase 1: Initialize Directory Structure

### 1.1 Check for Existing Structure

**Before creating diagrams**, verify that the directory structure exists:

Use the Bash tool to check:
```bash
ls -la doc/diagrams 2>/dev/null
```

If the output shows subdirectories `context/`, `container/`, `component/`, and `sequence/`, proceed to Phase 2.

### 1.2 Create Directory Structure

**If the structure doesn't exist**, run the initialization script:

```bash
bash .claude/skills/c4-diagrams/scripts/init-structure.sh
```

**Expected behavior:**
- Creates `doc/diagrams/` at project root if missing
- Creates four subdirectories:
  - `doc/diagrams/context/` - For context-level diagrams
  - `doc/diagrams/container/` - For container-level diagrams
  - `doc/diagrams/component/` - For component-level diagrams
  - `doc/diagrams/sequence/` - For sequence diagrams
- Reports what was created or verified
- Idempotent: safe to run multiple times

### 1.3 Verify Success

**After running the script**, confirm the structure was created:

```bash
ls -R doc/diagrams
```

You should see all four subdirectories.

**Error handling:**
- If the script fails with a permission error, ensure you have write permissions in the project directory
- If you're in the wrong directory, navigate to the project root first
- The script will provide specific error messages to guide troubleshooting

---

## Phase 2: Choose Diagram Type & Create File

### 2.1 Understand Diagram Types

Choose the appropriate diagram type based on what you want to visualize:

**Context Diagrams** (`context/`)
- **Purpose**: Show the system in its environment
- **Elements**: People, systems, external systems
- **Use when**: Explaining what the system does and who uses it
- **Audience**: Everyone (technical and non-technical)

**Container Diagrams** (`container/`)
- **Purpose**: Show high-level technical building blocks
- **Elements**: Web apps, mobile apps, databases, microservices
- **Use when**: Explaining the system's runtime architecture
- **Audience**: Technical stakeholders (developers, architects)

**Component Diagrams** (`component/`)
- **Purpose**: Show components within a container
- **Elements**: Controllers, services, repositories, modules
- **Use when**: Explaining internal structure of a specific container
- **Audience**: Developers working on the system

**Sequence Diagrams** (`sequence/`)
- **Purpose**: Show interactions between elements over time
- **Elements**: Any of the above, with time-ordered relationships
- **Use when**: Explaining workflows, processes, or API call chains
- **Audience**: Developers and architects
- **⚠️ Important constraints**:
  - ❌ **NO boundaries** - Container_Boundary, System_Boundary are not supported
  - ❌ **NO _Ext suffixes** - Use Container(), not Container_Ext()
  - ✅ Participants must be in a **flat list** (no nesting or grouping structures)
  - ✅ Relationships are **time-ordered** from top to bottom

**For detailed guidance on when to use each type**, see [Diagram Types Guide](./reference/diagram-types.md).

### 2.2 Check if Diagram Already Exists

**Before creating a new diagram**, check if it already exists:

Determine the diagram name (convert to lowercase, replace spaces with hyphens):
- User says: "Create a system context diagram" → name: `system-context`
- User says: "Web application container diagram" → name: `web-application`

Check for existing file:
```bash
ls doc/diagrams/{type}/{name}.puml 2>/dev/null
```

**If the file exists:**
- Read the file using the Read tool to understand its current state
- Skip to Phase 3 or Phase 4 to modify it

**If the file doesn't exist:**
- Continue to create a new diagram

### 2.3 Initialize New Diagram from Template

**To create a new diagram**, read the appropriate template and write it to the target location:

1. Read the template:
   ```
   Read .claude/skills/c4-diagrams/templates/{type}.puml
   ```
   Where `{type}` is one of: `context`, `container`, `component`, `sequence`

2. Optionally customize the template:
   - Replace title placeholder with user-specified title
   - Add initial comments or notes
   - Keep all C4-PlantUML directives intact

3. Write to target location:
   ```
   Write doc/diagrams/{type}/{name}.puml
   ```

**Validation:**
- Verify the file was created: `ls doc/diagrams/{type}/{name}.puml`
- Briefly read the file to confirm contents
- Proceed to Phase 3

---

## Phase 3: Add Elements

### 3.1 Parse Current Diagram State

**Before adding elements**, read the diagram file to understand what's already there:

```
Read doc/diagrams/{type}/{name}.puml
```

**Identify:**
- Existing elements (Person, System, Container, Component)
- Any boundaries or groupings
- Current layout and organization

### 3.2 Determine Elements to Add

**Based on the user's request**, identify what elements need to be added:

**Common element types by diagram:**

**Context diagrams:**
- `Person(id, "Name", "Description")` - Users and actors
- `System(id, "Name", "Description")` - Your system
- `System_Ext(id, "Name", "Description")` - External systems

**Container diagrams:**
- `Container(id, "Name", "Technology", "Description")` - Apps, services, databases
- `ContainerDb(id, "Name", "Technology", "Description")` - Databases specifically
- `ContainerQueue(id, "Name", "Technology", "Description")` - Message queues

**Component diagrams:**
- `Component(id, "Name", "Technology", "Description")` - Components within a container
- `ComponentDb(id, "Name", "Technology", "Description")` - Database components
- `ComponentQueue(id, "Name", "Technology", "Description")` - Queue components

**Sequence diagrams:**
- Use the same element types as above (Person, Container, Component, etc.)
- ⚠️ **CRITICAL**: Do NOT use boundaries (System_Boundary, Container_Boundary) - sequence diagrams require a **flat participant list**
- ⚠️ **CRITICAL**: Do NOT use _Ext suffixes (System_Ext, Container_Ext, ContainerDb_Ext) - use regular variants instead
- Example: Use `Container(cache, "Cache", "Redis", "Desc")` not `Container_Ext(...)`

**Boundaries** (Context/Container/Component diagrams only - NOT sequence):
```
System_Boundary(id, "Name", "Optional Description") {
  // Elements inside the boundary (indented with 2 spaces)
}
```

**For complete syntax reference**, see [Syntax Reference](./reference/syntax-reference.md).

### 3.3 Add Element Definitions

**To add elements**, use the Edit tool to insert element definitions at the appropriate location:

**Important syntax rules:**
- **IDs must be valid identifiers**: Use letters, numbers, underscores only
- **Sanitize IDs**: Replace hyphens and special characters with underscores
  - Example: "web-app" → "web_app"
  - Example: "API Gateway" → "API_Gateway"
- **Technology parameter**: Required for Container and Component elements (3rd parameter)
- **Quote all strings**: Names, technologies, and descriptions must be in quotes

**Example additions:**

For a context diagram:
```plantuml
Person(user, "User", "A customer using the system")
System(main_system, "Main System", "The core application")
System_Ext(payment_gateway, "Payment Gateway", "External payment processor")
```

For a container diagram:
```plantuml
Container(web_app, "Web Application", "React", "Provides UI for users")
ContainerDb(database, "Database", "PostgreSQL", "Stores application data")
Container(api, "API Server", "Node.js/Express", "Handles business logic")
```

### 3.4 Validate Element Additions

**After adding elements**, verify correctness:

1. Read the edited file to confirm changes
2. Check for syntax errors:
   - Unclosed parentheses
   - Missing quotes
   - Invalid IDs (hyphens, spaces, special characters)
   - Missing technology parameter for containers/components
3. Ensure all elements have proper types, names, and descriptions
4. Fix any errors before proceeding to Phase 4

---

## Phase 4: Define Relationships

### 4.1 Parse Existing Elements and Relationships

**Before adding relationships**, read the diagram to identify:

1. All defined elements and their IDs
2. Existing relationships (to avoid duplicates)
3. Logical connections that need to be added

### 4.2 Determine Relationships to Add

**Based on the user's request and diagram logic**, identify which elements should be connected:

**Relationship syntax:**
```plantuml
Rel(source_id, target_id, "Description")
Rel(source_id, target_id, "Description", "Technology/Protocol")
```

**Directional variants** (optional, for layout control):
- `Rel_U` - Relationship pointing up
- `Rel_D` - Relationship pointing down
- `Rel_L` - Relationship pointing left
- `Rel_R` - Relationship pointing right

**Examples:**
```plantuml
Rel(user, web_app, "Uses", "HTTPS")
Rel(web_app, api, "Makes API calls", "REST/JSON")
Rel(api, database, "Reads/writes", "JDBC")
Rel(main_system, payment_gateway, "Processes payments", "API")
```

### 4.3 Add Relationship Definitions

**To add relationships**, use the Edit tool to insert them after the element definitions:

**Best practices:**
- Add relationships in a dedicated section (after all elements)
- Group related relationships together
- Use descriptive labels that explain the interaction
- Include technology/protocol information when relevant

**For sequence diagrams:**
- Relationships are time-ordered (top to bottom)
- Use dividers to group logical steps: `== Step Name ==`
- Consider using `group` blocks for sub-processes:
  ```plantuml
  == Authentication ==
  group Login Process
    Rel(user, api, "Submits credentials")
    Rel(api, database, "Verifies user")
  end
  ```

### 4.4 Validate Relationships

**After adding relationships**, verify correctness:

1. Confirm both source and target IDs exist in the diagram
2. Check that relationship directions make logical sense
3. Ensure descriptions are clear and meaningful
4. Verify technology/protocol parameters are accurate
5. For sequence diagrams, confirm ordering is correct

**If validation fails:**
- Fix ID mismatches
- Correct syntax errors
- Adjust descriptions for clarity
- Re-read the file to verify fixes

---

## Phase 5: Render Diagram

### 5.1 Generate PNG from PUML

**To render the diagram**, run the rendering script:

```bash
python3 .claude/skills/c4-diagrams/scripts/render-diagram.py doc/diagrams/{type}/{name}.puml
```

**Example:**
```bash
python3 .claude/skills/c4-diagrams/scripts/render-diagram.py doc/diagrams/context/system-context.puml
```

**Expected behavior:**
- Reads the PUML file
- Encodes content for PlantUML server
- POSTs to https://www.plantuml.com/plantuml/
- Saves PNG response to same directory with same name
- Example: `doc/diagrams/context/system-context.png`

### 5.2 Verify Output

**After rendering**, confirm the PNG was created:

```bash
ls -lh doc/diagrams/{type}/{name}.png
```

**The script includes:**
- **Retry logic**: Attempts up to 3 times with exponential backoff (1s, 2s, 4s delays)
- **Timeout handling**: 15 second timeout per request
- **Clear error messages**: Specific errors for network, syntax, and server issues

### 5.3 Error Handling

**If rendering fails**, the script will provide specific error messages:

**Network errors:**
- Connection issues or timeouts
- Check internet connectivity
- Try again after a few moments

**HTTP 400 errors:**
- Invalid PlantUML syntax in the PUML file
- Read the file and check for syntax errors
- Common issues: unclosed boundaries, missing quotes, invalid IDs
- Manually validate at https://www.plantuml.com/plantuml/uml/

**HTTP 429 errors:**
- Rate limited by server
- Wait a minute before retrying
- Consider reducing render frequency

**HTTP 5xx errors:**
- PlantUML server issues
- Try again later
- Server typically recovers quickly

### 5.4 Next Steps

**After successful rendering:**

**Option 1: Iterate on the diagram**
- View the generated PNG
- If changes needed, return to Phase 3 or 4
- Edit elements or relationships
- Re-render (return to Phase 5.1)

**Option 2: Create additional diagrams**
- Return to Phase 2 to create a new diagram
- Consider creating diagrams at different levels:
  - Start with Context (big picture)
  - Add Container (technical structure)
  - Add Component (internal details)
  - Add Sequence (workflows)

**Option 3: Explore advanced features**
- Load [Best Practices Guide](./reference/best-practices.md) for design tips
- Load [C4 Model Concepts](./reference/c4-model.md) to understand deeper principles
- Load [C4-PlantUML Library Docs](./reference/c4-plantuml-readme.md) for advanced syntax

---

## Common Pitfalls

❌ **Don't** use hyphens in element IDs → ✅ **Do** use underscores:
```plantuml
System(web-app, "Web App", "Desc")      // WRONG
System(web_app, "Web App", "Desc")      // CORRECT
```

❌ **Don't** omit technology for containers/components → ✅ **Do** always include it:
```plantuml
Container(api, "API Server", "Handles logic")               // WRONG
Container(api, "API Server", "Node.js", "Handles logic")    // CORRECT
```

❌ **Don't** forget closing braces → ✅ **Do** always close boundaries:
```plantuml
System_Boundary(backend, "Backend") {
  Container(api, "API", "Node.js", "Server")
// WRONG - missing }
}  // CORRECT
```

❌ **Don't** reference undefined IDs → ✅ **Do** ensure all IDs are defined:
```plantuml
Rel(user, app, "Uses")  // WRONG if 'user' not defined first
```

❌ **Don't** use boundaries in sequence diagrams → ✅ **Do** use flat participant lists:
```plantuml
' WRONG - sequence diagrams don't support boundaries
Container_Boundary(backend, "Backend") {
  Container(api, "API", "Node.js", "Server")
}

' CORRECT - flat list of participants
Container(api, "API", "Node.js", "Server")
```

❌ **Don't** use _Ext suffixes in sequence diagrams → ✅ **Do** use regular variants:
```plantuml
Container_Ext(cache, "Cache", "Redis", "Cache")     // WRONG in sequence
Container(cache, "Cache", "Redis", "Cache")          // CORRECT
```

⚠️ **Important:** Place diagrams in correct subdirectories (`doc/diagrams/context/`, `container/`, `component/`, `sequence/`)

⚠️ **Important:** Validate PUML syntax before rendering to avoid errors and server requests

⚠️ **Important:** Sequence diagrams have unique syntax constraints - see template and syntax reference

---

## Reference Documentation

Load these on-demand for deeper information:

- **[C4 Model Concepts](./reference/c4-model.md)** - Theory, principles, and abstraction levels
- **[Diagram Types Guide](./reference/diagram-types.md)** - When to use each type, examples, audience considerations
- **[Syntax Reference](./reference/syntax-reference.md)** - Complete macro reference, ID rules, boundaries, relationships
- **[Best Practices](./reference/best-practices.md)** - Design patterns, layout, naming, anti-patterns
- **[C4-PlantUML Library Documentation](./reference/c4-plantuml-readme.md)** - Complete upstream docs, advanced features, customization
