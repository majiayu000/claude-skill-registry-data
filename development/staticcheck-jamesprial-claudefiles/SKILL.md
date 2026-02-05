---
name: staticcheck
description: Fix staticcheck issues
---

# staticcheck

Advanced static analyzer with comprehensive checks.

## Install
```bash
go install honnef.co/go/tools/cmd/staticcheck@latest
```

## Usage
```bash
staticcheck ./...
staticcheck -checks=all ./...
```

## Common Issues

### SA1019: Deprecated Function
```go
// Bad
ioutil.ReadFile("file.txt")

// Good
os.ReadFile("file.txt")
```

### SA4006: Unused Value
```go
// Bad
value := compute()
value = other()

// Good
_ = compute()
value := other()
```

### SA9003: Empty Branch
```go
// Bad
if err != nil {
    // TODO
}

// Good - remove or implement
if err != nil {
    return err
}
```

### S1002: Simplify Condition
```go
// Bad
if x == true {
    return true
}

// Good
return x
```

### ST1003: Naming Convention
```go
// Bad
func GetHTTPSUrl() string

// Good
func GetHTTPSURL() string
```

### SA1006: Printf on os.Stderr
```go
// Bad
fmt.Printf("error: %v\n", err)

// Good
fmt.Fprintf(os.Stderr, "error: %v\n", err)
```

### SA4010: Result Not Used
```go
// Bad
append(slice, item)

// Good
slice = append(slice, item)
```

## Configuration
```ini
# .staticcheck.conf
checks = ["all", "-ST1000"]
```
