---
name: spring-boot-testing
description: >
  Writes and runs tests for Spring Boot applications with the project's
  existing test stack: unit tests, @WebMvcTest/@DataJpaTest slices,
  @SpringBootTest with Testcontainers, coverage and flaky tests. Use when tests
  are requested for Spring Boot code; not for plain Java or JUnit code without
  Spring.
---

# Testing in Spring Boot

Guides writing and running tests in Spring Boot projects with Maven/Gradle.

## Verification ownership

Choose tests from behavior and risk: unit for pure logic, slices for framework boundaries, integration for persistence/security wiring, contracts for independently released services. Reuse `run_tests` and its fresh reports; coordinate with hooks and PR review so unchanged sources are verified once. The test-writer agent should deliver observable assertions, not tests mirroring implementation details.

## Default stack

Inspect the build and existing tests first. Reuse their framework, assertion
library, naming and fixture conventions; the table and examples are options
when the project has no established equivalent. Do not add AssertJ or Mockito
solely to match this guide.

| Layer           | Framework                        | Mocking            |
|-----------------|----------------------------------|--------------------|
| Unit tests      | JUnit Jupiter (JUnit 6 under Boot 4; JUnit 5 under Boot 3) + AssertJ | Mockito |
| Repository      | `@DataJpaTest`                   | —                  |
| Controller      | `@WebMvcTest`                    | REST Test Client / MockMvc + Mockito |
| Integration     | `@SpringBootTest`                | Testcontainers     |
| Contract/API    | Spring Cloud Contract or WireMock | —                 |

Virtual threads are opt-in with `spring.threads.virtual.enabled=true`. Test executor configuration is separate; exercise concurrency-sensitive behavior with the same setting used in production.

For Boot 4 MVC/JPA slices add the relevant test-scoped modular starters (`spring-boot-starter-webmvc-test`, `spring-boot-starter-data-jpa-test`) alongside the project test setup. Testcontainers integration needs `spring-boot-testcontainers`, `org.testcontainers:testcontainers-junit-jupiter` and `org.testcontainers:testcontainers-postgresql` under Boot-managed versions. Import Boot 4 slice annotations from `org.springframework.boot.webmvc.test.autoconfigure` / `org.springframework.boot.data.jpa.test.autoconfigure`; `TestEntityManager` is in `org.springframework.boot.jpa.test.autoconfigure`. Do not copy Boot 3 package names.

## Conventions

### 1. Folder structure

Mirror the source: `src/test/java/com/example/<project>/...`

### 2. Method naming

Keep the project naming style. With no existing convention, one readable option is:

```
should<Expectation>_when<Condition>
```

Example:
```java
@Test
void shouldReturnUser_whenValidId() { ... }

@Test
void shouldThrowNotFound_whenIdDoesNotExist() { ... }
```

### 3. Three A's pattern (Arrange-Act-Assert)

```java
// arrange
var user = new User("fixture@test.com");

// act
var result = userService.findByEmail("fixture@test.com");

// assert
assertThat(result).isPresent();
assertThat(result.get().email()).isEqualTo("fixture@test.com");
```

Use the project assertion library. The example uses AssertJ; JUnit assertions
are equally suitable when they express the required observable result.

### 4. Repository & JPA tests (`@DataJpaTest`)

```java
@DataJpaTest
class UserRepositoryTest {

    @Autowired private UserRepository repository;
    @Autowired private TestEntityManager em;

    @Test
    void shouldPersistAndFindByEmail() {
        var user = em.persistFlushFind(new User("alice@test.com", "Alice"));

        var found = repository.findByEmail("alice@test.com");

        assertThat(found).isPresent();
        assertThat(found.get().getName()).isEqualTo("Alice");
    }
}
```

### 5. Controller tests (`@WebMvcTest`)

Use `MockMvc` for MVC slices, or add `@AutoConfigureRestTestClient` for a MockMvc-backed `RestTestClient`. For a running-server integration test, use `@SpringBootTest(webEnvironment = RANDOM_PORT)` with `@AutoConfigureRestTestClient` (`org.springframework.boot.resttestclient.autoconfigure`, provided by `spring-boot-starter-webmvc-test`). Without that annotation, do not assume a `RestTestClient` bean.

```java
@WebMvcTest(UserController.class)
class UserControllerMockMvcTest {

    @Autowired private MockMvc mockMvc;

    @MockitoBean private UserService userService;

    @Test
    void shouldReturn200_whenSearch() throws Exception {
        given(userService.search(any())).willReturn(Page.empty());

        mockMvc.perform(get("/api/v1/users?size=10"))
               .andExpect(status().isOk())
               .andExpect(jsonPath("$.content").isArray());
    }
}
```

### 6. Integration tests (`@SpringBootTest` + Testcontainers)

For database integration, use the production database engine. The PostgreSQL
Testcontainers example below applies when that is the project database. Use the JUnit Testcontainers extension with static `@Container` fields for class lifecycle.

```java
@SpringBootTest(webEnvironment = RANDOM_PORT)
@Testcontainers
class UserIntegrationTest {

    @Container
    static PostgreSQLContainer postgres = new PostgreSQLContainer("postgres:18-alpine");

    @DynamicPropertySource
    static void datasourceProps(DynamicPropertyRegistry reg) {
        reg.add("spring.datasource.url", postgres::getJdbcUrl);
        reg.add("spring.datasource.username", postgres::getUsername);
        reg.add("spring.datasource.password", postgres::getPassword);
    }

    @Test
    void shouldCreateAndRetrieveUser() { ... }
}
```

Alternatively annotate the container with Boot `@ServiceConnection` and add `spring-boot-testcontainers`; that supplies connection details without `@DynamicPropertySource`. With Testcontainers 2, use `org.testcontainers.postgresql.PostgreSQLContainer` (no generic parameter) and the `testcontainers-postgresql` module; 1.x projects instead use `org.testcontainers.containers.PostgreSQLContainer<?>`.

### 7. Coverage (command)

These commands assume the project defines the coverage profile/property and a JaCoCo verification rule. Neither tool enforces `minCoverage` automatically. Configure the rule first.

```bash
# Maven
./mvnw verify -P coverage -DminCoverage=0.8

# Gradle
./gradlew check -DminCoverage=0.8
```

## AI test generation

Map each requested behavior or reported risk to a trigger, observable result
and appropriate test boundary. A unit test may focus on one class; a slice or
integration test should cover the collaborating behavior when the risk crosses
persistence, security or serialization boundaries. Select normal, boundary and
failure cases when they prove a requirement; do not impose a minimum set of
categories or mirror every implementation branch.

Follow existing fixture, naming and assertion conventions. Reuse test-data
factories or builders where present; helpers such as `aUser()` are examples.
Use observable results, state and required side effects as assertions. Avoid
mocking the configuration or collaborator that implements the behavior being
verified. On hosts without the shipped Claude test-writer agent, apply this
guidance directly and report the behavior covered and any missing prerequisites.

## References

- [Boot Testcontainers service connections](https://docs.spring.io/spring-boot/reference/testing/testcontainers.html)
- [Boot MVC test configuration](https://docs.spring.io/spring-boot/reference/testing/spring-boot-applications.html)
