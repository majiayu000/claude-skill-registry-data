---
name: spring-integration-test-wiring
description: Conventions for dependency injection and mocking in Spring Boot integration tests in this project. Use this whenever writing, reviewing, or refactoring integration test classes (anything annotated @SpringBootTest, or under src/test that talks to a real Spring context), especially when deciding how to wire dependencies or mock collaborators. Also consult this before adding @Autowired, @MockBean, @MockitoBean, or field injection in any test class.
---

# Spring Boot Integration Test Wiring for all projects with tests developed in Kotlin

Rules for how dependencies get injected and mocked in this project's integration tests. Apply these whenever creating a
new integration test class or reviewing/editing an existing one.

## 1. Constructor injection only — no field injection (only for Kotlin files .kt)

Integration test classes must wire their dependencies through the constructor, never through `@Autowired` fields.
This skill applies to all modules and submodules of the whole project. This means that all tests made in Kotlin are a
subject of this skill. Only Kotlin files, the ones with the .kt extension should be subject to this change. No other
files should be affected.

**Do:**

```kotlin
@SpringBootTest
class JeorgActionAOPLauncherExtAOPTest @Autowired constructor(
  private val bonitoCatcher: BonitoCatcher,
  private val codCatcher: CodCatcher
) {
}
```

**Don't:**

```kotlin
@SpringBootTest
class JeorgActionAOPLauncherExtAOPTest() {

    @Autowired
    lateinit var bonitoCatcher: BonitoCatcher

    @Autowired
    lateinit var codCatcher: CodCatcher;
}
```

Notes:

- For every file with extension .kt that ends in IT or Test, make sure that if they need `@Autowire` annotated fields or
  params, that they
  get injected via the mentioned above `@Autowired constructor` pattern.
- JUnit 5 + Spring's `TestConstructor` support allows constructor injection in test classes the same way it works in
  production beans. If the project hasn't set `spring.test.constructor.autowire.mode=all` in
  `application-test.properties` (or via `@TestConstructor(autowireMode = ALL)`), the constructor still needs an explicit
  `@Autowired` annotation as shown above — include it only in the constructor and remove it from the fields, or the
  injected params.
- Keep injected fields `private val`.
- If a test only needs one or two collaborators, still use the constructor — don't fall back to field injection "just
  for this one."
- If the `@Autowired constructor` pattern is already in use, make sure that all injected params are `private val`, but
  also remove `@Autowire` if they have it.
- For all beans using any of the annotations `@MockitoBean`, `@MockBean`, `@SpyBean`, `@MockkBean`, `@MockkSpyBean`, or
  others, and injected with `lateinit`, please put them with the correct annotation in the constructor as well

## 2. Replace initMocks with OpenMocks

### Example 1

When finding this:

```kotlin
initMocks(testRestTemplate)
```

Replace with:

```kotlin
openMocks(testRestTemplate)
```

Also replace imports from `import org.mockito.MockitoAnnotations.initMocks` to `import org.mockito.MockitoAnnotations.openMocks`

## 3. Migrate `@MockBean` annotations

The annotation `@MockBean` is deprecated and its usage needs to be replaced by `@MockitoBean`
The annotation `@SpyBean` is deprecated and its usage needs to be replaced by `@MockitoSpyBean`
The above annotations should be updated in the same way following the examples bellow.

### Example 1

On a class level, replace this:

```java
@MockBean(Planet.class)
private MyService myService;
```  
with this:

```java
@MockitoBean(types = Planet.class)
private MyService myService;
```

### Example 2

Replace also the usages of `import org.springframework.boot.test.mock.mockito.MockBean;` with `import org.springframework.test.context.bean.override.mockito.MockitoBean;`

### Example 3
The beans that are declared are like this:

```java
@MockBean
private BankCompanyBankRepository bankCompanyBankRepository;
```

should be replaced to something like:

```java
@MockitoBean
private BankCompanyBankRepository bankCompanyBankRepository;
```

## 4. MockMvc test upgrade for Sprin Boot 4.0.0

Please add:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-webmvc-test</artifactId>
    <scope>test</scope>
</dependency>
```

as a dependency for projects that use `WebMvcTest`

Replace the import: `import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest` to `org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest`


## 5. MockKBean uses different syntax in recent MockK versions

The syntax is slightly changed in the latest Spring MocK versions.

### Example 1

Changes in `MockKBean`

Replace `@MockkBean(classes = [DataSource::class])` with `@MockkBean(types = [DataSource::class])`


## 6. Test class checklist

Before submitting/reviewing an integration test class, confirm:

- [ ] All Spring-managed dependencies come in through the constructor
- [ ] Constructor is annotated `@Autowired` (unless project-wide `TestConstructor` autowire mode is configured)
- [ ] No `@Autowired` on fields
- [ ] Use the new Spring configuration for security
- [ ] New Spring versions don't use `AntPathRequestMatcher` anymore. Make sure none is used
- [ ] No `@MockBean` or `@SpyBean` annotations are used. Use `@MockitoBean` or `@MockitoSpyBean` instead.
- [ ] No `@MockkBean(classes = ` type of declarations left
- [ ] No more usages of `import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest`
