---
name: spring-boot-3-to-4-migration
description: >
  Guides migration of a Spring Boot 3.x project to 4.x: preparation, the
  OpenRewrite recipe (UpgradeSpringBoot_4_0), Jackson 2→3 changes, Spring
  Framework 7, modular starters, deprecated properties, Testcontainers 2,
  and verification. Use when asked to upgrade/migrate Spring Boot 3 to 4,
  modernize an old project, or diagnose post-migration errors.
---

# Spring Boot 3 → 4 migration

> Verify the project version, official support policy and target release compatibility before planning the migration. Boot 4 uses Spring Framework 7 and requires Java 17+; select a supported patch release and supported JDK.

> **Java baseline:** Spring Boot 4 requires Java 17+ as a minimum, but **Java 25 (LTS) is the recommended target** — it ships final Scoped Values and Stream Gatherers, and virtual threads are fully mature (synchronized-based pinning is fixed since Java 24).

## Migration deliverables and stages

Use `analyze_project` for an evidence-backed inventory: module/root, Boot/Framework/Security/Jackson versions (declared versus resolved), Java/toolchain, starters, BOMs, build plugins, configuration and integrations. Record unsupported third-party dependencies as blockers rather than assuming the rewrite handles them.

Capture a baseline before edits: build/test results, startup/readiness, representative JSON requests/responses (dates, nulls, enums, errors, pagination), authentication/authorization outcomes and database schema/migration state. Preserve snapshots with the existing application revision.

Separate stages: (1) stabilize on the latest 3.5.x (OSS support ended 2026-06-30; commercial support runs to 2032-06-30, verified 2026-11-10) and remove deprecations; (2) mechanical dependencies/imports/configuration; (3) adapt serialization/security/integrations; (4) runtime and consumer compatibility; (5) remove temporary migration tooling. Inspect the diff and run the relevant gate after each stage. Stop on an unresolved compatibility regression; do not combine it with unrelated refactors.

## 1. Preparation

Before touching anything:

1. **Upgrade to the latest 3.5.x** and resolve every deprecation in that version (removed APIs can become build/runtime failures in 4.x):
   Use `run_build` with `task:"dependencies"` to resolve the dependency tree
   and inspect the Spring Boot entries. Capture baseline tests with `run_tests`.
   If MCP is unavailable, use the shared runtime CLI in
   [build/run](../spring-boot-build-run/SKILL.md) with `task:"dependencies"`
   and `task:"test"`. Select the discovered module/profiles explicitly. Do not
   clean by default; use coordinated `run_build` with `task:"clean"` only when
   stale outputs are the demonstrated problem.
2. **Dedicated branch**:
   ```bash
   git checkout -b boot-4-migration
   ```
3. **Inventory** hot spots:
   - Direct use of `com.fasterxml.jackson.*` (custom serialization, mixins, modules).
   - Custom configuration properties (`@ConfigurationProperties`) and extensive YAML.
   - Tests with deprecated annotations and Testcontainers < 2.
   - Removed modular starters (see §3).
   - Flyway/Liquibase declared only as `flyway-core`/`liquibase-core`: Boot 4 needs `spring-boot-starter-flyway` / `spring-boot-starter-liquibase`, otherwise migrations silently stop running at startup.

## 2. Automated recipe (OpenRewrite)

The `org.openrewrite.java.spring.boot4.UpgradeSpringBoot_4_0` recipe does the mechanical work: upgrading the parent to Boot 4.0.x, Spring Framework 7, Spring Security 7, modular starters, renamed properties, BOM migrations, and test annotations. It includes `UpgradeSpringBoot_3_5`. After it, raise Boot to the current supported 4.x line (4.1.x as of 2026-11-10; 4.0.x OSS support ends 2026-12-31) and run `org.openrewrite.java.spring.boot4.SpringBootProperties_4_1`; there is no `UpgradeSpringBoot_4_1` recipe as of 2026-11-10.

```bash
./mvnw -U org.openrewrite.maven:rewrite-maven-plugin:run \
  -Drewrite.recipeArtifactCoordinates=org.openrewrite.recipe:rewrite-spring:<verified-version> \
  -Drewrite.activeRecipes=org.openrewrite.java.spring.boot4.UpgradeSpringBoot_4_0 \
  -Drewrite.exportDatatables=true

# Review in small commits, never one giant diff
git diff --stat
git diff -- pom.xml
git diff -- src/main
```

If the project allows it, temporarily add the properties migrator to detect keys that changed at runtime:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-properties-migrator</artifactId>
    <scope>runtime</scope>
</dependency>
```

Run the app, fix every warning it logs, and **remove it** at the end.

## 3. Structural changes the recipe covers

| Before (3.x)                        | After (4.x)                          |
|-------------------------------------|--------------------------------------|
| `spring-boot-starter-aop`          | `spring-boot-starter-aspectj` (the recipe removes it instead when nothing uses `org.aspectj.lang.annotation`) |
| `spring-boot-starter-web-services` | `spring-boot-starter-webservices`    |
| `spring-boot-starter-web`          | `spring-boot-starter-webmvc` (old name deprecated) |
| `spring-boot-starter-oauth2-resource-server` / `-client` | `spring-boot-starter-security-oauth2-resource-server` / `-client` (the old names still resolve in 4.1.1 as deprecated starters; their POM descriptions say so) |
| `flyway-core` / `liquibase-core` only | `spring-boot-starter-flyway` / `spring-boot-starter-liquibase` |
| Jackson 2 BOM (`jackson-bom.version`) | Jackson 3 is the default; Jackson 2 lives under `jackson-2-bom.version` |
| Testcontainers 1.x                 | Testcontainers 2.x                   |
| Spring Framework 6 / Security 6    | Spring Framework 7 / Security 7      |
| Jakarta EE 10                      | Jakarta EE 11                        |

Other underlying changes:
- **JSpecify**: null-safety is declared throughout the framework. Parameters/methods marked `@Nullable`/non-null may now trigger compiler complaints with `jSpecify` enabled.
- **Virtual threads** remain opt-in (`spring.threads.virtual.enabled=true`); measure the workload and downstream limits before enabling them.
- **Built-in API versioning** in Spring Framework 7 (if you versioned manually with headers, review `/api/v1/**` in your mappings).

## 4. Jackson 2 → 3 (the most treacherous change)

Databind/core packages move from `com.fasterxml.jackson.*` to `tools.jackson.*`; shared Jackson annotations remain in `com.fasterxml.jackson.annotation`. Review the recipe diff rather than blindly replacing all imports. What the recipe does **not** catch:

1. **Serialization defaults changed**: date formats and `null` handling change the shape of the JSON **without a compilation error**. Run the controller tests and compare the JSON output.
2. **Mapper beans and modules**: an application `ObjectMapper` bean no longer replaces Boot's mapper; define a `JsonMapper` bean (`tools.jackson.databind.json.JsonMapper`) or a `JsonMapperBuilderCustomizer` (renamed from `Jackson2ObjectMapperBuilderCustomizer`). `@JsonComponent`/`@JsonMixin` are now `@JacksonComponent`/`@JacksonMixin`. Boot 4 registers every Jackson module on the classpath (`spring.jackson.find-and-add-modules=false` restores explicit registration).
3. **Exceptions are unchecked**: `tools.jackson.core.JacksonException` extends `RuntimeException`, so a `catch (IOException)` around Jackson calls no longer catches parse/serialization failures (and may not compile). Catch `JacksonException` where handling is required.
4. **Deprecated/removed Jackson annotations**: search for `@JsonSerialize`, mixins, and `Module`s registered via configuration.
5. `spring.jackson.use-jackson2-defaults=true` is a temporary bridge to Boot 3 defaults; the `spring-boot-jackson2` module is deprecated and only a stop-gap.
6. If some third-party HTTP client still requires Jackson 2, keep its explicitly required Jackson 2 libraries isolated and let Boot's Jackson 2 dependency management handle their versions where available. Do not replace shared annotations blindly.

## 5. Verification

Use `run_build` with `task:"verify"` for Maven or `task:"check"` for Gradle
after each coherent migration stage. These full gates include the configured
compile/test lifecycle; do not run compile, test and verify consecutively.
For diagnosis, use `run_build` with `task:"compile"` or `run_tests` with the
concrete controller test class in `testClass`. The shared runtime validates
filters: do not pass a shell wildcard such as `*ControllerTest`.

When MCP is unavailable, use the shared runtime CLI and explicit project root
as described in [build/run](../spring-boot-build-run/SKILL.md). Inspect the exit
status, executed/reused scope and fresh test reports. A compile or selected
controller test is not a full gate. Codex users must request verification
explicitly because this plugin's hooks are disabled there.

Startup and OpenRewrite are separate application/migration processes outside
the finite build gate. Start the app only when needed for the requested runtime
checks and stop the instance you started after collecting evidence:

```bash
./mvnw spring-boot:run
# In another terminal, after startup reports readiness:
curl -sf http://localhost:8080/actuator/health | jq .
```

Compatibility evidence must include real endpoint status/headers/body comparisons, readiness and clean startup, security negative cases, transaction/database integration and independently released consumer contracts. Compiling the new imports is insufficient. Document intentional API changes and the consumer migration/rollback plan; do not downgrade an already-applied database migration during rollback.

Final checklist:
- [ ] Zero new deprecations in startup logs
- [ ] `spring-boot-properties-migrator` removed
- [ ] Response JSON identical to pre-migration (or the change documented)
- [ ] Testcontainers running on v2
- [ ] Startup log shows Flyway/Liquibase validating the expected schema version
- [ ] CI pipeline green on the target Java (25 LTS recommended, 17+ minimum)

## 6. If the project is further behind (3.0–3.3)

Migrate step by step: 3.0 → 3.2 → 3.4 → 3.5 → 4.0, using the corresponding recipe at each step (`UpgradeSpringBoot_3_2`, `UpgradeSpringBoot_3_4`, `UpgradeSpringBoot_3_5`, `UpgradeSpringBoot_4_0`). Compile and test between steps. Prefer staged upgrades when they help isolate failures; the sequence depends on dependencies and available recipes.

## References

- [Official Spring Boot 4 migration guide](https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-4.0-Migration-Guide)
- [OpenRewrite Boot 4 recipe](https://docs.openrewrite.org/recipes/java/spring/boot4/upgradespringboot_4_0-community-edition)

Replace `<verified-version>` with an explicit released recipe version before executing; inspect the recipe documentation and changelog for the chosen target.
