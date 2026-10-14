---
name: java
description: "Java engineering: records/sealed types, modules, streams, modern concurrency, Maven/Gradle builds, JUnit/Mockito testing. Use for Java work; Spring specifics live in frameworks/spring-boot."
---

# java

Modern Java first: write to the release in the repo, not to remembered Java 8.

## Activate when

- Writing, reviewing, or testing Java code; configuring Maven/Gradle; choosing concurrency or testing approaches.

## Do NOT activate for

- Spring Boot/WebFlux/Security/Data specifics (see frameworks/spring-boot, frameworks/spring-security).

## Procedure

1. Version: detect release from pom.xml/build.gradle (`maven.compiler.release`, `java.version`, toolchain); research behavior in https://docs.oracle.com/en/java/ for THAT release. Records, sealed types, pattern matching, and virtual threads are release-gated — never use without confirming the release supports them.
2. Structure: packages by domain boundary; public API minimal; prefer records for data carriers, sealed hierarchies for closed domains, composition over inheritance.
3. Modern idioms: `Optional` at boundaries (never fields/params boxing), streams for transforms (not for side effects), `java.time` exclusively, `HttpClient` for new HTTP code.
4. Concurrency: executor-based; virtual threads only when the release + workload fit (blocking I/O heavy); shared mutable state guarded or confined; test with concurrent workers.
5. Builds: Maven (pom.xml) or Gradle (Kotlin DSL preferred for new builds); lock/verify dependencies; never commit credentials in settings.
6. Testing: JUnit 5 + Mockito + AssertJ; Testcontainers for real infrastructure; see https://junit.org/junit5/docs/current/user-guide/ and https://site.mockito.org/ for the pinned versions.
7. Errors/logging: typed exceptions at boundaries, no swallowed interrupts (restore flag), structured logging with correlation ids.
8. Verify: `./mvnw verify` or `./gradlew check` green on the pinned JDK; new APIs cross-checked against the release docs.

## Failure modes

- Source/target mismatch across modules; dependency converges to two versions of one lib; tests passing on a newer JDK than CI/prod.

## References
- Registry: `../../research/documentation-search/references/framework-registry.yaml` (java, openjdk, maven, gradle, junit, mockito).
