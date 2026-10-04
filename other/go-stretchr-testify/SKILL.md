---
name: go-stretchr-testify
description: "Best practices for using stretchr/testify. Covers assertions, requirements, mocks, and test suites."
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 06 May 2026 06:30:00 GMT
---

## Assert vs Require

Testify provides two main packages for checking results:

- **`assert`**: Records a failure but allows the test to continue. Use this for verifying multiple independent conditions.
- **`require`**: Records a failure and stops the test immediately (`t.FailNow()`). Use this for preconditions where continuing would cause a panic (e.g., checking if a pointer is nil before dereferencing it).

```go
func TestUser(t *testing.T) {
    user, err := GetUser("123")
    require.NoError(t, err) // Stop here if error exists
    require.NotNil(t, user) // Stop here if user is nil
    
    assert.Equal(t, "John", user.Name) // Continue even if name is wrong
    assert.Equal(t, 30, user.Age)
}
```

## Common Assertions

| Assertion | Purpose |
| --- | --- |
| `Equal(expected, actual)` | Deep equality check. |
| `NoError(err)` | Fails if `err != nil`. |
| `ErrorIs(err, target)` | Checks if `err` matches `target` using `errors.Is`. |
| `Nil(obj)` / `NotNil(obj)` | Checks for nil. |
| `Contains(s, sub)` | Checks if slice/string/map contains a value/key. |
| `ElementsMatch(a, b)` | Checks if two slices have same elements, ignoring order. |
| `Eventually(fn, timeout, poll)` | Wait for an async condition to become true. |

**Important**: Always put the **expected** value first: `assert.Equal(t, expected, actual)`. Swapping them makes the failure diff confusing.

## Mocking with `testify/mock`

Mocks allow you to isolate the unit under test by simulating its dependencies.

```go
type MockRepo struct {
    mock.Mock
}

func (m *MockRepo) Get(id string) (*User, error) {
    args := m.Called(id)
    return args.Get(0).(*User), args.Error(1)
}

func TestService(t *testing.T) {
    mockRepo := new(MockRepo)
    mockRepo.On("Get", "123").Return(&User{Name: "John"}, nil)
    
    // ... call your service ...
    
    mockRepo.AssertExpectations(t) // Verify all expectations were met
}
```

## Test Suites

Suites group tests and provide lifecycle hooks (`SetupTest`, `TearDownTest`, etc.).

```go
type MySuite struct {
    suite.Suite
    db *DB
}

func (s *MySuite) SetupSuite() {
    s.db = ConnectDB()
}

func (s *MySuite) TestSomething() {
    s.Equal(1, 1)
}

func TestRunSuite(t *testing.T) {
    suite.Run(t, new(MySuite))
}
```

## Anti-patterns

- ❌ **Swapping Expected/Actual** — Leads to "Expected: actual, Got: expected" error messages.
- ❌ **Using `assert` for `nil` checks** — If `user` is nil, `user.Name` will panic after an `assert.NotNil` failure. Use `require.NotNil` instead.
- ❌ **Forgetting `AssertExpectations`** — Mocks will "pass" even if expected methods were never called.
- ❌ **Over-mocking** — Don't mock types from your own package unless necessary for isolation; prefer using real implementations when possible.
- ❌ **Mixing `assert` and `require` randomly** — Be consistent about what constitutes a fatal vs. non-fatal failure.
