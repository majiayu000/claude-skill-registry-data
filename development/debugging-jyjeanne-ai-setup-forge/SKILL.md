---
name: debugging
description: Diagnose and resolve Java/Spring Boot bugs, exceptions, and runtime issues using systematic debugging strategies. Use this skill whenever the user shares an error, stack trace, or unexpected behavior in Java/Spring Boot, or says things like "I have an error", "this throws an exception", "my Spring app won't start", "why is this returning null", "getting a 500 error", "my bean is not found", "LazyInitializationException", "transaction not working". Always use this skill to guide systematic diagnosis of any Java or Spring Boot issue.
---

# Java Debugging Skill

Systematically diagnose Java/Spring Boot issues using pattern recognition, stack trace analysis, and targeted investigation strategies.

## Debugging Framework

Always follow this sequence:
1. **Identify**: What type of error is it? (exception type, layer, timing)
2. **Locate**: Where in the stack trace does the problem originate?
3. **Hypothesize**: What are the 2-3 most likely root causes?
4. **Verify**: What log output or code change would confirm/deny each hypothesis?
5. **Fix**: Apply the minimal targeted fix.

---

## Common Spring Boot Exceptions & Solutions

### Application Startup Failures

**`NoSuchBeanDefinitionException`**
```
Caused by: org.springframework.beans.factory.NoSuchBeanDefinitionException:
No qualifying bean of type 'com.example.UserService' available
```
→ Causes & fixes:
- Missing `@Service` / `@Component` annotation → add it
- Class not in component scan path → check `@SpringBootApplication` package
- Interface injected but no implementation → verify impl class has `@Service`
- Multiple implementations without `@Primary` or `@Qualifier` → add qualifier

**`BeanCreationException`**
```
Error creating bean with name 'dataSource': ...
```
→ Causes:
- Missing DB dependency in `pom.xml`
- Wrong DB URL / credentials in `application.yml`
- DB not reachable at startup
→ Check `application.yml`, DB is running, driver on classpath

**`UnsatisfiedDependencyException`**
→ Circular dependency: A → B → A
```java
// Fix with @Lazy on one injection point
public ClassA(@Lazy ClassB classB) { ... }
// Or restructure to remove the cycle
```

---

### Runtime Exceptions

**`NullPointerException`**
```
java.lang.NullPointerException at UserService.java:42
```
→ Debug strategy:
1. Look at line 42 — which object is null?
2. Is it a Spring-injected bean? → check `@Service`/`@Autowired`
3. Is it data from DB? → the entity field may not be loaded (lazy)
4. Is it from a method return value? → check for null return

```java
// Add defensive logging before NPE
log.debug("user={}, user.address={}", user, user != null ? user.getAddress() : "N/A");
```

**`LazyInitializationException`**
```
org.hibernate.LazyInitializationException: failed to lazily initialize a collection
```
→ Cause: accessing lazy collection outside a transaction
→ Fixes (pick one):
```java
// Option 1: Use JOIN FETCH in the query
@Query("SELECT u FROM User u LEFT JOIN FETCH u.orders WHERE u.id = :id")

// Option 2: Use @Transactional on the calling method

// Option 3: Use @EntityGraph
@EntityGraph(attributePaths = "orders")
Optional<User> findById(Long id);

// ❌ DO NOT: open-in-view: true (anti-pattern)
```

**`OptimisticLockException` / `StaleObjectStateException`**
→ Cause: two threads updated the same entity simultaneously
→ Fix:
```java
@Version
private Long version; // Add to entity for optimistic locking

// Handle in service
try {
    return repository.save(entity);
} catch (OptimisticLockException e) {
    throw new ConflictException("Resource was modified by another user, please retry");
}
```

**`DataIntegrityViolationException`**
→ Cause: unique constraint, FK constraint, or NOT NULL violation
→ Debug: read the nested `ConstraintViolationException` message for the constraint name
→ Fix: validate before save, or catch and throw a domain exception:
```java
try {
    return userRepository.save(user);
} catch (DataIntegrityViolationException e) {
    if (e.getMessage().contains("users_email_key")) {
        throw new ConflictException("Email already in use");
    }
    throw e;
}
```

**`TransactionRequiredException`**
→ Cause: modifying entity outside transaction
→ Fix: add `@Transactional` to the service method

---

### HTTP / Controller Issues

**`400 Bad Request` (unexpected)**
→ Check order:
1. `@Valid` on `@RequestBody` parameter?
2. Bean Validation annotations on DTO fields?
3. JSON field names match DTO field names?
4. Correct `Content-Type: application/json` header?

**`404 Not Found` (for existing endpoint)**
→ Check:
1. `@RequestMapping` base path correct?
2. HTTP method matches? (`@GetMapping` vs `@PostMapping`)
3. Path variable name matches: `@PathVariable Long id` vs `/{id}`
4. Context path in `application.yml`?

**`500 Internal Server Error`**
→ Always check the server logs — the stack trace is in the logs, not in the response body (by design)
→ Enable detailed error output for dev:
```yaml
server:
  error:
    include-message: always
    include-binding-errors: always
```

**`HttpMessageNotReadableException`**
→ Jackson can't deserialize the JSON body
→ Check: LocalDate/LocalDateTime needs `@JsonFormat` or Jackson JavaTime module:
```java
@JsonFormat(pattern = "yyyy-MM-dd")
private LocalDate birthDate;
```

---

## Debugging Tools & Techniques

### Enable SQL Logging
```yaml
spring:
  jpa:
    show-sql: true
    properties.hibernate.format_sql: true
logging:
  level:
    org.hibernate.SQL: DEBUG
    org.hibernate.type.descriptor.sql: TRACE  # Show bind parameters
```

### Enable Spring Debug Logging
```yaml
logging:
  level:
    org.springframework.web: DEBUG          # HTTP requests/responses
    org.springframework.security: DEBUG     # Security filter chain
    org.springframework.transaction: DEBUG  # Transaction boundaries
```

### Actuator for Runtime Diagnosis
```java
// Add to pom.xml: spring-boot-starter-actuator
// Check bean context
GET /actuator/beans

// Check env and config
GET /actuator/env

// Check health
GET /actuator/health
```

### Minimal Reproducer Technique
When a bug is hard to isolate:
1. Create a standalone `@SpringBootTest` test that reproduces the issue
2. Remove dependencies one by one until the bug disappears
3. The last removed dependency is the cause

---

## Stack Trace Reading Guide

```
Exception in thread "main" java.lang.NullPointerException    ← Exception type
    at com.example.service.UserService.findUser(UserService.java:42)  ← YOUR code (root cause)
    at com.example.controller.UserController.getUser(UserController.java:28)
    at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)     ← Framework code (ignore)
    ...
```

**Rule**: Find the **first line in YOUR package** — that's where to start investigating.
Ignore framework lines (Spring, Hibernate, JDK) unless your code has no visible lines.
