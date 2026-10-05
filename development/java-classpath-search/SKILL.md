---
name: java-classpath-search
description: Use when you need to find which JAR contains a Java class, resolve import statements, identify classpath conflicts, or discover which dependency provides a class. Accepts fully qualified class names, simple class names, or partial patterns.
---

# Java Classpath Search

Fast search across all Maven dependencies to find which JARs contain a Java class.

## Overview

This skill searches a pre-built index of all classes in your Maven local repository, providing instant results for classpath queries. It's essential for resolving imports, debugging classpath conflicts, and discovering dependency sources.

## When to Use

- Finding which dependency provides a class
- Resolving "class not found" errors
- Checking for version conflicts (multiple JARs with same class)
- Discovering available implementations of an interface
- Understanding your project's dependency tree
- Verifying a dependency is in your local Maven repo

## Quick Reference

**Search patterns:**
- Fully qualified: `com.fasterxml.jackson.databind.ObjectMapper`
- Simple name: `ObjectMapper`
- Partial pattern: `jackson.ObjectMapper`

**Index location:** `$HOME/.cache/quarkusdev-skills/class-index.txt`

**Index refresh:** Automatic if missing or older than 7 days

## Implementation

### Step 1: Determine Search Pattern

Parse the user input (available as `$ARGUMENTS`):

| Input | Pattern Conversion |
|-------|-------------------|
| `com.fasterxml.jackson.databind.ObjectMapper` | `com/fasterxml/jackson/databind/ObjectMapper.class` |
| `ObjectMapper` | `/ObjectMapper.class` (any path ending with this) |
| `jackson.ObjectMapper` | `jackson/ObjectMapper.class` |

### Step 2: Ensure Index is Available

The class index is a tab-separated file mapping class paths to JAR paths.

```bash
INDEX="$HOME/.cache/quarkusdev-skills/class-index.txt"

# Check if index needs rebuilding (missing or older than 7 days)
if [ ! -f "$INDEX" ] || [ $(find "$INDEX" -mtime +7 2>/dev/null | wc -l) -gt 0 ]; then
  # Dispatch index rebuild as subagent (can take 30-60 seconds)
  # Use Agent tool with prompt:
  # "Run the build-class-index.sh script from this skill directory
  #  Report when indexing is complete."

  # Wait for subagent to complete before continuing
fi
```

**Note:** Index building is dispatched to a subagent to keep the main conversation responsive. The script uses 8 parallel workers and typically completes in under 60 seconds.

### Step 3: Search the Index

Search is instant (just grep on a text file):

**For fully qualified class name:**
```bash
grep "com/fasterxml/jackson/databind/ObjectMapper\.class" "$INDEX"
```

**For simple class name:**
```bash
grep -i "/ObjectMapper\.class" "$INDEX"
```

**For partial pattern:**
```bash
grep -i "jackson.*ObjectMapper\.class" "$INDEX"
```

### Step 4: Check Local Build Output

Also search project build directories for classes:

```bash
find . -path "*/target/classes/*ClassName.class" 2>/dev/null
```

### Step 5: Present Results

Format output to show:

1. **Class path within JAR** - The full package path
2. **JAR file path** - Highlight groupId, artifactId, version from path
3. **Maven coordinates** - Extract from JAR path:
   ```
   ~/.m2/repository/com/fasterxml/jackson/core/jackson-databind/2.15.0/jackson-databind-2.15.0.jar
   ```
   Becomes: `com.fasterxml.jackson.core:jackson-databind:2.15.0`

4. **Conflict warnings** - If multiple versions exist, flag as potential classpath issue

**Example output format:**
```
Found in 2 locations:

1. com/fasterxml/jackson/databind/ObjectMapper.class
   JAR: com.fasterxml.jackson.core:jackson-databind:2.15.0
   Path: ~/.m2/repository/com/fasterxml/jackson/core/jackson-databind/2.15.0/jackson-databind-2.15.0.jar

2. com/fasterxml/jackson/databind/ObjectMapper.class
   JAR: com.fasterxml.jackson.core:jackson-databind:2.14.2
   Path: ~/.m2/repository/com/fasterxml/jackson/core/jackson-databind/2.14.2/jackson-databind-2.14.2.jar

⚠️  WARNING: Multiple versions detected - potential classpath conflict
```

### Step 6: Handle No Results

If search returns nothing:

1. **Rebuild index** - Run the build-class-index.sh script from this skill directory
2. **Check spelling** - Suggest corrected class name
3. **Verify dependency** - Class might not be in local repo, suggest `mvn dependency:resolve`
4. **Broaden search** - Try searching for just the class name without package

## Index Details

**What's indexed:**
- All `.class` files in `~/.m2/repository/**/*.jar`
- Excludes: `-sources.jar`, `-javadoc.jar`, `-tests.jar`, `-test-*.jar`
- Excludes: Inner classes (`$`), `module-info`, `package-info`

**Index format:**
```
com/example/MyClass.class\t/path/to/artifact-1.0.0.jar
```

**Build time:** ~30-60 seconds with 8 parallel workers

**Size:** Varies by repository size (typically 5-20 MB)

## Tips

- Index is automatically refreshed every 7 days
- For inner classes, search JAR directly: `jar tf /path/to.jar | grep ClassName`
- Use `-i` flag for case-insensitive searches
- The index uses 8 parallel workers for fast building
- Subagent dispatch keeps main conversation responsive during index builds

## Supporting Tool

The index is built by `build-class-index.sh` (included in this skill directory):

```bash
#!/bin/bash
INDEX_FILE="${1:-$HOME/.cache/quarkusdev-skills/class-index.txt}"
REPO_DIR="${2:-$HOME/.m2/repository}"

find "$REPO_DIR" -name "*.jar" \
  -not -name "*-sources*" \
  -not -name "*-javadoc*" \
  -not -name "*-tests*" \
  -not -name "*-test-*" | \
  xargs -P 8 -I{} sh -c '
    jar tf "$1" 2>/dev/null | grep "\.class$" | grep -v "module-info\|package-info" | while read cls; do
      printf "%s\t%s\n" "$cls" "$1"
    done
  ' _ {} > "$INDEX_FILE"
```

## Platform Notes

This skill works with:
- **Claude Code**: Direct execution via Bash/Agent tools
- **Gemini CLI**: Use equivalent bash/file tools
- **Codex**: Use RunBash/SubAgent equivalents

The `build-class-index.sh` script is platform-independent (standard bash).
