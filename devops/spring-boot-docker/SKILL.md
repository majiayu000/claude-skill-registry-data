---
name: spring-boot-docker
description: >
  Containerize Spring Boot 4.x services with expert-level Dockerfiles and a
  docker-compose for daily local development: multi-stage builds with layered
  jars, dependency layer caching, JVM flags for containers (MaxRAMPercentage,
  virtual threads), non-root runtime, CDS/AOT training runs, healthchecks, and
  compose with Postgres + .env. Use when asked to dockerize, write a
  Dockerfile, docker-compose, optimize image size or startup, or fix
  container behavior.
---

# Docker for Spring Boot

## Scope

This skill owns container images, Compose and container lifecycle. Discover the build through `analyze_project` and reuse the existing build verification; do not repeat builds solely for review. CI publication is owned by the CI skill, and service health diagnosis by observability. Container status alone is not application readiness.


## Dockerfile (multi-stage, layered jar)

Boot supports layered jars: dependencies, spring-boot-loader, application
classes and snapshot dependencies become separate layers, so a code change
rebuilds only the last layer.

**Extract layers in the build stage** (Boot 3.3+ / 4.x uses the `tools` mode):

```dockerfile
# syntax=docker/dockerfile:1

# ── build stage ──────────────────────────────────────────────
FROM maven:3.10-eclipse-temurin-25 AS build
WORKDIR /workspace

# Cache dependencies as their own layer
COPY pom.xml .
COPY .mvn/ .mvn/
COPY mvnw .
RUN --mount=type=cache,target=/root/.m2 ./mvnw -B dependency:go-offline

# Build the jar
COPY src/ src/
RUN --mount=type=cache,target=/root/.m2 ./mvnw -B package -DskipTests

# Extract layered jar into layer directories
RUN cp target/*.jar application.jar
RUN java -Djarmode=tools -jar application.jar extract --layers --destination extracted

# ── runtime stage ────────────────────────────────────────────
FROM eclipse-temurin:25-jre AS runtime
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
RUN useradd --system --home /app --shell /usr/sbin/nologin spring
WORKDIR /app

COPY --from=build /workspace/extracted/dependencies/ ./
COPY --from=build /workspace/extracted/spring-boot-loader/ ./
COPY --from=build /workspace/extracted/snapshot-dependencies/ ./
COPY --from=build /workspace/extracted/application/ ./
USER spring

ENV JAVA_TOOL_OPTIONS="-XX:MaxRAMPercentage=75.0"
ENTRYPOINT ["java", "-jar", "application.jar"]
```

For Gradle, use a separate build stage with the project wrapper; do not run Gradle in the Maven stage. Adjust files for Groovy DSL and multi-module projects:

```dockerfile
FROM eclipse-temurin:25-jdk AS build
WORKDIR /workspace
COPY gradlew build.gradle.kts settings.gradle.kts ./
COPY gradle/ gradle/
COPY src/ src/
RUN --mount=type=cache,target=/root/.gradle ./gradlew --no-daemon bootJar -x test
# Configure bootJar to produce one executable jar; exclude plain jars.
RUN cp build/libs/*-boot.jar application.jar
RUN java -Djarmode=tools -jar application.jar extract --layers --destination extracted
```

Set `tasks.bootJar { archiveClassifier.set("boot") }` in `build.gradle.kts` for that filename glob. The Maven example likewise assumes exactly one executable jar in `target/`; use an explicit artifact name in multi-artifact projects.

### Rules

- **`-Djarmode=tools ... extract`** is the Boot 3.3+/4.x way (`layertools` was
  deprecated in 3.3 and removed in 4.1). Copy the four layer directories in that exact order —
  `application/` last, it is the one that changes most.
- **Never** run as root: end the runtime stage with `USER spring` so later `RUN` steps and the `ENTRYPOINT` run unprivileged. Copied files stay root-owned (read-only for the app) unless `--chown` is used; place root-only steps such as the AOT training run before `USER`.
- **`JAVA_TOOL_OPTIONS`**, not `ENTRYPOINT`-baked flags: lets deployments
  override without rebuilding.
- **`-XX:MaxRAMPercentage=75.0`** instead of fixed `-Xmx`: scales with the
  container memory limit. Never set heap ≥ container limit — the JVM needs
  metaspace, thread stacks and direct buffers beyond the heap.
- **`--mount=type=cache`** for the Maven/Gradle cache beats
  `dependency:go-offline` alone: survives layer invalidation.
- Tag base images by **version**, never `latest` (`eclipse-temurin:25-jre`).
  For stricter supply chain, pin by digest after verifying.

## Faster startup (optional): JVM AOT cache

For Java 25, benchmark an AOT cache using the same extracted layout and JDK as the runtime. Add the training step after copying the layers in the runtime stage and before switching to the non-root user, or grant that user write access to `/app`:

```dockerfile
RUN java -XX:AOTCacheOutput=app.aot -Dspring.context.exit=onRefresh -jar application.jar
ENTRYPOINT ["java", "-XX:AOTCache=app.aot", "-jar", "application.jar"]
```

Training initializes the application context and may access external services; provide isolated training configuration. Fail the image build if training fails. Keep the cache with the same classpath and runtime; measure startup gains rather than promising a multiplier. Spring AOT processing and the JVM AOT cache are distinct optimizations and can be combined after validation.

## .dockerignore

```
.git
.gitignore
.idea/
.vscode/
build/
target/
*.log
.env
.env.*
docker-compose*.yml
README.md
```

## docker-compose.yml (daily local development)

```yaml
services:
  app:
    build: .
    env_file: .env
    environment:
      SPRING_PROFILES_ACTIVE: local
      SPRING_DATASOURCE_URL: jdbc:postgresql://db:5432/app
      SPRING_DATASOURCE_USERNAME: ${POSTGRES_USER}
      SPRING_DATASOURCE_PASSWORD: ${POSTGRES_PASSWORD}
    ports:
      - "8080:8080"
    depends_on:
      db:
        condition: service_healthy
    develop:
      watch:
        - action: rebuild
          path: ./src
    healthcheck:
      test: ["CMD", "curl", "-fs", "http://localhost:8080/actuator/health"]
      interval: 30s
      timeout: 3s
      retries: 3
      start_period: 40s

  db:
    image: postgres:18-alpine
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d app"]
      interval: 5s
      timeout: 3s
      retries: 10

volumes:
  pgdata:
```

`.env` (gitignored) next to it:

```
POSTGRES_USER=dev
POSTGRES_PASSWORD=dev-password
```

`.env.example` committed with the same keys, no real values.

### Rules

- Use **`depends_on` + `condition: service_healthy`** for predictable local startup. Applications also need appropriate connection retries/failure handling because dependencies can restart after startup.
- The app's healthcheck needs **Actuator exposed** at least `health`
  (see the spring-boot-observability skill), and `curl` present in the
  runtime image — install it explicitly in the runtime image when using this HTTP check.
- **`develop.watch`** requires `docker compose up --watch` (Compose 2.25+) or `docker compose watch` (2.22+):
  rebuilds the image on source change. For faster iteration without rebuild,
  run the app with `./mvnw spring-boot:run` on the host and keep only the DB
  in compose — that is the recommended daily loop.
- Environment by profile: compose sets
  `SPRING_PROFILES_ACTIVE=local`; every deployment-specific value arrives via
  env vars (12-factor). Never bake environment-specific values into the image.

## Daily loop (recommended)

```bash
docker compose up -d db            # infrastructure in containers
./mvnw spring-boot:run             # app on the host, fast restarts
```

Full-container mode is for integration checks and CI parity:

```bash
docker compose up --watch          # app + db in containers
docker compose up --build          # clean rebuild
```

## References

- [Spring Boot Dockerfiles and AOT cache](https://docs.spring.io/spring-boot/reference/packaging/container-images/dockerfiles.html)
- [PostgreSQL official image: version 18 data layout](https://github.com/docker-library/docs/blob/master/postgres/README.md)

PostgreSQL 18 changed its data layout. Existing volumes need a planned database upgrade/export and restore; changing the mount alone does not upgrade older database files.
