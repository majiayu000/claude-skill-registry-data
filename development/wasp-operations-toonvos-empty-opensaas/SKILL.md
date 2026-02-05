---
name: wasp-operations
description: Complete Wasp operations patterns for queries and actions. Use when creating backend operations, implementing queries/actions, or working with server-side code. Includes type annotations, auth checks, entity access, client usage, and error handling.
triggers:
  [
    "create query",
    "add action",
    "operation",
    "backend",
    "server code",
    "query",
    "action",
    "operations.ts",
    "wasp operation",
    "server operation",
  ]
version: 1.0
last_updated: 2025-10-18
allowed_tools: [Read, Write, Edit, Bash]
---

# Wasp Operations Skill

## Quick Reference

**When to use this skill:**

- Creating new queries or actions
- Implementing backend operations
- Working with operations.ts files
- Setting up client-server communication
- Need auth checks, permissions, or validation patterns

**Key concepts:**

- Queries: Read operations using useQuery hook
- Actions: Write operations using direct async/await (NOT useAction by default)
- Type annotations: CRITICAL for context.entities access
- Auto-invalidation: Queries refetch when actions with same entities complete

---

## Complete Workflow

### 1. Define in main.wasp

**Location:** `app/main.wasp`

**Query declaration (READ operations):**

```wasp
query getTasks {
  fn: import { getTasks } from "@src/server/a3/operations",
  entities: [Task]  // REQUIRED for context.entities + auto-invalidation
}

query getTask {
  fn: import { getTask } from "@src/server/a3/operations",
  entities: [Task]
}
```

**Action declaration (WRITE operations):**

```wasp
action createTask {
  fn: import { createTask } from "@src/server/a3/operations",
  entities: [Task]  // Same entities as getTasks → auto-invalidates getTasks!
}

action updateTask {
  fn: import { updateTask } from "@src/server/a3/operations",
  entities: [Task]  // Auto-invalidates getTasks query
}

action deleteTask {
  fn: import { deleteTask } from "@src/server/a3/operations",
  entities: [Task]  // Auto-invalidates getTasks query
}
```

**Critical rules:**

- ✅ Use `@src/` prefix in main.wasp imports (NOT relative paths)
- ✅ List ALL entities accessed in `entities: [...]` array
- ✅ Same entities in query + action = auto-invalidation

---

### 2. Implement in operations.ts

**Location:** `app/src/{feature}/operations.ts` (one file per feature)

**Required imports:**

```typescript
import { HttpError } from "wasp/server";
import type {
  GetTasks,
  GetTask,
  CreateTask,
  UpdateTask,
  DeleteTask,
} from "wasp/server/operations";
import type { Task } from "wasp/entities";
```

**Import rules:**

- ✅ `wasp/server` for HttpError
- ✅ `wasp/server/operations` for type annotations
- ✅ `wasp/entities` for entity types
- ❌ NEVER use `@wasp/...` (wrong prefix)
- ❌ NEVER use `@src/...` in .ts files (use relative paths)

---

### 3. Pattern Library

#### Query Pattern: Get All (with filtering)

```typescript
/**
 * Get all tasks for authenticated user
 *
 * Features:
 * - Auth check
 * - Optional filtering
 * - Returns array
 */
export const getTasks: GetTasks<
  { status?: string }, // Args type
  Task[] // Return type
> = async (args, context) => {
  // 1. ALWAYS check auth first (MANDATORY)
  if (!context.user) throw new HttpError(401);

  // 2. Build query with optional filters
  const where: any = { userId: context.user.id };
  if (args.status) {
    where.status = args.status;
  }

  // 3. Query with context.entities (enabled by type annotation + entities in main.wasp)
  return context.entities.Task.findMany({
    where,
    orderBy: { createdAt: "desc" },
    include: {
      // Include related entities to avoid N+1 queries
      user: {
        select: { id: true, username: true },
      },
    },
  });
};
```

**Key points:**

- Type annotation `GetTasks<Args, Return>` is CRITICAL
- Without type annotation: `context.entities` is undefined!
- Auth check is FIRST line (security requirement)
- Use Prisma include for relations (avoid N+1 queries)

---

#### Query Pattern: Get Single (with permission check)

```typescript
/**
 * Get single task by ID
 *
 * Features:
 * - Auth check
 * - Resource existence check (404)
 * - Permission check (403)
 * - Returns single entity or throws
 */
export const getTask: GetTask<
  { id: string }, // Args type
  Task // Return type
> = async (args, context) => {
  // 1. Auth check
  if (!context.user) throw new HttpError(401);

  // 2. Fetch resource
  const task = await context.entities.Task.findUnique({
    where: { id: args.id },
    include: {
      user: {
        select: { id: true, username: true },
      },
    },
  });

  // 3. Check existence (404)
  if (!task) {
    throw new HttpError(404, "Task not found");
  }

  // 4. Check permission (403)
  if (task.userId !== context.user.id) {
    throw new HttpError(403, "Not authorized to access this task");
  }

  // 5. Return resource
  return task;
};
```

**Error sequence (CRITICAL):**

1. **401 Unauthorized:** No user (unauthenticated)
2. **404 Not Found:** Resource doesn't exist
3. **403 Forbidden:** User lacks permission
4. **400 Bad Request:** Invalid input

**Always check in this order!**

---

#### Action Pattern: Create (with validation)

```typescript
/**
 * Create new task
 *
 * Features:
 * - Auth check
 * - Input validation
 * - Auto-invalidates getTasks query
 * - Returns created entity
 */
export const createTask: CreateTask<
  { description: string; status?: string }, // Args type
  Task // Return type
> = async (args, context) => {
  // 1. Auth check
  if (!context.user) throw new HttpError(401);

  // 2. Validate input
  if (!args.description?.trim()) {
    throw new HttpError(400, "Description is required");
  }

  if (args.description.length > 500) {
    throw new HttpError(400, "Description must be 500 characters or less");
  }

  // 3. Create entity
  const task = await context.entities.Task.create({
    data: {
      description: args.description.trim(),
      status: args.status || "TODO",
      userId: context.user.id,
    },
  });

  // 4. Return created entity
  // Note: getTasks query auto-refetches if entities match in main.wasp
  return task;
};
```

**Auto-invalidation magic:**

- createTask has `entities: [Task]`
- getTasks has `entities: [Task]`
- When createTask completes → getTasks auto-refetches!
- No manual cache invalidation needed

---

#### Action Pattern: Update (with validation + permission)

```typescript
/**
 * Update existing task
 *
 * Features:
 * - Auth check
 * - Resource existence check
 * - Permission check
 * - Input validation
 * - Partial updates
 */
export const updateTask: UpdateTask<
  { id: string; data: { description?: string; status?: string } },
  Task
> = async (args, context) => {
  // 1. Auth check
  if (!context.user) throw new HttpError(401);

  // 2. Fetch existing resource
  const task = await context.entities.Task.findUnique({
    where: { id: args.id },
  });

  // 3. Check existence (404)
  if (!task) {
    throw new HttpError(404, "Task not found");
  }

  // 4. Check permission (403)
  if (task.userId !== context.user.id) {
    throw new HttpError(403, "Not authorized to update this task");
  }

  // 5. Validate input (if provided)
  if (args.data.description !== undefined) {
    if (!args.data.description.trim()) {
      throw new HttpError(400, "Description cannot be empty");
    }
    if (args.data.description.length > 500) {
      throw new HttpError(400, "Description must be 500 characters or less");
    }
  }

  // 6. Update entity
  const updatedTask = await context.entities.Task.update({
    where: { id: args.id },
    data: {
      ...(args.data.description && {
        description: args.data.description.trim(),
      }),
      ...(args.data.status && { status: args.data.status }),
    },
  });

  // 7. Return updated entity
  return updatedTask;
};
```

**Partial update pattern:**

- Use spread operator with conditional fields
- Validate only provided fields
- Preserve existing values if not updated

---

#### Action Pattern: Delete (with permission check)

```typescript
/**
 * Delete task
 *
 * Features:
 * - Auth check
 * - Resource existence check
 * - Permission check
 * - Returns deleted entity
 */
export const deleteTask: DeleteTask<{ id: string }, Task> = async (
  args,
  context,
) => {
  // 1. Auth check
  if (!context.user) throw new HttpError(401);

  // 2. Fetch existing resource
  const task = await context.entities.Task.findUnique({
    where: { id: args.id },
  });

  // 3. Check existence (404)
  if (!task) {
    throw new HttpError(404, "Task not found");
  }

  // 4. Check permission (403)
  if (task.userId !== context.user.id) {
    throw new HttpError(403, "Not authorized to delete this task");
  }

  // 5. Delete entity
  const deletedTask = await context.entities.Task.delete({
    where: { id: args.id },
  });

  // 6. Return deleted entity
  return deletedTask;
};
```

---

### 4. Use in Client Code

**Location:** `app/src/{feature}/components/*.tsx`

**Required imports:**

```typescript
import {
  useQuery,
  createTask,
  updateTask,
  deleteTask,
} from "wasp/client/operations";
```

**Query usage (useQuery hook):**

```typescript
function TasksPage() {
  // Use useQuery hook for queries
  const {
    data: tasks,      // Task[] | undefined
    isLoading,        // boolean
    error             // Error | undefined
  } = useQuery(getTasks, { status: 'TODO' })  // Optional args

  // Handle loading state
  if (isLoading) return <div>Loading...</div>

  // Handle error state
  if (error) return <div>Error: {error.message}</div>

  // Handle empty state
  if (!tasks || tasks.length === 0) return <div>No tasks</div>

  // Render data
  return (
    <div>
      {tasks.map((task) => (
        <TaskItem key={task.id} task={task} />
      ))}
    </div>
  )
}
```

**Action usage (direct async/await - DEFAULT):**

```typescript
function TaskForm() {
  const handleCreate = async (description: string) => {
    try {
      // ✅ CORRECT - Direct call (default approach)
      await createTask({ description, status: "TODO" });
      toast.success("Task created");
      // Wasp auto-refetches getTasks query!
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Failed to create task");
    }
  };

  const handleUpdate = async (id: string, data: any) => {
    try {
      await updateTask({ id, data });
      toast.success("Task updated");
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Failed to update task");
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await deleteTask({ id });
      toast.success("Task deleted");
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Failed to delete task");
    }
  };

  // ... rest of component
}
```

**CRITICAL: DO NOT use useAction by default!**

```typescript
// ❌ WRONG - useAction by default
const createTaskFn = useAction(createTask);
await createTaskFn(data);
// Blocks auto-invalidation, adds unnecessary complexity

// ✅ CORRECT - Direct call
await createTask(data);
// Simpler AND enables auto-invalidation
```

**ONLY use useAction for optimistic UI updates (advanced):**

```typescript
// Advanced pattern - optimistic updates
const deleteTaskFn = useAction(deleteTask, {
  optimisticUpdates: [
    {
      getQuerySpecifier: () => [getTasks],
      updateQuery: (oldTasks, { id }) => {
        return oldTasks.filter((task) => task.id !== id);
      },
    },
  ],
});

const handleOptimisticDelete = async (id: string) => {
  try {
    // UI updates immediately (optimistic)
    // Query refetches in background (actual)
    await deleteTaskFn({ id });
    toast.success("Task deleted");
  } catch (err) {
    // Optimistic update reverted if error
    toast.error("Failed to delete task");
  }
};
```

**When to use optimistic updates:**

- Critical user experience (perceived speed)
- Action highly likely to succeed
- Complex UI state needs immediate feedback

---

### 5. Restart Wasp (MANDATORY)

**After adding/modifying operations in main.wasp:**

```bash
# Stop current wasp process (Ctrl+C), then safe-start (multi-worktree safe)
../scripts/safe-start.sh
```

**Why restart is needed:**

- Type definitions regenerate only on restart
- New operation types won't be available until restart
- Changes to entities list require restart

**Common error if you forget:**

```
Cannot find module 'wasp/server/operations'
  or
Property 'Task' does not exist on type 'Context'
```

**Fix:** Stop wasp (Ctrl+C) and run `../scripts/safe-start.sh` (multi-worktree safe)

---

## Advanced Patterns

### Pattern: Complex Permission Check

```typescript
/**
 * Check if user can access resource based on multiple criteria
 */
async function canAccessTask(
  userId: string,
  taskId: string,
  context: any,
): Promise<boolean> {
  const task = await context.entities.Task.findUnique({
    where: { id: taskId },
    include: {
      project: {
        include: {
          members: true,
        },
      },
    },
  });

  if (!task) return false;

  // Owner can access
  if (task.userId === userId) return true;

  // Project members can access
  if (task.project?.members.some((m: any) => m.userId === userId)) {
    return true;
  }

  // Organization admins can access
  const userRole = await getUserOrgRole(userId, task.organizationId, context);
  if (["OWNER", "ADMIN"].includes(userRole)) return true;

  return false;
}

// Usage in operation
export const getTask: GetTask<{ id: string }, Task> = async (args, context) => {
  if (!context.user) throw new HttpError(401);

  const hasAccess = await canAccessTask(context.user.id, args.id, context);
  if (!hasAccess) throw new HttpError(403, "Not authorized");

  return context.entities.Task.findUnique({ where: { id: args.id } });
};
```

---

### Pattern: Input Validation with Zod

```typescript
import { z } from "zod";

const CreateTaskSchema = z.object({
  description: z.string().min(1, "Description required").max(500, "Too long"),
  status: z.enum(["TODO", "IN_PROGRESS", "DONE"]).optional(),
  dueDate: z.string().datetime().optional(),
});

export const createTask: CreateTask = async (args, context) => {
  if (!context.user) throw new HttpError(401);

  try {
    const validated = CreateTaskSchema.parse(args);
    return await context.entities.Task.create({
      data: { ...validated, userId: context.user.id },
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      const messages = error.errors.map(
        (e) => `${e.path.join(".")}: ${e.message}`,
      );
      throw new HttpError(400, messages.join(", "));
    }
    throw error;
  }
};
```

**Benefits:**

- Type-safe validation
- Clear error messages
- Reusable schemas
- Complex validation rules

---

### Pattern: Pagination

```typescript
export const getTasks: GetTasks<
  { page?: number; pageSize?: number },
  { tasks: Task[]; total: number; hasMore: boolean }
> = async (args, context) => {
  if (!context.user) throw new HttpError(401);

  const page = args.page || 0;
  const pageSize = args.pageSize || 20;

  const [tasks, total] = await Promise.all([
    context.entities.Task.findMany({
      where: { userId: context.user.id },
      skip: page * pageSize,
      take: pageSize,
      orderBy: { createdAt: "desc" },
    }),
    context.entities.Task.count({
      where: { userId: context.user.id },
    }),
  ]);

  return {
    tasks,
    total,
    hasMore: (page + 1) * pageSize < total,
  };
};
```

**Key points:**

- Use `skip` and `take` for pagination
- Run count query in parallel with Promise.all
- Return metadata (total, hasMore) for UI

---

### Pattern: Bulk Operations

```typescript
export const deleteMultipleTasks: DeleteMultipleTasks<
  { ids: string[] },
  { count: number }
> = async (args, context) => {
  if (!context.user) throw new HttpError(401);

  // Verify user owns all tasks
  const tasks = await context.entities.Task.findMany({
    where: { id: { in: args.ids } },
  });

  const unauthorized = tasks.filter((task) => task.userId !== context.user.id);
  if (unauthorized.length > 0) {
    throw new HttpError(403, "Not authorized to delete some tasks");
  }

  // Bulk delete
  const result = await context.entities.Task.deleteMany({
    where: {
      id: { in: args.ids },
      userId: context.user.id,
    },
  });

  return { count: result.count };
};
```

**Security note:**

- ALWAYS verify permissions for ALL items
- Use `deleteMany` only after permission check
- Return count for UI feedback

---

## Common Errors & Solutions

### Error: "Cannot find module 'wasp/...'"

**Cause:** Using wrong import prefix or forgot to restart

**Solutions:**

1. Use `wasp/...` NOT `@wasp/...`
2. Restart wasp: `../scripts/safe-start.sh` (multi-worktree safe)
3. Verify entity declared in main.wasp

```typescript
// ❌ WRONG
import { Task } from "@wasp/entities";

// ✅ CORRECT
import { Task } from "wasp/entities";
```

---

### Error: "Property 'Task' does not exist on type 'Context'"

**Cause:** Missing type annotation or entity not listed in main.wasp

**Solutions:**

1. Add type annotation: `GetTasks<Args, Return>`
2. Add entity to main.wasp: `entities: [Task]`
3. Restart wasp

```typescript
// ❌ WRONG - No type annotation
export const getTasks = async (args, context) => {
  return context.entities.Task.findMany(); // context.entities is undefined!
};

// ✅ CORRECT - With type annotation
export const getTasks: GetTasks<void, Task[]> = async (args, context) => {
  return context.entities.Task.findMany(); // Works!
};
```

---

### Error: Operation not auto-invalidating

**Cause:** Query and action have different entities lists

**Solution:** Use same entities in both

```wasp
// ❌ WRONG - Different entities
query getTasks {
  entities: [Task]
}
action createTask {
  entities: [Task, User]  // Extra entities prevent auto-invalidation
}

// ✅ CORRECT - Same entities
query getTasks {
  entities: [Task]
}
action createTask {
  entities: [Task]  // Matches query → auto-invalidation works!
}
```

---

### Error: "Not authorized" but user is logged in

**Cause:** Using wrong helper to access auth fields

**Solution:** Use Wasp helpers for email/username

```typescript
// ❌ WRONG - Direct access
if (context.user.email === 'admin@example.com') { ... }  // UNDEFINED!

// ✅ CORRECT - Use helper
import { getEmail } from 'wasp/auth'

const email = getEmail(context.user)
if (email === 'admin@example.com') { ... }  // Works!
```

---

## Critical Rules Checklist

### ✅ MUST DO:

1. **Add type annotations**

   - `GetQuery<Args, Return>`
   - `CreateAction<Args, Return>`
   - Without types: context.entities is undefined!

2. **Check auth FIRST**

   - `if (!context.user) throw new HttpError(401)`
   - First line of every operation
   - Security requirement

3. **List entities in main.wasp**

   - Required for context.entities access
   - Enables auto-invalidation between queries/actions
   - Add ALL entities accessed

4. **Use direct await for actions (default)**

   - `await createTask(data)` (simple, enables auto-invalidation)
   - NOT `useAction(createTask)` (only for optimistic UI)

5. **Restart after main.wasp changes**

   - Stop wasp (Ctrl+C)
   - Run `../scripts/safe-start.sh` (multi-worktree safe)
   - Types only regenerate on restart

6. **Follow error sequence**

   - 401: Not authenticated
   - 404: Resource not found
   - 403: Not authorized
   - 400: Bad request

7. **Avoid N+1 queries**

   - Use Prisma `include` for relations
   - Fetch related data in single query

8. **Validate input**
   - Check required fields
   - Check length constraints
   - Use Zod for complex validation

### ❌ NEVER DO:

1. **Skip type annotations**

   - Result: context.entities undefined
   - Error: Cannot access entities

2. **Skip auth check**

   - Result: Security vulnerability
   - Anyone can access operations

3. **Use useAction by default**

   - Result: Blocks auto-invalidation
   - Adds unnecessary complexity

4. **Forget to restart**

   - Result: Types not updated
   - Imports fail

5. **Use `@wasp/` prefix**

   - Correct: `wasp/entities`
   - Wrong: `@wasp/entities`

6. **Use `@src/` in .ts/.tsx files**

   - Correct: `../../utils/helper`
   - Wrong: `@src/utils/helper`

7. **Access user.email directly**

   - Correct: `getEmail(user)`
   - Wrong: `user.email` (undefined!)

8. **Mix up enum imports**
   - Types: `import type { UserRole } from 'wasp/entities'`
   - Values: `import { UserRole } from '@prisma/client'`

---

## Complete Examples Reference

See `.claude/templates/operations-patterns.ts` for copy-paste ready examples:

- **Lines 1-150:** Query patterns (get all, get single, filtered queries)
- **Lines 151-300:** Action patterns (create, update, delete)
- **Lines 301-450:** Client-side usage (useQuery, direct calls, optimistic UI)
- **Lines 451-594:** Advanced patterns (permissions, validation, pagination, bulk ops)

---

## Quick Decision Tree

```
Need to fetch data from server?
├─ YES → Create QUERY
│   1. Add query block to main.wasp
│   2. Implement with GetQuery<Args, Return> type
│   3. Use useQuery hook in client
│
└─ NO → Need to modify data?
    └─ YES → Create ACTION
        1. Add action block to main.wasp
        2. Implement with CreateAction<Args, Return> type
        3. Use direct await in client (NOT useAction)
```

---

## Summary

**This skill provides complete Wasp operations implementation guidance.**

**Key takeaways:**

1. Type annotations are CRITICAL (enables context.entities)
2. Auth check is MANDATORY first line (security)
3. Use direct await for actions (NOT useAction by default)
4. Same entities in query + action = auto-invalidation
5. Restart after main.wasp changes (types regenerate)

**When stuck:**

- Check if type annotation added
- Verify entities listed in main.wasp
- Confirm `../scripts/safe-start.sh` restarted after changes (multi-worktree safe)
- Review error sequence (401 → 404 → 403 → 400)
- Use helpers for auth fields (getEmail, getUsername)

**For complete examples:** See `.claude/templates/operations-patterns.ts`
