---
name: typescript
description: State-of-the-art TypeScript — strict compiler settings, Zod runtime validation, branded types, discriminated unions, and modern language features for fully type-safe codebases.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 1.0.0
---

# typescript

State-of-the-art TypeScript coding standards.  
Implements all mandatory rules from [`code-quality`](../../code-quality/SKILL.md): full type safety, typed errors, immutability, and clean naming.

## Instructions

Apply these rules to every TypeScript project regardless of framework (Node.js, React, Next.js, Bun, etc.).

---

## Guidelines

### Compiler — tsconfig.json

Always enable the full strict suite plus the extra safety flags:

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noImplicitOverride": true,
    "forceConsistentCasingInFileNames": true,
    "isolatedModules": true,
    "verbatimModuleSyntax": true,
    "moduleResolution": "bundler",
    "target": "ES2022",
    "lib": ["ES2022"]
  }
}
```

- **`strict: true`** enables `strictNullChecks`, `noImplicitAny`, `strictFunctionTypes`, `strictBindCallApply`, `strictPropertyInitialization`, and `useUnknownInCatchVariables`
- **`noUncheckedIndexedAccess`** makes `array[i]` return `T | undefined` — forces bounds checks
- **`exactOptionalPropertyTypes`** distinguishes `{ key?: string }` from `{ key: string | undefined }`
- **`verbatimModuleSyntax`** enforces `import type` for type-only imports

### Type Safety

#### No `any` — use `unknown` and narrow

```ts
// ❌ unsafe — bypasses the type checker
function parse(raw: any): User { return raw; }

// ✅ safe — forces narrowing before use
function parse(raw: unknown): User {
  return userSchema.parse(raw); // Zod throws if invalid
}
```

#### Zod for every external boundary

Validate all data that crosses a trust boundary (HTTP request body, API response, env vars, file content, query params):

```ts
import { z } from 'zod';

const CreateUserSchema = z.object({
  email: z.string().email(),
  age:   z.number().int().min(0).max(150),
  role:  z.enum(['admin', 'member', 'guest']),
});

type CreateUserDto = z.infer<typeof CreateUserSchema>;

// In a route handler
const result = CreateUserSchema.safeParse(req.body);
if (!result.success) {
  return res.status(422).json({ error: result.error.format() });
}
const dto: CreateUserDto = result.data; // fully typed, validated
```

#### Validated environment variables

```ts
import { z } from 'zod';

const EnvSchema = z.object({
  DATABASE_URL: z.string().url(),
  PORT:         z.coerce.number().default(3000),
  NODE_ENV:     z.enum(['development', 'test', 'production']),
  JWT_SECRET:   z.string().min(32),
});

export const env = EnvSchema.parse(process.env);
// Use env.DATABASE_URL, env.PORT — fully typed everywhere
```

#### Branded / Nominal types

Prevent mixing semantically different `string` or `number` values:

```ts
type UserId  = string & { readonly __brand: 'UserId' };
type OrderId = string & { readonly __brand: 'OrderId' };

const toUserId  = (id: string): UserId  => id as UserId;
const toOrderId = (id: string): OrderId => id as OrderId;

function getUser(id: UserId): Promise<User> { /* … */ }

// ❌ compile error — prevents accidental ID confusion
getUser(toOrderId('ord_123'));

// ✅
getUser(toUserId('usr_456'));
```

#### Discriminated unions over optional fields

```ts
// ❌ ambiguous — callers must check multiple optionals
type ApiResult = { data?: User; error?: string; loading?: boolean };

// ✅ exhaustively checkable — exactly one state at a time
type ApiResult<T> =
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error';   message: string };

function render(result: ApiResult<User>) {
  switch (result.status) {
    case 'loading': return <Spinner />;
    case 'success': return <Profile user={result.data} />;
    case 'error':   return <Alert msg={result.message} />;
    // TypeScript exhaustiveness check — no default needed
  }
}
```

#### `satisfies` operator for literal inference

```ts
// ❌ widened to Record<string, string> — loses key information
const routes = { home: '/', about: '/about' };

// ✅ validates shape AND preserves literal types
const routes = {
  home:  '/',
  about: '/about',
  blog:  '/blog',
} satisfies Record<string, `/${string}`>;

type RouteName = keyof typeof routes; // 'home' | 'about' | 'blog'
```

#### `const` type parameters (TypeScript 5.0+)

```ts
// Without const — T inferred as string[]
function identity<T>(arr: T[]): T[] { return arr; }

// With const — T inferred as readonly ['a', 'b']
function identity<const T extends readonly unknown[]>(arr: T): T { return arr; }
const result = identity(['a', 'b']); // type: readonly ['a', 'b']
```

### Error Handling

#### Typed error classes

```ts
// ❌ bare Error — caller can't distinguish error types
throw new Error('User not found');

// ✅ domain error — typed, catchable, loggable
class UserNotFoundError extends Error {
  readonly code = 'USER_NOT_FOUND' as const;
  constructor(readonly userId: string) {
    super(`User not found: ${userId}`);
    this.name = 'UserNotFoundError';
  }
}

// In catch blocks (strict mode makes `e` unknown)
try {
  await userService.get(id);
} catch (e) {
  if (e instanceof UserNotFoundError) {
    return res.status(404).json({ error: e.code, userId: e.userId });
  }
  throw e; // re-throw unexpected errors
}
```

#### Result type for recoverable errors

Use a `Result<T, E>` pattern to make errors part of the return type instead of exceptions for expected failure paths:

```ts
type Ok<T>  = { ok: true;  value: T };
type Err<E> = { ok: false; error: E };
type Result<T, E = Error> = Ok<T> | Err<E>;

const ok  = <T>(value: T): Ok<T>   => ({ ok: true,  value });
const err = <E>(error: E): Err<E>  => ({ ok: false, error });

async function findUser(id: UserId): Promise<Result<User, UserNotFoundError>> {
  const user = await db.users.findUnique({ where: { id } });
  return user ? ok(user) : err(new UserNotFoundError(id));
}

// Caller is forced to handle both paths
const result = await findUser(id);
if (!result.ok) return res.status(404).json({ error: result.error.code });
res.json(result.value);
```

### Immutability

```ts
// Prefer const at every level
const MAX_RETRIES = 3;

// Readonly object shapes
type Config = Readonly<{
  apiUrl: string;
  timeout: number;
}>;

// Readonly arrays
function sort(items: readonly string[]): string[] {
  return [...items].sort(); // clone before mutating
}

// as const for literal objects / tuples
const ROLES = ['admin', 'member', 'guest'] as const;
type Role = typeof ROLES[number]; // 'admin' | 'member' | 'guest'
```

### Naming Conventions

| Entity | Convention | Example |
|--------|-----------|---------|
| Variable / function | `camelCase` | `getUserByEmail` |
| Class / Interface / Type / Enum | `PascalCase` | `UserService`, `CreateUserDto` |
| File | `kebab-case` | `user-service.ts` |
| Constant (module-level) | `SCREAMING_SNAKE_CASE` | `MAX_PAGE_SIZE` |
| Boolean | `is/has/can` prefix | `isAuthenticated`, `hasPermission` |
| Zod schema | `PascalCase` + `Schema` suffix | `CreateUserSchema` |
| Type from Zod | `PascalCase` + `Dto`/`Input` suffix | `CreateUserDto` |

- **No `I` prefix** on interfaces (`UserService` not `IUserService`)
- **No `T` prefix** on generic type params beyond single-letter generics
- Use `import type` for type-only imports (enforced by `verbatimModuleSyntax`)

### Code Organisation

```
src/
  domain/          ← pure business logic; no HTTP/DB imports
    user/
      user.ts      ← entity + value objects
      user.errors.ts
      user.service.ts
  infra/           ← adapters: DB, HTTP clients, queues
    db/
    http/
  api/             ← HTTP layer: routes, middleware, schemas
  lib/             ← shared utilities (result, logger, env)
  index.ts
```

- **`domain/` must not import from `infra/` or `api/`** — enforce with ESLint `import/no-restricted-paths`
- One file per class/module; keep files ≤ 300 lines
- Re-export from `index.ts` barrel files only for public APIs; avoid deep barrel chains inside a module

### Documentation

```ts
/**
 * Finds a user by their email address.
 *
 * @param email - Must be a valid, normalised email address.
 * @returns The matching user or `null` if not found.
 * @throws {DatabaseError} When the DB connection fails.
 */
async function findUserByEmail(email: string): Promise<User | null> { /* … */ }
```

- All public functions, classes, and types must have TSDoc comments
- Use `@param`, `@returns`, `@throws` tags
- No commented-out code in committed files

### Tooling Baseline

| Tool | Purpose | Config |
|------|---------|--------|
| **TypeScript** `5.x` | Compiler | `tsconfig.json` with strict flags above |
| **ESLint** + `typescript-eslint` | Linting | `recommended-type-checked` ruleset |
| **Prettier** | Formatting | `.prettierrc` |
| **Zod** | Runtime validation | Schema files co-located with domain |
| **Vitest** | Unit / integration tests | `vitest.config.ts` |

---

## Examples

### Fully typed service with Result pattern

```ts
import { z } from 'zod';

// --- Schema & types ---
const CreatePostSchema = z.object({
  title:   z.string().min(1).max(200),
  content: z.string().min(1),
  authorId: z.string().uuid(),
});
type CreatePostDto = z.infer<typeof CreatePostSchema>;

// --- Domain errors ---
class AuthorNotFoundError extends Error {
  readonly code = 'AUTHOR_NOT_FOUND' as const;
  constructor(readonly authorId: string) {
    super(`Author not found: ${authorId}`);
    this.name = 'AuthorNotFoundError';
  }
}

// --- Service ---
class PostService {
  constructor(
    private readonly postRepo: PostRepository,
    private readonly userRepo: UserRepository,
  ) {}

  async create(dto: CreatePostDto): Promise<Result<Post, AuthorNotFoundError>> {
    const author = await this.userRepo.findById(dto.authorId);
    if (!author) return err(new AuthorNotFoundError(dto.authorId));

    const post = await this.postRepo.create({
      title:    dto.title,
      content:  dto.content,
      authorId: dto.authorId,
    });
    return ok(post);
  }
}

// --- Controller ---
app.post('/posts', async (req, res) => {
  const parsed = CreatePostSchema.safeParse(req.body);
  if (!parsed.success) {
    return res.status(422).json({ error: parsed.error.format() });
  }

  const result = await postService.create(parsed.data);
  if (!result.ok) {
    return res.status(404).json({ error: result.error.code });
  }
  res.status(201).json(result.value);
});
```

## References

- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/)
- [typescript-eslint recommended-type-checked](https://typescript-eslint.io/users/configs#recommended-type-checked)
- [Zod documentation](https://zod.dev)
- [TypeScript 5.x release notes](https://www.typescriptlang.org/docs/handbook/release-notes/overview.html)
- [Effective TypeScript (Dan Vanderkam)](https://effectivetypescript.com/)
- [Total TypeScript](https://www.totaltypescript.com/)
- [code-quality skill](../../code-quality/SKILL.md)
