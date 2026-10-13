---
name: mermaid-class-diagram
description: >
  Generate, render, and explain Mermaid class diagrams (UML). Use this skill whenever
  the user wants to visualize class structures, object-oriented models, entity relationships,
  system architecture, or data models using Mermaid syntax. Triggers include: "class diagram",
  "UML diagram", "show me the class structure", "diagram these classes", "model this system",
  "visualize my OOP design", "entity diagram", "draw relationships between classes",
  or any request to represent inheritance, composition, aggregation, associations, or interfaces
  visually. Also use when a user pastes code (Python, Java, TypeScript, etc.) and asks to
  diagram it, or when they describe a system and want a visual model. Always use this skill
  proactively when class/entity relationships are involved, even if "Mermaid" isn't mentioned.
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.0.0"
---

# Mermaid Class Diagram Skill

Generate, render, and explain Mermaid class diagrams using the `classDiagram` syntax.

---

## Workflow

1. **Understand the domain** — Extract classes, attributes, methods, and relationships from the user's description, code, or requirements.
2. **Generate valid Mermaid syntax** — Follow the syntax rules below.
3. **Render the diagram** — Use the `visualize:show_widget` tool to render inline.
4. **Explain the diagram** — Briefly describe the key design decisions.

---

## Mermaid classDiagram Syntax Reference

### Basic Structure

```
classDiagram
    class Animal {
        +String name
        +int age
        +makeSound() String
    }
```

Always start with `classDiagram` on its own line.

### Defining Classes

Two ways:

- **Keyword**: `class Animal`
- **Via relationship**: `Vehicle <|-- Car`

Class names: alphanumeric, underscores, dashes only.

**With label** (display name differs from id):

```
class Animal["Animal 🐾"]
```

### Members (Attributes & Methods)

Use `:` for one at a time, or `{}` for multiple:

```
classDiagram
    class BankAccount {
        +String owner
        -Float balance
        #String accountType
        ~String internalCode
        +deposit(amount Float) bool
        +withdraw(amount Float) bool$
        +getBalance() Float
    }
```

**Visibility prefixes:**
| Symbol | Meaning |
|--------|---------|
| `+` | Public |
| `-` | Private |
| `#` | Protected |
| `~` | Package/Internal |

**Classifiers (suffix after `()` or at end of field):**
| Symbol | Meaning |
|--------|---------|
| `*` | Abstract |
| `$` | Static |

**Generic types**: use `~` tilde: `List~String~`, `Map~String,int~`

**Return types**: add after space following `)`: `getItems() List~String~`

### Relationships

```
classDiagram
    ClassA <|-- ClassB       %% Inheritance
    ClassA *-- ClassB        %% Composition
    ClassA o-- ClassB        %% Aggregation
    ClassA --> ClassB        %% Association
    ClassA -- ClassB         %% Link (solid)
    ClassA ..> ClassB        %% Dependency
    ClassA ..|> ClassB       %% Realization
    ClassA .. ClassB         %% Link (dashed)
```

**With labels:**

```
Animal "1" --> "many" Prey : hunts
```

**Two-way relations:**

```
ClassA <|--|> ClassB
```

**Lollipop interfaces:**

```
bar ()-- foo
```

### Cardinality / Multiplicity

Place in quotes near arrows:

```
Customer "1" --> "0..*" Order : places
```

Options: `1`, `0..1`, `1..*`, `*`, `n`, `0..n`, `1..n`

### Annotations

```
classDiagram
    class Shape {
        <<Interface>>
        +area() float
    }
    class AbstractAnimal {
        <<Abstract>>
    }
    class UserService {
        <<Service>>
    }
    class Color {
        <<Enumeration>>
        RED
        GREEN
        BLUE
    }
```

### Namespaces

```
classDiagram
    namespace Geometry {
        class Point {
            +float x
            +float y
        }
        class Circle {
            +Point center
            +float radius
        }
    }
```

### Direction

```
classDiagram
    direction LR
```

Options: `TB` (top-bottom, default), `BT`, `LR`, `RL`

### Notes

```
note "This is a general note"
note for MyClass "This note is for MyClass"
```

### Comments

```
%% This is a comment
```

### Styling

```
classDiagram
    class Danger:::warning {
        +alert()
    }
    classDef warning fill:#f00,color:#fff,stroke:#900
```

---

## Rendering

After generating the Mermaid code, render it using the visualizer:

```html
<div id="diagram"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/mermaid/11.4.1/mermaid.min.js"></script>
<script>
  mermaid.initialize({ startOnLoad: true, theme: "default" });
</script>
<pre class="mermaid">
classDiagram
    %% paste diagram here
</pre>
```

Use `visualize:show_widget` with this HTML pattern. Set `theme` to `'dark'` if the context suggests dark mode.

---

## Design Best Practices

- **Limit to ~10–15 classes** per diagram for readability; split large systems into multiple diagrams by subsystem.
- **Use direction LR** for wide inheritance hierarchies; keep TB (default) for deep trees.
- **Prefer composition over inheritance** in diagrams when modeling modern OOP.
- **Always annotate interfaces** with `<<Interface>>` and abstract classes with `<<Abstract>>`.
- **Add cardinality** to associations whenever the multiplicity is meaningful to understanding the model.
- **Group related classes** in namespaces for large diagrams.
- **Use notes** to explain non-obvious design decisions inline.

---

## Common Patterns

### Inheritance Hierarchy

```
classDiagram
    Animal <|-- Dog
    Animal <|-- Cat
    Dog <|-- GoldenRetriever
    class Animal {
        <<Abstract>>
        +String name
        +makeSound()* String
    }
```

### Repository Pattern

```
classDiagram
    class IUserRepository {
        <<Interface>>
        +findById(id String) User
        +save(user User) void
    }
    IUserRepository <|.. UserRepository
    UserRepository --> Database : uses
```

### Aggregation vs Composition

```
classDiagram
    %% Composition: Department owns Employees (lifecycle tied)
    Department *-- Employee
    %% Aggregation: Team uses Players (independent lifecycle)
    Team o-- Player
```
