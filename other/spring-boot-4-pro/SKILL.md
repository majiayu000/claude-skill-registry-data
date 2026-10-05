---
name: spring-boot-4-pro
description: Expert in Spring Boot 4.x with Spring Framework 7, Spring Security 7, Jackson 3, Jakarta EE 11, Hibernate 7, JUnit 6, Java 17-25, and the full updated Spring portfolio. Use when working with Spring Boot 4.0+, migrating from Boot 3.x, or needing guidance on the new versions of the Spring ecosystem (Security 7, Data 2025.1, Cloud Northfields, Batch 6, etc.). Also trigger for questions about native API Versioning, HTTP Service Clients, the new OpenTelemetry starter, JSpecify null-safety, starter modularization, or any dependency changes introduced in Boot 4.
---

## Reference Stack — Spring Boot 4.x

| Component | Version in Boot 4.x |
|---|---|
| Spring Boot | 4.0.x / 4.1.x |
| Spring Framework | 7.0.x |
| Spring Security | 7.0.x (includes OAuth2 Authorization Server) |
| Spring Data BOM | 2025.1 |
| Spring Cloud | 2025.0 (Northfields) |
| Spring Integration | 7.0.x |
| Spring Kafka | 4.0.x |
| Spring Batch | 6.0.x |
| Spring LDAP | 4.0.x |
| Spring Session | 4.0.x |
| Spring WS | 5.0.x |
| Spring GraphQL | 2.0.x |
| Spring REST Docs | 4.0.x |
| Spring Modulith | 2.0.x |
| Hibernate | 7.1.x |
| Hibernate Validator | 9.0.x |
| HikariCP | 7.0.x |
| Jackson | **3.0.x** (group: `tools.jackson`) |
| JUnit | **6.0.x** |
| Mockito | 5.20.x |
| Flyway | 11.x |
| Liquibase | 5.0.x |
| Jakarta Persistence | 3.2 |
| Jakarta Servlet | 6.1 |
| Jakarta Validation | 3.1 |
| Testcontainers | 2.x |
| GraalVM | 25+ |
| OpenTelemetry | 1.55+ |
| Groovy | 5.0 |

**Java**: 17 minimum · 21 LTS recommended · 25 supported  
**Gradle**: 8.14+ (9 recommended) · **Maven**: 3.9+

---

## Breaking Changes from Boot 3.x

### Jackson 3 — GroupId change
```xml
<!-- BEFORE (Boot 3.x) -->
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-databind</artifactId>
</dependency>

<!-- NOW (Boot 4.x) -->
<dependency>
    <groupId>tools.jackson.core</groupId>
    <artifactId>jackson-databind</artifactId>
</dependency>
```
- Base package changes from `com.fasterxml.jackson` → `tools.jackson`
- Exception: `jackson-annotations` keeps `com.fasterxml.jackson.core`
- Jackson 2 dependency management is retained for libraries that still require it and can coexist with Jackson 3

### Spring Security 7 — OAuth2 Authorization Server unified
```xml
<!-- OAuth2 Authorization Server now lives inside Spring Security -->
<dependency>
    <groupId>org.springframework.security</groupId>
    <artifactId>spring-security-oauth2-authorization-server</artifactId>
    <version>7.0.x</version> <!-- same maven coordinates, only version changes -->
</dependency>
```
- `SecurityJackson2Modules` → `SecurityJacksonModules` (Jackson 3)
- `AuthorizationManager.check()` → `AuthorizationManager.authorize()`
- `WebSecurityConfigurerAdapter` definitively removed (already deprecated in Boot 3.x)
- Configuration exclusively component-based via `@Bean SecurityFilterChain`

### Jakarta EE 11 — mandatory baseline
- Servlet 6.1 required
- Jakarta Persistence 3.2
- Jakarta Validation 3.1
- No compatibility layers with Jakarta EE 10 or lower

### Hibernate 7
```groovy
// BEFORE
annotationProcessor("org.hibernate:hibernate-jpamodelgen")

// NOW
annotationProcessor("org.hibernate.orm:hibernate-processor")
```
- `hibernate-jpamodelgen` → `hibernate-processor`
- `hibernate-proxool` and `hibernate-vibur` are no longer published
- SQM may generate different SQL than Hibernate 6 — review tests that validate exact SQL strings

### JUnit 6
```xml
<!-- Boot 4 manages JUnit 6 automatically via BOM -->
<dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter</artifactId>
    <scope>test</scope>
</dependency>
```
- JUnit 5 APIs removed or deprecated; migrate to JUnit 6
- `@MockBean` / `@SpyBean` removed (deprecated in 3.4) → use `@MockitoBean` / `@MockitoSpyBean`

### Modularized Starters
```xml
<!-- BEFORE: spring-boot-starter-aop -->
<!-- NOW -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-aspectj</artifactId>
</dependency>

<!-- Security tests now require an explicit starter -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security-test</artifactId>
    <scope>test</scope>
</dependency>
```
- Each technology has its own starter and a `-test` companion
- `spring-boot-starter-test` no longer needs to be declared explicitly; pulled in by starters

---

## New Features in Boot 4.x

### Native API Versioning (no third-party libraries)
```java
// application.properties
spring.mvc.apiversion.enabled=true
spring.mvc.apiversion.header=X-API-Version

// Or via path prefix
spring.mvc.apiversion.path-prefix=/v{version}
```
```java
@RestController
@RequestMapping("/api/orders")
public class OrderController {

    @GetMapping
    @ApiVersion("1")
    public List<OrderV1> getOrdersV1() { ... }

    @GetMapping
    @ApiVersion("2")
    public List<OrderV2> getOrdersV2() { ... }
}
```
For advanced control, define beans of type `ApiVersionResolver`, `ApiVersionParser`, or `ApiVersionDeprecationHandler`.

### HTTP Service Clients — auto-configuration
```java
@HttpExchange(url = "${services.payment.url}")
public interface PaymentClient {

    @PostExchange("/payments")
    PaymentResponse createPayment(@RequestBody PaymentRequest request);

    @GetExchange("/payments/{id}")
    PaymentResponse getPayment(@PathVariable String id);
}
```
Boot 4 auto-configures the client if a `RestClient` bean is present — no manual `@Bean` factory required.

### Unified OpenTelemetry Starter
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-opentelemetry</artifactId>
</dependency>
```
- Auto-configures the full OpenTelemetry SDK
- Exports metrics and traces over OTLP with zero additional configuration
- Replaces the previous piecemeal Micrometer Tracing + OTLP setup

### JSpecify — first-class null-safety
```java
// package-info.java
@NullMarked
package com.example.myapp.domain;

import org.jspecify.annotations.NullMarked;
```
```java
import org.jspecify.annotations.Nullable;

public class UserService {
    public User findById(Long id) { ... }                    // non-null by contract
    public @Nullable User findByEmail(String email) { ... }  // explicitly nullable
}
```
- Spring Framework 7 and Boot 4 use JSpecify internally throughout the codebase
- IntelliJ recognizes it natively for inline warnings

### JmsClient (new API)
```java
@Service
public class OrderMessageService {

    private final JmsClient jmsClient;

    public void sendOrder(Order order) {
        jmsClient.send()
            .toQueue("orders")
            .body(order)
            .send();
    }
}
```
`JmsTemplate` and `JmsMessagingTemplate` remain supported alongside the new API.

### Task Decorator composition
When multiple `TaskDecorator` beans are present, Boot 4 automatically creates a `CompositeTaskDecorator` ordered by `@Order` / `Ordered`. No manual wiring needed.

---

## Spring Security 7 Patterns

### SecurityFilterChain — only valid approach
```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        return http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/public/**").permitAll()
                .requestMatchers("/api/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated()
            )
            .oauth2ResourceServer(oauth2 -> oauth2
                .jwt(jwt -> jwt.decoder(jwtDecoder()))
            )
            .build();
    }

    @Bean
    JwtDecoder jwtDecoder() {
        return NimbusJwtDecoder
            .withJwkSetUri("${spring.security.oauth2.resourceserver.jwt.jwk-set-uri}")
            .build();
    }
}
```

### Jackson 3 + Spring Security
```java
// BEFORE (Boot 3.x)
ObjectMapper mapper = new ObjectMapper();
SecurityJackson2Modules.enableDefaultTyping(mapper);

// NOW (Boot 4.x)
JsonMapper mapper = JsonMapper.builder()
    .addModules(SecurityJacksonModules.getModules(getClass().getClassLoader()))
    .build();
```

---

## Migration Path from Boot 3.x

### OpenRewrite — automates mechanical changes
```xml
<!-- pom.xml -->
<plugin>
    <groupId>org.openrewrite.maven</groupId>
    <artifactId>rewrite-maven-plugin</artifactId>
    <version>6.36.0</version>
    <configuration>
        <activeRecipes>
            <recipe>org.openrewrite.java.spring.boot4.UpgradeSpringBoot_4_0</recipe>
        </activeRecipes>
    </configuration>
    <dependencies>
        <dependency>
            <groupId>org.openrewrite.recipe</groupId>
            <artifactId>rewrite-spring</artifactId>
            <version>6.29.2</version>
        </dependency>
    </dependencies>
</plugin>
```
```bash
mvn rewrite:run
```
The recipe automatically covers:
- `UpgradeSpringBoot_3_5` — removes Boot 3.x deprecations
- `UpgradeSpringFramework_7_0`
- `UpgradeSpringSecurity_7_0`
- `SpringBatch5To6Migration`
- `MigrateToHibernate71`
- `MigrateToModularStarters`
- `ReplaceMockBeanAndSpyBean`
- `Testcontainers2Migration`
- `UpgradeSpringDoc_3_0`

### Recommended migration sequence
1. Upgrade to Boot **3.5.x** first — it deprecates everything removed in 4.0
2. Fix every deprecation compiler warning
3. Run OpenRewrite with `UpgradeSpringBoot_4_0` recipe
4. Review Jackson 3 changes (highest impact on custom serialization)
5. Validate Hibernate queries (SQM may produce different SQL)
6. Update modularized starters and test dependencies
7. Migrate to JUnit 6 and replace `@MockBean` → `@MockitoBean`

---

## Configuration & Observability

### Notable property changes (Boot 4)
```yaml
management:
  observations:
    annotations:
      enabled: true  # @Counted, @Timed with @MeterTag and SpEL support
  health:
    ssl:
      certificate-validity-warning-threshold: 14d
      # REMOVED: WILL_EXPIRE_SOON status — certificates now appear as VALID
      # NEW: expiringChains entry in the health response details
```
See the [Configuration Changelog](https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-4.0-Configuration-Changelog) for the full list.

### OpenTelemetry + Micrometer
```java
@RestController
public class OrderController {

    @GetMapping("/orders/{id}")
    @Timed(value = "order.fetch", description = "Time to fetch an order")
    @Counted(value = "order.fetch.count")
    public Order getOrder(@PathVariable Long id) { ... }
}
```

---

## Testing in Boot 4

### Modularized test dependencies
```xml
<!-- Security tests -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security-test</artifactId>
    <scope>test</scope>
</dependency>

<!-- Testcontainers -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-testcontainers</artifactId>
    <scope>test</scope>
</dependency>
```

### @MockitoBean / @MockitoSpyBean (replaces @MockBean)
```java
@SpringBootTest
class OrderServiceTest {

    @MockitoBean        // replaces @MockBean
    private PaymentClient paymentClient;

    @MockitoSpyBean     // replaces @SpyBean
    private OrderRepository orderRepository;

    @Autowired
    private OrderService orderService;

    @Test
    void shouldProcessPayment() {
        given(paymentClient.createPayment(any())).willReturn(successResponse());
        // ...
    }
}
```

### Testcontainers 2.x with Boot 4
```java
@SpringBootTest
@Testcontainers
class IntegrationTest {

    @Container
    @ServiceConnection
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16");

    // Boot auto-configures DataSource from the container coordinates
}
```

---

## Removed Features

| Feature | Replacement |
|---|---|
| Spock integration | Not yet supported (Groovy 5 incompatible) |
| Spring Session Hazelcast | Managed by Hazelcast team directly |
| Spring Session MongoDB | Managed by MongoDB team directly |
| Embedded launch scripts (fully executable jar) | Use Gradle application plugin |
| Reactive Pulsar auto-configuration | Removed (Spring Pulsar dropped reactive support) |
| SSL status `WILL_EXPIRE_SOON` | Certificates appear as `VALID`; use `expiringChains` |
| Public members in auto-configuration classes | Now package-private (were never public API) |
| `@MockBean` / `@SpyBean` | `@MockitoBean` / `@MockitoSpyBean` |
| `WebSecurityConfigurerAdapter` | `@Bean SecurityFilterChain` |
| `spring-boot-starter-aop` | `spring-boot-starter-aspectj` |

---

## Official Resources

- Release Notes: https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-4.0-Release-Notes
- Migration Guide: https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-4.0-Migration-Guide
- Spring Security 7 Migration: https://docs.spring.io/spring-security/reference/7.0/migration/index.html
- Spring Cloud 2025.0 (Northfields): https://github.com/spring-cloud/spring-cloud-release/wiki/Supported-Versions
- Configuration Changelog: https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-4.0-Configuration-Changelog
- OpenRewrite Boot 4 recipe: https://docs.openrewrite.org/recipes/java/spring/boot4/upgradespringboot_4_0-community-edition
