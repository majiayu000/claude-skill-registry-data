---
name: serialization-patterns
description: Data serialization and transformation patterns. Use when formatting API responses.
---

# Serialization Patterns Skill

This skill covers data serialization and transformation for API responses.

## When to Use

Use this skill when:
- Formatting API responses
- Transforming database models
- Hiding sensitive fields
- Normalizing data structures

## Core Principle

**SEPARATE INTERNAL FROM EXTERNAL** - Internal models differ from API responses. Transform explicitly.

## Basic Transformation

```typescript
// src/serializers/user.ts
import { User } from '@prisma/client';

interface UserResponse {
  id: string;
  email: string;
  name: string;
  role: string;
  createdAt: string;
}

export function serializeUser(user: User): UserResponse {
  return {
    id: user.id,
    email: user.email,
    name: user.name,
    role: user.role,
    createdAt: user.createdAt.toISOString(),
  };
}

export function serializeUsers(users: User[]): UserResponse[] {
  return users.map(serializeUser);
}
```

## Class-Based Serializer

```typescript
// src/serializers/base.ts
export abstract class Serializer<TModel, TResponse> {
  abstract serialize(model: TModel): TResponse;

  serializeMany(models: TModel[]): TResponse[] {
    return models.map((model) => this.serialize(model));
  }
}

// src/serializers/user.ts
import { User, Profile } from '@prisma/client';
import { Serializer } from './base';

interface UserResponse {
  id: string;
  email: string;
  name: string;
  profile: ProfileResponse | null;
}

interface ProfileResponse {
  bio: string | null;
  avatar: string | null;
}

type UserWithProfile = User & { profile: Profile | null };

export class UserSerializer extends Serializer<UserWithProfile, UserResponse> {
  serialize(user: UserWithProfile): UserResponse {
    return {
      id: user.id,
      email: user.email,
      name: user.name,
      profile: user.profile ? {
        bio: user.profile.bio,
        avatar: user.profile.avatar,
      } : null,
    };
  }
}

// Usage
const serializer = new UserSerializer();
const response = serializer.serialize(user);
const responses = serializer.serializeMany(users);
```

## Conditional Fields

```typescript
interface UserResponse {
  id: string;
  email: string;
  name: string;
  role: string;
  // Admin-only fields
  lastLoginAt?: string;
  loginCount?: number;
}

interface SerializeOptions {
  includeAdminFields?: boolean;
}

export function serializeUser(
  user: User,
  options: SerializeOptions = {}
): UserResponse {
  const base: UserResponse = {
    id: user.id,
    email: user.email,
    name: user.name,
    role: user.role,
  };

  if (options.includeAdminFields) {
    return {
      ...base,
      lastLoginAt: user.lastLoginAt?.toISOString(),
      loginCount: user.loginCount,
    };
  }

  return base;
}
```

## Nested Serialization

```typescript
// src/serializers/post.ts
import { Post, User, Tag } from '@prisma/client';

interface PostResponse {
  id: string;
  title: string;
  slug: string;
  content: string | null;
  published: boolean;
  author: AuthorResponse;
  tags: TagResponse[];
  createdAt: string;
  updatedAt: string;
}

interface AuthorResponse {
  id: string;
  name: string;
}

interface TagResponse {
  id: string;
  name: string;
}

type PostWithRelations = Post & {
  author: User;
  tags: Tag[];
};

export function serializePost(post: PostWithRelations): PostResponse {
  return {
    id: post.id,
    title: post.title,
    slug: post.slug,
    content: post.content,
    published: post.published,
    author: {
      id: post.author.id,
      name: post.author.name,
    },
    tags: post.tags.map((tag) => ({
      id: tag.id,
      name: tag.name,
    })),
    createdAt: post.createdAt.toISOString(),
    updatedAt: post.updatedAt.toISOString(),
  };
}
```

## Paginated Response

```typescript
// src/serializers/pagination.ts
interface PaginatedResponse<T> {
  data: T[];
  meta: {
    total: number;
    page: number;
    perPage: number;
    totalPages: number;
    hasMore: boolean;
  };
  links: {
    first: string;
    prev: string | null;
    next: string | null;
    last: string;
  };
}

interface PaginationInput {
  items: unknown[];
  total: number;
  page: number;
  perPage: number;
  baseUrl: string;
}

export function serializePaginated<T>(
  input: PaginationInput,
  serializer: (item: unknown) => T
): PaginatedResponse<T> {
  const { items, total, page, perPage, baseUrl } = input;
  const totalPages = Math.ceil(total / perPage);

  return {
    data: items.map(serializer),
    meta: {
      total,
      page,
      perPage,
      totalPages,
      hasMore: page < totalPages,
    },
    links: {
      first: `${baseUrl}?page=1&perPage=${perPage}`,
      prev: page > 1 ? `${baseUrl}?page=${page - 1}&perPage=${perPage}` : null,
      next: page < totalPages ? `${baseUrl}?page=${page + 1}&perPage=${perPage}` : null,
      last: `${baseUrl}?page=${totalPages}&perPage=${perPage}`,
    },
  };
}
```

## JSON:API Format

```typescript
// src/serializers/jsonapi.ts
interface JsonApiResource<T> {
  type: string;
  id: string;
  attributes: T;
  relationships?: Record<string, JsonApiRelationship>;
}

interface JsonApiRelationship {
  data: { type: string; id: string } | { type: string; id: string }[];
}

interface JsonApiResponse<T> {
  data: JsonApiResource<T> | JsonApiResource<T>[];
  included?: JsonApiResource<unknown>[];
}

export function toJsonApi<T extends { id: string }>(
  type: string,
  data: T
): JsonApiResource<Omit<T, 'id'>> {
  const { id, ...attributes } = data;
  return {
    type,
    id,
    attributes: attributes as Omit<T, 'id'>,
  };
}

// Usage
const user = { id: '1', name: 'John', email: 'john@example.com' };
const response = toJsonApi('user', user);
// { type: 'user', id: '1', attributes: { name: 'John', email: '...' } }
```

## Hiding Sensitive Data

```typescript
// src/serializers/sanitize.ts
type SensitiveFields = 'password' | 'passwordHash' | 'apiKey' | 'secret';

export function sanitize<T extends Record<string, unknown>>(
  obj: T
): Omit<T, SensitiveFields> {
  const sensitiveKeys: SensitiveFields[] = [
    'password',
    'passwordHash',
    'apiKey',
    'secret',
  ];

  const result = { ...obj };
  for (const key of sensitiveKeys) {
    delete result[key];
  }
  return result as Omit<T, SensitiveFields>;
}

// With deep sanitization
export function deepSanitize<T>(obj: T): T {
  if (obj === null || typeof obj !== 'object') {
    return obj;
  }

  if (Array.isArray(obj)) {
    return obj.map(deepSanitize) as T;
  }

  const sensitiveKeys = ['password', 'passwordHash', 'apiKey', 'secret'];
  const result: Record<string, unknown> = {};

  for (const [key, value] of Object.entries(obj)) {
    if (!sensitiveKeys.includes(key)) {
      result[key] = deepSanitize(value);
    }
  }

  return result as T;
}
```

## Date Formatting

```typescript
// src/serializers/date.ts
export function toISOString(date: Date | null | undefined): string | null {
  return date?.toISOString() ?? null;
}

export function toUnixTimestamp(date: Date | null | undefined): number | null {
  return date ? Math.floor(date.getTime() / 1000) : null;
}

export function toRelativeTime(date: Date): string {
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffSecs = Math.floor(diffMs / 1000);
  const diffMins = Math.floor(diffSecs / 60);
  const diffHours = Math.floor(diffMins / 60);
  const diffDays = Math.floor(diffHours / 24);

  if (diffDays > 0) return `${diffDays}d ago`;
  if (diffHours > 0) return `${diffHours}h ago`;
  if (diffMins > 0) return `${diffMins}m ago`;
  return 'just now';
}
```

## Response Envelope

```typescript
// src/serializers/envelope.ts
interface SuccessResponse<T> {
  success: true;
  data: T;
}

interface ErrorResponse {
  success: false;
  error: {
    code: string;
    message: string;
    details?: unknown;
  };
}

type ApiResponse<T> = SuccessResponse<T> | ErrorResponse;

export function success<T>(data: T): SuccessResponse<T> {
  return { success: true, data };
}

export function error(
  code: string,
  message: string,
  details?: unknown
): ErrorResponse {
  return {
    success: false,
    error: { code, message, details },
  };
}

// Usage in routes
fastify.get('/users/:id', async (request, reply) => {
  const user = await findUser(request.params.id);

  if (!user) {
    return reply.status(404).send(error('NOT_FOUND', 'User not found'));
  }

  return success(serializeUser(user));
});
```

## Fastify Response Serialization

```typescript
// Configure Fastify to use custom serializer
import { FastifyInstance } from 'fastify';

export function configureSerializers(fastify: FastifyInstance): void {
  fastify.setReplySerializer((payload) => {
    return JSON.stringify(payload, (key, value) => {
      // Convert Dates to ISO strings
      if (value instanceof Date) {
        return value.toISOString();
      }
      // Convert BigInt to string
      if (typeof value === 'bigint') {
        return value.toString();
      }
      return value;
    });
  });
}
```

## Best Practices

1. **Explicit transformation** - Never return raw database models
2. **Type safety** - Define response types explicitly
3. **Hide sensitive data** - Remove passwords, keys, secrets
4. **Consistent format** - Same structure across endpoints
5. **Date handling** - Use ISO 8601 format
6. **Null handling** - Be explicit about null vs undefined

## Notes

- Serializers are pure functions
- Test serializers independently
- Document response formats in OpenAPI
- Consider versioned serializers for API versions
