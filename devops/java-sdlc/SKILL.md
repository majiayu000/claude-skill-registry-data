---
name: java-sdlc
description: Complete Java Software Development Lifecycle - project setup, build tools (Maven/Gradle), testing (JUnit, Mockito), Spring Boot, code quality (SonarQube, Checkstyle), security scanning, CI/CD pipelines, and deployment patterns. Use for Java application development from scratch to production.
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Java SDLC Skill

You are a Senior Java Engineer specializing in the complete Software Development Lifecycle. You guide Java projects from initial setup through production deployment with best practices for enterprise-grade applications.

## Core Capabilities

### 1. Project Initialization

**Maven Projects:**
```bash
mvn archetype:generate -DgroupId=com.example -DartifactId=myapp -DarchetypeArtifactId=maven-archetype-quickstart
```

**Gradle Projects:**
```bash
gradle init --type java-application --dsl groovy
```

**Spring Boot Initializr:**
- Web, Data JPA, Security, Actuator, DevTools
- Spring Cloud dependencies
- Testcontainers support

### 2. Build Configuration

**Maven Best Practices:**
```xml
<!-- Parent POM -->
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.2.0</version>
</parent>

<!-- Dependency Management -->
<properties>
    <java.version>21</java.version>
    <maven.compiler.source>21</maven.compiler.source>
    <maven.compiler.target>21</maven.compiler.target>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
</properties>
```

**Gradle Best Practices:**
```groovy
java {
    sourceCompatibility = JavaVersion.VERSION_21
    targetCompatibility = JavaVersion.VERSION_21
}

tasks.withType(JavaCompile) {
    options.compilerArgs += ['--enable-preview']
}
```

### 3. Testing Strategy

**Unit Testing:**
- JUnit 5 (Jupiter)
- Mockito for mocking
- AssertJ for fluent assertions
- Parameterized tests

**Integration Testing:**
- Spring Boot Test
- Testcontainers (DB, Kafka, etc.)
- @SpringBootTest, @WebMvcTest, @DataJpaTest

**Code Coverage:**
- JaCoCo configuration
- Minimum coverage thresholds
- Coverage reports in CI/CD

### 4. Code Quality

**Static Analysis:**
- Checkstyle (Google Java Style)
- SpotBugs for bug patterns
- PMD for code quality
- SonarQube integration

**Code Formatting:**
- Google Java Format
- Spotless Maven plugin
- Pre-commit hooks

### 5. Security

**Dependency Scanning:**
- OWASP Dependency-Check
- Snyk integration
- GitHub Dependabot

**Code Security:**
- SonarQube security hotspots
- SpotBugs security plugin
- OWASP Top 10 compliance

**Secrets Management:**
- Spring Cloud Config
- AWS Secrets Manager integration
- Environment variable usage

### 6. CI/CD Pipelines

**GitHub Actions:**
```yaml
name: Java CI
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          java-version: '21'
          distribution: 'temurin'
          cache: maven
      - run: mvn verify
```

**Pipeline Stages:**
1. Compile
2. Unit tests
3. Integration tests (with Testcontainers)
4. Code quality gates
5. Security scan
6. Build artifact
7. Containerize
8. Deploy

### 7. Deployment Patterns

**Containerization:**
- Multi-stage Dockerfile
- JRE vs JDK runtime
- Layered jars for caching
- Distroless base images

**Kubernetes:**
- Helm charts
- ConfigMaps and Secrets
- Health probes (liveness/readiness)
- Resource limits
- HPA configuration

**Cloud Deployment:**
- AWS ECS/Fargate
- Google Cloud Run
- Azure Container Apps

### 8. Observability

**Logging:**
- SLF4J + Logback/Log4j2
- Structured JSON logging
- MDC for correlation IDs

**Metrics:**
- Micrometer + Prometheus
- Custom metrics
- JVM metrics

**Tracing:**
- Spring Cloud Sleuth
- OpenTelemetry
- Distributed tracing

### 9. API Development

**REST APIs:**
- Spring Web MVC/WebFlux
- OpenAPI/Swagger documentation
- Validation (Bean Validation)
- Exception handling
- HATEOAS

**gRPC:**
- Protocol Buffers
- gRPC server/client
- Streaming

**GraphQL:**
- Spring GraphQL
- Schema first
- Data loaders

### 10. Data Layer

**JPA/Hibernate:**
- Entity design
- Relationships (OneToMany, ManyToMany)
- Pagination
- Specifications
- Query optimization

**Database:**
- Flyway/Liquibase migrations
- Connection pooling (HikariCP)
- Transaction management

**Caching:**
- Caffeine (local)
- Redis (distributed)
- Spring Cache abstraction

## Common Patterns

### Hexagonal Architecture
```
├── domain/          # Core business logic
├── application/     # Use cases
├── infrastructure/  # Adapters
└── api/            # Entry points
```

### Event-Driven
- Spring Events (internal)
- Kafka/RabbitMQ (external)
- Event sourcing with Axon

### CQRS
- Command and Query separation
- Separate read/write models
- Event-driven sync

## Quick Commands

```bash
# Build
mvn clean verify
gradle clean build

# Tests
mvn test
mvn verify -P integration-tests

# Code quality
mvn spotless:apply
mvn checkstyle:check

# Security
mvn dependency-check:check

# Run
mvn spring-boot:run
java -jar target/*.jar
```

## Best Practices Checklist

- [ ] Use Java 17+ (preferably 21 LTS)
- [ ] Enable preview features cautiously
- [ ] Record classes for DTOs
- [ ] Pattern matching for switch/instanceof
- [ ] Virtual threads (Project Loom)
- [ ] Text blocks for multi-line strings
- [ ] Sealed classes for domain modeling
- [ ] Switch expressions
- [ ] Optional instead of null
- [ ] Try-with-resources
- [ ] Method references
- [ ] Streams API appropriately
- [ ] Immutable collections
- [ ] Defensive copying
- [ ] Fail fast validation
