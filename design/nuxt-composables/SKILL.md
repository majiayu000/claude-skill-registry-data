---
name: nuxt-composables
description: Creating custom Vue composables with proper patterns. Use when building reusable stateful logic, shared state management, or encapsulating feature-specific behavior.
---

# Nuxt Composables

Creating reusable stateful logic via Vue Composition API.

## Core Concepts

**[composables.md](references/composables.md)** - Patterns, naming, state management, best practices

## Singleton Pattern (Shared State)

State defined outside function persists across all callers:

```typescript
// app/composables/useUser.ts
let user = ref<User>()  // Singleton - shared across app

export default function useUser() {
  const setUser = (data: BaseEntity) => {
    user.value = User.hydrate(data)
  }
  const clearUser = () => { user.value = undefined }

  return { user, setUser, clearUser }
}
```

## Factory Pattern (Fresh State)

State defined inside function - new instance per call:

```typescript
// app/composables/useCounter.ts
export default function useCounter(initial = 0) {
  const count = ref(initial)  // Fresh per call
  const increment = () => count.value++
  const decrement = () => count.value--

  return { count, increment, decrement }
}
```

## Naming & File Conventions

| Convention | Example |
|------------|---------|
| File name | `useUser.ts`, `useCategories.ts` |
| Function | `export default function useUser()` |
| Return | Always object `{ state, methods }` |
| Refs | Reactive: `user`, not `userRef` |
