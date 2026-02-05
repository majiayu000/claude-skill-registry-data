---
name: ousterhout-principles
description: "Apply Ousterhout's software design principles: detect shallow modules, information leakage, and complexity red flags. Use when reviewing code, designing modules, refactoring, or discussing architecture."
allowed-tools:
  - Read
  - Grep
  - Glob
---

# Ousterhout's Software Design Principles

Quick checks for applying John Ousterhout's "A Philosophy of Software Design" principles. Managing complexity is the primary challenge in software engineering.

## Core Formula

**Module Value = Functionality - Interface Complexity**

The best modules are **deep**: simple interfaces hiding powerful implementations.

## 1. Deep vs Shallow Module Check

### Classic Deep Module Example
**Unix I/O**: Four simple operations (open, read, write, close) hide massive complexity (buffering, disk management, filesystem, drivers, caching).

### Assessment Questions

**Functionality Assessment:**
- How much does this module actually do?
- What complexity does it hide from callers?
- Could I significantly change implementation without breaking callers?

**Interface Assessment:**
- How many public methods/functions?
- How many parameters do they require?
- How much must callers know to use it correctly?

**The Feel Test:**
- Interface complexity ≈ implementation complexity? → **Shallow** (eliminate or deepen)
- Simple interface, powerful implementation? → **Deep** (good!)
- Just wrapping another module? → **Shallow** (probably unnecessary abstraction)

### Warning Signs

❌ **Shallow Module Indicators:**
- Wrapper class exposing most wrapped methods
- Pass-through functions adding no semantic value
- Abstraction hiding little complexity
- Thin layer that could be eliminated
- Interface almost as complex as implementation

✅ **Deep Module Indicators:**
- Simple interface (few methods, clear parameters)
- Powerful functionality (does a lot)
- Hides design decisions
- Changing internals doesn't break callers
- Worth the abstraction cost

## 2. Information Leakage Check

### Core Test
**"If I change implementation details, do callers break?"**

If YES → You have information leakage.

### Common Leakage Patterns

**Database Schema Leakage:**
```
❌ BAD: Return raw database rows/arrays
   - Callers depend on column order
   - Schema changes break calling code
   - Implementation (SQL) leaks through interface

✅ GOOD: Return domain objects
   - Hide schema behind types
   - Callers use named properties
   - Schema refactoring transparent to callers
```

**Internal Data Structure Leakage:**
```
❌ BAD: Expose internal buffer/cache structure
   - Callers know about your storage choices
   - Can't change data structures freely
   - Implementation details in public API

✅ GOOD: Provide abstract query interface
   - Hide how data is stored
   - Expose "what" not "how"
   - Free to optimize internals
```

**Implementation Detail Leakage:**
```
❌ BAD: Configuration forcing caller knowledge
   - Expose internal IDs, indices, ordering
   - Require callers to know implementation
   - Changes ripple to all callers

✅ GOOD: Domain-centric interface
   - Use domain language
   - Hide technical implementation
   - Stable despite internal changes
```

### Encapsulation Check

Ask yourself:
- Can I refactor internals without breaking callers?
- Do callers know about my implementation choices?
- Does my interface reveal "how" or just "what"?
- Would changing my data structure break callers?

**Principle**: Each module should hide design decisions from others.

## 3. Red Flag Scanner

### Critical Red Flags (Avoid)

**Generic Names:**
- `Manager`, `Util`, `Helper` → Vague, non-specific
- `Service`, `Handler`, `Processor` → Sometimes justified, often lazy
- `Base`, `Abstract` → Prefix anti-patterns

**Ask**: Does name reveal **what** it does? Or just **that** it does something?

**Temporal Decomposition:**
- `step1()`, `step2()`, `step3()`
- `phase1()`, `phase2()`
- `initialize()`, `process()`, `finalize()`

**Problem**: Organized by **WHEN** executed, not **WHAT** they do.

**Better**: Organize by functionality. Name by purpose, not sequence.

### Warning Signs

**Pass-Through Methods:**
- Method just delegates to another class
- Adds no transformation or logic
- No semantic value
- Just indirection for indirection's sake

**Configuration Overload:**
- Too many parameters/options
- Every implementation detail exposed
- Interface complexity ≈ implementation
- Callers must understand internals

### Context-Aware Exceptions

Some generic names have domain justification:
- `EventManager` in event-driven system → Acceptable
- But `EventBus` or `EventDispatcher` still better (more specific)

**Principle**: Prefer specific domain terms over generic technical terms.

### Quick Scan Questions

When reviewing a module:
1. Does name reveal what it does (not just that it exists)?
2. Is it organized by execution order (temporal anti-pattern)?
3. Does it just wrap another module without adding value?
4. Could I give it a more specific, intention-revealing name?
5. Does it have too many configuration options?

## Application Workflow

**When designing:**
1. Check module depth (value = functionality - interface complexity)
2. Ensure information hiding (callers isolated from implementation)
3. Avoid red flag names (be specific, avoid generic terms)

**When reviewing:**
1. Scan for Manager/Util/Helper (red flags)
2. Test: "If implementation changes, do callers break?" (leakage)
3. Assess: Simple interface + powerful implementation? (depth)

**When refactoring:**
1. Identify shallow modules → Consider eliminating or deepening
2. Find information leakage → Add encapsulation
3. Replace generic names → Use domain-specific terms

## Key Principles Summary

1. **Deep Modules**: Simple interfaces hiding powerful implementations
2. **Information Hiding**: Each module hides design decisions from others
3. **Avoid Complexity**: Fight generic names, temporal decomposition, pass-through methods

**Remember**: Complexity is anything that makes software hard to understand or modify. Fight it with every decision.
