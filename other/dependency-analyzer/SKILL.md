---
name: dependency-analyzer
description: Analyze Maven dependencies in Java projects to find unused, duplicate, or outdated dependencies. Use when user says "analyze dependencies", "find unused deps", "clean pom.xml", "dependency audit", or "check dependencies".
---

# Dependency Analyzer Skill

Analyzes Maven project dependencies to identify unused, potentially removable, or problematic dependencies.

## When to Use
- "analyze dependencies" / "check dependencies"
- "find unused dependencies" / "clean pom.xml"
- "dependency audit" / "dependency review"
- Before major version upgrades or dependency cleanup

## Analysis Strategy

### Step 1: Extract all dependencies from pom.xml
Read the pom.xml and list every `<dependency>` with groupId, artifactId, version, and scope.

### Step 2: Classify each dependency

For each dependency, determine its **type**:

| Type | How to detect | Can be safely removed? |
|------|--------------|----------------------|
| **Directly imported** | Has matching `import` statements in `src/main/java` or `src/test/java` | No - actively used |
| **Runtime/Provider** | No imports but required at runtime (JDBC drivers, security providers, logging backends, annotation processors) | No - needed at runtime |
| **Transitive duplicate** | Already pulled in by another dependency | Maybe - verify with `mvn dependency:tree` |
| **Unused** | No imports, not a runtime dependency, not referenced anywhere | Yes - candidate for removal |
| **Test-only** | Only imported in `src/test/java` but scoped as `compile` | Should change scope to `test` |

### Step 3: Search for usage

For each dependency, search for its **common packages** in the source code:

**Search method:**
1. Identify the base package of the dependency (e.g., `org.apache.poi` for Apache POI)
2. Search for `import <base-package>` in all Java files under `src/main/java` and `src/test/java`
3. Also search for annotations, class references, and Spring configuration references
4. Check `application*.yml` and `application*.properties` for configuration keys tied to the dependency

**Known runtime dependencies that won't have direct imports:**
- `postgresql` / JDBC drivers → used via `spring.datasource.url` config
- `spring-boot-starter-*` → pull in auto-configuration, no direct imports needed
- `hibernate-jpamodelgen` → annotation processor, generates code at compile time
- `lombok` → annotation processor
- `bcprov-*` / BouncyCastle → registered as security provider in `java.security`
- `logback-*` / `slf4j-*` → logging backends, used via SLF4J facade
- `spring-boot-devtools` → development tooling
- `micrometer-*` → metrics, auto-configured by Spring Boot actuator
- `jackson-*` → often used transitively via Spring Boot for JSON serialization

### Step 4: Generate report

Output a structured report:

```
## Dependency Analysis Report

### ✅ Actively Used (N dependencies)
- groupId:artifactId — used in X files, example: `com.example.MyClass`

### ⚠️ Scope Mismatch (N dependencies)
- groupId:artifactId — only used in tests but scoped as compile → change to `<scope>test</scope>`

### 🔍 Runtime/Provider (N dependencies)
- groupId:artifactId — no direct imports but required because: [reason]

### ❌ Potentially Unused (N dependencies)
- groupId:artifactId — no imports found, no runtime requirement identified
  → Recommendation: remove and verify compilation + tests pass

### 📦 Managed by BOM/Parent (N dependencies)
- groupId:artifactId — version managed by spring-boot-starter-parent
```

### Step 5: Verification recommendations

For each potentially unused dependency, suggest:
1. Remove from pom.xml
2. Run `mvn clean compile -DskipTests` to verify compilation
3. Run `mvn test` to verify tests pass
4. If either fails, the dependency is needed (possibly transitively)

## Important Notes

- **Never auto-remove dependencies** — always present findings and let the user decide
- **Spring Boot starters** are meta-dependencies that pull in many transitive deps — they rarely have direct imports themselves but are essential
- **BOM-managed versions** (via `<dependencyManagement>`) should be noted but are not candidates for removal from the BOM
- **Provided scope** dependencies (like `servlet-api`) are compile-time only and won't be in the final JAR
- A dependency with 0 imports is NOT automatically unused — always check runtime requirements
- When in doubt, recommend keeping the dependency and flagging for manual review
