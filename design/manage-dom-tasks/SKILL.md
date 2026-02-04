---
name: manage-dom-tasks
description: Create or update DOM event "tasks" used to communicate between components and services via `src/helpers/domTask.ts`. Use when adding a new task event, changing task params/returns, or updating handlers/dispatchers for those tasks in `src/setup/tasks.ts`, pages, or services.
---

# Manage DOM Tasks

Follow these steps to create or update a task (DOM event) in this project.

## 1) Find or add the task registry entry

Edit `src/setup/tasks.ts` to extend `TaskEventRegistry` with the task name, params, and return type.

Example (new task):

```ts
declare module '../helpers/domTask' {
  interface TaskEventRegistry {
    'login': { params: { user: string; password: string }; returns: void }
  }
}
```

Use discriminated unions for conditional params (e.g., when some params only apply for certain types):

```ts
declare module '../helpers/domTask' {
  interface TaskEventRegistry {
    'login': {
      params:
        | { type: 'google' }
        | { type: 'email'; email: string; password: string }
      returns: void
    }
  }
}
```

## 2) Update dispatchers (components/pages)

Find all dispatchers via `dispatchTask` (or `createTaskEvent`) and update params to match the registry type.

Example:

```ts
dispatchTask(this, 'login', { type: 'email', email, password })
```

## 3) Update handlers (services/components)

Update task handlers registered via `registerTaskHandler`, or decorators via `@taskHandler`.
Ensure handler signatures align with the registry params and return type.

Example:

```ts
registerTaskHandler('login', async (params) => {
  if (params.type === 'google') return
  await signInWithEmail(params.email, params.password)
})
```

## 4) Verify usage consistency

Use `rg` to find all occurrences of the task name and update:

- `dispatchTask(this, 'task-name', ...)`
- `registerTaskHandler('task-name', ...)`
- `@taskHandler('task-name')`

Prefer updating types first in `src/setup/tasks.ts` so TypeScript surfaces mismatches.
