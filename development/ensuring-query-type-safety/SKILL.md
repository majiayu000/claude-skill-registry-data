---
name: ensuring-query-type-safety
description: Use Prisma's generated types, `Prisma.validator`, and `GetPayload` for type-safe queries.
allowed-tools: Read, Write, Edit
---

# Type-Safe Queries in Prisma 6

Ensure type safety in all database queries using Prisma's generated types, `Prisma.validator` for custom fragments, and `GetPayload` for type inference.

## Generated Types

Prisma automatically generates TypeScript types from your schema.

**Basic Usage:**

```typescript
import { Prisma, User } from '@prisma/client';

async function getUser(id: string): Promise<User | null> {
  return prisma.user.findUnique({ where: { id } });
}
```

**With Relations:**

```typescript
type UserWithPosts = Prisma.UserGetPayload<{ include: { posts: true } }>;

async function getUserWithPosts(id: string): Promise<UserWithPosts | null> {
  return prisma.user.findUnique({
    where: { id },
    include: { posts: true },
  });
}
```

## Prisma.validator for Custom Types

Use `Prisma.validator` to create reusable, type-safe query fragments.

```typescript
// Query validator
const userWithProfile = Prisma.validator<Prisma.UserDefaultArgs>()({
  include: {
    profile: true,
    posts: {
      where: { published: true },
      orderBy: { createdAt: 'desc' },
    },
  },
});

type UserWithProfile = Prisma.UserGetPayload<typeof userWithProfile>;

async function getCompleteUser(id: string): Promise<UserWithProfile | null> {
  return prisma.user.findUnique({
    where: { id },
    ...userWithProfile,
  });
}

// Input validator
const createUserInput = Prisma.validator<Prisma.UserCreateInput>()({
  email: 'user@example.com',
  name: 'John Doe',
  profile: { create: { bio: 'Software developer' } },
});

async function createUser(data: typeof createUserInput) {
  return prisma.user.create({ data });
}

// Where clause validator
const activeUsersWhere = Prisma.validator<Prisma.UserWhereInput>()({
  isActive: true,
  deletedAt: null,
  posts: { some: { published: true } },
});

async;

function findActiveUsers() {
  return prisma.user.findMany({ where: activeUsersWhere });
}
```

## GetPayload Patterns

Infer types from query shapes using `GetPayload`.

```typescript
// Complex selections
const postWithAuthor = Prisma.validator<Prisma.PostDefaultArgs>()({
  select: {
    id: true,
    title: true,
    content: true,
    author: { select: { id: true, name: true, email: true } },
    tags: { select: { id: true, name: true } },
  },
});

type PostWithAuthor = Prisma.PostGetPayload<typeof postWithAuthor>;

async function getPostDetails(id: string): Promise<PostWithAuthor | null> {
  return prisma.post.findUnique({
    where: { id },
    ...postWithAuthor,
  });
}

// Nested GetPayload
type UserWithPostsAndComments = Prisma.UserGetPayload<{
  include: {
    posts: {
      include: {
        comments: { include: { author: true } };
      };
    };
  };
}>;

const userArgs = Prisma.validator<Prisma.UserDefaultArgs>()({
  include: {
    posts: {
      include: {
        comments: { include: { author: true } },
      },
    },
  },
});

async function getUserWithActivity(id: string): Promise<UserWithPostsAndComments | null> {
  return prisma.user.findUnique({
    where: { id },
    ...userArgs,
  });
}
```

## Avoiding `any`

Leverage TypeScript's type system instead of `any`.

```typescript
// Type-safe partial selections
function buildUserSelect<T extends Prisma.UserSelect>(
  select: T
): Prisma.UserGetPayload<{ select: T }> | null {
  return prisma.user.findFirst({ select }) as any;
}

type UserBasic = Prisma.UserGetPayload<{
  select: { id: true; email: true; name: true };
}>;

const userSelect = Prisma.validator<Prisma.UserSelect>()({
  id: true,
  email: true,
  name: true,
});

async function getUserBasic(id: string): Promise<UserBasic | null> {
  return prisma.user.findUnique({
    where: { id },
    select: userSelect,
  });
}

// Type-safe query builders
class TypedQueryBuilder<T> {
  constructor(private model: string) {}

  async findMany<A extends Prisma.UserDefaultArgs>(args?: A): Promise<Prisma.UserGetPayload<A>[]> {
    return prisma.user.findMany(args);
  }

  async findUnique<A extends Prisma.UserDefaultArgs>(
    args: Prisma.SelectSubset<A, Prisma.UserFindUniqueArgs>
  ): Promise<Prisma.UserGetPayload<A> | null> {
    return prisma.user.findUnique(args);
  }
}

const userQuery = new TypedQueryBuilder('user');
const users = await userQuery.findMany({
  where: { isActive: true },
  include: { posts: true },
});

// Conditional types
type UserArgs<T extends boolean> = T extends true
  ? Prisma.UserGetPayload<{ include: { posts: true } }>
  : Prisma.UserGetPayload<{ select: { id: true; email: true } }>;

async function getUser<T extends boolean>(
  id: string,
  includePosts: T
): Promise<UserArgs<T> | null> {
  if (includePosts) {
    return prisma.user.findUnique({
      where: { id },
      include: { posts: true },
    }) as Promise<UserArgs<T> | null>;
  }
  return prisma.user.findUnique({
    where: { id },
    select: { id: true, email: true },
  }) as Promise<UserArgs<T> | null>;
}
```

## Advanced Patterns

**Reusable Type-Safe Includes:**

```typescript
const includes = {
  userWithProfile: Prisma.validator<Prisma.UserDefaultArgs>()({
    include: { profile: true },
  }),
  userWithPosts: Prisma.validator<Prisma.UserDefaultArgs>()({
    include: { posts: { where: { published: true } } },
  }),
  userComplete: Prisma.validator<Prisma.UserDefaultArgs>()({
    include: { profile: true, posts: true, comments: true },
  }),
} as const;

type UserWithProfile = Prisma.UserGetPayload<typeof includes.userWithProfile>;
type UserWithPosts = Prisma.UserGetPayload<typeof includes.userWithPosts>;
type UserComplete = Prisma.UserGetPayload<typeof includes.userComplete>;

async function getUserVariant(
  id: string,
  variant: keyof typeof includes
): Promise<UserWithProfile | UserWithPosts | UserComplete | null> {
  return prisma.user.findUnique({
    where: { id },
    ...includes[variant],
  });
}
```

**Type-Safe Dynamic Queries:**

```typescript
type DynamicUserArgs = {
  includeProfile?: boolean;
  includePosts?: boolean;
  includeComments?: boolean;
};

function buildUserArgs(options: DynamicUserArgs): Prisma.UserDefaultArgs {
  const args: Prisma.UserDefaultArgs = {};
  if (options.includeProfile || options.includePosts || options.includeComments) {
    args.include = {};
    if (options.includeProfile) args.include.profile = true;
    if (options.includePosts) args.include.posts = true;
    if (options.includeComments) args.include.comments = true;
  }
  return args;
}

async function getDynamicUser(id: string, options: DynamicUserArgs) {
  return prisma.user.findUnique({
    where: { id },
    ...buildUserArgs(options),
  });
}
```

## Key Principles

1. Always use generated types from `@prisma/client`
2. Use `Prisma.validator` for reusable query fragments
3. Derive types from query shapes via `GetPayload`
4. Avoid `any`; leverage TypeScript's type system
5. Type dynamic queries with proper generics
6. Create const validators for common patterns

## Related Skills

**TypeScript Type Safety:**

- If avoiding any types in TypeScript, use the avoiding-any-types skill from typescript for strict type patterns
- If implementing generic patterns for type-safe queries, use the using-generics skill from typescript for advanced generic techniques
