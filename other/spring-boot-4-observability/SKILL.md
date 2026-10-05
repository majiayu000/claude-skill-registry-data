---
name: spring-boot-4-observability
description: Standardise logging and observability across Spring Boot 4.x / Java 25 microservices. Use when the user asks to "add tracing", "standardise logging", "set up logback", "configure Logstash", "wire MDC", "configure OpenTelemetry", "align observability with the rest of the team", or when introducing a new microservice that must follow the team's logging convention. Assumes Boot 4.x and Java 25 already in place.
---

## Idioma
Responde siempre en castellano.

## Objetivo

Aplicar de forma idéntica en cualquier microservicio Spring Boot 4.x / Java 25 del equipo:

1. **`logback-spring.xml`** con perfil `local` (consola legible) y `!local` (consola + Logstash TCP via `AsyncAppender`).
2. **`MdcRequestFilter`** que mete `requestId` y `path` en el MDC por cada request HTTP.
3. **Métricas Prometheus** etiquetadas con `application=${spring.application.name}`.
4. **Claves MDC homogéneas**: trazas distribuidas (`traceId`, `spanId`) preparadas para activar OpenTelemetry cuando esté Tempo/Jaeger detrás de Grafana.

Premisas: el micro **ya está** en Boot 4.x y Java 25. Si no, aplicar antes la skill `spring-boot-4-pro`.

---

## Phase 1 — Auditoría del estado actual

Antes de tocar nada, comprobar qué ya existe en el proyecto:

```bash
# pom.xml: confirma que hay logstash-logback-encoder
grep -A2 "logstash-logback-encoder" pom.xml

# logback existente
ls src/main/resources/logback*.xml

# Filtros / aspectos / handlers que ya tocan MDC
grep -rn "MDC\.put\|MDC\.clear" src/main/java | head

# Pom: actuator + prometheus
grep -E "spring-boot-starter-actuator|micrometer-registry-prometheus" pom.xml

# Properties: spring.application.name
grep -rn "spring.application.name\|application.name" src/main/resources/*.yml
```

Reportar al usuario:
- Si **falta** `logstash-logback-encoder`, hay que añadirlo.
- Si **falta** `spring.application.name`, no se puede etiquetar Prometheus correctamente — preguntar nombre.
- Si **existe** un `logback-local.xml` huérfano (no referenciado por `logging.config`), señalarlo y proponer borrarlo.
- Si ya hay MDC keys custom (`user`, `businessUnit`, `url`, `request_response_status`, etc.), conservarlas en el encoder JSON.

---

## Phase 2 — Cambios a aplicar

### 2.1 — `pom.xml`

Asegurar las dependencias siguientes (sin versiones explícitas, las gestiona Boot 4):

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>

<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-registry-prometheus</artifactId>
</dependency>

<dependency>
    <groupId>net.logstash.logback</groupId>
    <artifactId>logstash-logback-encoder</artifactId>
    <version>${logstash.version}</version>
</dependency>
```

Property recomendada: `<logstash.version>9.0</logstash.version>`.

### 2.2 — `application.yml` o `bootstrap.yml`

Bloque `management` con tag `application`:

```yaml
management:
  endpoints:
    web:
      base-path: /admin
      exposure:
        include: health, info, prometheus, custom
  metrics:
    tags:
      application: ${spring.application.name}
```

> Si ya existe el bloque `management.endpoints`, fusionar — no duplicar.

### 2.3 — `MdcRequestFilter.java`

Crear en `<basePackage>.config.traces.MdcRequestFilter`. **El nombre del paquete cambia por servicio**, pero el contenido es idéntico:

```java
package <BASE_PACKAGE>.config.traces;

import jakarta.servlet.*;
import jakarta.servlet.http.HttpServletRequest;
import org.slf4j.MDC;
import org.springframework.core.Ordered;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.util.Optional;
import java.util.UUID;

@Component
@Order(Ordered.HIGHEST_PRECEDENCE)
public class MdcRequestFilter implements Filter {

    @Override
    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain)
            throws IOException, ServletException {
        HttpServletRequest httpReq = (HttpServletRequest) req;
        String requestId = Optional.ofNullable(httpReq.getHeader("X-Request-ID"))
                .orElse(UUID.randomUUID().toString());
        try {
            MDC.put("requestId", requestId);
            MDC.put("path", httpReq.getRequestURI());
            chain.doFilter(req, res);
        } finally {
            MDC.clear();
        }
    }
}
```

> ⚠️ Si el servicio tiene **otros filtros** que también ponen claves en MDC (`user`, `businessUnit`, `url`, `request_response_status`...), conservarlos. `MdcRequestFilter` corre con `HIGHEST_PRECEDENCE` y limpia con `MDC.clear()` al final, lo cual borra TODAS las claves — incluidas las añadidas por filtros posteriores. **Eso está bien**: el clear ocurre tras `chain.doFilter()`, así que las claves de los filtros internos se preservan durante el procesamiento del request y se limpian al salir, evitando fugas entre threads del pool.

### 2.4 — `logback-spring.xml`

Crear (o reemplazar) en `src/main/resources/logback-spring.xml`. Plantilla canónica del equipo:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>

    <springProperty scope="context" name="profile" source="spring.profiles.active" defaultValue="local"/>
    <springProperty scope="context" name="appName" source="spring.application.name" defaultValue="<APP_NAME>"/>

    <jmxConfigurator/>

    <property name="LOG_PATTERN"
              value="%d{yyyy-MM-dd HH:mm:ss} [%t] %-5level %logger{36} [req:%X{requestId} path:%X{path}<EXTRA_MDC_PATTERN>] - %msg%n"/>
    <property name="LOGSTASH_DESTINATION" value="${LOGSTASH_DESTINATION:-logstashservice:4564}"/>

    <!-- Console Appender -->
    <appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>${LOG_PATTERN}</pattern>
            <charset>UTF-8</charset>
        </encoder>
    </appender>

    <!-- Logstash TCP Appender -->
    <appender name="LOGSTASH" class="net.logstash.logback.appender.LogstashTcpSocketAppender">
        <destination>${LOGSTASH_DESTINATION}</destination>
        <reconnectionDelay>10 second</reconnectionDelay>
        <keepAliveDuration>5 minutes</keepAliveDuration>

        <encoder class="net.logstash.logback.encoder.LogstashEncoder">
            <customFields>{"program":"${appName}","environment":"${profile}","team":"mirai-mat"}</customFields>
            <!-- Distributed tracing (filled when OpenTelemetry / Micrometer Tracing is enabled) -->
            <includeMdcKeyName>traceId</includeMdcKeyName>
            <includeMdcKeyName>spanId</includeMdcKeyName>
            <!-- Per-request context (MdcRequestFilter) -->
            <includeMdcKeyName>requestId</includeMdcKeyName>
            <includeMdcKeyName>path</includeMdcKeyName>
            <!-- Business context (project-specific MDC keys, keep only those that exist) -->
            <!-- <includeMdcKeyName>user</includeMdcKeyName> -->
            <!-- <includeMdcKeyName>businessUnit</includeMdcKeyName> -->
            <!-- <includeMdcKeyName>url</includeMdcKeyName> -->
            <!-- <includeMdcKeyName>request_response_status</includeMdcKeyName> -->
        </encoder>

        <ringBufferSize>512</ringBufferSize>
    </appender>

    <!-- Async wrapper to keep request threads from blocking on Logstash hiccups -->
    <appender name="ASYNC_LOGSTASH" class="ch.qos.logback.classic.AsyncAppender">
        <appender-ref ref="LOGSTASH"/>
        <queueSize>512</queueSize>
        <discardingThreshold>0</discardingThreshold>
        <includeCallerData>false</includeCallerData>
        <neverBlock>true</neverBlock>
    </appender>

    <!-- Specific loggers -->
    <logger name="org.springframework.cloud.config.client" level="ERROR"/>
    <logger name="org.springframework.boot" level="INFO"/>
    <logger name="org.springframework" level="INFO"/>
    <logger name="org.springframework.security" level="WARN"/>
    <logger name="org.springframework.orm.jpa" level="WARN"/>
    <logger name="org.hibernate" level="WARN"/>
    <logger name="org.springframework.context.support.PostProcessorRegistrationDelegate" level="WARN"/>
    <logger name="io.opentelemetry.exporter.internal.grpc.GrpcExporter" level="OFF"/>

    <!-- Local profile: console only -->
    <springProfile name="local">
        <logger name="<BASE_PACKAGE_DOTTED_PREFIX>" level="DEBUG" additivity="false">
            <appender-ref ref="STDOUT"/>
        </logger>

        <root level="INFO">
            <appender-ref ref="STDOUT"/>
        </root>
    </springProfile>

    <!-- Non-local profiles: console + Logstash -->
    <springProfile name="!local">
        <logger name="<BASE_PACKAGE_DOTTED_PREFIX>" level="DEBUG" additivity="false">
            <appender-ref ref="STDOUT"/>
            <appender-ref ref="ASYNC_LOGSTASH"/>
        </logger>

        <root level="INFO">
            <appender-ref ref="STDOUT"/>
            <appender-ref ref="ASYNC_LOGSTASH"/>
        </root>
    </springProfile>

</configuration>
```

**Reemplazar** los placeholders al aplicar:

| Placeholder | Cómo resolverlo |
|---|---|
| `<APP_NAME>` | Valor de `spring.application.name` (p.ej. `matadminservice`). |
| `<BASE_PACKAGE_DOTTED_PREFIX>` | El prefijo que cubre toda la app — típicamente `com.miraiadvisory.mat` o el equivalente del proyecto. Lee `MatXxxApplication.java` y deduce el paquete raíz. |
| `<EXTRA_MDC_PATTERN>` | Vacío por defecto. Si el servicio ya usa claves MDC custom, añadirlas al pattern de consola. P.ej. ` user:%X{user} BU:%X{businessUnit}`. |
| `<includeMdcKeyName>` adicionales | Descomentar las que se hayan detectado en la auditoría (Phase 1 grep `MDC.put`). |

### 2.5 — Limpieza

- Si existe `logback-local.xml`, `logback.xml` o `logback-test.xml` huérfanos (sin referencia desde `logging.config`), borrarlos.
- Eliminar cualquier `MicrometerConfig.java` que solo añada el tag `application=...` — está cubierto por `management.metrics.tags.application`.
- Confirmar que **no hay `pattern` con `%X{...}` que referencie claves no incluidas en el encoder JSON** (líneas vacías en producción).

---

## Phase 3 — Tests obligatorios

Crear `<basePackage>.config.traces.MdcRequestFilterTest`:

```java
package <BASE_PACKAGE>.config.traces;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.slf4j.MDC;

import java.io.IOException;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class MdcRequestFilterTest {

    private final MdcRequestFilter filter = new MdcRequestFilter();

    @Mock private HttpServletRequest request;
    @Mock private HttpServletResponse response;
    @Mock private FilterChain chain;

    @AfterEach
    void clearMdc() { MDC.clear(); }

    @Test
    void usesIncomingRequestIdAndPath() throws IOException, ServletException {
        when(request.getHeader("X-Request-ID")).thenReturn("incoming-id");
        when(request.getRequestURI()).thenReturn("/users/42");

        doAnswer(invocation -> {
            assertEquals("incoming-id", MDC.get("requestId"));
            assertEquals("/users/42", MDC.get("path"));
            return null;
        }).when(chain).doFilter(request, response);

        filter.doFilter(request, response, chain);

        verify(chain).doFilter(request, response);
        assertNull(MDC.get("requestId"), "MDC must be cleared after filter chain");
        assertNull(MDC.get("path"));
    }

    @Test
    void generatesRequestIdWhenHeaderMissing() throws IOException, ServletException {
        when(request.getHeader("X-Request-ID")).thenReturn(null);
        when(request.getRequestURI()).thenReturn("/users");

        doAnswer(invocation -> {
            String id = MDC.get("requestId");
            assertNotNull(id);
            assertDoesNotThrow(() -> UUID.fromString(id));
            return null;
        }).when(chain).doFilter(request, response);

        filter.doFilter(request, response, chain);
        verify(chain).doFilter(request, response);
    }

    @Test
    void clearsMdcEvenIfChainThrows() {
        when(request.getHeader("X-Request-ID")).thenReturn("rid");
        when(request.getRequestURI()).thenReturn("/x");

        assertDoesNotThrow(() -> {
            try {
                doAnswer(invocation -> { throw new ServletException("boom"); })
                        .when(chain).doFilter(request, response);
                filter.doFilter(request, response, chain);
            } catch (ServletException expected) { /* ok */ }
        });

        assertNull(MDC.get("requestId"));
        assertNull(MDC.get("path"));
    }
}
```

Ejecutar `mvn -B test -Dtest=MdcRequestFilterTest` y comprobar que pasan los 3.

---

## Phase 4 — Activar tracing distribuido (opcional, cuando exista Tempo/Jaeger)

Cuando el equipo monte Grafana Tempo (o Jaeger) y haya un OTLP collector accesible, **basta añadir**:

### 4.1 — `pom.xml`

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-opentelemetry</artifactId>
</dependency>
```

### 4.2 — `application.yml` (o bootstrap)

```yaml
management:
  tracing:
    sampling:
      probability: 1.0   # ajustar en prod (0.05 - 0.1 típico)
  otlp:
    tracing:
      endpoint: ${OTEL_EXPORTER_OTLP_TRACES_ENDPOINT:http://tempo:4318/v1/traces}
```

A partir de ese momento `traceId` y `spanId` se rellenan automáticamente en el MDC por cada request, y el JSON de log los incluirá sin tocar `logback-spring.xml` (ya están listadas en el encoder). En Grafana podrás cruzar **Loki ↔ Tempo** clicando un `traceId`.

> El header de propagación es `traceparent` (W3C Trace Context). Si llamas a otros micros del equipo con `RestClient`/`@HttpExchange`, Spring lo propaga solo. Si usas `WebClient` o cliente HTTP custom, verificar.

---

## Reglas de oro

- **Nunca** dejar `<includeMdcKeyName>` referenciando claves que ningún sitio del código pone — produce ruido vacío en el JSON.
- **Siempre** envolver el `LogstashTcpSocketAppender` en `AsyncAppender` con `neverBlock=true`. Si Logstash cae, el servicio no se debe quedar bloqueado.
- **Siempre** `additivity="false"` en el logger de paquete propio cuando se referencia explícitamente, para evitar duplicación con el `<root>`.
- `logback-spring.xml` (no `logback.xml`) — necesitas `<springProfile>` y `<springProperty>`.
- Ojo con `MDC.clear()` en filtros: si haces clear demasiado pronto, pierdes contexto. Hacerlo siempre en el `finally` del filtro **más externo** (el que tiene `HIGHEST_PRECEDENCE`).
- Las claves MDC custom de cada servicio (`user`, `businessUnit`, `url`...) **no se propagan entre servicios** — son locales. Para correlación cross-servicio se usa `traceId` (Phase 4).

---

## Checklist final

Después de aplicar la skill, comprobar:

- [ ] `mvn clean compile` pasa.
- [ ] `mvn test` con el `MdcRequestFilterTest` en verde.
- [ ] Arrancando con `--spring.profiles.active=local`, los logs salen por consola con el pattern legible y `[req:... path:...]` aparece en cada línea de un request HTTP.
- [ ] Arrancando con cualquier otro perfil, los logs salen también por TCP a `LOGSTASH_DESTINATION` en JSON.
- [ ] `curl /admin/prometheus` (o el endpoint correspondiente) devuelve métricas con tag `application="<spring.application.name>"`.
- [ ] No quedan ficheros `logback*.xml` huérfanos.
- [ ] No hay `MicrometerConfig` redundante.
