---
name: reviewing-hook-patterns
description: Review React hook usage for React 19 compliance and best practices
review: true
allowed-tools: Read, Grep, Glob
version: 1.0.0
---

# Review: React Hook Patterns

Reviews React hook patterns for React 19 compliance, deprecated APIs, and best practices.

**Activates:** Code reviews, compliance validation, React 19 migration checks, hook-related PRs

**Scope:** New hooks (`use()`, `useActionState`, `useOptimistic`), deprecated patterns (forwardRef, propTypes, defaultProps), hook rules, best practices, TypeScript compliance

**Focus:** Correctness, security (Server Actions), performance (re-renders), React 19 compliance

## Review Process

### Phase 1: Find Deprecated APIs

Use Grep (output_mode: "content"):

- `forwardRef`
- `\.propTypes\s*=` (removed in React 19)
- `\.defaultProps\s*=` (deprecated on function components)

### Phase 2: Validate Hook Usage

**use() API**

- ✅ Promises or Context, Suspense-wrapped (Promises), Error Boundary (Promises)
- ❌ NOT in try-catch; Promises must be stable (outside component)

**useActionState**

- ✅ Server Action receives (previousState, formData), returns serializable values, has error handling, validates inputs server-side
- ❌ Missing authentication checks

**useOptimistic**

- ✅ Pure update function, paired with startTransition, visual pending indicator
- ❌ NOT for critical operations

**Standard Hooks** (useState, useEffect, etc.)

- ✅ Top-level calls, all dependencies included, cleanup functions for effects
- ❌ Missing dependencies, direct state mutation

### Phase 3: TypeScript Validation

**useRef** requires initial value:

```typescript
// ✅ Correct
const ref = useRef<HTMLDivElement>(null);

// ❌ Incorrect (React 19)
const ref = useRef<HTMLDivElement>();
```

**Ref as prop** typed correctly:

```typescript
// ✅ Correct
interface Props {
  ref?: Ref<HTMLButtonElement>;
}

// ❌ Incorrect (using forwardRef)
const Comp = forwardRef<HTMLButtonElement, Props>(...);
```

### Phase 4: Identify Anti-Patterns

**Array index as key:**

```javascript
// ❌ Bad
{
  items.map((item, index) => <div key={index}>{item}</div>);
}

// ✅ Good
{
  items.map((item) => <div key={item.id}>{item}</div>);
}
```

**Direct state mutation:**

```javascript
// ❌ Bad
const [items, setItems] = useState([]);
items.push(newItem);
setItems(items);

// ✅ Good
setItems([...items, newItem]);
```

**Missing dependencies:**

```javascript
// ❌ Bad
useEffect(() => {
  fetchData(userId);
}, []);

// ✅ Good
useEffect(() => {
  fetchData(userId);
}, [userId]);
```

**Missing cleanup:**

```javascript
// ❌ Bad
useEffect(() => {
  const timer = setInterval(() => {}, 1000);
}, []);

// ✅ Good
useEffect(() => {
  const timer = setInterval(() => {}, 1000);
  return () => clearInterval(timer);
}, []);
```

## Report Format

### ✅ Compliant Patterns

List correct React 19 usage, good practices, proper hooks.

### ⚠️ Warnings (Non-blocking)

Deprecated APIs still functional but require migration: forwardRef, manual memoization (when React Compiler available), patterns with better React 19 alternatives.

### ❌ Issues (Must Fix)

- **Removed APIs:** propTypes, defaultProps on function components, string refs
- **Security:** Unvalidated Server Actions, missing authentication, XSS vulnerabilities
- **Hook Rules:** Conditional calls, missing dependencies, hooks outside components

### 📝 Recommendations

Migration paths, performance improvements, best practices, relevant skill references.

## Example Review: Form Component

**Code:**

```javascript
import { useState } from 'react';

function ContactForm() {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');

  async function handleSubmit(e) {
    e.preventDefault();
    await fetch('/api/contact', {
      method: 'POST',
      body: JSON.stringify({ email, message }),
    });
  }

  return (
    <form onSubmit={handleSubmit}>
      <input value={email} onChange={(e) => setEmail(e.target.value)} />
      <textarea value={message} onChange={(e) => setMessage(e.target.value)} />
      <button type="submit">Send</button>
    </form>
  );
}
```

### ❌ Issues

1. **Missing Server Action Pattern** — Use `useActionState` with server validation instead of client-side fetch
2. **No Validation** — Add server-side validation (security risk)
3. **No Loading State** — Use `isPending` for UX feedback
4. **No Error Handling** — Return error state from Server Action

### 📝 Corrected Implementation

```javascript
'use client';

import { useActionState } from 'react';
import { submitContact } from './actions';

function ContactForm() {
  const [state, formAction, isPending] = useActionState(submitContact, null);

  return (
    <form action={formAction}>
      <input name="email" type="email" required />
      <textarea name="message" required />
      <button type="submit" disabled={isPending}>
        {isPending ? 'Sending...' : 'Send'}
      </button>
      {state?.error && <p className="error">{state.error}</p>}
      {state?.success && <p>Message sent!</p>}
    </form>
  );
}
```

**Server Action (actions.js):**

```javascript
'use server';

import { z } from 'zod';

const schema = z.object({
  email: z.string().email(),
  message: z.string().min(10),
});

export async function submitContact(previousState, formData) {
  const data = {
    email: formData.get('email'),
    message: formData.get('message'),
  };

  const result = schema.safeParse(data);
  if (!result.success) return { error: 'Invalid input' };

  try {
    await db.contacts.create({ data: result.data });
    return { success: true };
  } catch (error) {
    return { error: 'Failed to send message' };
  }
}
```

## Example Review: forwardRef Component

**Code:**

```javascript
import { forwardRef } from 'react';

const Button = forwardRef((props, ref) => (
  <button ref={ref} {...props}>
    {props.children}
  </button>
));

Button.displayName = 'Button';
```

### ⚠️ Warnings

**Deprecated forwardRef Usage** — Still functional in React 19 but deprecated. Migrate to ref-as-prop pattern.

### 📝 React 19 Migration

```javascript
function Button({ children, ref, ...props }) {
  return (
    <button ref={ref} {...props}>
      {children}
    </button>
  );
}
```

**Benefits:** Simpler API, better TypeScript inference, follows React 19 patterns, less boilerplate.

## Review Standards

**MUST Flag:**

- Removed APIs (propTypes, defaultProps on functions, string refs)
- Hook rule violations (conditional calls, missing dependencies)
- Security issues (unvalidated Server Actions, missing auth)
- Missing Suspense/Error Boundaries for `use()` with Promises

**SHOULD Flag:**

- Deprecated APIs (forwardRef)
- Performance issues (unnecessary re-renders, missing memoization when needed)
- Missing TypeScript types for React 19 patterns
- Anti-patterns (array index keys, direct state mutation)

**MAY Suggest:**

- Better React 19 patterns available
- Component architecture improvements
- Code organization enhancements

**NEVER:**

- Enforce personal style preferences
- Require changes that don't improve correctness/security/performance
- Flag patterns working correctly in React 19
- Demand premature optimization

## Review Checklist

### New React 19 Features

- [ ] `use()` + Promises: Suspense + Error Boundary
- [ ] `use()` + Context: appropriate usage
- [ ] `useActionState`: Server Actions validate inputs
- [ ] `useOptimistic`: paired with `startTransition`
- [ ] `useFormStatus`: inside form components

### Deprecated Patterns

- [ ] No forwardRef or flagged for migration
- [ ] No propTypes on function components
- [ ] No defaultProps on function components
- [ ] No string refs

### Hook Rules

- [ ] All hooks at top level
- [ ] No conditional hook calls
- [ ] All dependencies included
- [ ] Cleanup functions for subscriptions

### TypeScript (if applicable)

- [ ] `useRef` has initial value
- [ ] Ref props typed with `Ref<HTMLElement>`
- [ ] Server Actions properly typed
- [ ] No deprecated type patterns

### Security

- [ ] Server Actions validate inputs
- [ ] Authentication checks present where needed
- [ ] `dangerouslySetInnerHTML` sanitized
- [ ] No sensitive data exposed to client

### Performance

- [ ] No array index as key
- [ ] No direct state mutation
- [ ] No missing dependencies (stale closures)
- [ ] Reasonable component structure

## Common Issues Reference

| Issue                       | Search Pattern       | Fix                     |
| --------------------------- | -------------------- | ----------------------- |
| forwardRef usage            | `forwardRef`         | Convert to ref-as-prop  |
| propTypes                   | `\.propTypes\s*=`    | Remove (use TypeScript) |
| defaultProps                | `\.defaultProps\s*=` | Use ES6 defaults        |
| Missing dependencies        | Manual review        | Add to dependency array |
| Array index keys            | `key={.*index}`      | Use stable ID           |
| Direct mutation             | Manual review        | Use immutable updates   |
| use() without Suspense      | Manual review        | Add Suspense boundary   |
| Server Action no validation | Manual review        | Add zod/yup validation  |

For comprehensive React 19 patterns and migration guides, see: `research/react-19-comprehensive.md`
