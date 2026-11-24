---
name: spring-boot-build-run
description: >
  Guides compilation, running, profiles and dependency/build troubleshooting in Spring Boot projects with Maven or
  Gradle. Use when a Spring Boot application must be built or run, a build or
  startup failure diagnosed, profiles switched or dependencies added/removed.
  Not for non-Spring Java builds; runtime health, log and trace diagnosis
  belongs to spring-boot-observability.
---

# Build & Run in Spring Boot

Guides compilation, execution, profile configuration, logs, and dependency management in Spring Boot.

> Read the project's Boot and Java versions first and keep them. The Java 25 / Boot 4 snippets below apply to new projects or projects already on that line. Spring Boot 4.1.2 requires Java 17+ and is compatible up to Java 27 (verified 2026-11-10); check the system requirements of the selected patch release.

## Discover once, execute once

Start with `analyze_project` when MCP is available: identify root, build system, wrapper, modules and Java target from evidence. Select the project/module before running a build. Prefer the repository wrapper; fallback to an installed tool only when no wrapper exists. A wrapper is executable project code, so use trusted repositories.

Use MCP `run_build` for finite compile/package/verify tasks and `run_tests` for test execution and fresh reports. Both share discovery and execution coordination with hooks. Pass the tool's documented module/profile options rather than constructing shell commands. A profile changes configuration and dependencies; inspect its definition first. A module's relative path is distinct from a Maven artifact selector or Gradle task prefix.

On Codex, this plugin disables its Claude hooks and does not register Claude agents or the Java LSP. After relevant edits, explicitly call `run_build` for the full verification gate and inspect the result before reporting success; there is no automatic Stop verification. Use the actual application workspace as the session cwd, not the installed plugin directory. `analyze_project` must identify the intended application before a build.

When MCP is unavailable, use the shared CLI below for finite builds. It accepts JSON on stdin and returns discovery/command/result evidence. The runtime coordinates locks and input fingerprints with MCP/hooks. Only an unchanged successful full-root default `verify` (Maven) or `check` (Gradle) can satisfy the full verification gate; a compile, selected test, module or profile run cannot. Batch edits before compiling. A failed build must be diagnosed before repeating it; do not clean by default or run compile, package and verify consecutively when verify already covers the needed lifecycle.

## Common commands

### Compile

Compiler setup for a Java 25 project (adapt to the project's release; no explicit maven-compiler-plugin version needed, Boot's parent manages it):

```xml
<!-- Maven: pom.xml properties -->
<properties>
    <java.version>25</java.version>
</properties>
```

```gradle
// Gradle: build.gradle
java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(25)
    }
}
```

```bash
# Claude Code writes the plugin directory into the value below when this skill
# loads; the shell environment has no plugin-root variable. Codex performs no
# substitution: replace the value with the absolute plugin directory (two
# levels above this skill folder), or skip this line when an absolute
# SBT_PLUGIN_ROOT is already exported (codex/run.mjs sets it for its child
# process). Single quotes make an unreplaced value fail visibly.
SBT_PLUGIN_ROOT='${CLAUDE_PLUGIN_ROOT}'
# Identify root/tool/wrapper/modules; paths in these JSON examples are illustrative.
python3 "${SBT_PLUGIN_ROOT}/runtime/project_runtime.py" <<'JSON'
{"action":"discover","projectRoot":"/path/to/project"}
JSON
# Compile using discovery, process coordination and evidence capture.
python3 "${SBT_PLUGIN_ROOT}/runtime/project_runtime.py" <<'JSON'
{"action":"run","projectRoot":"/path/to/project","task":"compile"}
JSON
# Full verification; reuse only an equivalent successful unchanged full gate.
python3 "${SBT_PLUGIN_ROOT}/runtime/project_runtime.py" <<'JSON'
{"action":"run","projectRoot":"/path/to/project","task":"verify"}
JSON
# Maven-only profile, selected discovered module; this is not the full gate.
python3 "${SBT_PLUGIN_ROOT}/runtime/project_runtime.py" <<'JSON'
{"action":"run","projectRoot":"/path/to/project","task":"package","module":"service","profiles":["integration"],"reuse":false}
JSON
```

`task` aliases map compile/test-compile/package/verify to the discovered build system. Maven profiles are rejected for Gradle: use its declared project configuration instead. To deliberately rerun a full verification, set `reuse:false`. Inspect `ok`, `exitCode`, `timedOut`, `outputLimitExceeded` and captured output; receiving JSON alone does not mean success.

When called directly from a shell, the runtime CLI runs the build in its own session. To cancel a run, send TERM, INT or HUP to the runtime process, which then ends the build tree. A SIGKILL sent to the shell's process group is not forwarded to that session. On Linux the build also ends if the runtime process dies; on macOS it can outlive the runtime until its own timeout.

### Run

```bash
# Default profile (or the project-configured default)
./mvnw spring-boot:run                # Maven
./gradlew bootRun                     # Gradle

# With a specific profile
./mvnw spring-boot:run -Dspring-boot.run.profiles=local
SPRING_PROFILES_ACTIVE=local ./gradlew bootRun

# With extra arguments
./mvnw spring-boot:run -Dspring-boot.run.arguments="--server.port=8081"
```

### Profiles

| File                             | When it loads                        |
|----------------------------------|--------------------------------------|
| `application.yml`                | Always (base)                        |
| `application-dev.yml`            | `spring.profiles.active: dev`        |
| `application-local.yml`          | Profile `local`; `dev` is separate unless grouped      |
| `application-staging.yml`        | Profile `staging`                    |
| `application-production.yml`     | Profile `production`                 |

Convention: do not commit `application-local.yml` (gitignored). Each developer keeps their own local properties.

### Startup failures

Inspect the actual console/service/container output and configured log source. Do not introduce a logging configuration merely to diagnose a build or startup failure.

For a known configured file, inspect relevant errors:
```bash
# Follow the log in the console
rg ERROR logs/spring.log

# If a separate HTTP access-log file is explicitly configured:
tail -n 100 logs/http-trace.log
```

A profile file activates only when its named profile is active. To activate both explicitly, use `SPRING_PROFILES_ACTIVE=dev,local`; later profiles override earlier ones for conflicting properties. The default command above does not activate `dev` unless the project configured it.

### Common dependencies

```xml
<!-- Maven: example version; keep API and processor aligned -->
<dependency>
    <groupId>org.mapstruct</groupId>
    <artifactId>mapstruct</artifactId>
    <version>1.6.3</version>
</dependency>
```

```gradle
// Gradle: add to build.gradle
implementation 'org.mapstruct:mapstruct:1.6.3'
annotationProcessor 'org.mapstruct:mapstruct-processor:1.6.3'
```

Maven also needs `org.mapstruct:mapstruct-processor:1.6.3` under the compiler plugin `annotationProcessorPaths` (especially with Java 23+). If Lombok is used, configure its processor and `lombok-mapstruct-binding` too.

**Dependency management commands:**

```bash
# Maven: dependencies with available updates (versions plugin)
./mvnw versions:display-dependency-updates
./mvnw versions:display-plugin-updates

# Gradle (requires the ben-manes/gradle-versions-plugin)
./gradlew dependencyUpdates

# Show the dependency tree for a library
./mvnw dependency:tree -Dincludes=org.springframework:spring-web
./gradlew dependencies --configuration runtimeClasspath
```

### Common troubleshooting

| Symptom                     | Typical cause                                | Fix                         |
|-----------------------------|----------------------------------------------|-----------------------------|
| Port already in use         | Another instance running                     | Inspect the owning process; stop only the intended app |
| Bean not found              | Component not scanned                        | Check `@ComponentScan`      |
| DB connection refused       | Endpoint/credentials/network or container not ready                   | Inspect configured JDBC target and connectivity                |
| CORS error                  | Missing `@CrossOrigin` or `allowed-origins`  | Enable `http.cors(...)` with a `CorsConfigurationSource` bean named `corsConfigurationSource` (see security hardening) |
| Unexplained 401             | Expired or malformed JWT                     | Check issuer, audience, signing keys and token expiry          |

For container workflows use [Docker](../spring-boot-docker/SKILL.md), pipeline design [CI](../spring-boot-ci/SKILL.md), and runtime health/log/trace diagnosis [observability](../spring-boot-observability/SKILL.md). Build/run owns commands and startup failures; those skills own their domain configuration.

## References

- [Boot logging properties](https://docs.spring.io/spring-boot/reference/features/logging.html)
- [MapStruct installation and annotation processing](https://mapstruct.org/documentation/installation/)
