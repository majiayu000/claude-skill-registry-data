---
name: go-error-wrapping
description: Wrap errors with context using fmt.Errorf %w pattern
---

# Error Wrapping with %w

## Pattern
Use `fmt.Errorf` with `%w` to add context while preserving the error chain.

## CORRECT
```go
func ReadConfig(path string) (*Config, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return nil, fmt.Errorf("read config %s: %w", path, err)
    }

    var cfg Config
    if err := json.Unmarshal(data, &cfg); err != nil {
        return nil, fmt.Errorf("parse config %s: %w", path, err)
    }

    return &cfg, nil
}
```

## WRONG
```go
// Bad: Loses error chain
return nil, fmt.Errorf("read config failed: %v", err)

// Bad: No context
return nil, err

// Bad: String concatenation
return nil, errors.New("read config: " + err.Error())
```

## Key Rules
1. Use `%w` to wrap, not `%v` or `%s`
2. Add meaningful context (file names, IDs, operations)
3. Keep messages lowercase, no punctuation
4. Preserve original error for type checking

## Example Chain
```go
// Error flows up with context at each layer:
// "process user 123: read config /etc/app.conf: open /etc/app.conf: no such file or directory"

func ProcessUser(id int) error {
    cfg, err := ReadConfig("/etc/app.conf")
    if err != nil {
        return fmt.Errorf("process user %d: %w", id, err)
    }
    // use cfg...
    return nil
}
```
