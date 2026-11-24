---
name: spring-boot-observability
description: >
  Observability setup for Spring Boot 4.x: Actuator (health, info, metrics,
  prometheus), custom Micrometer metrics, structured logging, tracing with
  Micrometer Tracing + OTel, correlation IDs and evidence-led diagnostics.
  Use when monitoring, health checks, structured logging, tracing, metrics,
  or production diagnostics are requested.
---

# Observability

## Diagnose from a symptom

Use `analyze_project` to identify configured management endpoints and evidence sources. When a local instance is running, `actuator_health` inspects health/readiness/liveness; report the actual HTTP outcome and distinguish DOWN, not-ready, unauthorized, absent and unreachable. A missing direct dependency is not proof that inherited/transitive observability is absent.

| Symptom | Collect | Next discrimination |
|---|---|---|
| App not accepting traffic | startup log, readiness, management/application ports | Startup failure, readiness dependency or wrong address? |
| Restarts | liveness and container exit reason | Process failure/resource limit vs incorrectly included external dependency? |
| Elevated latency | request timer histogram, trace, pool pending, GC/CPU | Local work, queueing or downstream duration? |
| HTTP errors | status distribution and sanitized trace/correlation ID | Auth, validation, timeout or application exception? |

Provide the observation, likely explanation, confidence and next check. Avoid equating correlation with causation. Collect only relevant diagnostics; redact credentials and personal data. Do not fetch `env`, heap dumps or all management endpoints automatically.

## Actuator

### Dependency

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

### Exposed endpoints

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
  endpoint:
    health:
      show-details: when-authorized
```

Protect management endpoints using network controls and a SecurityFilterChain; expose `env` and `loggers` only when explicitly needed and authorized.

### Custom health indicator

```java
import javax.sql.DataSource;
import org.springframework.stereotype.Component;
import org.springframework.boot.health.contributor.Health;
import org.springframework.boot.health.contributor.HealthIndicator;

@Component
public class DatabaseHealthIndicator implements HealthIndicator {
    private final DataSource dataSource;

    public DatabaseHealthIndicator(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    @Override
    public Health health() {
        try (var connection = dataSource.getConnection()) {
            return connection.isValid(5) ? Health.up().build() : Health.down().build();
        } catch (Exception exception) {
            return Health.down(exception).build();
        }
    }
}
```

Boot already supplies a database indicator when appropriate; add this only for a distinct check. Keep dependency checks out of liveness to prevent restart loops.

### Prometheus export

```yaml
management:
  prometheus:
    metrics:
      export:
        enabled: true
```

Add `io.micrometer:micrometer-registry-prometheus`. Endpoint: `/actuator/prometheus`; configure an authenticated/network-restricted scrape path.

## Structured logging

Boot's logging starter includes Logback. Enable Boot's JSON format instead of declaring a nonexistent `logback` artifact:

```yaml
logging:
  structured:
    format:
      console: logstash
```

### Correlation ID

The following servlet filter validates incoming IDs before echoing them and restores MDC after the request:

```java
import java.io.IOException;
import java.util.UUID;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.slf4j.MDC;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

@Component
public class CorrelationIdFilter extends OncePerRequestFilter {
    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response,
            FilterChain chain) throws ServletException, IOException {
        String supplied = request.getHeader("X-Correlation-Id");
        String correlationId = supplied != null && supplied.matches("[A-Za-z0-9._-]{1,64}")
            ? supplied : UUID.randomUUID().toString();
        String previous = MDC.get("correlationId");
        try {
            MDC.put("correlationId", correlationId);
            response.setHeader("X-Correlation-Id", correlationId);
            chain.doFilter(request, response);
        } finally {
            if (previous == null) MDC.remove("correlationId");
            else MDC.put("correlationId", previous);
        }
    }
}
```

Structured logging includes MDC fields. For text logging include `%X{correlationId}`. Async work requires explicit context propagation; prefer tracing's trace/span IDs for distributed calls.

## Tracing (Micrometer Tracing + OpenTelemetry)

For Boot 4 add `org.springframework.boot:spring-boot-starter-opentelemetry` alongside Actuator:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-opentelemetry</artifactId>
</dependency>
```

```yaml
management:
  tracing:
    sampling:
      probability: 0.1
  opentelemetry:
    tracing:
      export:
        otlp:
          endpoint: http://localhost:4318/v1/traces
```

Use Boot-configured HTTP client builders for outgoing propagation. Incoming requests are observed, but only sampled spans are exported. For custom business spans use a Micrometer `Observation` with the injected `ObservationRegistry`. `@WithSpan` alone requires additional instrumentation and is not automatically activated by these dependencies.

## Custom metrics with Micrometer

```java
@Component
public class OrderMetrics {
    private final Counter createdOrders;
    private final Timer placementTime;

    public OrderMetrics(MeterRegistry registry) { // Boot-managed registry, not static Metrics
        this.createdOrders = registry.counter("orders.created");
        this.placementTime = registry.timer("orders.placement.time");
    }

    public void onOrderCreated(Order o) {
        createdOrders.increment();
        placementTime.record(o.getPlacementDuration());
    }
}
```

View them at `/actuator/metrics` or `/actuator/prometheus`.

## Readiness, liveness and logs

```yaml
management:
  endpoint:
    health:
      probes:
        enabled: true
      show-details: when-authorized
```

Probe paths are `/actuator/health/readiness` and `/actuator/health/liveness` unless the management base path changes. Readiness controls traffic; liveness controls restart. Add external dependency checks to readiness only if loss truly makes this instance unable to serve; shared dependency failures can remove every instance from traffic.

Select logs from the application's actual console, service manager, container or configured file. Do not assume fixed paths and do not start a monitor when merely loading this skill. For requested live monitoring start a bounded session with its identified source and stop only that process.

## References

- [Boot structured logging](https://docs.spring.io/spring-boot/reference/features/logging.html#features.logging.structured)
- [Boot tracing starters and OTLP properties](https://docs.spring.io/spring-boot/reference/actuator/tracing.html)
- [Boot endpoints](https://docs.spring.io/spring-boot/reference/actuator/endpoints.html)
