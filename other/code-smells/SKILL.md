---
name: code-smells
description: Classic code quality indicators — function length, naming, duplication, nesting, magic values, dead code, and React-specific smells. Adapted from Clean Code and Airbnb style guide.
---

# Code Smells Review

## Quick Reference — Top 15 Code Smells

1. [ ] **Function >50 lines** — should be decomposed
2. [ ] **File >300 lines** — should be split into modules
3. [ ] **>3 parameters** on a function — use an options object
4. [ ] **Nesting >3 levels deep** — use early returns or extract functions
5. [ ] **Magic numbers/strings** — hardcoded values without named constants
6. [ ] **Duplicated code blocks** — same 5+ lines in multiple places
7. [ ] **Boolean parameters** — `doThing(true, false, true)` is unreadable
8. [ ] **Dead code** — unreachable branches, unused variables, commented-out blocks
9. [ ] **Inconsistent naming** — mixing camelCase and snake_case
10. [ ] **Comments explaining WHAT** — code should be self-documenting (WHY comments are good)
11. [ ] **Long ternary chains** in JSX — use early returns or a lookup object
12. [ ] **useEffect doing too much** — split into focused effects
13. [ ] **Component >5 props** — consider composition or compound components
14. [ ] **Array index as key** — `key={i}` causes bugs on reorder
15. [ ] **Inline styles mixed with Tailwind** — pick one approach

---

## Function-Level Smells

### Functions Over 50 Lines
A function doing 50+ things is doing too many things. Split by responsibility.

**Exception:** React components that are essentially just JSX layout can be longer, but the *logic* portion should still be <50 lines. If a component has 30 lines of hooks/logic + 100 lines of JSX, the logic portion needs review.

### Too Many Parameters
```ts
// ❌ Unreadable — what do these booleans mean?
createUser('John', 'john@test.com', true, false, 'admin', 1000)

// ✅ Self-documenting with options object
createUser({
  name: 'John',
  email: 'john@test.com',
  verified: true,
  newsletter: false,
  role: 'admin',
  creditLimit: 1000
})
```

### Deep Nesting (>3 levels)
```ts
// ❌ Arrow of doom
function processOrder(order) {
  if (order) {
    if (order.items.length > 0) {
      if (order.payment) {
        if (order.payment.verified) {
          // finally doing the actual work, 4 levels deep
        }
      }
    }
  }
}

// ✅ Guard clauses / early returns
function processOrder(order) {
  if (!order) return { error: 'No order' }
  if (order.items.length === 0) return { error: 'Empty order' }
  if (!order.payment) return { error: 'No payment' }
  if (!order.payment.verified) return { error: 'Unverified payment' }
  
  // Actual work at top level — clean and readable
}
```

### Magic Numbers and Strings
```ts
// ❌ What is 86400000? What is 'active'?
if (Date.now() - user.lastLogin > 86400000) {
  await updateStatus(user.id, 'active')
}

// ✅ Named constants
const ONE_DAY_MS = 24 * 60 * 60 * 1000
const UserStatus = { ACTIVE: 'active', INACTIVE: 'inactive' } as const

if (Date.now() - user.lastLogin > ONE_DAY_MS) {
  await updateStatus(user.id, UserStatus.ACTIVE)
}
```

### Boolean Parameters
```ts
// ❌ What does `true` mean here?
fetchUsers(true, false)

// ✅ Named options
fetchUsers({ includeInactive: true, withOrders: false })
```

---

## React-Specific Smells

### Long Ternary Chains in JSX
```tsx
// ❌ Deeply nested ternaries — impossible to read
return (
  <div>
    {loading ? (
      <Spinner />
    ) : error ? (
      <Error message={error} />
    ) : data.length === 0 ? (
      <Empty />
    ) : (
      <DataTable data={data} />
    )}
  </div>
)

// ✅ Early returns — each state is clear
if (loading) return <Spinner />
if (error) return <Error message={error} />
if (data.length === 0) return <Empty />
return <DataTable data={data} />
```

### useEffect Doing Too Much
```tsx
// ❌ One effect doing 3 unrelated things
useEffect(() => {
  fetchUser()
  setupWebSocket()
  trackPageView()
}, [])

// ✅ Separate concerns — each can have proper cleanup
useEffect(() => { fetchUser() }, [userId])
useEffect(() => {
  const ws = setupWebSocket()
  return () => ws.close()
}, [])
useEffect(() => { trackPageView() }, [pathname])
```

### Component Props Explosion
```tsx
// ❌ Too many props — hard to use, hard to maintain
<UserCard
  name={user.name}
  email={user.email}
  avatar={user.avatar}
  role={user.role}
  lastLogin={user.lastLogin}
  isOnline={user.isOnline}
  onEdit={handleEdit}
  onDelete={handleDelete}
  showActions={true}
/>

// ✅ Pass the whole object + compose
<UserCard user={user} onEdit={handleEdit} onDelete={handleDelete} />

// Or use compound components for complex cases
<UserCard user={user}>
  <UserCard.Actions>
    <EditButton onClick={handleEdit} />
    <DeleteButton onClick={handleDelete} />
  </UserCard.Actions>
</UserCard>
```

### Array Index as Key
```tsx
// ❌ Causes bugs when items are reordered, deleted, or inserted
{items.map((item, i) => <ListItem key={i} {...item} />)}

// ✅ Stable unique identifier
{items.map(item => <ListItem key={item.id} {...item} />)}
```
**Why it matters:** React uses keys to determine which elements changed. When using index as key and an item is deleted from the middle, React re-renders all subsequent items unnecessarily and may preserve wrong state.

---

## When NOT to Flag

- **Prototypes/MVPs:** Don't demand perfection on throwaway code. Flag only P0 issues.
- **Generated code:** Don't review auto-generated types, migration SQL, or config for style.
- **Test files:** Slightly verbose code in tests is acceptable for readability. Don't flag test files for function length or naming conventions.
- **Configuration files:** `next.config.ts`, `tailwind.config.ts`, etc. are inherently messy.
- **One-time scripts:** Migration scripts, seed scripts — focus on correctness, not elegance.

---

## Naming Conventions (from Airbnb guide)

| Element | Convention | Example |
|---------|-----------|---------|
| Variables, functions | camelCase | `getUserById`, `isActive` |
| Components | PascalCase | `UserCard`, `DashboardPage` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRIES`, `API_BASE_URL` |
| Types/Interfaces | PascalCase | `UserProfile`, `ApiResponse` |
| Files (components) | PascalCase or kebab-case | `UserCard.tsx` or `user-card.tsx` |
| Files (utilities) | camelCase or kebab-case | `formatDate.ts` or `format-date.ts` |
| Database columns | snake_case | `created_at`, `user_id` |
| Environment variables | UPPER_SNAKE_CASE | `NEXT_PUBLIC_API_URL` |

**Flag:** Mixing conventions within the same codebase (camelCase variables alongside snake_case variables).

## Sources
- Clean Code JavaScript (Ryan McDermott) — adapted from Robert C. Martin
- Airbnb JavaScript Style Guide
- React documentation on composition vs inheritance
- Next.js App Router patterns

## Changelog
- 2026-03-21: Initial skill — code smells for code review
