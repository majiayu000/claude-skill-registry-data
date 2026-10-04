---
name: test-patterns
description: Reference for writing tests that actually protect against regressions — deep assertions over spies, table-driven tests, fixture hygiene, AAA structure. Use when writing, reviewing, or refactoring tests.
---

# Test patterns

A test's job is to fail when the behavior is wrong. Most mediocre tests pass whether the code is right or not.

## Rules of thumb

### Assert behavior, not implementation

Bad:
```js
expect(spy).toHaveBeenCalled()
```
Good:
```js
expect(response.body.status).toBe('completed')
expect(db.getUser(id).lastSeenAt).toBe(mockNow)
```

Spy-assertions fail on refactor and protect nothing. Behavior-assertions fail when the user-visible contract breaks.

### One logical check per test

Many `expect` lines can add up to one assertion of one outcome — that's fine. What's not fine: one test that covers three unrelated behaviors so nobody can tell what broke when it fails.

### Arrange-Act-Assert

```js
it('rejects stale tokens', () => {
  // Arrange
  const token = signToken({ exp: yesterday() })
  // Act
  const result = verify(token)
  // Assert
  expect(result.ok).toBe(false)
  expect(result.reason).toBe('expired')
})
```

### Table-driven when the shape repeats

```js
test.each([
  ['empty',       '',         'required'],
  ['too short',   'ab',       'min_length'],
  ['has space',   'a b',      'invalid_char'],
  ['ok',          'alice',    null],
])('validateUsername(%s=%j)', (_, input, expected) => {
  expect(validateUsername(input).error).toBe(expected)
})
```

### Fixtures > inline setup

If three tests set up the same `validUser`, extract it. If the setup is 20 lines, it's probably doing too much — mock less, use a real test DB.

### Name tests as specs

The test name is a sentence the reader can understand without opening the code. `it('rejects stale tokens')` > `it('test2')`.

### Integration > unit for risk hotspots

Unit tests are great for pure logic. For "this endpoint returns the right data for this user" you want an integration test that hits a real database, a real router, and a real serializer. Mocks hide the bugs you actually ship.

## Framework-specific pointers

### Testing Library (React/Vue/Svelte)
- Query by role/label first, `getByTestId` last.
- `userEvent` over `fireEvent`.
- Avoid testing props/state; test what the user sees.

### Pytest
- Use fixtures for setup, not class-level `setUp`.
- `parametrize` for table tests.
- `-k` and markers to target — CI can split suites.

### Go
- Table tests with subtests: `t.Run(tt.name, func(t *testing.T) { ... })`.
- `t.Cleanup` over `defer` for teardown.

### Jest/Vitest
- `describe.each` + `test.each` for tables.
- Avoid `toHaveBeenCalled` when you can check the effect instead.
