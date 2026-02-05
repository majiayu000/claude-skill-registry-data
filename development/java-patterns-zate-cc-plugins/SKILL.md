---
name: java-patterns
description: This skill should be used for Java/Spring patterns, dependency injection, streams, Optional, Kotlin, Spring Boot, Maven, Gradle, JVM backend
whenToUse: Java code, Spring Boot, JUnit, Kotlin, .java files, .kt files, Maven, Gradle, JVM backend, Spring framework, Jakarta EE
whenNotToUse: Non-JVM code, Android-specific (use Android docs)
seeAlso:
  - skill: testing-strategies
    when: JUnit test architecture
  - skill: api-design
    when: Spring REST APIs
  - skill: architecture-patterns
    when: Java application structure
---

# Java Patterns

Idiomatic Java/Spring patterns for Java 17+.

## Records

```java
public record User(String name, String email) {}
```

## Optional

```java
Optional.ofNullable(user)
    .map(User::getEmail)
    .orElse("default@example.com");
```

## Streams

```java
List<String> names = users.stream()
    .filter(u -> u.isActive())
    .map(User::getName)
    .collect(Collectors.toList());
```

## Spring Dependency Injection

```java
@Service
public class UserService {
    private final UserRepository repo;

    public UserService(UserRepository repo) {
        this.repo = repo;
    }
}
```

## JUnit 5

```java
@Test
void shouldReturnUser() {
    User user = service.findById(1L);
    assertThat(user.getName()).isEqualTo("test");
}

@ParameterizedTest
@ValueSource(strings = {"a", "b", "c"})
void shouldValidate(String input) {
    assertTrue(validator.isValid(input));
}
```
