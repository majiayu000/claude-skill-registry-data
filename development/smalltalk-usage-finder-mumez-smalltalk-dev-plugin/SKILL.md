---
name: smalltalk-usage-finder
description: Class and method usage analyzer for Pharo Smalltalk. Provides expertise in understanding class responsibilities through class comments (get_class_comment), discovering usage patterns via references (search_references_to_class), finding example methods (exampleXXX patterns), analyzing method usage in context (search_references with polymorphism handling), generating package overviews (list_classes with comment analysis), and resolving ambiguous names (search_classes_like, search_methods_like). Use when understanding what a class does, finding usage examples for classes or methods, discovering how to use an API, analyzing package structure and purpose, resolving unclear class or method names, or learning usage patterns from real-world code.
---

# Smalltalk Usage Finder

Discover how Smalltalk classes, methods, and packages are used in practice through systematic analysis of documentation, examples, and real-world code.

## Core Analysis Workflows

### 1. Understanding Class Responsibilities

**Goal**: Discover what a class does and its intended purpose.

**Primary Tool**: `get_class_comment` - The authoritative source for class responsibility.

**Workflow**:
```
1. Verify class name (if uncertain): search_classes_like(query)
2. Get class comment: get_class_comment(class_name)
3. Present responsibility clearly
```

**Example**:
```
search_classes_like("Point")
→ ["Point", "PointArray", ...]

get_class_comment("Point")
→ "I represent an x-y pair of numbers usually designating a location on the screen."
```

**Best practice**: Always start with the class comment - it's the authoritative documentation.

### 2. Finding Class Usage Patterns

**Goal**: Learn how to use a class by examining real examples.

**Primary Tools**: `search_references_to_class`, `get_method_source`, `list_methods`

**Workflow**:
```
1. Check for example methods:
   - list_methods(package) or search_methods_like("example")
   - Filter for "exampleXXX" methods (class-side)
   - get_method_source for each example

2. Find real-world usage:
   - search_references_to_class(class_name)
   - Get source for top 5-10 references
   - Identify common patterns

3. Synthesize usage guide
```

**Example methods convention**:
- Class-side methods in `examples` category
- Named: `exampleSimple`, `example1`, `exampleWithData`
- Best source for learning how to use a class

### 3. Finding Method Usage

**Goal**: Understand how a specific method is used in context.

**Primary Tools**: `search_references`, `get_method_source`

**Challenge**: Polymorphism - same method name in multiple classes.

**Workflow**:
```
1. Verify method exists: search_methods_like(method_name)
2. Find all references: search_references(method_name)
3. Filter by context:
   - Get source for each reference
   - Look for variable naming clues (e.g., "aPoint" → Point)
   - Check type comments
4. Present usage with examples
```

**Filtering by context**:
- Variable names: `aPoint` → Point, `dict` → Dictionary
- Type hints: `"aPoint <Point>"`
- Method category: `arithmetic`, `accessing`, etc.

### 4. Generating Package Overviews

**Goal**: Understand package structure and purpose.

**Primary Tools**: `list_classes`, `get_class_comment`

**Workflow**:
```
1. List all classes: list_classes(package_name)
2. Get comments for key classes (top 10-20)
3. Identify class hierarchy and relationships
4. Find entry points (constructors, main classes)
5. Generate overview
```

**Focus on**:
- Base classes and their implementations
- Main entry points
- Common usage patterns

### 5. Handling Ambiguous Names

**Goal**: Resolve unclear or partial class/method names.

**Primary Tools**: `search_classes_like`, `search_methods_like`

**Workflow**:
```
1. Fuzzy search: search_classes_like(partial_name)
2. If multiple matches: present options to user
3. Once identified: proceed with normal workflow
```

**Example**:
```
search_classes_like("Dict")
→ ["Dictionary", "IdentityDictionary", "SmallDictionary", ...]

Present options:
"Found 3 classes:
1. Dictionary - General key-value storage
2. IdentityDictionary - Identity comparison
3. SmallDictionary - Optimized for <10 elements
Which one?"
```

## Quick Reference

### MCP Tools

**Class inspection**:
```
get_class_comment('ClassName')
get_class_source('ClassName')
```

**Method inspection**:
```
get_method_source(class: 'ClassName' method: 'methodName' is_class_method: false)
```

**Search tools**:
```
search_references_to_class('ClassName')
search_references('methodName')
search_classes_like('partial')
search_methods_like('partial')
```

**Package tools**:
```
list_classes('PackageName')
list_methods('PackageName')
```

## Best Practices

### 1. Verify Names First
Use fuzzy search when uncertain:

✅ **Good**: `search_classes_like('Dict')` → confirm → proceed
❌ **Bad**: Assume `Dict` is valid class name

### 2. Limit Search Results
Focus on top 5-10 most relevant:

✅ **Good**: Analyze top 5 references
❌ **Bad**: Try to analyze all 500 references

### 3. Prioritize Examples
Check for example methods first:

✅ **Good**: Search examples → if none, search references
❌ **Bad**: Immediately search all references

### 4. Trust Class Comments
They are authoritative documentation:

✅ **Good**: Start with `get_class_comment`
❌ **Bad**: Ignore comments, only look at code

### 5. Provide Context
Show surrounding code, not just isolated lines:

✅ **Good**: Show full method with context
❌ **Bad**: Show only the single line with method call

### 6. Handle Polymorphism
Use context clues to filter:

✅ **Good**: Check variable names, method category
❌ **Bad**: Assume first match is correct

### 7. Clarify Ambiguity
Ask user instead of guessing:

✅ **Good**: "Found 3 matches. Which one?"
❌ **Bad**: "Assuming you meant Stream..."

## Common Pitfalls

### Pitfall 1: Assuming Exact Names
**Problem**: User says "Point" but means "PointArray"
**Solution**: Always verify with `search_classes_like`

### Pitfall 2: Reference Overload
**Problem**: 500 search results overwhelming
**Solution**: Limit to top 10, filter by relevance

### Pitfall 3: Polymorphic Confusion
**Problem**: Same method in multiple classes
**Solution**: Use variable names and context to filter

### Pitfall 4: Missing Examples
**Problem**: Only checking instance-side
**Solution**: Check class-side for `exampleXXX` methods

### Pitfall 5: No Synthesis
**Problem**: Just showing raw search results
**Solution**: Analyze patterns and create usage guide

## Analysis Pattern Examples

### Example 1: Class Usage
```
User: "How do I use Point?"

1. get_class_comment('Point')
   → "I represent x-y pair..."

2. search_methods_like('example')
   → Find: "Point class>>exampleGrid"

3. get_method_source (example)
   → Shows: x@y syntax

4. search_references_to_class('Point')
   → Top usages in Rectangle, Morph

5. Synthesize:
   "Point is created with @: 100@200
    Common operations: x, y, +, -, *
    Example: center := (100@100 + 200@200) // 2"
```

### Example 2: Method Usage
```
User: "How to use distanceTo:?"

1. search_methods_like('distanceTo')
   → Multiple classes

2. search_references('distanceTo:')
   → Find usage examples

3. Filter by variable names:
   - "aPoint distanceTo:" → Point class
   - Context: geometric operations

4. get_method_source for Point version

5. Synthesize:
   "Point>>distanceTo: calculates distance
    Usage: point1 distanceTo: point2
    Returns: Float (Euclidean distance)"
```

For complete analysis techniques and detailed scenarios, see:

- **[Usage Analysis Reference](references/usage-analysis.md)** - Comprehensive analysis techniques
- **[Usage Scenarios](examples/usage-scenarios.md)** - Real-world analysis examples

## Summary

**Key workflow**: Verify → Search → Inspect → Filter → Synthesize → Present

**Analysis priorities**:
1. Start with class comments (authoritative)
2. Look for example methods (best learning resource)
3. Limit search results (top 5-10)
4. Provide context (surrounding code)
5. Synthesize findings (don't dump raw data)

**Remember**: The goal is understanding HOW to use code, not explaining implementation details.
