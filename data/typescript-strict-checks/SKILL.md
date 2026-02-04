---
name: typescript-strict-checks
description: Use when fixing TypeScript errors, implementing new features, or reviewing code. Ensures adherence to strict mode with noUncheckedIndexedAccess and exactOptionalPropertyTypes. Automatically applied to all TypeScript work.
allowed-tools: Read, Edit, Grep, Glob, Bash
---

# TypeScript Strict Checks Skill

## Overview

This skill enforces TypeScript strict mode compliance for the project, with special focus on `noUncheckedIndexedAccess` and `exactOptionalPropertyTypes` which cause the most common errors.

---

## Project TypeScript Configuration

**File**: `tsconfig.json`

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitAny": true,
    "noImplicitThis": true,
    "alwaysStrict": true
  }
}
```

**Key Settings That Cause Errors:**
- `noUncheckedIndexedAccess`: Array/object access returns `T | undefined`
- `exactOptionalPropertyTypes`: Optional properties must explicitly include `undefined` when set

---

## Common Error 1: noUncheckedIndexedAccess

### The Problem

Array and object index access returns `T | undefined` instead of `T`:

```typescript
const users = ['Alice', 'Bob', 'Charlie'];
const first = users[0]; // Type: string | undefined (not string!)

const obj = { name: 'Alice' };
const value = obj['name']; // Type: string | undefined
```

### Solutions

#### Solution 1: Check for undefined

```typescript
const first = users[0];
if (first === undefined) {
  logger.error('No users found');
  return;
}
// Now TypeScript knows first is string
console.log(first.toUpperCase()); // ✅ Safe
```

#### Solution 2: Optional Chaining

```typescript
// Access property safely
const name = users[0]?.toUpperCase();
// Type: string | undefined

// With nullish coalescing
const name = users[0]?.toUpperCase() ?? 'Unknown';
// Type: string
```

#### Solution 3: Non-null Assertion (Use Sparingly!)

```typescript
// Only when you're 100% certain it exists
const first = users[0]!;
// Type: string (assertion removes undefined)

// ⚠️ WARNING: Use only when you control the array and know it's non-empty
```

#### Solution 4: Array Methods (Preferred)

```typescript
// ✅ Use array methods that handle undefined
users.forEach(user => {
  // user is string, not string | undefined
  console.log(user.toUpperCase());
});

users.map(user => user.toUpperCase());

const first = users.find(u => u === 'Alice');
// Type: string | undefined (explicitly)
```

### Real Example from Codebase

```typescript
// ❌ WRONG
function getProjectStatus(projects: Project[]) {
  return projects[0].status; // Error: Object is possibly undefined
}

// ✅ CORRECT - Option 1: Guard
function getProjectStatus(projects: Project[]) {
  const first = projects[0];
  if (!first) return null;
  return first.status;
}

// ✅ CORRECT - Option 2: Optional chaining
function getProjectStatus(projects: Project[]) {
  return projects[0]?.status ?? null;
}

// ✅ CORRECT - Option 3: Array method
function getProjectStatus(projects: Project[]) {
  return projects.at(0)?.status ?? null;
}
```

---

## Common Error 2: exactOptionalPropertyTypes

### The Problem

Optional properties can't be set to `undefined` unless `undefined` is explicitly in the type:

```typescript
interface User {
  name: string;
  email?: string; // Can be omitted, but can't be set to undefined!
}

// ❌ Error: Type 'undefined' is not assignable to type 'string'
const user: User = { name: 'Alice', email: undefined };

// ✅ OK: Omit the property
const user: User = { name: 'Alice' };
```

### Solutions

#### Solution 1: Explicit undefined in Type

```typescript
interface User {
  name: string;
  email?: string | undefined; // Now can be omitted OR undefined
}

// ✅ Both work
const user1: User = { name: 'Alice' };
const user2: User = { name: 'Bob', email: undefined };
```

#### Solution 2: Omit Property Instead of Setting to undefined

```typescript
interface User {
  name: string;
  email?: string;
}

// ❌ Don't do this
const user = { name: 'Alice', email: undefined };

// ✅ Do this
const user = { name: 'Alice' };

// ✅ Or conditionally include
const user = {
  name: 'Alice',
  ...(email && { email }),
};
```

#### Solution 3: Use Required + Optional Pattern

```typescript
// Instead of optional with undefined
interface User {
  name: string;
  email: string | null; // Required but nullable
}

const user: User = { name: 'Alice', email: null }; // ✅ Clear intent
```

### Real Example from Codebase

```typescript
// ❌ WRONG
interface ProjectFormData {
  title: string;
  description?: string;
  clientId?: string;
}

function createProject(data: ProjectFormData) {
  return {
    title: data.title,
    description: data.description ?? undefined, // Error!
    clientId: data.clientId ?? undefined, // Error!
  };
}

// ✅ CORRECT - Option 1: Explicit undefined
interface ProjectFormData {
  title: string;
  description?: string | undefined;
  clientId?: string | undefined;
}

function createProject(data: ProjectFormData) {
  return {
    title: data.title,
    description: data.description ?? undefined, // ✅ OK
    clientId: data.clientId ?? undefined, // ✅ OK
  };
}

// ✅ CORRECT - Option 2: Conditional spread
interface ProjectFormData {
  title: string;
  description?: string;
  clientId?: string;
}

function createProject(data: ProjectFormData) {
  return {
    title: data.title,
    ...(data.description && { description: data.description }),
    ...(data.clientId && { clientId: data.clientId }),
  };
}

// ✅ CORRECT - Option 3: Use null
interface ProjectFormData {
  title: string;
  description: string | null;
  clientId: string | null;
}

function createProject(data: ProjectFormData) {
  return {
    title: data.title,
    description: data.description,
    clientId: data.clientId,
  };
}
```

---

## Common Error 3: Supabase Array/Object Returns

### The Problem

Supabase returns arrays from `.select()`, but with `noUncheckedIndexedAccess` you must handle potentially empty arrays:

```typescript
const { data } = await supabase
  .from('projects')
  .select('*')
  .eq('id', projectId);

// ❌ Error: data is Project[] | null, and data[0] is Project | undefined
const project = data[0];
```

### Solution: Use `.single()` for Single Records

```typescript
// ✅ CORRECT: Use .single() when expecting one record
const { data, error } = await supabase
  .from('projects')
  .select('*')
  .eq('id', projectId)
  .single(); // Returns Project | null, not Project[]

if (error || !data) {
  logger.error('Project not found', { projectId, error });
  return null;
}

// data is Project, not Project | undefined
return data;
```

### Solution: Check Array Before Access

```typescript
// When you need to use select without .single()
const { data } = await supabase
  .from('projects')
  .select('*')
  .eq('status', 'active');

if (!data || data.length === 0) {
  return [];
}

// Now safe to use data
return data.map(project => project.title);
```

---

## Common Error 4: React Query with Strict Types

### The Problem

React Query hooks return data that can be undefined during loading:

```typescript
const { data } = useQuery({
  queryKey: projectKeys.detail(projectId),
  queryFn: () => projectService.getById(projectId),
});

// ❌ Error: data is Project | undefined
return <div>{data.title}</div>;
```

### Solutions

#### Solution 1: Loading State Check

```typescript
const { data, isLoading } = useQuery({
  queryKey: projectKeys.detail(projectId),
  queryFn: () => projectService.getById(projectId),
});

if (isLoading || !data) {
  return <Spinner />;
}

// Now data is Project
return <div>{data.title}</div>;
```

#### Solution 2: Optional Chaining in JSX

```typescript
const { data } = useQuery({
  queryKey: projectKeys.detail(projectId),
  queryFn: () => projectService.getById(projectId),
});

return <div>{data?.title ?? 'Loading...'}</div>;
```

#### Solution 3: Type Guard Component

```typescript
function ProjectView({ projectId }: { projectId: string }) {
  const { data, isLoading } = useQuery({
    queryKey: projectKeys.detail(projectId),
    queryFn: () => projectService.getById(projectId),
  });

  if (isLoading) return <Spinner />;
  if (!data) return <EmptyState message="Project not found" />;

  // Data is guaranteed Project here
  return <ProjectDetails project={data} />;
}
```

---

## Key Patterns in Codebase

### Pattern 1: Query Keys Factory (as const)

**Location**: `src/features/*/services/*Keys.ts`

```typescript
// ✅ CORRECT: Use as const for strict typing
export const projectKeys = {
  all: ['projects'] as const,
  lists: () => [...projectKeys.all, 'list'] as const,
  list: (params: ProjectsQueryParams) =>
    [...projectKeys.lists(), params] as const,
  details: () => [...projectKeys.all, 'detail'] as const,
  detail: (id: string) => [...projectKeys.details(), id] as const,
} as const;

// Type is readonly, prevents accidental mutations
```

### Pattern 2: Service Method Return Types

**Location**: `src/features/*/services/*.ts`

```typescript
// ✅ CORRECT: Explicit return types
export class ProjectService {
  async getById(id: string): Promise<Project | null> {
    const { data, error } = await supabase
      .from('projects')
      .select('*')
      .eq('id', id)
      .single();

    if (error) {
      logger.error('Failed to fetch project', { id, error });
      return null;
    }

    return data; // Type: Project | null
  }

  async list(params: ProjectsQueryParams): Promise<Project[]> {
    const { data, error } = await supabase
      .from('projects')
      .select('*');

    if (error || !data) {
      logger.error('Failed to fetch projects', { error });
      return [];
    }

    return data; // Type: Project[]
  }
}
```

### Pattern 3: Zod Schemas with Strict Types

**Location**: `src/features/*/domain/*.ts`

```typescript
import { z } from 'zod';

// ✅ CORRECT: Use .nullable() or .optional() explicitly
export const projectSchema = z.object({
  id: z.string().uuid(),
  title: z.string().min(1),
  description: z.string().nullable(), // Can be null
  clientId: z.string().uuid().optional(), // Can be omitted
  status: z.enum(['draft', 'in_progress', 'review', 'done', 'archived']),
  createdAt: z.string().datetime(),
});

export type Project = z.infer<typeof projectSchema>;
// Result:
// {
//   id: string;
//   title: string;
//   description: string | null;
//   clientId?: string;
//   status: "draft" | "in_progress" | ...;
//   createdAt: string;
// }
```

---

## Testing for Compliance

### Commands

```bash
# Type check only (fast)
npm run typecheck

# Type check + build (slower, catches more issues)
npm run build

# Watch mode during development
npm run typecheck -- --watch
```

### VS Code Integration

The project has strict TypeScript checks enabled in VS Code. Errors show inline:

- Red squiggles for type errors
- Hover for detailed error messages
- Quick fixes available (Cmd/Ctrl + .)

---

## Common Fixes Checklist

When fixing TypeScript errors:

- [ ] Is it array/object access? → Add undefined check or optional chaining
- [ ] Is it optional property? → Add `| undefined` to type or use conditional spread
- [ ] Is it Supabase query? → Use `.single()` or check array length
- [ ] Is it React Query? → Add loading/undefined checks
- [ ] Is it a service method? → Explicit return type with `| null`
- [ ] Is it a Zod schema? → Use `.nullable()` or `.optional()`

---

## When to Use Non-null Assertion (!)

Use sparingly! Only when:

1. **You control the data source** and know it's non-empty
2. **Immediately after checking** in same scope:

```typescript
if (array.length > 0) {
  const first = array[0]!; // ✅ Safe, we just checked length
}
```

3. **Constants that are always defined**:

```typescript
const ADMIN_ROLE = 'admin' as const;
const roles = [ADMIN_ROLE];
const adminRole = roles[0]!; // ✅ Safe, constant array
```

**❌ DON'T use for:**
- User input
- API responses
- Database queries
- External data sources

---

## Legacy Code Exclusion

**Location**: `/src/legacy/`

The legacy directory is excluded from TypeScript compilation:

```json
// tsconfig.json
{
  "exclude": ["src/legacy/**/*"]
}
```

**Don't modify legacy code.** Migrate to new feature-based structure instead.

---

## Quick Reference

### Array Access

```typescript
// ❌ WRONG
const first = array[0];

// ✅ CORRECT
const first = array[0];
if (!first) return;

// OR
const first = array[0] ?? defaultValue;

// OR
const first = array.at(0);
```

### Optional Properties

```typescript
// ❌ WRONG
interface Props {
  value?: string;
}
const obj: Props = { value: undefined };

// ✅ CORRECT
interface Props {
  value?: string | undefined;
}
const obj: Props = { value: undefined };

// OR
interface Props {
  value?: string;
}
const obj: Props = {}; // Omit instead
```

### Supabase Queries

```typescript
// ❌ WRONG
const { data } = await supabase.from('projects').select('*').eq('id', id);
return data[0];

// ✅ CORRECT
const { data } = await supabase.from('projects').select('*').eq('id', id).single();
if (!data) return null;
return data;
```

### React Query

```typescript
// ❌ WRONG
const { data } = useQuery(...);
return <div>{data.title}</div>;

// ✅ CORRECT
const { data, isLoading } = useQuery(...);
if (isLoading || !data) return <Spinner />;
return <div>{data.title}</div>;
```

---

**Always run `npm run typecheck` before committing!**
