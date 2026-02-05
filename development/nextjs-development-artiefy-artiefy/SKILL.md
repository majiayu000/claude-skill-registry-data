---
name: nextjs-development
description: Specialized skill for developing with Next.js 16, including cache components, server actions, routing, and modern React patterns. Use when working on app router, server components, or Next.js specific features.
---

# Next.js Development Skill

This skill provides specialized knowledge and patterns for developing with Next.js 16 in the Artiefy project.

## When to Use This Skill

- Implementing new routes or pages in the app router
- Working with Server Components and Server Actions
- Configuring cache components and data fetching
- Handling layouts, error boundaries, and loading states
- Optimizing performance with Next.js 16 features

## Key Patterns and Conventions

### App Router Structure

- Use `src/app/` for all routes
- Role-based routing: `/super-admin`, `/admin`, `/educadores`, `/estudiantes`
- Server Components by default, mark client components with `'use client'`

### Server Actions

- Place in `src/server/` directory
- Use for form submissions and data mutations
- Validate with Zod schemas

### Data Fetching

- Server Components: Direct database queries
- Client Components: Use SWR for data fetching and caching
- Follow `Docs/doc-nextjs16/guia-swr-nextjs.md` for SWR patterns

### Cache Components

- Use `cacheComponents: false` in next.config.mjs (current setting)
- Implement manual caching with `unstable_cache` when needed
- Reference `Docs/doc-nextjs16/cache-components.md`

## Examples

### Creating a New Route

```tsx
// src/app/admin/new-page/page.tsx
export default function NewPage() {
  return (
    <div>
      <h1>New Admin Page</h1>
    </div>
  );
}
```

### Server Action

```ts
// src/server/actions/createUser.ts
'use server';

import { z } from 'zod';
import { db } from '@/server/db';

const schema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
});

export async function createUser(formData: FormData) {
  const data = schema.parse(Object.fromEntries(formData));
  await db.insert(users).values(data);
}
```

### Client Component with SWR

```tsx
'use client';
import useSWR from 'swr';

export function UserList({ initialData }) {
  const { data: users } = useSWR('/api/users', fetcher, {
    fallbackData: initialData,
  });

  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

## Resources

- [Next.js 16 Documentation](https://nextjs.org/docs)
- Project guides in `Docs/doc-nextjs16/`
- ESLint config: `eslint.config.mjs`
- TypeScript config: `tsconfig.json`
