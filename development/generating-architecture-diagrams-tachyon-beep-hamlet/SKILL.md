---
name: generating-architecture-diagrams
description: Generate C4 architecture diagrams from subsystem catalogs - codifies abstraction strategies, notation conventions, and selection criteria
---

# Generating Architecture Diagrams

## Purpose

Generate C4 architecture diagrams (Context, Container, Component levels) from subsystem catalogs, producing readable visualizations that communicate architecture without overwhelming readers.

## When to Use

- Coordinator delegates diagram generation from `02-subsystem-catalog.md`
- Task specifies writing to `03-diagrams.md`
- Need to visualize system architecture at multiple abstraction levels
- Output integrates with validation and final reporting phases

## Core Principle: Abstraction Over Completeness

**Readable diagrams communicate architecture. Overwhelming diagrams obscure it.**

Your goal: Help readers understand the system, not document every detail.

## Output Contract

When writing to `03-diagrams.md`, include:

**Required sections:**
1. **Context Diagram (C4 Level 1)**: System boundary, external actors, external systems
2. **Container Diagram (C4 Level 2)**: Major subsystems with dependencies
3. **Component Diagrams (C4 Level 3)**: Internal structure for 2-3 representative subsystems
4. **Assumptions and Limitations**: What you inferred, what's missing, diagram constraints

**For each diagram:**
- Title (describes what the diagram shows)
- Mermaid or PlantUML code block (as requested)
- Description (narrative explanation after diagram)
- Legend (notation explained)

## C4 Level Selection

### Level 1: Context Diagram

**Purpose:** System boundary and external interactions

**Show:**
- The system as single box
- External actors (users, administrators)
- External systems (databases, services, repositories)
- High-level relationships

**Don't show:**
- Internal subsystems (that's Level 2)
- Implementation details

**Example scope:** "User Data Platform and its external dependencies"

### Level 2: Container Diagram

**Purpose:** Major subsystems and their relationships

**Show:**
- Internal subsystems/services/plugins
- Dependencies between them
- External systems they connect to

**Abstraction strategies:**
- **Simple systems (≤8 subsystems)**: Show all subsystems individually
- **Complex systems (>8 subsystems)**: Use grouping strategies:
  - Group by category/domain (e.g., faction, layer, purpose)
  - Add metadata to convey scale (e.g., "13 skills", "9 services")
  - Reduce visual elements while preserving fidelity

**Don't show:**
- Internal components within subsystems (that's Level 3)
- Every file or class

**Example scope:** "15 plugins organized into 6 domain categories"

### Level 3: Component Diagrams

**Purpose:** Internal architecture of selected subsystems

**Selection criteria (choose 2-3 subsystems that):**
1. **Architectural diversity** - Show different patterns (router vs orchestrator, sync vs async)
2. **Scale representation** - Include largest/most complex if relevant
3. **Critical path** - Entry points, security-critical, data flow bottlenecks
4. **Avoid redundancy** - Don't show 5 examples of same pattern

**Show:**
- Internal components/modules/classes
- Relationships between components
- External dependencies for context

**Document selection rationale:**
```markdown
**Selection Rationale**:
- Plugin A: Largest (13 skills), shows router pattern
- Plugin B: Different organization (platform-based vs algorithm-based)
- Plugin C: Process orchestration (vs knowledge routing)

**Why Not Others**: 8 plugins follow similar pattern to A (redundant)
```

## Abstraction Strategies for Complexity

When facing many subsystems (10+):

### Strategy 1: Natural Grouping

**Look for existing structure:**
- Categories in metadata (AI/ML, Security, UX)
- Layers (presentation, business, data)
- Domains (user management, analytics, reporting)

**Example:**
```mermaid
subgraph "AI/ML Domain"
    YzmirRouter[Router: 1 skill]
    YzmirRL[Deep RL: 13 skills]
    YzmirLLM[LLM: 8 skills]
end
```

**Benefit:** Aligns with how users think about the system

### Strategy 2: Metadata Enrichment

**Add context without detail:**
- Skill counts: "Deep RL: 13 skills"
- Line counts: "342 lines"
- Status: "Complete" vs "WIP"

**Benefit:** Conveys scale without visual clutter

### Strategy 3: Strategic Sampling

**For Component diagrams, sample ~20%:**
- Choose diverse examples (not all similar)
- Document "Why these, not others"
- Prefer breadth over depth

**Benefit:** Readers see architectural variety without information overload

## Notation Conventions

### Relationship Types

Use different line styles for different semantics:

- **Solid lines** (`-->`) - Data dependencies, function calls, HTTP requests
- **Dotted lines** (`-.->`) - Routing relationships, optional dependencies, logical grouping
- **Bold lines** - Critical path, high-frequency interactions (if tooling supports)

**Example:**
```mermaid
Router -.->|"Routes to"| SpecializedSkill  # Logical routing
Gateway -->|"Calls"| AuthService          # Data flow
```

### Color Coding

Use color to create visual hierarchy:

- **Factions/domains** - Different color per group
- **Status** - Green (complete), yellow (WIP), gray (external)
- **Importance** - Highlight critical paths

**Document in legend:** Explain what colors mean

### Component Annotation

Add metadata in labels:

```mermaid
AuthService[Authentication Service<br/>Python<br/>342 lines]
```

## Handling Incomplete Information

### When Catalog Has Gaps

**Inferred components (reasonable):**
- Catalog references "Cache Service" repeatedly → Include in diagram
- **MUST document:** "Cache Service inferred from dependencies (not in catalog)"
- **Consider notation:** Dotted border or lighter color for inferred components

**Missing dependencies (don't guess):**
- Catalog says "Outbound: Unknown" → Document limitation
- **Don't invent:** Leave out rather than guess

### When Patterns Don't Map Directly

**Catalog says "Patterns Observed: Circuit breaker"**

**Reasonable:** Add circuit breaker component to diagram (it's architectural)

**Document:** "Circuit breaker shown based on pattern observation (not explicit component)"

## Documentation Template

After diagrams, include:

```markdown
## Assumptions and Limitations

### Assumptions
1. **Component X**: Inferred from Y references in catalog
2. **Protocol**: Assumed HTTP/REST based on API Gateway pattern
3. **Grouping**: Used faction categories from metadata

### Limitations
1. **Incomplete Catalog**: Only 5/10 subsystems documented
2. **Missing Details**: Database schema not available
3. **Deployment**: Scaling/replication not shown

### Diagram Constraints
- **Format**: Mermaid syntax (may not render in all viewers)
- **Abstraction**: Component diagrams for 3/15 subsystems only
- **Trade-offs**: Visual clarity prioritized over completeness

### Confidence Levels
- **High**: Subsystems A, B, C (well-documented)
- **Medium**: Subsystem D (some gaps in dependencies)
- **Low**: Subsystem E (minimal catalog entry)
```

## Mermaid vs PlantUML

**Default to Mermaid unless task specifies otherwise.**

**Mermaid advantages:**
- Native GitHub rendering
- Simpler syntax
- Better IDE support

**PlantUML when requested:**
```plantuml
@startuml
!include <C4/C4_Context>

Person(user, "User")
System(platform, "Platform")
Rel(user, platform, "Uses")
@enduml
```

## Success Criteria

**You succeeded when:**
- All 3 C4 levels generated (Context, Container, Component for 2-3 subsystems)
- Diagrams are readable (not overwhelming)
- Selection rationale documented
- Assumptions and limitations section present
- Syntax valid (Mermaid or PlantUML)
- Titles, descriptions, legends included
- Written to 03-diagrams.md

**You failed when:**
- Skipped diagram levels
- Created overwhelming diagrams (15 flat boxes instead of grouped)
- No selection rationale for Component diagrams
- Invalid syntax
- Missing documentation sections
- Invented relationships without noting as inferred

## Best Practices from Baseline Testing

### What Works

✅ **Faction-based grouping** - Reduce visual complexity (15 → 6 groups)
✅ **Metadata enrichment** - Skill counts, line counts convey scale
✅ **Strategic sampling** - 20% Component diagrams showing diversity
✅ **Clear rationale** - Document why you chose these examples
✅ **Notation for relationships** - Dotted (routing) vs solid (data)
✅ **Color hierarchy** - Visual grouping by domain
✅ **Trade-off documentation** - Explicit "what's visible vs abstracted"

### Common Patterns

**Router pattern visualization:**
- Show router as distinct component
- Use dotted lines for routing relationships
- Group routed-to components

**Layered architecture:**
- Use subgraphs for layers
- Show dependencies flowing between layers
- Don't duplicate components across layers

**Microservices:**
- Group related services by domain
- Show API gateway as entry point
- External systems distinct from internal services

## Integration with Workflow

This skill is typically invoked as:

1. **Coordinator** completes subsystem catalog (02-subsystem-catalog.md)
2. **Coordinator** validates catalog (optional validation gate)
3. **Coordinator** writes task specification for diagram generation
4. **YOU** read catalog systematically
5. **YOU** generate diagrams following abstraction strategies
6. **YOU** document assumptions, limitations, selection rationale
7. **YOU** write to 03-diagrams.md
8. **Validator** checks diagrams for syntax, completeness, readability

**Your role:** Translate catalog into readable visual architecture using abstraction and selection strategies.
