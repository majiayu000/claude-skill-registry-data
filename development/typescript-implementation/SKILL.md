---
name: typescript-implementation
description: Implement TypeScript patterns, convert JavaScript to TypeScript, add type annotations, create generics, implement decorators, and enforce strict type safety in Angular projects.
sasmp_version: "1.3.0"
bonded_agent: 01-typescript-fundamentals
bond_type: PRIMARY_BOND
---

# TypeScript Implementation Skill

## Quick Start

### Basic Types
```typescript
// Primitive types
let name: string = "Angular";
let version: number = 18;
let active: boolean = true;

// Union types
let id: string | number;

// Type aliases
type User = {
  name: string;
  age: number;
};
```

### Interfaces and Generics
```typescript
interface Component {
  render(): string;
}

// Generic interface
interface Repository<T> {
  getAll(): T[];
  getById(id: number): T | undefined;
}

class UserRepository implements Repository<User> {
  getAll(): User[] { /* ... */ }
  getById(id: number): User | undefined { /* ... */ }
}
```

### Decorators (Essential for Angular)
```typescript
// Class decorator
function Component(config: any) {
  return function(target: any) {
    target.prototype.selector = config.selector;
  };
}

// Method decorator
function Log(target: any, propertyKey: string, descriptor: PropertyDescriptor) {
  const originalMethod = descriptor.value;
  descriptor.value = function(...args: any[]) {
    console.log(`Calling ${propertyKey} with:`, args);
    return originalMethod.apply(this, args);
  };
  return descriptor;
}

// Parameter decorator
function Required(target: any, propertyKey: string, parameterIndex: number) {
  // Validation logic
}
```

## Essential Concepts

### Advanced Types

**Utility Types:**
- `Partial<T>` - Make all properties optional
- `Required<T>` - Make all properties required
- `Readonly<T>` - Make all properties readonly
- `Record<K, T>` - Object with specific key types
- `Pick<T, K>` - Select specific properties
- `Omit<T, K>` - Exclude specific properties

**Conditional Types:**
```typescript
type IsString<T> = T extends string ? true : false;
type A = IsString<"hello">; // true
type B = IsString<number>; // false
```

**Mapped Types:**
```typescript
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};
```

### Generic Constraints
```typescript
// Extend constraint
function processUser<T extends User>(user: T) {
  console.log(user.name); // OK, T has 'name'
}

// Keyof constraint
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}
```

## Advanced Features

### Type Guards
```typescript
// Type predicate
function isUser(value: unknown): value is User {
  return typeof value === 'object' && value !== null && 'name' in value;
}

// Discriminated unions
type Shape =
  | { kind: 'circle'; radius: number }
  | { kind: 'square'; side: number };

function getArea(shape: Shape) {
  switch (shape.kind) {
    case 'circle': return Math.PI * shape.radius ** 2;
    case 'square': return shape.side ** 2;
  }
}
```

### Module System
```typescript
// Export
export interface User { name: string; }
export const API_URL = 'https://api.example.com';

// Import
import { User, API_URL } from './types';
import * as Types from './types'; // Namespace import
```

## Async Programming
```typescript
// Promises
async function fetchUser(): Promise<User> {
  const response = await fetch('/api/users/1');
  return response.json();
}

// Error handling
async function safeRequest() {
  try {
    const result = await fetchUser();
  } catch (error) {
    console.error('Request failed:', error);
  }
}
```

## Best Practices

1. **Avoid `any`**: Use `unknown` and type guards instead
2. **Use strict mode**: Enable `strict` in tsconfig.json
3. **Leverage utility types**: Reduce code duplication
4. **Document complex types**: Use JSDoc for clarity
5. **Test type definitions**: Use type-level tests

## Common Patterns

### Result Type Pattern
```typescript
type Result<T, E> =
  | { ok: true; value: T }
  | { ok: false; error: E };

function createUser(data: any): Result<User, string> {
  try {
    // validation and creation
    return { ok: true, value: user };
  } catch (e) {
    return { ok: false, error: e.message };
  }
}
```

### Builder Pattern
```typescript
class QueryBuilder<T> {
  private query: any = {};

  where(field: keyof T, value: any): this {
    this.query[field] = value;
    return this;
  }

  build() {
    return this.query;
  }
}
```

## Real-World Angular Examples

### Service Type Safety
```typescript
@Injectable()
export class UserService {
  constructor(private http: HttpClient) {}

  getUser(id: number): Observable<User> {
    return this.http.get<User>(`/api/users/${id}`);
  }
}
```

### Component Props
```typescript
interface ComponentProps {
  title: string;
  items: Item[];
  onSelect: (item: Item) => void;
}

@Component({
  selector: 'app-list',
  template: `...`
})
export class ListComponent implements ComponentProps {
  @Input() title!: string;
  @Input() items: Item[] = [];
  @Output() itemSelected = new EventEmitter<Item>();

  onSelect(item: Item) {
    this.itemSelected.emit(item);
  }
}
```

## Performance Tips

- Use `const` assertions for literal types
- Leverage structural typing for flexibility
- Use discriminated unions for safe pattern matching
- Avoid circular type dependencies
- Use `omit` to reduce property access

## Resources

- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Advanced Types](https://www.typescriptlang.org/docs/handbook/2/types-from-types.html)
- [TypeScript Playground](https://www.typescriptlang.org/play)
