---
name: java-decompile
description: Use when you need to view the source code of a Java class from project dependencies, understand a library's API implementation, find method signatures, or explore how a dependency works internally. Accepts fully qualified or simple class names.
---

# Java Class Decompiler

Decompile and view the source code for Java classes from project dependencies.

## Overview

This skill decompiles Java classes from Maven dependencies using Vineflower (a modern Java decompiler) via jbang, allowing you to inspect library internals, understand API implementations, and find method signatures without leaving your workflow.

## When to Use

- Need to understand how a library method is implemented
- Looking for exact method signatures or parameter types
- Exploring the internals of a dependency
- Debugging issues related to third-party libraries
- Finding which overloads are available for a class

## Quick Reference

**Input formats:**
- Fully qualified: `com.fasterxml.jackson.databind.ObjectMapper`
- Simple name: `ObjectMapper` (will search for matches)

**Tools used:**
- Vineflower decompiler (via jbang)
- Maven classpath
- Fallback: javap for bytecode disassembly

**Requirements:**
- jbang installed (https://www.jbang.dev/)

## Implementation

### Step 1: Determine the Class Name

Parse the user's input (available as `$ARGUMENTS` in command context):
- If it contains dots (`.`), treat as fully qualified name
- If it's a simple name, you'll need to search for it first

### Step 2: Find the JAR Containing the Class

Convert class name to file path: replace `.` with `/`, append `.class`

**Option A: Use Maven classpath file (fast for first search)**
```bash
# Build classpath file if missing
if [ ! -f /tmp/quarkus-classpath.txt ]; then
  mvn dependency:build-classpath -Dmdep.outputFile=/tmp/quarkus-classpath.txt -q 2>/dev/null
fi

# Search for the class in classpath JARs
CLASSPATH=$(cat /tmp/quarkus-classpath.txt)
```

**Option B: Search Maven local repository directly**
```bash
find ~/.m2/repository -name "*.jar" | while read jar; do
  if jar tf "$jar" 2>/dev/null | grep -q "com/example/ClassName.class"; then
    echo "$jar"
    break
  fi
done
```

**Option C: Check local build output** (for project classes)
```bash
find . -path "*/target/classes/com/example/ClassName.class" 2>/dev/null
```

### Step 3: Decompile the Class

**Primary method: Vineflower via jbang**

Vineflower works on JAR files, so extract the specific class or decompile the entire JAR:

```bash
# Option A: Decompile specific class from JAR
# Create temp directory for output
TEMP_DIR=$(mktemp -d)

# Decompile the JAR containing the class
jbang org.vineflower:vineflower:RELEASE "/path/to/the.jar" "$TEMP_DIR"

# Find and display the decompiled class
find "$TEMP_DIR" -name "ClassName.java" -exec cat {} \;

# Cleanup
rm -rf "$TEMP_DIR"
```

```bash
# Option B: For single class extraction (faster)
# Extract the class file first
CLASS_FILE="com/example/ClassName.class"
jar xf "/path/to/the.jar" "$CLASS_FILE"

# Decompile just that class
TEMP_DIR=$(mktemp -d)
jbang org.vineflower:vineflower:RELEASE "$CLASS_FILE" "$TEMP_DIR"
cat "$TEMP_DIR/com/example/ClassName.java"

# Cleanup
rm -rf "$CLASS_FILE" "$TEMP_DIR"
```

**Fallback method: javap** (if jbang/Vineflower unavailable)
```bash
javap -p -c -cp "/path/to/the.jar" "fully.qualified.ClassName"
```

**Note:** jbang automatically downloads and caches Vineflower on first use.

### Step 4: Present Decompiled Source

Show the decompiled code with syntax highlighting. Highlight key elements:
- Public API methods and their signatures
- Constructor parameters
- Important fields
- Annotations
- Package and imports

### Step 5: Handle Multiple Matches

If the user provided a simple class name and multiple matches exist:
1. List all matching classes with their packages
2. Show which JAR each comes from
3. Ask which one to decompile

## Common Patterns

**Searching within a specific JAR:**
```bash
jar tf /path/to/some.jar | grep -i ClassName
```

**Finding all classes with a name pattern:**
```bash
# Use the class-index if available
grep -i "ClassName" "$HOME/.cache/quarkusdev-skills/class-index.txt"
```

## Tips

- Quarkus internal classes may be in `target/classes/` rather than `.m2`
- Vineflower produces more readable output than javap
- jbang automatically manages Vineflower versions and dependencies
- Use `-p` flag with javap to show private members
- For inner classes, include the `$` in the class name
- Vineflower decompiles entire JARs - for single classes, extract first for faster results

## Platform Notes

This skill works with:
- **Claude Code**: Direct execution
- **Gemini CLI**: Use equivalent file/bash tools
- **Codex**: Use RunBash/ReadFile equivalents

Tool scripts are platform-independent (bash/python).
