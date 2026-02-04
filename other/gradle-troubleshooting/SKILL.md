---
name: gradle-troubleshooting
description: |
  Diagnose and fix common Gradle build issues including OutOfMemory errors,
  dependency conflicts, build cache problems, configuration cache issues,
  and slow builds. Use when builds fail, run slowly, or behave unexpectedly.
  Includes debug commands, common causes, and proven solutions.
---

# Gradle Troubleshooting

## Table of Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Quick Start](#quick-start)
- [Instructions](#instructions)
- [Examples](#examples)
- [Commands Reference](#commands-reference)
- [Troubleshooting Checklist](#troubleshooting-checklist)
- [Quick Reference: Common Issues](#quick-reference-common-issues)
- [See Also](#see-also)

## Purpose

Quickly diagnose and resolve Gradle build problems using systematic debugging techniques, build scans, and proven solutions. This skill covers memory issues, dependency resolution, caching problems, and performance analysis.

## When to Use

Use this skill when you need to:
- Debug OutOfMemoryError or heap space issues
- Resolve dependency conflicts and version mismatches
- Fix build cache or configuration cache problems
- Diagnose slow build performance
- Troubleshoot daemon or wrapper issues
- Debug plugin loading failures
- Resolve TestContainers or Docker connectivity issues
- Investigate test failures in CI but not locally

## Quick Start

When a build fails, run in order:

```bash
# 1. Stop daemon and clean
./gradlew --stop
./gradlew clean

# 2. Run with diagnostics
./gradlew build --stacktrace --info

# 3. If still failing, generate build scan
./gradlew build --scan

# 4. If slow, profile
./gradlew build --profile
```

## Instructions

### Step 1: Diagnose with Debug Output

Run with increasing verbosity to identify the issue:

```bash
# Stack trace (shows where error occurred)
./gradlew build --stacktrace

# Full stack trace (complete call stack)
./gradlew build --full-stacktrace

# Info logging (what Gradle is doing)
./gradlew build --info

# Debug logging (very detailed, generates lots of output)
./gradlew build --debug

# Use grep to filter
./gradlew build --info 2>&1 | grep -i error
./gradlew build --info 2>&1 | grep cache
```

### Step 2: Identify the Issue Category

**OutOfMemoryError**:
```bash
./gradlew build 2>&1 | grep -i "outofmemory\|java heap\|metaspace"
```

**Dependency resolution**:
```bash
./gradlew dependencies --info 2>&1 | grep -i "could not\|failed\|error"
./gradlew dependencyInsight --dependency spring-core
```

**Build cache problems**:
```bash
./gradlew build --no-build-cache --info 2>&1 | grep cache
```

**Configuration cache**:
```bash
./gradlew build --no-configuration-cache --info
```

**Plugin issues**:
```bash
./gradlew build --stacktrace 2>&1 | grep -A 5 "plugin"
```

### Step 3: Fix OutOfMemoryError

**Immediate fix** - Increase heap size:

```bash
# For this build only
./gradlew build -Dorg.gradle.jvmargs="-Xmx8g"

# Or stop daemon and increase persistent memory
./gradlew --stop
```

**Permanent fix** - Update `gradle.properties`:

```properties
# For standard projects (10-30 modules)
org.gradle.jvmargs=-Xmx4g -XX:MaxMetaspaceSize=1g -XX:+HeapDumpOnOutOfMemoryError -Dfile.encoding=UTF-8

# For large projects (30+ modules)
org.gradle.jvmargs=-Xmx8g -XX:MaxMetaspaceSize=2g -XX:+HeapDumpOnOutOfMemoryError -Dfile.encoding=UTF-8

# For very large projects
org.gradle.jvmargs=-Xmx12g -XX:MaxMetaspaceSize=3g -XX:+HeapDumpOnOutOfMemoryError -Dfile.encoding=UTF-8
```

**Verify fix**:

```bash
./gradlew --stop  # Must restart daemon
./gradlew build --info 2>&1 | grep "XX:Xmx"
```

### Step 4: Debug Dependency Resolution

Understand why dependencies aren't resolving:

```bash
# Show full dependency tree
./gradlew dependencies

# Show specific configuration
./gradlew dependencies --configuration implementation

# Find where a dependency comes from
./gradlew dependencyInsight --dependency spring-core

# Show dependency insights for specific config
./gradlew dependencyInsight --dependency jackson-databind --configuration implementation

# Refresh and re-download
./gradlew build --refresh-dependencies
```

**Common solutions**:

**Option 1: Force specific version**:

```kotlin
// build.gradle.kts
configurations.all {
    resolutionStrategy {
        force("com.google.guava:guava:32.1.3-jre")
    }
}
```

**Option 2: Exclude problematic transitive dependency**:

```kotlin
dependencies {
    implementation("com.example:library:1.0") {
        exclude(group = "commons-logging", module = "commons-logging")
    }
}
```

**Option 3: Use dependency constraints**:

```kotlin
dependencies {
    constraints {
        implementation("org.apache.commons:commons-lang3:3.18.0")
    }
}
```

### Step 5: Debug Build Cache Issues

Test if build cache is causing problems:

```bash
# Disable cache for this build
./gradlew build --no-build-cache

# If this fixes it, cache is the problem
# Clean cache
rm -rf ~/.gradle/caches/build-cache-*

# Check cache status
./gradlew build --build-cache --info | grep cache

# Verify task is cacheable
./gradlew build --info 2>&1 | grep "Cache key"
```

**Common build cache issues**:

**Issue**: Build slower with cache enabled

```bash
# Check for non-cacheable tasks
./gradlew build --info 2>&1 | grep -i "non-cacheable"
```

**Issue**: Incorrect cached results

```bash
# Clean entire cache
rm -rf ~/.gradle/caches

# Rebuild
./gradlew build
```

### Step 6: Debug Configuration Cache

Test if configuration cache is compatible:

```bash
# Start with warnings (not errors)
./gradlew build --configuration-cache-problems=warn

# Check report
# build/reports/configuration-cache/<hash>/configuration-cache-report.html

# Once issues fixed, enable strict mode
./gradlew build --configuration-cache-problems=fail
```

**Common configuration cache issues**:

**Issue**: Build fails with configuration cache

```bash
# Disable temporarily
./gradlew build --no-configuration-cache

# Check for incompatible plugins
./gradlew build --configuration-cache-problems=warn --info

# View detailed report
open build/reports/configuration-cache/report.html
```

**Issue**: Plugins not compatible

```bash
# Update plugins to latest versions
./gradlew wrapper --gradle-version 9.2
./gradlew build -x test  # Skip tests temporarily
```

### Step 7: Diagnose Slow Builds

Use profiling to identify bottlenecks:

```bash
# Generate profile report
./gradlew build --profile

# Report location
# build/reports/profile/profile-<timestamp>.html
open build/reports/profile/profile-*.html

# Or use build scan (cloud-based analysis)
./gradlew build --scan
```

**Common slow build causes**:

**Configuration phase slow**:
```bash
# Check what's slow in configuration
./gradlew build --info 2>&1 | grep -E "Evaluating|Processing"

# Enable configuration cache
./gradlew build --configuration-cache
```

**Compilation slow**:
```bash
# Enable incremental compilation (should be default)
# Check for full recompilation
./gradlew build --info 2>&1 | grep -i "incremental\|full"

# Clean and rebuild
./gradlew clean build
```

**Tests slow**:
```bash
# Run unit tests only (exclude integration tests)
./gradlew test -x integrationTest

# Enable parallel test execution
# In build.gradle.kts:
# tasks.test { maxParallelForks = Runtime.getRuntime().availableProcessors() / 2 }
```

**Network slow**:
```bash
# Check network dependency resolution
./gradlew build --info 2>&1 | grep "Downloading\|Uploading"

# Use offline mode if dependencies are cached
./gradlew build --offline

# Check repositories configuration
./gradlew build --info 2>&1 | grep repositories
```

### Step 8: Daemon Management Issues

Handle daemon-related problems:

```bash
# Check daemon status
./gradlew --status

# Stop all daemons
./gradlew --stop

# Run without daemon (if daemon is problematic)
./gradlew build --no-daemon

# Run with new daemon (fresh start)
./gradlew --stop && ./gradlew build
```

**Issue: Daemon using old gradle.properties**:

```bash
# Stop daemon
./gradlew --stop

# Update gradle.properties
# org.gradle.jvmargs=-Xmx4g

# Run build (new daemon starts with new settings)
./gradlew build
```

**Issue: Daemon crashed**:

```bash
# Kill daemon process
pkill -f "gradle.*daemon"

# Or use Gradle command
./gradlew --stop

# Verify no daemons running
./gradlew --status

# Run build
./gradlew build
```

### Step 9: Gradle Wrapper Issues

Fix wrapper script problems:

```bash
# Make wrapper executable
chmod +x gradlew

# Regenerate wrapper
gradle wrapper --gradle-version 9.2

# Validate wrapper
./gradlew wrapper --gradle-version 9.2 --validate-distribution-url

# Check current version
./gradlew --version
```

**Issue: Wrong Gradle version**:

```bash
# Update to specific version
./gradlew wrapper --gradle-version 9.2

# Or latest
./gradlew wrapper --gradle-version latest

# Verify
./gradlew --version
```

### Step 10: Plugin and Repository Issues

Resolve plugin loading problems:

```bash
# Check plugin resolution
./gradlew build --stacktrace 2>&1 | grep -i plugin

# Add plugin repositories (settings.gradle.kts)
# pluginManagement {
#     repositories {
#         gradlePluginPortal()
#         mavenCentral()
#     }
# }

# Force refresh plugin resolution
./gradlew build --refresh-dependencies
```

## Examples

### Example 1: Complete Troubleshooting Workflow

```bash
# 1. Initial failure
./gradlew build
# BUILD FAILED

# 2. Get details
./gradlew build --stacktrace
# Shows: OutOfMemoryError: Java heap space

# 3. Fix: Update gradle.properties
echo "org.gradle.jvmargs=-Xmx4g -XX:MaxMetaspaceSize=1g" >> gradle.properties

# 4. Stop daemon and retry
./gradlew --stop
./gradlew build

# BUILD SUCCESSFUL
```

### Example 2: Dependency Conflict Resolution

```bash
# Build fails with version conflict
./gradlew build
# ERROR: Could not resolve dependency: conflicting versions

# Investigate
./gradlew dependencyInsight --dependency commons-lang3

# You see:
# commons-lang3:3.8.1 <- old-library
# commons-lang3:3.18.0 <- new-library

# Solution: Force newer version
# In build.gradle.kts:
configurations.all {
    resolutionStrategy {
        force("org.apache.commons:commons-lang3:3.18.0")
    }
}

./gradlew build
# BUILD SUCCESSFUL
```

### Example 3: Slow Build Performance Analysis

```bash
# Build is slow
./gradlew build
# Took 3 minutes

# Profile the build
./gradlew build --profile
# Report: build/reports/profile/profile-2025-11-14-09-30-45.html

# Analysis shows:
# - Configuration phase: 45 seconds (slow!)
# - Compilation: 60 seconds
# - Tests: 90 seconds

# Solution: Enable configuration cache
# In gradle.properties:
echo "org.gradle.configuration-cache=true" >> gradle.properties
echo "org.gradle.caching=true" >> gradle.properties

./gradlew --stop
./gradlew build
# Took 45 seconds (88% faster!)
```

### Example 4: Configuration Cache Debugging

```bash
# Build fails with configuration cache
./gradlew build --configuration-cache
# ERROR: Unsupported class: MyCustomTask

# Start with warnings
./gradlew build --configuration-cache-problems=warn

# Check report
open build/reports/configuration-cache/report.html
# Shows: Task 'MyCustomTask' is not serializable

# Solution: Update task to be configuration cache compatible
# In build.gradle.kts:
// Before
tasks.register("myTask") {
    // Non-cacheable work
}

// After
tasks.register("myTask") {
    @Input
    val myProperty = "value"
    // Make task properly input/output decorated
}

./gradlew build --configuration-cache
# SUCCESS!
```

### Example 5: TestContainers Docker Issues

```bash
# Integration tests fail with Docker error
./gradlew integrationTest
# ERROR: Could not connect to Docker daemon

# Check Docker
docker ps
# Cannot connect to Docker daemon

# Solution: Start Docker
# On macOS
open /Applications/Docker.app

# Set environment variables
export TESTCONTAINERS_DOCKER_SOCKET_OVERRIDE=/var/run/docker.sock
export DOCKER_HOST=unix://${HOME}/.docker/run/docker.sock

# Retry
./gradlew integrationTest
# BUILD SUCCESSFUL
```

## Commands Reference

### Diagnostic Commands

```bash
# === DEBUG OUTPUT ===
./gradlew build --stacktrace         # Stack trace
./gradlew build --full-stacktrace    # Full stack trace
./gradlew build --info               # Info logging
./gradlew build --debug              # Debug logging
./gradlew build --console=plain      # Plain text output

# === BUILD ANALYSIS ===
./gradlew build --scan               # Build scan (visual analysis)
./gradlew build --profile            # Profile report
./gradlew build --dry-run            # Show what would run

# === CACHING ===
./gradlew build --no-build-cache     # Disable build cache
./gradlew build --no-configuration-cache  # Disable config cache
./gradlew build --build-cache --info # Check cache usage

# === DAEMON ===
./gradlew --status                   # Show daemon status
./gradlew --stop                     # Stop daemons
./gradlew build --no-daemon          # Run without daemon

# === DEPENDENCIES ===
./gradlew dependencies               # Show dependency tree
./gradlew dependencies --info        # Show with details
./gradlew dependencyInsight --dependency spring-core  # Find dependency
./gradlew build --refresh-dependencies  # Force refresh

# === CLEANING ===
./gradlew clean                      # Clean build outputs
rm -rf ~/.gradle/caches              # Clear entire cache
./gradlew --stop && rm -rf ~/.gradle/caches  # Hard reset
```

### Filtering Output

```bash
# Grep for common issues
./gradlew build --info 2>&1 | grep -i error
./gradlew build --info 2>&1 | grep cache
./gradlew build --info 2>&1 | grep "Xmx"
./gradlew build --stacktrace 2>&1 | head -50
```

## Troubleshooting Checklist

When builds fail, work through this checklist:

1. ✅ **Clear and restart**:
   ```bash
   ./gradlew --stop
   ./gradlew clean
   ```

2. ✅ **Check basics**:
   ```bash
   ./gradlew --version           # Verify Gradle version
   java -version                 # Verify Java version
   ```

3. ✅ **Get detailed output**:
   ```bash
   ./gradlew build --stacktrace --info
   ```

4. ✅ **Refresh dependencies**:
   ```bash
   ./gradlew build --refresh-dependencies
   ```

5. ✅ **Disable caching**:
   ```bash
   ./gradlew build --no-build-cache --no-configuration-cache
   ```

6. ✅ **Check environment**:
   ```bash
   env | grep GRADLE
   env | grep JAVA
   ```

7. ✅ **Review recent changes**:
   - Changes to build.gradle.kts?
   - Changes to gradle.properties?
   - Updated plugins?

8. ✅ **Generate build scan**:
   ```bash
   ./gradlew build --scan
   ```

9. ✅ **Run without daemon**:
   ```bash
   ./gradlew build --no-daemon
   ```

10. ✅ **Last resort - Full reset**:
    ```bash
    ./gradlew --stop
    rm -rf ~/.gradle/caches
    rm -rf build/
    ./gradlew clean build
    ```

## Quick Reference: Common Issues

| Issue | Symptoms | Command | Fix |
|-------|----------|---------|-----|
| OutOfMemory | `Java heap space` | `./gradlew build -Xmx8g` | Increase in `gradle.properties` |
| Slow build | Takes 2+ minutes | `./gradlew build --profile` | Enable caching in `gradle.properties` |
| Dependency missing | `Could not resolve` | `./gradlew dependencyInsight` | Check repositories, force version |
| Cache invalid | Failures with cache on | `./gradlew --no-build-cache` | `rm -rf ~/.gradle/caches` |
| Daemon stale | Config not applied | `./gradlew --stop` | Restart daemon |
| Plugin not found | `Plugin not found` | `./gradlew --stacktrace` | Check `pluginManagement` repos |
| Test failures | Tests fail in CI only | `./gradlew test --info` | Check environment variables |
| Docker errors | TestContainers fail | `docker ps` | Verify Docker running |

## See Also

- [gradle-performance-optimization](../gradle-performance-optimization/SKILL.md) - Optimize builds
- [gradle-dependency-management](../gradle-dependency-management/SKILL.md) - Resolve dependencies
- [gradle-testing-setup](../gradle-testing-setup/SKILL.md) - Configure tests
- [Gradle Troubleshooting Guide](https://docs.gradle.org/current/userguide/troubleshooting.html)
- [Build Scans](https://scans.gradle.com/) - Analyze builds visually
