---
name: implementing-server-actions
description: Teaches Server Actions in React 19 for form handling and data mutations. Use when implementing forms, mutations, or server-side logic. Server Actions are async functions marked with 'use server'.
allowed-tools: Read, Write, Edit
version: 1.0.0
---

# Server Actions

Server Actions are async functions executed on the server, callable from Client Components.

## Key Concepts

**Defining Server Actions:**

```javascript
'use server';

export async function createUser(formData) {
  const name = formData.get('name');
  const email = formData.get('email');

  const user = await db.users.create({ name, email });
  return { success: true, userId: user.id };
}
```

**Using in Forms:**

```javascript
'use client';

import { createUser } from './actions';

function SignupForm() {
  return (
    <form action={createUser}>
      <input name="name" required />
      <input name="email" type="email" required />
      <button type="submit">Sign Up</button>
    </form>
  );
}
```

## Security Requirements

**MUST validate all inputs:**

```javascript
'use server';

import { z } from 'zod';

const schema = z.object({
  name: z.string().min(2).max(50),
  email: z.string().email(),
});

export async function createUser(formData) {
  const result = schema.safeParse({
    name: formData.get('name'),
    email: formData.get('email'),
  });

  if (!result.success) {
    return { error: result.error.flatten().fieldErrors };
  }

  const user = await db.users.create(result.data);
  return { success: true, userId: user.id };
}
```

**MUST check authentication:**

```javascript
'use server';

export async function deletePost(postId) {
  const session = await getSession();

  if (!session?.user) {
    throw new Error('Unauthorized');
  }

  const post = await db.posts.findUnique({ where: { id: postId } });

  if (post.authorId !== session.user.id) {
    throw new Error('Forbidden');
  }

  await db.posts.delete({ where: { id: postId } });
  return { success: true };
}
```

## Progressive Enhancement

Server Actions work before JavaScript loads:

```javascript
'use client';

import { useActionState } from 'react';
import { submitForm } from './actions';

function Form() {
  const [state, formAction] = useActionState(
    submitForm,
    null,
    '/api/submit'
  );

  return <form action={formAction}>...</form>;
}
```

For comprehensive Server Actions documentation, see: `research/react-19-comprehensive.md` lines 644-733.

## Related Skills

**Zod v4 Error Handling:**
- handling-zod-errors skill from the zod-4 plugin - SafeParse pattern, error flattening, and user-friendly error messages for server action validation

**Prisma 6 Integration:**
- If setting up PrismaClient singleton pattern for Server Actions in serverless Next.js, use the creating-client-singletons skill from prisma-6 for proper initialization preventing connection pool exhaustion.
- If validating database inputs in server actions, use the validating-query-inputs skill from prisma-6 for Zod validation pipeline patterns
- If ensuring type-safe Prisma queries with GetPayload patterns, use the ensuring-query-type-safety skill from prisma-6 for type-safe database operations
- For multi-step mutations and complex database operations, use the handling-transaction-errors skill from prisma-6 for comprehensive transaction error handling in server actions
