---
skill: c4-diagram
model: sonnet
description: Generate C4 architecture diagrams from system notes
tags: [activity/architecture, domain/tooling, type/diagram]
---

# /c4-diagram Skill

Generate Mermaid C4 diagrams from System note frontmatter data.

## When to Use This Skill

Use `/c4-diagram` when you need to generate C4 architecture diagrams in Mermaid format from the structured `c4:` data stored in System note frontmatter. This complements the `/diagram` skill (which generates Python `diagrams` PNGs) by producing inline Mermaid that renders natively in Obsidian.

## Usage

```
/c4-diagram <system-name> [level]
```

### Arguments

| Argument      | Required | Description                                             |
| ------------- | -------- | ------------------------------------------------------- |
| `system-name` | Yes      | Name of the System note (e.g., `CRM`, `ERP`, `SAP BTP`) |
| `level`       | No       | `context` (L1, default), `container` (L2), or `both`    |

### Examples

```
/c4-diagram CRM
/c4-diagram ERP container
/c4-diagram SAP BTP both
```

## Instructions

### Phase 1: Read System Data

1. Find the System note matching the name argument:
   - Search for `System - <name>.md` in the vault root
   - If not found, try graph query: `node scripts/graph-query.js --search "<name>" --type System`

2. Read the note and extract the `c4:` frontmatter section. Required fields:
   - `c4.actors` - People/roles (for Context diagram)
   - `c4.containers` - Internal services (for Container diagram)
   - `c4.externalRelationships` - External system connections
   - `c4.internalRelationships` - Container-to-container connections
   - `c4.description` - System description
   - `c4.boundary` - Whether system is internal or external

3. If `c4:` data is missing or empty, inform the user:
   > This system note has no `c4:` data. Add C4 architecture data to the frontmatter first. See the System template for the schema.

### Phase 2: Generate Mermaid C4

Generate the Mermaid code following these **best practices**:

#### General Rules

- **Maximum 10 elements** per diagram (actors + systems + containers)
- **Descriptions under 40 characters** - truncate if needed
- **Use directional relationships** - `Rel_D` (down) for primary flow, `Rel_R` (right) for secondary
- **Order**: Persons → System Boundary → External Systems → Relationships → Config
- **Always include** `UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")` at the end
- **Alias naming**: Use camelCase without spaces (e.g., `dataEngineer`, `sapS4hana`)
- **Strip wiki-link syntax** from target names (e.g., `[[System - CRM]]` → `CRM`)

#### C4 Context Diagram (Level 1)

Generate a `C4Context` diagram:

```mermaid
C4Context
    title <System Name> - System Context

    %% Actors (from c4.actors)
    Person(<alias>, "<name>", "<description>")

    %% The system itself
    System(<sysAlias>, "<System Name>", "<c4.description>")

    %% External systems (from c4.externalRelationships targets)
    System_Ext(<alias>, "<target name>", "<brief description>")

    %% Relationships
    %% Actor → System (from c4.actors[].relationship)
    Rel_D(<actorAlias>, <sysAlias>, "<relationship>", "")

    %% System → External (from c4.externalRelationships)
    %% Use direction based on relationship.direction:
    %%   outgoing → Rel_D(system, ext, ...)
    %%   incoming → Rel_D(ext, system, ...)
    %%   bidirectional → Rel(system, ext, ...) (no direction suffix)
    Rel_D(<sysAlias>, <extAlias>, "<description>", "<technology>")

    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
```

#### C4 Container Diagram (Level 2)

Generate a `C4Container` diagram:

```mermaid
C4Container
    title <System Name> - Container Diagram

    %% Key actors (pick top 2-3 from c4.actors)
    Person(<alias>, "<name>", "<description>")

    %% System boundary with containers
    System_Boundary(<boundaryAlias>, "<System Name>") {
        %% From c4.containers
        %% Use Container for services, ContainerDb for databases
        Container(<alias>, "<name>", "<technology>", "<description>")
        ContainerDb(<alias>, "<name>", "<technology>", "<description>")
    }

    %% External systems (from c4.externalRelationships)
    System_Ext(<alias>, "<target name>", "<brief description>")

    %% Actor → Container relationships
    Rel_D(<actorAlias>, <containerAlias>, "<action>", "<protocol>")

    %% Internal relationships (from c4.internalRelationships)
    Rel(<sourceAlias>, <targetAlias>, "<description>", "<technology>")

    %% External relationships (from c4.externalRelationships)
    %% Connect to the specific container that owns the relationship
    %% If unclear, connect to the Integration Layer or main container
    Rel_D(<containerAlias>, <extAlias>, "<description>", "<technology>")

    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
```

#### Deciding Container vs ContainerDb

- If `technology` contains: `oracle`, `postgres`, `mysql`, `dynamodb`, `redis`, `mongodb`, `snowflake`, `s3` → use `ContainerDb`
- Otherwise → use `Container`

#### Handling Large Systems (>10 elements)

If the system has more than 10 elements total:

1. **Context diagram**: Group related external systems. Show the top 6-8 most critical relationships.
2. **Container diagram**: Show top 6-8 containers. Add a note listing omitted containers.

### Phase 3: Output

1. **Display the generated Mermaid** in the response for the user to copy
2. **Ask the user** where to place the diagram:
   - Update the System note's existing C4 diagram sections (replace template placeholders)
   - Create a standalone Page note: `Page - C4 Diagrams - <System Name>.md`
   - Just display (don't save)

3. If saving to the System note, replace the placeholder Mermaid blocks in the "## C4 Architecture Diagrams" section.

4. If creating a standalone Page, use this structure:

```markdown
---
type: Page
title: "C4 Diagrams - <System Name>"
created: <today>
modified: <today>
confidence: high
freshness: current
source: synthesis
verified: false
reviewed: <today>
tags:
  [
    activity/architecture,
    type/diagram,
    domain/<relevant>,
    technology/<relevant>,
  ]
---

# C4 Diagrams - <System Name>

> Auto-generated from `c4:` frontmatter on [[System - <Name>]]. Regenerate with `/c4-diagram <name> both`.

## Context Diagram (Level 1)

<mermaid block>

## Container Diagram (Level 2)

<mermaid block>

---

**Generated:** <today>
**Source:** [[System - <Name>]]
**Skill:** `/c4-diagram`
```

## Mermaid C4 Reference

### Element Types

| Element         | Syntax                                       | Use For                |
| --------------- | -------------------------------------------- | ---------------------- |
| Person          | `Person(alias, "Name", "Desc")`              | Human actors           |
| System          | `System(alias, "Name", "Desc")`              | This system (internal) |
| System_Ext      | `System_Ext(alias, "Name", "Desc")`          | External systems       |
| Container       | `Container(alias, "Name", "Tech", "Desc")`   | Services, apps         |
| ContainerDb     | `ContainerDb(alias, "Name", "Tech", "Desc")` | Databases, stores      |
| System_Boundary | `System_Boundary(alias, "Name") { ... }`     | Group containers       |

### Relationship Types

| Relationship | Syntax                             | Use For                      |
| ------------ | ---------------------------------- | ---------------------------- |
| Rel          | `Rel(from, to, "Label", "Tech")`   | No direction preference      |
| Rel_D        | `Rel_D(from, to, "Label", "Tech")` | Top-to-bottom (primary flow) |
| Rel_R        | `Rel_R(from, to, "Label", "Tech")` | Left-to-right (secondary)    |
| Rel_L        | `Rel_L(from, to, "Label", "Tech")` | Right-to-left                |
| Rel_U        | `Rel_U(from, to, "Label", "Tech")` | Bottom-to-top                |

### Layout Configuration

Always end with:

```
UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
```

Adjust `$c4ShapeInRow` based on element count:

- 1-6 elements: `"3"`
- 7-10 elements: `"4"`
- 10+ elements: `"5"` (but prefer splitting the diagram)

## Relationship to Other Skills

| Skill         | Difference                                                               |
| ------------- | ------------------------------------------------------------------------ |
| `/diagram`    | Generates Python `diagrams` PNGs (better for presentations, cloud icons) |
| `/c4-diagram` | Generates Mermaid C4 (inline rendering, Git-friendly, native Obsidian)   |

Use `/c4-diagram` for documentation that lives in the vault. Use `/diagram` for standalone images for presentations or Confluence.

## Troubleshooting

| Issue                  | Solution                                                     |
| ---------------------- | ------------------------------------------------------------ |
| Diagram doesn't render | Check Mermaid syntax - no special characters in descriptions |
| Too cluttered          | Reduce to 8 elements, use `$c4ShapeInRow="4"`                |
| Relationships overlap  | Use `Rel_R` and `Rel_L` to spread horizontally               |
| Missing data           | Add `c4:` frontmatter to the System note first               |

---

**Invoke with:** `/c4-diagram <system-name> [context|container|both]`

**Example:** `/c4-diagram CRM both` → Generates C4 Context and Container diagrams from CRM's frontmatter
