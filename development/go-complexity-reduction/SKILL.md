---
name: Go Complexity Reduction
description: This skill should be used when the user asks about "gocyclo", "funlen", "cyclop", "nestif", "cognitive complexity", "refactor long function", "reduce nesting", "complexity reduction", or needs guidance on simplifying complex Go code. Provides patterns and techniques for reducing Go code complexity while preserving behavior.
---

# Go Complexity Reduction

Patterns and techniques for reducing cognitive complexity in Go code while preserving exact behavior.

## Overview

Complexity linters measure how hard code is to understand and maintain:

| Linter | Measures | Threshold |
|--------|----------|-----------|
| **gocyclo** | Cyclomatic complexity (decision points) | >15 warning, >20 error |
| **funlen** | Function length in lines | >60 lines |
| **cyclop** | Package-level complexity | varies |
| **nestif** | Nesting depth | >4 levels |
| **maintidx** | Maintainability index | <20 |

## Core Principle

**Boring, obvious code > clever, compact code**

When refactoring:
- Preserve exact input/output behavior
- Keep side effects in the same order
- Don't change error messages
- Make existing tests pass unchanged

## Pattern 1: Guard Clauses

Replace nested conditions with early returns.

### Before
```go
func process(data *Data) error {
    if data != nil {
        if data.Valid() {
            if data.Ready() {
                return doWork(data)
            }
        }
    }
    return errors.New("cannot process")
}
```

### After
```go
func process(data *Data) error {
    if data == nil {
        return errors.New("nil data")
    }
    if !data.Valid() {
        return errors.New("invalid data")
    }
    if !data.Ready() {
        return errors.New("data not ready")
    }
    return doWork(data)
}
```

**Impact:** nestif 3→0, gocyclo reduced

## Pattern 2: Extract Switch Cases

Move switch case logic to dedicated handlers.

### Before
```go
func handle(op string, ctx context.Context, req *Request) (*Response, error) {
    switch op {
    case "create":
        // 20 lines of create logic
        validate(req)
        prepare(req)
        result := create(ctx, req)
        return result, nil
    case "update":
        // 15 lines of update logic
        ...
    case "delete":
        // 10 lines of delete logic
        ...
    }
}
```

### After
```go
func handle(op string, ctx context.Context, req *Request) (*Response, error) {
    switch op {
    case "create":
        return handleCreate(ctx, req)
    case "update":
        return handleUpdate(ctx, req)
    case "delete":
        return handleDelete(ctx, req)
    default:
        return nil, fmt.Errorf("unknown op: %s", op)
    }
}

func handleCreate(ctx context.Context, req *Request) (*Response, error) {
    // Focused, testable function
}
```

**Impact:** cyclop reduced, each handler independently testable

## Pattern 3: Extract Loop Bodies

Keep loops simple, move complex logic to helpers.

### Before
```go
func processAll(items []Item) error {
    for _, item := range items {
        // 30 lines of processing
        if err := validate(item); err != nil {
            log.Error(err)
            continue
        }
        transformed := transform(item)
        if err := save(transformed); err != nil {
            return err
        }
        notify(transformed)
    }
    return nil
}
```

### After
```go
func processAll(items []Item) error {
    for _, item := range items {
        if err := processItem(item); err != nil {
            return errors.Wrapf(err, "item %s", item.ID)
        }
    }
    return nil
}

func processItem(item Item) error {
    if err := validate(item); err != nil {
        log.Error(err)
        return nil // skip invalid items
    }
    transformed := transform(item)
    if err := save(transformed); err != nil {
        return err
    }
    notify(transformed)
    return nil
}
```

**Impact:** Linear main loop, testable processing

## Pattern 4: Replace Boolean Soup

Extract complex conditionals to named functions.

### Before
```go
if (a && b) || (c && !d) || (e && f && !g) {
    doSomething()
}
```

### After
```go
if shouldProcess(a, b, c, d, e, f, g) {
    doSomething()
}

// shouldProcess returns true when the processing conditions are met.
// Returns true if:
// - Both a and b are set, OR
// - c is set and d is not, OR
// - e and f are set and g is not
func shouldProcess(a, b, c, d, e, f, g bool) bool {
    return (a && b) || (c && !d) || (e && f && !g)
}
```

**Impact:** Main code readable, logic testable

## Pattern 5: Lookup Tables

Replace conditional chains with data structures.

### Before
```go
func getConfig(format string, version int, env string) Config {
    if format == "json" && version >= 2 && env == "prod" {
        return prodJSONConfig
    }
    if format == "json" && version >= 2 && env == "dev" {
        return devJSONConfig
    }
    if format == "xml" && env == "prod" {
        return prodXMLConfig
    }
    // ... more conditions
    return defaultConfig
}
```

### After
```go
type configKey struct {
    format  string
    version int
    env     string
}

var configs = map[configKey]Config{
    {"json", 2, "prod"}: prodJSONConfig,
    {"json", 2, "dev"}:  devJSONConfig,
    {"xml", 0, "prod"}:  prodXMLConfig,
}

func getConfig(format string, version int, env string) Config {
    if cfg, ok := configs[configKey{format, version, env}]; ok {
        return cfg
    }
    return defaultConfig
}
```

**Impact:** Data-driven, trivially testable, easy to extend

## Pattern 6: Split Responsibilities

One function should do one thing.

### Before
```go
func LoadAndProcess(path string) (*Result, error) {
    // Read file
    data, err := os.ReadFile(path)
    if err != nil { return nil, err }

    // Parse
    var config Config
    if err := json.Unmarshal(data, &config); err != nil {
        return nil, err
    }

    // Validate
    if config.Name == "" { return nil, errors.New("missing name") }
    if config.Port < 0 { return nil, errors.New("invalid port") }

    // Transform
    result := &Result{...}
    // 20 lines of transformation

    return result, nil
}
```

### After
```go
func LoadAndProcess(path string) (*Result, error) {
    config, err := loadConfig(path)
    if err != nil { return nil, err }

    if err := validateConfig(config); err != nil {
        return nil, err
    }

    return transformConfig(config), nil
}

func loadConfig(path string) (*Config, error) { ... }
func validateConfig(c *Config) error { ... }
func transformConfig(c *Config) *Result { ... }
```

**Impact:** Each function single-purpose, testable

## Helper Function Rules

When extracting helpers:

1. **Pure functions** - No I/O, no mutations, no side effects
2. **Explicit dependencies** - Pass everything needed as parameters
3. **Keep unexported** - Unless reuse is needed elsewhere
4. **Descriptive names** - `validateUserInput` not `validate`

## Quality Targets

| Level | Complexity Reduction | Helpers | Nesting |
|-------|---------------------|---------|---------|
| Good | ≥30% | 2-5 | Reduced |
| Excellent | ≥50% | Each <20 lines | Zero in main fn |

## Verification

After refactoring:

```bash
# Tests must pass
go test -race ./...

# Lints must be clean
golangci-lint run --enable gocyclo,funlen,nestif ./...
```
