---
name: spring-boot-basics
description: Comprehensive guide to Spring Boot fundamentals - auto-configuration, starters, properties, and profiles
sasmp_version: "1.3.0"
bonded_agent: 01-spring-boot-fundamentals
bond_type: PRIMARY_BOND
version: "2.0.0"
updated: "2024-12-30"
---

# Spring Boot Basics Skill

Master Spring Boot fundamentals including auto-configuration, starters, externalized configuration, and profile management.

## Overview

This skill provides comprehensive knowledge for building production-ready Spring Boot applications from scratch.

## Parameters

| Name | Type | Required | Default | Validation |
|------|------|----------|---------|------------|
| `spring_version` | string | ✗ | 3.3.x | Semver format |
| `java_version` | number | ✗ | 21 | 17, 21, or 23 |
| `build_tool` | enum | ✗ | maven | maven \| gradle |
| `packaging` | enum | ✗ | jar | jar \| war |

## Topics Covered

### Core (Must Know)
- **Auto-Configuration**: How Spring Boot auto-configures beans based on classpath
- **Starters**: Pre-configured dependency sets for common scenarios
- **Application Properties**: Externalized configuration with `application.properties/yml`
- **Profiles**: Environment-specific configuration with `@Profile`

### Intermediate
- **Configuration Properties**: Type-safe configuration with `@ConfigurationProperties`
- **Actuator**: Production-ready monitoring and management endpoints
- **Logging**: Logback/Log4j2 configuration and best practices
- **DevTools**: Development-time features for productivity

### Advanced
- **Custom Starters**: Building reusable starter modules
- **Auto-Configuration Classes**: Creating custom auto-configuration
- **Conditional Beans**: `@ConditionalOnProperty`, `@ConditionalOnClass`
- **Native Compilation**: GraalVM native image support

## Code Examples

### Basic Application
```java
@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

### Configuration Properties
```java
@ConfigurationProperties(prefix = "app")
@Validated
public record AppConfig(
    @NotBlank String name,
    @NotNull Database database,
    List<String> allowedOrigins
) {
    public record Database(
        @NotBlank String url,
        String username,
        String password,
        @Min(1) @Max(100) int poolSize
    ) {}
}
```

```yaml
# application.yml
app:
  name: my-service
  database:
    url: jdbc:postgresql://localhost:5432/mydb
    username: ${DB_USER}
    password: ${DB_PASSWORD}
    pool-size: 10
  allowed-origins:
    - http://localhost:3000
    - https://myapp.com
```

### Profile-Specific Configuration
```yaml
# application-dev.yml
spring:
  config:
    activate:
      on-profile: dev
  datasource:
    url: jdbc:h2:mem:devdb

---
# application-prod.yml
spring:
  config:
    activate:
      on-profile: prod
  datasource:
    url: jdbc:postgresql://${DB_HOST}:5432/proddb
```

### Actuator Configuration
```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
  endpoint:
    health:
      show-details: when_authorized
      probes:
        enabled: true
```

## Retry Logic

| Scenario | Max Retries | Backoff | Notes |
|----------|-------------|---------|-------|
| Config server connection | 6 | 1s, 1.5x multiplier | Use `spring.config.import` |
| Database connection | 3 | 2s exponential | Configure in connection pool |

## Troubleshooting

### Failure Modes

| Issue | Diagnosis | Fix |
|-------|-----------|-----|
| Bean not created | Check `@ConditionalOn*` | Run with `--debug` flag |
| Property not binding | Wrong prefix or type | Validate YAML syntax |
| Profile not active | Not set in env | Use `-Dspring.profiles.active` |

### Debug Checklist

```
□ Run with --debug to see auto-configuration report
□ Verify property sources with /actuator/env
□ Confirm active profiles with /actuator/info
□ Check application.yml indentation
```

## Unit Test Template

```java
@SpringBootTest
class ApplicationConfigTest {

    @Autowired
    private AppConfig appConfig;

    @Test
    void shouldLoadConfiguration() {
        assertThat(appConfig.name()).isEqualTo("my-service");
        assertThat(appConfig.database().poolSize()).isEqualTo(10);
    }
}
```

## Usage

```
Skill("spring-boot-basics")
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2024-12-30 | Production-grade with examples, troubleshooting |
| 1.0.0 | 2024-01-01 | Initial release |
