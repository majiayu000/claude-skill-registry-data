---
name: go-nil-interface
description: Interface nil trap - typed nil is not nil
---

# Interface Nil Trap

## Problem
A typed nil pointer stored in an interface is NOT nil.

## Pattern

### WRONG - Typed nil escapes
```go
func GetUser(id int) error {
    var err *MyError  // typed nil
    if id < 0 {
        err = &MyError{"invalid id"}
    }
    return err  // Returns non-nil interface containing nil pointer!
}

if err := GetUser(1); err != nil {
    // This branch RUNS even though no error occurred
    fmt.Println("error:", err)
}
```

### CORRECT - Return untyped nil
```go
func GetUser(id int) error {
    if id < 0 {
        return &MyError{"invalid id"}
    }
    return nil  // Return untyped nil
}

if err := GetUser(1); err != nil {
    // This branch does NOT run
    fmt.Println("error:", err)
}
```

## Why It Happens
Interface contains (type, value). Typed nil has (type=*MyError, value=nil).
This is different from (type=nil, value=nil).

## Quick Fix
- [ ] Return nil directly, not typed nil variable
- [ ] Or return concrete type, not interface
