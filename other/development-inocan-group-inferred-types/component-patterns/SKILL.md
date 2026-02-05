---
name: component-patterns
description: |
  Build well-structured React components using variant patterns, pure components, and container patterns. Provides patterns for component organization, type safety, and separation of concerns.

  Use when: building components with multiple display modes, organizing component hierarchies, implementing container/presentational patterns, reducing component proliferation while maintaining clear APIs.
---

# Component Patterns

Build well-structured React components using proven patterns for organization, type safety, and separation of concerns.

## Overview

This skill covers patterns for building React components that are:
- **Type-safe** - TypeScript enforces correct props
- **Composable** - Components can be combined flexibly
- **Maintainable** - Clear separation of concerns
- **Scalable** - Patterns that work as the codebase grows

## Quick Start

### Variant Components

Use discriminated unions for components with multiple modes:

```typescript
interface ViewProps { variant: 'view'; todo: Todo; onEdit: () => void; }
interface EditProps { variant: 'edit'; todo: Todo; onSave: (v: Values) => Promise<void>; }

type TodoCardProps = ViewProps | EditProps;

function TodoCard(props: TodoCardProps) {
  switch (props.variant) {
    case 'view': return <ViewVariant {...props} />;
    case 'edit': return <EditVariant {...props} />;
  }
}
```

### Pure Components

Components that receive all data via props:

```typescript
interface TodoListProps {
  todos: Todo[];
  onSelect: (id: string) => void;
  selectedId?: string;
}

function TodoList({ todos, onSelect, selectedId }: TodoListProps) {
  return (
    <ul>
      {todos.map(todo => (
        <li 
          key={todo.id} 
          onClick={() => onSelect(todo.id)}
          className={todo.id === selectedId ? 'selected' : ''}
        >
          {todo.title}
        </li>
      ))}
    </ul>
  );
}
```

### Container Components

Components that connect data to presentation:

```typescript
function TodosPage() {
  const { todos, handleSelect, selectedId } = useTodosPage();
  
  return <TodoList todos={todos} onSelect={handleSelect} selectedId={selectedId} />;
}
```

## Component Types

| Type | Responsibility | Data Access | Location |
|------|---------------|-------------|----------|
| **Container** | Data retrieval, orchestration | Uses hooks | `src/app/` |
| **Pure** | Render UI from props | Props only | `src/components/` |
| **Variant** | Multiple modes via discriminator | Props only | `src/components/` |

## Topics

For deeper understanding, explore these focused topics:

### [`topics/variants.md`](./topics/variants.md)
**Variant Components**

Build discriminated union components with a single entry point and deep internal variation. Covers type definitions, switch dispatching, exhaustiveness checking, and common patterns.

**Start here if:** You're building components with multiple display modes (view/edit/create) or states (selected/default).

---

### [`topics/pure-components.md`](./topics/pure-components.md)
**Pure Components**

Build components that receive all data and behavior via props. Covers prop design, composition, and testing strategies.

**Start here if:** You're building reusable UI components or want to understand the presentational layer.

---

### [`topics/containers.md`](./topics/containers.md)
**Container Components**

Connect data sources to pure components. Covers when to use containers, prop drilling alternatives, and composition strategies.

**Start here if:** You need to understand how pages connect hooks to UI components.

---

## File Templates

See `templates/` for starter code:
- `variant-component.tsx` - Discriminated union component

## Key Principles

1. **Props down, events up** - Data flows down, actions flow up
2. **Single responsibility** - Each component does one thing well
3. **Explicit variants** - Use discriminated unions, not boolean flags
4. **Type narrowing** - Let TypeScript narrow props based on variant
5. **Colocate related code** - Keep variants together, split when they diverge
