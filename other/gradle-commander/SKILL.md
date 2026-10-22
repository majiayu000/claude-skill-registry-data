---
name: Gradle Commander
description: Expert instructions for managing Android builds using Gradle.
---

# Gradle Commander

This skill provides expertise in interacting with the Gradle build system for Android projects.

## Core Principles
1.  **Always use the Wrapper**: Use `./gradlew` (or `gradlew.bat` on Windows) instead of a system-installed `gradle` binary to ensure version consistency.
2.  **Clean Builds**: When facing inexplicable build errors, running a clean task often helps.
3.  **Parallel Execution**: Gradle runs tasks in parallel by default; be aware of potential race conditions in custom tasks.

## Common Commands

### 1. Building the APK
To build the debug APK:
```bash
./gradlew assembleDebug
```
To build the release APK (requires signing config):
```bash
./gradlew assembleRelease
```

### 2. Installation
To build and install the debug APK onto a connected device:
```bash
./gradlew installDebug
```

### 3. Cleaning
To remove the `build` directory:
```bash
./gradlew clean
```

### 4. Running Tests
Unit tests:
```bash
./gradlew testDebugUnitTest
```
Android Instrumentation tests:
```bash
./gradlew connectedDebugAndroidTest
```

### 5. Dependency Analysis
To see the dependency tree for the app module (debug variant):
```bash
./gradlew app:dependencies --configuration debugCompileClasspath
```

## Troubleshooting Build Errors
- **Read the Output**: Scroll up from the "Build Failed" message. The actual error is often hidden amidst warnings.
- **Stacktrace**: If the error is vague, run with `--stacktrace` (e.g., `./gradlew assembleDebug --stacktrace`).
- **Info/Debug**: For deeper inspection, use `--info` or `--debug`.
