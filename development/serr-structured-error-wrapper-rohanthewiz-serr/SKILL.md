---
name: serr-structured-error-wrapper
description: "Serr allows us to enrich our Go application errors with location, etc, and bubble them up to the caller where we only have to log once"
---

# SErr - Structured Error Package for Go

SErr enriches errors with contextual attributes and metadata at each stack frame as errors bubble up to the caller. Rather than logging at every level, wrap errors with attributes throughout the call stack, then extract all accumulated context at the top level for structured logging.

## Key Philosophy

- Errors bubble up with accumulated context without logging at intermediate frames
- Attributes are added at each function call level (location, function name, custom fields)
- All metadata can be extracted in structured format for logging systems
- Supports both machine-readable attribute maps and human-readable string representations

## Import

```go
import "github.com/rohanthewiz/serr"
```

## Error Creation

### New - Create a new structured error

```go
// Basic error with message
err := serr.New("something went wrong")

// Error with key-value attributes
err := serr.New("database error", "table", "users", "operation", "insert")
```

### F - Create error with formatted message

```go
err := serr.F("failed to process item %d: %s", itemID, reason)
```

### NewSErr - Create with concrete SErr type

```go
se := serr.NewSErr("my error", "att1", "val1", "att2", "val2")
```

## Error Wrapping

### Wrap - Wrap existing error with attributes

```go
// Wrap with a message
err := serr.Wrap(dbErr, "failed to save user")

// Wrap with key-value pairs
err := serr.Wrap(dbErr, "table", "users", "user_id", userID)

// Each wrap automatically adds location and function context
```

### WrapF - Wrap with formatted message

```go
err := serr.WrapF(baseErr, "processing item %d failed with code %s", itemID, code)
```

### WrapAsSErr - Wrap returning concrete SErr

```go
se := serr.WrapAsSErr(err, "context", "additional info")
```

## Attribute Access

### Fields - Get all fields as string slice

```go
fields := se.Fields() // Returns []string{key, val, key, val, ...}
```

### FieldsMap - Get attributes as map

```go
mapFields := se.FieldsMap()
if val, ok := mapFields["user_id"]; ok {
    fmt.Println("User:", val)
}
```

### FieldsMapOfAny - Get attributes with any value types

```go
se.AppendAttributes("count", 123, "enabled", true)
mapAny := se.FieldsMapOfAny()
count := mapAny["count"].(int) // 123
```

### GetAttribute - Get single attribute value

```go
if val, ok := se.GetAttribute("key"); ok {
    // val is of type any
}
```

## Adding Attributes

### AppendKeyValPairs - Add string key-value pairs

```go
se.AppendKeyValPairs("key1", "val1", "key2", "val2")
```

### AppendAttributes - Add any type key-value pairs

```go
se.AppendAttributes("count", 42, "ratio", 3.14, "active", true)
```

## String Formatting

### StringFromErr - Get enriched string representation

```go
errStr := serr.StringFromErr(err)
// Output: base error => location[pkg/service.go:42] function[pkg.DoThing] msg[context message]
```

### FieldsAsString - Format fields as key[value] pairs

```go
str := se.FieldsAsString()
// Output: key1[val1], key2[val2], location[file.go:10], function[pkg.Func]
```

### FieldsAsCustomString - Format with custom separators

```go
str := se.FieldsAsCustomString(", ", " -> ")
// attrSep: separator between attributes
// levelSep: separator between values of duplicate keys
```

## User-Facing Messages

### SetUserMsg - Set user-displayable message with severity

```go
se.SetUserMsg("Your payment could not be processed", serr.Severity.Error)

// Available severities:
// serr.Severity.Success
// serr.Severity.Error
// serr.Severity.Warn
// serr.Severity.Info
```

### UserMsg - Get user message and severity

```go
// From SErr instance
msg, severity := se.UserMsg()

// From any error
msg, severity := serr.UserMsg(err)

// With fallback message
msg, severity := serr.UserMsgFromErr(err, "An unexpected error occurred")
```

## Unwrapping and Core Error

### GetError - Get the wrapped underlying error

```go
coreErr := se.GetError()
```

### Unwrap - Standard Go 1.13+ unwrapping

```go
unwrapped := errors.Unwrap(se)
```

## Duplicate Key Handling

When a key is repeated across wraps, values are concatenated with arrows showing the call order:

```go
se1 := serr.NewSErr("error", "status", "initial")
se2 := serr.WrapAsSErr(se1, "status", "updated")

fields := se2.FieldsMap()
// fields["status"] = "updated - initial" (newest first)
```

## Nil Error Handling

Wrap safely handles nil errors:

```go
result := serr.Wrap(nil, "some message")
// Returns nil (logs warning internally)
```

## Common Patterns

### Multi-Layer Error Wrapping

```go
// Database layer
func getUser(id string) (*User, error) {
    user, err := db.Query(...)
    if err != nil {
        return nil, serr.Wrap(err, "user_id", id, "operation", "query")
    }
    return user, nil
}

// Service layer
func processUser(id string) error {
    user, err := getUser(id)
    if err != nil {
        return serr.Wrap(err, "action", "process_user")
    }
    // ... processing
    return nil
}

// Handler layer - extract all context for logging
func handleRequest(w http.ResponseWriter, r *http.Request) {
    err := processUser(r.URL.Query().Get("id"))
    if err != nil {
        logger.LogErr(err, "Request failed")
        // All accumulated context from every layer is logged
    }
}
```

### Structured Logging Integration

```go
import "github.com/rohanthewiz/logger"

if err != nil {
    // All SErr attributes are extracted and logged
    logger.LogErr(err, "Operation failed")
}
```

### User Error Messages

```go
func handlePayment(amount float64) error {
    err := paymentService.Process(amount)
    if err != nil {
        se := serr.WrapAsSErr(err, "amount", fmt.Sprintf("%.2f", amount))
        se.SetUserMsg("Payment could not be processed. Please try again.", serr.Severity.Error)
        return se
    }
    return nil
}

// In handler
if err != nil {
    msg, sev := serr.UserMsg(err)
    sendResponse(msg, sev)
}
```

## Utility Functions

### FunctionLoc - Get file location

```go
loc := serr.FunctionLoc() // Returns "pkg/file.go:42"
```

### FunctionName - Get function name

```go
name := serr.FunctionName() // Returns "pkg.FunctionName"
```

### Clone - Copy an SErr

```go
clone := se.Clone()
```
