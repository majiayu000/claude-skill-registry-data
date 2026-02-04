---
name: critical-rules
description: Use always - non-negotiable rules for TypeScript safety, socket events, and React patterns
---

# Critical Rules

**MANDATORY rules that must NEVER be violated.** These prevent common bugs and ensure code quality.

## Checklist

### Rule 1: TypeScript Type Safety

- [ ] **NEVER use `any` type** - no exceptions, including tests
  - ❌ `const data: any = response`
  - ✅ `const data: unknown = response`
  - ✅ `const data = response as UserData`
  - ✅ For test mocks: `as unknown as Type`

**Why:** `any` disables all type checking and hides bugs. Use proper types, `unknown`, or type assertions instead.

**Examples:**

```typescript
// ❌ Bad - loses all type safety
function process(data: any) {
  return data.user.name // No error if user is undefined!
}

// ✅ Good - proper typing
function process(data: unknown) {
  if (isUserData(data)) {
    return data.user.name
  }
  throw new Error('Invalid data')
}

// ✅ Good - type assertion when you know the type
const mockSocket = {
  on: vi.fn(),
  emit: vi.fn()
} as unknown as Socket
```

### Rule 2: Socket Event Handling

- [ ] **NEVER use `socket.on()` directly in components**
  - ❌ `socket.on('event', callback)` - Breaks on reconnection
  - ✅ `useSocketEvent('event', callback, [callback])` - Reactive and safe

**Why:** Direct `socket.on()` doesn't re-subscribe when socket reconnects. Use the `useSocketEvent` hook which handles reconnection automatically.

**Examples:**

```typescript
// ❌ Bad - loses events after reconnection
useEffect(() => {
  const socket = useSocket.getState().socket
  socket?.on(SocketEvents.DOWNLOAD_START, handleDownload)
}, [])

// ✅ Good - handles reconnection automatically
useSocketEvent(SocketEvents.DOWNLOAD_START, handleDownload, [handleDownload])
```

### Rule 3: useEffect Cleanup

- [ ] **Cleanup functions must be synchronous**
  - ❌ `return async () => { await cleanup() }` - Breaks React
  - ✅ `return () => { cleanup().catch(console.error) }` - Fire-and-forget

**Why:** React expects cleanup functions to be synchronous. Async cleanup functions are ignored.

**Examples:**

```typescript
// ❌ Bad - async cleanup is ignored
useEffect(() => {
  startService()
  return async () => {
    await stopService() // Never runs!
  }
}, [])

// ✅ Good - synchronous cleanup with fire-and-forget async
useEffect(() => {
  startService()
  return () => {
    stopService().catch(console.error)
  }
}, [])

// ✅ Good - synchronous cleanup only
useEffect(() => {
  const interval = setInterval(poll, 1000)
  return () => clearInterval(interval)
}, [])
```

### Rule 4: Test Behavior, Not Implementation

- [ ] **Test what the code does, not how it does it**
  - ❌ Testing that `socket.on` was called 3 times
  - ✅ Testing that component responds correctly to events

**Why:** Implementation details change frequently. Behavior tests remain stable and catch real bugs.

**Examples:**

```typescript
// ❌ Bad - tests implementation
it('should call socket.on with download event', () => {
  render(<Component />)
  expect(mockSocket.on).toHaveBeenCalledWith(SocketEvents.DOWNLOAD_START, expect.any(Function))
})

// ✅ Good - tests behavior
it('should show download progress when download starts', () => {
  render(<Component />)

  act(() => {
    handlers[SocketEvents.DOWNLOAD_START]({ id: '123', filename: 'model.bin' })
  })

  expect(screen.getByText('Downloading model.bin')).toBeInTheDocument()
})
```

## Verification

Before committing code, verify these rules are followed:

- [ ] Run `pnpm run type-check` - catches `any` types
- [ ] Search for `socket.on` - should only appear in `useSocketEvent` hook
- [ ] Review useEffect cleanup - must be synchronous
- [ ] Review tests - focus on behavior, not implementation

## Consequences

**Violating these rules leads to:**

- Type safety violations → Runtime errors in production
- Socket event loss → Features stop working after reconnect
- Broken cleanup → Memory leaks and stale subscriptions
- Brittle tests → False failures during refactoring
