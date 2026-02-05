---
name: smalltalk-implementation-finder
description: Method implementation finder and analyzer for Pharo Smalltalk. Provides expertise in discovering implementors across class hierarchies (search_implementors), analyzing implementation patterns, learning coding idioms from existing implementations, assessing refactoring impact (counting implementors and references), finding duplicate code for consolidation, understanding abstract method implementations (subclassResponsibility), and tracing method overrides through inheritance chains. Use when analyzing method implementations across classes, learning implementation idioms, assessing refactoring risk before changes, finding duplicate implementations for consolidation, understanding how abstract methods are implemented in concrete classes, or tracing which classes override specific methods.
---

# Smalltalk Implementation Finder

Find and analyze method implementations across class hierarchies to understand abstract methods, implementation patterns, and assess refactoring opportunities.

## Purpose

Use this skill to:
- **Learn implementation idioms** by studying existing code
- **Assess refactoring impact** before making changes
- **Discover implementation patterns** across class hierarchies
- **Find duplicate implementations** that could be consolidated
- **Understand subclass responsibilities** for abstract methods

## Core Workflow

```
1. Find implementors → search_implementors(method_name)
2. Get source code → get_method_source(class, method)
3. Analyze patterns → Compare implementations
4. Apply learnings → Use discovered idioms in your code
```

## Primary Use Cases

### 1. Learning Implementation Idioms

**When to use**: Implementing a method for the first time and want to follow conventions.

**Quick workflow**:
```
1. search_implementors("methodName")
2. Sample 5-10 well-known classes
3. get_method_source for each
4. Identify common pattern
5. Apply to your implementation
```

**Common idioms**:
- `hash` → Combine fields with `bitXor:`
- `initialize` → Call `super initialize` first
- `=` → Check class equality, then compare fields
- `printOn:` → Use class identifier + element printing

**Example**: Learning hash implementation
```
Point>>hash → "^ x hash bitXor: y hash"
Association>>hash → "^ key hash bitXor: value hash"

Pattern: field1 hash bitXor: field2 hash
```

### 2. Assessing Refactoring Impact

**When to use**: Planning to change a method signature or refactor implementations.

**Quick workflow**:
```
1. Count implementors: search_implementors(method)
2. Count references: search_references(method)
3. Assess impact: Low (<5 impl, <20 refs) / Medium (5-20, 20-100) / High (20+, 100+)
4. Decide: Proceed / Add new method / Don't change
```

**Example**: Changing `at:put:`
```
Implementors: 50+ classes
References: 500+ call sites
Impact: VERY HIGH
Decision: Don't change. Add new method instead.
```

### 3. Finding Duplicate Code

**When to use**: Suspect multiple classes have identical implementations.

**Quick workflow**:
```
1. Find implementors in same hierarchy
2. Get source for each
3. Compare for duplicates
4. Refactor identical code to superclass
```

**Example**: Consolidating `isEmpty`
```
Array>>isEmpty → "^ self size = 0"
Set>>isEmpty → "^ self size = 0"
OrderedCollection>>isEmpty → "^ self size = 0"

Action: Pull up to Collection superclass
```

### 4. Understanding Abstract Methods

**When to use**: Encountering `self subclassResponsibility` and need to see concrete implementations.

**Quick workflow**:
```
1. Check abstract definition in superclass
2. Find all implementors
3. Study 3-5 concrete implementations
4. Understand expected behavior
```

**Example**: Understanding `Collection>>do:`
```
Collection>>do: → "self subclassResponsibility"
Array>>do: → "1 to: self size do: [:i | aBlock value: (self at: i)]"
LinkedList>>do: → "[node notNil] whileTrue: [aBlock value: node value. ...]"

Understanding: Each uses its own iteration strategy
```

### 5. Narrowing Usage Search

**When to use**: Finding references to a specific class's implementation, not all implementations.

**Quick workflow**:
```
1. Find implementors
2. Find all references
3. Filter by receiver type/context
4. Focus on relevant usage
```

**Example**: Finding `Collection>>select:` usage (not `Dictionary>>select:`)
```
Implementors: [Collection, Dictionary, Interval, ...]
References: 1000+ call sites

Filter by variable context:
  "myArray select: [...]" → Collection implementation
  "myDict select: [...]" → Dictionary implementation
```

## MCP Tools

### search_implementors
```
mcp__smalltalk-interop__search_implementors: 'methodName'
```
Returns all classes implementing the method.

### get_method_source
```
mcp__smalltalk-interop__get_method_source: class: 'ClassName' method: 'methodName'
```
Gets source code for a specific implementation.

### eval (for hierarchy exploration)
```
mcp__smalltalk-interop__eval: 'Collection allSubclasses'
```
Useful for scoping analysis to specific hierarchies.

### search_references
```
mcp__smalltalk-interop__search_references: 'methodName'
```
Finds all senders (combines well with implementor analysis).

## Quick Reference

| Goal | Tools | Pattern |
|------|-------|---------|
| Learn idiom | search_implementors → get_method_source | Sample 5-10, identify pattern |
| Assess impact | search_implementors + search_references | Count both, assess risk |
| Find duplicates | search_implementors → get_method_source | Compare, find identical |
| Narrow usage | search_implementors → search_references | Filter by receiver type |

## Best Practices

### ✅ Do

- **Scope by hierarchy**: Focus on relevant class hierarchies using `eval("ClassA allSubclasses")`
- **Sample wisely**: Choose well-known, well-implemented classes (Array, Dictionary, Point)
- **Count first**: Get overview before analyzing 500+ implementations
- **Check super**: Understand inherited behavior

### ❌ Don't

- Analyze all implementors without filtering
- Use obscure classes as examples
- Ignore superclass implementations
- Assume same method name = same behavior

## Common Workflows

### Workflow: Implement Abstract Method
```
Problem: Need to implement printOn: in new class

1. search_implementors("printOn:")
2. Filter to similar classes
3. get_method_source for 3-5 examples
4. Identify pattern
5. Apply to your class
```

### Workflow: Assess Refactoring
```
Problem: Want to change at:put: signature

1. search_implementors("at:put:") → Count implementations
2. search_references("at:put:") → Count call sites
3. Assess impact (High/Medium/Low)
4. Decide: Change / Add new / Don't change
```

### Workflow: Find Duplication
```
Problem: Suspect duplicate isEmpty implementations

1. search_implementors("isEmpty")
2. Focus on Collection hierarchy
3. get_method_source for subclasses
4. Compare for identical code
5. Refactor to superclass if identical
```

## Detailed Resources

For comprehensive analysis techniques and real-world scenarios, see:

- **[Implementation Analysis Reference](references/implementation-analysis.md)** - Detailed techniques for analyzing implementations, MCP tools reference, advanced patterns, and performance considerations
- **[Implementation Scenarios](examples/implementation-scenarios.md)** - Real-world examples including implementing abstract methods, assessing refactoring impact, finding duplicate code, learning idioms, and understanding template method patterns

## Summary

**Key principle**: Implementations across a hierarchy reveal design patterns and idioms. Use them to write better, more idiomatic code.

**Primary workflow**: Find implementors → Get source → Analyze patterns → Apply learnings

**Remember**: Always scope your analysis to relevant hierarchies and representative classes to avoid information overload.
