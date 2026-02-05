---
name: go-functional-options
description: Use the Functional Option Pattern for configurable Go constructors. Applies to types needing multiple optional parameters with validation and defaults. Includes Go 1.25 generics support.
---

# Go Functional Options Pattern

Use the Functional Option Pattern for configurable constructors in Go code. This pattern is recommended for any type that requires configuration with multiple optional parameters.

## Go Version

Use Go 1.25 or later for generics support.

## Pattern Structure

### 1. Define Option Function Type

```go
type option func(*targetStruct) error
```

The option type is always:
- A function that takes a pointer to your struct
- Returns an error for validation failures
- Use lowercase `option` as the type name

### 2. Constructor with Variadic Options

```go
func NewThing(opts ...option) (*thing, error) {
    t := &thing{
        // Set sensible defaults first
        input:  os.Stdin,
        output: os.Stdout,
    }
    for _, opt := range opts {
        err := opt(t)
        if err != nil {
            return nil, err
        }
    }
    return t, nil
}
```

Key points:
- Accept `opts ...option` as variadic parameter
- Initialize struct with sensible defaults before applying options
- Apply options in order, checking for errors
- Return both the struct pointer and error

### 3. Option Factory Functions

```go
func WithInput(input io.Reader) option {
    return func(t *thing) error {
        if input == nil {
            return errors.New("nil input reader")
        }
        t.input = input
        return nil
    }
}

func WithOutput(output io.Writer) option {
    return func(t *thing) error {
        if output == nil {
            return errors.New("nil output writer")
        }
        t.output = output
        return nil
    }
}

func WithConfigFromArgs(args []string) option {
    return func(t *thing) error {
        if len(args) < 1 {
            return nil // Empty args is not an error
        }
        // Process args...
        return nil
    }
}
```

Naming conventions:
- Use `WithXxx()` for option factory functions
- Use `WithXxxFromArgs()` when parsing from command-line arguments
- Return the closure that performs the actual configuration
- Always validate inputs and return errors for invalid configuration
- Allow empty/nil inputs when appropriate (return nil error)

### 4. Simple Closure Pattern (No Error Returns)

When options are simple value assignments (enums, modes, flags) that cannot fail, use `type Option func(*config)` without error returns. The constructor handles validation after all options are applied. See [EXAMPLES.md](EXAMPLES.md) for the netkit configuration example.

## Usage Examples

### Basic Usage

```go
c, err := NewCounter(
    WithInput(inputBuf),
)
if err != nil {
    return err
}
```

### Multiple Options

```go
m, err := NewMatcher(
    WithInput(strings.NewReader(data)),
    WithOutput(outputBuf),
    WithSearchTextFromArgs(os.Args[1:]),
)
if err != nil {
    fmt.Fprintln(os.Stderr, err)
    os.Exit(1)
}
```

### With Command-Line Args

```go
func Main() {
    c, err := NewCounter(
        WithInputFromArgs(os.Args[1:]),
    )
    if err != nil {
        fmt.Fprintln(os.Stderr, err)
        os.Exit(1)
    }
    fmt.Println(c.Lines())
}
```

## When to Use This Pattern

Use functional options when:
- Creating types that need configuration with multiple optional parameters
- You want to provide sensible defaults
- Configuration may fail and needs validation
- You want to keep the API flexible for future additions
- Users should be able to compose configuration options

Don't use when:
- Only one or two required parameters (use regular function parameters)
- No configuration needed (simple constructors are fine)
- The type is too simple to warrant the pattern

## Testing Functional Options

### Test Individual Options

```go
func TestWithInput_ErrorsOnNilInput(t *testing.T) {
    t.Parallel()
    _, err := NewCounter(
        WithInput(nil),
    )
    if err == nil {
        t.Fatal("want error on nil input, got nil")
    }
}
```

### Test Option Combinations

```go
func TestWithInputFromArgs_IgnoresEmptyArgs(t *testing.T) {
    t.Parallel()
    inputBuf := bytes.NewBufferString("1\n2\n3")
    c, err := NewCounter(
        WithInput(inputBuf),
        WithInputFromArgs([]string{}),
    )
    if err != nil {
        t.Fatal(err)
    }
    // Verify the earlier option (WithInput) is still active
    want := 3
    got := c.Lines()
    if want != got {
        t.Errorf("want %d, got %d", want, got)
    }
}
```

### Test Option Ordering

Options are applied in order, so later options can override earlier ones:

```go
func TestOptionsApplyInOrder(t *testing.T) {
    t.Parallel()
    buf1 := bytes.NewBufferString("first")
    buf2 := bytes.NewBufferString("second")
    c, err := NewCounter(
        WithInput(buf1),
        WithInput(buf2), // This should override buf1
    )
    if err != nil {
        t.Fatal(err)
    }
    // Test should verify buf2 is used
}
```

## Alternative Pattern: Interface-Based Options (Uber Style)

Uber's Go Style Guide recommends an interface-based approach for libraries and public APIs. This alternative provides additional testability and debuggability benefits compared to closures.

### Interface-Based Implementation

```go
// package db

type options struct {
    cache  bool
    logger *zap.Logger
}

type Option interface {
    apply(*options)
}

type cacheOption bool

func (c cacheOption) apply(opts *options) {
    opts.cache = bool(c)
}

func WithCache(c bool) Option {
    return cacheOption(c)
}

type loggerOption struct {
    Log *zap.Logger
}

func (l loggerOption) apply(opts *options) {
    opts.logger = l.Log
}

func WithLogger(log *zap.Logger) Option {
    return loggerOption{Log: log}
}

// Open creates a connection.
func Open(addr string, opts ...Option) (*Connection, error) {
    options := options{
        cache:  defaultCache,
        logger: zap.NewNop(),
    }

    for _, o := range opts {
        o.apply(&options)
    }

    // Use options.cache and options.logger
    // ...
}
```

### Usage

```go
db.Open(addr)
db.Open(addr, db.WithLogger(log))
db.Open(addr, db.WithCache(false))
db.Open(addr, db.WithCache(true), db.WithLogger(log))
```

**Advantages:** Testable (options comparable), debuggable (can implement `fmt.Stringer`), flexible (additional interfaces), type-safe

**Disadvantages:** More verbose, no built-in error handling, more boilerplate

See [EXAMPLES.md](EXAMPLES.md) for a complete database connection example using this pattern.

## Choosing Between Closure and Interface Approaches

### Use Closure-Based When:

- Building **application code** with straightforward configuration needs
- **Error handling** during option application is important
- Working with **dynamic validation** (e.g., opening files, network checks)
- Prioritizing **simplicity and readability**
- Building CLI tools or internal services

See [EXAMPLES.md](EXAMPLES.md) for complete closure-based examples (line counter, text matcher).

### Use Interface-Based (Uber Pattern) When:

- Building **reusable libraries** for external consumption
- Options need to be **comparable** in tests
- **Debugging option application** is critical
- Options should implement **additional interfaces** (like `fmt.Stringer`)
- Building public APIs expected to expand
- Error handling can be done **before** option creation

### Error Handling Tradeoff

**Closure approach:**
```go
func WithInput(input io.Reader) option {
    return func(c *counter) error {
        if input == nil {
            return errors.New("nil input reader")
        }
        c.input = input
        return nil  // Error returned during application
    }
}
```

**Interface approach:**
```go
func WithCache(c bool) Option {
    return cacheOption(c)  // No error possible
}
```

The closure approach allows validation to fail during option application, useful for opening files, validating complex input, or performing I/O operations. The interface approach requires validation before calling the option factory or in the constructor after all options are applied.

### Testing Differences

**Closure-Based Testing** (test behavior):
```go
func TestWithInput_ErrorsOnNilInput(t *testing.T) {
    t.Parallel()
    _, err := NewCounter(WithInput(nil))
    if err == nil {
        t.Fatal("want error on nil input, got nil")
    }
}
```

**Interface-Based Testing** (can compare options):
```go
func TestCacheOptions(t *testing.T) {
    t.Parallel()
    opt1 := db.WithCache(true)
    opt2 := db.WithCache(true)
    // Interface-based options are comparable
    if opt1 != opt2 {
        t.Error("expected equal options")
    }
}

func TestCacheOptionString(t *testing.T) {
    t.Parallel()
    opt := db.WithCache(true)
    // Can implement fmt.Stringer for debugging
    got := opt.String()
    want := "WithCache(true)"
    if got != want {
        t.Errorf("got %q, want %q", got, want)
    }
}
```

## Go 1.25 Features

Go 1.25 introduces generics with type parameters, which can enhance the Functional Options Pattern in some scenarios:

### Generic Option Functions

For libraries that need to support multiple similar types, you can create generic option factories:

```go
// Generic option type for any config struct
type Option[T any] func(*T) error

// Generic setter that works with any comparable type
func WithValue[T any, V comparable](setter func(*T, V), value V) Option[T] {
    return func(cfg *T) error {
        setter(cfg, value)
        return nil
    }
}
```

### When to Use Generics with Options

Use generics sparingly with functional options:
- **Do use** when creating reusable option utilities across multiple types
- **Don't use** for simple, single-type configuration (adds unnecessary complexity)
- **Consider** for libraries where the same option pattern applies to multiple config types

For most application code, the non-generic pattern (as shown above) is simpler and more maintainable.

## Generic Interface-Based Options (Advanced)

For maximum reusability, combine Uber's interface pattern with Go 1.25 generics to create option utilities that work across multiple configuration types.

### Benefits

- **Type-safe reuse**: Same option utilities work with different config types
- **Maintains testability**: Options are still comparable (unlike generic closures)
- **Option composition**: Build reusable option libraries
- **Better type inference**: Go can infer types from context

### Generic Option Interface

```go
package options

import (
    "fmt"
    "time"
)

// Option is a generic interface for any config type T
type Option[T any] interface {
    apply(*T)
    fmt.Stringer  // Options can be debugged
}

// timeoutOption works with any config type
type timeoutOption[T any] struct {
    duration time.Duration
    setter   func(*T, time.Duration)
}

func (t timeoutOption[T]) apply(cfg *T) {
    t.setter(cfg, t.duration)
}

func (t timeoutOption[T]) String() string {
    return fmt.Sprintf("WithTimeout(%v)", t.duration)
}

// WithTimeout creates a timeout option for any config type
func WithTimeout[T any](
    d time.Duration,
    setter func(*T, time.Duration),
) Option[T] {
    return timeoutOption[T]{duration: d, setter: setter}
}
```

### Usage Across Multiple Types

```go
type DBConfig struct {
    ConnTimeout time.Duration
    MaxConns    int
}

type HTTPConfig struct {
    ReadTimeout time.Duration
    MaxRequests int
}

// Same option utility works with both types
dbOpts := []Option[DBConfig]{
    WithTimeout(5*time.Second, func(c *DBConfig, d time.Duration) {
        c.ConnTimeout = d
    }),
}

httpOpts := []Option[HTTPConfig]{
    WithTimeout(10*time.Second, func(c *HTTPConfig, d time.Duration) {
        c.ReadTimeout = d
    }),
}
```

### When to Use

**Use generic interface-based options when:**
- Creating reusable option utility libraries
- Same option pattern applies to multiple config types
- Type safety AND testability are both critical
- Building framework or infrastructure code

**Don't use when:**
- Working with a single configuration type (non-generic is simpler)
- Application-level code (closure-based is more practical)
- Error handling during option application is needed

See [EXAMPLES.md](EXAMPLES.md) for a complete implementation of generic interface-based options.

## Complete Working Examples

For complete, production-ready code examples demonstrating all approaches, see **[EXAMPLES.md](EXAMPLES.md)**, which includes:

- **Closure-based examples**: Line counter and text matcher with error handling
- **Interface-based example**: Database connection (Uber style)
- **Generic interface example**: Reusable option utilities across multiple types

The examples show:
- Full implementations with imports and error handling
- Usage patterns and testing strategies
- Explanations of when to use each approach
- Real-world CLI tool and library code
