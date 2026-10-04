---
name: gradle-build
description: >-
  Gradle Kotlin DSL build standards for Java game mod projects. Use when editing
  build.gradle.kts, settings.gradle.kts, gradle.properties, or when adding dependencies,
  configuring tasks, or troubleshooting build failures.
---

# Gradle Build Standards

## Project Context

- **Build system**: Gradle with Kotlin DSL (`build.gradle.kts`)
- **Java version**: 25 (configured via `java.toolchain`)
- **Plugin**: `hytale-mod` (provides `runServer`, asset management)
- **Dependency sources**: Maven Central + `maven.hytale-modding.info`

## Key Rules

### Dependencies

```kotlin
// ✅ compileOnly for API jars (provided at runtime by the game)
compileOnly(libs.jetbrains.annotations)

// ✅ implementation for bundled libs (included in mod jar)
implementation(files("libs/HyUI-0.9.5-all.jar"))

// ❌ NEVER use implementation for game API classes
// They are already on the classpath at runtime
```

### Version Catalog

- Use `libs.<alias>` references from `gradle/libs.versions.toml`
- Never hardcode version strings in `build.gradle.kts`
- Exception: local file jars (`files("libs/...")`)

### Task Configuration

```kotlin
// ✅ Use typed task configuration
tasks.named<ProcessResources>("processResources") { ... }
tasks.withType<Jar> { ... }

// ❌ Don't use string-only task references
tasks.getByName("processResources")
```

### Resource Processing

- `manifest.json` uses template expansion → protect with `exclude("manifest.json")` in sync tasks
- Assets sync from `build/resources/main` → `src/main/resources` after server stop
- JSON spell/config files go in `src/main/resources/Server/`

### Common Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| `ClassNotFoundException` at runtime | Wrong dependency scope | `compileOnly` → game provides it |
| Assets not loading | Wrong resource path | Check `Server/Spells/` structure |
| Template not expanded | Missing `filesMatching` | Add to `processResources` block |
| Build cache stale | Incremental build issue | `./gradlew clean build` |

## Build Commands

```bash
# Full build
./gradlew build

# Run dev server (if hytale-mod plugin provides it)
./gradlew runServer

# Clean + rebuild
./gradlew clean build

# Check dependencies
./gradlew dependencies --configuration compileClasspath
```

## File Structure

```
project/
├── build.gradle.kts          # Main build config
├── settings.gradle.kts       # Project settings
├── gradle.properties         # Plugin properties (version, author, etc.)
├── gradle/
│   └── libs.versions.toml    # Version catalog
├── libs/                     # Local jar dependencies
└── src/main/
    ├── java/                 # Java source
    └── resources/
        ├── manifest.json     # Plugin manifest (templated)
        ├── Server/           # Server-side assets
        │   ├── Spells/       # Spell JSON configs
        │   └── Languages/    # i18n files
        └── Common/           # Shared assets
```
