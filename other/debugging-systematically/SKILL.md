---
name: debugging-systematically
description: Systematic debugging methodology. Reproduce → Isolate → Hypothesize → Verify → Fix → Confirm.
type: workflow
tier: library
domains: [backend, debugging]
trigger: "debug, diagnose, trace, investigate, root cause, error, crash, unexpected behavior"
---

## The 6-Step Debugging Protocol

### Step 1: Reproduce Reliably
Before anything else, make the bug reproducible.

```bash
# Write a failing test that reproduces the bug
it('reproduces bug #123', async () => {
  // The exact scenario that causes the bug
  const result = await service.doThing(buggyInput);
  expect(result).toBe(expectedValue); // This fails currently
});
```

If you can't write a reproducible test, you don't understand the bug yet.

### Step 2: Read the Error

Read the FULL error message + stack trace. Most bugs tell you exactly where they are.

Checklist:
- What file and line number?
- What was the actual value vs expected?
- Is there an inner error wrapped in the outer one?

### Step 3: Narrow the Scope (Binary Search)

```
Full system broken?
  → Is it the database connection or the business logic?
    → Is it in the controller or the service?
      → Is it in the query or the parsing?
```

Add `console.log` / breakpoints to establish:
- What inputs enter the broken function?
- What does the function actually return?

### Step 4: Form a Hypothesis

State your hypothesis explicitly:

> "I believe the bug is caused by [X] because [evidence Y]."

Common hypotheses:
- Off-by-one error
- Async/await missing (uncaught promise)
- Null/undefined not handled
- Type coercion (== vs ===)
- Race condition
- Stale cache/state

### Step 5: Verify (Don't Fix Yet)

Prove your hypothesis is correct BEFORE fixing:
```typescript
// Add assertion to confirm hypothesis
console.assert(typeof userId === 'string', `userId is ${typeof userId}`);
```

If the hypothesis is wrong, go back to Step 3.

### Step 6: Fix and Confirm

1. Apply the minimal fix
2. Run the reproduction test — it should now pass
3. Run the full test suite — nothing should break
4. Write a regression test if one didn't exist

## Common Bug Patterns

**Async bugs:**
```typescript
// BUG: forgot await
const user = getUser(id); // returns Promise, not User
user.name; // undefined

// FIX:
const user = await getUser(id);
```

**Null propagation:**
```typescript
// BUG: assuming chain never null
const name = user.profile.address.city;

// FIX:
const name = user?.profile?.address?.city ?? 'Unknown';
```

**Race condition:**
```typescript
// BUG: two async ops on same resource
await Promise.all([updateUser(id, {a: 1}), updateUser(id, {b: 2})]);
// One update overwrites the other

// FIX: serialize or use atomic DB operation
await db.user.update({ where: {id}, data: {a: 1, b: 2} });
```

## Tools

```bash
# Node.js debugging
node --inspect src/index.js
# Then open chrome://inspect

# Print full error stack
process.on('unhandledRejection', (reason) => {
  console.error('Unhandled rejection:', reason);
});
```
