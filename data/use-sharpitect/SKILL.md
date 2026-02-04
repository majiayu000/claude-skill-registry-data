---
name: use-sharpitect
description: Navigate and analyze C# codebases using Sharpitect's semantic tools. Use when searching for C# declarations, understanding inheritance, finding method callers/callees, or exploring code relationships in .NET projects.
allowed-tools: mcp__Sharpitect__search_declarations, mcp__Sharpitect__get_inheritance, mcp__Sharpitect__get_callers, mcp__Sharpitect__get_callees, mcp__Sharpitect__get_usages, mcp__Sharpitect__get_relationships, mcp__Sharpitect__get_dependencies, mcp__Sharpitect__get_dependents, mcp__Sharpitect__get_node, mcp__Sharpitect__get_signature, mcp__Sharpitect__get_tree, mcp__Sharpitect__get_children, mcp__Sharpitect__get_ancestors, mcp__Sharpitect__get_file_declarations, mcp__Sharpitect__list_by_kind, Read, Grep, Glob, LSP
---

# Sharpitect: Semantic C# Navigation

## Overview

Sharpitect provides semantic understanding of C# codebases through MCP tools. **Always prefer Sharpitect MCP tools over text-based searching (Grep/Glob) when working with C# code.**

## When to Use Sharpitect Tools

Use Sharpitect tools as your **first choice** for:

### Finding Declarations
- **Instead of**: `Grep` with pattern matching
- **Use**: `search_declarations` to find classes, interfaces, methods, properties by name
- **Benefits**: Exact semantic matches, understands C# syntax, filters by declaration kind

### Understanding Type Hierarchies
- **Instead of**: Reading class files and searching for base classes
- **Use**: `get_inheritance` with `direction: descendants` (implementations) or `ancestors` (base types)
- **Benefits**: Complete hierarchy tree, includes interfaces and abstract classes

### Finding Method/Property Usage
- **Instead of**: `Grep` for method names (which may match strings, comments, etc.)
- **Use**: `get_callers` to find what calls a method, or `get_usages` for all references
- **Benefits**: Accurate call sites only, no false positives from comments or strings

### Understanding Dependencies
- **Instead of**: Reading code to find what a method calls
- **Use**: `get_callees` to see all methods/properties a method uses
- **Benefits**: Complete dependency graph, includes transitive calls

### Exploring Code Structure
- **Instead of**: `Glob` to list files and `Read` to understand structure
- **Use**: `get_tree` to see containment hierarchy, `get_children` for members
- **Benefits**: Semantic structure, filtered by kind, shows relationships

### Finding Project Dependencies
- **Instead of**: Reading .csproj files or searching for using statements
- **Use**: `get_dependencies` (what a project references) or `get_dependents` (what depends on a project)
- **Benefits**: Complete project graph, includes transitive dependencies

## Tool Selection Guide

### Use Sharpitect MCP tools for:
1. **Finding C# elements**: Classes, methods, properties, interfaces
2. **Understanding relationships**: Inheritance, calls, dependencies, usages
3. **Navigating structure**: Hierarchies, containment, project organization
4. **Precise queries**: "Find all implementations of IFoo"

### Fall back to generic tools only when:
1. **Reading source code**: Use `Read` to see actual implementation
2. **Searching non-code content**: Comments, strings, XML docs, config files
3. **Cross-language search**: JavaScript, JSON, Markdown files
4. **Pattern matching**: Complex regex patterns not supported by Sharpitect

## Common Workflows

### Workflow 1: "Find implementations of an interface"
```
1. search_declarations(query="IGraphRepository", kind="interface")
2. get_inheritance(id="...", direction="descendants")
```

### Workflow 2: "Where is this method called?"
```
1. search_declarations(query="LoadGraph", kind="method")
2. get_callers(id="...", depth=1)
```

### Workflow 3: "What does this class depend on?"
```
1. search_declarations(query="SqliteGraphRepository", kind="class")
2. get_relationships(id="...", relationshipKind="uses", direction="outgoing")
```

### Workflow 4: "Show me all classes in a namespace"
```
1. search_declarations(query="Sharpitect.Analysis.Graph", kind="namespace")
2. get_children(id="...", kind="class")
```

### Workflow 5: "Find all methods that call a specific method"
```
1. search_declarations(query="SaveNode", kind="method")
2. get_usages(id="...", usageKind="call")
```

## Key Sharpitect Tools Reference

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `search_declarations` | Find declarations by name | First step for finding any C# element |
| `get_inheritance` | Get type hierarchy | Understanding class/interface relationships |
| `get_callers` | Find who calls a method | Tracing method usage upstream |
| `get_callees` | Find what a method calls | Understanding method dependencies |
| `get_usages` | Find all references | Comprehensive usage analysis |
| `get_relationships` | Get all relationships | Exploring complex relationships |
| `get_dependencies` | Project dependencies | Understanding project references |
| `get_tree` | Containment hierarchy | Exploring code structure |
| `get_signature` | Type/method signature | Getting detailed type information |
| `get_file_declarations` | Declarations in a file | Quick overview of file contents |

## Important Notes

- **Always use Sharpitect first**: Even if you think Grep might work, try Sharpitect first
- **Combine with Read**: Use Sharpitect to find locations, then `Read` to see implementation
- **Be specific with kinds**: Use `kind` parameter to filter (class, interface, method, property, etc.)
- **Use depth wisely**: For `get_callers`/`get_callees`, start with depth=1, increase if needed
- **Check the database**: If Sharpitect returns no results, the codebase may not be analyzed yet (run `sharpitect analyze`)

## Examples

### ❌ Don't do this:
```
Grep pattern="class.*IGraphRepository" to find implementations
```

### ✅ Do this instead:
```
1. search_declarations(query="IGraphRepository", kind="interface", matchMode="exact")
2. get_inheritance(id="...", direction="descendants")
```

---

### ❌ Don't do this:
```
Grep pattern="LoadGraph\\(" to find method calls
```

### ✅ Do this instead:
```
1. search_declarations(query="LoadGraph", kind="method")
2. get_callers(id="...")
```

---

### ❌ Don't do this:
```
Read all files in a namespace to understand structure
```

### ✅ Do this instead:
```
1. search_declarations(query="Sharpitect.Analysis", kind="namespace")
2. get_tree(rootId="...", maxDepth=2)
```

## Summary

**When working with C# code, think "Sharpitect first, generic tools second."** Sharpitect understands C# semantics and provides accurate, efficient navigation. Only fall back to Grep/Glob/Read when you need non-semantic searches or actual source code content.
