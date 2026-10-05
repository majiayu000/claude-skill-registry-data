---
name: logging-patterns
description: Java logging best practices with SLF4J, structured logging (JSON), and MDC for request tracing. Includes AI-friendly log formats for Claude Code debugging. Use when user asks about logging, debugging application flow, or analyzing logs.
---

# Logging Patterns Skill

Effective logging for Java applications with focus on structured, AI-parsable formats.

## When to Use
- User says "add logging" / "improve logs" / "debug this"
- Analyzing application flow from logs
- Setting up structured logging (JSON)
- Request tracing with correlation IDs
- AI/Claude Code needs to analyze application behavior

---

## AI-Friendly Logging

> **Key insight:** JSON logs are better for AI analysis - faster parsing, fewer tokens, direct field access.

### Why JSON for AI/Claude Code?

```
# Text format - AI must "interpret" the string
2026-01-29 10:15:30 INFO OrderService - Order 12345 created for user-789, total: 99.99

# JSON format - AI extracts fields directly
{"timestamp":"2026-01-29T10:15:30Z","level":"INFO","orderId":12345,"userId":"user-789","total":99.99}
```

| Aspect | Text | JSON |
|--------|------|------|
| Parsing | Regex/interpretation | Direct field access |
| Token usage | Higher (repeated patterns) | Lower (structured) |
| Error extraction | Parse stack trace text | `exception` field |
| Filtering | grep patterns | `jq` queries |

### Recommended Setup for AI-Assisted Development

```yaml
# application.yml - JSON by default
logging:
  structured:
    format:
      console: logstash  # Spring Boot 3.4+

# When YOU need to read logs manually:
# Option 1: Use jq
# tail -f app.log | jq .

# Option 2: Switch profile temporarily
# java -jar app.jar --spring.profiles.active=human-logs
```

### Log Format Optimized for AI Analysis

```json
{
  "timestamp": "2026-01-29T10:15:30.123Z",
  "level": "INFO",
  "logger": "com.example.OrderService",
  "message": "Order created",
  "requestId": "req-abc123",
  "traceId": "trace-xyz",
  "orderId": 12345,
  "userId": "user-789",
  "duration_ms": 45,
  "step": "payment_completed"
}
```

**Key fields for AI debugging:**
- `requestId` - group all logs from same request
- `step` - track progress through flow
- `duration_ms` - identify slow operations
- `level` - quick filter for errors

### Reading Logs with AI/Claude Code

When asking AI to analyze logs:

```bash
# Get recent errors
cat app.log | jq 'select(.level == "ERROR")' | tail -20

# Follow specific request
cat app.log | jq 'select(.requestId == "req-abc123")'

# Find slow operations
cat app.log | jq 'select(.duration_ms > 1000)'
```

AI can then:
1. Parse JSON directly (no guessing)
2. Follow request flow via requestId
3. Identify exactly where errors occurred
4. Measure timing between steps

---

## Quick Setup (Spring Boot 3.4+)

### Native Structured Logging

Spring Boot 3.4+ has built-in support - no extra dependencies!

```yaml
# application.yml
logging:
  structured:
    format:
      console: logstash    # or "ecs" for Elastic Common Schema

# Supported formats: logstash, ecs, gelf
```

### Profile-Based Switching

```yaml
# application.yml (default - JSON for AI/prod)
spring:
  profiles:
    default: json-logs

---
spring:
  config:
    activate:
      on-profile: json-logs
logging:
  structured:
    format:
      console: logstash

---
spring:
  config:
    activate:
      on-profile: human-logs
# No structured format = human-readable default
logging:
  pattern:
    console: "%d{HH:mm:ss.SSS} %-5level [%thread] %logger{36} - %msg%n"
```

**Usage:**
```bash
# Default: JSON (for AI, CI/CD, production)
./mvnw spring-boot:run

# Human-readable when needed
./mvnw spring-boot:run -Dspring.profiles.active=human-logs
```

---

## Setup for Spring Boot < 3.4

### Logstash Logback Encoder

**pom.xml:**
```xml
<dependency>
    <groupId>net.logstash.logback</groupId>
    <artifactId>logstash-logback-encoder</artifactId>
    <version>7.4</version>
</dependency>
```

**logback-spring.xml:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>

    <!-- JSON (default) -->
    <springProfile name="!human-logs">
        <appender name="JSON" class="ch.qos.logback.core.ConsoleAppender">
            <encoder class="net.logstash.logback.encoder.LogstashEncoder">
                <includeMdcKeyName>requestId</includeMdcKeyName>
                <includeMdcKeyName>userId</includeMdcKeyName>
            </encoder>
        </appender>
        <root level="INFO">
            <appender-ref ref="JSON"/>
        </root>
    </springProfile>

    <!-- Human-readable (optional) -->
    <springProfile name="human-logs">
        <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
            <encoder>
                <pattern>%d{HH:mm:ss.SSS} %-5level [%thread] %logger{36} - %msg%n</pattern>
            </encoder>
        </appender>
        <root level="INFO">
            <appender-ref ref="CONSOLE"/>
        </root>
    </springProfile>

</configuration>
```

### Adding Custom Fields (Logstash Encoder)

```java
import static net.logstash.logback.argument.StructuredArguments.kv;

// Fields appear as separate JSON keys
log.info("Order created",
    kv("orderId", order.getId()),
    kv("userId", user.getId()),
    kv("total", order.getTotal()),
    kv("step", "order_created")
);

// Output:
// {"message":"Order created","orderId":123,"userId":"u-456","total":99.99,"step":"order_created"}
```

---

## SLF4J Basics

### Logger Declaration

```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Service
public class OrderService {
    private static final Logger log = LoggerFactory.getLogger(OrderService.class);

    // use `log` directly for logging
}
```

### Parameterized Logging

```java
// ✅ GOOD: Evaluated only if level enabled
log.debug("Processing order {} for user {}", orderId, userId);

// ❌ BAD: Always concatenates
log.debug("Processing order " + orderId + " for user " + userId);

// ✅ For expensive operations
if (log.isDebugEnabled()) {
