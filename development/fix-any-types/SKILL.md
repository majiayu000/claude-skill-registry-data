---
name: fix-any-types
description: >
  Remove all uses of `any` from a TypeScript file and replace them with correct,
  narrow types, inferring from usage, existing interfaces, and runtime shapes.
  Use when someone says "fix the any types", "get rid of these anys", "type this
  properly", "stop using any here", or "tighten up the types in this file".
  Prefers unknown over any when a type cannot be determined. Distinct from
  functional-typescript, which covers broader FP patterns and general type design
  -- reach for this skill specifically when `any` itself is the problem.
---

# fix-any-types

## You are a TypeScript type safety assistant. Your job is to eliminate `any` from a file by replacing each occurrence with the narrowest correct type derivable from the code — not by blindly substituting `unknown`. Every replacement must be justified by evidence from the code itself.

## Step 1 — Baseline the current type state

Before changing anything, establish the current TypeScript error baseline:

```bash
npx tsc --noEmit 2>&1 | head -50
```

If `tsc` is not in `node_modules`, try:

```bash
npx tsc --noEmit --project tsconfig.json 2>&1 | head -50
```

Record:

- how many type errors exist before your changes
- whether `strict` mode is enabled in `tsconfig.json` (read it)
- whether `noImplicitAny` is already on
- the TypeScript version (`npx tsc --version`)

The goal is to finish with the **same or fewer** type errors — never more.

---

## Step 2 — Catalogue every `any` occurrence in the file

Read the target file fully. Find every location where `any` appears, categorized by usage type:

| Category                | Examples                                                                |
| ----------------------- | ----------------------------------------------------------------------- |
| **Explicit annotation** | `const x: any`, `let items: any[]`, `data: any`                         |
| **Return type**         | `function foo(): any`, `async bar(): Promise<any>`                      |
| **Parameter type**      | `function handle(event: any)`, `(err: any) => {}`                       |
| **Generic argument**    | `Promise<any>`, `Array<any>`, `Map<string, any>`, `Record<string, any>` |
| **Type cast**           | `x as any`, `<any>x`                                                    |
| **Implicit any**        | unannotated parameters in non-strict mode, `catch (e)` in older TS      |
| **Re-exported any**     | types imported from an external module that are typed as `any`          |

Also flag adjacent patterns that defeat the type system without literally using `any`:

- `@ts-ignore` and `@ts-expect-error` suppressing real type errors (not legitimate suppressions)
- `object` used as a catch-all value type
- `Function` as a type (loses parameter and return types)
- `{}` as a catch-all (catches non-null/undefined values — often a mistake)

Build a numbered list: **N occurrences found across M categories**.

---

## Step 3 — Resolve the correct type for each occurrence

For each `any` occurrence, derive the correct replacement by investigating the code:

### 3a — Look at how the value is used (usage-driven inference)

Read all sites where the variable or parameter is accessed after being declared as `any`:

- which properties are accessed on it? → those become the required fields of an interface
- which methods are called on it? → narrows it to a type that has those methods
- is it passed to another function? → check that function's parameter type
- is it returned from the function? → check what the caller expects

Example:

```typescript
// Before: any
function processUser(user: any) {
  console.log(user.id, user.email, user.createdAt);
}

// After: derive from property access
function processUser(user: { id: string; email: string; createdAt: Date }) {
```

### 3b — Look at what is assigned to it (assignment-driven inference)

Read all sites where the variable is assigned a value:

- if a literal object is assigned, extract its shape
- if a function return value is assigned, look up that function's return type
- if a fetched API response is assigned, look for a corresponding DTO or response type

### 3c — Check for existing types that already describe this shape

Search the codebase for interfaces, type aliases, or Zod/class-validator schemas that match the inferred shape:

```
grep for "interface User", "type User", "class User", Prisma-generated types, etc.
```

Reuse an existing type if it matches — do not create a duplicate.

### 3d — Check for generic opportunities

If a function works with the same shape regardless of the specific type, introduce a generic instead of a concrete type:

```typescript
// Before
function getFirst(arr: any[]): any {
  return arr[0];
}

// After
function getFirst<T>(arr: T[]): T {
  return arr[0];
}
```

### 3e — Use `unknown` only when the type genuinely cannot be determined

`unknown` is the correct choice when:

- the value comes from an external system with no schema (raw JSON parse result, `localStorage.getItem`)
- the value is a `catch (e)` clause (TS 4.0+ default for `useUnknownInCatchVariables`)
- the function is explicitly designed to accept anything (a serializer, a logger)

When using `unknown`, always add a type guard or assertion before the value is used:

```typescript
// Before
function log(value: any) {
  console.log(value.toString());
}

// After
function log(value: unknown) {
  console.log(String(value));
}
```

---

## Step 4 — Identify types that need to be defined

For each inferred shape that does not already exist in the codebase, decide where to define it:

- **Co-located type**: define in the same file if it is only used there
- **Shared type file**: move to `src/types/`, `src/shared/types.ts`, or equivalent if it is used across multiple files — check where similar types live first
- **Existing type augmentation**: if the shape is a subset of an existing interface, use `Pick<T, 'field1' | 'field2'>` or `Partial<T>` rather than defining a new interface

Prefer:

- `interface` for object shapes that will be extended or implemented
- `type` for unions, intersections, mapped types, and aliases
- `Pick`, `Omit`, `Partial`, `Required`, `ReturnType`, `Parameters` utility types where they avoid duplication

---

## Step 5 — Apply changes in a safe order

Make changes in this order to avoid cascading errors:

1. **Define new shared types first** — before referencing them in the target file
2. **Fix explicit annotations** — these are the lowest risk; just replacing the annotation
3. **Fix parameter types** — may require updating callers if the new type is more restrictive
4. **Fix return types** — may require updating the function body to match
5. **Remove type casts** (`as any`) — often requires the most investigation; the cast was hiding a real incompatibility
6. **Fix generic arguments** — replace `Promise<any>` with `Promise<SpecificType>`, etc.

After each logical group of changes, run:

```bash
npx tsc --noEmit 2>&1
```

If a change introduces new errors, address them before moving on. Do not accumulate broken state.

---

## Step 6 — Handle `as any` casts carefully

`as any` casts are the most dangerous occurrence — they actively suppress the type checker. Each one is hiding a real incompatibility that must be resolved rather than silenced.

For each `as any` cast:

1. Remove the cast and read the resulting type error
2. Determine whether the incompatibility is in the source type, the target type, or both
3. Fix the underlying incompatibility rather than replacing `as any` with `as unknown as TargetType`

Acceptable reasons to keep a cast (replace `as any` with a narrower cast and comment explaining why):

- Interoperating with a poorly typed third-party library
- A runtime invariant that TypeScript cannot express (document this with a comment)

Never replace `as any` with `as unknown as T` without understanding why the types don't match.

---

## Step 7 — Verify the final state

After all changes:

```bash
npx tsc --noEmit 2>&1
git diff <target-file>
```

Confirm:

- zero new type errors introduced (existing errors may remain if they predate this change)
- no `any` occurrences remain (run `grep -n ": any\|as any\|<any>" <file>`)
- no `@ts-ignore` comments were added to suppress errors created by this refactor
- the behavior of the code is unchanged — no logic was modified, only type annotations

---

## Step 8 — Report the changes

```text
TypeScript any removal: <filename>
──────────────────────────────────────────────────

Occurrences found: N
  Explicit annotations:  N
  Parameter types:       N
  Return types:          N
  Generic arguments:     N
  Type casts (as any):   N

Types defined or reused:
  NEW  src/types/order.ts — OrderSummary (used in 2 places)
  REUSE src/users/user.entity.ts — User (already existed)
  UTILITY Pick<Product, 'id' | 'name'> (inline, no new file needed)

Replacements made: N
  <variable/function>  any → <new type>    (reason: inferred from property access)
  <variable/function>  any → unknown       (reason: raw JSON parse result, guarded before use)
  <variable/function>  any[] → Order[]     (reason: matches existing Order interface)

Remaining any (if any):
  line 42: as any — kept: third-party lib EventEmitter has no typed overload for this event

Type errors before: N  |  Type errors after: N
──────────────────────────────────────────────────
```
