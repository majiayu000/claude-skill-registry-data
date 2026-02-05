---
name: validating-forms
description: Teaches client and server-side form validation patterns in React 19 with Server Actions. Use when implementing form validation, input checking, or error handling.
allowed-tools: Read, Write, Edit
version: 1.0.0
---

# Form Validation Patterns

React 19 forms require validation on both client and server.

## Client-Side Validation

Use HTML5 validation + custom logic:

```javascript
<form action={submitForm}>
  <input
    name="email"
    type="email"
    required
    pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$"
  />

  <input
    name="age"
    type="number"
    min="18"
    max="120"
    required
  />

  <button type="submit">Submit</button>
</form>
```

## Server-Side Validation (Required)

**Always validate on server** - client validation can be bypassed:

```javascript
'use server';

import { z } from 'zod';

const schema = z.object({
  email: z.string().email('Invalid email'),
  age: z.number().min(18, 'Must be 18+').max(120),
  password: z.string().min(8, 'Password must be 8+ characters'),
});

export async function registerUser(previousState, formData) {
  const data = {
    email: formData.get('email'),
    age: Number(formData.get('age')),
    password: formData.get('password'),
  };

  const result = schema.safeParse(data);

  if (!result.success) {
    return {
      errors: result.error.flatten().fieldErrors,
    };
  }

  try {
    const user = await db.users.create({ data: result.data });
    return { success: true, userId: user.id };
  } catch (error) {
    if (error.code === 'P2002') {
      return { errors: { email: ['Email already exists'] } };
    }
    return { error: 'Registration failed' };
  }
}
```

## Display Errors

```javascript
'use client';

import { useActionState } from 'react';
import { registerUser } from './actions';

export default function RegisterForm() {
  const [state, formAction, isPending] = useActionState(registerUser, null);

  return (
    <form action={formAction}>
      <div>
        <input name="email" type="email" required />
        {state?.errors?.email && (
          <span className="error">{state.errors.email[0]}</span>
        )}
      </div>

      <div>
        <input name="age" type="number" required />
        {state?.errors?.age && (
          <span className="error">{state.errors.age[0]}</span>
        )}
      </div>

      <div>
        <input name="password" type="password" required />
        {state?.errors?.password && (
          <span className="error">{state.errors.password[0]}</span>
        )}
      </div>

      <button type="submit" disabled={isPending}>
        {isPending ? 'Registering...' : 'Register'}
      </button>

      {state?.error && <p className="error">{state.error}</p>}
      {state?.success && <p>Registration successful!</p>}
    </form>
  );
}
```

## Validation Libraries

Recommended: **Zod** for type-safe validation:

```javascript
import { z } from 'zod';

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  confirmPassword: z.string(),
}).refine(data => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ['confirmPassword'],
});
```

For comprehensive validation patterns, see: `research/react-19-comprehensive.md`.

## Related Skills

**Zod v4 Validation:**
- handling-zod-errors skill from the zod-4 plugin - Advanced error customization with unified error API, custom messages, and error formatting for better user feedback
- writing-zod-transformations skill from the zod-4 plugin - Built-in string transformations (trim, toLowerCase) for normalizing user input before validation
