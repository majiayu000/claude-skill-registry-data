---
name: implementing-parallel-routes
description: Teach parallel routes and slot patterns in Next.js 16. Use when implementing parallel routes, working with @slot syntax, or encountering missing default.tsx errors.
allowed-tools: Read, Write, Edit, Glob, TodoWrite
version: 1.0.0
---

# Parallel Routes in Next.js 16

## Concept

Parallel routes allow you to simultaneously render multiple pages within the same layout. Each route is defined in a "slot" using the `@folder` naming convention.

Key characteristics:
- Slots are defined with `@` prefix (e.g., `@team`, `@analytics`)
- Each slot is passed as a prop to the parent layout
- Slots render independently and can have their own loading/error states
- Navigation within one slot doesn't affect other slots

## Basic Structure

```tree
app/
├── @team/
│   ├── page.tsx
│   └── default.tsx
├── @analytics/
│   ├── page.tsx
│   └── default.tsx
├── layout.tsx
└── page.tsx
```

The layout receives slots as props:

```typescript
export default function Layout({
  children,
  team,
  analytics,
}: {
  children: React.ReactNode
  team: React.ReactNode
  analytics: React.ReactNode
}) {
  return (
    <div>
      <div>{children}</div>
      <div className="grid grid-cols-2 gap-4">
        <div>{team}</div>
        <div>{analytics}</div>
      </div>
    </div>
  )
}
```

## default.tsx Requirement

**CRITICAL**: Every slot MUST have a `default.tsx` file.

When navigating to a route that doesn't match the current slot, Next.js will render the `default.tsx` fallback. Without it, you'll get a 404 error.

```typescript
export default function Default() {
  return null
}
```

Common error:
```
Error: The default export is not a React Component in route: /@team
```

Solution: Add `default.tsx` to every `@slot` directory.

## Navigation Behavior

Parallel routes handle navigation differently than normal routes:

### Soft Navigation
When navigating using `<Link>` or `router.push()`:
- Active slots maintain their current state
- Only the children segment updates
- Slots remain "mounted"

### Hard Navigation
When navigating via browser refresh or direct URL entry:
- All slots reset to their default state
- `default.tsx` files render for unmatched routes
- Each slot independently resolves its route

Example scenario:
```tree
app/
├── @modal/
│   ├── login/
│   │   └── page.tsx
│   └── default.tsx
├── layout.tsx
└── page.tsx
```

1. User visits `/` → `@modal` renders `default.tsx`
2. User clicks link to `/login` → `@modal` renders `login/page.tsx`
3. User refreshes page → URL changes back to `/`, `@modal` renders `default.tsx`

This is why intercepting routes typically use parallel routes for modals.

## Slot Matching

Slots match based on the current URL segment:

```tree
app/
├── dashboard/
│   ├── @sidebar/
│   │   ├── settings/
│   │   │   └── page.tsx
│   │   └── default.tsx
│   ├── settings/
│   │   └── page.tsx
│   └── layout.tsx
└── page.tsx
```

At `/dashboard/settings`:
- `dashboard/settings/page.tsx` renders in `children`
- `dashboard/@sidebar/settings/page.tsx` renders in `sidebar` slot
- If `@sidebar/settings/page.tsx` doesn't exist, `@sidebar/default.tsx` renders

## Conditional Rendering

You can conditionally render slots:

```typescript
export default function Layout({
  children,
  modal,
  auth,
}: {
  children: React.ReactNode
  modal: React.ReactNode
  auth: React.ReactNode
}) {
  const session = await getSession()

  return (
    <div>
      {children}
      {modal}
      {!session && auth}
    </div>
  )
}
```

## Common Gotchas

### 1. Missing default.tsx
**Problem**: 404 errors when navigating
**Solution**: Add `default.tsx` to every slot directory

### 2. Slot not rendering
**Problem**: Slot prop is undefined in layout
**Solution**: Check slot name matches `@folder` name (case-sensitive)

### 3. Unexpected resets
**Problem**: Slot resets to default on navigation
**Solution**: Ensure target route exists in slot, or use `default.tsx` intentionally

### 4. Nested layouts
**Problem**: Slots not accessible in nested layouts
**Solution**: Slots only pass to immediate parent layout, not descendants

### 5. Route groups with slots
**Problem**: Confusion about where to place `@slot` folders
**Solution**: Place slots at the same level as the layout that consumes them

```tree
app/
├── (marketing)/
│   ├── @hero/
│   │   └── page.tsx
│   ├── layout.tsx
│   └── page.tsx
```

## Practical Example: Modal Pattern

```tree
app/
├── @modal/
│   ├── (.)photo/
│   │   └── [id]/
│   │       └── page.tsx
│   └── default.tsx
├── photo/
│   └── [id]/
│       └── page.tsx
├── layout.tsx
└── page.tsx
```

Layout with modal slot:

```typescript
export default function Layout({
  children,
  modal,
}: {
  children: React.ReactNode
  modal: React.ReactNode
}) {
  return (
    <>
      {children}
      {modal}
    </>
  )
}
```

Modal slot default:

```typescript
export default function Default() {
  return null
}
```

Intercepted route renders in modal:

```typescript
export default function PhotoModal({ params }: { params: { id: string } }) {
  return (
    <dialog open>
      <img src={`/photos/${params.id}.jpg`} />
    </dialog>
  )
}
```

Direct route renders full page:

```typescript
export default function PhotoPage({ params }: { params: { id: string } }) {
  return (
    <main>
      <img src={`/photos/${params.id}.jpg`} />
    </main>
  )
}
```

## When to Use Parallel Routes

Good use cases:
- Dashboard layouts with independent panels
- Modal/drawer patterns with intercepting routes
- Split views with independent navigation
- A/B testing different UI sections
- Conditional sidebar/navigation rendering

Avoid when:
- Simple component composition suffices
- You need parent-child data flow
- Navigation should be tightly coupled
- You're just trying to organize files (use route groups instead)

## References

- Next.js Docs: https://nextjs.org/docs/app/building-your-application/routing/parallel-routes
- Intercepting Routes: nextjs-16 skill `ROUTING-intercepting-routes`
- Route Groups: nextjs-16 skill `ROUTING-route-groups`
