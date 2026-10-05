---
name: check-architecture
description: Architecture validation for Spring Boot 3.x (3.2+) applications — detects layer violations, bean design problems, configuration anti-patterns, and structural drift that causes production failures. Use when reviewing a PR that touches configuration, when a service has grown too large, when beans are being added to existing classes, when Spring Security or transaction configuration changes, or when onboarding to a new module. Also use when code works but "feels wrong" architecturally. This skill catches problems that compile and pass tests but break under load or in edge cases.
---

# Check Architecture Skill

Structural validation for Spring Boot 3.5.x / Java 17-21. Focuses on problems that pass code review but cause production incidents.

## Core Principle

> Code that works is not the same as code that is architecturally sound. Bad architecture compounds — it is cheap to fix now and expensive to fix in production.

---

## Phase 1: Layer Integrity

Spring Boot applications fail in predictable ways when layer boundaries are violated.

### Dependency direction check

```
CORRECT direction:
Controller → Service → Repository → DB
Controller → Service → ExternalClient
                    ↘ DomainModel

VIOLATIONS to detect:
```

```java
// ❌ Repository injected directly into Controller
@RestController
public class UserController {
    @Autowired
    private UserRepository userRepository;  // ← bypasses service layer, no transaction management
}

// ❌ Controller logic in Service
@Service
public class UserService {
    public ResponseEntity<UserDTO> getUser(Long id) {  // ← HTTP concern in business layer
        ...
        return ResponseEntity.notFound().build();
    }
}

// ❌ Entity returned from Controller (exposes internals, breaks serialization)
@GetMapping("/{id}")
public User getUser(@PathVariable Long id) {  // ← should return UserDTO/UserResponse
    return userService.findById(id);
}

// ❌ Business logic in Repository
public interface OrderRepository extends JpaRepository<Order, Long> {
    @Modifying
    @Query("UPDATE Order o SET o.status = 'CANCELLED' WHERE o.userId = :userId AND o.total > 1000")
    void cancelExpensiveOrdersForUser(@Param("userId") Long userId);  // ← business rule in data layer
}
```

### Check: where does each class live conceptually?

```
controller/   → HTTP in, DTO out. No business logic. No direct DB access.
service/      → Business logic. Transactions. Orchestration. No HTTP types.
repository/   → Data access only. No business rules.
model/        → Entities. No Spring annotations except JPA.
dto/          → Records or immutable classes. No JPA annotations.
config/       → @Configuration, @Bean. No business logic.
exception/    → Custom exceptions + @RestControllerAdvice handler.
```

---

## Phase 2: Bean Design Audit

### Scope problems

```java
// ❌ Stateful singleton (default scope) — race condition under concurrent requests
@Service  // singleton by default
public class ReportService {
    private List<String> errors = new ArrayList<>();  // ← shared state across all requests!

    public void process(Request req) {
        errors.clear();  // ← thread-safe? No.
        ...
    }
}

// ✅ Fix: make errors a local variable, or use @Scope("request") if truly request-scoped

// ❌ Prototype bean injected into singleton — prototype created once, never refreshed
@Service  // singleton
public class OrderService {
    @Autowired
    private ShoppingCart cart;  // ← if cart is @Scope("prototype"), this is injected once at startup
}

// ✅ Fix: inject ApplicationContext and call getBean(), or use ObjectProvider<ShoppingCart>
```

### Constructor injection completeness

```java
// ❌ Field injection — hides dependencies, untestable without Spring context
@Service
public class UserService {
    @Autowired private UserRepository userRepository;
    @Autowired private EmailService emailService;
}

// ✅ Constructor injection — dependencies explicit, testable with new UserService(mockRepo, mockEmail)
@Service
public class UserService {
    private final UserRepository userRepository;
    private final EmailService emailService;

    public UserService(UserRepository userRepository, EmailService emailService) {
        this.userRepository = userRepository;
        this.emailService = emailService;
    }
}
```

### Circular dependency detection

```
Flag any service that injects another service that injects back:
UserService → OrderService → UserService  ← circular

Spring Boot 3.x fails fast on circular deps by default (spring.main.allow-circular-references=false)
But check if the codebase has this set to true — it means someone worked around a structural problem.
```

---

## Phase 3: Configuration Audit (Spring Boot 3.5.x)

### Security configuration

```java
// ❌ Deprecated Spring Security 5 style (still compiles in Boot 3.x but wrong)
@Bean
public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    http.authorizeRequests()           // ← deprecated, use authorizeHttpRequests()
        .antMatchers("/public/**")     // ← deprecated, use requestMatchers()
        .permitAll();
    return http.build();
}

// ✅ Spring Security 6 / Boot 3.x style
@Bean
public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    return http
        .authorizeHttpRequests(auth -> auth
            .requestMatchers("/public/**").permitAll()
            .requestMatchers("/api/admin/**").hasRole("ADMIN")
            .anyRequest().authenticated())
        .csrf(AbstractHttpConfigurer::disable)
        .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
        .build();
}

// ❌ Method security not enabled but @PreAuthorize used
// @PreAuthorize annotations silently ignored without:
@Configuration
@EnableMethodSecurity  // ← required in Boot 3.x (replaces @EnableGlobalMethodSecurity)
public class SecurityConfig { }
```

### Configuration properties

```java
// ❌ @Value for grouped properties — fragile, not type-safe
@Value("${app.payment.timeout}")
private int timeout;
@Value("${app.payment.retries}")
private int retries;

// ✅ @ConfigurationProperties — validated, refactorable, IDE-friendly
@ConfigurationProperties(prefix = "app.payment")
@Validated
public record PaymentProperties(
    @Positive int timeout,
    @Min(1) @Max(10) int retries
) {}

// ❌ Properties accessed in @Bean methods via @Value — order-dependent, can fail
@Configuration
public class AppConfig {
    @Value("${app.url}")
    private String url;  // ← might not be resolved yet when @Bean is processed
}
```

### Actuator exposure

```yaml
# ❌ Exposing all endpoints in production
management:
  endpoints:
    web:
      exposure:
        include: "*"   # ← exposes /actuator/env, /actuator/heapdump, /actuator/shutdown

# ✅ Explicit safe exposure
management:
  endpoints:
    web:
      exposure:
        include: health, info, metrics, prometheus
  endpoint:
    health:
      show-details: when-authorized
```

---

## Phase 4: Transaction Architecture

### Service-level transaction design

```java
// ❌ No class-level default — each method needs explicit annotation, easy to forget
@Service
public class OrderService {
    public List<Order> findAll() { ... }          // ← no transaction at all
    @Transactional
    public Order create(OrderRequest req) { ... }
}

// ✅ Class-level readOnly default + override for writes
@Service
@Transactional(readOnly = true)  // ← default for all methods: read-optimized
public class OrderService {
    public List<Order> findAll() { ... }          // ← inherits readOnly

    @Transactional  // ← overrides to readOnly=false for writes
    public Order create(OrderRequest req) { ... }
}

// ❌ @Transactional on private methods — silently ignored by Spring proxy
@Service
public class UserService {
    @Transactional
    private void updateUserInternal(User u) { ... }  // ← no transaction, Spring can't proxy private
}
```

---

## Phase 5: Virtual Threads (Java 21 + Spring Boot 3.2+)

If virtual threads are enabled (`spring.threads.virtual.enabled=true`), check for:

```java
// ❌ synchronized methods/blocks — pin virtual thread to carrier thread, kills scalability
@Service
public class CacheService {
    private final Map<String, Object> cache = new HashMap<>();

    public synchronized Object get(String key) { ... }  // ← thread pinning with virtual threads
    // ✅ Fix: use ConcurrentHashMap + computeIfAbsent, or ReentrantLock
}

// ❌ ThreadLocal used for request context — virtual threads don't inherit ThreadLocal
// (ScopedValue is the Java 21 replacement)
private static final ThreadLocal<RequestContext> context = new ThreadLocal<>();
// ← With virtual threads: check if MDC, SecurityContext, or custom ThreadLocals are used correctly

// ❌ Blocking operations held without yielding
// Virtual threads handle blocking I/O well, but synchronized + blocking = pinning
```

---

## Output Format

```markdown
## Architecture Review: [Module / PR / Class]

### Layer Violations
| Location | Violation | Severity | Fix |
|----------|-----------|----------|-----|
| UserController.java:34 | Direct UserRepository injection | HIGH | Inject UserService instead |
| OrderService.java:67 | Returns ResponseEntity | MEDIUM | Return domain object, let controller wrap |

### Bean Design Issues
- **Stateful singleton** (ReportService.java): `errors` field is shared state — race condition under load
- **Field injection** (PaymentService.java): 4 fields use @Autowired — convert to constructor injection

### Configuration Issues
- **Deprecated Security API** (SecurityConfig.java): authorizeRequests() + antMatchers() — migrate to Boot 3.x API
- **@EnableMethodSecurity missing**: @PreAuthorize found in 3 services but annotation not enabled — silently ignored

### Transaction Architecture
- **No class-level @Transactional** (UserService.java): 6 read methods run without transaction
- **Private @Transactional** (OrderService.java:89): annotation on private method — no effect

### Virtual Threads (if enabled)
- **synchronized block** (CacheService.java:23): thread pinning risk — replace with ReentrantLock or ConcurrentHashMap

### Overall Assessment: [SOUND / NEEDS WORK / CRITICAL ISSUES]

### Priority fixes before merge:
1. [Highest risk item]
2. ...

### Technical debt to schedule:
- [Items that work now but should be addressed in next sprint]
```

---

## Quick Architecture Checklist

| Area | Check |
|------|-------|
| Layers | Controllers don't access repositories directly |
| Layers | Services don't return HTTP types |
| Layers | Entities don't leak out of service layer |
| Beans | Constructor injection everywhere |
| Beans | No stateful singletons |
| Config | Spring Security 6 API (not deprecated 5 style) |
| Config | @EnableMethodSecurity if @PreAuthorize used |
| Config | @ConfigurationProperties for grouped config |
| Transactions | Class-level @Transactional(readOnly=true) on services |
| Transactions | @Transactional not on private methods |
| Virtual threads | No synchronized if spring.threads.virtual.enabled=true |
| Actuator | Not exposing * in production |
