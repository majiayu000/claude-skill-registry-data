---
name: structurizr-architecture-sync
description: Maintain Structurizr C4 architecture diagrams (workspace.dsl) in sync with code changes so the model reflects the current system. Use when adding components (processors, handlers, repositories, entities), modifying component relationships, changing architectural boundaries, or implementing new patterns (CQRS, events, subscribers). Skip when `capabilities.structurizr` is false.
---

# Structurizr Architecture Synchronization

## Profile keys consumed

- `capabilities.structurizr`
- `project.name`
- `php.version`
- `framework.name`
- `architecture.source_root`
- `architecture.bounded_contexts`
- `architecture.shared_context`
- `persistence.engine`
- `make.start`
- `make.deptrac`

## Capability gate

This skill is gated on `capabilities.structurizr`. If the key is `false`
or absent, the repository does not maintain a Structurizr workspace:
record a skip note ("structurizr capability absent in profile") and stop.
Do not create a `workspace.dsl` from scratch under this skill.

## Context (Input)

Use this skill when:

- Adding new components (controllers, handlers, services, repositories)
- Creating new entities or aggregates
- Modifying component relationships or dependencies
- Implementing new architectural patterns (CQRS, events, subscribers)
- Adding infrastructure components (databases, caches, message brokers)
- Refactoring that changes component structure
- After fixing Deptrac violations (may indicate architecture drift)
- Creating new bounded contexts or modules
- Implementing new API endpoints with significant handlers

## Task (Function)

Keep the Structurizr workspace (`workspace.dsl`) synchronized with
codebase changes, ensuring C4 model diagrams accurately represent the
current system architecture.

**Success Criteria**:

- `workspace.dsl` contains all significant components
- Component relationships match actual code dependencies
- Layer groupings (Application/Domain/Infrastructure) are accurate
- Component descriptions reflect current purpose
- All infrastructure dependencies are documented
- C4 diagrams render without errors (check at
  `http://localhost:${STRUCTURIZR_PORT:-8080}`)

## Naming: derive from the profile, never hardcode

Element names in `workspace.dsl` come from the project profile, not from
this skill:

- **Software system and service container**: named after `project.name`.
- **Container technology label**: `PHP <php.version> / <framework.name>`.
- **Component sets / groups**: one per entry in
  `architecture.bounded_contexts`; shared-kernel components (when
  `architecture.shared_context` is non-null) are documented only when
  architecturally significant.
- **Database element**: named/typed after `persistence.engine`.

When editing an existing workspace, reuse the identifiers already defined
there — never rename established elements to match this skill's examples.

---

## Quick Start: Update Architecture in 5 Steps

### Step 1: Identify Architectural Changes

Determine if your code changes are architecturally significant:

**DO update workspace.dsl when adding**:

- Processors (HTTP/GraphQL handlers)
- Command Handlers (CQRS pattern)
- Event Subscribers (event-driven patterns)
- Entities (core domain objects)
- Domain Events (significant business events)
- Repositories (data access)
- Event Bus or infrastructure services
- External dependencies (DB, Cache, Message Broker)

**DON'T update for**:

- Factory classes
- Transformer classes (unless critical)
- Value objects (unless architecturally significant)
- Interface definitions (except hexagonal ports)
- Base classes
- DTOs and input/output objects
- Utility classes and helpers

**Decision rule**: if the class appears in a Deptrac layer boundary
discussion, dispatches/handles commands or events, or touches an external
system, document it. If it is a pure data carrier or construction helper,
omit it. **Target**: 15-25 components per diagram for clarity.

### Step 2: Add Component to Appropriate Group

Edit `workspace.dsl` and add the component in the correct layer group:

```dsl
group "Application" {
    newProcessor = component "NewProcessor" "Handles new requests" "RequestProcessor" {
        tags "Item"
    }
}
```

**Layers** (must mirror the hexagonal layers under
`architecture.source_root`):

- `group "Application"` - Controllers, Processors, Handlers, Subscribers
- `group "Domain"` - Entities, Domain Events
- `group "Infrastructure"` - Repositories, Event Bus, Infrastructure services

**External dependencies** (the `persistence.engine` database, cache,
message broker) go OUTSIDE groups at container level.

### Step 3: Define Relationships

Add relationships showing how your component interacts:

```dsl
// After all component definitions
newProcessor -> commandHandler "dispatches NewCommand"
commandHandler -> repository "uses"
repository -> database "accesses data"
```

**Common patterns**: entry point → handler (`dispatches <Command>`),
handler → aggregate/entity (`creates`, `updates`), handler → repository
(`uses`), repository → database (`reads/writes`), aggregate → event bus
(`publishes <Event>`), subscriber ← event bus (`subscribes to <Event>`).
Labels describe the actual code dependency, not a wish.

### Step 4: Verify Diagram Renders

View the updated diagram:

```bash
# Refresh browser (Structurizr Lite auto-reloads)
# Port is configurable via STRUCTURIZR_PORT in .env (default: 8080)
open http://localhost:${STRUCTURIZR_PORT:-8080}
# Navigate to "Diagrams" → the component view
```

**Check for**:

- No syntax errors displayed
- New component appears
- Relationships are visible
- Component is in correct layer group

### Step 5: Position and Save

1. **Drag components** in the UI to improve layout
2. **Click "Save workspace"** button (saves positions to `workspace.json`)
3. **Ship both files together**: `workspace.dsl` and `workspace.json`
   belong in the same commit/PR as the code change they document.

---

## Diagram as Code Workflow

### Setup

Structurizr Lite runs as part of the local container stack (boot via the
target mapped by `make.start`), typically declared in a compose override:

```yaml
structurizr:
  image: structurizr/lite:2024.07.02
  ports:
    - '${STRUCTURIZR_PORT}:8080'
  volumes:
    - ./:/usr/local/structurizr
```

**Access**: `http://localhost:${STRUCTURIZR_PORT:-8080}` (port
configurable via `.env`).

### Standard Development Flow

1. **Implement code changes** → Add handler, entity, repository
2. **Update workspace.dsl** → Add component + relationships
3. **View locally** → Refresh browser at configured port
4. **Position components** → Drag in UI, click "Save workspace"
5. **Ship together** → Code + workspace.dsl + workspace.json in same PR

### Manual Positioning in UI

**Automatic layout doesn't work well** - use manual positioning:

1. Open Structurizr UI in browser
2. Navigate to "Diagrams" → the component view
3. Drag components to arrange (left-to-right flow recommended)
4. Click "Save workspace" button in top-right
5. Positions saved to `workspace.json` in project root
6. Ship `workspace.json` with `workspace.dsl`

**Layout best practices**:

- Processors/Controllers on the left (entry points)
- Command Handlers in the middle (business logic)
- Repositories to the right of handlers
- Database/Cache/Message Broker on far right (external)

---

## Critical Principles

### What Makes a Good Architecture Diagram

**Clarity over Completeness**:

- 15-25 components (optimal readability)
- Focus on architectural significance
- Clear left-to-right or top-to-bottom flow
- External dependencies clearly visible

**Layer Separation**:

- Application: Entry points and orchestration
- Domain: Business logic and entities
- Infrastructure: Technical implementation

**Meaningful Relationships**:

- Show actual code dependencies
- Use descriptive labels
- Avoid circular dependencies

### Alignment with Deptrac

Layer groupings in `workspace.dsl` MUST match the layer configuration
enforced by the target mapped by `make.deptrac`:

```dsl
group "Application"     ↔  Application layer in deptrac.yaml
group "Domain"          ↔  Domain layer in deptrac.yaml
group "Infrastructure"  ↔  Infrastructure layer in deptrac.yaml
```

This ensures architecture documentation matches enforced boundaries.
If the diagram and Deptrac disagree, fix the diagram (or the code via
[deptrac-fixer](../deptrac-fixer/SKILL.md)) — never edit `deptrac.yaml`
to make the picture come true.

---

## Integration with Other Skills

Use this skill **after**:

- [implementing-ddd-architecture](../implementing-ddd-architecture/SKILL.md) - After creating domain model
- [api-platform-crud](../api-platform-crud/SKILL.md) - After adding API endpoints
- [deptrac-fixer](../deptrac-fixer/SKILL.md) - After fixing layer violations

Use this skill **before**:

- [documentation-sync](../documentation-sync/SKILL.md) - Update docs with architecture
- [ci-workflow](../ci-workflow/SKILL.md) - Validate all changes

---

## Troubleshooting

**Issue**: Structurizr UI shows "Element does not exist" error

**Solution**: Check that component variable names in relationships match
the component definitions exactly; filtered views referencing undefined
or excluded identifiers are the usual culprit.

---

**Issue**: Diagram shows components in wrong positions after pull

**Solution**: Ensure `workspace.json` is committed along with
`workspace.dsl`. The JSON file stores manual positions.

---

**Issue**: DSL syntax validation fails

**Solution**:

1. Check balanced braces `{}`
2. Verify all components are defined before relationships
3. Ensure no duplicate variable names

---

**Issue**: Too many components (30+), diagram is cluttered

**Solution**: Aim for 15-25 components. Omit DTOs, utilities, and
factories per the Step 1 DON'T list.

---

**Issue**: Can't determine if component should be documented

**Solution**: Apply the Step 1 decision rule — boundary-relevant,
command/event-dispatching, or external-system-touching classes are in;
data carriers and construction helpers are out.

## External Resources

- **Structurizr DSL Documentation**: <https://docs.structurizr.com/dsl>
- **C4 Model**: <https://c4model.com/>
- **Structurizr Lite**: <https://docs.structurizr.com/lite>
