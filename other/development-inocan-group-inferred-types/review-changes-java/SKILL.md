---
name: review-changes-java
description: Systematic code review workflow to evaluate changes against Java and Spring standards. Use when reviewing Pull Requests, commits, or diffs. Ensures robustness, maintainability, and adherence to best practices.
---

# Review Changes (Java/Spring Boot)

Systematic workflow for reviewing Java/Spring code against established standards.

## 1. Understand the Change
- What problem does this solve?
- What is the scope of impact?
- Are tests included and do they cover the use cases?

## 2. Java Best Practices Review
- **Robustness:**
    - Is `try-with-resources` used to close resources?
    - Is exception handling correct?
- **Immutability:**
    - Are fields declared `final` where possible?
    - Could the class be immutable?
- **Types:**
    - Are Raw Types (e.g., `List`) avoided?
    - Is `Optional` used correctly (e.g., `isPresent()` followed by `get()`, or prefer `orElse`, `map`)?
- **Contracts:**
    - If `equals()` is implemented, is `hashCode()` also implemented?
- **Lambdas/Streams:**
    - Is the streams code readable?
    - Are Method References used where possible?
- **Naming:**
    - Clear and descriptive names (no abbreviations)?

## 3. Spring Patterns Review
- **Dependency Injection:**
    - Is injection done via **constructor**? (Avoid `@Autowired` on fields).
- **Configuration:**
    - Is it using `@ConfigurationProperties` (preferred) or `@Value`?
- **Layers:**
    - Is business logic in the `@Service`?
    - Is the `@Controller` only orchestrating the call (no business logic)?
    - Is the `@Repository` called directly by the `Controller`? (Should not be).
- **Transactions:**
    - Is `@Transactional` used correctly (generally on public `Service` methods)?
- **Web:**
    - Is `WebClient` used instead of `RestTemplate`?
- **Security:**
    - Are endpoints secured by Spring Security?
    - Is sensitive data excluded from logs?

## 4. Testing
- **Unit Tests:** Use Mockito correctly?
- **Test Slices:** Is the correct slice used (e.g., `@WebMvcTest`)?
- **Testcontainers:** Is it used for integration tests with a real database?
- **Assertions:** Are assertions clear and testing behavior, not implementation?

## 5. Feedback Format

### Required Changes (Blocking)
- Security vulnerabilities.
- Violations of Java contracts (e.g., equals/hashCode).
- Use of Raw Types.
- Field-based dependency injection.

### Suggested Improvements (Non-blocking)
- Refactoring opportunities (e.g., use Method Reference).
- Naming could be clearer.
- Convert `@Value` to `@ConfigurationProperties`.

### Positive Feedback
- Great use of Testcontainers!
- Good application of the Builder pattern.