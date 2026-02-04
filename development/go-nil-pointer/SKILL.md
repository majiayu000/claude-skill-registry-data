---
name: go-nil-pointer
description: Pointer receiver nil safety - methods can be called on nil
---

# Pointer Receiver Nil

## Problem
Methods with pointer receivers can be called on nil. Must handle nil receiver.

## Pattern

### WRONG - Assume receiver is non-nil
```go
type Tree struct {
    Value int
    Left  *Tree
}

func (t *Tree) Sum() int {
    return t.Value + t.Left.Sum()  // PANIC if t or t.Left is nil
}
```

### CORRECT - Handle nil receiver
```go
type Tree struct {
    Value int
    Left  *Tree
    Right *Tree
}

func (t *Tree) Sum() int {
    if t == nil {
        return 0  // Nil tree has sum of 0
    }
    return t.Value + t.Left.Sum() + t.Right.Sum()
}

// Now safe to call
var tree *Tree  // nil
sum := tree.Sum()  // Returns 0, no panic
```

## Use Cases
Nil receiver pattern enables elegant recursive algorithms and optional behavior.

## Quick Fix
- [ ] Check if receiver is nil at method start
- [ ] Define sensible zero behavior for nil receiver
- [ ] Document whether methods are nil-safe

## When NOT to Use
If nil receiver doesn't make semantic sense, panic early with clear message.
