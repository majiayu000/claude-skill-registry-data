---
name: typescript-basics
description: TypeScript patterns for React including interfaces, type annotations, generics, null handling, and utility types. Use when writing type-safe React code.
---

# TypeScript Basics

## Overview
These TypeScript patterns ensure type-safe, maintainable React code. Follow these guidelines for all frontend development.

## Interface Definitions

### Data Model Interfaces
```typescript
interface Task {
  id: string;
  title: string;
  description: string | null;
  isCompleted: boolean;
  createdAt: string;
}

type TaskStatus = 'pending' | 'completed' | 'archived';
```

### Request/Response Types
```typescript
interface CreateTaskRequest {
  title: string;
  description?: string;
}

interface PagedResponse<T> {
  items: T[];
  page: number;
  totalCount: number;
}
```

## Type Annotations

### Function Parameters
```typescript
function handleClick(id: string): void {
  console.log(id);
}

async function fetchTasks(): Promise<Task[]> {
  const response = await fetch('/api/tasks');
  return response.json();
}
```

### State Types
```typescript
const [tasks, setTasks] = useState<Task[]>([]);
const [error, setError] = useState<string | null>(null);
```

### Event Handlers
```typescript
function handleSubmit(e: React.FormEvent<HTMLFormElement>): void {
  e.preventDefault();
}

function handleChange(e: React.ChangeEvent<HTMLInputElement>): void {
  setValue(e.target.value);
}
```

## Null and Undefined

### Nullable Types
```typescript
interface Task {
  description: string | null;  // Explicitly null
}

interface UpdateRequest {
  title?: string;  // Optional (undefined)
}
```

### Null Checks
```typescript
const title = task?.title ?? 'Untitled';
```

## Utility Types

```typescript
type TaskUpdate = Partial<Task>;           // All optional
type TaskSummary = Pick<Task, 'id' | 'title'>;  // Select props
type CreateTask = Omit<Task, 'id' | 'createdAt'>;  // Exclude props
```

## Best Practices

### Avoid `any`
```typescript
// Bad
function processData(data: any) { ... }

// Good
function processData(data: Task[]) { ... }
```

### Export Types
```typescript
export interface Task { ... }
import type { Task } from '../types/task';
```
