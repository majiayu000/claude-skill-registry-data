---
name: java-api-discovery
description: Discover Java API signatures from compiled JARs using javap instead of guessing or relying on incomplete documentation. Use when encountering unknown methods, pagination patterns, union types, or compilation errors from incorrect API assumptions.
---

# Java API Discovery

Efficiently discover actual API signatures from compiled JARs using `javap`. This approach eliminates guessing and trial-and-error by examining the compiled bytecode directly.

## When to Use This Skill

- Encountering compilation errors from incorrect method assumptions
- Working with unfamiliar Java SDKs or libraries
- Need to understand pagination patterns (offset vs cursor)
- Dealing with union types or polymorphic responses
- Verifying field existence before writing code
- Documentation is incomplete, outdated, or ambiguous

## Core Workflow

### 1. Find the JAR

```bash
# Gradle projects
find ~/.gradle/caches -name "*library-name*.jar" -type f 2>/dev/null | head -5

# Maven projects
find ~/.m2/repository -name "*library-name*.jar" -type f 2>/dev/null | head -5

# Project libs
find . -name "*.jar" -type f 2>/dev/null
```

### 2. List Package Contents

```bash
# List all classes in a package
jar tf /path/to/library.jar | grep "com/example/package" | head -20

# Find specific class
jar tf /path/to/library.jar | grep -i "ClassName"
```

### 3. Examine Class API

```bash
# Show all public methods
javap -cp /path/to/library.jar com.example.ClassName

# Filter for getters
javap -cp /path/to/library.jar com.example.ClassName | grep -E "public.*get"

# Filter for setters/builders
javap -cp /path/to/library.jar com.example.ClassName | grep -E "public.*(set|with|build)"

# Show full signatures including generics
javap -s -cp /path/to/library.jar com.example.ClassName
```

### 4. Verify Before Coding

**Before writing any API call:**
1. Find the exact method name with javap
2. Check return type (especially for collections: `List` vs `Set`)
3. Verify parameter types
4. Look for builder patterns vs constructors

## Common Patterns to Discover

### Pagination
```bash
# Check for pagination methods
javap -cp /path/to/jar com.example.ApiClient | grep -iE "(page|offset|cursor|limit)"
```

**Common patterns:**
- Offset-based: `pageOffset(Long)`, `pageLimit(Long)`
- Cursor-based: `pageCursor(String)`, `nextCursor()`
- Token-based: `pageToken(String)`, `nextPageToken()`

### Union Types
```bash
# Look for getActualInstance pattern
javap -cp /path/to/jar com.example.Response | grep -E "(getActualInstance|instanceof)"
```

**Handling union types:**
```java
Object actual = response.getActualInstance();
if (actual instanceof TypeA) {
    TypeA typed = (TypeA) actual;
}
```

### Builder vs Constructor
```bash
# Check construction options
javap -cp /path/to/jar com.example.Model | grep -E "(public.*\(|builder|Builder)"
```

### Enum Constants
```bash
# List enum values
javap -cp /path/to/jar com.example.TokenType | grep -E "public static final"
```

## Quick Reference

| Need | Command |
|------|---------|
| Find JAR | `find ~/.gradle/caches -name "*name*.jar"` |
| List classes | `jar tf file.jar \| grep package` |
| All methods | `javap -cp file.jar com.Class` |
| Getters only | `javap ... \| grep "get"` |
| With generics | `javap -s -cp file.jar com.Class` |

## Common Pitfalls

- ❌ **Guessing method names** → Always verify with javap
- ❌ **Assuming collection types** → Check if `List`, `Set`, or `Collection`
- ❌ **Trusting old documentation** → Bytecode is truth
- ❌ **Ignoring return types** → Union types need `getActualInstance()`

## Progressive Context

- For helper scripts: see `scripts/discover-api.sh`
- For detailed patterns: see `reference.md`