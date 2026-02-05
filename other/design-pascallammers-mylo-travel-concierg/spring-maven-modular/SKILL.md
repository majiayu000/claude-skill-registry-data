---
name: spring-maven-modular
version: 1.0.0
description: |
  Maven Modular Architecture with profiles for optional components.
  Enable/disable modules like Redis, Kafka, RabbitMQ dynamically.

triggers:
  - "maven"
  - "module"
  - "profile"
  - "dependency"
  - "optional"
---

# Maven Modular Architecture

## Module Flags

| Module | Default | Property |
|--------|---------|----------|
| PostgreSQL | ON | `module.postgresql.enabled` |
| Redis | OFF | `module.redis.enabled` |
| Kafka | OFF | `module.kafka.enabled` |
| RabbitMQ | OFF | `module.rabbitmq.enabled` |
| OAuth2 | OFF | `module.oauth2.enabled` |

## Usage

```bash
# Minimal (PostgreSQL only)
mvn clean install -Pminimal

# With Redis
mvn clean install -Dmodule.redis.enabled=true

# With Kafka
mvn clean install -Dmodule.kafka.enabled=true

# Full stack
mvn clean install -Pfull-stack

# Custom combination
mvn clean install -Dmodule.redis.enabled=true -Dmodule.kafka.enabled=true
```

## Profiles

### Minimal Profile
- PostgreSQL (always)
- JWT Authentication

### Full Stack Profile
- PostgreSQL
- Redis
- Kafka
- OAuth2

## Spring Configuration

Use `@ConditionalOnModuleEnabled` to conditionally load beans:

```java
@Configuration
@ConditionalOnModuleEnabled("redis")
public class RedisConfig {
    // Only loaded when modules.redis.enabled=true
}
```

## application.yml

```yaml
modules:
  postgresql:
    enabled: true
  redis:
    enabled: ${MODULE_REDIS_ENABLED:false}
  kafka:
    enabled: ${MODULE_KAFKA_ENABLED:false}
  rabbitmq:
    enabled: ${MODULE_RABBITMQ_ENABLED:false}
  oauth2:
    enabled: ${MODULE_OAUTH2_ENABLED:false}
```
