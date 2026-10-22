---
name: Code Style & Lint Enforcer
description: Instructions for maintaining code quality via Android Lint and style rules.
---

# Code Style & Lint Enforcer

This skill guides the usage of Android Lint to ensure code quality and adherence to best practices.

## Running Lint
Execute the lint task via Gradle Commander:
```bash
./gradlew lint
```
(Or `lintDebug`, `lintRelease` for specific variants).

## Interpreting Results
- **HTML Report**: Usually found at `app/build/reports/lint-results.html`.
- **XML Report**: `app/build/reports/lint-results.xml`.

## Common Fixes

### 1. Unused Resources
*Error*: "The resource 'R.string.foo' appears to be unused"
*Action*: Verify it's truly unused (check for dynamic reflection usage). If confirmed, remove it.

### 2. Deprecated APIs
*Error*: "Usage of deprecated method"
*Action*: Check the documentation for the recommended replacement.

### 3. Hardcoded Text
*Error*: "HardcodedString: Hardcoded string "Loading...", should use @string resource"
*Action*: Move the string to `strings.xml` (See **Localization & String Manager** skill).

### 4. Accessibility
*Error*: "Missing contentDescription"
*Action*: Add `android:contentDescription="@string/desc_..."` to ImageViews and ImageButtons. Use `@null` only for decorative images.
