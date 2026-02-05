---
name: ts-module
description: Creates TypeScript modules following immutable, fluent API patterns with proper encapsulation.
---

# TypeScript Module Creation

Create modules with immutable data, fluent APIs, and clear separation of concerns.

## Core Principles

- Immutable by default (Object.freeze in constructor)
- Fluent API for method chaining
- Props pattern for multiple arguments
- Getters instead of getXxx methods
- All properties readonly

## Function Template

```ts
type Props = {}

/**
 * Function description
 */
export function FunctionName(props: Props) {
  // props.prop1 // Use props directly
  // const { prop1, prop2 } = props // Do NOT use destructuring
}
```

## Class Template

```ts
type Props = {}

/**
 * Class description
 */
export class ClassName {
  constructor(private readonly props: Props) {
    Object.freeze(this)
  }

  /**
   * Method description
   */
  method() {
    // implementation
  }
}
```

## Design Patterns

### Fluent API

Return new objects for immutability and method chaining.

```ts
export class Document {
  constructor(private readonly data: Data) {}

  withTitle(title: string): Document {
    return new Document({ ...this.data, title })
  }

  toMarkdown(): string {
    return this.format()
  }
}

// Usage
const result = document.withTitle("New").withAuthor("John").toMarkdown()
```

### Service Layer

Coordinate multiple domain objects and external resources.

```ts
export class DocumentService {
  constructor(
    private readonly fileSystem: FileSystem,
    private readonly parser: Parser,
    private readonly validator: Validator
  ) {}

  async process(path: string): Promise<Document> {
    const content = await this.fileSystem.read(path)
    const parsed = this.parser.parse(content)
    return new Document(this.validator.validate(parsed))
  }
}
```

### Facade

Hide complexity behind simple methods.

```ts
export class DocumentFacade {
  async get(path: string): Promise<Document> {
    const content = await this.readFile(path)
    const parsed = this.parse(content)
    const validated = this.validate(parsed, await this.getSchema(path))
    return new Document(validated)
  }
}
```

### Other Patterns

- **Factory Method**: Create objects without specifying exact classes
- **Adapter**: Allow incompatible interfaces to work together
- **Builder**: Construct complex objects step by step

## Method Naming

- `with*()` - Transformations (returns new instance)
- `to*()` - Output conversion
- `get*()` - Retrieval (prefer getters)

## Refactoring Decision Rules

- **Extract to domain method**: When logic appears in 2+ places
- **Create fluent method**: When manual object manipulation is required
- **Use Service Layer**: When coordinating 3+ related operations

## Anti-Patterns

### Domain Logic Encapsulation

```ts
// Bad: Manual operations scattered
const merged = { ...document.properties, ...newProperties }
const formatted = formatMarkdown(merged, document.content)

// Good: Logic encapsulated
const markdown = document.withProperties(newProperties).toMarkdown()
```

### Separation of Concerns

```ts
// Bad: Mixed concerns
async function processData(data) {
  if (!data.name) throw new Error()
  data.name = data.name.toUpperCase()
  await db.save(data)
  return data
}

// Good: Separated concerns
const validated = validator.validate(data)
const transformed = transformer.transform(validated)
const saved = await repository.save(transformed)
```
