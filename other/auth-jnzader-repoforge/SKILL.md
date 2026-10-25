---
name: add-auth-endpoint
description: >
  Adding authentication endpoints and managing auth state across the app.
  Trigger: when adding new auth-protected routes or API calls.
license: Apache-2.0
metadata:
  author: repoforge
  version: "1.0"
  complexity: low
  token_estimate: 450
  dependencies: []
  related_skills: []
  load_priority: high
---

<!-- L1:START -->
# add-auth-endpoint

One sentence: Adding authentication endpoints and managing auth state across the app.

**Trigger**: when adding new auth-protected routes or API calls.
<!-- L1:END -->

<!-- L2:START -->
## Quick Reference

| Task | Pattern |
|------|---------|
| Add auth provider | `<AuthProvider>` |
| Get auth state | `useAuth()` |
<!-- L2:END -->

<!-- L3:START -->
## Critical Patterns

### Use AuthProvider to wrap app

Wrap the app shell with `AuthProvider` to make `useAuth` available throughout the component tree.

```typescript
import { AuthProvider } from '@/lib/auth';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <AuthProvider>
    <App />
  </AuthProvider>,
);
```

### Use useAuth to access context

Call `useAuth()` anywhere inside a provider-wrapped tree to get the auth context without prop-drilling.

```typescript
const { token, loading } = useAuth();
if (loading) return <LoadingSpinner />;
```

## When to Use

- Adding a new protected API route
- Checking auth state in a component
- Accessing user token globally

## Commands

```bash
docker build -t myapp .
docker run -p 3000:80 myapp
```

## Anti-Patterns

### Don't: Access auth outside AuthProvider

Calling `useAuth()` outside an `AuthProvider` boundary throws an error.

```typescript
const { token } = useAuth(); // BAD: throws 'useAuth must be used within an AuthProvider'
```
<!-- L3:END -->