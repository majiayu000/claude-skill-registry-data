---
name: dgroomes-project-conventions
description: Conventions and style guidelines for dgroomes' personal projects. Use when upgrading, maintaining, or creating projects in dgroomes' repositories. Covers README style, Gradle configuration, version catalogs, commit messages, and general code conventions.
---

# dgroomes Project Conventions

## Overview

This skill captures the conventions and patterns used across dgroomes' personal "playground" repositories. Apply these conventions when upgrading dependencies, restructuring projects, or creating new content.


## README Conventions

### Structure and Formatting

- Single-line description immediately after the `# heading`
- Use 📚 emoji prefix for playground/learning repos (e.g., "📚 Learning and exploring JUnit.")
- **Two newlines** before each markdown section (not one)
- Use `-` for list items, not `*`

### Required Sections

1. **Title** - `# project-name`
2. **One-line description** - With 📚 emoji for playground repos
3. **Quote block** (optional) - Official tagline from the technology's website
4. **Overview** - Expanded description of the project
5. **Subproject listings** (if applicable) - Each with `### \`subproject/\`` heading
6. **Instructions** - Numbered steps with code blocks
7. **Wish List** - TODOs and future work
8. **Reference** - Links (singular "Reference", not "References")

### Quote Block Style

```markdown
> The programmer-friendly testing framework for Java and the JVM
>
> -- <cite>https://junit.org/</cite>
```

### Overview Section

- Comes after the one-line description and optional quote block
- Provides expanded context, motivation, or explanation
- Can include multiple paragraphs
- No "Follow these instructions" here - that goes in Instructions section

### Instructions Section

- Start with intro line: "Follow these instructions to..." or "Follow the below instructions to..."
- Numbered list (1, 2, 3...)
- Sub-bullets use `*` with 3-space indent for commands and explanations
- **STRONG GUIDELINE: Never go more than one indentation level** - no nested sub-sub-bullets
- Use fenced code blocks with `shell` language
- Code fences are indented to align with the bullet text (3 spaces + `* ` + fence)
- Include timing information when demonstrating performance ("The command took X seconds for me")

Example structure:
```markdown
## Instructions

Follow these instructions to build and run the project.

1. Pre-requisite: Java 25
2. Build the program
   * ```shell
     ./gradlew build
     ```
   * The command took 2.3 seconds for me
3. Run the tests
   * ```shell
     ./gradlew test
     ```
```

Note the indentation pattern:
- Number at column 0
- `* ` at column 3 (3 spaces)
- Code fence at column 5 (aligned with text after `* `)
- Code content at column 5 (same as fence)

### Wish List Conventions

- Use `- [ ]` for open items
- Use `- [x] DONE` for completed items (keep these, don't delete!)
- Use `- [ ] SKIP` for skipped items (unchecked, not `[x]`)
- Format: `- [x] DONE Description of what was done`


## Gradle Conventions

### Version Catalog (libs.versions.toml)

- Place in `gradle/libs.versions.toml`
- For composite builds (includeBuild), each needs its own `gradle/libs.versions.toml`
- **Alphabetical ordering** in both `[versions]` and `[libraries]` sections
- Include release notes URL as comment

```toml
[versions]
junit = "6.0.1" # JUnit releases: https://junit.org/junit5/docs/current/release-notes/index.html
slf4j = "2.0.17" # SLF4J releases: http://www.slf4j.org/news.html

[libraries]
junit-bom = { module = "org.junit:junit-bom", version.ref = "junit" }
junit-jupiter = { module = "org.junit.jupiter:junit-jupiter" }
slf4j-api = { module = "org.slf4j:slf4j-api", version.ref = "slf4j" }
```

### Build File Style

- Use `layout.buildDirectory.dir("path")` instead of string interpolation like `"${layout.buildDirectory.asFile.get()}/path"`
- Use Java toolchain for version specification:
  ```kotlin
  java {
      toolchain {
          languageVersion.set(JavaLanguageVersion.of(25))
      }
  }
  ```

### JUnit BOM Usage

- Use the JUnit BOM for dependency management
- BOM manages versions for jupiter, platform, vintage
- **Exception**: `junit-platform-console-standalone` needs explicit version (it's an uber-jar not managed by BOM)

```kotlin
dependencies {
    implementation(platform(libs.junit.bom))
    testImplementation(platform(libs.junit.bom))

    testImplementation(libs.junit.jupiter)
    testRuntimeOnly(libs.junit.platform.launcher)

    // Needs explicit version - not managed by BOM
    junitLauncher(libs.junit.platform.console.standalone)
}
```


## JUnit 6 Specifics

### Unified Versioning

JUnit 6 uses unified versioning - Platform, Jupiter, and Vintage all share the same version number. The old JUnit 5 pattern of "replace leading 5 with 1 for Platform" is obsolete.

### CLI Changes

JUnit 6 Console Launcher uses subcommands. Add `execute` before options:

```bash
# JUnit 5 style (old)
java -jar junit-platform-console-standalone.jar --scan-classpath

# JUnit 6 style (new)
java -jar junit-platform-console-standalone.jar execute --scan-classpath
```


## General Code Conventions

### Comments

- **Never delete existing comments** - preserve them when rewriting code
- **Never add comments** unless explaining cryptic or unusual code
- No docstrings, type annotations, or comments on code you didn't change

### File Operations

- Never delete files yourself - ask the user to do it
- Prefer editing existing files over creating new ones

### Preserving Content

- Don't delete timing information in READMEs (it's narrative content)
- Don't delete DONE wish list items (they document project history)
- Don't delete existing emoji usage


## Commit Message Style

Short and descriptive. Patterns:

- `Upgrades: JUnit 6, Java 25, Gradle version catalog`
- `[subproject] Description of change`
- `Update lib versions; readme style`
- Single word for simple changes: `Upgrades`, `Cleanup`


## Project Structure Patterns

### Standalone Subprojects

- Each subproject is completely independent
- Root `settings.gradle.kts` uses `includeBuild()` for composite builds
- Each subproject has its own README, build files, and potentially gradle wrapper

### Utility Projects

- Helper projects (like `util/`) use `include()` not `includeBuild()`
- These share the root project's version catalog
