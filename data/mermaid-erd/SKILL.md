---
name: mermaid-erd
description: >
  Generate, render, and explain Mermaid Entity Relationship Diagrams (ERD) using erDiagram
  syntax. Use this skill whenever the user wants to model database schemas, data models,
  relational structures, or entity relationships. Triggers include: "ER diagram", "ERD",
  "entity relationship", "database schema", "data model", "draw my tables", "show table
  relationships", "model the database", "schema diagram", "foreign key diagram", or any
  request to visualize how data entities relate to each other. Also use when a user shares
  SQL DDL, ORM models, or describes tables/entities and wants a diagram. Proactively use
  this skill whenever database design, relational modeling, or schema visualization is
  involved — even if the user doesn't say "ERD" or "Mermaid".
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.0.0"
---

# Mermaid Entity Relationship Diagram Skill

Generate, render, and explain Mermaid ERDs using the `erDiagram` syntax.

---

## Workflow

1. **Understand the domain** — Extract entities, attributes, keys, and relationships from the user's description, SQL, ORM models, or requirements.
2. **Generate valid Mermaid syntax** — Follow the syntax rules below.
3. **Render the diagram** — Use the HTML + mermaid.js pattern below.
4. **Explain key design decisions** — Briefly note cardinality choices, identifying vs non-identifying relationships, and any FK/attribute tradeoffs.

---

## Mermaid erDiagram Syntax Reference

### Basic Structure

```
erDiagram
    CUSTOMER ||--o{ ORDER : places
    ORDER ||--|{ LINE-ITEM : contains
    CUSTOMER }|..|{ DELIVERY-ADDRESS : uses
```

Always start with `erDiagram` on its own line.

### Entities

Entity names can be any unicode characters. Use double quotes for names with spaces:

```
erDiagram
    CUSTOMER { }
    "Order Item" { }
```

**Entity name aliases** — display a different label than the internal name:

```
erDiagram
    CUST[Customer] { }
    ORD[Order] { }
    CUST ||--o{ ORD : places
```

Convention: entity names are often written in ALL_CAPS or PascalCase, though Mermaid doesn't enforce this.

### Attributes

Define attributes inside `{}` blocks with `type name` pairs:

```
erDiagram
    CUSTOMER {
        int id PK
        string firstName
        string lastName
        string email UK
        date createdAt
    }
    ORDER {
        int id PK
        int customerId FK
        decimal totalAmount
        string status
        timestamp placedAt "When order was submitted"
    }
```

**Attribute types**: any alphanumeric string starting with a letter — `int`, `string`, `varchar`, `boolean`, `date`, `timestamp`, `decimal`, `uuid`, `json`, etc. No enforced set.

**Attribute names**: alphanumeric, hyphens, underscores allowed. Prefix with `*` as an alternative PK indicator.

**Keys**:
| Key | Meaning |
|-----|---------|
| `PK` | Primary Key |
| `FK` | Foreign Key |
| `UK` | Unique Key |
| `PK, FK` | Composite — multiple keys on one attribute |

**Comments**: double-quoted string at the end of an attribute line:

```
string status "pending, active, or closed"
```

### Relationship Syntax

```
ENTITY_A [cardinality_left][link][cardinality_right] ENTITY_B : "label"
```

#### Cardinality Markers

| Symbol (left side) | Symbol (right side) | Meaning      |
| ------------------ | ------------------- | ------------ |
| `\|o`              | `o\|`               | Zero or one  |
| `\|\|`             | `\|\|`              | Exactly one  |
| `}o`               | `o{`                | Zero or more |
| `}\|`              | `\|{`               | One or more  |

**Reading the markers**: the outermost character is the maximum, the innermost is the minimum.

**Aliases** (readable alternatives):

```
CUSTOMER one or more--one or more ORDER : has
CUSTOMER 1+--1+ ORDER : has
CUSTOMER zero or more--zero or more ORDER : has
CUSTOMER 0+--0+ ORDER : has
CUSTOMER only one--only one ORDER : has
CUSTOMER 1--1 ORDER : has
```

#### Link Type (Identifying vs Non-Identifying)

| Symbol | Alias           | Meaning                                            | Line style  |
| ------ | --------------- | -------------------------------------------------- | ----------- |
| `--`   | `to`            | Identifying — child cannot exist without parent    | Solid line  |
| `..`   | `optionally to` | Non-identifying — entities can exist independently | Dashed line |

**Identifying**: `ORDER ||--|{ LINE-ITEM : contains` — a LINE-ITEM cannot exist without an ORDER.

**Non-identifying**: `PERSON }|..|{ CAR : "drives"` — a PERSON and CAR can exist without each other.

#### Common Relationship Patterns

```
erDiagram
    %% One-to-many (identifying): customer has orders
    CUSTOMER ||--o{ ORDER : places

    %% One-to-many (identifying): order has line items
    ORDER ||--|{ LINE-ITEM : contains

    %% Many-to-many (non-identifying): resolved via junction table
    PRODUCT }|..|{ CATEGORY : "belongs to"

    %% Zero or one: user may have a profile
    USER ||--o| PROFILE : has

    %% Exactly one to exactly one
    USER ||--|| ACCOUNT : owns
```

### Direction

```
erDiagram
    direction LR
```

Options: `TB` (default), `BT`, `LR`, `RL`

Use `LR` for wide schemas with many entities; keep `TB` for deep hierarchies.

### Comments

```
%% This is a comment — ignored by the parser
```

### Styling

```
erDiagram
    CUSTOMER:::highlight { ... }
    classDef highlight fill:#f9f,stroke:#333,stroke-width:2px
```

---

## Rendering

ERDs must be rendered with mermaid.js, not raw SVG — layout, crow's foot connectors, and attribute rows are handled automatically. Use this HTML pattern:

```html
<style>
  #erd svg {
    max-width: 100%;
  }
</style>
<div id="erd" style="padding: 1rem 0"></div>
<script type="module">
  import mermaid from "https://esm.sh/mermaid@11/dist/mermaid.esm.min.mjs";
  const dark = matchMedia("(prefers-color-scheme: dark)").matches;
  await document.fonts.ready;
  mermaid.initialize({
    startOnLoad: false,
    theme: "base",
    fontFamily: '"Anthropic Sans", sans-serif',
    themeVariables: {
      darkMode: dark,
      fontSize: "13px",
      fontFamily: '"Anthropic Sans", sans-serif',
      lineColor: dark ? "#9c9a92" : "#73726c",
      textColor: dark ? "#c2c0b6" : "#3d3d3a"
    }
  });
  const diagram = `erDiagram
    CUSTOMER ||--o{ ORDER : places
    ORDER ||--|{ LINE-ITEM : contains
    CUSTOMER {
        int id PK
        string name
        string email UK
    }
    ORDER {
        int id PK
        int customerId FK
        date placedAt
    }
    LINE-ITEM {
        int id PK
        int orderId FK
        int productId FK
        int quantity
        decimal unitPrice
    }
`;
  const { svg } = await mermaid.render("erd-svg", diagram);
  document.getElementById("erd").innerHTML = svg;
</script>
```

**Key init settings to never change:**

- `fontFamily` and `fontSize` are used for layout measurement — deviating causes text clipping
- `theme: 'base'` allows `themeVariables` to apply
- Always `await document.fonts.ready` before rendering

---

## Design Best Practices

### What to include as attributes

- **Always include**: PKs, FKs (if it's a physical/relational model), key business fields
- **Omit FKs** for logical/conceptual models — the relationship lines already convey the association
- **Omit exhaustive columns** — pick 4–8 most meaningful attributes per entity; details go in documentation
- **Use comments** (`"..."`) to clarify non-obvious field purposes or allowed values

### Naming

- Use **singular nouns** for entity names (`CUSTOMER`, not `CUSTOMERS`)
- Use **snake_case or camelCase** consistently for attributes
- **Label every relationship** with a short verb phrase from the perspective of the first entity

### Cardinality decisions

- Default to `||--o{` (one-to-many, zero or more) for most parent–child relationships
- Use `||--|{` (one-to-many, one or more) when a child must always have at least one record
- Reserve `..` (dashed/non-identifying) for optional or many-to-many associations
- Many-to-many relationships should typically be resolved to a **junction/bridge entity**

### Identifying vs Non-Identifying

- Use solid lines (`--`) when the child record's existence depends on the parent (e.g., ORDER LINE → ORDER)
- Use dashed lines (`..`) when both entities are independent (e.g., STUDENT ↔ COURSE via enrollment)

### Diagram size

- **≤ 10–12 entities** per diagram for readability
- Split large schemas by bounded context/domain (e.g., "Orders domain", "Users domain")
- Use `direction LR` for wide schemas

---

## Common Patterns

### One-to-Many with junction table (Many-to-Many resolution)

```
erDiagram
    STUDENT }|..|{ COURSE : enrolls
    STUDENT ||--o{ ENROLLMENT : has
    COURSE ||--o{ ENROLLMENT : has
    ENROLLMENT {
        int studentId PK, FK
        int courseId PK, FK
        date enrolledAt
        string grade
    }
```

### Self-referencing entity (hierarchical data)

```
erDiagram
    EMPLOYEE {
        int id PK
        string name
        int managerId FK "references EMPLOYEE.id"
    }
    EMPLOYEE ||--o{ EMPLOYEE : manages
```

### Soft-delete / audit pattern

```
erDiagram
    RECORD {
        uuid id PK
        timestamp createdAt
        timestamp updatedAt
        timestamp deletedAt "null if active"
        int createdBy FK
    }
```

### Polymorphic association (noted in comment)

```
erDiagram
    %% Tags can apply to posts OR comments — polymorphic
    TAG }|..|{ POST : labels
    TAG }|..|{ COMMENT : labels
    TAG {
        int id PK
        string name UK
    }
```

### Type/Status tables

```
erDiagram
    ORDER_STATUS {
        int id PK
        string code UK "pending|active|shipped|closed"
        string label
    }
    ORDER }o--|| ORDER_STATUS : has
```
