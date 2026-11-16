---
name: type-safety-patterns
description: Type safety — Python type hints with mypy/pyright, TypeScript strict mode, branded types, Zod validation, runtime checks
triggers:
  - type safety
  - type hints python
  - mypy pyright
  - typescript strict
  - branded types
  - zod schema
  - runtime type checking
  - type narrowing
  - no any typescript
  - type annotations
do_not_use_for:
  - full validation schemas — use pydantic for complex input validation
  - error handling — use error-handling-patterns
  - general AI anti-patterns — use ai-code-maintainability
see_also:
  - ai-code-maintainability
  - error-handling-patterns
  - pydantic-ai
---

# Type Safety Patterns

## Python: Strict Type Hints

```python
from __future__ import annotations  # postponed eval, works with forward refs
from typing import Optional, Union, Literal, TypeVar, Generic
from collections.abc import Callable, Sequence
from dataclasses import dataclass

# Avoid bare Optional[X] — use X | None (Python 3.10+)
def find_user(user_id: str) -> User | None: ...

# Union with discriminator
type Event = ClickEvent | SubmitEvent | ErrorEvent

# Literal for fixed string values
Status = Literal["active", "inactive", "pending"]

def update_status(user_id: str, status: Status) -> None: ...

# TypeVar for generic functions
T = TypeVar("T")

def first_or_default(items: Sequence[T], default: T) -> T:
    return items[0] if items else default
```

## Python: Mypy / Pyright Config

```toml
# pyproject.toml — pyright (recommended, faster)
[tool.pyright]
pythonVersion = "3.11"
typeCheckingMode = "strict"
reportMissingImports = true
reportMissingTypeStubs = false
reportUnknownMemberType = false  # relax for external libs

# mypy alternative
[tool.mypy]
python_version = "3.11"
strict = true
ignore_missing_imports = true
warn_return_any = true
warn_unused_ignores = true
```

## Python: Branded/Newtype

```python
from typing import NewType, Annotated

# NewType — distinct at type-check time, same at runtime
UserId = NewType("UserId", str)
OrderId = NewType("OrderId", str)

def get_user(user_id: UserId) -> User: ...
def get_order(order_id: OrderId) -> Order: ...

user_id = UserId("u-123")
order_id = OrderId("o-456")

# get_user(order_id)  # ← mypy error: Expected UserId, got OrderId

# Annotated with constraints
from annotated_types import Gt, Le
from pydantic import TypeAdapter

PositiveInt = Annotated[int, Gt(0)]
Percentage = Annotated[float, Gt(0.0), Le(100.0)]

adapter = TypeAdapter(Percentage)
adapter.validate_python(50.0)    # ok
adapter.validate_python(150.0)   # ValidationError
```

## TypeScript: Strict Mode

```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,   // arr[0] is T | undefined
    "exactOptionalPropertyTypes": true,  // ? means missing, not undefined
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "forceConsistentCasingInFileNames": true
  }
}
```

## TypeScript: Branded Types

```typescript
// Nominal typing — prevents accidental mix-ups
declare const __brand: unique symbol;
type Brand<T, B> = T & { [__brand]: B };

type UserId = Brand<string, "UserId">;
type OrderId = Brand<string, "OrderId">;

function createUserId(raw: string): UserId {
  return raw as UserId;  // only place we cast
}

function getUser(id: UserId): Promise<User> { ... }

const userId = createUserId("u-123");
const orderId = "o-456" as OrderId;

getUser(userId);   // ✅ ok
getUser(orderId);  // ❌ TypeScript error: Argument of type 'OrderId' not assignable to 'UserId'
```

## TypeScript: Zod Runtime Validation

```typescript
import { z } from "zod";

// Schema as single source of truth for type + validation
const UserSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1).max(100),
  age: z.number().int().min(0).max(150),
  role: z.enum(["admin", "user", "guest"]),
  email: z.string().email(),
  createdAt: z.coerce.date(),
});

type User = z.infer<typeof UserSchema>;   // no duplicate interface needed

// Validate at boundary
function parseUser(raw: unknown): User {
  return UserSchema.parse(raw);            // throws ZodError if invalid
}

// Or safe parse (no throw)
const result = UserSchema.safeParse(raw);
if (!result.success) {
  logger.warn("invalid user data", { errors: result.error.issues });
  return null;
}
const user = result.data;   // User — fully typed
```

## Type Narrowing

```typescript
// Discriminated union — exhaustive checking
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "square"; side: number }
  | { kind: "triangle"; base: number; height: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":   return Math.PI * shape.radius ** 2;
    case "square":   return shape.side ** 2;
    case "triangle": return (shape.base * shape.height) / 2;
    default:
      // exhaustive check — TypeScript errors if a case is missing
      const _exhaustive: never = shape;
      throw new Error(`Unknown shape: ${_exhaustive}`);
  }
}
```

## Anti-Fake-Pass Checks

- `from __future__ import annotations` is needed for forward references in Python 3.9
- `NewType` only creates distinct types at check time — `isinstance()` won't detect them at runtime
- `noUncheckedIndexedAccess: true` makes `arr[0]` type `T | undefined` — handle the undefined case
- Zod `parse()` throws `ZodError` — use `safeParse()` in user-facing code
- `strict: true` in tsconfig enables 8 flags at once — add each flag individually if migrating legacy code
- Branded types require a `createXxx()` factory that does the cast — don't cast everywhere
