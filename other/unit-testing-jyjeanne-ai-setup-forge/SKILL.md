---
name: unit-testing
description: Generate comprehensive unit and integration tests for Java/Spring Boot code using JUnit 5, Mockito, and Spring Boot Test. Use this skill whenever the user wants to write tests, improve test coverage, generate test cases for a class or method, test a Spring service or controller, or says things like "write tests for this", "generate unit tests", "add test coverage", "mock this dependency", "test this service", "write an integration test". Always use this skill for any Java testing task — it defines testing patterns, naming conventions, and coverage strategies.
---

# Java Unit Testing Skill

Generate thorough, maintainable tests for Java/Spring Boot following the AAA pattern, proper mocking strategies, and meaningful assertion coverage.

## Testing Strategy by Layer

### Service Layer → Unit Tests (Pure JUnit 5 + Mockito)

```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private EmailService emailService;

    @InjectMocks
    private UserServiceImpl userService;

    // Tests here
}
```

### Controller Layer → Slice Tests (@WebMvcTest)

```java
@WebMvcTest(UserController.class)
class UserControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private UserService userService;

    @Autowired
    private ObjectMapper objectMapper;

    // Tests here
}
```

### Repository Layer → Slice Tests (@DataJpaTest)

```java
@DataJpaTest
class UserRepositoryTest {

    @Autowired
    private UserRepository userRepository;

    // Tests here - uses in-memory H2
}
```

### Integration Tests → @SpringBootTest

```java
@SpringBootTest
@AutoConfigureMockMvc
@Transactional
class UserIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    // Full stack tests
}
```

## Test Method Naming Convention

Use the pattern: `methodName_stateUnderTest_expectedBehavior`

```java
findById_existingId_returnsUser()
findById_nonExistentId_throwsResourceNotFoundException()
createUser_duplicateEmail_throwsConflictException()
createUser_validRequest_persistsAndReturnsResponse()
deleteUser_adminRole_deletesSuccessfully()
deleteUser_insufficientRole_throwsForbiddenException()
```

## AAA Pattern — Always Follow This Structure

```java
@Test
void findById_existingId_returnsUser() {
    // ARRANGE
    Long userId = 1L;
    User mockUser = User.builder().id(userId).name("Alice").build();
    when(userRepository.findById(userId)).thenReturn(Optional.of(mockUser));

    // ACT
    UserResponse result = userService.findById(userId);

    // ASSERT
    assertThat(result).isNotNull();
    assertThat(result.getId()).isEqualTo(userId);
    assertThat(result.getName()).isEqualTo("Alice");
    verify(userRepository, times(1)).findById(userId);
}
```

## Coverage Checklist

For every method, generate tests for:

- ✅ **Happy path** — normal input, expected output
- ✅ **Not found** — entity doesn't exist → exception thrown
- ✅ **Invalid input** — null, empty, out of range
- ✅ **Duplicate / conflict** — unique constraint violation
- ✅ **Boundary values** — min/max for numeric fields, empty list vs null list
- ✅ **Side effects** — verify `save()`, `delete()`, external service calls
- ✅ **Exception propagation** — when dependency throws, service propagates correctly

## Mockito Patterns

**Stubbing**
```java
when(repo.findById(1L)).thenReturn(Optional.of(entity));
when(repo.save(any(User.class))).thenAnswer(inv -> inv.getArgument(0));
doThrow(new DataIntegrityViolationException("...")).when(repo).save(any());
```

**Verification**
```java
verify(repo, times(1)).save(any(User.class));
verify(emailService, never()).sendWelcomeEmail(any());
verifyNoMoreInteractions(repo);
```

**ArgumentCaptor**
```java
ArgumentCaptor<User> captor = ArgumentCaptor.forClass(User.class);
verify(repo).save(captor.capture());
assertThat(captor.getValue().getEmail()).isEqualTo("alice@test.com");
```

## MockMvc Patterns for Controller Tests

```java
@Test
void createUser_validRequest_returns201() throws Exception {
    CreateUserRequest request = new CreateUserRequest("Alice", "alice@test.com");
    UserResponse response = new UserResponse(1L, "Alice", "alice@test.com");

    when(userService.create(any())).thenReturn(response);

    mockMvc.perform(post("/api/v1/users")
            .contentType(MediaType.APPLICATION_JSON)
            .content(objectMapper.writeValueAsString(request)))
        .andExpect(status().isCreated())
        .andExpect(jsonPath("$.id").value(1L))
        .andExpect(jsonPath("$.name").value("Alice"));
}

@Test
void createUser_invalidEmail_returns400() throws Exception {
    CreateUserRequest request = new CreateUserRequest("Alice", "not-an-email");

    mockMvc.perform(post("/api/v1/users")
            .contentType(MediaType.APPLICATION_JSON)
            .content(objectMapper.writeValueAsString(request)))
        .andExpect(status().isBadRequest())
        .andExpect(jsonPath("$.message").exists());
}
```

## Assertions — Prefer AssertJ over JUnit Assertions

```java
// Prefer AssertJ
assertThat(result).isNotNull();
assertThat(result.getName()).isEqualTo("Alice");
assertThat(list).hasSize(3).extracting(User::getName).containsExactly("A", "B", "C");

// For exceptions
assertThatThrownBy(() -> userService.findById(999L))
    .isInstanceOf(ResourceNotFoundException.class)
    .hasMessageContaining("999");
```

## Test Data Builders

Always suggest a test builder/factory for entities used across multiple tests:

```java
public class UserTestFactory {
    public static User.UserBuilder defaultUser() {
        return User.builder()
            .id(1L)
            .name("Test User")
            .email("test@example.com")
            .active(true)
            .createdAt(LocalDateTime.now());
    }
}
```
