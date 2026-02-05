---
name: type-patterns
description: |
  Type-safe patterns using Result types, discriminated unions, and exhaustive matching.
  Reference for implementing immutable, type-safe core logic without exceptions.
---

# Type Safety Patterns

## Core Rules

| Avoid | Use Instead |
|-------|-------------|
| `any` | Proper type definitions |
| `as` type assertions | Discriminated unions |
| `throw` exceptions | Result type |
| Type guards | `ts-pattern` `.exhaustive()` |

## Result Type

```typescript
export type Result<T, E> =
  | { readonly type: "success"; readonly data: T }
  | { readonly type: "error"; readonly error: E }

// Domain-specific error types
export type AppError =
  | { type: "notFound"; resource: string }
  | { type: "validation"; field: string; message: string }
  | { type: "permission"; action: string }
  | { type: "network"; status: number }
  | { type: "unknown"; cause: unknown }
```

## ts-pattern Exhaustive Matching

```typescript
import { match } from "ts-pattern"

const handleResult = <T>(result: Result<T, AppError>) =>
  match(result)
    .with({ type: "success" }, ({ data }) => renderData(data))
    .with({ type: "error" }, ({ error }) =>
      match(error)
        .with({ type: "notFound" }, () => showNotFound())
        .with({ type: "validation" }, ({ message }) => showValidation(message))
        .with({ type: "permission" }, () => showPermissionError())
        .with({ type: "network" }, ({ status }) => showNetworkError(status))
        .with({ type: "unknown" }, () => showUnknown())
        .exhaustive()
    )
    .exhaustive()
```

## Discriminated Union Pattern

```typescript
// Base interface with discriminant
interface BaseNode {
  readonly id: string
  readonly name: string
}

// Discriminated variants
interface FileNode extends BaseNode {
  readonly type: "file"
  readonly size: number
  readonly mimeType: string
}

interface FolderNode extends BaseNode {
  readonly type: "folder"
  readonly children: ReadonlyArray<TreeNode>
}

export type TreeNode = FileNode | FolderNode

// Exhaustive handling
const getIcon = (node: TreeNode) =>
  match(node)
    .with({ type: "file" }, () => FileIcon)
    .with({ type: "folder" }, () => FolderIcon)
    .exhaustive()
```

## Immutable Class Pattern

```typescript
export class SelectionManager<T extends { id: string }> {
  private constructor(
    private readonly selectedIds: ReadonlySet<string>,
    private readonly anchorId: string | null
  ) {}

  static empty<T extends { id: string }>(): SelectionManager<T> {
    return new SelectionManager(new Set(), null)
  }

  select(itemId: string): SelectionManager<T> {
    return new SelectionManager(new Set([itemId]), itemId)
  }

  toggle(itemId: string): SelectionManager<T> {
    const next = new Set(this.selectedIds)
    if (next.has(itemId)) {
      next.delete(itemId)
    } else {
      next.add(itemId)
    }
    return new SelectionManager(next, itemId)
  }

  isSelected(itemId: string): boolean {
    return this.selectedIds.has(itemId)
  }
}
```

## Readonly Collections

```typescript
// Prefer readonly variants
type Items = ReadonlyArray<Item>
type Lookup = ReadonlyMap<string, Item>
type UniqueIds = ReadonlySet<string>

// Immutable updates
const addItem = (items: ReadonlyArray<Item>, item: Item): ReadonlyArray<Item> =>
  [...items, item]

const removeItem = (items: ReadonlyArray<Item>, id: string): ReadonlyArray<Item> =>
  items.filter(item => item.id !== id)
```

## Branded Types

```typescript
// Prevent type confusion
declare const brand: unique symbol

type UserId = string & { readonly [brand]: "UserId" }
type PostId = string & { readonly [brand]: "PostId" }

const createUserId = (id: string): UserId => id as UserId
const createPostId = (id: string): PostId => id as PostId

// Compile-time safety
declare function getUser(id: UserId): User
declare function getPost(id: PostId): Post

const userId = createUserId("123")
const postId = createPostId("456")

getUser(userId)  // ✅ OK
getUser(postId)  // ❌ Type error
```

## Option Type (for nullable values)

```typescript
export type Option<T> =
  | { readonly type: "some"; readonly value: T }
  | { readonly type: "none" }

export const some = <T>(value: T): Option<T> => ({ type: "some", value })
export const none: Option<never> = { type: "none" }

// Usage
const findUser = (id: string): Option<User> =>
  users.has(id) ? some(users.get(id)!) : none

const userName = match(findUser("123"))
  .with({ type: "some" }, ({ value }) => value.name)
  .with({ type: "none" }, () => "Unknown")
  .exhaustive()
```

## References

- [ts-pattern Documentation](https://github.com/gvergnaud/ts-pattern)
- [TypeScript Handbook - Narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html)
- [TypeScript Handbook - Discriminated Unions](https://www.typescriptlang.org/docs/handbook/2/narrowing.html#discriminated-unions)
