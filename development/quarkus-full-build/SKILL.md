---
name: quarkus-full-build
description: Use when asked to do a full build, complete build, rebuild, or build everything in a Quarkus project. Runs the full Quarkus build with optimized flags via a subagent to keep the main conversation responsive.
---

# Quarkus Full Build

Run a complete build of the Quarkus project with optimized settings.

## Overview

This skill executes a full Quarkus build using Maven with flags optimized for speed and the Quarkus project structure. The build is dispatched to a subagent to keep your main conversation responsive during the long-running compilation.

## When to Use

- User asks to "do a full build"
- User requests "complete build" or "rebuild everything"
- User wants to "build the whole project"
- After major changes that require rebuilding all modules
- Before running integration tests
- When preparing a release or deployment

**When NOT to use:**
- For building specific modules (use `quarkus-module-build` instead)
- For incremental compilation (just run `mvn compile` directly)
- For running tests only (use `mvn test` directly)

## Quick Reference

**Build command:**
```bash
mvn install -Dquickly -Dno-test-modules -Dskip.gradle.build=true -T 16C -Prelocations
```

**Flags explained:**
- `-Dquickly` - Skip tests, formatting checks, and other non-essential tasks
- `-Dno-test-modules` - Don't build test-only modules
- `-Dskip.gradle.build=true` - Skip Gradle-based builds (Quarkus is Maven)
- `-T 16C` - Parallel build with 16 threads per CPU core
- `-Prelocations` - Use relocations profile for optimized dependencies

**Typical build time:** 5-15 minutes (depends on project size and machine)

## Implementation

### Step 1: Dispatch Build to Subagent

Use the Agent tool to run the build in a separate context. This keeps the main conversation responsive while the build runs.

**Subagent prompt:**
```
Run a full Quarkus build with the following command:

mvn install -Dquickly -Dno-test-modules -Dskip.gradle.build=true -T 16C -Prelocations

Monitor the Maven output and report:
1. Whether the build succeeded or failed
2. If it failed, include the relevant error output (compilation errors, test failures, etc.)
3. Total build time

Do not include the full Maven output unless there are errors.
```

### Step 2: Monitor Subagent Progress

The subagent will:
1. Execute the Maven build command
2. Watch for success/failure indicators in Maven output
3. Report back when complete

You don't need to poll - the subagent will notify when done.

### Step 3: Report Results

After the subagent completes, summarize:

**On success:**
```
✓ Full Quarkus build completed successfully in 8m 42s

The project is ready for testing or deployment.
```

**On failure:**
```
✗ Full Quarkus build failed during compilation

Error in extensions/quarkus-graphql/runtime:
[ERROR] /path/to/GraphQLService.java:[45,23] cannot find symbol
  symbol:   method getSchema()
  location: variable config of type GraphQLConfig

The GraphQLService class is calling a method that doesn't exist in GraphQLConfig.
```

### Step 4: Offer Next Steps

**After success:**
- Suggest running tests if they were skipped
- Offer to build specific modules if changes are localized
- Mention deployment options if appropriate

**After failure:**
- Identify the failing module
- Suggest fixes based on error type
- Offer to build just the failing module after fixes

## Common Build Flags

| Flag | Purpose | When to Use |
|------|---------|-------------|
| `-Dquickly` | Skip tests and checks | Fast feedback during development |
| `-DskipTests` | Skip test execution only | When tests are slow but you want other checks |
| `-T 1C` | Single-threaded | Debugging build order issues |
| `-T 16C` | Parallel (16 threads/core) | Fast builds on powerful machines |
| `-am` | Also make dependencies | Building a module with its dependencies |
| `-pl module` | Build specific module | Testing changes in one module |

## Build Troubleshooting

**Out of memory:**
```bash
export MAVEN_OPTS="-Xmx4g -XX:MaxMetaspaceSize=1g"
mvn install -Dquickly ...
```

**Stale artifacts:**
```bash
mvn clean install -Dquickly ...
```

**Dependency resolution issues:**
```bash
mvn dependency:purge-local-repository
mvn install -Dquickly ...
```

## Platform Notes

This skill is platform-agnostic:
- **Claude Code**: Use Agent tool for subagent dispatch
- **Gemini CLI**: Use SubAgent tool
- **Codex**: Use SubAgent/Background execution

The Maven command itself is universal across all platforms.

## Related Skills

- **quarkus-module-build** - Build specific modules only
- **java-classpath-search** - Find dependencies after build
- **java-decompile** - Inspect built classes
