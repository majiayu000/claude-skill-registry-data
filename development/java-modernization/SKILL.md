---
name: java-modernization
description: >-
  Modernizes Java applications by upgrading the Java version and updating dependencies
  to compatible versions — improving security, performance, and maintainability while
  keeping the project buildable at every step.

  Use this skill whenever the user wants to upgrade Java versions, migrate from javax to
  Jakarta EE, update Spring Boot, modernize dependencies, or do any kind of Java version
  migration — even if they phrase it as "upgrade to Java 21", "migrate to Spring Boot 3",
  "update dependencies", "fix javax imports", "modernize the project", or "update to Jakarta".

  This skill covers: build system readiness, Jakarta EE namespace migration, database/ORM
  modernization, core dependency updates, Spring ecosystem upgrades, and final integration
  verification. Always use this skill for Java upgrade or dependency modernization tasks.

  Triggers: "upgrade java", "migrate to java 17/21", "update spring boot", "javax to jakarta",
  "modernize dependencies", "update pom.xml", "dependency upgrades", "java version migration".
---

# Java Application Modernization

## Objective
Modernize Java applications by upgrading to a newer Java version and updating dependencies to compatible versions, enhancing security, performance, and maintainability while ensuring the application remains buildable at each step.

## Summary
This skill follows a constraint-based approach organized into logical groups. Each group must be completed successfully before proceeding to the next. The focus is on maintaining buildable states and proper dependency sequencing rather than prescriptive step-by-step instructions.

## Entry Criteria
- Project builds successfully with the current Java version
- Maven or Gradle build system present with accessible configuration files
- Maven version compatibility verified (Maven 3.6.0+ required for Java 17+, Maven 3.9.0+ required for compiler plugin 3.13+)
- Complete inventory of dependencies available (`pom.xml`, `build.gradle`, etc.)
- Test suite or validation methods accessible to verify successful migration
- Source code in version control to allow rollback if needed
- Development environment supports both current and target Java versions during transition
- Sufficient permissions to update dependencies and modify configuration files

## Pre-flight Validation
Before starting, verify:
- Maven/Gradle version compatibility (`mvn --version` or `gradle --version`)
- Establish a clean build baseline (build must pass before any changes)
- Required tool versions available in the environment

---

## Transformation Groups

Complete each group fully before proceeding to the next.

### Group 1: Build System Readiness
**Goal**: Prepare the build system for the target Java version.

**Atomic operations (keep separate — different failure modes):**
1. Establish build baseline — run the build with the current Java version and confirm it passes
2. Update build tools atomically: Gradle wrapper + compiler plugin + Lombok (to versions in Mandatory Dependency Versions)
3. Update Java version in all `pom.xml` / `build.gradle` files + verify compilation

**Success criteria**: Project builds successfully targeting the new Java version.

---

### Group 2: Jakarta EE Migration
**Goal**: Complete the `javax` → `jakarta` namespace migration as a single atomic operation.

**Do NOT split this into multiple steps — partial Jakarta migration breaks the build.**

**Single coordinated operation:**
1. Update ALL Jakarta dependencies together: validation, servlet, persistence, annotation, mail, activation, xml.bind, xml.ws, jws (to versions in Mandatory Dependency Versions)
2. Update ALL `import javax.*` statements across the entire codebase in one pass
3. Update `web.xml` and `persistence.xml` schemas to Jakarta namespaces

**Success criteria**: No `javax.*` imports remain (except `javax.xml` and `javax.swing`). Project builds successfully.

---

### Group 3: Database & ORM Modernization
**Goal**: Update the database ecosystem as a coordinated group.

**Single atomic operation covering:**
- Database drivers: MySQL, PostgreSQL, H2 (update to compatible versions)
- ORM frameworks: Hibernate, MyBatis-Plus (update to compatible versions)
- Connection pooling: Druid, HikariCP (update to compatible versions)
- Update deprecated JPA repository methods (`getOne()` → `getReferenceById()`)
- Pagination libraries: PageHelper (update to compatible version)

**Success criteria**: Database connectivity verified. ORM operations work correctly.

---

### Group 4: Core Dependencies
**Goal**: Update foundational libraries as coordinated functional groups.

**Operation A — Apache Commons & Utility Libraries:**
- Apache Commons: `commons-lang3`, `commons-io`, `commons-collections4`, `commons-fileupload`
- Utilities: Netty, Freemarker, Jedis
- HTTP libraries: HttpClient, OkHttp

**Operation B — Serialization & Processing Libraries:**
- Jackson (use version from Mandatory Dependency Versions), FastJSON, Gson
- XML processing: Xerces, Saxon, XMLBeans
- Workflow engines: Flowable

**Success criteria**: Core functionality stable. Project builds without dependency conflicts.

---

### Group 5: Spring Ecosystem Modernization
**Goal**: Modernize the Spring framework as a coordinated unit.

**Critical sequence — do NOT swap these:**

1. **Spring Security configuration first** (if present)
   - Update Spring Security config for new API changes BEFORE Spring Boot upgrade
   - Update authentication/authorization patterns

2. **Complete Spring ecosystem update**
   - Update Spring Boot (to version in Mandatory Dependency Versions) + all Spring dependencies
   - Migrate Swagger to SpringDoc OpenAPI
   - Update `application.properties` / `application.yml` for Spring Boot compatibility
   - Update caching frameworks: Ehcache (if present)

**Success criteria**: Spring Boot application starts and all endpoints function correctly.

---

### Group 6: Final Integration & Verification
**Goal**: Ensure complete system integration and compatibility.

**Operations:**
1. Fix remaining target Java version language compatibility issues
2. Update build plugins to target Java version compatible versions
3. Address deprecated API usage
4. Run the complete test suite
5. Verify end-to-end functionality
6. Document all changes in a validation summary

**Success criteria**: Full application functionality verified. All tests pass.

---

## Critical Sequencing Constraints

### Must Complete Before Next Group
| Group | Gate |
|-------|------|
| 1 | Build tools updated, new Java version compiles |
| 2 | All Jakarta migrations complete, no `javax.*` imports remain |
| 3 | Database connectivity verified |
| 4 | Core libraries functional, no dependency conflicts |
| 5 | Spring Boot starts successfully |
| 6 | Full functionality verified |

### Must Group Together (Atomic Operations)
- Jakarta dependencies + import statements — one coordinated change
- Database drivers + ORM + connection pooling — database ecosystem together
- Spring Security config + Spring Boot upgrade — Spring ecosystem together

### Must Sequence Correctly
- Build tools → Java version changes
- Lombok compatibility → Java version changes
- Complete Jakarta migration → Spring Boot upgrade
- Spring Security configuration → Spring Boot upgrade

---

## Mandatory Dependency Versions

| Dependency | Version |
|------------|---------|
| Gradle wrapper | 8.11+ |
| Maven compiler plugin | 3.0.5 (older Maven) or 3.13.0+ (Maven 3.9.0+) |
| Lombok | 1.18.36+ |
| Jackson | 2.15.2 (LTS) |
| Spring Boot | 3.2.12 (LTS) |
| Jakarta validation-api | 3.0.2 |
| Jakarta servlet-api | 6.0.0 |
| Jakarta persistence-api | 3.1.0 |
| Jakarta annotation-api | 2.1.1 |

---

## Runtime Environment Management

Use the appropriate Java version for each transformation stage:

```bash
# During Groups 1 baseline — use source Java version
mvn clean install   # (with system default or source-appropriate JAVA_HOME)

# During Groups 2–6 — use target Java version
JAVA_HOME=/path/to/target/jdk mvn clean install
```

---

## Group Completion Validation

After each group, confirm:
- Build command passes without errors
- Application starts without errors (where applicable)
- No conflicting or missing dependencies

### Failure Recovery
If a group fails:
1. Revert to the previous group's passing state
2. Identify the specific failure
3. Fix and re-attempt the failed group
4. Document the issue and resolution

---

## Planning Guidance

### How to Scope the Transformation Plan
Generate only the operations needed based on the actual codebase. Skip groups that don't apply.

**Complexity guidelines:**
- Simple (Java version upgrade, minimal deps): 6–10 operations
- Medium (Jakarta migration, DB drivers, utilities): 10–15 operations
- Complex (Spring Boot ecosystem, multiple frameworks, enterprise): 15–25 operations

### Functional Grouping Examples

**Serialization Libraries (group together):**
Jackson + Gson + XStream + Protobuf — data serialization libraries interact and should be tested together.

**Core Utility Libraries (group together):**
Apache Commons (lang3, io, codec, collections4) + Guava + Netty — foundational utilities with minimal interdependencies.

**Database Ecosystem (group together):**
MySQL driver + Hibernate + HikariCP + PageHelper — database components are tested together.

### Anti-Patterns to Avoid
- Splitting Jakarta migration into per-dependency operations — always migrate all Jakarta deps + imports atomically
- Upgrading Spring Boot before completing Jakarta migration
- Running the baseline build with the target Java version instead of the source version

---

## Constraints and Guardrails

1. Keep all tests enabled — resolve failures through proper code fixes, not by disabling tests
2. Upgrade Java version consistently across all modules (no mixed versions)
3. Never downgrade dependency versions from the source baseline
4. Focus modifications exclusively on target Java version compatibility requirements
5. Upgrade APIs only when required for version compatibility
6. Preserve existing import structure and maintain consistent API usage patterns
7. Preserve all existing comments and licensing information without modification
8. Remove any temporary debugging code introduced during transformation before finishing
9. **Baseline establishment (Group 1, Step 1) must use the source Java version, not the target**

---

## Exit Criteria

- Build command completes without errors with the target Java version
- All tests pass with the same or better success rate than the baseline
- No `javax.*` imports remain (except `javax.xml` and `javax.swing`)
- All mandatory dependency versions are updated as specified
- Any skipped or incompatible updates are documented with reasons
