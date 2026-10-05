---
name: quarkus-module-build
description: Use when asked to build, compile, or rebuild specific Quarkus modules. Accepts multiple module names and builds them in parallel via subagents. Examples - build graphql module, compile openapi and rest, rebuild security extensions.
---

# Quarkus Module Build

Build one or more specific modules in a Quarkus project with parallel execution.

## Overview

This skill builds specific Quarkus modules (extensions, libraries, etc.) in parallel using subagents. It's optimized for rapid iteration during development when you only need to rebuild changed modules rather than the entire project.

## When to Use

- Building specific modules after local changes
- Compiling a subset of extensions for testing
- Rebuilding modules after dependency updates
- Quick iteration during feature development
- After resolving compilation errors in specific modules

**When NOT to use:**
- For full project builds (use `quarkus-full-build` instead)
- For running tests (use `mvn test` directly)
- For single commands (just run `mvn` directly)

## Quick Reference

**Input format:** Module names separated by spaces or "and"
- `/module-build graphql and openapi`
- `/module-build security`
- `build the graphql rest and mongodb modules`

**Build command per module:**
```bash
cd <module-path> && mvn clean install -DskipTests
```

**Execution:** Parallel via subagents (all modules build simultaneously)

## Implementation

### Step 1: Parse Module Names

Extract module names from user input (available as `$ARGUMENTS`):

```bash
# Split on spaces and "and"
echo "graphql and openapi rest" | tr ' ' '\n' | grep -v "^and$"
# Result: graphql, openapi, rest
```

**Parsing examples:**
- `graphql and openapi` → `["graphql", "openapi"]`
- `graphql openapi rest` → `["graphql", "openapi", "rest"]`
- `build security` → `["security"]`

### Step 2: Find Module Directories

For each module name, search the project structure:

```bash
find . -maxdepth 5 -type f -name "pom.xml" -path "*/<module-name>/*" | head -5
```

**Selection priority:**
1. `extensions/<module-name>/` - Extension modules
2. `<module-name>/` - Top-level modules
3. `integration-tests/<module-name>/` - Integration test modules
4. `devtools/<module-name>/` - Developer tools

**Example:**
```bash
# Looking for "graphql"
find . -maxdepth 5 -type f -name "pom.xml" -path "*/graphql/*" | head -5
```

Might return:
```
./extensions/graphql/deployment/pom.xml
./extensions/graphql/runtime/pom.xml
./integration-tests/graphql/pom.xml
```

Choose the best match:
- For extension builds: `extensions/graphql/` (parent directory)
- For specific component: `extensions/graphql/runtime/`

### Step 3: Dispatch Parallel Builds

For each module, dispatch a subagent using the Agent tool. **Run all subagents in parallel** (multiple Agent calls in one response).

**Subagent prompt template:**
```
Build the Quarkus module at: <module-path>

Run the following command:
cd <module-path> && mvn clean install -DskipTests

Monitor the Maven output and report:
1. Whether the build succeeded or failed
2. If failed, include the relevant error output
3. Build time

Module: <module-name>
```

**Example with 3 modules:**
```
Dispatching 3 parallel builds:

Agent 1: Build extensions/graphql/
Agent 2: Build extensions/openapi/
Agent 3: Build extensions/rest/
```

### Step 4: Monitor Build Progress

Each subagent will:
1. Navigate to module directory
2. Run Maven build
3. Monitor for SUCCESS/FAILURE
4. Report back with results

You will be notified as each completes - no polling needed.

### Step 5: Report Results

After all subagents complete, present a summary:

**Format:**
```
Module Build Results (3 modules)

✓ graphql - Built successfully in 2m 15s
✓ openapi - Built successfully in 1m 48s
✗ rest - Build failed

Error in rest module:
[ERROR] /path/to/RestService.java:[23,15] cannot find symbol
  symbol:   class MissingClass
  location: package com.example

The RestService is trying to import a class that doesn't exist.
Next steps: Check if the dependency providing MissingClass is declared in the rest module's pom.xml
```

### Step 6: Suggest Next Steps

**After all succeed:**
- Suggest running tests for the built modules
- Mention the full build if many modules were changed

**After any fail:**
- Identify the specific module with issues
- Suggest fixes based on error type
- Offer to rebuild after fixes

## Advanced Build Options

**Build with dependencies:**
```bash
mvn install -DskipTests -am -pl :module-name
```
- `-am` = "also make" dependencies
- `-pl` = "project list" specific module

**Build without clean:**
```bash
mvn install -DskipTests
```
Faster for incremental changes.

**Build with tests:**
```bash
mvn clean install
```
Use when you need verification.

## Finding Module Paths

**Common Quarkus patterns:**

| Module Type | Path Pattern |
|-------------|--------------|
| Extension runtime | `extensions/<name>/runtime/` |
| Extension deployment | `extensions/<name>/deployment/` |
| Extension parent | `extensions/<name>/` |
| Integration test | `integration-tests/<name>/` |
| Dev tool | `devtools/<name>/` |
| Core | `core/<name>/` |

**Listing all modules:**
```bash
find . -name "pom.xml" -path "*/extensions/*" | sed 's|/pom.xml||' | sort
```

## Troubleshooting

**Module not found:**
```bash
# List all available modules
mvn help:evaluate -Dexpression=project.modules -q -DforceStdout
```

**Build order issues:**
Build the parent module to resolve dependencies:
```bash
cd extensions/<module-name>
mvn clean install -DskipTests
```

**Stale artifacts:**
```bash
cd <module-path>
mvn clean
mvn install -DskipTests
```

## Platform Notes

This skill is platform-agnostic:
- **Claude Code**: Use Agent tool for parallel subagents
- **Gemini CLI**: Use SubAgent tool
- **Codex**: Use SubAgent equivalents

The Maven commands are universal across platforms.

## Related Skills

- **quarkus-full-build** - Build entire project
- **java-classpath-search** - Find dependencies
- **java-decompile** - Inspect compiled classes
