---
name: using-the-use-hook
description: React 19's use() API for reading Promises/Context conditionally. For async data fetching, Suspense, conditional context access, useContext migration.
allowed-tools: Read, Write, Edit, Glob, Grep
version: 1.0.0
---

# Using the `use()` Hook in React 19

Teaches when and how to use React 19's new `use()` API: reads Promises (suspending component) and Context (conditionally—inside if statements, loops, after early returns).

**Activates when**: User mentions `use()`, `use hook`, async patterns, Suspense + data fetching, conditional context, or useContext migration.

## Key Capabilities vs. Traditional Hooks

| Feature            | Hooks     | `use()`        |
| ------------------ | --------- | -------------- |
| Conditional calls  | ❌        | ✅             |
| After early return | ❌        | ✅             |
| Inside loops       | ❌        | ✅             |
| Read Promises      | ❌        | ✅ (suspends)  |
| Error handling     | try-catch | Error Boundary |

## Usage Patterns

**Reading Promises**:

```javascript
import { use, Suspense } from 'react';

async function fetchUser(id) {
  const res = await fetch(`/api/users/${id}`);
  return res.json();
}

function UserProfile({ userId }) {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <UserData promise={fetchUser(userId)} />
    </Suspense>
  );
}

function UserData({ promise }) {
  const user = use(promise);
  return <div>{user.name}</div>;
}
```

**Conditional Context Access**:

```javascript
import { use, createContext } from 'react';

const ThemeContext = createContext('light');

function Button({ isPrimary, children }) {
  let className = 'button';
  if (isPrimary) {
    const theme = use(ThemeContext);
    className += ` ${theme}`;
  }
  return <button className={className}>{children}</button>;
}
```

**Reusable Custom Hook**:

```javascript
import { use, cache } from 'react';

const getUser = cache(async (id) => {
  const res = await fetch(`/api/users/${id}`);
  return res.json();
});

function useUser(userId) {
  if (!userId) return null;
  return use(getUser(userId));
}
```

## Implementation Workflow

**Async data**: Pass Promise as prop from parent → wrap component in Suspense boundary → use `use(promise)` in child → catch errors with Error Boundary.

**Conditional context**: Replace `useContext(Context)` with `use(Context)` for flexibility across conditional branches, loops, post-early-return.

**Migration from useContext**: Find `useContext(Context)` calls → replace with `use(Context)` → benefits: now conditional if needed.

## Requirements & Validation

**MUST**:

- Wrap `use(promise)` in Suspense boundary with fallback
- Use Error Boundary (not try-catch) for error handling
- Create Promises in parents/Server Components, pass as props
- Use `cache()` wrapper to prevent duplicate requests

**NEVER**:

- Call `use()` inside try-catch blocks
- Create new Promises inside component (causes infinite loops)
- Use `use()` outside Component/Hook functions
- Omit Suspense boundary for Promises

**Verify**:

1. Suspense boundary wraps every `use(promise)` with fallback
2. Error Boundary catches Promise errors
3. Promises created externally or with `cache()`—stable across renders
4. All conditional logic branches tested

---

For comprehensive React 19 `use()` documentation:

`research/react-19-comprehensive.md` lines 241–311 (use API, Promise Patterns, useContext sections).
